# phase2/phase2_03d_cv_permutation_shap_importance.py
# Purpose: phase2_03c found near-zero Spearman correlation between MDI,
#          permutation importance, and SHAP for Finding 5's RF gene rankings.
#          Two suspected causes: (1) MDI came from the full-training-set fit
#          while permutation/SHAP ran on a single tiny 20% test fold - not a
#          fair comparison; (2) that fold is severely underpowered, especially
#          at 12m (11 total events, ~2 positive test cases), where the
#          single-split test AUC was 0.48 (worse than chance).
#
# This script replaces the single train/test split with repeated stratified
# CV (5 splits x 5 repeats = 25 folds per threshold) and computes MDI,
# permutation importance, and SHAP IDENTICALLY within each fold - a fair
# three-way comparison that also uses far more of the data than one 20%
# split allows.
#
# Does NOT modify phase2_03.py, phase2_03b.py, phase2_03c.py, config.yaml,
# or .git. New file only.
#
# Run from project root:
#   python -u phase2\phase2_03d_cv_permutation_shap_importance.py

from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.stats import spearmanr
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold
import shap

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_clinical, load_treatment, load_expression
from src.preprocessing import (
    extract_survival,
    identify_platinum_patients,
    build_labelled_survival,
    clean_expression,
    align_expression_to_labels,
)
from src.features import select_high_variance_genes, scale_features
from src.models import build_random_forest

# ── Paths (same convention as phase2_03/03b/03c) ─────────────────────────
DATA_DIR = Path(
    "D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
    "3rd Sem FALL 2025/BINF 760 ML/Project data/"
    "ov_tcga_pan_can_atlas_2018"
)
PHASE2_OUT = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

N_SPLITS = 5
N_REPEATS = 5
PERM_N_REPEATS = 10
EXPECTED_SEED = 42
EMT_ECM_GENES = ["COL1A1", "COL1A2", "THBS1", "THBS2", "FLNA", "CTNNB1"]

t_start = time.time()


def log(msg: str) -> None:
    print(msg, flush=True)


log("=" * 70)
log("phase2_03d - Repeated CV: MDI vs Permutation vs SHAP (fair comparison)")
log("=" * 70)

# ── 0. Load config (read-only) ────────────────────────────────────────────
log("\n=== Step 0: Load config (read-only; not modified) ===")
with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

seed = cfg["project"]["seed"]
top_n_genes = cfg["features"]["top_n_genes"]
thresholds = cfg["clinical"]["thresholds"]
time_col = cfg["clinical"]["time_col"]
status_col = cfg["clinical"]["status_col"]
platinum_drugs = cfg["clinical"]["platinum_drugs"]
rf_cfg_base = cfg["model"]["random_forest"]

log(f"  project.seed         = {seed}")
log(f"  features.top_n_genes = {top_n_genes}")
log(f"  clinical.thresholds  = {thresholds}")
log(f"  model.random_forest  = {rf_cfg_base}")
log(f"  CV design: RepeatedStratifiedKFold(n_splits={N_SPLITS}, n_repeats={N_REPEATS}, "
    f"random_state={seed}) -> {N_SPLITS*N_REPEATS} folds/threshold")
log(f"  permutation_importance n_repeats={PERM_N_REPEATS} "
    f"(x{N_SPLITS*N_REPEATS} folds = {PERM_N_REPEATS*N_SPLITS*N_REPEATS} effective repeat-evaluations/threshold)")
log(f"  (data.data_dir in config.yaml is stale; using hardcoded DATA_DIR)\n    {DATA_DIR}")

assert seed == EXPECTED_SEED, (
    f"config.yaml seed ({seed}) != expected ({EXPECTED_SEED}) - stopping."
)

# ── 1. Load raw data ONCE (reused across all thresholds and all folds) ───
log("\n=== Step 1: Load raw data (once) ===")
clinical = load_clinical(DATA_DIR, cfg["data"]["clinical_file"])
treatment = load_treatment(DATA_DIR, cfg["data"]["treatment_file"])
log("  Reading RSEM expression matrix (~30s)...")
expr_raw = load_expression(DATA_DIR, cfg["data"]["expression_file"])
log(f"  clinical shape={clinical.shape} | treatment shape={treatment.shape} "
    f"| expr_raw shape={expr_raw.shape}")

