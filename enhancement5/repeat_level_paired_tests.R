## ============================================================
## Enhancement 5 — Post-hoc: repeat-level paired comparison
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## Pure post-hoc statistical analysis on already-computed CV results.
## Does NOT re-run any modeling and does NOT touch any existing script,
## config.yaml, or .git.
##
## The 25 outer folds are 5 repeats x 5 folds, and folds within a repeat
## share the same underlying cohort (just reshuffled). Treating all 25
## as independent overstates the effective sample size. Instead: average
## the 5 within-repeat folds down to one number per repeat (5 repeat-level
## means), then paired-test those 5 numbers (full vs baseline).

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

log_msg <- function(...) {
  cat(..., "\n")
  flush(stdout())
}

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
out_dir <- file.path(project_root, "enhancement5", "outputs")

fileA <- file.path(out_dir, "cv_results_cohortA_n235.csv")
fileB <- file.path(out_dir, "cv_results_cohortB_n163.csv")

cohortA <- read.csv(fileA, stringsAsFactors = FALSE)
cohortB <- read.csv(fileB, stringsAsFactors = FALSE)

log_msg("cv_results_cohortA_n235.csv columns:", paste(names(cohortA), collapse = ", "))
log_msg("cv_results_cohortB_n163.csv columns:", paste(names(cohortB), collapse = ", "))

req_cols <- c("fold_id", "repeat_id", "cindex_baseline", "cindex_full_lambdamin", "cindex_full_lambda1se")
for (nm in c("cohortA", "cohortB")) {
  df <- get(nm)
  missing <- setdiff(req_cols, names(df))
  if (length(missing) > 0) {
    stop(nm, " is missing expected column(s): ", paste(missing, collapse = ", "),
         ". Actual columns: ", paste(names(df), collapse = ", "))
  }
}

## ------------------------------------------------------------------
## Core routine: repeat-level averaging + paired tests for one
## cohort x lambda-choice combination
## ------------------------------------------------------------------
run_repeat_level_test <- function(df, lambda_col, cohort_label, lambda_label) {

  ## 1. Average the 5 fold-level C-index values within each repeat_id,
  ##    separately for baseline and full model.
  repeat_means <- aggregate(
    cbind(baseline_mean = cindex_baseline, full_mean = get(lambda_col)) ~ repeat_id,
    data = df, FUN = mean
  )
  repeat_means <- repeat_means[order(repeat_means$repeat_id), ]

  ## 2. Paired difference (full - baseline) at each of the 5 repeat-level means.
  repeat_means$difference <- repeat_means$full_mean - repeat_means$baseline_mean

  n_repeats <- nrow(repeat_means)
  log_msg(sprintf("\n=== %s | %s (n_repeats=%d) ===", cohort_label, lambda_label, n_repeats))
  print(repeat_means, row.names = FALSE)

  diffs <- repeat_means$difference

  ## 3. Paired t-test (equivalently, one-sample t-test of diffs against 0)
  t_res <- t.test(diffs, mu = 0)

  ## 4. Wilcoxon signed-rank test on the same 5 differences
  wilcox_res <- tryCatch(
    wilcox.test(diffs, mu = 0),
    warning = function(w) suppressWarnings(wilcox.test(diffs, mu = 0)),
    error = function(e) NULL
  )
  wilcox_p <- if (is.null(wilcox_res)) NA_real_ else wilcox_res$p.value

  mean_diff <- mean(diffs)
  sd_diff <- sd(diffs)

  log_msg(sprintf("mean difference = %.4f | SD = %.4f | t = %.4f | paired-t p = %.4f | Wilcoxon p = %s",
                   mean_diff, sd_diff, t_res$statistic, t_res$p.value,
                   ifelse(is.na(wilcox_p), "NA", sprintf("%.4f", wilcox_p))))

  list(
    summary_row = data.frame(
      cohort = cohort_label,
      lambda = lambda_label,
      n_repeats = n_repeats,
      mean_difference = mean_diff,
      sd_difference = sd_diff,
      t_statistic = as.numeric(t_res$statistic),
      paired_t_pvalue = t_res$p.value,
      wilcoxon_pvalue = wilcox_p
    ),
    repeat_table = data.frame(
      cohort = cohort_label,
      lambda = lambda_label,
      repeat_means
    )
  )
}

## ------------------------------------------------------------------
## Run for all 4 combinations
## ------------------------------------------------------------------
resA_min <- run_repeat_level_test(cohortA, "cindex_full_lambdamin", "CohortA_n235", "lambda.min")
resA_1se <- run_repeat_level_test(cohortA, "cindex_full_lambda1se", "CohortA_n235", "lambda.1se")
resB_min <- run_repeat_level_test(cohortB, "cindex_full_lambdamin", "CohortB_n163", "lambda.min")
resB_1se <- run_repeat_level_test(cohortB, "cindex_full_lambda1se", "CohortB_n163", "lambda.1se")

summary_table <- rbind(
  resA_min$summary_row, resA_1se$summary_row,
  resB_min$summary_row, resB_1se$summary_row
)

out_csv <- file.path(out_dir, "repeat_level_paired_tests.csv")
write.csv(summary_table, out_csv, row.names = FALSE)

log_msg("\n============================================================")
log_msg("Summary table (all 4 cohort x lambda combinations):")
print(summary_table, row.names = FALSE)
log_msg("\nWrote summary to:", out_csv)
log_msg("============================================================")
