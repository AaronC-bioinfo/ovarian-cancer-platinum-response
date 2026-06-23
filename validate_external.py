"""
validate_external.py
Apply trained TCGA classifiers to harmonised GSE63885 microarray data.
Evaluates AUC on both label sets:
  - Clinical label: CR/PR=0 (responder) vs P/SD=1 (non-responder)
  - DFS label: sensitive=0 vs resistant=1

Usage:
    python validate_external.py
    python validate_external.py --models-dir outputs/models --data-dir data/external
"""

import argparse
import os
import pickle
import warnings
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="External validation on GSE63885")
parser.add_argument("--models-dir",  default="outputs/models",  help="Directory with .pkl model files")
parser.add_argument("--data-dir",    default="data/external",   help="Directory with harmonised CSVs")
parser.add_argument("--results-dir", default="outputs/results", help="Output directory for results")
parser.add_argument("--figures-dir", default="outputs/figures", help="Output directory for figures")
parser.add_argument("--top-n-genes", type=int, default=500,     help="Number of top-variance genes to use")
args = parser.parse_args()

os.makedirs(args.results_dir, exist_ok=True)
os.makedirs(args.figures_dir, exist_ok=True)

print("=" * 60)
print("External Validation: GSE63885")
print("=" * 60)

# ---------------------------------------------------------------------------
# Load harmonised expression and metadata
# ---------------------------------------------------------------------------
print("\nLoading harmonised expression matrix...")
expr = pd.read_csv(os.path.join(args.data_dir, "harmonised_expression.csv"),
                   index_col=0)
print(f"Expression: {expr.shape[0]} genes x {expr.shape[1]} samples")

print("Loading metadata...")
meta = pd.read_csv(os.path.join(args.data_dir, "harmonised_metadata.csv"))
print(f"Metadata: {meta.shape[0]} samples")
print(f"Metadata columns: {list(meta.columns)}")

# Align samples
common = [s for s in meta["sample_id"].values if s in expr.columns]
expr   = expr[common]
meta   = meta[meta["sample_id"].isin(common)].set_index("sample_id").loc[common]
print(f"\nAligned samples: {len(common)}")

# ---------------------------------------------------------------------------
# Define label sets
# ---------------------------------------------------------------------------
labels = {}

# Label 1: use pre-computed platinum_label_clinical if available
if "platinum_label_clinical" in meta.columns:
    y_clin = pd.to_numeric(meta["platinum_label_clinical"], errors="coerce")
    labels["clinical"] = y_clin
    print(f"\nClinical label distribution:\n{y_clin.value_counts(dropna=False)}")
else:
    # Fallback: parse from clinical status column
    cs_col = [c for c in meta.columns if "clinical_status_post" in c]
    cs_col = cs_col[0] if cs_col else None
    if cs_col:
        clinical_map = {"CR": 0, "PR": 0, "SD": 1, "P": 1}
        y_clin = meta[cs_col].map(clinical_map)
        labels["clinical"] = y_clin
        print(f"\nClinical label distribution:\n{y_clin.value_counts(dropna=False)}")

# Label 2: DFS-based platinum sensitivity
# Handle duplicate column names from merge (.x / .y suffixes)
dfs_col = None
for c in ["platinum_label_dfs", "platinum_label_dfs.y", "platinum_label_dfs.x"]:
    if c in meta.columns:
        dfs_col = c
        break
if dfs_col:
    y_dfs = pd.to_numeric(meta[dfs_col], errors="coerce")
    labels["dfs"] = y_dfs
    print(f"\nDFS label distribution (from {dfs_col}):\n{y_dfs.value_counts(dropna=False)}")

# ---------------------------------------------------------------------------
# Load trained models and feature gene list
# ---------------------------------------------------------------------------
# Find all model pkl files
model_files = [f for f in os.listdir(args.models_dir) if f.endswith(".pkl")]
print(f"\nFound {len(model_files)} model files: {model_files}")

# Parse model files: expect naming like lr_12m.pkl, rf_18m.pkl, svm_24m.pkl
models = {}
for mf in model_files:
    name = mf.replace(".pkl", "")
    with open(os.path.join(args.models_dir, mf), "rb") as f:
        models[name] = pickle.load(f)
    print(f"  Loaded: {name}")

