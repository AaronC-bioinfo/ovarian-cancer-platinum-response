# phase2/phase2_03_rf_feature_importance.py
# Purpose: Load trained Random Forest models, extract feature importances,
#          and export top genes for pathway enrichment analysis.
# Run from project root:
#   python phase2/phase2_03_rf_feature_importance.py

import sys
import os
import pickle
import json
import numpy as np
import pandas as pd
from pathlib import Path

# ── Project root on sys.path ───────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR = Path(
    "D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
    "3rd Sem FALL 2025/BINF 760 ML/Project data/"
    "ov_tcga_pan_can_atlas_2018"
)
MODELS_DIR  = PROJECT_ROOT / "outputs" / "models"
PHASE2_OUT  = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)

RSEM_PATH = DATA_DIR / "data_mrna_seq_v2_rsem.txt"

# ── 1. Discover saved model files ─────────────────────────────────────────────
print("=== Scanning for saved models ===")
if not MODELS_DIR.exists():
    print(f"ERROR: models directory not found: {MODELS_DIR}")
    print("Searching for .pkl files anywhere under outputs/...")
    pkl_files = list((PROJECT_ROOT / "outputs").rglob("*.pkl"))
    for f in pkl_files:
        print(f"  {f}")
    sys.exit(1)

pkl_files = sorted(MODELS_DIR.glob("*.pkl"))
print(f"Found {len(pkl_files)} .pkl files in {MODELS_DIR}:")
for f in pkl_files:
    print(f"  {f.name}")

# ── 2. Load gene names from RSEM file (column headers = gene symbols) ─────────
print("\n=== Loading gene names from RSEM file ===")
# RSEM file: first col = Hugo_Symbol, second col = Entrez_Gene_Id, rest = samples
# Read just the header row to get gene names efficiently
rsem_header = pd.read_csv(RSEM_PATH, sep="\t", nrows=0, comment="#")
all_cols = rsem_header.columns.tolist()
print(f"  Total columns in RSEM: {len(all_cols)}")
print(f"  First 5 columns: {all_cols[:5]}")

# The pipeline filters to platinum patients and drops non-expression columns,
# then applies variance filter. We need the exact gene list the model was trained on.
# Strategy: load from a saved feature list if it exists, otherwise reconstruct.

feature_list_path = MODELS_DIR / "feature_names.json"
feature_list_pkl  = MODELS_DIR / "feature_names.pkl"

gene_names = None

if feature_list_path.exists():
    print(f"  Loading feature names from: {feature_list_path}")
    with open(feature_list_path) as f:
        gene_names = json.load(f)
    print(f"  Loaded {len(gene_names)} feature names")
elif feature_list_pkl.exists():
    print(f"  Loading feature names from: {feature_list_pkl}")
    with open(feature_list_pkl, "rb") as f:
        gene_names = pickle.load(f)
    print(f"  Loaded {len(gene_names)} feature names")
else:
    print("  No saved feature name file found.")
    print("  Searching outputs/ for any feature list files...")
    for ext in ["*.json", "*.pkl", "*.csv", "*.txt"]:
        found = list((PROJECT_ROOT / "outputs").rglob(ext))
        if found:
            print(f"  {ext}: {[f.name for f in found[:10]]}")

# ── 3. Load each RF model and extract importances ─────────────────────────────
print("\n=== Extracting Random Forest feature importances ===")

rf_results = {}

for pkl_path in pkl_files:
    model_name = pkl_path.stem
    try:
        with open(pkl_path, "rb") as f:
            obj = pickle.load(f)
    except Exception as e:
        print(f"  SKIP {model_name}: could not load ({e})")
        continue

    # Handle various storage formats: raw model, dict, tuple
    model = None
    if hasattr(obj, "feature_importances_"):
        model = obj
    elif isinstance(obj, dict):
        print(f"  {model_name}: dict with keys {list(obj.keys())[:8]}")
        for key in ["model", "clf", "estimator", "rf", "classifier"]:
            if key in obj and hasattr(obj[key], "feature_importances_"):
                model = obj[key]
                break
        if model is None:
            # Try all values
            for val in obj.values():
                if hasattr(val, "feature_importances_"):
                    model = val
                    break
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            if hasattr(item, "feature_importances_"):
                model = item
                break

    if model is None:
        print(f"  SKIP {model_name}: no feature_importances_ found "
              f"(type={type(obj).__name__})")
        continue

    importances = model.feature_importances_
    n_features  = len(importances)
    print(f"  {model_name}: {n_features} features, "
          f"top importance={importances.max():.6f}")
    rf_results[model_name] = importances

if not rf_results:
    print("\nERROR: No RF models with feature_importances_ found.")
    print("Listing all pkl file types for diagnosis:")
    for pkl_path in pkl_files:
        with open(pkl_path, "rb") as f:
            obj = pickle.load(f)
        print(f"  {pkl_path.name}: type={type(obj).__name__}")
        if isinstance(obj, dict):
            print(f"    keys: {list(obj.keys())}")
    sys.exit(1)

# ── 4. Reconcile feature count with gene names ────────────────────────────────
print("\n=== Reconciling feature counts ===")
n_features_model = len(next(iter(rf_results.values())))
print(f"  Features in first RF model: {n_features_model}")

