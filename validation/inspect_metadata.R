.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

cat("=== GSE63885 characteristics ===\n")
lines <- readLines("data/external/GSE63885_series_matrix.txt", warn = FALSE)
meta  <- lines[grepl("^!Sample_characteristics_ch1", lines)]
cat(meta[1:15], sep = "\n")

cat("\n\n=== GSE9891 characteristics ===\n")
lines <- readLines("data/external/GSE9891_series_matrix.txt", warn = FALSE)
meta  <- lines[grepl("^!Sample_characteristics_ch1", lines)]
cat(meta[1:10], sep = "\n")
