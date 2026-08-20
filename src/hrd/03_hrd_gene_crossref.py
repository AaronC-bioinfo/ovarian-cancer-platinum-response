"""
Enhancement 4 -- Step 3: RF gene x HRD pathway cross-reference
Ovarian Cancer Platinum Response Project

Checks whether any of the genes driving Finding 5's RF feature importance
(or the broader top-500 variance-filtered list) are themselves canonical
homologous-recombination-repair (HRR) / HRD pathway genes -- i.e. whether
the platinum-response signal is picking up direct DNA-repair biology, as
opposed to (or in addition to) the EMT/ECM signal already established.

NOTE ON THE GENE PANEL: there is no single universally agreed "the" HRD
gene list in the field -- clinical panels (Myriad myChoice, FoundationOne
HRD, etc.) and academic curations vary somewhat in scope. The panel below
is a widely-cited literature curation of core HRR pathway genes (Pennington
et al. 2014, Clin Cancer Res, plus the Fanconi Anemia core complex genes
commonly grouped with it). If you want to compare against a different/
larger panel, edit HRD_PATHWAY_GENES below and re-run -- the rest of the
script doesn't need to change.
"""

import os
import pandas as pd

PROJECT_ROOT = r"C:\PROJECTS\ovarian-cancer-platinum-response"
rf_importance_file = os.path.join(PROJECT_ROOT, "phase2", "outputs",
                                   "rf_feature_importances_named.csv")
top500_file = os.path.join(PROJECT_ROOT, "phase2", "outputs",
                            "top500_genes_named.txt")
out_dir = os.path.join(PROJECT_ROOT, "hrd")
os.makedirs(out_dir, exist_ok=True)

# Core homologous recombination repair (HRR) genes, per Pennington et al.
# 2014 (Clin Cancer Res 20(3):764-75) plus the Fanconi Anemia core complex
# genes frequently grouped alongside HRR in HRD-focused studies.
HRD_PATHWAY_GENES = {
    # Core HR machinery
    "BRCA1", "BRCA2", "RAD51", "RAD51B", "RAD51C", "RAD51D", "RAD54L",
    "PALB2", "BARD1", "BRIP1",
    # Damage sensing / checkpoint kinases
    "ATM", "ATR", "ATRX", "CHEK1", "CHEK2", "MRE11", "NBN", "RAD50",
    # Fanconi Anemia core complex (commonly grouped with HRR)
    "FANCA", "FANCC", "FANCD2", "FANCE", "FANCF", "FANCG", "FANCI",
    "FANCL", "FANCM",
    # Additional recombination/replication-fork genes sometimes included
    "XRCC2", "XRCC3", "PPP2R2A",
}

print(f"HRD pathway panel: {len(HRD_PATHWAY_GENES)} genes")
print(", ".join(sorted(HRD_PATHWAY_GENES)))

# ---- Cross-reference against RF importance list (all genes with a
# computed importance score, not just the printed top 10) ----
if os.path.exists(rf_importance_file):
    rf_df = pd.read_csv(rf_importance_file)
    gene_col = "gene" if "gene" in rf_df.columns else rf_df.columns[0]
    rf_genes = set(rf_df[gene_col].astype(str))
    rf_hrd_overlap = rf_genes & HRD_PATHWAY_GENES
    print(f"\n=== RF importance list ({len(rf_genes)} genes) vs HRD panel ===")
    print(f"Overlap: {len(rf_hrd_overlap)} genes: {sorted(rf_hrd_overlap) if rf_hrd_overlap else '(none)'}")
    if rf_hrd_overlap:
        overlap_rows = rf_df[rf_df[gene_col].isin(rf_hrd_overlap)].sort_values(
            rf_df.columns[1] if len(rf_df.columns) > 1 else gene_col, ascending=False
        )
        print(overlap_rows.to_string(index=False))
else:
    print(f"\nWARNING: {rf_importance_file} not found -- skipping RF importance cross-reference.")
    rf_hrd_overlap = set()

# ---- Cross-reference against the broader top-500 variance-filtered list ----
if os.path.exists(top500_file):
    with open(top500_file) as f:
        top500_genes = set(line.strip() for line in f if line.strip())
    top500_hrd_overlap = top500_genes & HRD_PATHWAY_GENES
    print(f"\n=== Top-500 variance-filtered list ({len(top500_genes)} genes) vs HRD panel ===")
    print(f"Overlap: {len(top500_hrd_overlap)} genes: {sorted(top500_hrd_overlap) if top500_hrd_overlap else '(none)'}")
else:
    print(f"\nWARNING: {top500_file} not found -- skipping top-500 cross-reference.")
    top500_hrd_overlap = set()

# ---- Save results ----
result_rows = []
for gene in sorted(HRD_PATHWAY_GENES):
    result_rows.append({
        "gene": gene,
        "in_rf_importance_list": gene in rf_hrd_overlap,
        "in_top500_variance_list": gene in top500_hrd_overlap,
    })
result_df = pd.DataFrame(result_rows)
out_csv = os.path.join(out_dir, "hrd_gene_crossref.csv")
result_df.to_csv(out_csv, index=False)

print("\n============================================")
print(f"HRD panel genes found in RF importance list:   {len(rf_hrd_overlap)} / {len(HRD_PATHWAY_GENES)}")
print(f"HRD panel genes found in top-500 variance list: {len(top500_hrd_overlap)} / {len(HRD_PATHWAY_GENES)}")
print(f"Wrote full cross-reference table to:\n  {out_csv}")
print("============================================")
