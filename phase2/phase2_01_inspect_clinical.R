# phase2_01_inspect_clinical.R  (v2)
# Fixes: (1) use AGENT column directly for platinum filter
#        (2) check data_clinical_sample.txt for TMB / ANEUPLOIDY_SCORE
# Run from project root:
#   Rscript phase2\phase2_01_inspect_clinical.R

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

DATA_DIR <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

# ── Helper: load a cBioPortal tab-delimited file (skips # comment lines) ──────
load_cbio <- function(path) {
  read.table(path, header = TRUE, sep = "\t",
             comment.char = "#", quote = "",
             stringsAsFactors = FALSE, check.names = FALSE)
}

# ── 1. Clinical patient file ───────────────────────────────────────────────────
cat("Loading data_clinical_patient.txt...\n")
clin <- load_cbio(file.path(DATA_DIR, "data_clinical_patient.txt"))
cat(sprintf("  %d rows x %d cols\n", nrow(clin), ncol(clin)))

# ── 2. Clinical sample file (TMB / ANEUPLOIDY_SCORE live here) ────────────────
sample_path <- file.path(DATA_DIR, "data_clinical_sample.txt")
if (file.exists(sample_path)) {
  cat("\nLoading data_clinical_sample.txt...\n")
  samp <- load_cbio(sample_path)
  cat(sprintf("  %d rows x %d cols\n", nrow(samp), ncol(samp)))
  cat("  Column names:\n")
  print(colnames(samp))
} else {
  cat("\nWARNING: data_clinical_sample.txt NOT FOUND\n")
  cat("Files present in DATA_DIR:\n")
  print(list.files(DATA_DIR, pattern = "\\.txt$"))
  samp <- NULL
}

# ── 3. Treatment timeline -> platinum patients ─────────────────────────────────
cat("\nLoading data_timeline_treatment.txt...\n")
trt <- load_cbio(file.path(DATA_DIR, "data_timeline_treatment.txt"))
cat(sprintf("  %d rows x %d cols\n", nrow(trt), ncol(trt)))

cat("\n  Unique AGENT values (first 30):\n")
print(head(sort(unique(trt$AGENT)), 30))

plat_rows     <- trt[grepl("platin", trt$AGENT, ignore.case = TRUE), ]
plat_patients <- unique(plat_rows$PATIENT_ID)
cat(sprintf("\n  AGENT values matching 'platin': %d rows, %d unique patients\n",
            nrow(plat_rows), length(plat_patients)))

cat("  Matching AGENT values found:\n")
print(unique(plat_rows$AGENT))

# ── 4. Filter clinical patient data to platinum subset ────────────────────────
clin_plat <- clin[clin$PATIENT_ID %in% plat_patients, ]
cat(sprintf("\nPlatinum-subset (patient file): %d patients\n", nrow(clin_plat)))

# ── 5. Join sample-level data if available ────────────────────────────────────
if (!is.null(samp)) {
  pid_col_samp <- if ("PATIENT_ID" %in% colnames(samp)) "PATIENT_ID" else colnames(samp)[1]
  cat(sprintf("\nJoining sample file on column: %s\n", pid_col_samp))

  samp_dedup <- samp[!duplicated(samp[[pid_col_samp]]), ]

  merged <- merge(clin_plat, samp_dedup, by.x = "PATIENT_ID",
                  by.y = pid_col_samp, all.x = TRUE, suffixes = c("", "_samp"))
  cat(sprintf("After join: %d rows x %d cols\n", nrow(merged), ncol(merged)))
} else {
  merged <- clin_plat
}

# ── 6. Coverage report ─────────────────────────────────────────────────────────
cat("\n══════════════════════════════════════════════\n")
cat("COVERAGE REPORT — platinum-treated subset\n")
cat("══════════════════════════════════════════════\n")

report_col <- function(df, pattern, label) {
  col <- grep(pattern, colnames(df), ignore.case = TRUE, value = TRUE)
  if (length(col) == 0) {
    cat(sprintf("  %-28s  ** COLUMN NOT FOUND **\n", label))
    return(invisible(NA_character_))
  }
  col <- col[1]
  vals <- df[[col]]
  vals[vals %in% c("", "NA", "[Not Available]", "[Not Evaluated]")] <- NA
  n_total   <- nrow(df)
  n_missing <- sum(is.na(vals))
  n_present <- n_total - n_missing
  pct       <- round(100 * n_present / n_total, 1)
  cat(sprintf("  %-28s  col='%s'  %d/%d present (%.1f%%)\n",
              label, col, n_present, n_total, pct))
  nums <- suppressWarnings(as.numeric(vals))
  if (!all(is.na(nums))) {
    cat(sprintf("    numeric range: %.3f - %.3f  |  median: %.3f\n",
                min(nums, na.rm=TRUE), max(nums, na.rm=TRUE), median(nums, na.rm=TRUE)))
  } else {
    cat(sprintf("    value counts: %s\n",
                paste(names(table(vals, useNA="no")),
                      table(vals, useNA="no"), sep="=", collapse=" | ")))
  }
  invisible(col)
}

report_col(merged, "^OS_MONTHS$",        "OS_MONTHS")
report_col(merged, "^OS_STATUS$",        "OS_STATUS")
report_col(merged, "TMB",                "TMB_NONSYNONYMOUS")
report_col(merged, "ANEUPLOIDY",         "ANEUPLOIDY_SCORE")

# ── 7. Complete-case count across all 4 key variables ────────────────────────
cat("\n-- Complete-case count (OS_MONTHS + OS_STATUS + TMB + ANEUPLOIDY) --\n")
key_patterns <- c("^OS_MONTHS$", "^OS_STATUS$", "TMB", "ANEUPLOIDY")
key_cols <- sapply(key_patterns, function(p)
  grep(p, colnames(merged), ignore.case=TRUE, value=TRUE)[1])
key_cols <- key_cols[!is.na(key_cols)]
cat("  Using columns: "); print(key_cols)

if (length(key_cols) >= 2) {
  sub <- merged[, key_cols, drop=FALSE]
  for (col in key_cols) {
    v <- sub[[col]]
    v[v %in% c("", "NA", "[Not Available]", "[Not Evaluated]")] <- NA
    sub[[col]] <- v
  }
  cc <- sum(complete.cases(sub))
  cat(sprintf("  Complete cases: %d / %d\n", cc, nrow(sub)))
}

cat("\n══════════════════════════════════════════════\n")
cat("Done. Paste full output into chat.\n")