# ---------------------------------------------------------------------------
# Load TCGA training gene list to identify top-500 variance genes
# ---------------------------------------------------------------------------
# Use TCGA corrected expression to identify which genes were selected
tcga_corr_path = os.path.join(args.data_dir, "tcga_corrected_expression.csv")
print(f"\nLoading TCGA corrected expression for gene selection...")
tcga_corr = pd.read_csv(tcga_corr_path, index_col=0)
print(f"TCGA corrected: {tcga_corr.shape[0]} genes x {tcga_corr.shape[1]} samples")

# Select top-N genes by variance on TCGA training data (same as pipeline)
gene_variances = tcga_corr.var(axis=1)
top_genes = gene_variances.nlargest(args.top_n_genes).index.tolist()
print(f"Selected top {args.top_n_genes} variance genes from TCGA")

# Filter expression to top genes
available_genes = [g for g in top_genes if g in expr.index]
print(f"Top genes available in GEO data: {len(available_genes)} of {args.top_n_genes}")

X_full = expr.loc[available_genes].T  # samples x genes
print(f"Feature matrix: {X_full.shape}")

# ---------------------------------------------------------------------------
# Run validation for each label set
# ---------------------------------------------------------------------------
all_results = []

for label_name, y_raw in labels.items():
    print(f"\n{'='*50}")
    print(f"Label set: {label_name}")
    print(f"{'='*50}")

    # Align labels with expression
    y = y_raw.reindex(X_full.index)
    labeled_mask = y.notna()
    X_lab = X_full[labeled_mask]
    y_lab = y[labeled_mask].astype(int)

    print(f"Labeled samples: {labeled_mask.sum()} "
          f"(class 0: {(y_lab==0).sum()}, class 1: {(y_lab==1).sum()})")

    if (y_lab == 0).sum() < 2 or (y_lab == 1).sum() < 2:
        print("  Skipping — insufficient samples in one class")
        continue

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_lab)

    # Try each model
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(f"External Validation ROC — GSE63885 ({label_name} labels)",
                 fontsize=13)

    model_names = {
        "Logistic_Regression": "Logistic Regression",
        "Random_Forest":       "Random Forest",
        "SVM":                 "SVM (RBF)"
    }

    for ax_idx, (short, full_name) in enumerate(model_names.items()):
        ax = axes[ax_idx]

        # Find matching models (any threshold)
        matching = {k: v for k, v in models.items() if k.startswith(short + "_")}

        if not matching:
            ax.text(0.5, 0.5, f"No {full_name}\nmodels found",
                    ha="center", va="center", transform=ax.transAxes)
            ax.set_title(full_name)
            continue

        for model_key, model in sorted(matching.items()):
            threshold = model_key.split("_")[-1]
            try:
                if hasattr(model, "predict_proba"):
                    y_prob = model.predict_proba(X_scaled)[:, 1]
                elif hasattr(model, "decision_function"):
                    y_prob = model.decision_function(X_scaled)
                else:
                    print(f"  {model_key}: no predict_proba or decision_function")
                    continue

                auc = roc_auc_score(y_lab, y_prob)
                fpr, tpr, _ = roc_curve(y_lab, y_prob)
                ax.plot(fpr, tpr, label=f"{threshold} (AUC={auc:.3f})")

                all_results.append({
                    "model":     full_name,
                    "threshold": threshold,
                    "label_set": label_name,
                    "n_samples": int(labeled_mask.sum()),
                    "n_class0":  int((y_lab == 0).sum()),
                    "n_class1":  int((y_lab == 1).sum()),
                    "auc":       round(auc, 4)
                })
                print(f"  {model_key}: AUC = {auc:.4f}")

            except Exception as e:
                print(f"  {model_key}: ERROR — {e}")

        ax.plot([0, 1], [0, 1], "k--", alpha=0.4)
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title(full_name)
        ax.legend(fontsize=8)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1.02])

    plt.tight_layout()
    fig_path = os.path.join(args.figures_dir,
                            f"fig_external_validation_roc_{label_name}.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"\nROC figure saved: {fig_path}")

# ---------------------------------------------------------------------------
# Save results table
# ---------------------------------------------------------------------------
if all_results:
    results_df = pd.DataFrame(all_results)
    results_df = results_df.sort_values(["label_set", "model", "threshold"])
    out_path = os.path.join(args.results_dir, "external_validation_results.csv")
    results_df.to_csv(out_path, index=False)
    print(f"\n{'='*60}")
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(results_df.to_string(index=False))
    print(f"\nSaved: {out_path}")
else:
    print("\nNo results generated — check model files and labels.")

print("\n=== External Validation Complete ===")
