## ============================================================
## Enhancement 5 "” Phase 2: Expression-augmented elastic-net Cox model
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## Nested cross-validated elastic-net-penalized Cox regression (glmnet),
## augmenting the Finding-4 clinical baseline with the top-200 SHAP-ranked
## expression genes (Finding 5, without-12m gene list).
##
## Two cohorts, evaluated by ONE reusable nested-CV function:
##   Cohort A (n=235, PRIMARY):     log_tmb + aneu (forced) + 200 genes (penalized)
##   Cohort B (n=163, ROBUSTNESS):  log_tmb + aneu + BRCA_any_mutated (forced) + 200 genes (penalized)
##
## This script does not modify any existing script, config.yaml, or .git.

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
suppressPackageStartupMessages({
  library(glmnet)
  library(survival)
  library(data.table)
})

set.seed(42)

log_msg <- function(...) {
  cat(..., "\n")
  flush(stdout())
}

project_root  <- "C:/PROJECTS/ovarian-cancer-platinum-response"
tcga_path     <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

cohort_file    <- file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv")
brca_file      <- file.path(project_root, "hrd/brca_status.csv")
genelist_file  <- file.path(project_root, "phase2/outputs/cv_top200_genes_shap_without12m.txt")
expr_file      <- file.path(tcga_path, "data_mrna_seq_v2_rsem.txt")
enrich_sig_file<- file.path(project_root, "phase2/outputs/enrichment_results_significant.csv")

out_dir <- file.path(project_root, "enhancement5", "outputs")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

log_msg("============================================================")
log_msg("Enhancement 5 Phase 2: expression-augmented elastic-net Cox")
log_msg("============================================================\n")

## ------------------------------------------------------------------
## Defensive column lookup helper (same pattern as Enhancement 3/4)
## ------------------------------------------------------------------
find_col <- function(df, candidates, label) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0) {
    stop("Could not find a column for '", label, "'. Looked for: ",
         paste(candidates, collapse = ", "), ". Actual columns: ",
         paste(names(df), collapse = ", "))
  }
  hit[1]
}

normalize_id <- function(x) toupper(trimws(gsub("[.]", "-", x)))

## ------------------------------------------------------------------
## 1. Load base cohort (n=432) + BRCA status + gene list
## ------------------------------------------------------------------
log_msg("=== Loading clinical/cohort files ===")
cohort <- fread(cohort_file, data.table = FALSE)
brca   <- fread(brca_file,   data.table = FALSE)

log_msg("cox_patients_with_risk.csv columns:", paste(names(cohort), collapse = ", "))
log_msg("brca_status.csv columns:           ", paste(names(brca), collapse = ", "))

col_patient <- find_col(cohort, c("PATIENT_ID", "PatientID"), "patient ID")
col_os_time <- find_col(cohort, c("os_time", "OS_MONTHS"), "OS time")
col_os_stat <- find_col(cohort, c("os_event", "OS_STATUS", "OS_EVENT"), "OS event")
col_aneup   <- find_col(cohort, c("aneu", "ANEUPLOIDY_SCORE"), "aneuploidy")

if ("log_tmb" %in% names(cohort)) {
  tmb_col <- "log_tmb"
} else if ("LOG_TMB" %in% names(cohort)) {
  tmb_col <- "LOG_TMB"
} else {
  stop("No log_tmb / LOG_TMB column found in cohort file. Columns: ",
       paste(names(cohort), collapse = ", "))
}
log_msg("Using columns -> patient:", col_patient, "| time:", col_os_time,
        "| event:", col_os_stat, "| tmb:", tmb_col, "| aneu:", col_aneup)

os_status_raw <- cohort[[col_os_stat]]
if (is.character(os_status_raw)) {
  cohort$os_event_num <- as.integer(grepl("DECEASED|1", os_status_raw))
} else {
  cohort$os_event_num <- as.integer(os_status_raw)
}

cohort$.join_id <- normalize_id(cohort[[col_patient]])
brca$.join_id   <- normalize_id(brca$PATIENT_ID)

