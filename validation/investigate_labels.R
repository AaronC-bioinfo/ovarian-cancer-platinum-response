.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# =============================================================================
# investigate_labels.R
# 1. Check what supplementary files GSE9891 has
# 2. Fix GSE63885 platinum sensitivity column parsing
# =============================================================================

cat("=== Investigating label availability ===\n\n")

OUT_DIR <- "data/external"

# --- GSE9891: look for supplementary file references in series matrix --------
cat("--- GSE9891 supplementary file lines ---\n")
lines98 <- readLines(file.path(OUT_DIR, "GSE9891_series_matrix.txt"), warn=FALSE)
suppl_lines <- lines98[grepl("supplementary|Series_overall|Series_summary|Series_type", 
                              lines98, ignore.case=TRUE)]
cat(suppl_lines[1:20], sep="\n")

cat("\n\n--- GSE9891 Series-level metadata ---\n")
series_lines <- lines98[grepl("^!Series_", lines98)]
cat(series_lines, sep="\n")

# --- GSE63885: show raw platinum sensitivity lines to debug parsing ----------
cat("\n\n--- GSE63885 raw platinum sensitivity line (first 300 chars) ---\n")
lines63 <- readLines(file.path(OUT_DIR, "GSE63885_series_matrix.txt"), warn=FALSE)
plat_line <- lines63[grepl("platinium_sensitivity|platinium sensitivity", 
                             lines63, ignore.case=TRUE)]
if (length(plat_line) > 0) {
  # Split by tab and show first few values
  parts <- strsplit(plat_line[1], "\t")[[1]]
  cat("Number of tab-separated fields:", length(parts), "\n")
  cat("First field (key):", parts[1], "\n")
  cat("First value:", gsub('"','', parts[2]), "\n")
  cat("Second value:", gsub('"','', parts[3]), "\n")
  cat("Last non-NA value:", gsub('"','', parts[length(parts)]), "\n")
} else {
  cat("No platinum sensitivity line found — checking column names:\n")
  char_lines <- lines63[grepl("^!Sample_characteristics_ch1", lines63)]
  for (i in seq_along(char_lines)) {
    parts <- strsplit(char_lines[i], "\t")[[1]]
    first_val <- gsub('"','', parts[2])
    cat("Row", i, ":", substr(first_val, 1, 60), "\n")
  }
}

# --- GSE9891: check if there's a separate clinical data file on GEO ----------
cat("\n\n--- GSE9891 Sample_supplementary_file lines ---\n")
suppl_sample <- lines98[grepl("^!Sample_supplementary_file", lines98)]
if (length(suppl_sample) > 0) {
  cat(suppl_sample[1], "\n")
} else {
  cat("No sample supplementary files found\n")
}

cat("\n\n--- GSE9891 description lines (may contain survival info) ---\n")
desc_lines <- lines98[grepl("^!Sample_description", lines98)]
if (length(desc_lines) > 0) {
  parts <- strsplit(desc_lines[1], "\t")[[1]]
  cat("First few descriptions:\n")
  cat(gsub('"','', parts[2:6]), sep="\n")
}

cat("\n=== Done ===\n")
