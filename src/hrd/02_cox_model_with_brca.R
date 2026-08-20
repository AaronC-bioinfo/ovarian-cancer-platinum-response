## ============================================================
## Enhancement 4 "” Step 2: Cox model with BRCA1/2 mutation status
## Ovarian Cancer Platinum Response Project
## ============================================================

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(survival)
library(data.table)

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
cohort_file  <- file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv")
brca_file    <- file.path(project_root, "hrd/brca_status.csv")
out_dir      <- file.path(project_root, "hrd")

cohort <- fread(cohort_file, data.table = FALSE)
brca   <- fread(brca_file, data.table = FALSE)

cat("cox_patients_with_risk.csv columns:\n  ", paste(names(cohort), collapse = ", "), "\n\n")

find_col <- function(df, candidates, label) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0) {
    stop("Could not find a column for '", label, "' in cox_patients_with_risk.csv.\n",
         "Looked for: ", paste(candidates, collapse = ", "), "\n",
         "Actual columns are: ", paste(names(df), collapse = ", "))
  }
  hit[1]
}

col_patient <- find_col(cohort, c("PATIENT_ID", "PatientID"), "patient ID")
col_os_time <- find_col(cohort, c("OS_MONTHS", "os_time"), "overall survival time")
col_os_stat <- find_col(cohort, c("OS_STATUS", "OS_EVENT", "os_event"), "overall survival status")
col_aneup   <- find_col(cohort, c("ANEUPLOIDY_SCORE", "aneu"), "aneuploidy score")

if ("log_tmb" %in% names(cohort)) {
  tmb_term <- "log_tmb"
} else if ("LOG_TMB" %in% names(cohort)) {
  tmb_term <- "LOG_TMB"
} else {
  col_tmb  <- find_col(cohort, c("TMB_NONSYNONYMOUS", "TMB", "tmb"), "TMB")
  tmb_term <- paste0("log1p(", col_tmb, ")")
}
cat("Using TMB term:", tmb_term, "\n")

os_status_raw <- cohort[[col_os_stat]]
if (is.character(os_status_raw)) {
  cohort$OS_STATUS_NUM <- as.integer(grepl("DECEASED|1", os_status_raw))
} else {
  cohort$OS_STATUS_NUM <- as.integer(os_status_raw)
}

## ---- Normalize IDs defensively before merging (cheap insurance after
## the dot/dash surprise in Enhancement 3, even though MAF barcodes are
## standard TCGA format and shouldn't need it) ----
normalize_id <- function(x) toupper(trimws(gsub("[.]", "-", x)))
cohort$.join_id <- normalize_id(cohort[[col_patient]])
brca$.join_id   <- normalize_id(brca$PATIENT_ID)

cat("Sample cohort IDs:", paste(head(cohort[[col_patient]], 3), collapse = ", "), "\n")
cat("Sample BRCA IDs:  ", paste(head(brca$PATIENT_ID, 3), collapse = ", "), "\n")

merged <- merge(cohort, brca[, c(".join_id", "BRCA1_mutated", "BRCA2_mutated", "BRCA_any_mutated")],
                 by = ".join_id")
merged$.join_id <- NULL
cat("\nPatients with both clinical covariates and BRCA status:", nrow(merged), "\n")
cat("BRCA-mutant patients in this cohort:", sum(merged$BRCA_any_mutated), "\n\n")

if (nrow(merged) == 0) {
  stop("0 matches after ID normalization -- compare the sample ID lines above.")
}

## ---- Model A: baseline, refit on the matched subset for a fair
## comparison ----
fmla_baseline <- as.formula(paste0(
  "Surv(", col_os_time, ", OS_STATUS_NUM) ~ ", tmb_term, " + ", col_aneup
))
cox_baseline <- coxph(fmla_baseline, data = merged)

## ---- Model B: BRCA-added ----
fmla_brca <- as.formula(paste0(
  "Surv(", col_os_time, ", OS_STATUS_NUM) ~ ", tmb_term, " + ",
  col_aneup, " + BRCA_any_mutated"
))
cox_brca <- coxph(fmla_brca, data = merged)

cat("=== Baseline model (matched n, no BRCA) ===\n")
print(summary(cox_baseline))
cat("\n=== BRCA-added model ===\n")
print(summary(cox_brca))

ph_test <- cox.zph(cox_brca)
cat("\n=== Schoenfeld PH test (BRCA-added model) ===\n")
print(ph_test)

extract_hr <- function(model, label) {
  s <- summary(model)
  data.frame(
    model     = label,
    term      = rownames(s$coefficients),
    HR        = s$coefficients[, "exp(coef)"],
    p_value   = s$coefficients[, "Pr(>|z|)"],
    c_index   = s$concordance["C"],
    row.names = NULL
  )
}

comparison <- rbind(
  extract_hr(cox_baseline, "baseline_matched"),
  extract_hr(cox_brca,     "brca_added")
)

out_csv <- file.path(out_dir, "cox_hazard_ratios_brca.csv")
write.csv(comparison, out_csv, row.names = FALSE)

## ---- Persist matched-subset size + summary â†’ CSV ----
## Added 2026-07-20 (Phase 3 of AUDIT_2026-07-20.md fixes). The manuscript
## cites the matched-subset size (n=335) but it was only printed to stdout.
brca_summary <- data.frame(
  metric = c("n_matched_subset", "n_brca_mutant",
             "c_index_baseline", "c_index_brca_added"),
  value  = c(nrow(merged), sum(merged$BRCA_any_mutated),
             round(summary(cox_baseline)$concordance["C"], 4),
             round(summary(cox_brca)$concordance["C"], 4)),
  manuscript_value = c(335, NA, 0.573, 0.588),
  row.names = NULL,
  stringsAsFactors = FALSE
)
summary_csv <- file.path(out_dir, "brca_cox_summary.csv")
write.csv(brca_summary, summary_csv, row.names = FALSE)
cat("Wrote matched-subset summary to:\n  ", summary_csv, "\n")

cat("\n============================================\n")
cat("C-index, baseline:  ", round(summary(cox_baseline)$concordance["C"], 3), "\n")
cat("C-index, BRCA-added:", round(summary(cox_brca)$concordance["C"], 3), "\n")
cat("Wrote comparison table to:\n  ", out_csv, "\n")
cat("============================================\n")

