# phase2/phase2_03b_recover_gene_names.py
# Purpose: Replicate the pipeline's variance filter to recover the exact
#          500-gene list that the RF models were trained on, then re-export
#          all importance tables with real gene names.
# Run from project root:
#   python phase2\phase2_03b_recover_gene_names.py

import sys
import os
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = Path(
    "D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
    "3rd Sem FALL 2025/BINF 760 ML/Project data/"
    "ov_tcga_pan_can_atlas_2018"
)
MODELS_DIR = PROJECT_ROOT / "outputs" / "models"
PHASE2_OUT = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)

RSEM_PATH      = DATA_DIR / "data_mrna_seq_v2_rsem.txt"
TREATMENT_PATH = DATA_DIR / "data_timeline_treatment.txt"

# ── 1. Load treatment file → platinum patient IDs ─────────────────────────────
print("=== Step 1: Identify platinum-treated patients ===")
trt = pd.read_csv(TREATMENT_PATH, sep="\t", comment="#", low_memory=False)
plat_mask     = trt["AGENT"].str.contains("platin", case=False, na=False)
plat_patients = set(trt.loc[plat_mask, "PATIENT_ID"].unique())
print(f"  Platinum patients: {len(plat_patients)}")

# ── 2. Load RSEM expression matrix ────────────────────────────────────────────
print("\n=== Step 2: Load RSEM expression matrix ===")
print("  (Reading RSEM — may take ~30 seconds)")
rsem_raw = pd.read_csv(RSEM_PATH, sep="\t", comment="#", index_col=0, low_memory=False)

# Drop Entrez column if present (second column after Hugo_Symbol index)
if "Entrez_Gene_Id" in rsem_raw.columns:
    rsem_raw = rsem_raw.drop(columns=["Entrez_Gene_Id"])

print(f"  RSEM shape (genes x samples): {rsem_raw.shape}")

# ── 3. Filter columns to platinum-treated patients ────────────────────────────
print("\n=== Step 3: Filter to platinum-treated patients ===")
# TCGA sample IDs in RSEM are like TCGA-04-1348-01
# Patient IDs in treatment file are like TCGA-04-1348
# Match: first 12 characters of sample ID = patient ID
sample_cols   = rsem_raw.columns.tolist()
sample_to_pat = {s: s[:12] for s in sample_cols}
plat_samples  = [s for s, p in sample_to_pat.items() if p in plat_patients]

print(f"  Total samples in RSEM: {len(sample_cols)}")
print(f"  Platinum-matching samples: {len(plat_samples)}")

rsem_plat = rsem_raw[plat_samples].copy()
print(f"  Expression matrix (platinum): {rsem_plat.shape}")

# ── 4. Drop duplicate gene symbols ────────────────────────────────────────────
print("\n=== Step 4: Drop duplicate gene symbols ===")
before = rsem_plat.shape[0]
rsem_plat = rsem_plat[~rsem_plat.index.duplicated(keep="first")]
print(f"  Genes before: {before} | after dedup: {rsem_plat.shape[0]}")

# ── 5. Compute per-gene variance and select top 500 ───────────────────────────
print("\n=== Step 5: Variance filter → top 500 genes ===")
# Variance computed on raw RSEM values across platinum samples
# (StandardScaler is applied post-split, so variance filter uses raw values)
gene_variances = rsem_plat.var(axis=1)  # variance across samples for each gene

top500_genes = (
    gene_variances
    .sort_values(ascending=False)
    .head(500)
    .index
    .tolist()
)

print(f"  Top-500 gene variance range:")
print(f"    #1   (highest): {gene_variances[top500_genes[0]]:.2f}  ({top500_genes[0]})")
print(f"    #500 (cutoff) : {gene_variances[top500_genes[499]]:.2f}  ({top500_genes[499]})")
print(f"\n  Top 20 highest-variance genes:")
for i, g in enumerate(top500_genes[:20]):
    print(f"    {i+1:3d}. {g:<20s}  var={gene_variances[g]:.2f}")

# ── 6. Verify feature count matches models ────────────────────────────────────
print(f"\n=== Step 6: Verify against model feature count ===")
# Load one RF model to check
rf_path = MODELS_DIR / "Random_Forest_12m.pkl"
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    with open(rf_path, "rb") as f:
        rf_model = pickle.load(f)
