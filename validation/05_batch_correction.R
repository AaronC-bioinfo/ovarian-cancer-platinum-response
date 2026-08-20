.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# =============================================================================
# 05_batch_correction.R
# 1. Load GSE63885 gene-level expression (log2 RMA)
# 2. Load TCGA expression (raw RSEM from data_mrna_seq_v2_rsem.txt)
# 3. Intersect gene sets
# 4. Z-score normalize each dataset independently
# 5. Apply ComBat batch correction (platform as batch)
# 6. Export harmonised matrix for Python classifier
# Output: data/external/harmonised_expression.csv
#         data/external/harmonised_metadata.csv
# =============================================================================

cat("=== Step 5: Batch Correction ===\n\n")

OUT_DIR  <- "data/external"

# --- Install sva (ComBat) if needed -----------------------------------------
if (!requireNamespace("sva", quietly = TRUE)) {
  cat("Installing sva package...\n")
  BiocManager::install("sva",
                       lib = "C:/Users/AMAC_WORK/R/library",
                       update = FALSE, ask = FALSE)
}
library(sva)
library(BiocGenerics)

cat("sva loaded OK\n\n")

# --- Load GSE63885 gene-level expression ------------------------------------
cat("Loading GSE63885 gene expression...\n")
geo_expr <- read.csv(file.path(OUT_DIR, "GSE63885_expr_gene.csv"),
                     row.names = 1, check.names = FALSE)
cat("GSE63885:", nrow(geo_expr), "genes x", ncol(geo_expr), "samples\n")

# --- Load TCGA RSEM expression ----------------------------------------------
tcga_path <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018/data_mrna_seq_v2_rsem.txt"

if (!file.exists(tcga_path)) {
  cat("ERROR: Cannot find TCGA RSEM file at:\n", tcga_path, "\n")
  quit(status=1)
}

cat("Loading TCGA expression from:", tcga_path, "\n")
tcga_raw <- read.table(tcga_path, header=TRUE, sep="\t",
                       row.names=NULL, check.names=FALSE,
                       comment.char="", quote="")

# First column is Hugo_Symbol, second may be Entrez_Gene_Id
gene_col <- 1
if (ncol(tcga_raw) > 1 && colnames(tcga_raw)[2] == "Entrez_Gene_Id") {
  gene_col <- 1
  tcga_raw <- tcga_raw[, -2]  # drop Entrez column
}

# Set gene symbols as row names, handle duplicates by keeping max mean
gene_names <- tcga_raw[[1]]
tcga_raw   <- tcga_raw[, -1]  # drop gene name column

cat("TCGA raw dimensions:", length(gene_names), "genes x", ncol(tcga_raw), "samples\n")

# Remove NA or empty gene names
keep <- !is.na(gene_names) & nchar(trimws(gene_names)) > 0
tcga_raw   <- tcga_raw[keep, ]
gene_names <- gene_names[keep]

# Convert to numeric matrix
tcga_mat <- as.matrix(tcga_raw)
mode(tcga_mat) <- "numeric"
rownames(tcga_mat) <- gene_names

# Handle duplicate gene names: keep row with max mean expression
cat("Handling duplicate gene names...\n")
row_means  <- rowMeans(tcga_mat, na.rm=TRUE)
ord        <- order(gene_names, -row_means)
tcga_mat   <- tcga_mat[ord, ]
gene_names <- gene_names[ord]
tcga_mat   <- tcga_mat[!duplicated(gene_names), ]
cat("After deduplication:", nrow(tcga_mat), "genes\n")

# Log2 transform RSEM (add 1 pseudocount to handle zeros)
cat("Log2-transforming TCGA RSEM values (log2(x+1))...\n")
tcga_mat[tcga_mat < 0] <- 0  # floor negatives at 0
tcga_log <- log2(tcga_mat + 1)

cat("TCGA log2 value range:",
    round(min(tcga_log, na.rm=TRUE), 2), "to",
    round(max(tcga_log, na.rm=TRUE), 2), "\n\n")

# --- Intersect gene sets ----------------------------------------------------
cat("Intersecting gene sets...\n")
geo_genes  <- rownames(geo_expr)
tcga_genes <- rownames(tcga_log)
common_genes <- intersect(geo_genes, tcga_genes)
cat("GSE63885 genes:", length(geo_genes), "\n")
cat("TCGA genes:    ", length(tcga_genes), "\n")
cat("Common genes:  ", length(common_genes), "\n\n")

geo_sub  <- as.matrix(geo_expr[common_genes, ])
tcga_sub <- tcga_log[common_genes, ]

