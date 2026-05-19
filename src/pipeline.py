"""
pipeline.py
───────────
End-to-end orchestration: data → features → models → evaluation → figures.

This module is the single entry point for a full pipeline run.
Call ``run_pipeline(cfg)`` with the loaded config dict to reproduce
all results and figures.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from .data_loader import load_clinical, load_expression, load_treatment
from .evaluation import build_results_table, evaluate_all_models
from .features import scale_features, select_high_variance_genes
from .models import cross_validate_model, get_all_models, save_model, train_model
from .preprocessing import (
    align_expression_to_labels,
    build_labelled_survival,
    clean_expression,
    extract_survival,
    identify_platinum_patients,
)
from .visualization import (
    plot_calibration_curves,
    plot_class_distribution,
    plot_confusion_matrices,
    plot_cv_auc_heatmap,
    plot_feature_importance,
    plot_roc_curves,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────────────────────


def run_pipeline(cfg: dict[str, Any]) -> dict:
    """
    Execute the complete ML pipeline.

    Args:
        cfg: Configuration dict loaded from ``config/config.yaml``.

    Returns:
        Results dict containing:
            ``results_table`` (pd.DataFrame),
            ``cv_results`` (nested dict),
            ``trained_models`` (nested dict),
            ``feature_sets`` (nested dict with X_train, X_test, y_train, y_test
                              per threshold).
    """
    seed = cfg["project"]["seed"]
    data_cfg = cfg["data"]
    clin_cfg = cfg["clinical"]
    feat_cfg = cfg["features"]
    model_cfg = cfg["model"]
    out_cfg = cfg["output"]

    fig_dir = Path(out_cfg["figures_dir"])
    model_dir = Path(out_cfg["models_dir"])
    results_dir = Path(out_cfg["results_dir"])
    for d in [fig_dir, model_dir, results_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # ── 1. Load raw data ──────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("STEP 1 — Data loading")
    logger.info("=" * 60)

    clinical = load_clinical(data_cfg["data_dir"], data_cfg["clinical_file"])
    treatment = load_treatment(data_cfg["data_dir"], data_cfg["treatment_file"])
    expr_raw = load_expression(data_cfg["data_dir"], data_cfg["expression_file"])

    # ── 2. Preprocessing ─────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("STEP 2 — Preprocessing")
    logger.info("=" * 60)

    surv = extract_survival(clinical, clin_cfg["time_col"], clin_cfg["status_col"])
    platinum_ids = identify_platinum_patients(treatment, clin_cfg["platinum_drugs"])
    labelled_dict = build_labelled_survival(
        surv, platinum_ids, clin_cfg["time_col"], clin_cfg["thresholds"]
    )
    expr = clean_expression(expr_raw)

    # ── 3. Feature engineering + modelling per threshold ─────────────────
    logger.info("=" * 60)
    logger.info("STEP 3–5 — Feature engineering, training & evaluation")
    logger.info("=" * 60)

    all_evaluation_results: list[dict] = []
    cv_results: dict[int, dict] = {}
    trained_models: dict[int, dict] = {}
    feature_sets: dict[int, dict] = {}
    label_series: dict[int, pd.Series] = {}

    for thr, labelled in labelled_dict.items():
        logger.info("-" * 40)
        logger.info("Threshold: %dm", thr)
        logger.info("-" * 40)

        # Align expression matrix to labelled patients
        X, y = align_expression_to_labels(expr, labelled)
        label_series[thr] = y

        # Train / test split
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=model_cfg["test_size"],
            random_state=seed,
            stratify=y,
        )

        # Feature selection (fit on train only — no leakage)
        X_train_red, X_test_red = select_high_variance_genes(
            X_train, X_test, top_n=feat_cfg["top_n_genes"]
        )

        # Scaling
        X_train_sc, X_test_sc, scaler = scale_features(X_train_red, X_test_red)

        feature_sets[thr] = dict(
            X_train=X_train_red,
            X_test=X_test_red,
            X_train_scaled=X_train_sc,
            X_test_scaled=X_test_sc,
            y_train=y_train,
            y_test=y_test,
            scaler=scaler,
        )

        # Build & train models
        models = get_all_models(cfg)
        thr_trained: dict[str, Any] = {}

        for name, model in models.items():
            trained = train_model(model, X_train_sc, y_train)
            thr_trained[name] = trained
            save_model(trained, model_dir / f"{name.replace(' ', '_')}_{thr}m.pkl")

            # Cross-validation
            cv = cross_validate_model(
                trained,
                X_train_sc,
                y_train,
                n_splits=model_cfg["cv_folds"],
                seed=seed,
            )
            cv_results.setdefault(thr, {})[name] = cv

        trained_models[thr] = thr_trained

        # Evaluation on held-out test set
        eval_results = evaluate_all_models(thr_trained, X_test_sc, y_test, threshold=thr)
        all_evaluation_results.extend(eval_results)

    # ── 4. Summary table ─────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("STEP 6 — Building results summary")
    logger.info("=" * 60)

    results_table = build_results_table(all_evaluation_results)
    results_table.to_csv(results_dir / "model_performance_summary.csv", index=False)
    logger.info("Results table saved.")
    logger.info("\n%s", results_table.to_string(index=False))

    # ── 5. Visualisations ────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("STEP 7 — Generating figures")
    logger.info("=" * 60)

    _generate_figures(
        label_series=label_series,
        trained_models=trained_models,
        feature_sets=feature_sets,
        all_evaluation_results=all_evaluation_results,
        cv_results=cv_results,
        fig_dir=fig_dir,
        cfg=cfg,
    )

    logger.info("Pipeline complete. All outputs in: %s", Path(out_cfg["figures_dir"]).parent)

    return {
        "results_table": results_table,
        "cv_results": cv_results,
        "trained_models": trained_models,
        "feature_sets": feature_sets,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Private helpers
# ─────────────────────────────────────────────────────────────────────────────


def _generate_figures(
    label_series: dict,
    trained_models: dict,
    feature_sets: dict,
    all_evaluation_results: list[dict],
    cv_results: dict,
    fig_dir: Path,
    cfg: dict,
) -> None:
    """Generate and save all project figures."""

    dpi = cfg["output"]["figure_dpi"]

    # Figure 1 — Class distribution
    plot_class_distribution(
        label_series,
        save_path=fig_dir / "fig1_class_distribution.png",
    )

    # Figure 2 — ROC curves per threshold
    for thr, results in _group_results_by_threshold(all_evaluation_results).items():
        probs = {r["model_name"].split(" (")[0]: r["y_prob"] for r in results}
        y_test = feature_sets[thr]["y_test"]
        plot_roc_curves(
            y_test,
            probs,
            title=f"ROC Curves — {thr}-month endpoint",
            save_path=fig_dir / f"fig2_roc_{thr}m.png",
        )

    # Figure 3 — Confusion matrices per threshold
    for thr, results in _group_results_by_threshold(all_evaluation_results).items():
        preds = {r["model_name"].split(" (")[0]: r["y_pred"] for r in results}
        y_test = feature_sets[thr]["y_test"]
        plot_confusion_matrices(
            y_test,
            preds,
            title=f"Confusion Matrices — {thr}-month endpoint",
            save_path=fig_dir / f"fig3_confusion_{thr}m.png",
        )

    # Figure 4 — CV AUC heatmap
    plot_cv_auc_heatmap(
        cv_results,
        save_path=fig_dir / "fig4_cv_auc_heatmap.png",
    )

    # Figure 5 — Feature importance (Random Forest, all thresholds)
    for thr, models in trained_models.items():
        rf = models.get("Random Forest")
        if rf is not None and hasattr(rf, "feature_importances_"):
            feature_names = np.array(feature_sets[thr]["X_train"].columns)
            plot_feature_importance(
                feature_names,
                rf.feature_importances_,
                title=f"Top Predictive Genes — RF {thr}-month",
                save_path=fig_dir / f"fig5_feature_importance_{thr}m.png",
            )

    # Figure 6 — Calibration curves (RF across thresholds)
    calib_data = {}
    for thr, models in trained_models.items():
        rf = models.get("Random Forest")
        if rf is not None:
            y_test = feature_sets[thr]["y_test"]
            y_prob = rf.predict_proba(feature_sets[thr]["X_test_scaled"])[:, 1]
            calib_data[f"RF {thr}m"] = (y_test, y_prob)

    if calib_data:
        plot_calibration_curves(
            calib_data,
            save_path=fig_dir / "fig6_calibration_curves.png",
        )


def _group_results_by_threshold(results: list[dict]) -> dict[int, list[dict]]:
    """Group a flat list of eval results by threshold."""
    grouped: dict[int, list] = {}
    for r in results:
        grouped.setdefault(r["threshold"], []).append(r)
    return grouped
