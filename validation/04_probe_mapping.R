.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# =============================================================================
# 04_probe_mapping.R
# Map Affymetrix GPL570 probe IDs to gene symbols using hgu133plus2.db
# Collapse multi-probe genes by max mean expression
# Filter to serous/undifferentiated samples only
# Output: data/external/GSE63885_expr_gene.csv
# =============================================================================

cat("=== Step 4: Probe-to-Gene Mapping ===\n\n")

OUT_DIR <- "data/external"

# --- Install Bioconductor + hgu133plus2.db if needed ------------------------
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  cat("Installing BiocManager...\n")
  install.packages("BiocManager",
                   lib  = "C:/Users/AMAC_WORK/R/library",
                   repos = "https://cloud.r-project.org")
}
library(BiocManager)

if (!requireNamespace("hgu133plus2.db", quietly = TRUE)) {
  cat("Installing hgu133plus2.db (Bioconductor annotation package)...\n")
  BiocManager::install("hgu133plus2.db",
                       lib  = "C:/Users/AMAC_WORK/R/library",
                       update = FALSE, ask = FALSE)
}
library(hgu133plus2.db)

cat("hgu133plus2.db loaded OK\n\n")

# --- Load raw expression matrix for GSE63885 --------------------------------
cat("Loading GSE63885 expression matrix...\n")
expr_raw <- read.csv(file.path(OUT_DIR, "GSE63885_expr_raw.csv"),
                     row.names = 1, check.names = FALSE)
cat("Raw dimensions:", nrow(expr_raw), "probes x", ncol(expr_raw), "samples\n")

# --- Load clean metadata to get serous/undiff sample IDs --------------------
meta <- read.csv(file.path(OUT_DIR, "GSE63885_meta_clean.csv"),
                 stringsAsFactors = FALSE)
serous_ids <- meta$sample_id
cat("Serous/undiff sample IDs:", length(serous_ids), "\n")

# Filter expression to serous/undiff samples only
common_ids <- intersect(serous_ids, colnames(expr_raw))
cat("Matching sample IDs found in expr matrix:", length(common_ids), "\n")
expr <- expr_raw[, common_ids]
cat("After sample filter:", nrow(expr), "probes x", ncol(expr), "samples\n\n")

# --- Map probe IDs to gene symbols ------------------------------------------
cat("Mapping probe IDs to gene symbols...\n")

probe_ids <- rownames(expr)

# Use hgu133plus2SYMBOL to map probe → gene symbol
symbol_map <- mapIds(hgu133plus2.db,
                     keys    = probe_ids,
                     column  = "SYMBOL",
                     keytype = "PROBEID",
                     multiVals = "first")

cat("Total probes:", length(probe_ids), "\n")
cat("Probes with gene symbol:", sum(!is.na(symbol_map)), "\n")
cat("Probes without mapping:", sum(is.na(symbol_map)), "\n\n")

# --- Collapse multi-probe genes: keep probe with max mean expression --------
cat("Collapsing multi-probe genes (max mean expression)...\n")

# Add gene symbols to expression matrix
expr$gene_symbol <- symbol_map[rownames(expr)]

# Remove probes without gene symbol
expr_mapped <- expr[!is.na(expr$gene_symbol), ]
cat("Probes after removing unmapped:", nrow(expr_mapped), "\n")

# For each gene, keep probe with highest mean expression across samples
sample_cols <- setdiff(colnames(expr_mapped), "gene_symbol")

expr_num <- expr_mapped[, sample_cols]
# Ensure numeric
expr_num <- as.data.frame(lapply(expr_num, as.numeric))
rownames(expr_num) <- rownames(expr_mapped)

expr_num$gene_symbol <- expr_mapped$gene_symbol
expr_num$mean_expr   <- rowMeans(expr_num[, sample_cols], na.rm = TRUE)

# Sort by mean expression descending, keep first occurrence per gene
expr_sorted <- expr_num[order(expr_num$gene_symbol, -expr_num$mean_expr), ]
expr_collapsed <- expr_sorted[!duplicated(expr_sorted$gene_symbol), ]

# Set gene symbol as row name
rownames(expr_collapsed) <- expr_collapsed$gene_symbol
expr_gene <- expr_collapsed[, sample_cols]

cat("Genes after collapsing:", nrow(expr_gene), "\n\n")

# --- Quick sanity check ------------------------------------------------------
cat("=== Sanity Check ===\n")
cat("Expression matrix dimensions:", nrow(expr_gene), "genes x", 
    ncol(expr_gene), "samples\n")
cat("Value range (should be log2 RMA ~3-14):",
    round(min(expr_gene, na.rm=TRUE), 2), "to",
    round(max(expr_gene, na.rm=TRUE), 2), "\n")
cat("Any NAs:", sum(is.na(expr_gene)), "\n")
cat("Sample genes: ", paste(rownames(expr_gene)[1:5], collapse=", "), "\n\n")

# --- Save output -------------------------------------------------------------
out_path <- file.path(OUT_DIR, "GSE63885_expr_gene.csv")
write.csv(expr_gene, out_path, quote = FALSE)
cat("Saved:", out_path, "\n")
cat("Dimensions:", nrow(expr_gene), "genes x", ncol(expr_gene), "samples\n")

cat("\n=== Step 4 Complete ===\n")
cat("Next: run 05_batch_correction.R\n")