if gene_names is not None:
    print(f"  Features in loaded gene list: {len(gene_names)}")
    if len(gene_names) != n_features_model:
        print(f"  WARNING: mismatch — gene list has {len(gene_names)}, "
              f"model expects {n_features_model}")
        gene_names = None

if gene_names is None:
    # Reconstruct: read RSEM, drop ID cols, apply same filters as pipeline
    print("  Reconstructing gene list from RSEM file...")
    print("  (Reading RSEM — this may take ~30 seconds)")
    rsem = pd.read_csv(RSEM_PATH, sep="\t", comment="#", index_col=0)
    # Drop Entrez column if present
    if "Entrez_Gene_Id" in rsem.columns:
        rsem = rsem.drop(columns=["Entrez_Gene_Id"])
    # Drop duplicate gene symbols — keep first
    rsem = rsem[~rsem.index.duplicated(keep="first")]
    print(f"  RSEM shape after dedup: {rsem.shape}")
    # The pipeline uses top-500 variance features
    # We'll report all genes and let the top-N cutoff handle it
    gene_names = rsem.index.tolist()
    print(f"  Gene names available: {len(gene_names)}")
    print(f"  NOTE: if model has {n_features_model} features and RSEM has "
          f"{len(gene_names)} genes, the pipeline applied a variance filter.")

# ── 5. Average importances across thresholds for each RF model ────────────────
print("\n=== Aggregating importances ===")

# Group by model type (LR, RF, SVM) and threshold (12m, 18m, 24m)
# File naming convention: e.g. rf_12m.pkl, RandomForest_18m.pkl, etc.
rf_only = {k: v for k, v in rf_results.items()
           if "rf" in k.lower() or "random" in k.lower() or "forest" in k.lower()}
all_models = rf_results  # fallback if naming differs

print(f"  Total models loaded: {len(rf_results)}")
print(f"  RF-identified models: {list(rf_only.keys())}")

target_results = rf_only if rf_only else all_models
print(f"  Using: {list(target_results.keys())}")

# Stack and average
imp_matrix = np.vstack(list(target_results.values()))
mean_importance = imp_matrix.mean(axis=0)
std_importance  = imp_matrix.std(axis=0)
print(f"  Averaged across {imp_matrix.shape[0]} models")

# ── 6. Build importance dataframe ─────────────────────────────────────────────
if gene_names and len(gene_names) == len(mean_importance):
    imp_df = pd.DataFrame({
        "gene":            gene_names,
        "mean_importance": mean_importance,
        "std_importance":  std_importance,
    })
else:
    print(f"  WARNING: gene_names length ({len(gene_names) if gene_names else 0}) "
          f"!= importances length ({len(mean_importance)})")
    print("  Using numeric feature indices.")
    imp_df = pd.DataFrame({
        "gene":            [f"feature_{i}" for i in range(len(mean_importance))],
        "mean_importance": mean_importance,
        "std_importance":  std_importance,
    })

imp_df = imp_df.sort_values("mean_importance", ascending=False).reset_index(drop=True)
imp_df["rank"] = imp_df.index + 1

print(f"\n  Top 20 features by mean importance:")
print(imp_df.head(20).to_string(index=False))

# ── 7. Save full importance table ─────────────────────────────────────────────
full_csv = PHASE2_OUT / "rf_feature_importances_full.csv"
imp_df.to_csv(full_csv, index=False)
print(f"\n  Full importance table saved: {full_csv}")

# ── 8. Export top-N gene lists for pathway enrichment ─────────────────────────
for top_n in [50, 100, 200, 500]:
    top_genes = imp_df.head(top_n)["gene"].tolist()
    out_path = PHASE2_OUT / f"top{top_n}_genes.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(top_genes))
    print(f"  Top-{top_n} gene list saved: {out_path}")

# ── 9. Per-model importance tables ────────────────────────────────────────────
print("\n=== Saving per-model importance tables ===")
for model_name, importances in target_results.items():
    if gene_names and len(gene_names) == len(importances):
        df = pd.DataFrame({
            "gene": gene_names,
            "importance": importances
        }).sort_values("importance", ascending=False)
    else:
        df = pd.DataFrame({
            "gene": [f"feature_{i}" for i in range(len(importances))],
            "importance": importances
        }).sort_values("importance", ascending=False)
    out = PHASE2_OUT / f"rf_importances_{model_name}.csv"
    df.to_csv(out, index=False)
    print(f"  Saved: {out.name}")

# ── 10. Summary ───────────────────────────────────────────────────────────────
print("\n══════════════════════════════════════════════")
print("RF FEATURE IMPORTANCE EXTRACTION — SUMMARY")
print("══════════════════════════════════════════════")
print(f"  Models processed     : {len(target_results)}")
print(f"  Features per model   : {n_features_model}")
print(f"  Top gene (avg)       : {imp_df.iloc[0]['gene']}  "
      f"(importance={imp_df.iloc[0]['mean_importance']:.6f})")
print(f"  Top 10 genes: {imp_df.head(10)['gene'].tolist()}")
print(f"\n  Output files in {PHASE2_OUT}:")
print(f"    rf_feature_importances_full.csv")
for top_n in [50, 100, 200, 500]:
    print(f"    top{top_n}_genes.txt")
print("══════════════════════════════════════════════")
print("Done. Paste full output into chat.")