surv = extract_survival(clinical, time_col, status_col)
platinum_ids = identify_platinum_patients(treatment, platinum_drugs)
labelled_dict = build_labelled_survival(surv, platinum_ids, time_col, thresholds)
expr = clean_expression(expr_raw)
log(f"  Platinum patients: {len(platinum_ids)}")
for thr, df in labelled_dict.items():
    log(f"  Threshold {thr}m: {len(df)} labelled patients "
        f"({int((df['response']==1).sum())} events / {int((df['response']==0).sum())} non-events)")
log(f"  Expression cleaned shape (genes x patients): {expr.shape}")

# ── 2. Per-threshold repeated CV ───────────────────────────────────────────
fold_auc_records: list[dict] = []
mdi_long_records: list[pd.DataFrame] = []
perm_long_records: list[pd.DataFrame] = []
shap_long_records: list[pd.DataFrame] = []

for thr in thresholds:
    log(f"\n{'='*70}")
    log(f"THRESHOLD {thr}m - {N_SPLITS*N_REPEATS} folds")
    log(f"{'='*70}")

    X, y = align_expression_to_labels(expr, labelled_dict[thr])
    log(f"  Full cohort for this threshold: X={X.shape}, "
        f"y class counts={y.value_counts().to_dict()}")

    rskf = RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=seed)

    mdi_accum: dict[str, list[float]] = defaultdict(list)
    perm_accum: dict[str, list[float]] = defaultdict(list)
    shap_accum: dict[str, list[float]] = defaultdict(list)

    fold_counter = 0
    for train_idx, test_idx in rskf.split(X, y):
        fold_counter += 1
        repeat_num = (fold_counter - 1) // N_SPLITS + 1
        split_num = (fold_counter - 1) % N_SPLITS + 1

        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        X_train_red, X_test_red = select_high_variance_genes(X_train, X_test, top_n=top_n_genes)
        gene_list = X_train_red.columns.tolist()
        X_train_sc, X_test_sc, scaler = scale_features(X_train_red, X_test_red)

        model = build_random_forest({**rf_cfg_base, "seed": seed})
        model.fit(X_train_sc, y_train)

        n_events_test = int(y_test.sum())
        if y_test.nunique() < 2:
            log(f"  [{thr}m] fold {fold_counter:2d}/25 (repeat {repeat_num}, split {split_num}): "
                f"n_train={len(train_idx)} n_test={len(test_idx)} n_events_test={n_events_test} "
                f"*** only one class in y_test - AUC/permutation skipped, MDI still recorded ***")
            fold_auc = np.nan
            skip_test_metrics = True
        else:
            y_prob = model.predict_proba(X_test_sc)[:, 1]
            fold_auc = roc_auc_score(y_test, y_prob)
            skip_test_metrics = False
            log(f"  [{thr}m] fold {fold_counter:2d}/25 (repeat {repeat_num}, split {split_num}): "
                f"n_train={len(train_idx)} n_test={len(test_idx)} n_events_test={n_events_test} "
                f"AUC={fold_auc:.4f}")

        fold_auc_records.append(dict(
            threshold=thr, fold_id=fold_counter, repeat=repeat_num, split=split_num,
            n_train=len(train_idx), n_test=len(test_idx), n_events_test=n_events_test,
            auc=fold_auc,
        ))

        # MDI - from this fold's fitted model, no test data needed
        for g, imp in zip(gene_list, model.feature_importances_):
            mdi_accum[g].append(float(imp))

        if not skip_test_metrics:
            # Permutation importance on the test fold
            perm_result = permutation_importance(
                model, X_test_sc, y_test,
                n_repeats=PERM_N_REPEATS, random_state=seed, scoring="roc_auc", n_jobs=-1,
            )
            for g, imp in zip(gene_list, perm_result.importances_mean):
                perm_accum[g].append(float(imp))

            # SHAP TreeExplainer on the test fold, positive class (event=1)
            explainer = shap.TreeExplainer(model)
            sv = explainer.shap_values(X_test_sc)
            if isinstance(sv, list):
                sv_class1 = sv[1]
            else:
                sv_arr = np.asarray(sv)
                sv_class1 = sv_arr[:, :, 1] if sv_arr.ndim == 3 else sv_arr
            mean_abs_shap = np.abs(sv_class1).mean(axis=0)
            for g, imp in zip(gene_list, mean_abs_shap):
                shap_accum[g].append(float(imp))

    # ── Aggregate this threshold's per-gene importances across its 25 folds ──
    elapsed = time.time() - t_start
    log(f"  -- {thr}m: all {fold_counter} folds done ({elapsed/60:.1f} min elapsed total) --")

    def to_long_df(accum: dict[str, list[float]]) -> pd.DataFrame:
        rows = [
            dict(gene=g, threshold=thr, mean_importance=float(np.mean(v)),
                 std_importance=float(np.std(v)), n_folds_present=len(v))
            for g, v in accum.items()
        ]
        return pd.DataFrame(rows).sort_values("mean_importance", ascending=False).reset_index(drop=True)

    mdi_thr_df = to_long_df(mdi_accum)
    perm_thr_df = to_long_df(perm_accum)
    shap_thr_df = to_long_df(shap_accum)

    log(f"  MDI: {len(mdi_thr_df)} unique genes across folds "
        f"({(mdi_thr_df['n_folds_present']==fold_counter).sum()} present in all {fold_counter})")
    log(f"  Permutation: {len(perm_thr_df)} unique genes "
        f"({(perm_thr_df['n_folds_present']==perm_thr_df['n_folds_present'].max()).sum()} present in all "
        f"scored folds)")
    log(f"  SHAP: {len(shap_thr_df)} unique genes "
        f"({(shap_thr_df['n_folds_present']==shap_thr_df['n_folds_present'].max()).sum()} present in all "
        f"scored folds)")

    mdi_long_records.append(mdi_thr_df)
    perm_long_records.append(perm_thr_df)
    shap_long_records.append(shap_thr_df)

    # Checkpoint save after each threshold, in case of interruption
    pd.DataFrame(fold_auc_records).to_csv(PHASE2_OUT / "cv_fold_auc_summary.csv", index=False)
    pd.concat(mdi_long_records, ignore_index=True).to_csv(PHASE2_OUT / "cv_mdi_importances_full.csv", index=False)
    pd.concat(perm_long_records, ignore_index=True).to_csv(PHASE2_OUT / "cv_permutation_importances_full.csv", index=False)
    pd.concat(shap_long_records, ignore_index=True).to_csv(PHASE2_OUT / "cv_shap_importances_full.csv", index=False)
    log(f"  Checkpoint saved (cv_fold_auc_summary.csv, cv_{{mdi,permutation,shap}}_importances_full.csv)")

