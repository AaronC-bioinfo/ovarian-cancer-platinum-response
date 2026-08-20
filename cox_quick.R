# ---- DO NOT DELETE YET -------------------------------------------------------
# Flagged by the 2026-08-20 fix pass. This was scheduled for deletion as a
# throwaway, but it is currently LOAD-BEARING: it is the script that actually
# produced phase2/outputs/cox_summary_stats.csv (2026-08-20 00:04), and therefore
# the provenance of the manuscript's C-index 0.570 and log-rank p 0.023.
#
# phase2/phase2_02_cox_model.R halted on a mojibake parse error before reaching
# its own write of cox_summary_stats.csv (see rerun_log_R2.txt / rerun_log_R3.txt),
# which is why this fallback exists. That encoding fault has now been repaired.
#
# Safe to delete once phase2/phase2_02_cox_model.R has been re-run end to end and
# has regenerated BOTH cox_summary_stats.csv (6-row long format) and
# km_risk_groups.png at full size.
# ------------------------------------------------------------------------------
.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(survival)
d <- read.csv("phase2/outputs/cox_patients_with_risk.csv")
fit <- coxph(Surv(os_time, os_event) ~ log_tmb + aneu, data = d)
ci <- summary(fit)$concordance[1]
sd <- survdiff(Surv(os_time, os_event) ~ risk_group, data = d)
lp <- 1 - pchisq(sd$chisq, length(sd$n) - 1)
cat(sprintf("C-index = %.4f\n", ci))
cat(sprintf("log-rank p = %.4f\n", lp))
write.csv(data.frame(c_index = ci, logrank_p = lp),
          "phase2/outputs/cox_summary_stats.csv", row.names = FALSE)