## Standardize working columns onto fixed names used throughout the rest
## of this script, regardless of source-file naming.
base <- data.frame(
  PATIENT_ID = cohort[[col_patient]],
  join_id    = cohort$.join_id,
  os_time    = as.numeric(cohort[[col_os_time]]),
  os_event   = cohort$os_event_num,
  log_tmb    = as.numeric(cohort[[tmb_col]]),
  aneu       = as.numeric(cohort[[col_aneup]]),
  stringsAsFactors = FALSE
)
log_msg("Base cohort (all platinum patients with clinical covariates):", nrow(base), "\n")

## ------------------------------------------------------------------
## 2. Load + clean expression matrix, subset to the 200 SHAP genes
## ------------------------------------------------------------------
log_msg("=== Loading expression matrix (this can take a moment) ===")
genes_wanted <- readLines(genelist_file)
genes_wanted <- trimws(genes_wanted)
genes_wanted <- genes_wanted[nzchar(genes_wanted)]
log_msg("Gene list file:", genelist_file, "->", length(genes_wanted), "genes requested")

expr_raw <- fread(expr_file, header = TRUE, sep = "\t", data.table = FALSE, showProgress = TRUE)
log_msg("Raw expression matrix:", nrow(expr_raw), "rows x", ncol(expr_raw), "columns")

req_cols <- c("Hugo_Symbol")
if (!all(req_cols %in% names(expr_raw))) {
  stop("Expression file is missing expected column 'Hugo_Symbol'. Actual columns (first 5): ",
       paste(head(names(expr_raw), 5), collapse = ", "))
}

## Subset to the requested gene list. Report any genes not found, and
## deduplicate any Hugo_Symbol that appears more than once (keep first
## occurrence) so each requested gene maps to exactly one row -- required
## for a well-defined glmnet design matrix.
expr_sub <- expr_raw[expr_raw$Hugo_Symbol %in% genes_wanted, , drop = FALSE]
dup_genes <- unique(expr_sub$Hugo_Symbol[duplicated(expr_sub$Hugo_Symbol)])
if (length(dup_genes) > 0) {
  log_msg("NOTE: ", length(dup_genes), " requested gene symbol(s) have duplicate rows in the RSEM file; keeping first occurrence:")
  log_msg("     ", paste(dup_genes, collapse = ", "))
  expr_sub <- expr_sub[!duplicated(expr_sub$Hugo_Symbol), , drop = FALSE]
}

missing_genes <- setdiff(genes_wanted, expr_sub$Hugo_Symbol)
if (length(missing_genes) > 0) {
  log_msg("WARNING: ", length(missing_genes), " requested gene(s) not found in expression file:")
  log_msg("     ", paste(missing_genes, collapse = ", "))
} else {
  log_msg("All", length(genes_wanted), "requested genes found in expression file.")
}

rownames(expr_sub) <- expr_sub$Hugo_Symbol
expr_sub$Hugo_Symbol <- NULL
expr_sub$Entrez_Gene_Id <- NULL

## Truncate sample barcodes -> 12-char TCGA patient ID (matches
## src/preprocessing.py::clean_expression convention exactly), then
## average any duplicate samples per patient.
sample_ids <- colnames(expr_sub)
patient_ids_from_expr <- substr(sample_ids, 1, 12)
colnames(expr_sub) <- patient_ids_from_expr

uniq_patients <- unique(patient_ids_from_expr)
if (length(uniq_patients) < ncol(expr_sub)) {
  log_msg("Averaging", ncol(expr_sub) - length(uniq_patients),
          "duplicate-patient sample column(s) in the expression matrix...")
  expr_mat_avg <- sapply(uniq_patients, function(pid) {
    cols <- which(patient_ids_from_expr == pid)
    if (length(cols) == 1) as.numeric(expr_sub[, cols]) else rowMeans(expr_sub[, cols, drop = FALSE])
  })
  rownames(expr_mat_avg) <- rownames(expr_sub)
  expr_clean <- as.data.frame(expr_mat_avg)
} else {
  expr_clean <- expr_sub
}
expr_clean_join_id <- normalize_id(colnames(expr_clean))
colnames(expr_clean) <- expr_clean_join_id

log_msg("Clean expression matrix:", nrow(expr_clean), "genes x", ncol(expr_clean), "patients\n")

## ------------------------------------------------------------------
## 3. Build Cohort A (nâ‰ˆ235: base cohort âˆ© RNA-seq) and
##    Cohort B (nâ‰ˆ163: Cohort A âˆ© BRCA status)
## ------------------------------------------------------------------
log_msg("=== Building cohorts ===")

