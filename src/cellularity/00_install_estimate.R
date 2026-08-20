## ============================================================
## Enhancement 3 — Step 0: Install and verify the ESTIMATE package
## Ovarian Cancer Platinum Response Project
## ============================================================

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

## ESTIMATE is not on CRAN or Bioconductor — it is hosted on R-Forge.
## Dependencies (utils is base R; only 'estimate' itself needs installing).

if (!requireNamespace("estimate", quietly = TRUE)) {
  message("Installing 'estimate' from R-Forge...")
  install.packages(
    "estimate",
    repos = "http://r-forge.r-project.org",
    type  = "source",
    lib   = "C:/Users/AMAC_WORK/R/library"
  )
}

## --- Fallback if R-Forge is unreachable or the build fails ---
## R-Forge occasionally has TLS/availability issues from behind
## institutional networks. If the install above fails, try:
##
##   install.packages("remotes")
##   remotes::install_github("bhklab/estimate")
##
## and if BOTH fail, fall back to TIMER2.0 web portal
## (https://timer.cistrome.org/) which computes comparable purity
## estimates without a local R package — this was already flagged as
## a contingency in the Enhancement 3 handoff.

library(estimate)

cat("\n============================================\n")
cat("ESTIMATE package loaded successfully.\n")
cat("Version: ", as.character(utils::packageVersion("estimate")), "\n")
cat("Available functions: ", paste(ls("package:estimate"), collapse = ", "), "\n")
cat("============================================\n")

## Sanity check: confirm the three functions we need for the pipeline exist
required_fns <- c("filterCommonGenes", "estimateScore", "outputGCT")
missing_fns  <- setdiff(required_fns, ls("package:estimate"))

if (length(missing_fns) > 0) {
  stop("Missing expected ESTIMATE functions: ", paste(missing_fns, collapse = ", "))
} else {
  cat("All required functions present: ", paste(required_fns, collapse = ", "), "\n")
  cat("Ready to proceed to 01_run_estimate.R\n")
}
