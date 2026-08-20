## ============================================================
## Enhancement 4 — Step 1: Extract BRCA1/2 mutation status from MAF
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## No precomputed BRCA1/2 status column exists in the clinical files
## (confirmed via 00_inspect_hrd_data.R) -- deriving it from the MAF-format
## data_mutations.txt instead.

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(data.table)

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
tcga_path <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

maf_file <- file.path(tcga_path, "data_mutations.txt")
out_dir  <- file.path(project_root, "hrd")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out_csv  <- file.path(out_dir, "brca_status.csv")

cat("Loading MAF file (this can be large)...\n")
maf <- fread(maf_file, header = TRUE, sep = "\t", data.table = FALSE,
             quote = "", showProgress = TRUE)

cat("MAF dimensions:", nrow(maf), "rows x", ncol(maf), "columns\n")
cat("Confirming expected columns present: Hugo_Symbol, Variant_Classification, Tumor_Sample_Barcode\n")
required <- c("Hugo_Symbol", "Variant_Classification", "Tumor_Sample_Barcode")
missing_req <- setdiff(required, names(maf))
if (length(missing_req) > 0) {
  stop("MAF file is missing expected column(s): ", paste(missing_req, collapse = ", "),
       "\nActual columns: ", paste(names(maf), collapse = ", "))
}

## ---- Subset to BRCA1/BRCA2 rows only ----
brca_rows <- maf[maf$Hugo_Symbol %in% c("BRCA1", "BRCA2"), ]
cat("\nTotal BRCA1/BRCA2 mutation calls (any type):", nrow(brca_rows), "\n")

## ---- Diagnostic: show the ACTUAL variant classification breakdown
## before deciding what counts as a functionally relevant mutation,
## rather than assuming a standard non-silent list blind. ----
cat("\n=== Variant_Classification breakdown for BRCA1/BRCA2 calls ===\n")
print(table(brca_rows$Hugo_Symbol, brca_rows$Variant_Classification))

## Standard "non-silent" MAF classification set (MutSigCV / TCGA convention)
## -- mutations expected to alter protein function, used broadly in cancer
## genomics to define a gene as "mutated" for downstream covariate purposes.
non_silent_classes <- c(
  "Missense_Mutation", "Nonsense_Mutation", "Frame_Shift_Del", "Frame_Shift_Ins",
  "In_Frame_Del", "In_Frame_Ins", "Splice_Site", "Nonstop_Mutation",
  "Translation_Start_Site", "De_novo_Start_OutOfFrame", "De_novo_Start_InFrame"
)

present_non_silent <- intersect(non_silent_classes, unique(brca_rows$Variant_Classification))
present_other <- setdiff(unique(brca_rows$Variant_Classification), non_silent_classes)
cat("\nNon-silent classes present in this data:", paste(present_non_silent, collapse = ", "), "\n")
cat("Other (excluded) classes present in this data:", paste(present_other, collapse = ", "), "\n")

brca_functional <- brca_rows[brca_rows$Variant_Classification %in% non_silent_classes, ]
cat("\nBRCA1/BRCA2 calls retained after non-silent filter:", nrow(brca_functional),
    "of", nrow(brca_rows), "total calls\n")

## ---- Build per-patient status ----
## Tumor_Sample_Barcode is typically the full sample barcode (e.g.
## TCGA-04-1331-01); patient ID is the first 12 characters.
brca_functional$PATIENT_ID <- substr(brca_functional$Tumor_Sample_Barcode, 1, 12)

brca1_patients <- unique(brca_functional$PATIENT_ID[brca_functional$Hugo_Symbol == "BRCA1"])
brca2_patients <- unique(brca_functional$PATIENT_ID[brca_functional$Hugo_Symbol == "BRCA2"])
either_patients <- union(brca1_patients, brca2_patients)

## ---- Need the full patient list (all patients with mutation data
## available) to correctly assign 0 = "no mutation found" rather than
## just listing the mutated ones ----
all_mutation_patients <- unique(substr(maf$Tumor_Sample_Barcode, 1, 12))
cat("\nTotal patients with any mutation data:", length(all_mutation_patients), "\n")

status_df <- data.frame(
  PATIENT_ID = all_mutation_patients,
  BRCA1_mutated = as.integer(all_mutation_patients %in% brca1_patients),
  BRCA2_mutated = as.integer(all_mutation_patients %in% brca2_patients)
)
status_df$BRCA_any_mutated <- as.integer(status_df$BRCA1_mutated == 1 | status_df$BRCA2_mutated == 1)

write.csv(status_df, out_csv, row.names = FALSE)

cat("\n============================================\n")
cat("BRCA1 mutated (non-silent):", length(brca1_patients), "patients\n")
cat("BRCA2 mutated (non-silent):", length(brca2_patients), "patients\n")
cat("Either BRCA1 or BRCA2 mutated:", length(either_patients), "patients\n")
cat("Total patients in mutation data:", length(all_mutation_patients), "patients\n")
cat("Wrote per-patient BRCA status to:\n  ", out_csv, "\n")
cat("============================================\n")