# ── 3. Fold AUC distribution per threshold + sanity check vs phase2_03c ──
log(f"\n{'='*70}")
log("AUC DISTRIBUTION ACROSS FOLDS (per threshold) + sanity check vs single-split (phase2_03c)")
log(f"{'='*70}")
auc_df = pd.DataFrame(fold_auc_records)
auc_stats_rows = []
verify_path = PHASE2_OUT / "phase2_03c_reconstruction_verification.csv"
single_split_auc = {}
if verify_path.exists():
    v = pd.read_csv(verify_path)
    single_split_auc = dict(zip(v["threshold"], v["recomputed_auc"]))

for thr in thresholds:
    sub = auc_df[(auc_df["threshold"] == thr) & auc_df["auc"].notna()]["auc"]
    stats = dict(threshold=thr, n_folds=len(sub), mean_auc=sub.mean(), std_auc=sub.std(),
                 min_auc=sub.min(), max_auc=sub.max())
    log(f"  {thr}m: mean={stats['mean_auc']:.4f} std={stats['std_auc']:.4f} "
        f"min={stats['min_auc']:.4f} max={stats['max_auc']:.4f}  (n={stats['n_folds']} folds)")
    if thr in single_split_auc:
        ss = single_split_auc[thr]
        within_range = stats["min_auc"] <= ss <= stats["max_auc"]
        log(f"    phase2_03c single-split AUC = {ss:.4f}  "
            f"{'within fold range - consistent with sampling noise' if within_range else '*** OUTSIDE fold range - investigate, may not be sampling noise alone ***'}")
        stats["single_split_auc"] = ss
        stats["single_split_within_fold_range"] = bool(within_range)
    auc_stats_rows.append(stats)
