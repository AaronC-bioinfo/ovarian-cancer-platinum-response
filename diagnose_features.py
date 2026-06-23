"""
diagnose_features.py
Investigates whether poor external validation AUC is due to:
1. Poor feature overlap (TCGA top-500 genes vs GSE63885 informative genes)
2. Gene expression correlation between platforms post-ComBat
3. Whether GSE63885-native gene selection yields better AUC (upper bound test)

Outputs:
  outputs/results/feature_diagnostic.csv
  outputs/figures/fig_feature_overlap_diagnostic.png
"""

import os
import warnings
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import f_classif
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

MODELS_DIR  = "outputs/models"
DATA_DIR    = "data/external"
RESULTS_DIR = "outputs/results"
FIGURES_DIR = "outputs/figures"
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

print("=" * 60)
print("Feature Diagnostic: TCGA → GSE63885 Transfer Analysis")
print("=" * 60)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("\nLoading data...")
expr = pd.read_csv(os.path.join(DATA_DIR, "harmonised_expression.csv"), index_col=0)
meta = pd.read_csv(os.path.join(DATA_DIR, "harmonised_metadata.csv"))
tcga = pd.read_csv(os.path.join(DATA_DIR, "tcga_corrected_expression.csv"), index_col=0)

# Align samples
common = [s for s in meta["sample_id"].values if s in expr.columns]
expr_al = expr[common]
meta_al = meta[meta["sample_id"].isin(common)].set_index("sample_id").loc[common]

# Labels
y_dfs = pd.to_numeric(
    meta_al.get("platinum_label_dfs.y", meta_al.get("platinum_label_dfs", None)),
    errors="coerce")
y_clin = pd.to_numeric(meta_al.get("platinum_label_clinical"), errors="coerce")

print(f"GEO expression: {expr_al.shape}")
print(f"TCGA expression: {tcga.shape}")

# ---------------------------------------------------------------------------
# Diagnostic 1: TCGA top-500 genes — are they variable in GSE63885?
# ---------------------------------------------------------------------------
print("\n--- Diagnostic 1: TCGA top-500 gene variance in GSE63885 ---")

tcga_var      = tcga.var(axis=1).sort_values(ascending=False)
top500_tcga   = tcga_var.head(500).index.tolist()
top1000_tcga  = tcga_var.head(1000).index.tolist()
top2000_tcga  = tcga_var.head(2000).index.tolist()

# Variance of TCGA top-500 genes in GEO data
geo_var = expr_al.var(axis=1)
geo_var_top500  = geo_var.reindex(top500_tcga).dropna()
geo_var_all     = geo_var

print(f"Median variance of ALL genes in GEO:           {geo_var_all.median():.4f}")
print(f"Median variance of TCGA top-500 genes in GEO:  {geo_var_top500.median():.4f}")
print(f"Ratio (top-500 vs all):                         {geo_var_top500.median()/geo_var_all.median():.2f}x")

# ---------------------------------------------------------------------------
# Diagnostic 2: Post-ComBat inter-platform gene correlation
# ---------------------------------------------------------------------------
print("\n--- Diagnostic 2: Post-ComBat gene correlation (TCGA vs GEO mean expression) ---")

# Compare mean expression per gene: TCGA vs GEO
tcga_sub = tcga.reindex(expr_al.index).dropna()
geo_sub  = expr_al.reindex(tcga_sub.index)

tcga_means = tcga_sub.mean(axis=1)
geo_means  = geo_sub.mean(axis=1)

corr = tcga_means.corr(geo_means)
print(f"Pearson correlation of per-gene mean (TCGA vs GEO): {corr:.4f}")
print("(>0.85 = good correction; <0.70 = batch effect remains)")

# ---------------------------------------------------------------------------
# Diagnostic 3: Upper bound — GSE63885-native gene selection (leave-one-out)
# ---------------------------------------------------------------------------
print("\n--- Diagnostic 3: Upper bound AUC using GSE63885-native top-500 genes ---")
print("(This uses labels from GEO itself — not a valid validation, but shows signal ceiling)")

results = []