expr_patients <- colnames(expr_clean)
cohortA_ids <- intersect(base$join_id, expr_patients)
cohortA <- base[base$join_id %in% cohortA_ids, ]
cohortA <- cohortA[!duplicated(cohortA$join_id), ]
log_msg("Cohort A (RNA-seq available):", nrow(cohortA), "patients,",
        sum(cohortA$os_event), "events")

cohortB_ids <- intersect(cohortA$join_id, brca$.join_id)
cohortB <- merge(cohortA, brca[, c(".join_id", "BRCA_any_mutated")],
                  by.x = "join_id", by.y = ".join_id")
cohortB <- cohortB[!duplicated(cohortB$join_id), ]
log_msg("Cohort B (RNA-seq + BRCA status available):", nrow(cohortB), "patients,",
        sum(cohortB$os_event), "events\n")

if (nrow(cohortA) == 0 || nrow(cohortB) == 0) {
  stop("Empty cohort after intersection -- check ID normalization (join_id samples below).")
}
log_msg("Sample cohort join_ids:      ", paste(head(cohortA$join_id, 3), collapse = ", "))
log_msg("Sample expression join_ids:  ", paste(head(expr_patients, 3), collapse = ", "))
log_msg("Sample BRCA join_ids:        ", paste(head(brca$.join_id, 3), collapse = ", "))
cat("\n")

## Gene expression sub-matrices aligned (patients x genes) to each cohort,
## in the SAME gene order for both cohorts.
gene_order <- rownames(expr_clean)
exprA <- t(expr_clean[, cohortA$join_id, drop = FALSE])
exprA <- exprA[, gene_order, drop = FALSE]
rownames(exprA) <- cohortA$join_id

exprB <- t(expr_clean[, cohortB$join_id, drop = FALSE])
exprB <- exprB[, gene_order, drop = FALSE]
rownames(exprB) <- cohortB$join_id

## ------------------------------------------------------------------
## 4. Stratified fold generator (dependency-free equivalent of
##    caret::createFolds; avoids installing a new heavy package beyond
##    the already-approved glmnet).
## ------------------------------------------------------------------
make_stratified_folds <- function(y, k, seed) {
  set.seed(seed)
  folds <- integer(length(y))
  for (cls in unique(y)) {
    idx <- which(y == cls)
    idx <- sample(idx)
    folds[idx] <- rep(1:k, length.out = length(idx))
  }
  folds
}

## ------------------------------------------------------------------
## 5. Reusable nested-CV function
## ------------------------------------------------------------------
ALPHA_GRID <- seq(0, 1, by = 0.1)
OUTER_K <- 5
OUTER_REPEATS <- 5
OUTER_SEEDS <- c(42, 43, 44, 45, 46)

