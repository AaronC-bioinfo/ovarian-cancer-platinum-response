# phase2_02_cox_model.R
# Purpose: Fit Cox proportional hazards model on platinum-treated TCGA-OV patients.
#          Outcome:    OS (overall survival)
#          Covariates: TMB_NONSYNONYMOUS, ANEUPLOIDY_SCORE
#          Outputs:    Cox summary, C-index, HR table CSV, KM plot PNG
# Run from project root:
#   Rscript phase2\phase2_02_cox_model.R

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# ---- 0. Install required packages if missing --------------------------------
required_pkgs <- c("survival", "survminer", "ggplot2")
for (pkg in required_pkgs) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("Installing %s...\n", pkg))
    install.packages(pkg, repos = "https://cloud.r-project.org",
                     lib = "C:/Users/AMAC_WORK/R/library")
  }
}
library(survival)
library(survminer)
library(ggplot2)

# ---- 1. Paths ---------------------------------------------------------------
DATA_DIR <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"
OUT_DIR  <- "phase2/outputs"
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

load_cbio <- function(path) {
  read.table(path, header = TRUE, sep = "\t",
             comment.char = "#", quote = "",
             stringsAsFactors = FALSE, check.names = FALSE)
}

# ---- 2. Load and merge data -------------------------------------------------
cat("Loading clinical files...\n")
clin <- load_cbio(file.path(DATA_DIR, "data_clinical_patient.txt"))
samp <- load_cbio(file.path(DATA_DIR, "data_clinical_sample.txt"))
trt  <- load_cbio(file.path(DATA_DIR, "data_timeline_treatment.txt"))

# Platinum patients
plat_patients <- unique(
  trt$PATIENT_ID[grepl("platin", trt$AGENT, ignore.case = TRUE)]
)
cat(sprintf("  Platinum-treated patients: %d\n", length(plat_patients)))

# Filter and join
clin_plat <- clin[clin$PATIENT_ID %in% plat_patients, ]
samp_dedup <- samp[!duplicated(samp$PATIENT_ID), ]
df <- merge(clin_plat, samp_dedup, by = "PATIENT_ID",
            all.x = TRUE, suffixes = c("", "_samp"))
cat(sprintf("  After merge: %d rows\n", nrow(df)))

# ---- 3. Prepare survival variables ------------------------------------------
cat("\nPreparing survival variables...\n")

# OS_TIME: numeric months
df$os_time <- suppressWarnings(as.numeric(df$OS_MONTHS))

# OS_EVENT: 1 = deceased, 0 = living/censored
# Raw values are "0:LIVING" and "1:DECEASED"
df$os_event <- ifelse(grepl("^1", df$OS_STATUS), 1L, 0L)
cat(sprintf("  Events (deceased): %d | Censored (living): %d\n",
            sum(df$os_event == 1), sum(df$os_event == 0)))

# Covariates: numeric
df$tmb    <- suppressWarnings(as.numeric(df$TMB_NONSYNONYMOUS))
df$aneu   <- suppressWarnings(as.numeric(df$ANEUPLOIDY_SCORE))

# Complete-case subset
cc <- df[!is.na(df$os_time) & !is.na(df$os_event) &
         !is.na(df$tmb)     & !is.na(df$aneu), ]
cat(sprintf("  Complete cases for Cox model: %d / %d\n", nrow(cc), nrow(df)))

# ---- 4. Descriptive statistics for covariates -------------------------------
cat("\nCovariate summary (complete-case subset):\n")
cat(sprintf("  TMB_NONSYNONYMOUS : min=%.3f  median=%.3f  max=%.3f\n",
            min(cc$tmb), median(cc$tmb), max(cc$tmb)))
cat(sprintf("  ANEUPLOIDY_SCORE  : min=%.1f   median=%.1f   max=%.1f\n",
            min(cc$aneu), median(cc$aneu), max(cc$aneu)))

# Log-transform TMB (right-skewed; common in survival literature)
cc$log_tmb <- log1p(cc$tmb)   # log(TMB + 1)
cat("\n  TMB is right-skewed - using log1p(TMB) in Cox model.\n")
cat(sprintf("  log1p(TMB): min=%.3f  median=%.3f  max=%.3f\n",
            min(cc$log_tmb), median(cc$log_tmb), max(cc$log_tmb)))

# ---- 5. Fit Cox model -------------------------------------------------------
cat("\n---- Fitting Cox proportional hazards model ----\n")
surv_obj <- Surv(time = cc$os_time, event = cc$os_event)

# Model 1: log(TMB) + ANEUPLOIDY_SCORE
cox_fit <- coxph(surv_obj ~ log_tmb + aneu, data = cc)
cat("\nCox model summary:\n")
print(summary(cox_fit))

# ---- 6. C-index -------------------------------------------------------------
cindex <- summary(cox_fit)$concordance
cat(sprintf("\nC-index: %.4f  (SE: %.4f)\n", cindex[1], cindex[2]))

# ---- 7. Hazard ratio table -> CSV -------------------------------------------
cat("\nExtracting hazard ratio table...\n")
cox_sum  <- summary(cox_fit)
coef_mat <- cox_sum$coefficients
conf_mat <- cox_sum$conf.int

hr_table <- data.frame(
  Variable    = rownames(coef_mat),
  HR          = round(exp(coef_mat[, "coef"]), 4),
  HR_95CI_low = round(conf_mat[, "lower .95"], 4),
  HR_95CI_hi  = round(conf_mat[, "upper .95"], 4),
  p_value     = signif(coef_mat[, "Pr(>|z|)"], 4),
  stringsAsFactors = FALSE
)
# Rename rows for readability
hr_table$Variable <- c("log(TMB + 1)", "Aneuploidy Score")
print(hr_table)

