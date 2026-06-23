.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# =============================================================================
# 03_fix_labels.R
# 1. Download GSE9891_clinical_anns.csv and inspect survival/response columns
# 2. Fix GSE63885 platinum sensitivity parsing
# =============================================================================

cat("=== Step 3: Fix Labels ===\n\n")

OUT_DIR <- "data/external"

# --- Download GSE9891 clinical annotations -----------------------------------
clin_path <- file.path(OUT_DIR, "GSE9891_clinical_anns.csv")

if (!file.exists(clin_path)) {
  cat("Downloading GSE9891_clinical_anns.csv ...\n")
  download.file(
    "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE9nnn/GSE9891/suppl/GSE9891_clinical_anns.csv",
    clin_path, mode = "wb"
  )
} else {
  cat("Already exists: GSE9891_clinical_anns.csv\n")
}

cat("\n--- GSE9891 clinical annotations: first look ---\n")
clin98 <- read.csv(clin_path, stringsAsFactors = FALSE, check.names = FALSE)
cat("Dimensions:", nrow(clin98), "rows x", ncol(clin98), "cols\n")
cat("Column names:\n")
print(colnames(clin98))
cat("\nFirst 5 rows:\n")
print(head(clin98, 5))

cat("\n--- Column value distributions ---\n")
for (col in colnames(clin98)) {
  vals <- clin98[[col]]
  if (is.numeric(vals)) {
    cat(col, ": numeric, range", min(vals, na.rm=TRUE), 
        "to", max(vals, na.rm=TRUE), 
        ", NAs:", sum(is.na(vals)), "\n")
  } else {
    cat(col, ":\n")
    print(table(vals, useNA="ifany"))
    cat("\n")
  }
}

# --- Fix GSE63885 platinum sensitivity ---------------------------------------
cat("\n\n--- Fixing GSE63885 platinum sensitivity ---\n")

lines63 <- readLines(file.path(OUT_DIR, "GSE63885_series_matrix.txt"), warn=FALSE)
char_lines <- lines63[grepl("^!Sample_characteristics_ch1", lines63)]

cat("Total characteristics rows in GSE63885:", length(char_lines), "\n")
cat("\nKey from each row:\n")
for (i in seq_along(char_lines)) {
  parts <- strsplit(char_lines[i], "\t")[[1]]
  first_val <- gsub('"', '', parts[2])
  key <- trimws(sub(":.*", "", first_val))
  cat(i, ":", key, "\n")
}

# Extract platinum sensitivity values directly by row index
# Row 11 based on earlier inspection = platinum sensitivity
plat_row <- char_lines[grepl("platinium sensitivity", char_lines, ignore.case=TRUE)]
if (length(plat_row) > 0) {
  parts <- strsplit(plat_row[1], "\t")[[1]]
  vals  <- gsub('"', '', parts[-1])
  # Extract just the value after the last ":"
  clean_vals <- trimws(sub(".*:\\s*", "", vals))
  clean_vals[clean_vals == "NA"] <- NA
  cat("\nPlatinum sensitivity values (first 10):\n")
  print(clean_vals[1:10])
  cat("\nDistribution:\n")
  print(table(clean_vals, useNA="ifany"))
  
  # Save as a lookup for later use
  # Get sample IDs
  acc_line  <- lines63[grepl("^!Sample_geo_accession", lines63)][1]
  acc_parts <- strsplit(acc_line, "\t")[[1]]
  sample_ids <- gsub('"', '', acc_parts[-1])
  
  plat_fix <- data.frame(
    sample_id = sample_ids,
    platinum_sensitivity_raw = clean_vals,
    platinum_label_dfs = ifelse(clean_vals == "resistant", 1L,
                         ifelse(clean_vals %in% c("moderately sensitive", 
                                                   "highly sensitive"), 0L,
                         NA_integer_)),
    stringsAsFactors = FALSE
  )
  write.csv(plat_fix, file.path(OUT_DIR, "GSE63885_plat_fix.csv"), 
            row.names=FALSE)
  cat("\nFixed platinum label distribution:\n")
  print(table(plat_fix$platinum_label_dfs, useNA="ifany"))
  cat("Saved GSE63885_plat_fix.csv\n")
}

cat("\n=== Step 3 Complete ===\n")