run_nested_cv <- function(cohort_df, gene_mat, forced_covars, cohort_label,
                           baseline_formula) {

  n_forced <- length(forced_covars)
  n_genes  <- ncol(gene_mat)
  penalty_factor <- c(rep(0, n_forced), rep(1, n_genes))

  cv_rows <- list()
  alpha_rows <- list()
  fold_counter <- 0

  for (r in seq_len(OUTER_REPEATS)) {
    fold_assign <- make_stratified_folds(cohort_df$os_event, k = OUTER_K, seed = OUTER_SEEDS[r])

    for (k in seq_len(OUTER_K)) {
      fold_counter <- fold_counter + 1
      test_idx  <- which(fold_assign == k)
      train_idx <- setdiff(seq_len(nrow(cohort_df)), test_idx)

      train_df <- cohort_df[train_idx, ]
      test_df  <- cohort_df[test_idx, ]
      train_genes <- gene_mat[train_idx, , drop = FALSE]
      test_genes  <- gene_mat[test_idx, , drop = FALSE]

      ## z-score genes using outer-train mean/sd only, apply to outer-test
      train_genes_scaled <- scale(train_genes)
      center <- attr(train_genes_scaled, "scaled:center")
      scale_ <- attr(train_genes_scaled, "scaled:scale")
      scale_[scale_ == 0] <- 1  # guard against zero-variance genes in a fold
      test_genes_scaled <- scale(test_genes, center = center, scale = scale_)

      x_train <- as.matrix(cbind(train_df[, forced_covars, drop = FALSE], train_genes_scaled))
      x_test  <- as.matrix(cbind(test_df[, forced_covars, drop = FALSE], test_genes_scaled))

      y_train <- survival::Surv(train_df$os_time, train_df$os_event)
      y_test  <- survival::Surv(test_df$os_time, test_df$os_event)

      ## ---- alpha grid search via cv.glmnet's internal 5-fold CV ----
      best_alpha <- NA
      best_dev <- Inf
      best_fit <- NULL
      for (a in ALPHA_GRID) {
        fit_a <- tryCatch(
          glmnet::cv.glmnet(x_train, y_train, family = "cox", alpha = a,
                             penalty.factor = penalty_factor, nfolds = 5),
          error = function(e) NULL
        )
        if (is.null(fit_a)) next
        min_dev <- min(fit_a$cvm, na.rm = TRUE)
        if (is.finite(min_dev) && min_dev < best_dev) {
          best_dev <- min_dev
          best_alpha <- a
          best_fit <- fit_a
        }
      }

      if (is.null(best_fit)) {
        log_msg(sprintf("[%s] fold %2d/25 (repeat %d, fold %d): ALL alphas failed to fit -- skipping",
                         cohort_label, fold_counter, r, k))
        next
      }

      lam_min <- best_fit$lambda.min
      lam_1se <- best_fit$lambda.1se

      pred_min <- as.numeric(predict(best_fit, newx = x_test, s = "lambda.min", type = "link"))
      pred_1se <- as.numeric(predict(best_fit, newx = x_test, s = "lambda.1se", type = "link"))

      ## NOTE on reverse=TRUE: concordance()'s formula interface assumes by
      ## default that LARGER x predicts LARGER y (longer survival). A Cox
      ## linear predictor is the opposite (larger lp = higher hazard =
      ## shorter survival), so it must be passed reverse=TRUE or every
      ## C-index comes back as (1 - true C). Confirmed against the
      ## survival package's own concordance vignette. coxph objects passed
      ## directly to concordance() handle this automatically; the manual
      ## Surv(...) ~ lp formula form used here does not.
      cidx_min <- tryCatch(
        survival::concordance(y_test ~ pred_min, reverse = TRUE)$concordance,
        error = function(e) NA_real_)
      cidx_1se <- tryCatch(
        survival::concordance(y_test ~ pred_1se, reverse = TRUE)$concordance,
        error = function(e) NA_real_)

      ## ---- baseline (unpenalized) coxph on the SAME split ----
      cox_base <- tryCatch(coxph(baseline_formula, data = train_df), error = function(e) NULL)
      cidx_base <- NA_real_
      if (!is.null(cox_base)) {
        pred_base <- tryCatch(predict(cox_base, newdata = test_df, type = "lp"), error = function(e) NULL)
        if (!is.null(pred_base)) {
          cidx_base <- tryCatch(
            survival::concordance(y_test ~ pred_base, reverse = TRUE)$concordance,
            error = function(e) NA_real_)
        }
      }

      log_msg(sprintf("[%-8s] fold %2d/25 (repeat %d, fold %d): alpha*=%.1f | C-index base=%.3f | full(min)=%.3f | full(1se)=%.3f",
                       cohort_label, fold_counter, r, k, best_alpha,
                       ifelse(is.na(cidx_base), NA, cidx_base),
                       ifelse(is.na(cidx_min), NA, cidx_min),
                       ifelse(is.na(cidx_1se), NA, cidx_1se)))

      cv_rows[[fold_counter]] <- data.frame(
        cohort = cohort_label,
        fold_id = fold_counter,
        repeat_id = r,
        inner_fold = k,
        n_train = length(train_idx),
        n_test = length(test_idx),
        alpha_selected = best_alpha,
        cindex_baseline = cidx_base,
        cindex_full_lambdamin = cidx_min,
        cindex_full_lambda1se = cidx_1se
      )
      alpha_rows[[fold_counter]] <- data.frame(
        cohort = cohort_label, fold_id = fold_counter, alpha_selected = best_alpha
      )
    }
  }

  cv_results <- do.call(rbind, cv_rows)
  alpha_summary <- do.call(rbind, alpha_rows)
  list(cv_results = cv_results, alpha_summary = alpha_summary)
}