hr_csv <- file.path(OUT_DIR, "cox_hazard_ratios.csv")
write.csv(hr_table, hr_csv, row.names = FALSE)
cat(sprintf("HR table saved: %s\n", hr_csv))

# ---- 8. Schoenfeld residuals - proportional hazards assumption test ---------
cat("\n---- Proportional hazards assumption (Schoenfeld residuals) ----\n")
ph_test <- cox.zph(cox_fit)
print(ph_test)
ph_csv <- file.path(OUT_DIR, "cox_ph_test.csv")
write.csv(as.data.frame(ph_test$table), ph_csv, row.names = TRUE)
cat(sprintf("PH test table saved: %s\n", ph_csv))

# ---- 9. Risk group stratification - tertiles of linear predictor ------------
cat("\n---- Stratifying patients into risk tertiles ----\n")
cc$lp    <- predict(cox_fit, type = "lp")  # linear predictor
cc$risk_group <- cut(cc$lp,
                     breaks = quantile(cc$lp, probs = c(0, 1/3, 2/3, 1)),
                     labels = c("Low", "Medium", "High"),
                     include.lowest = TRUE)
cat("Risk group sizes:\n")
print(table(cc$risk_group))

# ---- 10. Kaplan-Meier curves by risk group ----------------------------------
cat("\nFitting KM curves by risk group...\n")
km_fit <- survfit(Surv(os_time, os_event) ~ risk_group, data = cc)
print(km_fit)

# Log-rank test
lr_test <- survdiff(Surv(os_time, os_event) ~ risk_group, data = cc)
cat("\nLog-rank test:\n")
print(lr_test)
lr_pval <- 1 - pchisq(lr_test$chisq, df = length(lr_test$n) - 1)
cat(sprintf("Log-rank p-value: %.4g\n", lr_pval))

# KM plot
km_png <- file.path(OUT_DIR, "km_risk_groups.png")
p_km <- ggsurvplot(
  km_fit,
  data          = cc,
  pval          = TRUE,
  pval.method   = TRUE,
  conf.int      = TRUE,
  risk.table    = TRUE,
  risk.table.height = 0.28,
  legend.labs   = c("Low risk", "Medium risk", "High risk"),
  legend.title  = "Predicted risk\n(Cox tertiles)",
  palette       = c("#2166AC", "#F4A582", "#D6604D"),
  xlab          = "Time (months)",
  ylab          = "Overall Survival Probability",
  title         = "Kaplan-Meier: Cox-predicted risk tertiles\n(TCGA-OV, platinum-treated, n=432)",
  ggtheme       = theme_bw(base_size = 13)
)
png(km_png, width = 8, height = 7, units = "in", res = 150)
print(p_km)
dev.off()
cat(sprintf("KM plot saved: %s\n", km_png))

# ---- 11. Save enriched dataset for Python handoff ---------------------------
handoff_csv <- file.path(OUT_DIR, "cox_patients_with_risk.csv")
out_cols <- c("PATIENT_ID", "os_time", "os_event", "tmb", "log_tmb",
              "aneu", "lp", "risk_group")
write.csv(cc[, out_cols], handoff_csv, row.names = FALSE)
cat(sprintf("Patient risk scores saved: %s\n", handoff_csv))

# ---- 11b. Persist model-level summary statistics -> CSV ---------------------
# Added 2026-07-20 (Phase 3 of AUDIT_2026-07-20.md fixes). The C-index and
# KM log-rank p were computed but only printed to stdout; the manuscript cites
# both (C-index 0.570, log-rank p 0.023), so they are now written to a file.
summary_stats <- data.frame(
  metric = c("n_complete_cases", "n_events", "c_index", "c_index_se",
             "km_logrank_p", "schoenfeld_global_p"),
  value  = c(nrow(cc), sum(cc$os_event),
             round(cindex[1], 4), round(cindex[2], 4),
             signif(lr_pval, 4),
             signif(ph_test$table["GLOBAL", "p"], 4)),
  manuscript_value = c(432, 242, 0.570, NA, 0.023, 0.178),
  stringsAsFactors = FALSE
)
stats_csv <- file.path(OUT_DIR, "cox_summary_stats.csv")
write.csv(summary_stats, stats_csv, row.names = FALSE)
cat(sprintf("Model summary stats saved: %s\n", stats_csv))

# ---- 12. Summary printout ---------------------------------------------------
cat("\n==============================================================================\n")
cat("PHASE 2 COX MODEL - RESULTS SUMMARY\n")
cat("==============================================================================\n")
cat(sprintf("  N (complete cases)  : %d\n", nrow(cc)))
cat(sprintf("  Events (deaths)     : %d\n", sum(cc$os_event)))
cat(sprintf("  C-index             : %.4f (SE %.4f)\n", cindex[1], cindex[2]))
cat(sprintf("  Log-rank p-value    : %.4g\n", lr_pval))
cat(sprintf("  PH test global p    : %.4f\n", ph_test$table["GLOBAL", "p"]))
cat("\n  Hazard Ratios:\n")
for (i in seq_len(nrow(hr_table))) {
  cat(sprintf("    %-20s  HR=%.3f (95%% CI: %.3f-%.3f)  p=%.4g\n",
              hr_table$Variable[i],
              hr_table$HR[i],
              hr_table$HR_95CI_low[i],
              hr_table$HR_95CI_hi[i],
              hr_table$p_value[i]))
}
cat("\n  Output files:\n")
cat(sprintf("    %s\n", hr_csv))
cat(sprintf("    %s\n", ph_csv))
cat(sprintf("    %s\n", km_png))
cat(sprintf("    %s\n", handoff_csv))
cat("==============================================================================\n")
cat("Done. Paste full output into chat.\n")

