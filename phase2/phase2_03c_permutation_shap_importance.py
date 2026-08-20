# phase2/phase2_03c_permutation_shap_importance.py
# Purpose: Replace MDI-based RF feature importance (biased — see
#          https://explained.ai/rf-importance/, flagged by Dr. Lockhart) with
#          permutation importance and TreeSHAP, computed on the ACTUAL
#          held-out test set for each threshold model.
#
# Context (confirmed during Phase 1 investigation):
#   - No train/test split or fitted StandardScaler was ever persisted to
#     disk, so both are reconstructed here from the raw TCGA files using the
#     project's own src/ modules (not reimplemented) and the confirmed seed.
#   - The real pipeline (src/pipeline.py) computes the top-500 variance
#     filter on EACH THRESHOLD'S OWN TRAIN SPLIT, not on the full platinum
#     cohort. phase2_03b's single shared gene list does not necessarily match
#     what each RF model actually trained on, so this script reconstructs the
#     split AND the gene list independently per threshold (12m/18m/24m) and
#     verifies each against the pickled model before trusting it.
#   - This script does not touch config/config.yaml, .git, or the existing
#     MDI output files from phase2_03/phase2_03b.
#
# Run from project root:
#   python phase2\phase2_03c_permutation_shap_importance.py

from __future__ import annotations

import sys
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.stats import spearmanr
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
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

# ── Paths ──────────────────────────────────────────────────────────────────
# NOTE: config.yaml's data.data_dir is a stale sandbox path from a previous
# Cowork session. phase2_03.py and phase2_03b.py both bypass it and hardcode
# the real local path — we do the same here for consistency.
DATA_DIR = Path(
    "D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
    "3rd Sem FALL 2025/BINF 760 ML/Project data/"
    "ov_tcga_pan_can_atlas_2018"
)
MODELS_DIR = PROJECT_ROOT / "outputs" / "models"
RESULTS_DIR = PROJECT_ROOT / "outputs" / "results"
PHASE2_OUT = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"

N_REPEATS = 30
EXPECTED_SEED = 42  # confirmed project.seed in config.yaml during Phase 1

print("=" * 70)
print("phase2_03c - Permutation importance + TreeSHAP (per-threshold reconstruction)")
print("=" * 70)

# ── 0. Load config (read-only) ───────────────────────────────────────────
print("\n=== Step 0: Load config (read-only; not modified) ===")
with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

print(f"  project.seed         = {cfg['project']['seed']}")
print(f"  model.test_size      = {cfg['model']['test_size']}")
print(f"  features.top_n_genes = {cfg['features']['top_n_genes']}")
print(f"  clinical.thresholds  = {cfg['clinical']['thresholds']}")
print(f"  clinical.platinum_drugs = {cfg['clinical']['platinum_drugs']}")
print(f"  (data.data_dir in config.yaml is stale; using hardcoded DATA_DIR)")
print(f"    DATA_DIR = {DATA_DIR}")

seed = cfg["project"]["seed"]
test_size = cfg["model"]["test_size"]
top_n_genes = cfg["features"]["top_n_genes"]
thresholds = cfg["clinical"]["thresholds"]
time_col = cfg["clinical"]["time_col"]
status_col = cfg["clinical"]["status_col"]
platinum_drugs = cfg["clinical"]["platinum_drugs"]

assert seed == EXPECTED_SEED, (
    f"config.yaml seed ({seed}) != expected ({EXPECTED_SEED}) - "
    f"STOPPING, do not silently reconstruct with the wrong seed."
)

# ── 1. Load raw data (once) ──────────────────────────────────────────────
print("\n=== Step 1: Load raw data ===")
clinical = load_clinical(DATA_DIR, cfg["data"]["clinical_file"])
treatment = load_treatment(DATA_DIR, cfg["data"]["treatment_file"])
print("  Reading RSEM expression matrix (~30s)...")
expr_raw = load_expression(DATA_DIR, cfg["data"]["expression_file"])
print(f"  clinical shape={clinical.shape} | treatment shape={treatment.shape} "
      f"| expr_raw shape={expr_raw.shape}")
print(f"  clinical dtypes (first 5): {clinical.dtypes.head(5).to_dict()}")
print(f"  expr_raw columns (first 5): {expr_raw.columns.tolist()[:5]}")

# ── 2. Preprocessing (reuses src/ verbatim - same functions as the real
#       training pipeline, so this is guaranteed identical, not a
#       reimplementation that could silently drift) ──────────────────────
print("\n=== Step 2: Preprocessing (src/preprocessing.py, same as src/pipeline.py) ===")
surv = extract_survival(clinical, time_col, status_col)
platinum_ids = identify_platinum_patients(treatment, platinum_drugs)
labelled_dict = build_labelled_survival(surv, platinum_ids, time_col, thresholds)
expr = clean_expression(expr_raw)
print(f"  Platinum patients: {len(platinum_ids)}")
for thr, df in labelled_dict.items():
    print(f"  Threshold {thr}m: {len(df)} labelled patients")
