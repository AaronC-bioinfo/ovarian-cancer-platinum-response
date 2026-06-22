"""
ablation.py
───────────
Methods-critique analysis: quantifies how much reported ROC-AUC is inflated by
(a) computing variance-based feature selection on the FULL dataset before
    the train/test split (the classic genomics leakage bug), and
(b) reporting performance from a single train/test split instead of
    repeated/nested cross-validation.

This module does NOT require any new data — it re-runs the existing
pipeline under controlled conditions and reports the delta.

Usage:
    from src.ablation import run_leakage_ablation, run_split_variance_ablation
    results = run_leakage_ablation(expr, labelled_dict, cfg)
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

from .models import get_all_models, train_model
from .preprocessing import align_expression_to_labels

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Leakage ablation: full-data variance selection vs. train-only selection
# ─────────────────────────────────────────────────────────────────────────────


def _select_top_variance(X: pd.DataFrame, top_n: int) -> pd.Index:
    return X.var(axis=0).nlargest(top_n).index


def _select_top_f_score(X: pd.DataFrame, y: np.ndarray, top_n: int) -> pd.Index:
    """
    Select the top_n genes by univariate ANOVA F-score against the label.

    This is a SUPERVISED feature selection method — unlike variance filtering,
    it directly uses y, which is exactly the channel through which leakage
    causes severe overoptimism when computed on the full dataset before
    splitting (a well-documented failure mode in genomics ML literature,
    distinct from the much milder effect of unsupervised filtering).

    Real RSEM expression data can contain NaN values (e.g. a gene with a
    missing measurement in some samples) — sklearn's f_classif cannot
    handle NaN and raises on real data even though clean synthetic test
    fixtures never exercise this path. Filled defensively with 0 here.
    """
    from sklearn.feature_selection import f_classif

    X_filled = X.fillna(0)
    f_scores, _ = f_classif(X_filled, y)
    f_scores = pd.Series(f_scores, index=X.columns).fillna(0)
    return f_scores.nlargest(top_n).index


def run_leakage_ablation(
    expr: pd.DataFrame,
    labelled_dict: dict[int, pd.DataFrame],
    cfg: dict[str, Any],
    n_repeats: int = 30,
) -> pd.DataFrame:
    """
    Compare test-set AUC when gene-variance feature selection is computed:
      (A) LEAKY    — on the full dataset (train + test) before splitting
      (B) CORRECT  — on the training split only

    Repeats the train/test split `n_repeats` times with different random
    seeds to produce a distribution of AUCs for each condition, so the
    difference can be reported with a mean and standard deviation rather
    than a single anecdotal number.

    Args:
        expr:          Clean expression matrix (genes × patients).
        labelled_dict: Output of build_labelled_survival — {threshold: df}.
        cfg:           Project config dict.
        n_repeats:     Number of random train/test splits per condition.

    Returns:
        Tidy DataFrame with columns [threshold, model, condition, auc, seed].
    """
    top_n = cfg["features"]["top_n_genes"]
    test_size = cfg["model"]["test_size"]
    base_seed = cfg["project"]["seed"]

    rows = []

    for thr, labelled in labelled_dict.items():
        X, y = align_expression_to_labels(expr, labelled)

        for rep in range(n_repeats):
            seed = base_seed + rep

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=seed, stratify=y
            )

            # ── Condition A: LEAKY — variance computed on full X before split ──
            leaky_genes = _select_top_variance(X, top_n)
            Xtr_leaky, Xte_leaky = X_train[leaky_genes], X_test[leaky_genes]

            # ── Condition B: CORRECT — variance computed on X_train only ──
            correct_genes = _select_top_variance(X_train, top_n)
            Xtr_correct, Xte_correct = X_train[correct_genes], X_test[correct_genes]

            for condition, (Xtr, Xte) in {
                "leaky_full_data_variance": (Xtr_leaky, Xte_leaky),
                "correct_train_only_variance": (Xtr_correct, Xte_correct),
            }.items():
                scaler = StandardScaler()
                Xtr_sc = scaler.fit_transform(Xtr)
                Xte_sc = scaler.transform(Xte)

                models = get_all_models(cfg)
                for name, model in models.items():
                    fitted = train_model(model, Xtr_sc, y_train)
                    y_prob = fitted.predict_proba(Xte_sc)[:, 1]
                    auc = roc_auc_score(y_test, y_prob)

                    rows.append(
                        {
                            "threshold_m": thr,
                            "model": name,
                            "condition": condition,
                            "auc": auc,
                            "seed": seed,
                        }
                    )

        logger.info("Leakage ablation complete for %d-month threshold.", thr)

    return pd.DataFrame(rows)


def summarize_leakage_ablation(ablation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate the raw ablation results into a mean ± std summary table,
    plus the AUC inflation (leaky − correct) per model/threshold.

    Args:
        ablation_df: Output of run_leakage_ablation.

    Returns:
        Summary DataFrame with columns [threshold_m, model, leaky_auc_mean,
        leaky_auc_std, correct_auc_mean, correct_auc_std, auc_inflation].
    """
    summary = (
        ablation_df.groupby(["threshold_m", "model", "condition"])["auc"]
        .agg(["mean", "std"])
        .reset_index()
        .pivot(index=["threshold_m", "model"], columns="condition", values=["mean", "std"])
    )
    summary.columns = ["_".join(c) for c in summary.columns]
    summary = summary.reset_index()

    summary["auc_inflation"] = (
        summary["mean_leaky_full_data_variance"] - summary["mean_correct_train_only_variance"]
    )

    return summary.sort_values(["threshold_m", "model"]).round(4)


