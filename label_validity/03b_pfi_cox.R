## ============================================================
## label_validity/03b_pfi_cox.R
## Q2 analysis A3, part 2 — Cox model for PFI (time to progression)
## (claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A3)
##
## Reuses the v2 Cox code with ONLY the endpoint swapped:
##   * phase2/phase2_02_cox_model.R  — cohort and covariates (log1p(TMB) + aneuploidy)
##   * src/hrd/02_cox_model_with_brca.R — BRCA merge and baseline-vs-BRCA comparison
## Cohort: phase2/outputs/cox_patients_with_risk.csv (n = 432; platinum = AGENT
##   matching "platin", so it includes TCGA-29-1711, oxaliplatin only — one patient
##   more than the classification cohort; same cohort as the v2 OS Cox model).
## Endpoint: TCGA-CDR PFI / PFI.time (days from diagnosis → months / 30.4375),
##   from label_validity/outputs/cdr_ov_pfi.csv (exported from
##   TCGA-CDR-SupplementalTableS1.xlsx, sheet TCGA-CDR, type == "OV").
##
## Run from project root on the host:
##   "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" label_validity\03b_pfi_cox.R
##
## Outputs → label_validity/outputs/
##   a3_pfi_cox_hr.csv       HRs, 95% CI, p for all models
##   a3_pfi_cox_summary.csv  n, events, C-index per model
##   a3_pfi_cox_ph.csv       Schoenfeld tests per model
##
## ============================================================
## PREDICTIONS (written 2026-10-29 before running — DEC-019)
## ============================================================
## Already seen (disclosed): A3 part 1 found BRCA mutants 0/25 PFI-from-platinum
## resistant and aneuploidy higher in PFI-from-platinum-resistant patients
## (r = +0.21, q = 0.004). v2 OS Cox: aneuploidy HR 1.021 (p 0.017), TMB HR 0.894
## (p 0.238), C-index 0.570; BRCA HR 0.455 (p 0.024), n = 335.
##   P1  Baseline PFI model (n ≈ 432): aneuploidy HR > 1 with p < 0.05;
##       log1p(TMB) HR CI includes 1.
##   P2  BRCA model (matched subset ≈ 335): BRCA_any_mutated HR < 1 with p < 0.05,
##       and its HR is lower than the v2 OS estimate (0.455).
##   P3  Baseline PFI C-index between 0.53 and 0.62.
##   P4  Global Schoenfeld p > 0.05 for the baseline model.
## No multiplicity correction: 3 pre-specified models, each reported in full.
## ============================================================

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(survival)

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
out_dir <- file.path(project_root, "label_validity/outputs")

cohort <- read.csv(file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv"),
                   stringsAsFactors = FALSE)
pfi    <- read.csv(file.path(out_dir, "cdr_ov_pfi.csv"), stringsAsFactors = FALSE)
brca   <- read.csv(file.path(project_root, "hrd/brca_status.csv"), stringsAsFactors = FALSE)

stopifnot(nrow(cohort) == 432, all(c("PATIENT_ID", "log_tmb", "aneu") %in% names(cohort)))

df <- merge(cohort[, c("PATIENT_ID", "log_tmb", "aneu")], pfi, by = "PATIENT_ID")
df$pfi_time_m <- df$pfi_time_d / 30.4375
df <- df[!is.na(df$pfi_time_m) & !is.na(df$pfi_event) & df$pfi_time_m >= 0, ]
cat(sprintf("Cox cohort with CDR PFI: %d / 432 (events %d)\n", nrow(df), sum(df$pfi_event)))

fit_one <- function(fmla, data, label) {
  ## do.call embeds the data in the call, so cox.zph() can rebuild the model frame
  m  <- do.call(coxph, list(formula = fmla, data = data))
  s  <- summary(m)
  ph <- cox.zph(m)
  list(
    hr = data.frame(model = label, term = rownames(s$coefficients),
                    HR = s$coefficients[, "exp(coef)"],
                    HR_lo = s$conf.int[, "lower .95"], HR_hi = s$conf.int[, "upper .95"],
                    p = s$coefficients[, "Pr(>|z|)"], row.names = NULL),
    sm = data.frame(model = label, n = s$n, events = s$nevent,
                    c_index = s$concordance["C"], c_index_se = s$concordance["se(C)"],
                    row.names = NULL),
    ph = data.frame(model = label, term = rownames(ph$table),
                    chisq = ph$table[, "chisq"], df = ph$table[, "df"], p = ph$table[, "p"],
                    row.names = NULL)
  )
}

## Model 1: baseline, full cohort (phase2 formula, endpoint swapped)
r1 <- fit_one(Surv(pfi_time_m, pfi_event) ~ log_tmb + aneu, df, "pfi_baseline_full")

## Models 2–3: BRCA matched subset (src/hrd/02 structure, endpoint swapped)
mb <- merge(df, brca[, c("PATIENT_ID", "BRCA_any_mutated")], by = "PATIENT_ID")
cat(sprintf("BRCA matched subset: %d (mutant %d)\n", nrow(mb), sum(mb$BRCA_any_mutated)))
r2 <- fit_one(Surv(pfi_time_m, pfi_event) ~ log_tmb + aneu, mb, "pfi_baseline_matched")
r3 <- fit_one(Surv(pfi_time_m, pfi_event) ~ log_tmb + aneu + BRCA_any_mutated, mb, "pfi_brca_added")

hr <- rbind(r1$hr, r2$hr, r3$hr)
sm <- rbind(r1$sm, r2$sm, r3$sm)
ph <- rbind(r1$ph, r2$ph, r3$ph)
write.csv(hr, file.path(out_dir, "a3_pfi_cox_hr.csv"), row.names = FALSE)
write.csv(sm, file.path(out_dir, "a3_pfi_cox_summary.csv"), row.names = FALSE)
write.csv(ph, file.path(out_dir, "a3_pfi_cox_ph.csv"), row.names = FALSE)

cat("\n== Hazard ratios ==\n");  print(hr, digits = 4)
cat("\n== Summary ==\n");        print(sm, digits = 4)
cat("\n== Schoenfeld ==\n");     print(ph, digits = 4)
cat("\nWritten to", out_dir, "\n")
