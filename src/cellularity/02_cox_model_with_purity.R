## ============================================================
## Enhancement 3 — Step 2: Cox model with tumour purity covariate
## Ovarian Cancer Platinum Response Project
## ============================================================

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(survival)
library(data.table)

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
cohort_file  <- file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv")
purity_file  <- file.path(project_root, "cellularity/estimate_scores.csv")
out_dir      <- file.path(project_root, "cellularity")

cohort <- fread(cohort_file, data.table = FALSE)
purity <- fread(purity_file, data.table = FALSE)

cat("cox_patients_with_risk.csv columns:\n  ", paste(names(cohort), collapse = ", "), "\n\n")

## ---- Detect required columns rather than assuming exact names ----
find_col <- function(df, candidates, label) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0) {
    stop("Could not find a column for '", label, "' in cox_patients_with_risk.csv.\n",
         "Looked for: ", paste(candidates, collapse = ", "), "\n",
         "Actual columns are: ", paste(names(df), collapse = ", "), "\n",
         "Paste that column list back and I'll fix the mapping.")
  }
  hit[1]
}

col_patient <- find_col(cohort, c("PATIENT_ID", "PatientID"), "patient ID")
col_os_time <- find_col(cohort, c("OS_MONTHS", "os_time"), "overall survival time")
col_os_stat <- find_col(cohort, c("OS_STATUS", "OS_EVENT", "os_event"), "overall survival status")
col_aneup   <- find_col(cohort, c("ANEUPLOIDY_SCORE", "aneu"), "aneuploidy score")

## Prefer an already log-transformed TMB column if one exists (matches
## Finding 4's exact covariate) rather than re-applying log1p() on top of
## it, which would double-transform.
if ("log_tmb" %in% names(cohort)) {
  tmb_term <- "log_tmb"
} else if ("LOG_TMB" %in% names(cohort)) {
  tmb_term <- "LOG_TMB"
} else {
  col_tmb  <- find_col(cohort, c("TMB_NONSYNONYMOUS", "TMB", "tmb"), "TMB")
  tmb_term <- paste0("log1p(", col_tmb, ")")
}
cat("Using TMB term:", tmb_term, "\n")

## OS_STATUS in TCGA clinical files is often "1:DECEASED"/"0:LIVING" text
## rather than numeric 0/1 -- coxph needs a numeric event indicator.
os_status_raw <- cohort[[col_os_stat]]
if (is.character(os_status_raw)) {
  cohort$OS_STATUS_NUM <- as.integer(grepl("DECEASED|1", os_status_raw))
} else {
  cohort$OS_STATUS_NUM <- as.integer(os_status_raw)
}

## ---- Join purity onto the full cohort (inner join -> up to 235 patients) ----
## ESTIMATE's internal file I/O (filterCommonGenes/estimateScore) runs
## sample IDs through R's default check.names=TRUE behavior somewhere in
## the chain, which silently converts "-" to "." in column headers (e.g.
## TCGA-04-1331 -> TCGA.04.1331). The cohort file keeps the original
## dashes. Normalize both sides before matching rather than guessing.
normalize_id <- function(x) toupper(trimws(gsub("[.]", "-", x)))

cat("Sample cohort IDs:  ", paste(head(cohort[[col_patient]], 3), collapse = ", "), "\n")
cat("Sample purity IDs:  ", paste(head(purity$PATIENT_ID, 3), collapse = ", "), "\n")

cohort$.join_id <- normalize_id(cohort[[col_patient]])
purity$.join_id <- normalize_id(purity$PATIENT_ID)

merged <- merge(cohort, purity[, c(".join_id", "TumorPurity")], by = ".join_id")
merged$.join_id <- NULL
cat("Patients with both clinical covariates and purity score:", nrow(merged), "\n\n")

if (nrow(merged) == 0) {
  stop("Still 0 matches after dot/dash normalization. Compare the sample ",
       "ID lines printed above and paste them back -- there may be a ",
       "different format mismatch (e.g. extra whitespace, a sample-type ",
       "suffix, or case sensitivity beyond what normalize_id() strips).")
}

## ---- Model A: baseline (same formula as Finding 4), refit on the n=235
## purity subset so the C-index comparison is apples-to-apples, not
## confounded by the drop from 432 -> 235 patients ----
fmla_baseline <- as.formula(paste0(
  "Surv(", col_os_time, ", OS_STATUS_NUM) ~ ", tmb_term, " + ", col_aneup
))
cox_baseline <- coxph(fmla_baseline, data = merged)

## ---- Model B: purity-corrected ----
fmla_purity <- as.formula(paste0(
  "Surv(", col_os_time, ", OS_STATUS_NUM) ~ ", tmb_term, " + ",
  col_aneup, " + TumorPurity"
))
cox_purity <- coxph(fmla_purity, data = merged)

cat("=== Baseline model (n=235, no purity) ===\n")
print(summary(cox_baseline))
cat("\n=== Purity-corrected model (n=235) ===\n")
print(summary(cox_purity))

## ---- Proportional hazards check on the corrected model ----
ph_test <- cox.zph(cox_purity)
cat("\n=== Schoenfeld PH test (purity-corrected model) ===\n")
print(ph_test)

## ---- Assemble comparison table ----
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
  extract_hr(cox_baseline, "baseline_n235"),
  extract_hr(cox_purity,   "purity_corrected_n235")
)

out_csv <- file.path(out_dir, "cox_hazard_ratios_purity.csv")
write.csv(comparison, out_csv, row.names = FALSE)

cat("\n============================================\n")
cat("C-index, baseline (n=235):        ", round(summary(cox_baseline)$concordance["C"], 3), "\n")
cat("C-index, purity-corrected (n=235):", round(summary(cox_purity)$concordance["C"], 3), "\n")
cat("Wrote comparison table to:\n  ", out_csv, "\n")
cat("============================================\n")