# ─────────────────────────────────────────────────────────────────────────────
# Supervised feature-selection leakage (contrast condition)
# ─────────────────────────────────────────────────────────────────────────────


def run_supervised_leakage_ablation(
    expr: pd.DataFrame,
    labelled_dict: dict[int, pd.DataFrame],
    cfg: dict[str, Any],
    n_repeats: int = 30,
) -> pd.DataFrame:
    """
    Same design as run_leakage_ablation, but using SUPERVISED feature
    selection (ANOVA F-score against y) instead of unsupervised variance
    filtering. This is the contrast condition: leakage is expected to be
    substantially larger here, because F-score selection directly uses
    label information from the held-out fold when computed on the full
    dataset before splitting.

    Args:
        expr:          Clean expression matrix (genes × patients).
        labelled_dict: Output of build_labelled_survival — {threshold: df}.
        cfg:           Project config dict.
        n_repeats:     Number of random train/test splits per condition.

    Returns:
        Tidy DataFrame with columns [threshold, model, condition, auc, seed],
        directly comparable to run_leakage_ablation's output (same schema,
        condition labels prefixed with 'supervised_').
    """
    top_n = cfg["features"]["top_n_genes"]
    test_size = cfg["model"]["test_size"]
    base_seed = cfg["project"]["seed"]

    rows = []

    for thr, labelled in labelled_dict.items():
        X, y = align_expression_to_labels(expr, labelled)
        y_arr = np.asarray(y)

        for rep in range(n_repeats):
            seed = base_seed + rep

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=seed, stratify=y
            )

            # ── LEAKY: F-score computed on full X, y before splitting ──
            leaky_genes = _select_top_f_score(X, y_arr, top_n)
            Xtr_leaky, Xte_leaky = X_train[leaky_genes].fillna(0), X_test[leaky_genes].fillna(0)

            # ── CORRECT: F-score computed on training fold only ──
            correct_genes = _select_top_f_score(X_train, y_train, top_n)
            Xtr_correct, Xte_correct = X_train[correct_genes].fillna(0), X_test[correct_genes].fillna(0)

            for condition, (Xtr, Xte) in {
                "supervised_leaky_full_data_fscore": (Xtr_leaky, Xte_leaky),
                "supervised_correct_train_only_fscore": (Xtr_correct, Xte_correct),
            }.items():
                scaler = StandardScaler()
                Xtr_sc = scaler.fit_transform(Xtr)
                Xte_sc = scaler.transform(Xte)

                models = get_all_models(cfg)
                for name, model in models.items():
                    fitted = train_model(model, Xtr_sc, y_train)
                    y_prob = fitted.predict_proba(Xte_sc)[:, 1]
                    auc = roc_auc_score(y_test, y_prob)

                    rows.append(
                        {
                            "threshold_m": thr,
                            "model": name,
                            "condition": condition,
                            "auc": auc,
                            "seed": seed,
                        }
                    )

        logger.info("Supervised leakage ablation complete for %d-month threshold.", thr)

    return pd.DataFrame(rows)


def summarize_supervised_leakage_ablation(ablation_df: pd.DataFrame) -> pd.DataFrame:
    """Same aggregation as summarize_leakage_ablation, for the supervised contrast."""
    summary = (
        ablation_df.groupby(["threshold_m", "model", "condition"])["auc"]
        .agg(["mean", "std"])
        .reset_index()
        .pivot(index=["threshold_m", "model"], columns="condition", values=["mean", "std"])
    )
    summary.columns = ["_".join(c) for c in summary.columns]
    summary = summary.reset_index()

    summary["auc_inflation"] = (
        summary["mean_supervised_leaky_full_data_fscore"]
        - summary["mean_supervised_correct_train_only_fscore"]
    )

    return summary.sort_values(["threshold_m", "model"]).round(4)


