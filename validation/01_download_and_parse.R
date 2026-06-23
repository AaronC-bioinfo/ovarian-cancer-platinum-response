.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
# =============================================================================
# 01_download_and_parse.R
# Download GSE63885 and GSE9891 series matrix files from NCBI GEO FTP,
# parse expression matrices and sample metadata, save as CSV.
# =============================================================================

cat("=== Step 1: Download and Parse GEO Series Matrix Files ===\n")

# --- Configuration -----------------------------------------------------------
OUT_DIR <- "data/external"
dir.create(OUT_DIR, recursive = TRUE, showWarnings = FALSE)

DATASETS <- list(
  GSE63885 = list(
    url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE63nnn/GSE63885/matrix/GSE63885_series_matrix.txt.gz",
    gz  = file.path(OUT_DIR, "GSE63885_series_matrix.txt.gz"),
    txt = file.path(OUT_DIR, "GSE63885_series_matrix.txt")
  ),
  GSE9891 = list(
    url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE9nnn/GSE9891/matrix/GSE9891_series_matrix.txt.gz",
    gz  = file.path(OUT_DIR, "GSE9891_series_matrix.txt.gz"),
    txt = file.path(OUT_DIR, "GSE9891_series_matrix.txt")
  )
)

# --- Helper: download if not already present ---------------------------------
download_if_missing <- function(url, dest_gz, dest_txt) {
  if (!file.exists(dest_txt)) {
    if (!file.exists(dest_gz)) {
      cat("  Downloading", basename(dest_gz), "...\n")
      download.file(url, dest_gz, mode = "wb", quiet = FALSE)
    }
    cat("  Decompressing", basename(dest_gz), "...\n")
    R.utils::gunzip(dest_gz, dest_txt, remove = FALSE, overwrite = TRUE)
  } else {
    cat("  Already exists:", basename(dest_txt), "\n")
  }
}

# Install R.utils if needed
if (!requireNamespace("R.utils", quietly = TRUE)) {
  cat("Installing R.utils...\n")
  install.packages("R.utils", repos = "https://cloud.r-project.org")
}
library(R.utils)

# --- Download both datasets --------------------------------------------------
for (name in names(DATASETS)) {
  cat("\nProcessing", name, "\n")
  d <- DATASETS[[name]]
  download_if_missing(d$url, d$gz, d$txt)
}

# --- Helper: parse a series matrix file --------------------------------------
parse_series_matrix <- function(txt_path, dataset_name) {
  cat("\nParsing", dataset_name, "...\n")
  lines <- readLines(txt_path, warn = FALSE)

  # --- Extract metadata (lines starting with !Sample_)
  meta_lines <- lines[grepl("^!Sample_", lines)]
  meta_list  <- lapply(meta_lines, function(l) {
    parts <- strsplit(l, "\t")[[1]]
    key   <- sub("^!", "", parts[1])
    vals  <- gsub('"', '', parts[-1])
    list(key = key, vals = vals)
  })

  # Build metadata data frame
  keys <- sapply(meta_list, `[[`, "key")
  n_samples <- length(meta_list[[1]]$vals)
  meta_df <- as.data.frame(
    lapply(meta_list, function(x) x$vals),
    stringsAsFactors = FALSE
  )
  colnames(meta_df) <- keys
  meta_df$dataset <- dataset_name

  # Sample IDs from Sample_geo_accession
  sample_ids <- as.character(meta_df$Sample_geo_accession)

  # --- Extract expression matrix (lines after !series_matrix_table_begin)
  start <- which(lines == "!series_matrix_table_begin") + 1
  end   <- which(lines == "!series_matrix_table_end")   - 1

  if (length(start) == 0 || length(end) == 0) {
    stop("Could not find expression table boundaries in ", txt_path)
  }

  expr_lines <- lines[start:end]
  expr_con   <- textConnection(expr_lines)
  expr_df    <- read.table(expr_con, header = TRUE, sep = "\t",
                           quote = '"', row.names = 1,
                           stringsAsFactors = FALSE, check.names = FALSE)
  close(expr_con)

  # Assign sample IDs as column names
  if (ncol(expr_df) == length(sample_ids)) {
    colnames(expr_df) <- sample_ids
  } else {
    warning("Column count mismatch for ", dataset_name,
            ": expr=", ncol(expr_df), " meta=", length(sample_ids))
  }

  cat("  Probes:", nrow(expr_df), "| Samples:", ncol(expr_df), "\n")
  cat("  Metadata rows:", nrow(meta_df), "\n")

  list(expr = expr_df, meta = meta_df)
}

# --- Parse both datasets -----------------------------------------------------
parsed <- list()
for (name in names(DATASETS)) {
  parsed[[name]] <- parse_series_matrix(DATASETS[[name]]$txt, name)
}

# --- Save raw parsed outputs -------------------------------------------------
cat("\nSaving raw parsed outputs...\n")

for (name in names(parsed)) {
  expr_path <- file.path(OUT_DIR, paste0(name, "_expr_raw.csv"))
  meta_path <- file.path(OUT_DIR, paste0(name, "_meta_raw.csv"))

  write.csv(parsed[[name]]$expr, expr_path, quote = FALSE)
  write.csv(parsed[[name]]$meta, meta_path, row.names = FALSE, quote = FALSE)

  cat("  Saved:", basename(expr_path), "\n")
  cat("  Saved:", basename(meta_path), "\n")
}

# --- Quick sanity check ------------------------------------------------------
cat("\n=== Sanity Check ===\n")
for (name in names(parsed)) {
  cat(name, "—",
      nrow(parsed[[name]]$expr), "probes x",
      ncol(parsed[[name]]$expr), "samples\n")
  cat("  Metadata columns:", paste(colnames(parsed[[name]]$meta), collapse=", "), "\n\n")
}

cat("=== Step 1 Complete ===\n")
cat("Next: run 02_probe_mapping.R\n")