print(f"  Expression cleaned shape (genes x patients): {expr.shape}")

# ── 3. Per-threshold reconstruction of split + gene filter + scaler ──────
results: dict[int, dict] = {}

for thr in thresholds:
    print(f"\n{'-'*60}")
    print(f"THRESHOLD {thr}m")
    print(f"{'-'*60}")

    X, y = align_expression_to_labels(expr, labelled_dict[thr])
    print(f"  Aligned X: {X.shape} | y class counts: {y.value_counts().to_dict()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    )
    print(f"  Split: X_train={X_train.shape} X_test={X_test.shape}")

    X_train_red, X_test_red = select_high_variance_genes(X_train, X_test, top_n=top_n_genes)
    gene_list = X_train_red.columns.tolist()
    print(f"  Variance-filtered (train-only): {X_train_red.shape[1]} genes")
    print(f"  First 5 genes (desc. train variance): {gene_list[:5]}")

    X_train_sc, X_test_sc, scaler = scale_features(X_train_red, X_test_red)
    print(f"  Scaled. X_test_sc shape: {X_test_sc.shape}")

    model_path = MODELS_DIR / f"Random_Forest_{thr}m.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    n_model_features = model.n_features_in_
    print(f"  Loaded {model_path.name}: n_features_in_={n_model_features}, "
          f"n_estimators={model.n_estimators}, max_depth={model.max_depth}, "
          f"min_samples_split={model.min_samples_split}, "
          f"class_weight={model.class_weight}, random_state={model.random_state}")

    if n_model_features != X_test_sc.shape[1]:
        print(f"  *** MISMATCH: model expects {n_model_features} features, "
              f"reconstruction produced {X_test_sc.shape[1]} - SKIPPING {thr}m ***")
        continue

    y_prob = model.predict_proba(X_test_sc)[:, 1]
    recomputed_auc = roc_auc_score(y_test, y_prob)
    print(f"  Recomputed ROC-AUC on reconstructed test set: {recomputed_auc:.4f}")

    results[thr] = dict(
        model=model,
        X_test_sc=X_test_sc,
        y_test=y_test.values,
        gene_list=gene_list,
        recomputed_auc=recomputed_auc,
    )

if not results:
    print("\nERROR: no threshold reconstructed successfully. Stopping.")
    sys.exit(1)

# ── 4. Verify against reported AUCs ───────────────────────────────────────
print(f"\n{'='*70}")
print("VERIFICATION: reconstructed AUC vs outputs/results/model_performance_summary.csv")
print(f"{'='*70}")
perf_path = RESULTS_DIR / "model_performance_summary.csv"
verify_rows = []
if perf_path.exists():
    perf = pd.read_csv(perf_path)
    print(f"  Loaded {perf_path.name}: {perf.shape}, columns={perf.columns.tolist()}")
    for thr, r in results.items():
        match = perf[(perf["model"] == f"Random Forest ({thr}m)") & (perf["threshold_m"] == thr)]
        if len(match):
            reported_auc = float(match["roc_auc"].iloc[0])
            diff = abs(reported_auc - r["recomputed_auc"])
            print(f"  {thr}m: reported={reported_auc:.4f}  recomputed={r['recomputed_auc']:.4f}  "
                  f"diff={diff:.6f}  {'OK' if diff < 0.01 else '*** LARGE DIFF - RECONSTRUCTION SUSPECT ***'}")
        else:
            reported_auc, diff = np.nan, np.nan
            print(f"  {thr}m: no matching row found in {perf_path.name}")
        verify_rows.append(dict(threshold=thr, reported_auc=reported_auc,
                                 recomputed_auc=r["recomputed_auc"], diff=diff))
else:
    print(f"  WARNING: {perf_path} not found - cannot verify against reported AUCs")
pd.DataFrame(verify_rows).to_csv(PHASE2_OUT / "phase2_03c_reconstruction_verification.csv", index=False)
print(f"  Saved phase2_03c_reconstruction_verification.csv")

# ── 5. Gene-set diagnostic across thresholds ──────────────────────────────
print(f"\n{'='*70}")
print("DIAGNOSTIC: top-500 gene set overlap across thresholds")
print(f"{'='*70}")
gene_sets = {thr: set(r["gene_list"]) for thr, r in results.items()}
thr_list = sorted(gene_sets.keys())
diag_rows = []
for i in range(len(thr_list)):
    for j in range(i + 1, len(thr_list)):
        a, b = thr_list[i], thr_list[j]
        inter = gene_sets[a] & gene_sets[b]
        print(f"  {a}m vs {b}m: {len(inter)}/{top_n_genes} genes shared "
              f"({len(gene_sets[a]-gene_sets[b])} only in {a}m, "
              f"{len(gene_sets[b]-gene_sets[a])} only in {b}m)")
        diag_rows.append(dict(pair=f"{a}m_vs_{b}m", shared=len(inter),
                               only_a=len(gene_sets[a] - gene_sets[b]),
                               only_b=len(gene_sets[b] - gene_sets[a])))

old_list_path = PHASE2_OUT / "top500_genes_variance_order.txt"
if old_list_path.exists():
    old_genes = set(old_list_path.read_text().splitlines())
    for thr in thr_list:
        inter = gene_sets[thr] & old_genes
        print(f"  {thr}m (train-only, per-threshold) vs phase2_03b single full-cohort list: "
              f"{len(inter)}/{top_n_genes} shared")
        diag_rows.append(dict(pair=f"{thr}m_vs_phase2_03b_list", shared=len(inter),
                               only_a=len(gene_sets[thr] - old_genes),
                               only_b=len(old_genes - gene_sets[thr])))
pd.DataFrame(diag_rows).to_csv(PHASE2_OUT / "phase2_03c_gene_set_diagnostic.csv", index=False)
print(f"  Saved phase2_03c_gene_set_diagnostic.csv")

# ── 6. Permutation importance ─────────────────────────────────────────────
print(f"\n{'='*70}")
print(f"PERMUTATION IMPORTANCE (n_repeats={N_REPEATS}, scoring=roc_auc, random_state={seed})")
print(f"{'='*70}")
perm_per_thr: dict[int, pd.Series] = {}
for thr, r in results.items():
    print(f"  Computing for {thr}m ({len(r['gene_list'])} features, "
          f"{r['X_test_sc'].shape[0]} test samples)...")
    perm_result = permutation_importance(
        r["model"], r["X_test_sc"], r["y_test"],
        n_repeats=N_REPEATS, random_state=seed, scoring="roc_auc", n_jobs=-1,
    )
    df = pd.DataFrame({
        "gene": r["gene_list"],
        "importance": perm_result.importances_mean,
        "importance_std": perm_result.importances_std,
    }).sort_values("importance", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    out = PHASE2_OUT / f"permutation_importances_Random_Forest_{thr}m.csv"
    df.to_csv(out, index=False)
    print(f"    Saved {out.name} | top gene: {df.iloc[0]['gene']} ({df.iloc[0]['importance']:.5f})")
    perm_per_thr[thr] = df.set_index("gene")["importance"]

# ── 7. SHAP TreeExplainer ─────────────────────────────────────────────────
print(f"\n{'='*70}")
print("SHAP TreeExplainer - mean(|SHAP|) per gene")
print(f"{'='*70}")
shap_per_thr: dict[int, pd.Series] = {}
for thr, r in results.items():
    print(f"  Computing TreeSHAP for {thr}m...")
    explainer = shap.TreeExplainer(r["model"])
    sv = explainer.shap_values(r["X_test_sc"])
    if isinstance(sv, list):
        sv_class1 = sv[1]
        print(f"    shap_values returned list of {len(sv)} arrays (legacy API); using index 1 (class=1)")
    else:
        sv_arr = np.asarray(sv)
        if sv_arr.ndim == 3:
            sv_class1 = sv_arr[:, :, 1]
            print(f"    shap_values returned 3D array {sv_arr.shape}; using [:,:,1] (class=1)")
        else:
            sv_class1 = sv_arr
            print(f"    shap_values returned 2D array {sv_arr.shape}")
    mean_abs_shap = np.abs(sv_class1).mean(axis=0)
    df = pd.DataFrame({
        "gene": r["gene_list"],
        "importance": mean_abs_shap,
    }).sort_values("importance", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    out = PHASE2_OUT / f"shap_importances_Random_Forest_{thr}m.csv"
    df.to_csv(out, index=False)
    print(f"    Saved {out.name} | top gene: {df.iloc[0]['gene']} ({df.iloc[0]['importance']:.5f})")
    shap_per_thr[thr] = df.set_index("gene")["importance"]

# ── 8. Aggregate across thresholds ────────────────────────────────────────
print(f"\n{'='*70}")
print("AGGREGATING across thresholds (mean over thresholds where gene present)")
print(f"{'='*70}")


def aggregate(per_thr: dict[int, pd.Series], label: str) -> pd.DataFrame:
    combined = pd.concat(per_thr, axis=1)
    n_present = combined.notna().sum(axis=1)
    mean_imp = combined.mean(axis=1, skipna=True)
    std_imp = combined.std(axis=1, skipna=True)
    out = pd.DataFrame({
        "gene": combined.index,
        "mean_importance": mean_imp.values,
        "std_importance": std_imp.values,
        "n_thresholds_present": n_present.values,
    }).sort_values("mean_importance", ascending=False).reset_index(drop=True)
    out["rank"] = out.index + 1
    print(f"  {label}: {len(out)} unique genes across all thresholds "
          f"({(n_present == len(per_thr)).sum()} present in all {len(per_thr)})")
    return out


perm_agg = aggregate(perm_per_thr, "Permutation")
shap_agg = aggregate(shap_per_thr, "SHAP")

perm_agg.to_csv(PHASE2_OUT / "permutation_importances_full.csv", index=False)
shap_agg.to_csv(PHASE2_OUT / "shap_importances_full.csv", index=False)

for top_n in [50, 100, 200, 500]:
    (PHASE2_OUT / f"top{top_n}_genes_permutation.txt").write_text(
        "\n".join(perm_agg.head(top_n)["gene"].tolist()))
    (PHASE2_OUT / f"top{top_n}_genes_shap.txt").write_text(
        "\n".join(shap_agg.head(top_n)["gene"].tolist()))
print("  Saved top-{50,100,200,500}_genes_{permutation,shap}.txt")

# ── 9. Load MDI baseline for comparison ───────────────────────────────────
print(f"\n{'='*70}")
print("LOADING MDI baseline (phase2_03b output) for comparison")
print(f"{'='*70}")
mdi_path = PHASE2_OUT / "rf_feature_importances_named.csv"
mdi = pd.read_csv(mdi_path)
print(f"  Loaded {mdi_path.name}: {mdi.shape}, columns={mdi.columns.tolist()}")
mdi_s = mdi.set_index("gene")["mean_importance"]
perm_s = perm_agg.set_index("gene")["mean_importance"]
shap_s = shap_agg.set_index("gene")["mean_importance"]

# ── 10. Spearman correlations ─────────────────────────────────────────────
print(f"\n{'='*70}")
print("COMPARISON: Spearman rank correlation")
print(f"{'='*70}")


def spearman_on_common(a: pd.Series, b: pd.Series, name_a: str, name_b: str) -> dict:
    common = a.index.intersection(b.index)
    rho, p = spearmanr(a.loc[common], b.loc[common])
    print(f"  {name_a} vs {name_b}: n_common_genes={len(common)}, rho={rho:.4f}, p={p:.2e}")
    return dict(pair=f"{name_a}_vs_{name_b}", n_common_genes=len(common), spearman_rho=rho, p_value=p)


corr_rows = [
    spearman_on_common(mdi_s, perm_s, "MDI", "Permutation"),
    spearman_on_common(mdi_s, shap_s, "MDI", "SHAP"),
    spearman_on_common(perm_s, shap_s, "Permutation", "SHAP"),
]
corr_df = pd.DataFrame(corr_rows)
corr_df.to_csv(PHASE2_OUT / "comparison_spearman_correlations.csv", index=False)
print("  Saved comparison_spearman_correlations.csv")

# ── 11. Top-N set overlap ─────────────────────────────────────────────────
print(f"\n{'='*70}")
print("COMPARISON: top-N gene set overlap")
print(f"{'='*70}")


def topn_set(series: pd.Series, n: int) -> set:
    return set(series.sort_values(ascending=False).head(n).index)


overlap_rows = []
pairs = [
    ("MDI", mdi_s, "Permutation", perm_s),
    ("MDI", mdi_s, "SHAP", shap_s),
    ("Permutation", perm_s, "SHAP", shap_s),
]
for name_a, s_a, name_b, s_b in pairs:
    for n in [10, 50, 100, 200]:
        set_a, set_b = topn_set(s_a, n), topn_set(s_b, n)
        inter = set_a & set_b
        only_a = set_a - set_b
        only_b = set_b - set_a
        print(f"  Top-{n}: {name_a} vs {name_b} -> overlap={len(inter)}/{n}  "
              f"only_{name_a}={len(only_a)}  only_{name_b}={len(only_b)}")
        overlap_rows.append(dict(
            pair=f"{name_a}_vs_{name_b}", top_n=n, overlap_count=len(inter),
            only_in_a=len(only_a), only_in_b=len(only_b),
            gained_in_b=";".join(sorted(only_b)), dropped_from_a=";".join(sorted(only_a)),
        ))
overlap_df = pd.DataFrame(overlap_rows)
overlap_df.to_csv(PHASE2_OUT / "comparison_topN_overlap.csv", index=False)
print("  Saved comparison_topN_overlap.csv")

# ── 12. Final summary ──────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
print(corr_df.to_string(index=False))
print()
print(overlap_df[["pair", "top_n", "overlap_count", "only_in_a", "only_in_b"]].to_string(index=False))
print(f"\nOutput files written to: {PHASE2_OUT}")
print("Done. Paste full output into chat.")