pd.DataFrame(auc_stats_rows).to_csv(PHASE2_OUT / "cv_fold_auc_stats_by_threshold.csv", index=False)
log("  Saved cv_fold_auc_stats_by_threshold.csv")

# ── 4. Cross-threshold aggregation: WITH 12m and WITHOUT 12m, x3 methods ──
log(f"\n{'='*70}")
log("CROSS-THRESHOLD AGGREGATION (with-12m and without-12m, x3 methods)")
log(f"{'='*70}")

mdi_long = pd.concat(mdi_long_records, ignore_index=True)
perm_long = pd.concat(perm_long_records, ignore_index=True)
shap_long = pd.concat(shap_long_records, ignore_index=True)


def cross_threshold_aggregate(long_df: pd.DataFrame, thresholds_to_use: list[int]) -> pd.DataFrame:
    sub = long_df[long_df["threshold"].isin(thresholds_to_use)]
    pivot = sub.pivot_table(index="gene", columns="threshold", values="mean_importance")
    n_present = pivot.notna().sum(axis=1)
    mean_imp = pivot.mean(axis=1, skipna=True)
    out = pd.DataFrame({
        "gene": pivot.index,
        "mean_importance": mean_imp.values,
        "n_thresholds_present": n_present.values,
    }).sort_values("mean_importance", ascending=False).reset_index(drop=True)
    out["rank"] = out.index + 1
    return out


agg = {}  # (method, scenario) -> df
method_longs = {"mdi": mdi_long, "permutation": perm_long, "shap": shap_long}
for method, long_df in method_longs.items():
    agg[(method, "with12m")] = cross_threshold_aggregate(long_df, thresholds)
    agg[(method, "without12m")] = cross_threshold_aggregate(long_df, [t for t in thresholds if t != 12])
    log(f"  {method}: with12m -> {len(agg[(method,'with12m')])} genes | "
        f"without12m -> {len(agg[(method,'without12m')])} genes")

for (method, scenario), df in agg.items():
    for top_n in [50, 100, 200, 500]:
        out_path = PHASE2_OUT / f"cv_top{top_n}_genes_{method}_{scenario}.txt"
        out_path.write_text("\n".join(df.head(top_n)["gene"].tolist()))
log("  Saved cv_top{50,100,200,500}_genes_{mdi,permutation,shap}_{with12m,without12m}.txt (24 files)")

# ── 5a. Spearman correlations, with12m and without12m ─────────────────────
log(f"\n{'='*70}")
log("COMPARISON: Spearman rank correlation (with12m vs without12m)")
log(f"{'='*70}")


def spearman_on_common(a: pd.Series, b: pd.Series, name_a: str, name_b: str) -> dict:
    common = a.index.intersection(b.index)
    rho, p = spearmanr(a.loc[common], b.loc[common])
    return dict(pair=f"{name_a}_vs_{name_b}", n_common_genes=len(common), spearman_rho=rho, p_value=p)


