"""
Enhancement 3 -- Step 3: Purity-corrected pathway enrichment
Ovarian Cancer Platinum Response Project

Tests whether Finding 5's ribosomal/translation signal (adj p ~10^-34) is a
tumour-cellularity artefact rather than platinum-response biology.

Methodology (matched to the original Finding 5 pipeline so the comparison
is apples-to-apples):
  1. Same 235-patient platinum-treated RNA-seq subset used for ESTIMATE.
  2. Same variance-filter approach on RAW RSEM values (no log transform --
     PROJECT_LOG.md explicitly notes the original filter ran on
     "pre-split, raw RSEM"), same n=500 gene count.
  3. ONLY CHANGE: each gene's expression is residualized against
     TumorPurity (OLS) before the variance filter, so genes whose apparent
     variability was actually driven by purity differences between
     patients get down-weighted or dropped from the top-500.
  4. Re-run the same 4 Enrichr libraries used originally.

Reuses the top500_genes_named.txt already on disk as the "before" list
for the comparison rather than re-deriving it, since re-deriving from
raw expression could accidentally introduce a second uncontrolled
methodology difference alongside the purity correction.
"""

import os
import time
import requests
import pandas as pd
import numpy as np

# ---- Paths ----
PROJECT_ROOT = r"C:\PROJECTS\ovarian-cancer-platinum-response"
TCGA_PATH = (r"D:\ALIENWARE\WORK DATA\George Mason\Course Work"
             r"\3rd Sem FALL 2025\BINF 760 ML\Project data"
             r"\ov_tcga_pan_can_atlas_2018")

expr_file = os.path.join(TCGA_PATH, "data_mrna_seq_v2_rsem.txt")
purity_file = os.path.join(PROJECT_ROOT, "cellularity", "estimate_scores.csv")
original_top500_file = os.path.join(PROJECT_ROOT, "phase2", "outputs",
                                     "top500_genes_named.txt")
out_dir = os.path.join(PROJECT_ROOT, "cellularity")
os.makedirs(out_dir, exist_ok=True)

N_TOP_GENES = 500
ENRICHR_LIBRARIES = [
    "KEGG_2021_Human",
    "Reactome_2022",
    "GO_Biological_Process_2023",
    "MSigDB_Hallmark_2020",
]
ADJ_P_THRESHOLD = 0.05

# ---- Step 1: load expression + purity, match samples ----
print("Loading expression matrix...")
expr = pd.read_csv(expr_file, sep="\t")
gene_col = "Hugo_Symbol" if "Hugo_Symbol" in expr.columns else expr.columns[0]
sample_cols_all = [c for c in expr.columns if c not in ("Hugo_Symbol", "Entrez_Gene_Id")]

purity = pd.read_csv(purity_file)
# ESTIMATE's internal I/O converts "-" to "." in sample IDs (same issue
# hit in 02_cox_model_with_purity.R) -- normalize before matching.
purity["PATIENT_ID_NORM"] = (purity["PATIENT_ID"].astype(str)
                              .str.replace(".", "-", regex=False)
                              .str.strip().str.upper())

sample_patient_prefix = pd.Series(sample_cols_all).str[:12]
match_mask = sample_patient_prefix.isin(purity["PATIENT_ID_NORM"])
keep_cols = pd.Series(sample_cols_all)[match_mask].tolist()
print(f"Matched {len(keep_cols)} expression samples to purity scores")

if len(keep_cols) < 100:
    raise SystemExit(
        f"Only {len(keep_cols)} samples matched -- expected ~235. "
        "Check ID normalization before proceeding."
    )

# Build purity vector aligned to keep_cols order
prefix_to_purity = dict(zip(purity["PATIENT_ID_NORM"], purity["TumorPurity"]))
purity_vec = np.array([prefix_to_purity[c[:12]] for c in keep_cols])

# ---- Step 2: clean gene symbols (drop blank/None, collapse duplicates) ----
expr_subset = expr[[gene_col] + keep_cols].rename(columns={gene_col: "GeneSymbol"})
expr_subset = expr_subset[
    expr_subset["GeneSymbol"].notna() &
    (expr_subset["GeneSymbol"] != "") &
    (expr_subset["GeneSymbol"] != "None")
]
n_before = len(expr_subset)
if expr_subset["GeneSymbol"].duplicated().any():
    expr_subset = expr_subset.assign(
        _mean_expr=expr_subset[keep_cols].mean(axis=1)
    ).sort_values("_mean_expr", ascending=False)
    expr_subset = expr_subset.drop_duplicates(subset="GeneSymbol").drop(columns="_mean_expr")
print(f"Gene rows: {n_before} -> {len(expr_subset)} unique genes after dedup")

expr_subset = expr_subset.set_index("GeneSymbol")

# ---- Step 3: residualize each gene's expression against purity ----
print("Residualizing expression against tumour purity (OLS per gene)...")
X = np.column_stack([np.ones_like(purity_vec), purity_vec])  # intercept + purity
Y = expr_subset[keep_cols].values.astype(float)  # genes x samples

# Closed-form OLS for all genes at once: beta = (X'X)^-1 X'Y^T
beta, _, _, _ = np.linalg.lstsq(X, Y.T, rcond=None)
fitted = X @ beta            # samples x genes
residuals = Y.T - fitted     # samples x genes
residual_var = residuals.var(axis=0, ddof=1)  # variance per gene, on residuals