for label_name, y_raw in [("dfs", y_dfs), ("clinical", y_clin)]:
    y = y_raw.reindex(expr_al.columns)
    mask = y.notna()
    X_all = expr_al.T
    X_lab = X_all[mask]
    y_lab = y[mask].astype(int)

    if (y_lab == 0).sum() < 5 or (y_lab == 1).sum() < 5:
        print(f"  {label_name}: skipping (too few samples in one class)")
        continue

    print(f"\n  Label: {label_name} | n={mask.sum()} | class0={( y_lab==0).sum()} class1={(y_lab==1).sum()}")

    # Native top-500 by variance (unsupervised — no leakage)
    gene_var = X_lab.var(axis=0).sort_values(ascending=False)
    top500_native = gene_var.head(500).index.tolist()

    # Native top-500 by F-score (supervised — shows ceiling with leakage)
    f_scores, _ = f_classif(X_lab, y_lab)
    top500_fscore = X_lab.columns[np.argsort(f_scores)[::-1][:500]].tolist()

    for gene_set_name, gene_set in [
        ("TCGA top-500 (variance)",    top500_tcga),
        ("TCGA top-1000 (variance)",   top1000_tcga),
        ("TCGA top-2000 (variance)",   top2000_tcga),
        ("GEO native top-500 (variance, no leakage)", top500_native),
        ("GEO native top-500 (F-score, leaky ceiling)", top500_fscore),
    ]:
        avail = [g for g in gene_set if g in X_lab.columns]
        if len(avail) < 50:
            print(f"    {gene_set_name}: only {len(avail)} genes available — skipping")
            continue

        X_feat = X_lab[avail]
        scaler = StandardScaler()
        X_sc   = scaler.fit_transform(X_feat)

        for clf_name, clf in [
            ("LR",  LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
            ("RF",  RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)),
        ]:
            try:
                clf.fit(X_sc, y_lab)
                if hasattr(clf, "predict_proba"):
                    y_prob = clf.predict_proba(X_sc)[:, 1]
                else:
                    y_prob = clf.decision_function(X_sc)
                auc = roc_auc_score(y_lab, y_prob)
                print(f"    {clf_name} | {gene_set_name[:45]:45s} | AUC = {auc:.4f}")
                results.append({
                    "label": label_name,
                    "model": clf_name,
                    "gene_set": gene_set_name,
                    "n_genes": len(avail),
                    "auc": round(auc, 4)
                })
            except Exception as e:
                print(f"    {clf_name} | {gene_set_name}: ERROR — {e}")

# ---------------------------------------------------------------------------
# Diagnostic 4: Visualise gene variance distributions
# ---------------------------------------------------------------------------
print("\n--- Diagnostic 4: Generating variance distribution plot ---")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Feature Diagnostic: TCGA top-500 genes in GSE63885", fontsize=12)

# Plot 1: variance distribution
ax = axes[0]
ax.hist(geo_var_all.values, bins="auto", alpha=0.5, label="All GEO genes", color="steelblue")
ax.hist(geo_var_top500.values, bins="auto", alpha=0.7, label="TCGA top-500 in GEO", color="tomato")
ax.set_xlabel("Gene variance (post-ComBat)")
ax.set_ylabel("Count")
ax.set_title("Variance distribution in GSE63885")
ax.legend()

# Plot 2: mean expression correlation TCGA vs GEO
ax = axes[1]
# Sample 2000 genes for readability
idx = np.random.choice(len(tcga_means), min(2000, len(tcga_means)), replace=False)
ax.scatter(tcga_means.iloc[idx], geo_means.iloc[idx], alpha=0.3, s=5, color="steelblue")
ax.set_xlabel("TCGA mean expression (post-ComBat)")
ax.set_ylabel("GSE63885 mean expression (post-ComBat)")
ax.set_title(f"Per-gene mean correlation\nr = {corr:.3f}")

plt.tight_layout()
fig_path = os.path.join(FIGURES_DIR, "fig_feature_overlap_diagnostic.png")
plt.savefig(fig_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"Figure saved: {fig_path}")

# ---------------------------------------------------------------------------
# Save results
# ---------------------------------------------------------------------------
if results:
    df = pd.DataFrame(results)
    out = os.path.join(RESULTS_DIR, "feature_diagnostic.csv")
    df.to_csv(out, index=False)
    print(f"\nSaved: {out}")
    print("\nFull results table:")
    print(df.to_string(index=False))

print("\n=== Feature Diagnostic Complete ===")