## ------------------------------------------------------------------
## 6. Reusable full-cohort final-model fitter
## ------------------------------------------------------------------
fit_final_model <- function(cohort_df, gene_mat, forced_covars, cohort_label) {
  n_forced <- length(forced_covars)
  n_genes  <- ncol(gene_mat)
  penalty_factor <- c(rep(0, n_forced), rep(1, n_genes))

  genes_scaled <- scale(gene_mat)
  x_all <- as.matrix(cbind(cohort_df[, forced_covars, drop = FALSE], genes_scaled))
  y_all <- survival::Surv(cohort_df$os_time, cohort_df$os_event)

  log_msg(sprintf("[%s] Fitting FINAL model on full cohort (n=%d)...", cohort_label, nrow(cohort_df)))

  best_alpha <- NA
  best_dev <- Inf
  best_fit <- NULL
  for (a in ALPHA_GRID) {
    fit_a <- tryCatch(
      glmnet::cv.glmnet(x_all, y_all, family = "cox", alpha = a,
                         penalty.factor = penalty_factor, nfolds = 5),
      error = function(e) NULL
    )
    if (is.null(fit_a)) next
    min_dev <- min(fit_a$cvm, na.rm = TRUE)
    if (is.finite(min_dev) && min_dev < best_dev) {
      best_dev <- min_dev
      best_alpha <- a
      best_fit <- fit_a
    }
  }
  log_msg(sprintf("[%s] FINAL model alpha* = %.1f | lambda.min = %.5f | lambda.1se = %.5f",
                   cohort_label, best_alpha, best_fit$lambda.min, best_fit$lambda.1se))

  extract_genes <- function(lambda_val, lambda_label) {
    coefs <- as.matrix(coef(best_fit, s = lambda_val))
    coefs_df <- data.frame(term = rownames(coefs), coefficient = coefs[, 1])
    coefs_df <- coefs_df[coefs_df$coefficient != 0, ]
    coefs_df <- coefs_df[!(coefs_df$term %in% c("(Intercept)", forced_covars)), ]
    coefs_df$hazard_ratio <- exp(coefs_df$coefficient)
    coefs_df <- coefs_df[order(-abs(coefs_df$coefficient)), ]
    rownames(coefs_df) <- NULL
    colnames(coefs_df)[1] <- "gene"
    log_msg(sprintf("[%s] Non-zero genes at %s: %d", cohort_label, lambda_label, nrow(coefs_df)))
    coefs_df
  }

  list(
    alpha_selected = best_alpha,
    lambda_min = best_fit$lambda.min,
    lambda_1se = best_fit$lambda.1se,
    genes_lambdamin = extract_genes(best_fit$lambda.min, "lambda.min"),
    genes_lambda1se = extract_genes(best_fit$lambda.1se, "lambda.1se")
  )
}

## ------------------------------------------------------------------
## 7. Run nested CV for both cohorts
## ------------------------------------------------------------------
baseline_formula_A <- Surv(os_time, os_event) ~ log_tmb + aneu
baseline_formula_B <- Surv(os_time, os_event) ~ log_tmb + aneu + BRCA_any_mutated

log_msg("=== Cohort A nested CV (n=", nrow(cohortA), ") ===")
resultsA <- run_nested_cv(
  cohort_df = cohortA, gene_mat = exprA,
  forced_covars = c("log_tmb", "aneu"),
  cohort_label = "CohortA",
  baseline_formula = baseline_formula_A
)

log_msg("\n=== Cohort B nested CV (n=", nrow(cohortB), ") ===")
resultsB <- run_nested_cv(
  cohort_df = cohortB, gene_mat = exprB,
  forced_covars = c("log_tmb", "aneu", "BRCA_any_mutated"),
  cohort_label = "CohortB",
  baseline_formula = baseline_formula_B
)

write.csv(resultsA$cv_results, file.path(out_dir, "cv_results_cohortA_n235.csv"), row.names = FALSE)
write.csv(resultsB$cv_results, file.path(out_dir, "cv_results_cohortB_n163.csv"), row.names = FALSE)