raw_var = Y.var(axis=1, ddof=1)  # original (uncorrected) variance, for reference

variance_df = pd.DataFrame({
    "GeneSymbol": expr_subset.index,
    "raw_variance": raw_var,
    "purity_corrected_variance": residual_var,
})

# ---- Step 4: top-500 gene lists, before vs after correction ----
top500_corrected = (variance_df.sort_values("purity_corrected_variance", ascending=False)
                     .head(N_TOP_GENES)["GeneSymbol"].tolist())

if os.path.exists(original_top500_file):
    with open(original_top500_file) as f:
        top500_original = [line.strip() for line in f if line.strip()]
else:
    print(f"WARNING: {original_top500_file} not found -- falling back to "
          "raw (uncorrected) top-500 from this run instead of Finding 5's "
          "actual original list. Overlap comparison below will not be a "
          "true before/after check.")
    top500_original = (variance_df.sort_values("raw_variance", ascending=False)
                        .head(N_TOP_GENES)["GeneSymbol"].tolist())

overlap = set(top500_original) & set(top500_corrected)
dropped = set(top500_original) - set(top500_corrected)
added = set(top500_corrected) - set(top500_original)

print(f"\nTop-{N_TOP_GENES} gene list overlap: {len(overlap)} / {N_TOP_GENES} "
      f"genes retained after purity correction")
print(f"Dropped (were purity-driven): {len(dropped)} genes")
print(f"Added (newly top-variance after correction): {len(added)} genes")

pd.DataFrame({
    "gene": sorted(dropped)
}).to_csv(os.path.join(out_dir, "genes_dropped_after_purity_correction.csv"), index=False)
pd.DataFrame({
    "gene": sorted(added)
}).to_csv(os.path.join(out_dir, "genes_added_after_purity_correction.csv"), index=False)


# ---- Step 5: Enrichr on the corrected top-500 list ----
def enrichr_analysis(genes, library, description="purity_corrected_top500"):
    add_url = "https://maayanlab.cloud/Enrichr/addList"
    payload = {
        "list": (None, "\n".join(genes)),
        "description": (None, description),
    }
    r = requests.post(add_url, files=payload, timeout=30)
    r.raise_for_status()
    user_list_id = r.json()["userListId"]

    enrich_url = "https://maayanlab.cloud/Enrichr/enrich"
    params = {"userListId": user_list_id, "backgroundType": library}
    r2 = requests.get(enrich_url, params=params, timeout=30)
    r2.raise_for_status()
    return r2.json().get(library, [])


print("\nRunning Enrichr on purity-corrected top-500 gene list...")
all_results = []
for lib in ENRICHR_LIBRARIES:
    print(f"  Querying {lib}...")
    try:
        results = enrichr_analysis(top500_corrected, lib)
    except requests.RequestException as e:
        print(f"  WARNING: Enrichr request failed for {lib}: {e}")
        continue
    for row in results:
        # Enrichr result row: [rank, term, pvalue, zscore, combined_score,
        #                       overlapping_genes, adj_pvalue, old_pvalue, old_adj_pvalue]
        all_results.append({
            "library": lib,
            "term": row[1],
            "p_value": row[2],
            "z_score": row[3],
            "combined_score": row[4],
            "overlap_genes": ";".join(row[5]),
            "adj_p_value": row[6],
        })
    time.sleep(1)  # be polite to the API between library calls

enrichment_df = pd.DataFrame(all_results).sort_values("adj_p_value")
enrichment_df.to_csv(os.path.join(out_dir, "enrichment_corrected_all.csv"), index=False)

significant_df = enrichment_df[enrichment_df["adj_p_value"] < ADJ_P_THRESHOLD]
significant_df.to_csv(os.path.join(out_dir, "enrichment_corrected_significant.csv"), index=False)

# ---- Step 6: specific checks -- did the ribosomal signal survive? ----
ribosome_terms = enrichment_df[
    enrichment_df["term"].str.contains("ribosom|translation", case=False, na=False)
]
emt_terms = enrichment_df[
    enrichment_df["term"].str.contains("epithelial mesenchymal|EMT", case=False, na=False)
]

print("\n============================================")
print(f"Purity-corrected top-{N_TOP_GENES} gene list: {len(top500_corrected)} genes")
print(f"Overlap with original top-500: {len(overlap)}/{N_TOP_GENES}")
print(f"Significant terms (adj p<{ADJ_P_THRESHOLD}): {len(significant_df)}")
print("\nRibosome/translation terms after correction:")
if len(ribosome_terms) > 0:
    print(ribosome_terms[["term", "adj_p_value"]].to_string(index=False))
else:
    print("  NONE FOUND -- ribosomal signal did not survive purity correction")

print("\nEMT terms after correction:")
if len(emt_terms) > 0:
    print(emt_terms[["term", "adj_p_value"]].to_string(index=False))
else:
    print("  NONE FOUND")

print(f"\nWrote full results to:\n  {os.path.join(out_dir, 'enrichment_corrected_all.csv')}")
print(f"Wrote significant-only results to:\n  {os.path.join(out_dir, 'enrichment_corrected_significant.csv')}")
print("============================================")
