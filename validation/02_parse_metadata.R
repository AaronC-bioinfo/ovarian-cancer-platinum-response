.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# =============================================================================
# 02_parse_metadata.R
# Parse characteristics fields from both GEO series matrix files,
# filter to serous/undifferentiated histology, assign binary platinum labels.
# Output: data/external/metadata_clean.csv
# =============================================================================

cat("=== Step 2: Parse Metadata and Filter Histology ===\n")

OUT_DIR <- "data/external"

# --- Helper: parse characteristics rows into named columns ------------------
parse_characteristics <- function(txt_path, dataset_name) {
  cat("\nParsing characteristics for", dataset_name, "...\n")
  lines <- readLines(txt_path, warn = FALSE)

  # Get sample IDs from !Sample_geo_accession line
  acc_line  <- lines[grepl("^!Sample_geo_accession", lines)][1]
  parts     <- strsplit(acc_line, "\t")[[1]]
  sample_ids <- gsub('"', '', parts[-1])
  n_samples  <- length(sample_ids)

  # Get all characteristics lines
  char_lines <- lines[grepl("^!Sample_characteristics_ch1", lines)]

  # Parse each line: extract key from first value, then all values
  result <- data.frame(sample_id = sample_ids, dataset = dataset_name,
                       stringsAsFactors = FALSE)

  for (cl in char_lines) {
    parts <- strsplit(cl, "\t")[[1]]
    vals  <- gsub('"', '', parts[-1])  # remove quotes, drop first col

    # Extract key from first non-NA value
    first_val <- vals[!is.na(vals) & nchar(trimws(vals)) > 0][1]
    if (is.na(first_val)) next

    # Key is everything before the first ":"
    key <- trimws(sub(":.*", "", first_val))
    # Clean key to be a valid column name
    key_clean <- gsub("[^a-zA-Z0-9]", "_", tolower(key))
    key_clean <- gsub("_+", "_", key_clean)
    key_clean <- sub("_$", "", key_clean)

    # Value is everything after the first ":"
    clean_vals <- trimws(sub("^[^:]+:\\s*", "", vals))
    clean_vals[clean_vals == "NA"] <- NA

    if (length(clean_vals) == n_samples) {
      result[[key_clean]] <- clean_vals
    } else {
      cat("  WARNING: column", key_clean, "has", length(clean_vals),
          "values, expected", n_samples, "— skipping\n")
    }
  }

  cat("  Samples:", nrow(result), "| Columns:", ncol(result), "\n")
  result
}

# --- Parse both datasets ----------------------------------------------------
meta63 <- parse_characteristics(
  file.path(OUT_DIR, "GSE63885_series_matrix.txt"), "GSE63885")
meta98 <- parse_characteristics(
  file.path(OUT_DIR, "GSE9891_series_matrix.txt"),  "GSE9891")

cat("\n=== Column names ===\n")
cat("GSE63885:", paste(colnames(meta63), collapse=", "), "\n\n")
cat("GSE9891: ", paste(colnames(meta98), collapse=", "), "\n\n")

# --- Filter GSE63885: serous + undifferentiated only ------------------------
cat("=== GSE63885 histology counts ===\n")
print(table(meta63$histophatological_type_of_tumor, useNA="ifany"))

keep63 <- grepl("serous|undifferentiated", 
                meta63$histophatological_type_of_tumor, 
                ignore.case = TRUE)
meta63_f <- meta63[keep63, ]
cat("\nAfter serous/undifferentiated filter:", nrow(meta63_f), "samples\n")

# --- Filter GSE9891: Ser/PapSer (serous) + Malignant only -------------------
cat("\n=== GSE9891 Type counts ===\n")
print(table(meta98$type, useNA="ifany"))
cat("\n=== GSE9891 Subtype counts ===\n")
print(table(meta98$subtype, useNA="ifany"))

keep98 <- meta98$type == "Malignant" & 
          grepl("Ser/PapSer", meta98$subtype, fixed = TRUE)
meta98_f <- meta98[keep98, ]
cat("\nAfter Malignant+Ser/PapSer filter:", nrow(meta98_f), "samples\n")

# --- Assign binary platinum label for GSE63885 ------------------------------
# Primary label: clinical status (CR/PR = responder=0; P/SD = non-responder=1)
# Secondary: platinum sensitivity (resistant=1; moderately/highly sensitive=0)
# Tertiary: DFS-derived (DFS <= 180 days = resistant=1)

cat("\n=== GSE63885 clinical status counts ===\n")
cs_col <- grep("clinical_status_post", colnames(meta63_f), value=TRUE)[1]
cat("Using column:", cs_col, "\n")
print(table(meta63_f[[cs_col]], useNA="ifany"))

cat("\n=== GSE63885 platinum sensitivity counts ===\n")
ps_col <- grep("platinium_sensitivity|platinum_sensitivity", 
               colnames(meta63_f), value=TRUE)[1]
cat("Using column:", ps_col, "\n")
print(table(meta63_f[[ps_col]], useNA="ifany"))

# Assign label
meta63_f$platinum_label_clinical <- ifelse(
  meta63_f[[cs_col]] %in% c("CR", "PR"), 0L,   # responder
  ifelse(meta63_f[[cs_col]] %in% c("P", "SD"), 1L,  # non-responder
  NA_integer_))

meta63_f$platinum_label_dfs <- ifelse(
  meta63_f[[ps_col]] %in% c("resistant"), 1L,
  ifelse(meta63_f[[ps_col]] %in% c("moderately sensitive","highly sensitive"), 0L,
  NA_integer_))

cat("\nGSE63885 clinical label distribution:\n")
print(table(meta63_f$platinum_label_clinical, useNA="ifany"))
cat("\nGSE63885 DFS-based label distribution:\n")
print(table(meta63_f$platinum_label_dfs, useNA="ifany"))

# --- Assign binary platinum label for GSE9891 --------------------------------
cat("\n=== GSE9891 available columns for labeling ===\n")
cat(paste(colnames(meta98_f), collapse=", "), "\n")

# GSE9891 uses PFI (platinum-free interval) — look for debulking/survival cols
survival_cols <- grep("surv|pfi|pfs|os|debulk|response|chemo|plat|resist|sensitiv",
                      colnames(meta98_f), ignore.case=TRUE, value=TRUE)
cat("\nSurvival/response-related columns found:", 
    paste(survival_cols, collapse=", "), "\n")

for (col in survival_cols) {
  cat("\n", col, ":\n")
  print(table(meta98_f[[col]], useNA="ifany"))
}

# --- Save filtered metadata --------------------------------------------------
cat("\n=== Saving filtered metadata ===\n")
write.csv(meta63_f, file.path(OUT_DIR, "GSE63885_meta_clean.csv"),
          row.names=FALSE)
write.csv(meta98_f, file.path(OUT_DIR, "GSE9891_meta_clean.csv"),
          row.names=FALSE)

cat("Saved GSE63885_meta_clean.csv —", nrow(meta63_f), "samples\n")
cat("Saved GSE9891_meta_clean.csv  —", nrow(meta98_f), "samples\n")

cat("\n=== Step 2 Complete ===\n")
cat("Next: run 03_probe_mapping.R\n")