## ------------------------------------------------------------------
## 8. CV summary
## ------------------------------------------------------------------
summarize_cv <- function(df, cohort_label) {
  rbind(
    data.frame(cohort = cohort_label, model = "baseline",
               lambda = NA,
               mean_cindex = mean(df$cindex_baseline, na.rm = TRUE),
               sd_cindex = sd(df$cindex_baseline, na.rm = TRUE),
               n_folds = sum(!is.na(df$cindex_baseline))),
    data.frame(cohort = cohort_label, model = "full_expression",
               lambda = "lambda.min",
               mean_cindex = mean(df$cindex_full_lambdamin, na.rm = TRUE),
               sd_cindex = sd(df$cindex_full_lambdamin, na.rm = TRUE),
               n_folds = sum(!is.na(df$cindex_full_lambdamin))),
    data.frame(cohort = cohort_label, model = "full_expression",
               lambda = "lambda.1se",
               mean_cindex = mean(df$cindex_full_lambda1se, na.rm = TRUE),
               sd_cindex = sd(df$cindex_full_lambda1se, na.rm = TRUE),
               n_folds = sum(!is.na(df$cindex_full_lambda1se)))
  )
}

cv_summary <- rbind(
  summarize_cv(resultsA$cv_results, "CohortA_n235"),
  summarize_cv(resultsB$cv_results, "CohortB_n163")
)
write.csv(cv_summary, file.path(out_dir, "cv_summary.csv"), row.names = FALSE)

log_msg("\n=== CV summary (mean +/- SD C-index across 25 folds) ===")
print(cv_summary)

## ------------------------------------------------------------------
## 9. Alpha selection distribution
## ------------------------------------------------------------------
alpha_selection_summary <- rbind(resultsA$alpha_summary, resultsB$alpha_summary)
write.csv(alpha_selection_summary, file.path(out_dir, "alpha_selection_summary.csv"), row.names = FALSE)

log_msg("\n=== Alpha* distribution per cohort ===")
print(table(alpha_selection_summary$cohort, alpha_selection_summary$alpha_selected))

## ------------------------------------------------------------------
## 10. Final models (fit once per cohort on the FULL cohort)
## ------------------------------------------------------------------
log_msg("\n=== Fitting final models on full cohorts ===")
finalA <- fit_final_model(cohortA, exprA, c("log_tmb", "aneu"), "CohortA")
finalB <- fit_final_model(cohortB, exprB, c("log_tmb", "aneu", "BRCA_any_mutated"), "CohortB")

write.csv(finalA$genes_lambdamin, file.path(out_dir, "final_model_genes_cohortA_lambdamin.csv"), row.names = FALSE)
write.csv(finalA$genes_lambda1se, file.path(out_dir, "final_model_genes_cohortA_lambda1se.csv"), row.names = FALSE)
write.csv(finalB$genes_lambdamin, file.path(out_dir, "final_model_genes_cohortB_lambdamin.csv"), row.names = FALSE)
write.csv(finalB$genes_lambda1se, file.path(out_dir, "final_model_genes_cohortB_lambda1se.csv"), row.names = FALSE)

## ---- Persist FINAL-model alpha* per cohort â†’ CSV ----
## Added 2026-07-20 (Phase 3 of AUDIT_2026-07-20.md fixes). The manuscript's
## "pure ridge (alpha*=0)" claim for Cohort B refers to the FINAL refit's
## selected alpha, which was only printed to stdout (line ~395). The per-fold
## CV distribution (alpha_selection_summary.csv) does NOT support "alpha=0"
## as a blanket statement, so the final-model value is written explicitly.
final_alpha_summary <- data.frame(
  cohort = c("CohortA_n235", "CohortB_n163"),
  final_model_alpha = c(finalA$alpha_selected, finalB$alpha_selected),
  lambda_min = c(finalA$lambda_min, finalB$lambda_min),
  lambda_1se = c(finalA$lambda_1se, finalB$lambda_1se),
  manuscript_claim = c(NA, 0),
  stringsAsFactors = FALSE
)
write.csv(final_alpha_summary, file.path(out_dir, "final_model_alpha.csv"), row.names = FALSE)
log_msg(sprintf("Final-model alpha*: CohortA=%.1f  CohortB=%.1f  -> final_model_alpha.csv",
                finalA$alpha_selected, finalB$alpha_selected))

## ------------------------------------------------------------------
## 11. EMT/ECM gene overlap tracking
## ------------------------------------------------------------------
log_msg("\n=== Building EMT/ECM gene overlap table ===")