# ─────────────────────────────────────────────────────────────────────────────
# Statistical significance of the leakage effect
# ─────────────────────────────────────────────────────────────────────────────


def test_leakage_significance(
    ablation_df: pd.DataFrame,
    leaky_condition: str | None = None,
) -> pd.DataFrame:
    """
    Paired significance test of leaky vs. correct AUC, per model/threshold.

    Each repeat (seed) produces one leaky AUC and one correct AUC from the
    SAME train/test split — only the feature-selection condition differs —
    so a paired test (Wilcoxon signed-rank, with paired t-test as a
    cross-check) is the statistically appropriate choice over an unpaired
    test, and is more powerful for detecting small, consistent effects.

    Args:
        ablation_df:     Output of run_leakage_ablation OR
                         run_supervised_leakage_ablation (any 2-condition,
                         seed-paired ablation dataframe with columns
                         [threshold_m, model, condition, auc, seed]).
        leaky_condition: Name of the condition representing the LEAKY
                         setup. If None, inferred by matching any
                         condition name containing "leaky" — this avoids
                         depending on alphabetical sort order, which does
                         not reliably put "leaky" first or second.

    Returns:
        DataFrame with columns [threshold_m, model, leaky_condition,
        correct_condition, mean_inflation (leaky − correct), wilcoxon_p,
        ttest_p, n_pairs, significant_at_05].
    """
    from scipy.stats import ttest_rel, wilcoxon

    rows = []
    conditions = sorted(ablation_df["condition"].unique())
    if len(conditions) != 2:
        raise ValueError(
            f"Expected exactly 2 conditions to compare, got {len(conditions)}: {conditions}"
        )

    if leaky_condition is None:
        leaky_matches = [c for c in conditions if "leaky" in c.lower()]
        if len(leaky_matches) != 1:
            raise ValueError(
                f"Could not unambiguously infer the leaky condition from {conditions}. "
                "Pass leaky_condition explicitly."
            )
        leaky_condition = leaky_matches[0]
    correct_condition = [c for c in conditions if c != leaky_condition][0]

    for (thr, model), group in ablation_df.groupby(["threshold_m", "model"]):
        leaky = group[group["condition"] == leaky_condition].set_index("seed")["auc"]
        correct = group[group["condition"] == correct_condition].set_index("seed")["auc"]
        common_seeds = leaky.index.intersection(correct.index)
        leaky, correct = leaky.loc[common_seeds], correct.loc[common_seeds]

        # Positive mean_inflation = leaky AUC higher than correct AUC
        diff = leaky - correct
        mean_inflation = diff.mean()

        try:
            wilcoxon_p = wilcoxon(leaky, correct).pvalue
        except ValueError:
            # All differences are zero, or too few pairs
            wilcoxon_p = np.nan

        ttest_p = ttest_rel(leaky, correct).pvalue

        rows.append(
            {
                "threshold_m": thr,
                "model": model,
                "leaky_condition": leaky_condition,
                "correct_condition": correct_condition,
                "mean_inflation": round(mean_inflation, 4),
                "wilcoxon_p": round(wilcoxon_p, 4) if not np.isnan(wilcoxon_p) else np.nan,
                "ttest_p": round(ttest_p, 4),
                "n_pairs": len(common_seeds),
                "significant_at_05": bool(ttest_p < 0.05),
            }
        )

    result = pd.DataFrame(rows).sort_values(["threshold_m", "model"])
    logger.info(
        "Leakage significance test: %d/%d model-threshold combinations significant at p<0.05",
        result["significant_at_05"].sum(),
        len(result),
    )
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Single-split vs. repeated/nested CV ablation
# ─────────────────────────────────────────────────────────────────────────────