for scenario in ["with12m", "without12m"]:
    mdi_s = agg[("mdi", scenario)].set_index("gene")["mean_importance"]
    perm_s = agg[("permutation", scenario)].set_index("gene")["mean_importance"]
    shap_s = agg[("shap", scenario)].set_index("gene")["mean_importance"]
    rows = [
        spearman_on_common(mdi_s, perm_s, "MDI", "Permutation"),
        spearman_on_common(mdi_s, shap_s, "MDI", "SHAP"),
        spearman_on_common(perm_s, shap_s, "Permutation", "SHAP"),
    ]
    log(f"  [{scenario}]")
    for r in rows:
        log(f"    {r['pair']}: n_common={r['n_common_genes']}, rho={r['spearman_rho']:.4f}, p={r['p_value']:.2e}")
    pd.DataFrame(rows).to_csv(PHASE2_OUT / f"cv_comparison_spearman_{scenario}.csv", index=False)
log("  Saved cv_comparison_spearman_{with12m,without12m}.csv")

# ── 5b. Top-N overlap, with12m and without12m ──────────────────────────────
log(f"\n{'='*70}")
log("COMPARISON: top-N gene set overlap (with12m vs without12m)")
log(f"{'='*70}")


def topn_set(series: pd.Series, n: int) -> set:
    return set(series.sort_values(ascending=False).head(n).index)


for scenario in ["with12m", "without12m"]:
    mdi_s = agg[("mdi", scenario)].set_index("gene")["mean_importance"]
    perm_s = agg[("permutation", scenario)].set_index("gene")["mean_importance"]
    shap_s = agg[("shap", scenario)].set_index("gene")["mean_importance"]
    pairs = [("MDI", mdi_s, "Permutation", perm_s),
             ("MDI", mdi_s, "SHAP", shap_s),
             ("Permutation", perm_s, "SHAP", shap_s)]
    overlap_rows = []
    log(f"  [{scenario}]")
    for name_a, s_a, name_b, s_b in pairs:
        for n in [10, 50, 100, 200]:
            set_a, set_b = topn_set(s_a, n), topn_set(s_b, n)
            inter, only_a, only_b = set_a & set_b, set_a - set_b, set_b - set_a
            log(f"    Top-{n}: {name_a} vs {name_b} -> overlap={len(inter)}/{n}")
            overlap_rows.append(dict(
                pair=f"{name_a}_vs_{name_b}", top_n=n, overlap_count=len(inter),
                only_in_a=len(only_a), only_in_b=len(only_b),
                gained_in_b=";".join(sorted(only_b)), dropped_from_a=";".join(sorted(only_a)),
            ))
    pd.DataFrame(overlap_rows).to_csv(PHASE2_OUT / f"cv_comparison_topN_overlap_{scenario}.csv", index=False)
log("  Saved cv_comparison_topN_overlap_{with12m,without12m}.csv")

# ── 6. EMT/ECM gene tracking (Finding 5 Theme 2 sanity check) ─────────────
log(f"\n{'='*70}")
log(f"EMT/ECM GENE TRACKING: {EMT_ECM_GENES}")
log(f"{'='*70}")
tracking_rows = []
for method in ["mdi", "permutation", "shap"]:
    for scenario in ["with12m", "without12m"]:
        df = agg[(method, scenario)]
        ranked = df.set_index("gene")["rank"]
        for gene in EMT_ECM_GENES:
            present = gene in ranked.index
            rank = int(ranked.loc[gene]) if present else None
            tracking_rows.append(dict(
                gene=gene, method=method, scenario=scenario,
                present=present, rank=rank,
                in_top50=bool(present and rank <= 50),
                in_top100=bool(present and rank <= 100),
            ))
            status = f"rank {rank}" if present else "NOT PRESENT (dropped by variance filter in all folds used)"
            log(f"  {gene:10s} | {method:11s} | {scenario:11s} -> {status}")
tracking_df = pd.DataFrame(tracking_rows)
tracking_df.to_csv(PHASE2_OUT / "cv_emt_ecm_gene_tracking.csv", index=False)
log("  Saved cv_emt_ecm_gene_tracking.csv")

# ── 7. Final summary ───────────────────────────────────────────────────────
elapsed_total = time.time() - t_start
log(f"\n{'='*70}")
log("SUMMARY")
log(f"{'='*70}")
log(f"Total runtime: {elapsed_total/60:.1f} minutes")
log(f"Output files written to: {PHASE2_OUT}")
log("Done. Paste full output into chat.")