# --- Z-score normalize each dataset independently ---------------------------
cat("Z-score normalizing each dataset independently (per gene)...\n")

zscore_rows <- function(mat) {
  # z-score each gene (row) across samples
  m <- rowMeans(mat, na.rm=TRUE)
  s <- apply(mat, 1, sd, na.rm=TRUE)
  s[s == 0] <- 1  # avoid division by zero for constant genes
  t(scale(t(mat), center=m, scale=s))
}

geo_z  <- zscore_rows(geo_sub)
tcga_z <- zscore_rows(tcga_sub)

cat("GSE63885 z-scored range:",
    round(min(geo_z, na.rm=TRUE), 2), "to",
    round(max(geo_z, na.rm=TRUE), 2), "\n")
cat("TCGA z-scored range:",
    round(min(tcga_z, na.rm=TRUE), 2), "to",
    round(max(tcga_z, na.rm=TRUE), 2), "\n\n")

# --- Filter low-variance genes before ComBat --------------------------------
cat("Filtering low-variance genes before ComBat...\n")

# Remove genes with near-zero variance in either batch
var_geo  <- apply(geo_z,  1, var, na.rm=TRUE)
var_tcga <- apply(tcga_z, 1, var, na.rm=TRUE)
keep_var <- var_geo > 1e-6 & var_tcga > 1e-6 & !is.na(var_geo) & !is.na(var_tcga)

geo_z_f  <- geo_z[keep_var, ]
tcga_z_f <- tcga_z[keep_var, ]
cat("Genes after variance filter:", sum(keep_var), "of", length(keep_var), "\n\n")

# --- Combine and run ComBat -------------------------------------------------
cat("Combining matrices for ComBat...\n")
combined <- cbind(tcga_z_f, geo_z_f)
batch    <- c(rep(1, ncol(tcga_z_f)),   # batch 1 = TCGA (RNA-seq)
              rep(2, ncol(geo_z_f)))     # batch 2 = GSE63885 (microarray)

cat("Combined dimensions:", nrow(combined), "genes x", ncol(combined), "samples\n")
cat("Batch 1 (TCGA):", sum(batch==1), "| Batch 2 (GEO):", sum(batch==2), "\n\n")

cat("Running ComBat...\n")
corrected <- ComBat(dat=combined, batch=batch, mod=NULL,
                    par.prior=TRUE, prior.plots=FALSE)
cat("ComBat complete\n\n")

# --- Split back into TCGA and GEO -------------------------------------------
tcga_corrected <- corrected[, batch == 1]
geo_corrected  <- corrected[, batch == 2]
cat("Genes retained after ComBat:", nrow(geo_corrected), "\n")

cat("Post-ComBat GEO range:",
    round(min(geo_corrected, na.rm=TRUE), 2), "to",
    round(max(geo_corrected, na.rm=TRUE), 2), "\n")

# =============================================================================
# --- Cross-platform alignment diagnostics -----------------------------------
# Added 2026-07-20 (Phase 2 of AUDIT_2026-07-20.md fixes).
# The manuscript Methods/Results report two diagnostics that were described
# but never computed in code:
#   (A) post-ComBat inter-platform Pearson correlation of gene-level mean
#       expression  (manuscript value: r = -0.005)
#   (B) variance of TCGA's top-500 selected genes vs variance of all genes,
#       measured within the GEO dataset itself  (manuscript value: ratio ~1.00)
# Both are written to validation/outputs/combat_diagnostics.csv so the claim
# is backed by a reproducible artifact rather than prose alone.
# =============================================================================
cat("\n--- Computing cross-platform alignment diagnostics ---\n")

DIAG_DIR <- "validation/outputs"
if (!dir.exists(DIAG_DIR)) dir.create(DIAG_DIR, recursive = TRUE)

# (A) Inter-platform Pearson correlation of gene-level mean expression,
#     computed on the common genes AFTER ComBat correction.
tcga_gene_mean <- rowMeans(tcga_corrected, na.rm = TRUE)
geo_gene_mean  <- rowMeans(geo_corrected,  na.rm = TRUE)
stopifnot(length(tcga_gene_mean) == length(geo_gene_mean))
combat_pearson_r <- cor(tcga_gene_mean, geo_gene_mean,
                        method = "pearson", use = "complete.obs")
cat(sprintf("(A) post-ComBat inter-platform Pearson r (gene-level mean) = %.6f\n",
            combat_pearson_r))

