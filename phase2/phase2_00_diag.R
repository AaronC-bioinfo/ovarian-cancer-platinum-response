# phase2_00_diag.R
# Purpose: Confirm R is running, print working directory, and check file paths.
# Run from project root:
#   Rscript phase2\phase2_00_diag.R

cat("=== R IS RUNNING ===\n")
cat(sprintf("Working directory: %s\n", getwd()))

DATA_DIR <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

files_to_check <- c(
  "data_clinical_patient.txt",
  "data_timeline_treatment.txt",
  "data_mrna_seq_v2_rsem.txt"
)

cat("\n=== FILE CHECK ===\n")
for (f in files_to_check) {
  full_path <- file.path(DATA_DIR, f)
  exists    <- file.exists(full_path)
  cat(sprintf("  [%s] %s\n", ifelse(exists, "FOUND", "MISSING"), full_path))
}

cat("\n=== DONE ===\n")