n_model_features = len(rf_model.feature_importances_)
print(f"  Model expects: {n_model_features} features")
print(f"  Our gene list: {len(top500_genes)} genes")

if n_model_features != len(top500_genes):
    print(f"  MISMATCH — checking if pipeline used a different N")
    print(f"  Trying top-{n_model_features} genes instead...")
    top500_genes = (
        gene_variances
        .sort_values(ascending=False)
        .head(n_model_features)
        .index
        .tolist()
    )
    print(f"  Adjusted to {len(top500_genes)} genes")
else:
    print(f"  MATCH ✓")

# ── 7. Load all RF models and extract importances with gene names ──────────────
print("\n=== Step 7: Extract RF importances with gene names ===")
rf_files = sorted(MODELS_DIR.glob("Random_Forest_*.pkl"))
all_importances = {}

for rf_path in rf_files:
    model_name = rf_path.stem
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with open(rf_path, "rb") as f:
            model = pickle.load(f)
    importances = model.feature_importances_
    all_importances[model_name] = importances
    print(f"  {model_name}: {len(importances)} features loaded")

# ── 8. Build named importance dataframe ───────────────────────────────────────
print("\n=== Step 8: Build importance tables ===")
imp_matrix    = np.vstack(list(all_importances.values()))
mean_imp      = imp_matrix.mean(axis=0)
std_imp       = imp_matrix.std(axis=0)

imp_df = pd.DataFrame({
    "gene":            top500_genes,
    "mean_importance": mean_imp,
    "std_importance":  std_imp,
    "variance_in_data": [gene_variances[g] for g in top500_genes],
})
imp_df = imp_df.sort_values("mean_importance", ascending=False).reset_index(drop=True)
imp_df["rank"] = imp_df.index + 1

print("\nTop 30 genes by mean RF importance (averaged across 12m/18m/24m):")
print(imp_df.head(30)[["rank","gene","mean_importance","std_importance"]].to_string(index=False))

# ── 9. Save outputs ───────────────────────────────────────────────────────────
print("\n=== Step 9: Save outputs ===")

# Full table
full_csv = PHASE2_OUT / "rf_feature_importances_named.csv"
imp_df.to_csv(full_csv, index=False)
print(f"  Full named importance table: {full_csv.name}")

# Top-N gene lists (plain text, one gene per line — ready for Enrichr/g:Profiler)
for top_n in [50, 100, 200, 500]:
    out_path = PHASE2_OUT / f"top{top_n}_genes_named.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(imp_df.head(top_n)["gene"].tolist()))
    print(f"  Top-{top_n} named gene list: {out_path.name}")

# Per-threshold tables
for model_name, importances in all_importances.items():
    df = pd.DataFrame({
        "gene": top500_genes,
        "importance": importances,
    }).sort_values("importance", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    out = PHASE2_OUT / f"rf_importances_named_{model_name}.csv"
    df.to_csv(out, index=False)
    print(f"  Per-model table: {out.name}")

# Also save the top500 gene list in order of variance (for reference)
var_order_path = PHASE2_OUT / "top500_genes_variance_order.txt"
with open(var_order_path, "w") as f:
    f.write("\n".join(top500_genes))
print(f"  Top-500 genes (variance order): {var_order_path.name}")

# ── 10. Summary ───────────────────────────────────────────────────────────────
print("\n══════════════════════════════════════════════")
print("GENE NAME RECOVERY — SUMMARY")
print("══════════════════════════════════════════════")
print(f"  Platinum samples used for variance: {len(plat_samples)}")
print(f"  Genes after dedup:                  {rsem_plat.shape[0]}")
print(f"  Top-N selected (matches model):     {len(top500_genes)}")
print(f"\n  Top 10 genes by RF importance:")
for _, row in imp_df.head(10).iterrows():
    print(f"    {int(row['rank']):3d}. {row['gene']:<20s}  "
          f"importance={row['mean_importance']:.6f}  "
          f"(±{row['std_importance']:.6f})")
print("\n══════════════════════════════════════════════")
print("Done. Paste full output into chat.")