# (B) Variance ratio: TCGA's top-500 variance-selected genes vs all genes,
#     with variance measured in the GEO dataset's own (pre-ComBat, log2 RMA)
#     expression. Selection uses variance on the TCGA log2 matrix (the same
#     unsupervised criterion the classifier pipeline uses), restricted to the
#     genes common to both platforms.
top_n_sel   <- 500
tcga_var_log <- apply(tcga_sub, 1, var, na.rm = TRUE)   # tcga_sub = TCGA log2, common genes
n_sel        <- min(top_n_sel, sum(!is.na(tcga_var_log)))
top_genes    <- names(sort(tcga_var_log, decreasing = TRUE))[seq_len(n_sel)]

geo_var_log  <- apply(geo_sub, 1, var, na.rm = TRUE)    # geo_sub  = GEO log2 RMA, common genes
mean_var_selected_in_geo <- mean(geo_var_log[top_genes], na.rm = TRUE)
mean_var_all_in_geo      <- mean(geo_var_log,            na.rm = TRUE)
variance_ratio <- mean_var_selected_in_geo / mean_var_all_in_geo
cat(sprintf("(B) TCGA-top%d variance / all-gene variance, measured in GEO = %.4f\n",
            n_sel, variance_ratio))

combat_diag <- data.frame(
  metric = c("post_combat_interplatform_pearson_r",
             "geo_variance_ratio_tcga_top500_vs_all",
             "n_common_genes",
             "n_tcga_selected_genes",
             "mean_var_selected_genes_in_geo",
             "mean_var_all_genes_in_geo"),
  value = c(combat_pearson_r,
            variance_ratio,
            length(common_genes),
            n_sel,
            mean_var_selected_in_geo,
            mean_var_all_in_geo),
  manuscript_value = c(-0.005, 1.00, NA, 500, NA, NA),
  stringsAsFactors = FALSE
)
write.csv(combat_diag, file.path(DIAG_DIR, "combat_diagnostics.csv"),
          row.names = FALSE, quote = FALSE)
cat("Saved", file.path(DIAG_DIR, "combat_diagnostics.csv"), "\n")

# Loud flag if the computed values diverge materially from the manuscript claim.
if (abs(combat_pearson_r - (-0.005)) > 0.05) {
  cat("\n*** WARNING: post-ComBat Pearson r =", round(combat_pearson_r, 4),
      "differs materially from the manuscript's -0.005 ***\n")
  cat("*** The manuscript external-validation claim must be updated. ***\n")
}
if (abs(variance_ratio - 1.00) > 0.15) {
  cat("\n*** WARNING: variance ratio =", round(variance_ratio, 4),
      "differs materially from the manuscript's ~1.00 ***\n")
  cat("*** The manuscript external-validation claim must be updated. ***\n")
}
cat("--- Diagnostics complete ---\n\n")

# --- Load and merge metadata ------------------------------------------------
cat("Loading GSE63885 metadata...\n")
meta  <- read.csv(file.path(OUT_DIR, "GSE63885_meta_clean.csv"),
                  stringsAsFactors=FALSE)
plat  <- read.csv(file.path(OUT_DIR, "GSE63885_plat_fix.csv"),
                  stringsAsFactors=FALSE)

# Merge labels into metadata
meta <- merge(meta, plat[, c("sample_id", "platinum_sensitivity_raw",
                               "platinum_label_dfs")],
              by="sample_id", all.x=TRUE)

# Keep only samples present in corrected GEO matrix
keep_samples <- intersect(meta$sample_id, colnames(geo_corrected))
meta_final   <- meta[meta$sample_id %in% keep_samples, ]

# --- Save outputs -----------------------------------------------------------
cat("\nSaving outputs...\n")

# GEO harmonised expression (genes x samples)
geo_out <- as.data.frame(geo_corrected[, meta_final$sample_id])
write.csv(geo_out, file.path(OUT_DIR, "harmonised_expression.csv"), quote=FALSE)

# TCGA corrected expression (for reference / re-training if needed)
write.csv(as.data.frame(tcga_corrected),
          file.path(OUT_DIR, "tcga_corrected_expression.csv"), quote=FALSE)

# Metadata with labels
write.csv(meta_final, file.path(OUT_DIR, "harmonised_metadata.csv"),
          row.names=FALSE, quote=FALSE)

cat("Saved harmonised_expression.csv  -",
    nrow(geo_out), "genes x", ncol(geo_out), "samples\n")
cat("Saved tcga_corrected_expression.csv\n")
cat("Saved harmonised_metadata.csv    -", nrow(meta_final), "samples\n")

cat("\n=== Step 5 Complete ===\n")
cat("Next: run Python validate_external.py\n")

