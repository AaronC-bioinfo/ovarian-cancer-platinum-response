## ============================================================
## Enhancement 4 — Step 0: Locate HRD score + BRCA1/2 status columns
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## Same lesson as Enhancement 3: inspect actual column names before
## writing any model code, rather than guessing and debugging blind.

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(data.table)

tcga_path <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

cat("============================================\n")
cat("Files available in TCGA-OV data directory:\n")
cat("============================================\n")
print(list.files(tcga_path))

## ---- Clinical sample file (per Enhancement 3/4 handoff, HRD + BRCA
## status are expected here) ----
sample_file  <- file.path(tcga_path, "data_clinical_sample.txt")
patient_file <- file.path(tcga_path, "data_clinical_patient.txt")

inspect_clinical_file <- function(path, label) {
  if (!file.exists(path)) {
    cat("\n", label, "NOT FOUND at:", path, "\n")
    return(invisible(NULL))
  }
  cat("\n============================================\n")
  cat(label, "\n")
  cat("============================================\n")

  ## cBioPortal clinical files have 4 metadata header lines starting with
  ## '#' before the real header row -- skip them, but also print raw
  ## first few lines in case the format differs from expectation.
  raw_lines <- readLines(path, n = 6)
  cat("First 6 raw lines (to confirm header row location):\n")
  for (i in seq_along(raw_lines)) {
    cat(sprintf("  [%d] %s\n", i, substr(raw_lines[i], 1, 150)))
  }

  n_header_lines <- sum(startsWith(raw_lines, "#"))
  df <- fread(path, skip = n_header_lines, header = TRUE, data.table = FALSE)
  cat("\nDetected", n_header_lines, "'#' header lines; data header row: line", n_header_lines + 1, "\n")
  cat("Dimensions:", nrow(df), "rows x", ncol(df), "columns\n\n")

  cat("All column names:\n")
  print(names(df))

  ## Search for anything HRD- or BRCA-related
  hrd_cols   <- grep("HRD", names(df), ignore.case = TRUE, value = TRUE)
  brca_cols  <- grep("BRCA", names(df), ignore.case = TRUE, value = TRUE)
  loh_cols   <- grep("LOH|LST|TAI|SCAR", names(df), ignore.case = TRUE, value = TRUE)  # HRD sub-scores
  mut_cols   <- grep("MUT|GERMLINE|SOMATIC", names(df), ignore.case = TRUE, value = TRUE)

  cat("\n--- Candidate HRD-related columns ---\n")
  if (length(hrd_cols) > 0) print(hrd_cols) else cat("  (none found)\n")

  cat("\n--- Candidate BRCA-related columns ---\n")
  if (length(brca_cols) > 0) print(brca_cols) else cat("  (none found)\n")

  cat("\n--- Candidate HRD sub-score columns (LOH/LST/TAI/SCAR) ---\n")
  if (length(loh_cols) > 0) print(loh_cols) else cat("  (none found)\n")

  cat("\n--- Candidate mutation-status columns ---\n")
  if (length(mut_cols) > 0) print(mut_cols) else cat("  (none found)\n")

  ## If any candidates found, show a value preview
  all_candidates <- unique(c(hrd_cols, brca_cols, loh_cols, mut_cols))
  if (length(all_candidates) > 0) {
    cat("\n--- Value preview for candidate columns (first 10 rows) ---\n")
    print(head(df[, all_candidates, drop = FALSE], 10))
    cat("\n--- Summary of candidate columns ---\n")
    for (col in all_candidates) {
      cat("\n", col, ":\n", sep = "")
      if (is.numeric(df[[col]])) {
        print(summary(df[[col]]))
      } else {
        print(table(df[[col]], useNA = "ifany"))
      }
    }
  }

  invisible(df)
}

sample_df  <- inspect_clinical_file(sample_file, "data_clinical_sample.txt")
patient_df <- inspect_clinical_file(patient_file, "data_clinical_patient.txt")

## ---- Check for a mutations file too, in case BRCA1/2 status lives
## there instead (common in cBioPortal exports as data_mutations.txt) ----
mutation_candidates <- list.files(tcga_path, pattern = "mutation", ignore.case = TRUE)
cat("\n============================================\n")
cat("Files matching 'mutation' in filename:\n")
print(mutation_candidates)
cat("============================================\n")

cat("\nDone. Review the candidate column lists above, then tell me which\n")
cat("columns actually hold HRD score and BRCA1/2 status so I can write\n")
cat("02_cox_model_with_hrd.R against the real column names.\n")