def run_split_variance_ablation(
    expr: pd.DataFrame,
    labelled_dict: dict[int, pd.DataFrame],
    cfg: dict[str, Any],
    n_repeats: int = 30,
) -> pd.DataFrame:
    """
    Quantify how much a single train/test split's reported AUC varies
    purely due to random split choice — i.e. the variance a paper would
    be hiding if it reported only one split's AUC.

    Uses CORRECT (train-only) feature selection in every repeat, isolating
    split-variance from the leakage effect studied in run_leakage_ablation.

    Args:
        expr:          Clean expression matrix.
        labelled_dict: {threshold: labelled df}.
        cfg:           Project config dict.
        n_repeats:     Number of random splits to sample.

    Returns:
        Tidy DataFrame with columns [threshold_m, model, auc, seed].
    """
    top_n = cfg["features"]["top_n_genes"]
    test_size = cfg["model"]["test_size"]
    base_seed = cfg["project"]["seed"]

    rows = []
    for thr, labelled in labelled_dict.items():
        X, y = align_expression_to_labels(expr, labelled)

        for rep in range(n_repeats):
            seed = base_seed + rep
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=seed, stratify=y
            )

            genes = _select_top_variance(X_train, top_n)
            Xtr, Xte = X_train[genes], X_test[genes]

            scaler = StandardScaler()
            Xtr_sc = scaler.fit_transform(Xtr)
            Xte_sc = scaler.transform(Xte)

            models = get_all_models(cfg)
            for name, model in models.items():
                fitted = train_model(model, Xtr_sc, y_train)
                y_prob = fitted.predict_proba(Xte_sc)[:, 1]
                auc = roc_auc_score(y_test, y_prob)
                rows.append({"threshold_m": thr, "model": name, "auc": auc, "seed": seed})

    return pd.DataFrame(rows)


def bootstrap_auc_ci(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    n_bootstrap: int = 1000,
    ci: float = 0.95,
    seed: int = 42,
) -> dict[str, float]:
    """
    Compute a bootstrap confidence interval for ROC-AUC on a single test set.

    Args:
        y_true:      True binary labels.
        y_prob:      Predicted probabilities for the positive class.
        n_bootstrap: Number of bootstrap resamples.
        ci:          Confidence level (e.g. 0.95 for 95% CI).
        seed:        Random seed.

    Returns:
        Dict with keys: point_estimate, ci_lower, ci_upper, std.
    """
    rng = np.random.RandomState(seed)
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    n = len(y_true)

    boot_aucs = []
    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, n)
        if len(np.unique(y_true[idx])) < 2:
            continue  # skip resamples with only one class present
        boot_aucs.append(roc_auc_score(y_true[idx], y_prob[idx]))

    boot_aucs = np.array(boot_aucs)
    alpha = (1 - ci) / 2

    return {
        "point_estimate": roc_auc_score(y_true, y_prob),
        "ci_lower": float(np.percentile(boot_aucs, 100 * alpha)),
        "ci_upper": float(np.percentile(boot_aucs, 100 * (1 - alpha))),
        "std": float(boot_aucs.std()),
        "n_valid_bootstraps": len(boot_aucs),
    }


def nested_cross_validate(
    model_builder,
    X: np.ndarray,
    y: np.ndarray,
    feature_selector,
    outer_splits: int = 5,
    inner_splits: int = 3,
    seed: int = 42,
) -> dict[str, float]:
    """
    Nested cross-validation: outer loop estimates generalisation performance,
    inner loop (implicit via feature_selector being refit per outer fold)
    ensures feature selection never sees the outer test fold.

    This gives an honest, low-bias estimate of AUC for small-n genomics data,
    versus a single held-out split which has high variance.

    Args:
        model_builder:    Zero-arg callable returning a fresh sklearn estimator.
        X:                Full feature matrix (DataFrame, patients × genes).
        y:                Full label array.
        feature_selector: Callable(X_train, X_test) -> (X_train_sel, X_test_sel).
        outer_splits:      Number of outer CV folds.
        inner_splits:      (Reserved for future hyperparameter tuning within folds.)
        seed:              Random seed.

    Returns:
        Dict with keys: mean_auc, std_auc, fold_aucs (list).
    """
    outer_cv = StratifiedKFold(n_splits=outer_splits, shuffle=True, random_state=seed)
    fold_aucs = []

    X_arr = X.values if hasattr(X, "values") else X
    y_arr = np.asarray(y)

    for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X_arr, y_arr)):
        X_train = X.iloc[train_idx] if hasattr(X, "iloc") else X_arr[train_idx]
        X_test = X.iloc[test_idx] if hasattr(X, "iloc") else X_arr[test_idx]
        y_train, y_test = y_arr[train_idx], y_arr[test_idx]

        X_train_sel, X_test_sel = feature_selector(X_train, X_test)

        scaler = StandardScaler()
        X_train_sc = scaler.fit_transform(X_train_sel)
        X_test_sc = scaler.transform(X_test_sel)

        model = model_builder()
        model.fit(X_train_sc, y_train)
        y_prob = model.predict_proba(X_test_sc)[:, 1]

        fold_auc = roc_auc_score(y_test, y_prob)
        fold_aucs.append(fold_auc)
        logger.info("Nested CV fold %d: AUC = %.3f", fold_idx + 1, fold_auc)

    return {
        "mean_auc": float(np.mean(fold_aucs)),
        "std_auc": float(np.std(fold_aucs)),
        "fold_aucs": fold_aucs,
    }