## Explicit anchor genes carried over from Finding 5's SHAP/permutation
## tracking, plus the 24-gene MSigDB Hallmark EMT overlap already
## established at top200 in phase2_04_pathway_enrichment.py
## (enrichment_results_significant.csv, adj_p=3.45e-19).
explicit_anchor_genes <- c("CTNNB1", "THBS2", "COL1A1", "COL1A2", "THBS1", "FLNA")
msigdb_emt24_genes <- c("NOTCH2","TAGLN","LRP1","IGFBP4","COL12A1","IGFBP2","THBS2",
                         "FSTL1","SAT1","THBS1","DCN","COL1A1","ACTA2","MMP14",
                         "COL1A2","COL4A2","ANPEP","MGP","SERPINH1","FLNA","COL6A3",
                         "TGFBI","VIM","MYL9")

theme2_genes <- union(explicit_anchor_genes, msigdb_emt24_genes)
gene_source <- sapply(theme2_genes, function(g) {
  src <- c()
  if (g %in% explicit_anchor_genes) src <- c(src, "explicit_anchor")
  if (g %in% msigdb_emt24_genes) src <- c(src, "msigdb_emt24_top200")
  paste(src, collapse = ";")
})

lookup_gene <- function(df, gene) {
  row <- df[df$gene == gene, ]
  if (nrow(row) == 0) return(c(selected = FALSE, coefficient = NA, hazard_ratio = NA))
  c(selected = TRUE, coefficient = row$coefficient[1], hazard_ratio = row$hazard_ratio[1])
}

emt_rows <- list()
for (g in theme2_genes) {
  a_min <- lookup_gene(finalA$genes_lambdamin, g)
  a_1se <- lookup_gene(finalA$genes_lambda1se, g)
  b_min <- lookup_gene(finalB$genes_lambdamin, g)
  b_1se <- lookup_gene(finalB$genes_lambda1se, g)
  emt_rows[[g]] <- data.frame(
    gene = g,
    source = gene_source[[g]],
    cohortA_lambdamin_selected = as.logical(a_min["selected"]),
    cohortA_lambdamin_coef = as.numeric(a_min["coefficient"]),
    cohortA_lambdamin_HR = as.numeric(a_min["hazard_ratio"]),
    cohortA_lambda1se_selected = as.logical(a_1se["selected"]),
    cohortA_lambda1se_coef = as.numeric(a_1se["coefficient"]),
    cohortA_lambda1se_HR = as.numeric(a_1se["hazard_ratio"]),
    cohortB_lambdamin_selected = as.logical(b_min["selected"]),
    cohortB_lambdamin_coef = as.numeric(b_min["coefficient"]),
    cohortB_lambdamin_HR = as.numeric(b_min["hazard_ratio"]),
    cohortB_lambda1se_selected = as.logical(b_1se["selected"]),
    cohortB_lambda1se_coef = as.numeric(b_1se["coefficient"]),
    cohortB_lambda1se_HR = as.numeric(b_1se["hazard_ratio"])
  )
}
emt_ecm_overlap <- do.call(rbind, emt_rows)
rownames(emt_ecm_overlap) <- NULL
write.csv(emt_ecm_overlap, file.path(out_dir, "emt_ecm_overlap.csv"), row.names = FALSE)

n_selected_any <- sum(rowSums(emt_ecm_overlap[, c("cohortA_lambdamin_selected","cohortA_lambda1se_selected",
                                                    "cohortB_lambdamin_selected","cohortB_lambda1se_selected")],
                               na.rm = TRUE) > 0)
log_msg(sprintf("EMT/ECM tracked genes selected (non-zero) in at least one model/lambda: %d / %d",
                 n_selected_any, length(theme2_genes)))

## ------------------------------------------------------------------
## 12. Final report
## ------------------------------------------------------------------
log_msg("\n============================================================")
log_msg("DONE. Outputs written to:", out_dir)
log_msg("  cv_results_cohortA_n235.csv")
log_msg("  cv_results_cohortB_n163.csv")
log_msg("  cv_summary.csv")
log_msg("  alpha_selection_summary.csv")
log_msg("  final_model_genes_cohortA_lambdamin.csv / _lambda1se.csv")
log_msg("  final_model_genes_cohortB_lambdamin.csv / _lambda1se.csv")
log_msg("  emt_ecm_overlap.csv")
log_msg("============================================================")

