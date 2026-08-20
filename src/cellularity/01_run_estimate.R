## ============================================================
## Enhancement 3 — Step 1: Run ESTIMATE on the platinum-treated cohort
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## Reuses the SAME 432-patient platinum-treated cohort already
## established in Finding 4 (phase2/outputs/cox_patients_with_risk.csv)
## rather than re-deriving the AGENT-field filter, so purity scores
## line up 1:1 with the existing Cox model patients.

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(estimate)
library(data.table)

## ---- Paths ----
project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
tcga_path    <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

expr_file    <- file.path(tcga_path, "data_mrna_seq_v2_rsem.txt")
cohort_file  <- file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv")

out_dir <- file.path(project_root, "cellularity")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

gct_raw_file      <- file.path(out_dir, "tcga_ov_platinum_expr.gct")
gct_filtered_file <- file.path(out_dir, "tcga_ov_platinum_expr_filtered.gct")
gct_score_file    <- file.path(out_dir, "estimate_score.gct")
scores_csv        <- file.path(out_dir, "estimate_scores.csv")

## ---- Step A: load expression matrix (cBioPortal RSEM format) ----
cat("Loading expression matrix...\n")
expr <- fread(expr_file, header = TRUE, sep = "\t", data.table = FALSE)

## cBioPortal RSEM files have Hugo_Symbol + Entrez_Gene_Id as first two columns
gene_col <- if ("Hugo_Symbol" %in% names(expr)) "Hugo_Symbol" else names(expr)[1]
sample_cols_all <- setdiff(names(expr), c("Hugo_Symbol", "Entrez_Gene_Id"))

## ---- Step B: load the platinum-treated cohort (432 patients) ----
cohort <- fread(cohort_file, data.table = FALSE)
patient_id_col <- if ("PATIENT_ID" %in% names(cohort)) "PATIENT_ID" else names(cohort)[1]
platinum_ids <- unique(cohort[[patient_id_col]])
cat("Platinum-treated cohort loaded:", length(platinum_ids), "patients\n")

## TCGA sample barcodes are longer than patient IDs (patient ID is first
## 12 chars, e.g. TCGA-XX-XXXX). Match on that prefix.
sample_patient_prefix <- substr(sample_cols_all, 1, 12)
keep_cols <- sample_cols_all[sample_patient_prefix %in% platinum_ids]

cat("Expression samples matched to platinum cohort:", length(keep_cols),
    "of", length(platinum_ids), "expected\n")

## NOTE: not every patient in the 432-patient clinical Cox cohort has RNA-seq
## on file -- Finding 5's pathway enrichment already ran on a smaller
## "platinum-treated subset (252 samples)" for this same reason. A match
## count in that ballpark (roughly 230-260) is expected, not an error. Only
## worry if the count is drastically lower (e.g. <100), which would suggest
## a barcode-format mismatch rather than genuine missing RNA-seq data.
if (length(keep_cols) < 100) {
  warning("Only ", length(keep_cols), " of ", length(platinum_ids),
          " platinum-treated patients matched an expression sample column ",
          "-- well below the ~252 seen in Finding 5, likely a barcode-format ",
          "mismatch rather than missing RNA-seq data.")
}

expr_subset <- expr[, c(gene_col, keep_cols)]
names(expr_subset)[1] <- "GeneSymbol"

## ---- Step C0: drop missing symbols and collapse duplicates ----
## RSEM files commonly have blank/"None" symbols and multiple rows sharing
## the same Hugo_Symbol (different loci/probes). filterCommonGenes() uses
## the symbol as a row name internally, which requires uniqueness -- for
## duplicates, keep the row with the highest mean expression (standard
## practice: the most-expressed probe is the most informative one to keep).
n_before <- nrow(expr_subset)
expr_subset <- expr_subset[!is.na(expr_subset$GeneSymbol) &
                              expr_subset$GeneSymbol != "" &
                              expr_subset$GeneSymbol != "None", ]
n_dup <- sum(duplicated(expr_subset$GeneSymbol))
if (n_dup > 0) {
  mean_expr <- rowMeans(as.matrix(expr_subset[, keep_cols]), na.rm = TRUE)
  expr_subset <- expr_subset[order(-mean_expr), ]
  expr_subset <- expr_subset[!duplicated(expr_subset$GeneSymbol), ]
}
cat("Gene rows: ", n_before, "-> dropped blank/None symbols and", n_dup,
    "duplicate symbols ->", nrow(expr_subset), "unique genes remaining\n")

## ---- Step C: write plain tab-delimited text (filterCommonGenes' actual
## expected input -- NOT a pre-built GCT). filterCommonGenes() itself
## produces the GCT as output; feeding it an already-GCT'd file (via
## outputGCT() first) renames the ID column to NAME/Description and
## silently breaks id="GeneSymbol" matching (0 genes matched bug). ----
cat("Writing tab-delimited expression file for ESTIMATE...\n")
tmp_txt <- file.path(out_dir, "_tmp_platinum_expr.txt")
write.table(expr_subset, tmp_txt, sep = "\t", quote = FALSE, row.names = FALSE)

## ---- Step D: filter to ESTIMATE's common gene list, then score ----
cat("Filtering to ESTIMATE common gene set...\n")
filterCommonGenes(
  input.f  = tmp_txt,
  output.f = gct_filtered_file,
  id       = "GeneSymbol"
)

cat("Running estimateScore (platform = 'illumina', RNA-seq)...\n")
estimateScore(
  input.ds  = gct_filtered_file,
  output.ds = gct_score_file,
  platform  = "illumina"
)

## ---- Step E: read scores back, compute derived tumour purity ----
scores_raw <- read.table(gct_score_file, skip = 2, header = TRUE, sep = "\t",
                          row.names = 1, check.names = FALSE)
scores_raw$Description <- NULL
scores_t <- as.data.frame(t(scores_raw))
scores_t$SAMPLE_BARCODE <- rownames(scores_t)
scores_t$PATIENT_ID     <- substr(scores_t$SAMPLE_BARCODE, 1, 12)

## Standard ESTIMATE -> tumour purity conversion (Yoshihara et al. 2013,
## Nat Commun) — validated for RNA-seq / Illumina platform scores.
scores_t$TumorPurity <- cos(0.6049872018 + 0.0001467884 * scores_t$ESTIMATEScore)

scores_t <- scores_t[, c("PATIENT_ID", "SAMPLE_BARCODE",
                          "StromalScore", "ImmuneScore", "ESTIMATEScore",
                          "TumorPurity")]

write.csv(scores_t, scores_csv, row.names = FALSE)

cat("\n============================================\n")
cat("Done. Wrote", nrow(scores_t), "patient purity scores to:\n  ", scores_csv, "\n")
cat("Purity range: [", round(min(scores_t$TumorPurity), 3), ",",
    round(max(scores_t$TumorPurity), 3), "]\n")
cat("Next step: cox_model_with_purity.R (add TumorPurity as a Cox covariate)\n")
cat("============================================\n")

file.remove(tmp_txt)
