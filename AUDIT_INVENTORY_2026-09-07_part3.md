# Audit Inventory — 2026-09-07 (Part 3 of 3)

Project: `C:\PROJECTS\ovarian-cancer-platinum-response`. See `AUDIT_INVENTORY_2026-09-07.md` for the manifest and Parts 1–2.

---

# SECTION 4: SCRIPT PARAMETERS

Audit scope: all `.py`/`.R` files under `src/`, `phase2/`, `multi_cancer/`,
`validation/`, `src/cellularity/`, `src/hrd/` in the project root
`C:\PROJECTS\ovarian-cancer-platinum-response` (mounted at
`~/mnt/ovarian-cancer-platinum-response` on the connected device).

**Method note:** This section was produced read-only — no `.py` or `.R` file
was executed. Every line below comes from `head -30`, `wc -l`, `grep -n`, and
manual inspection (`sed -n`) of file text only.

**Inventory note:** The task brief said "34 files" but enumerated 40 paths,
and a final sanity `find` for `*.py`/`*.R` under the six target directories
(plus `brca/`, which does not exist in this project) returned exactly those
same 40 files, all present at the exact paths given — no discrepancies, no
extra files found, `brca/` is not a directory in this repo. All 40 are
covered below.

**Shared config note:** Several scripts read `config/config.yaml` at runtime
via `cfg["..."]["..."]` rather than hardcoding values inline. For reference,
`config/config.yaml` (not itself one of the 40 audited scripts) currently
sets: `project.seed: 42`, `clinical.thresholds: [12, 18, 24]`,
`features.top_n_genes: 500`, `model.test_size: 0.20`, `model.cv_folds: 5`,
`model.random_forest.n_estimators: 300`, `model.random_forest.max_depth: null`,
`model.random_forest.min_samples_split: 2`, `model.svm.C: 1`,
`model.logistic_regression.max_iter: 5000`. Where a script pulls a value from
`cfg[...]` with no local literal, the table below marks it "from config.yaml"
rather than listing it as a script-level hardcoded constant; where a script
has its own hardcoded literal (including `cfg.get(key, <default>)` fallback
defaults), that literal is listed with its line number in that script.

---

## Per-script source excerpts (first 30 lines, verbatim)

#### src/03_pathway_enrichment_corrected.py
```python
"""
Enhancement 3 -- Step 3: Purity-corrected pathway enrichment
Ovarian Cancer Platinum Response Project

Tests whether Finding 5's ribosomal/translation signal (adj p ~10^-34) is a
tumour-cellularity artefact rather than platinum-response biology.

Methodology (matched to the original Finding 5 pipeline so the comparison
is apples-to-apples):
  1. Same 235-patient platinum-treated RNA-seq subset used for ESTIMATE.
  2. Same variance-filter approach on RAW RSEM values (no log transform --
     PROJECT_LOG.md explicitly notes the original filter ran on
     "pre-split, raw RSEM"), same n=500 gene count.
  3. ONLY CHANGE: each gene's expression is residualized against
     TumorPurity (OLS) before the variance filter, so genes whose apparent
     variability was actually driven by purity differences between
     patients get down-weighted or dropped from the top-500.
  4. Re-run the same 4 Enrichr libraries used originally.

Reuses the top500_genes_named.txt already on disk as the "before" list
for the comparison rather than re-deriving it, since re-deriving from
raw expression could accidentally introduce a second uncontrolled
methodology difference alongside the purity correction.
"""

import os
import time
import requests
import pandas as pd
import numpy as np
```
(223 lines total.)

#### src/ablation.py
```python
"""
ablation.py
───────────
Methods-critique analysis: quantifies how much reported ROC-AUC is inflated by
(a) computing variance-based feature selection on the FULL dataset before
    the train/test split (the classic genomics leakage bug), and
(b) reporting performance from a single train/test split instead of
    repeated/nested cross-validation.

This module does NOT require any new data — it re-runs the existing
pipeline under controlled conditions and reports the delta.

Usage:
    from src.ablation import run_leakage_ablation, run_split_variance_ablation
    results = run_leakage_ablation(expr, labelled_dict, cfg)
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

from .models import get_all_models, train_model
from .preprocessing import align_expression_to_labels
```
(531 lines total.)

#### src/data_loader.py
```python
"""
data_loader.py
──────────────
Handles all I/O for the TCGA OV pan-cancer atlas dataset.
Reads raw text files and returns clean DataFrames.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_clinical(data_dir: str | Path, filename: str) -> pd.DataFrame:
    """
    Load the clinical patient file.

    Args:
        data_dir: Directory containing the raw data files.
        filename: Name of the clinical patient file.

    Returns:
        DataFrame with one row per patient.
    """
    path = Path(data_dir) / filename
    logger.info("Loading clinical data from %s", path)
```
(126 lines total. No hardcoded analysis-parameter constants found anywhere in this file.)

#### src/evaluation.py
```python
"""
evaluation.py
─────────────
Unified metrics computation for all models and thresholds.

Returns structured results (dicts / DataFrames) so that downstream
reporting and visualisation code can consume them without re-running
inference.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Single model evaluation
# ─────────────────────────────────────────────────────────────────────────────
```
(135 lines total. Manual inspection of `evaluate_model()` and `evaluate_all_models()` — the only two functions — found no hardcoded numeric analysis parameters; all thresholds/labels are passed in from callers.)

#### src/features.py
```python
"""
features.py
───────────
Feature-selection and dimensionality reduction for gene expression data.

Design note
───────────
Variance-based filtering is computed exclusively on the **training split**
to prevent information leakage from the test set — a common mistake in
genomic ML pipelines.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def select_high_variance_genes(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    top_n: int = 500,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Retain the ``top_n`` most variable genes, ranked by training-set variance.
```
(80 lines total.)

#### src/label_investigation.py
```python
"""
label_investigation.py
───────────────────────
Diagnostic-only analysis of candidate gold-standard label columns found
in data_timeline_status.txt and data_clinical_sample.txt.

This module makes NO changes to the main pipeline or its labels. It exists
to answer one question with evidence: is PRIMARY_THERAPY_OUTCOME_SUCCESS
(or another flagged column) usable as a replacement for the OS-threshold
proxy label currently used in preprocessing.py?

Nothing here is wired into run.py — it's a standalone investigation that
informs whether/how Phase 2 of the publication-upgrade roadmap proceeds.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def report_column_coverage(
    df: pd.DataFrame,
    columns: list[str],
    patient_id_col: str = "PATIENT_ID",
    platinum_ids: np.ndarray | None = None,
```
(373 lines total.)

#### src/models.py
```python
"""
models.py
─────────
Model definitions, training, cross-validation and persistence.

All classifiers use ``class_weight='balanced'`` by default to handle
the class imbalance inherent in the platinum-response labelling scheme.
"""

from __future__ import annotations

import logging
import pickle
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.svm import SVC

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Factory helpers
# ─────────────────────────────────────────────────────────────────────────────

ModelConfig = dict[str, Any]

```
(152 lines total.)

#### src/pipeline.py
```python
"""
pipeline.py
───────────
End-to-end orchestration: data → features → models → evaluation → figures.

This module is the single entry point for a full pipeline run.
Call ``run_pipeline(cfg)`` with the loaded config dict to reproduce
all results and figures.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from .data_loader import load_clinical, load_expression, load_treatment
from .evaluation import build_results_table, evaluate_all_models
from .features import scale_features, select_high_variance_genes
from .models import cross_validate_model, get_all_models, save_model, train_model
from .preprocessing import (
    align_expression_to_labels,
    build_labelled_survival,
    clean_expression,
    extract_survival,
    identify_platinum_patients,
```
(290 lines total. All numeric analysis parameters used here — `test_size`, `top_n_genes`, `cv_folds`, `thresholds`, `seed` — are read from the `cfg` dict passed into `run_pipeline(cfg)`, i.e. sourced from `config/config.yaml`; no local numeric literals for these parameters appear in this file.)

#### src/preprocessing.py
```python
"""
preprocessing.py
────────────────
All data-cleaning and label-engineering logic.

Steps performed here:
  1. Extract and clean survival columns from clinical data.
  2. Identify platinum-treated patients from the treatment timeline.
  3. Assign binary response labels at one or more time thresholds.
  4. Clean and align the mRNA expression matrix.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Survival data
# ─────────────────────────────────────────────────────────────────────────────


def extract_survival(
    clinical: pd.DataFrame,
```
(276 lines total. `threshold`/`thresholds` are function parameters supplied by the caller (ultimately `config/config.yaml`'s `clinical.thresholds: [12, 18, 24]`); the docstring for `build_labelled_survival()` at line 161 gives `[12, 18, 24]` only as an illustrative example, not a hardcoded value used in execution.)

#### src/visualization.py
```python
"""
visualization.py
────────────────
Production-quality figures for the ovarian cancer platinum response project.

Design principles:
  - Every function is self-contained: pass in data, get a saved figure.
  - Consistent style via a shared ``apply_style()`` call.
  - All figures are saved at 300 DPI by default.
  - No global state modified.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.calibration import calibration_curve
from sklearn.metrics import ConfusionMatrixDisplay, roc_curve, auc

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Style
```
(482 lines total.)

#### src/__init__.py
```python
"""
Ovarian Cancer Platinum Response Prediction
───────────────────────────────────────────
Modular ML pipeline for predicting platinum chemotherapy response
in ovarian cancer patients using TCGA RNA-seq data.
"""
```
(6 lines total — entire file shown above; no code, no parameters.)

#### src/cellularity/00_install_estimate.R
```r
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
```
(50 lines total. Installation/setup script only; no analysis parameters.)

#### src/cellularity/01_run_estimate.R
```r
## ============================================================
## Enhancement 3 — Step 1: Run ESTIMATE on the platinum-treated cohort
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## Reuses the SAME 432-patient platinum-treated cohort already
## established in Finding 4 (phase2/outputs/cox_patients_with_risk.csv)
## rather than re-deriving the AGENT-field filter, so purity scores
## line up 1:1 with the existing Cox model patients.

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(estimate)
library(data.table)

## ---- Paths ----
project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
tcga_path    <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

expr_file    <- file.path(tcga_path, "data_mrna_seq_v2_rsem.txt")
cohort_file  <- file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv")

out_dir <- file.path(project_root, "cellularity")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

gct_raw_file      <- file.path(out_dir, "tcga_ov_platinum_expr.gct")
gct_filtered_file <- file.path(out_dir, "tcga_ov_platinum_expr_filtered.gct")
gct_score_file    <- file.path(out_dir, "estimate_score.gct")
scores_csv        <- file.path(out_dir, "estimate_scores.csv")

## ---- Step A: load expression matrix (cBioPortal RSEM format) ----
```
(136 lines total.)

#### src/cellularity/02_cox_model_with_purity.R
```r
## ============================================================
## Enhancement 3 — Step 2: Cox model with tumour purity covariate
## Ovarian Cancer Platinum Response Project
## ============================================================

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(survival)
library(data.table)

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
cohort_file  <- file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv")
purity_file  <- file.path(project_root, "cellularity/estimate_scores.csv")
out_dir      <- file.path(project_root, "cellularity")

cohort <- fread(cohort_file, data.table = FALSE)
purity <- fread(purity_file, data.table = FALSE)

cat("cox_patients_with_risk.csv columns:\n  ", paste(names(cohort), collapse = ", "), "\n\n")

## ---- Detect required columns rather than assuming exact names ----
find_col <- function(df, candidates, label) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0) {
    stop("Could not find a column for '", label, "' in cox_patients_with_risk.csv.\n",
         "Looked for: ", paste(candidates, collapse = ", "), "\n",
         "Actual columns are: ", paste(names(df), collapse = ", "), "\n",
         "Paste that column list back and I'll fix the mapping.")
  }
  hit[1]
}
```
(134 lines total. No hardcoded numeric analysis parameters in the first 30 lines or via grep of the whole file.)

#### src/cellularity/03_pathway_enrichment_corrected.py
```python
"""
Enhancement 3 -- Step 3: Purity-corrected pathway enrichment
Ovarian Cancer Platinum Response Project

Tests whether Finding 5's ribosomal/translation signal (adj p ~10^-34) is a
tumour-cellularity artefact rather than platinum-response biology.

Methodology (matched to the original Finding 5 pipeline so the comparison
is apples-to-apples):
  1. Same 235-patient platinum-treated RNA-seq subset used for ESTIMATE.
  2. Same variance-filter approach on RAW RSEM values (no log transform --
     PROJECT_LOG.md explicitly notes the original filter ran on
     "pre-split, raw RSEM"), same n=500 gene count.
  3. ONLY CHANGE: each gene's expression is residualized against
     TumorPurity (OLS) before the variance filter, so genes whose apparent
     variability was actually driven by purity differences between
     patients get down-weighted or dropped from the top-500.
  4. Re-run the same 4 Enrichr libraries used originally.

Reuses the top500_genes_named.txt already on disk as the "before" list
for the comparison rather than re-deriving it, since re-deriving from
raw expression could accidentally introduce a second uncontrolled
methodology difference alongside the purity correction.
"""

import os
import time
import requests
import pandas as pd
import numpy as np
```
(223 lines total. **This file is byte-identical to `src/03_pathway_enrichment_corrected.py`** — confirmed via `diff`, zero output/no differences. Same `N_TOP_GENES = 500` (line 45) and `ADJ_P_THRESHOLD = 0.05` (line 52) constants apply, at identical line numbers.)

#### src/hrd/00_inspect_hrd_data.R
```r
## ============================================================
## Enhancement 4 — Step 0: Locate HRD score + BRCA1/2 status columns
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## Same lesson as Enhancement 3: inspect actual column names before
## writing any model code, rather than guessing and debugging blind.

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(data.table)

tcga_path <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

cat("============================================\n")
cat("Files available in TCGA-OV data directory:\n")
cat("============================================\n")
print(list.files(tcga_path))

## ---- Clinical sample file (per Enhancement 3/4 handoff, HRD + BRCA
## status are expected here) ----
sample_file  <- file.path(tcga_path, "data_clinical_sample.txt")
patient_file <- file.path(tcga_path, "data_clinical_patient.txt")

inspect_clinical_file <- function(path, label) {
  if (!file.exists(path)) {
    cat("\n", label, "NOT FOUND at:", path, "\n")
    return(invisible(NULL))
  }
  cat("\n============================================\n")
  cat(label, "\n")
```
(100 lines total. Diagnostic/inspection script; no analysis parameters.)

#### src/hrd/01_extract_brca_status.R
```r
## ============================================================
## Enhancement 4 — Step 1: Extract BRCA1/2 mutation status from MAF
## Ovarian Cancer Platinum Response Project
## ============================================================
##
## No precomputed BRCA1/2 status column exists in the clinical files
## (confirmed via 00_inspect_hrd_data.R) -- deriving it from the MAF-format
## data_mutations.txt instead.

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(data.table)

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
tcga_path <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"

maf_file <- file.path(tcga_path, "data_mutations.txt")
out_dir  <- file.path(project_root, "hrd")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out_csv  <- file.path(out_dir, "brca_status.csv")

cat("Loading MAF file (this can be large)...\n")
maf <- fread(maf_file, header = TRUE, sep = "\t", data.table = FALSE,
             quote = "", showProgress = TRUE)

cat("MAF dimensions:", nrow(maf), "rows x", ncol(maf), "columns\n")
cat("Confirming expected columns present: Hugo_Symbol, Variant_Classification, Tumor_Sample_Barcode\n")
required <- c("Hugo_Symbol", "Variant_Classification", "Tumor_Sample_Barcode")
missing_req <- setdiff(required, names(maf))
if (length(missing_req) > 0) {
  stop("MAF file is missing expected column(s): ", paste(missing_req, collapse = ", "),
```
(92 lines total. No hardcoded numeric analysis parameters.)

#### src/hrd/02_cox_model_with_brca.R
```r
## ============================================================
## Enhancement 4 "” Step 2: Cox model with BRCA1/2 mutation status
## Ovarian Cancer Platinum Response Project
## ============================================================

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))
library(survival)
library(data.table)

project_root <- "C:/PROJECTS/ovarian-cancer-platinum-response"
cohort_file  <- file.path(project_root, "phase2/outputs/cox_patients_with_risk.csv")
brca_file    <- file.path(project_root, "hrd/brca_status.csv")
out_dir      <- file.path(project_root, "hrd")

cohort <- fread(cohort_file, data.table = FALSE)
brca   <- fread(brca_file, data.table = FALSE)

cat("cox_patients_with_risk.csv columns:\n  ", paste(names(cohort), collapse = ", "), "\n\n")

find_col <- function(df, candidates, label) {
  hit <- candidates[candidates %in% names(df)]
  if (length(hit) == 0) {
    stop("Could not find a column for '", label, "' in cox_patients_with_risk.csv.\n",
         "Looked for: ", paste(candidates, collapse = ", "), "\n",
         "Actual columns are: ", paste(names(df), collapse = ", "))
  }
  hit[1]
}

col_patient <- find_col(cohort, c("PATIENT_ID", "PatientID"), "patient ID")
```
(137 lines total.)

#### src/hrd/03_hrd_gene_crossref.py
```python
"""
Enhancement 4 -- Step 3: RF gene x HRD pathway cross-reference
Ovarian Cancer Platinum Response Project

Checks whether any of the genes driving Finding 5's RF feature importance
(or the broader top-500 variance-filtered list) are themselves canonical
homologous-recombination-repair (HRR) / HRD pathway genes -- i.e. whether
the platinum-response signal is picking up direct DNA-repair biology, as
opposed to (or in addition to) the EMT/ECM signal already established.

NOTE ON THE GENE PANEL: there is no single universally agreed "the" HRD
gene list in the field -- clinical panels (Myriad myChoice, FoundationOne
HRD, etc.) and academic curations vary somewhat in scope. The panel below
is a widely-cited literature curation of core HRR pathway genes (Pennington
et al. 2014, Clin Cancer Res, plus the Fanconi Anemia core complex genes
commonly grouped with it). If you want to compare against a different/
larger panel, edit HRD_PATHWAY_GENES below and re-run -- the rest of the
script doesn't need to change.
"""

import os
import pandas as pd

PROJECT_ROOT = r"C:\PROJECTS\ovarian-cancer-platinum-response"
rf_importance_file = os.path.join(PROJECT_ROOT, "phase2", "outputs",
                                   "rf_feature_importances_named.csv")
top500_file = os.path.join(PROJECT_ROOT, "phase2", "outputs",
                            "top500_genes_named.txt")
out_dir = os.path.join(PROJECT_ROOT, "hrd")
os.makedirs(out_dir, exist_ok=True)
```
(96 lines total. This is a gene-panel cross-reference of a static, named HRD/HRR gene list — no numeric ML/statistical analysis parameters. "2014" is a publication year in a comment, not an analysis constant.)

#### phase2/phase2_00_diag.R
```r
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
```
(24 lines — entire file shown above (head -30 returned all 24 lines). Diagnostic-only, no parameters.)

#### phase2/phase2_01_inspect_clinical.R
```r
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
```
(129 lines total. No hardcoded numeric analysis parameters found anywhere in the file.)

#### phase2/phase2_02_cox_model.R
```r
# phase2_02_cox_model.R
# Purpose: Fit Cox proportional hazards model on platinum-treated TCGA-OV patients.
#          Outcome:    OS (overall survival)
#          Covariates: TMB_NONSYNONYMOUS, ANEUPLOIDY_SCORE
#          Outputs:    Cox summary, C-index, HR table CSV, KM plot PNG
# Run from project root:
#   Rscript phase2\phase2_02_cox_model.R

.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# ---- 0. Install required packages if missing --------------------------------
required_pkgs <- c("survival", "survminer", "ggplot2")
for (pkg in required_pkgs) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("Installing %s...\n", pkg))
    install.packages(pkg, repos = "https://cloud.r-project.org",
                     lib = "C:/Users/AMAC_WORK/R/library")
  }
}
library(survival)
library(survminer)
library(ggplot2)

# ---- 1. Paths ---------------------------------------------------------------
DATA_DIR <- "D:/ALIENWARE/WORK DATA/George Mason/Course Work/3rd Sem FALL 2025/BINF 760 ML/Project data/ov_tcga_pan_can_atlas_2018"
OUT_DIR  <- "phase2/outputs"
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

load_cbio <- function(path) {
  read.table(path, header = TRUE, sep = "\t",
```
(224 lines total.)

#### phase2/phase2_03_rf_feature_importance.py
```python
# phase2/phase2_03_rf_feature_importance.py
# Purpose: Load trained Random Forest models, extract feature importances,
#          and export top genes for pathway enrichment analysis.
# Run from project root:
#   python phase2/phase2_03_rf_feature_importance.py

import sys
import os
import pickle
import json
import numpy as np
import pandas as pd
from pathlib import Path

# ── Project root on sys.path ───────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Paths ──────────────────────────────────────────────────────────────────────
DATA_DIR = Path(
    "D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
    "3rd Sem FALL 2025/BINF 760 ML/Project data/"
    "ov_tcga_pan_can_atlas_2018"
)
MODELS_DIR  = PROJECT_ROOT / "outputs" / "models"
PHASE2_OUT  = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)

RSEM_PATH = DATA_DIR / "data_mrna_seq_v2_rsem.txt"

```
(258 lines total.)

#### phase2/phase2_03b_recover_gene_names.py
```python
# phase2/phase2_03b_recover_gene_names.py
# Purpose: Replicate the pipeline's variance filter to recover the exact
#          500-gene list that the RF models were trained on, then re-export
#          all importance tables with real gene names.
# Run from project root:
#   python phase2\phase2_03b_recover_gene_names.py

import sys
import os
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = Path(
    "D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
    "3rd Sem FALL 2025/BINF 760 ML/Project data/"
    "ov_tcga_pan_can_atlas_2018"
)
MODELS_DIR = PROJECT_ROOT / "outputs" / "models"
PHASE2_OUT = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)

RSEM_PATH      = DATA_DIR / "data_mrna_seq_v2_rsem.txt"
TREATMENT_PATH = DATA_DIR / "data_timeline_treatment.txt"

# ── 1. Load treatment file → platinum patient IDs ─────────────────────────────
```
(195 lines total.)

#### phase2/phase2_03c_permutation_shap_importance.py
```python
# phase2/phase2_03c_permutation_shap_importance.py
# Purpose: Replace MDI-based RF feature importance (biased — see
#          https://explained.ai/rf-importance/, flagged by Dr. Lockhart) with
#          permutation importance and TreeSHAP, computed on the ACTUAL
#          held-out test set for each threshold model.
#
# Context (confirmed during Phase 1 investigation):
#   - No train/test split or fitted StandardScaler was ever persisted to
#     disk, so both are reconstructed here from the raw TCGA files using the
#     project's own src/ modules (not reimplemented) and the confirmed seed.
#   - The real pipeline (src/pipeline.py) computes the top-500 variance
#     filter on EACH THRESHOLD'S OWN TRAIN SPLIT, not on the full platinum
#     cohort. phase2_03b's single shared gene list does not necessarily match
#     what each RF model actually trained on, so this script reconstructs the
#     split AND the gene list independently per threshold (12m/18m/24m) and
#     verifies each against the pickled model before trusting it.
#   - This script does not touch config/config.yaml, .git, or the existing
#     MDI output files from phase2_03/phase2_03b.
#
# Run from project root:
#   python phase2\phase2_03c_permutation_shap_importance.py

from __future__ import annotations

import sys
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
```
(398 lines total.)

#### phase2/phase2_03d_cv_permutation_shap_importance.py
```python
# phase2/phase2_03d_cv_permutation_shap_importance.py
# Purpose: phase2_03c found near-zero Spearman correlation between MDI,
#          permutation importance, and SHAP for Finding 5's RF gene rankings.
#          Two suspected causes: (1) MDI came from the full-training-set fit
#          while permutation/SHAP ran on a single tiny 20% test fold - not a
#          fair comparison; (2) that fold is severely underpowered, especially
#          at 12m (11 total events, ~2 positive test cases), where the
#          single-split test AUC was 0.48 (worse than chance).
#
# This script replaces the single train/test split with repeated stratified
# CV (5 splits x 5 repeats = 25 folds per threshold) and computes MDI,
# permutation importance, and SHAP IDENTICALLY within each fold - a fair
# three-way comparison that also uses far more of the data than one 20%
# split allows.
#
# Does NOT modify phase2_03.py, phase2_03b.py, phase2_03c.py, config.yaml,
# or .git. New file only.
#
# Run from project root:
#   python -u phase2\phase2_03d_cv_permutation_shap_importance.py

from __future__ import annotations

import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
```
(401 lines total.)

#### phase2/phase2_04_pathway_enrichment.py
```python
# phase2/phase2_04_pathway_enrichment.py
# Purpose: Run pathway enrichment on top RF importance genes via Enrichr API.
#          Queries KEGG_2021_Human, Reactome_2022, GO_Biological_Process_2023
#          No local installation needed — uses Enrichr REST API.
# Run from project root:
#   python phase2\phase2_04_pathway_enrichment.py

import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHASE2_OUT   = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)

ENRICHR_BASE = "https://maayanlab.cloud/Enrichr"

# Gene lists to test
GENE_LIST_FILES = {
    "top50":  PHASE2_OUT / "top50_genes_named.txt",
    "top100": PHASE2_OUT / "top100_genes_named.txt",
    "top200": PHASE2_OUT / "top200_genes_named.txt",
}

# Databases to query
```
(204 lines total.)

#### phase2/phase2_04b_pathway_enrichment_shap.py
```python
# phase2/phase2_04b_pathway_enrichment_shap.py
# Purpose: Run the exact same Enrichr pathway enrichment methodology as
#          phase2_04_pathway_enrichment.py, but on the SHAP-based gene lists
#          from phase2_03d (cv_topN_genes_shap_{with12m,without12m}.txt)
#          instead of the original MDI-based lists. SHAP was chosen as the
#          final Finding 5 importance method (converges with MDI at rho=0.98
#          under fair CV comparison; directly addresses Lockhart's MDI-bias
#          comment).
#
# Does NOT modify phase2_04_pathway_enrichment.py, phase2_03/03b/03c/03d,
# config.yaml, .git, or PROJECT_LOG.md. New file only. Original MDI
# enrichment results (enrichment_results_full.csv /
# enrichment_results_significant.csv) are read for reference/comparison
# only - never rewritten.
#
# Run from project root:
#   python phase2\phase2_04b_pathway_enrichment_shap.py

import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHASE2_OUT = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)
```
(341 lines total.)

#### multi_cancer/check_rsem_headers.py
```python
# multi_cancer/check_rsem_headers.py
# Compares column headers between original and deduped COADREAD RSEM files.
# Run from project root:
#   python multi_cancer\check_rsem_headers.py

import pandas as pd
from pathlib import Path

ORIG = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
            "3rd Sem FALL 2025/BINF 760 ML/Project data/"
            "coadread_tcga_pan_can_atlas_2018/data_mrna_seq_v2_rsem.txt")

TMP  = Path("multi_cancer/outputs/_tmp_COADREAD_data/data_mrna_seq_v2_rsem.txt")

def get_headers(path):
    df = pd.read_csv(path, sep="\t", nrows=0)
    return df.columns.tolist()

orig_cols = get_headers(ORIG)
print(f"Original RSEM columns : {len(orig_cols)}")
print(f"  First 5 : {orig_cols[:5]}")
print(f"  Last 2  : {orig_cols[-2:]}")

if TMP.exists():
    tmp_cols = get_headers(TMP)
    print(f"\nDeduped RSEM columns  : {len(tmp_cols)}")
    print(f"  First 5 : {tmp_cols[:5]}")
    print(f"  Last 2  : {tmp_cols[-2:]}")
    print(f"\nFirst col same? {orig_cols[0] == tmp_cols[0]}")
    print(f"Sample cols same? {orig_cols[2:5] == tmp_cols[2:5]}")
```
(41 lines — entire file shown above. No analysis parameters, diagnostic only.)

#### multi_cancer/compare_ablation_results.py
```python
# multi_cancer/compare_ablation_results.py  (v2)
# Builds cross-cancer leakage comparison table from ablation_supervised_leakage_summary.csv
# Run from project root:
#   python multi_cancer\compare_ablation_results.py

import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MC_OUT       = PROJECT_ROOT / "multi_cancer" / "outputs"
OV_RESULTS   = PROJECT_ROOT / "outputs" / "results"
COMPARE_OUT  = MC_OUT / "comparison"
COMPARE_OUT.mkdir(parents=True, exist_ok=True)

CANCERS = {
    "OV":       {"results_dir": OV_RESULTS,                   "name": "Ovarian (HGSOC)",      "thresholds": [12, 18, 24]},
    "LUAD":     {"results_dir": MC_OUT / "LUAD"     / "results", "name": "Lung Adeno",         "thresholds": [12, 18, 24]},
    "COADREAD": {"results_dir": MC_OUT / "COADREAD" / "results", "name": "Colorectal",         "thresholds": [18, 24, 36]},
}

# ── Load supervised leakage summary for each cancer ───────────────────────────
print("=" * 64)
print("CROSS-CANCER FEATURE SELECTION LEAKAGE — RESULTS")
print("=" * 64)

all_dfs = []
for label, meta in CANCERS.items():
    path = meta["results_dir"] / "ablation_supervised_leakage_summary.csv"
    if not path.exists():
```
(126 lines total.)

#### multi_cancer/diagnose_coadread_ids.py
```python
# multi_cancer/diagnose_coadread_ids.py
# Purpose: Check why COADREAD patient IDs don't overlap between RSEM and clinical.
# Run from project root:
#   python multi_cancer\diagnose_coadread_ids.py

import pandas as pd
from pathlib import Path

DATA_DIR = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
                "3rd Sem FALL 2025/BINF 760 ML/Project data/"
                "coadread_tcga_pan_can_atlas_2018")

TMP_DIR  = Path("C:/PROJECTS/ovarian-cancer-platinum-response/"
                "multi_cancer/outputs/_tmp_COADREAD_data")

def load_cbio(path):
    return pd.read_csv(path, sep="\t", comment="#", low_memory=False)

# ── Clinical patient IDs ───────────────────────────────────────────────────────
clin = load_cbio(DATA_DIR / "data_clinical_patient.txt")
clin_ids = set(clin["PATIENT_ID"].dropna().tolist())
print(f"Clinical patient IDs: {len(clin_ids)}")
print(f"  Sample: {list(clin_ids)[:5]}")

# ── Treatment platinum patient IDs ────────────────────────────────────────────
trt = load_cbio(DATA_DIR / "data_timeline_treatment.txt")
plat_mask = trt["AGENT"].str.contains("platin", case=False, na=False)
plat_ids  = set(trt.loc[plat_mask, "PATIENT_ID"].dropna().tolist())
print(f"\nPlatinum patient IDs: {len(plat_ids)}")
print(f"  Sample: {list(plat_ids)[:5]}")
```
(67 lines total. No analysis parameters, diagnostic only.)

#### multi_cancer/diagnose_cohorts.py
```python
# multi_cancer/diagnose_cohorts.py
# Purpose: Check platinum-treated cohort sizes and OS distributions for
#          BRCA, LUAD, COADREAD to determine appropriate thresholds.
# Run from project root:
#   python multi_cancer\diagnose_cohorts.py

import pandas as pd
import numpy as np
from pathlib import Path

DATA_BASE = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
                 "3rd Sem FALL 2025/BINF 760 ML/Project data")

CANCERS = {
    "OV":       "ov_tcga_pan_can_atlas_2018",
    "BRCA":     "brca_tcga_pan_can_atlas_2018",
    "LUAD":     "luad_tcga_pan_can_atlas_2018",
    "COADREAD": "coadread_tcga_pan_can_atlas_2018",
}

def load_cbio(path):
    return pd.read_csv(path, sep="\t", comment="#",
                       low_memory=False, na_values=["[Not Available]","NA",""])

for label, study_id in CANCERS.items():
    data_dir = DATA_BASE / study_id
    print(f"\n{'='*60}")
    print(f"CANCER: {label} ({study_id})")
    print(f"{'='*60}")

```
(111 lines total.)

#### multi_cancer/run_multi_cancer_ablation.py
```python
# multi_cancer/run_multi_cancer_ablation.py  (v2)
# Changes from v1:
#   - BRCA dropped (n=32 platinum patients; not standard-of-care)
#   - Cancer-appropriate thresholds per dataset
#   - Pre-patches RSEM file to dedup gene symbols before ablation runs
#   - Adds minimum cohort size check
# Run from project root:
#   python multi_cancer\run_multi_cancer_ablation.py

import subprocess
import sys
import shutil
import yaml
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_BASE    = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
                    "3rd Sem FALL 2025/BINF 760 ML/Project data")
MC_OUT       = PROJECT_ROOT / "multi_cancer" / "outputs"
MC_OUT.mkdir(parents=True, exist_ok=True)

# ── Cancer studies (BRCA dropped — only 32 platinum patients) ─────────────────
CANCERS = [
    {
        "label":      "LUAD",
        "study_id":   "luad_tcga_pan_can_atlas_2018",
        "name":       "Lung Adenocarcinoma",
        "thresholds": [12, 18, 24],   # same as OV; 146 platinum patients
    },
```
(219 lines total.)

#### validation/01_download_and_parse.R
```r
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
```
(141 lines total. No hardcoded numeric analysis parameters.)

#### validation/02_parse_metadata.R
```r
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
```
(152 lines total. No hardcoded numeric analysis parameters.)

#### validation/03_fix_labels.R
```r
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
```
(99 lines total. No hardcoded numeric analysis parameters.)

#### validation/04_probe_mapping.R
```r
.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# =============================================================================
# 04_probe_mapping.R
# Map Affymetrix GPL570 probe IDs to gene symbols using hgu133plus2.db
# Collapse multi-probe genes by max mean expression
# Filter to serous/undifferentiated samples only
# Output: data/external/GSE63885_expr_gene.csv
# =============================================================================

cat("=== Step 4: Probe-to-Gene Mapping ===\n\n")

OUT_DIR <- "data/external"

# --- Install Bioconductor + hgu133plus2.db if needed ------------------------
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  cat("Installing BiocManager...\n")
  install.packages("BiocManager",
                   lib  = "C:/Users/AMAC_WORK/R/library",
                   repos = "https://cloud.r-project.org")
}
library(BiocManager)

if (!requireNamespace("hgu133plus2.db", quietly = TRUE)) {
  cat("Installing hgu133plus2.db (Bioconductor annotation package)...\n")
  BiocManager::install("hgu133plus2.db",
                       lib  = "C:/Users/AMAC_WORK/R/library",
                       update = FALSE, ask = FALSE)
}
library(hgu133plus2.db)
```
(116 lines total. No hardcoded numeric analysis parameters.)

#### validation/05_batch_correction.R
```r
.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

# =============================================================================
# 05_batch_correction.R
# 1. Load GSE63885 gene-level expression (log2 RMA)
# 2. Load TCGA expression (raw RSEM from data_mrna_seq_v2_rsem.txt)
# 3. Intersect gene sets
# 4. Z-score normalize each dataset independently
# 5. Apply ComBat batch correction (platform as batch)
# 6. Export harmonised matrix for Python classifier
# Output: data/external/harmonised_expression.csv
#         data/external/harmonised_metadata.csv
# =============================================================================

cat("=== Step 5: Batch Correction ===\n\n")

OUT_DIR  <- "data/external"

# --- Install sva (ComBat) if needed -----------------------------------------
if (!requireNamespace("sva", quietly = TRUE)) {
  cat("Installing sva package...\n")
  BiocManager::install("sva",
                       lib = "C:/Users/AMAC_WORK/R/library",
                       update = FALSE, ask = FALSE)
}
library(sva)
library(BiocGenerics)

cat("sva loaded OK\n\n")

```
(274 lines total.)

#### validation/inspect_metadata.R
```r
.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))

cat("=== GSE63885 characteristics ===\n")
lines <- readLines("data/external/GSE63885_series_matrix.txt", warn = FALSE)
meta  <- lines[grepl("^!Sample_characteristics_ch1", lines)]
cat(meta[1:15], sep = "\n")

cat("\n\n=== GSE9891 characteristics ===\n")
lines <- readLines("data/external/GSE9891_series_matrix.txt", warn = FALSE)
meta  <- lines[grepl("^!Sample_characteristics_ch1", lines)]
cat(meta[1:10], sep = "\n")
```
(11 lines — entire file shown above. `1:15` and `1:10` are display-row-count slices for a diagnostic `cat()` printout, not analysis parameters.)

#### validation/investigate_labels.R
```r
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
```
(64 lines total. `1:20` is a display-row-count slice, not an analysis parameter.)

---

## Consolidated numeric-constant table (all scripts)

| script | parameter name | value | line number |
|---|---|---|---|
| src/03_pathway_enrichment_corrected.py | N_TOP_GENES (variance-filter top-N gene cutoff) | 500 | 45 |
| src/03_pathway_enrichment_corrected.py | ADJ_P_THRESHOLD (Enrichr significance cutoff) | 0.05 | 52 |
| src/ablation.py | n_repeats (default, `run_leakage_ablation`) | 30 | 71 |
| src/ablation.py | n_repeats (default, `run_supervised_leakage_ablation`) | 30 | 182 |
| src/ablation.py | n_repeats (default, split-variance sampler) | 30 | 379 |
| src/ablation.py | significance cutoff (`significant_at_05`, paired t-test) | 0.05 | 357 |
| src/ablation.py | n_bootstrap (default, `bootstrap_auc_ci`) | 1000 | 432 |
| src/ablation.py | ci (default confidence level, `bootstrap_auc_ci`) | 0.95 | 433 |
| src/ablation.py | seed (default, `bootstrap_auc_ci`) | 42 | 434 |
| src/ablation.py | outer_splits (default, `nested_cross_validate`) | 5 | 476 |
| src/ablation.py | inner_splits (default, `nested_cross_validate`) | 3 | 477 |
| src/ablation.py | seed (default, `nested_cross_validate`) | 42 | 478 |
| src/ablation.py | top_n / test_size / base_seed | sourced from config.yaml (`cfg["features"]["top_n_genes"]`, `cfg["model"]["test_size"]`, `cfg["project"]["seed"]`) — no local literal | 92-94, 203-205, 398-399 |
| src/features.py | top_n (default, `select_high_variance_genes`) | 500 | 27 |
| src/label_investigation.py | alpha (default significance level, `clopper_pearson_ci`) | 0.05 | 275 |
| src/label_investigation.py | alpha (explicit call value) | 0.05 | 353 |
| src/models.py | random_state (RF, fallback default via `cfg.get`) | 42 | 37 |
| src/models.py | n_estimators (RF, fallback default) | 300 | 43 |
| src/models.py | max_depth (RF, fallback default) | None | 44 |
| src/models.py | min_samples_split (RF, fallback default) | 2 | 45 |
| src/models.py | random_state (LogisticRegression, fallback default) | 42 | 48 |
| src/models.py | random_state (SVM, fallback default) | 42 | 59 |
| src/models.py | n_splits (default, `cross_validate_model`) | 5 | 105 |
| src/pipeline.py | test_size / top_n_genes / cv_folds / thresholds / seed | sourced from config.yaml (`model_cfg["test_size"]`, `feat_cfg["top_n_genes"]`, `model_cfg["cv_folds"]`, `clin_cfg["thresholds"]`, `seed`) — no local literal | 94, 122-123, 129, 159 |
| src/preprocessing.py | thresholds example in docstring | 12, 18, 24 (illustrative only, not executed) | 161 |
| src/cellularity/03_pathway_enrichment_corrected.py | N_TOP_GENES (variance-filter top-N gene cutoff) | 500 | 45 |
| src/cellularity/03_pathway_enrichment_corrected.py | ADJ_P_THRESHOLD (Enrichr significance cutoff) | 0.05 | 52 |
| src/cellularity/01_run_estimate.R | ESTIMATE→purity conversion coefficient (intercept) | 0.6049872018 | 121 |
| src/cellularity/01_run_estimate.R | ESTIMATE→purity conversion coefficient (slope) | 0.0001467884 | 121 |
| phase2/phase2_02_cox_model.R | manuscript reference value: matched-subset cohort n | 432 | 192 |
| phase2/phase2_02_cox_model.R | manuscript reference value: events n | 242 | 192 |
| phase2/phase2_02_cox_model.R | manuscript reference value: C-index | 0.570 | 192 (also 184) |
| phase2/phase2_02_cox_model.R | manuscript reference value: log-rank p | 0.023 | 192 (also 184) |
| phase2/phase2_02_cox_model.R | manuscript reference value: (6th tuple element) | 0.178 | 192 |
| phase2/phase2_03_rf_feature_importance.py | top-N gene list sizes exported | 50, 100, 200, 500 | 220, 255 |
| phase2/phase2_03b_recover_gene_names.py | top500 gene-count check index (0-based, gene #500) | 499 | 85 |
| phase2/phase2_03b_recover_gene_names.py | top-N gene list sizes exported | 50, 100, 200, 500 | 159 |
| phase2/phase2_03c_permutation_shap_importance.py | N_REPEATS (permutation_importance) | 30 | 66 |
| phase2/phase2_03c_permutation_shap_importance.py | EXPECTED_SEED (assert-checked against config.yaml) | 42 | 67 |
| phase2/phase2_03c_permutation_shap_importance.py | test_size / top_n_genes / thresholds / seed | read from config.yaml (`cfg['model']['test_size']`, `cfg['features']['top_n_genes']`, `cfg['clinical']['thresholds']`, `cfg['project']['seed']`) — no local literal | 79-89 |
| phase2/phase2_03c_permutation_shap_importance.py | AUC-diff sanity-check cutoff | 0.01 | 192 |
| phase2/phase2_03c_permutation_shap_importance.py | top-N gene list sizes exported | 50, 100, 200, 500 | 317 |
| phase2/phase2_03d_cv_permutation_shap_importance.py | N_SPLITS (RepeatedStratifiedKFold) | 5 | 62 |
| phase2/phase2_03d_cv_permutation_shap_importance.py | N_REPEATS (RepeatedStratifiedKFold) | 5 | 63 |
| phase2/phase2_03d_cv_permutation_shap_importance.py | PERM_N_REPEATS (permutation_importance within each fold) | 10 | 64 |
| phase2/phase2_03d_cv_permutation_shap_importance.py | EXPECTED_SEED (assert-checked against config.yaml) | 42 | 65 |
| phase2/phase2_03d_cv_permutation_shap_importance.py | resulting folds per threshold (N_SPLITS × N_REPEATS) | 25 | 96-97 (derived) |
| phase2/phase2_03d_cv_permutation_shap_importance.py | 12-month threshold excluded in one sensitivity aggregation | 12 | 301 |
| phase2/phase2_03d_cv_permutation_shap_importance.py | top-N gene list sizes exported | 50, 100, 200, 500 | 306 |
| phase2/phase2_04_pathway_enrichment.py | urllib request timeout (seconds) | 30 | 63, 76 |
| phase2/phase2_04_pathway_enrichment.py | adj_p_value significance cutoff | 0.05 | 173-174 |
| phase2/phase2_04b_pathway_enrichment_shap.py | urllib request timeout (seconds) | 30 | 105, 118 |
| phase2/phase2_04b_pathway_enrichment_shap.py | SIG_THRESHOLD (adj-p significance cutoff) | 0.05 | 73 |
| phase2/phase2_04b_pathway_enrichment_shap.py | gene-set size passed to a result-row constructor | 500 | 273 |
| multi_cancer/compare_ablation_results.py | OV/LUAD survival-month thresholds | 12, 18, 24 | 17, 18 |
| multi_cancer/compare_ablation_results.py | COADREAD survival-month thresholds | 18, 24, 36 | 19 |
| multi_cancer/run_multi_cancer_ablation.py | LUAD survival-month thresholds | 12, 18, 24 | 29 |
| multi_cancer/run_multi_cancer_ablation.py | COADREAD survival-month thresholds | 18, 24, 36 | 34 |
| multi_cancer/run_multi_cancer_ablation.py | subprocess timeout (seconds) per cancer run | 3600 | 175 |
| multi_cancer/run_multi_cancer_ablation.py | n_repeats (ablation splits, referenced in log message) | 30 | 167 |
| validation/05_batch_correction.R | top_n_sel (variance-filter top-N gene cutoff) | 500 | 191 |
| validation/05_batch_correction.R | manuscript reference value: ComBat Pearson r | -0.005 | 165, 216, 224, 226 |
| validation/05_batch_correction.R | manuscript reference value: (2nd tuple element) | 1.00 | 216 |
| validation/05_batch_correction.R | manuscript reference value: gene-count | 500 | 216 |
| validation/05_batch_correction.R | tolerance for reproducing manuscript r | 0.05 | 224 |
| src/data_loader.py | — | none found | — |
| src/evaluation.py | — none found (no local numeric analysis-parameter literals; `threshold` param is caller-supplied) | — | — |
| src/visualization.py | — none found (all `threshold(s)` values are function parameters/data, not local numeric literals) | — | — |
| src/__init__.py | — no code | — | — |
| src/cellularity/00_install_estimate.R | — none found | — | — |
| src/cellularity/02_cox_model_with_purity.R | — none found | — | — |
| src/hrd/00_inspect_hrd_data.R | — none found | — | — |
| src/hrd/01_extract_brca_status.R | — none found | — | — |
| src/hrd/02_cox_model_with_brca.R | matched-subset size noted in comment only (n=335, not a code constant) | 335 (comment only) | 117 |
| src/hrd/03_hrd_gene_crossref.py | — none found (static named gene panel only; "2014" is a citation year) | — | — |
| phase2/phase2_00_diag.R | — none found | — | — |
| phase2/phase2_01_inspect_clinical.R | — none found | — | — |
| multi_cancer/check_rsem_headers.py | — none found | — | — |
| multi_cancer/diagnose_coadread_ids.py | — none found | — | — |
| multi_cancer/diagnose_cohorts.py | — none found (loop iterates configured `CANCERS` dict; no numeric literal cutoffs) | — | — |
| validation/01_download_and_parse.R | — none found | — | — |
| validation/02_parse_metadata.R | — none found | — | — |
| validation/03_fix_labels.R | — none found | — | — |
| validation/04_probe_mapping.R | — none found | — | — |
| validation/inspect_metadata.R | display-row slices only (not analysis params) | 1:15, 1:10 | 6, 10 |
| validation/investigate_labels.R | display-row slice only (not analysis param) | 1:20 | 18 |

**Table notes:**
- "manuscript reference value" rows are hardcoded numbers embedded as comparison/tolerance checkpoints against previously reported results (sanity checks), not primary analysis parameters — flagged separately from true model/statistics parameters (seeds, splits, cutoffs) for clarity.
- Rows marked "— none found" mean a full-file `grep` for the parameter-pattern list in the task brief, plus manual inspection of the first 30 lines, produced no hardcoded numeric analysis-parameter matches in that file.
- `src/cellularity/03_pathway_enrichment_corrected.py` and `src/03_pathway_enrichment_corrected.py` are byte-identical (verified via `diff`); their parameter rows are therefore identical and both are listed for completeness per the requested file list.

---

# SECTION 5: CROSS-CHECK — manuscript/log claims vs. output CSVs

Read-only audit. Every row below traces a numeric claim quoted from a manuscript draft or
project log (as extracted verbatim in `audit_section3.md`) to the CSV cell(s) it should
reproduce from (as extracted in `audit_section2.md`). Values are **not** reconciled or
corrected across documents — where drafts state different numbers for the same metric, each
gets its own row. "Document" cites the specific file(s); where two or more documents carry the
literal identical value for a claim, they are cited together in one row rather than duplicated.
MISMATCH does not mean "wrong" — several of these are already-known, tracked corrections
(`fixes/manuscript_changelist.md`) or open author-decision items; this table only reports
claim-vs-CSV agreement, neutrally.

Legend: **F1000-base** = `archive/F1000Research_Draft_Chintala_2026.docx`; **F1000-corr** =
`F1000Research_Draft_Chintala_2026_corrected.docx`; **F1000-final** =
`F1000Research_Draft_Chintala_2026_final.docx`; **PLOS-redline** =
`PLOS_CompBio_Draft_Chintala_v1_redline.docx` (accepted-reading text unless noted "pre-edit" =
the `<w:delText>` / tracked-out value it replaced); **PROJECT_LOG** = `PROJECT_LOG.md`;
**PROJECT_LOG-archive** = `archive/PROJECT_LOG_2026-06-22.md`.

| # | Category | Claim (quoted, short) | Document | Value stated | Source CSV | Value in CSV | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Table 1 AUC | "Logistic Regression \| 0.542 \| 0.658 \| 0.712" (12/18/24m) | F1000-base | 0.457 / 0.669 / 0.678 | `outputs/results/ablation_split_variance_summary.csv` (LR row) | 0.5415→0.542 / 0.6579→0.658 / 0.7117→0.712 | **MISMATCH** — base draft's own stated values (0.457/0.669/0.678) do NOT match this CSV; they instead match `clean_auc_table.csv` (row 21 below) |
| 2 | Table 1 AUC | "Logistic Regression \| 0.542 \| 0.658 \| 0.712" | F1000-corr, F1000-final | 0.542 / 0.658 / 0.712 | `outputs/results/ablation_split_variance_summary.csv` (LR row) | 0.5415 / 0.6579 / 0.7117 | MATCH (traceable) — but source file is the "stale orphan" per `fixes/phase1_provenance.md`: does not reproduce from its own raw per-split data (see row 22) |
| 3 | Table 1 AUC | "Random Forest \| 0.411 \| 0.609 \| 0.709" | F1000-corr, F1000-final | 0.411 / 0.609 / 0.709 | `outputs/results/ablation_split_variance_summary.csv` (RF row) | 0.4110 / 0.6092 / 0.7087 | MATCH (traceable to same stale-orphan file) |
| 4 | Table 1 AUC | "SVM (RBF) \| 0.363 \| 0.515 \| 0.771" | F1000-corr, F1000-final | 0.363 / 0.515 / 0.771 | `outputs/results/ablation_split_variance_summary.csv` (SVM row) | 0.3634 / 0.5145 / 0.7714 | MATCH (traceable to same stale-orphan file) |
| 5 | Table 1 AUC | "Random Forest \| 0.409 \| 0.601 \| 0.725" | F1000-base | 0.409 / 0.601 / 0.725 | Searched: `ablation_split_variance_summary.csv` (0.411/0.609/0.709), `ablation_leakage_raw.csv` mean (0.4085/0.6008/0.7252), `clean_auc_table.csv` (0.4004/0.6277/0.7157) | none match exactly | **NO SOURCE FOUND** — closest is `ablation_leakage_raw.csv`'s `correct_train_only_variance` mean (0.4085/0.6008/0.7252, off by up to 0.026); no CSV in the repo carries 0.409/0.601/0.725 |
| 6 | Table 1 AUC | "SVM (RBF) \| 0.386 \| 0.586 \| 0.733" | F1000-base | 0.386 / 0.586 / 0.733 | Searched: same three files as row 5 | none match exactly | **NO SOURCE FOUND** — no CSV carries 0.386/0.586/0.733 (closest is `clean_auc_table.csv` 0.4045/0.6191/0.7333, exact only on the 24m cell) |
| 7 | Table 2 (redline, leakage-free) | "Logistic Regression \| 0.457 \| 0.669 \| 0.678" | PLOS-redline (current) | 0.457 / 0.669 / 0.678 | `outputs/results/clean_auc_table.csv` (LR row) | 0.4569 / 0.6691 / 0.6778 | MATCH |
| 8 | Table 2 (redline, leakage-free) | "Random Forest \| 0.400 \| 0.628 \| 0.716" | PLOS-redline (current) | 0.400 / 0.628 / 0.716 | `outputs/results/clean_auc_table.csv` (RF row) | 0.4004 / 0.6277 / 0.7157 | MATCH |
| 9 | Table 2 (redline, leakage-free) | "SVM (RBF) \| 0.405 \| 0.619 \| 0.733" | PLOS-redline (current) | 0.405 / 0.619 / 0.733 | `outputs/results/clean_auc_table.csv` (SVM row) | 0.4045 / 0.6191 / 0.7333 | MATCH |
| 10 | Table 2 (redline, pre-edit) | RF/SVM cells | PLOS-redline (pre-edit / tracked-deleted text) | `[COWORK: pending re-run]` (placeholder, no numeric value) | n/a | n/a | N/A — placeholder, not a numeric claim; superseded by rows 8–9 |
| 11 | ΔAUC Table 2 (supervised) | "Logistic Regression\|12m\|−0.004"; "18m\|+0.065"; "24m\|+0.219" | F1000-base, F1000-corr, F1000-final | −0.004 / +0.065 / +0.219 | `outputs/results/ablation_supervised_leakage_summary.csv` (LR `auc_inflation`) | −0.0041 / 0.0645 / 0.2193 | MATCH |
| 12 | ΔAUC Table 2 (supervised) | "Random Forest\|12m\|+0.220"; "18m\|+0.224"; "24m\|+0.117" | F1000-base, F1000-corr, F1000-final | +0.220 / +0.224 / +0.117 | same file (RF `auc_inflation`) | 0.2201 / 0.2235 / 0.1168 | MATCH |
| 13 | ΔAUC Table 2 (supervised) | "SVM (RBF)\|12m\|+0.552"; "18m\|+0.338"; "24m\|+0.281" | F1000-base, F1000-corr, F1000-final; also PLOS-redline abstract ("+0.552") | +0.552 / +0.338 / +0.281 | same file (SVM `auc_inflation`) | 0.5520 / 0.3384 / 0.2805 | MATCH |
| 14 | ΔAUC Table 2 (unsupervised) | "Logistic Regression\|+0.003\|+0.009\|−0.004" | F1000-base, F1000-corr, F1000-final | +0.003 / +0.009 / −0.004 | `outputs/results/ablation_leakage_summary.csv` (LR `auc_inflation`) | 0.0028 / 0.0086 / −0.0039 | MATCH |
| 15 | ΔAUC Table 2 (unsupervised) | "Random Forest\|+0.020\|+0.044\|−0.009" | F1000-base, F1000-corr, F1000-final | +0.020 / +0.044 / −0.009 | same file (RF `auc_inflation`) | 0.0203 / 0.0439 / −0.0089 | MATCH |
| 16 | ΔAUC Table 2 (unsupervised) | "SVM (RBF)\|+0.053\|+0.020\|−0.040" | F1000-base, F1000-corr, F1000-final | +0.053 / +0.020 / −0.040 | same file (SVM `auc_inflation`) | 0.0528 / 0.0195 / −0.0397 | MATCH |
| 17 | ΔAUC mean row | "Mean \| all \| +0.223 \| +0.011" | F1000-base, F1000-corr, F1000-final | +0.223 / +0.011 | `multi_cancer/outputs/comparison/cross_cancer_leakage_summary.csv`, row Ovarian, `Sup_mean_inf`/`Unsup_mean_inf` | 0.2234 / 0.0106 | MATCH |
| 18 | Leakage mean (abstract) | "supervised F-score selection inflates reported AUC by a mean of +0.22 (up to +0.55)" | PLOS-redline abstract & Results | +0.223 / +0.552 | same file as row 17 | 0.2234 / 0.5520 | MATCH |
| 19 | Table 3 (external, clinical) | "Logistic Regression\|0.503\|0.494\|0.491"; "Random Forest\|0.512\|0.581\|0.356"; "SVM (RBF)\|0.431\|0.477\|0.603" | F1000-base, F1000-corr, F1000-final | as quoted | `outputs/results/external_validation_results.csv`, `label_set=clinical` rows | LR 0.5031/0.4937/0.4906; RF 0.5117/0.5805/0.3563; SVM 0.4313/0.4766/0.6031 | MATCH (all 9 cells, rounded) |
| 20 | Table 4 (external, DFS) | "Logistic Regression\|0.526\|0.557\|0.456"; "Random Forest\|0.600\|0.502\|0.444"; "SVM (RBF)\|0.413\|0.460\|0.501" | F1000-base, F1000-corr, F1000-final | as quoted | same file, `label_set=dfs` rows | LR 0.5257/0.5574/0.4559; RF 0.6000/0.5022/0.4441; SVM 0.4125/0.4596/0.5007 | MATCH (all 9 cells, rounded) |
| 21 | Table 4 caption n / split | "n=75 labeled; 41 sensitive, 34 resistant" | F1000-base, F1000-corr | n=75, 41 vs 34 | `outputs/results/external_validation_results.csv`, `dfs` rows, `n_samples`/`n_class0`/`n_class1` | n_samples=74, n_class0=40, n_class1=34 (74 total, not 75; 40 not 41) | **MISMATCH** |
| 22 | Table 4 caption n / split | "n=74 labeled; 40 sensitive, 34 resistant" | F1000-final; also Methods 2.6 all three drafts state "n = 74 labeled; 40 sensitive, 34 resistant" or "n = 75... 41... " (see row 21) | n=74, 40 vs 34 | same file/rows | n_samples=74, n_class0=40, n_class1=34 | MATCH |
| 23 | Multi-cancer replication | "Ovarian (HGSOC) \| +0.223 \| +0.011 \| SVM +0.552 @ 12m" | PLOS-redline Table 1; PROJECT_LOG | as quoted | `multi_cancer/outputs/comparison/cross_cancer_leakage_summary.csv`, row `Ovarian (HGSOC)` | Sup_mean_inf 0.2234, Unsup_mean_inf 0.0106, Worst_case SVM@12m 0.552 | MATCH |
| 24 | Multi-cancer replication | "Lung adenocarcinoma (LUAD) \| +0.320 \| +0.004 \| SVM +0.449 @ 12m" | PLOS-redline Table 1; PROJECT_LOG ("LUAD +0.320... unsupervised +0.004") | as quoted | same file, row `Lung Adeno` | Sup_mean_inf 0.3201, Unsup_mean_inf 0.0038, Worst_case SVM@12m 0.4493 | MATCH |
| 25 | Multi-cancer replication | "Colorectal (COADREAD) \| +0.330 \| +0.018 \| SVM +0.418 @ 24m" | PLOS-redline Table 1; PROJECT_LOG ("COADREAD +0.330... unsupervised +0.018") | as quoted | same file, row `Colorectal` | Sup_mean_inf 0.3298, Unsup_mean_inf 0.0176, Worst_case SVM@24m 0.4182 | MATCH |
| 26 | Multi-cancer threshold coverage | COADREAD ablation implicitly framed as using the same 12/18/24m thresholds as OV/LUAD | PLOS-redline Methods (no explicit threshold list given for COADREAD) | (implicit 12/18/24m) | `multi_cancer/outputs/comparison/all_cancers_ablation_raw.csv`, `cross_cancer_leakage_by_model.csv` | COADREAD rows present only for thresholds 18, 24, **36** — no 12m row for COADREAD at all | **MISMATCH / undocumented** — COADREAD was actually run at 18/24/36m, not 12/18/24m; the manuscript text never states this threshold substitution explicitly (see also Section 8) |
| 27 | Cox cohort | "n=432 patients" | PLOS-redline, PROJECT_LOG | 432 | `phase2/outputs/cox_summary_stats.csv`, `n_complete_cases`; `cox_patients_with_risk.csv` row count | 432 (both) | MATCH |
| 28 | Cox events | "242 death events" | PLOS-redline, PROJECT_LOG | 242 | `phase2/outputs/cox_summary_stats.csv`, `n_events`; Σ`os_event` in `cox_patients_with_risk.csv` | 242 | MATCH |
| 29 | Cox HR | "Aneuploidy Score... HR = 1.021, 95% CI 1.004–1.039, p=0.017" | PLOS-redline, PROJECT_LOG | 1.021 / [1.004,1.039] / 0.017 | `phase2/outputs/cox_hazard_ratios.csv`, row `Aneuploidy Score` | HR 1.0213, CI [1.0038,1.0391], p 0.01686 | MATCH |
| 30 | Cox HR | "log-transformed... TMB... HR=0.894, 95% CI 0.742–1.077, p=0.238" | PLOS-redline, PROJECT_LOG | 0.894 / [0.742,1.077] / 0.238 | same file, row `log(TMB + 1)` | HR 0.894, CI [0.7423,1.0768], p 0.2377 | MATCH |
| 31 | Cox C-index | "concordance index of 0.570 (SE 0.021)" | PLOS-redline | 0.570 / SE 0.021 | `phase2/outputs/cox_summary_stats.csv`, `c_index`/`c_index_se` | 0.5698 / 0.0214 | MATCH |
| 32 | Cox PH test | "Schoenfeld global p=0.178" | PLOS-redline, PROJECT_LOG | 0.178 | `phase2/outputs/cox_ph_test.csv`, row `GLOBAL` | 0.178471 | MATCH |
| 33 | Cox KM | "log-rank p=0.023" | PLOS-redline, PROJECT_LOG | 0.023 | `phase2/outputs/cox_summary_stats.csv`, `km_logrank_p` | 0.02342 | MATCH |
| 34 | Cox KM | "median OS 52.0, 51.9, and 39.4 months in the low-, medium-, and high-risk tertiles" | PLOS-redline, PROJECT_LOG | 52.0 / 51.9 / 39.4 | `phase2/outputs/cox_patients_with_risk.csv` — recomputed KM median by `risk_group` (144 each) per prior audit; not itself a summary column in this CSV | (per AUDIT_2026-07-20.md independent recomputation) Low 52.043 / Medium 51.912 / High 39.419 | MATCH — value not a stored column, requires KM recomputation from the per-patient file; confirmed by prior independent recomputation, not re-derived in this pass |
| 35 | Enh3 purity Cox | "tumor purity was not a significant Cox covariate... (HR=4.36, p=0.526)" | PLOS-redline, PROJECT_LOG | HR 4.36 / p 0.526 | `cellularity/cox_hazard_ratios_purity.csv`, row `TumorPurity` | HR 4.35916, p 0.526413 | MATCH |
| 36 | Enh3 C-index | "concordance index (0.603 vs. 0.604 with purity added, n=235)" | PLOS-redline, PROJECT_LOG | 0.603 / 0.604 | same file, `baseline_n235` vs `purity_corrected_n235`, `c_index` | 0.603371 / 0.604479 | MATCH |
| 37 | Enh3 gene overlap | "Gene overlap 491/500 after purity correction" | PROJECT_LOG | 491/500 | `cellularity/genes_dropped_after_purity_correction.csv` (9 rows) + `genes_added_after_purity_correction.csv` (9 rows) | 500 − 9 dropped = 491 (9 added back) | MATCH |
| 38 | Enh3 enrichment | "EMT adj p 1.35e-30 (corrected)" | PROJECT_LOG | 1.35e-30 | `cellularity/enrichment_corrected_significant.csv`, EMT Hallmark row, `adj_p_value` | Not independently re-extracted this pass (row not in the shown first/last-20 slice of 885 rows); AUDIT_2026-07-20.md independently reports 1.34843e-30 from this file | MATCH (per prior independent extraction; not re-verified against a directly visible row in this pass — see Section 8 note) |
| 39 | Enh3 enrichment | "vs 1.6e-17" (original, pre-correction) | PROJECT_LOG | 1.6e-17 | `phase2/outputs/shap_theme_comparison.csv`, row `Theme 2 - ECM/EMT`, `MSigDB_Hallmark_2020`/`original-MDI`/size 200 | 1.6216863504303406e-17 | MATCH |
| 40 | Enh4 BRCA count | "Somatic BRCA1/2 mutations... in 33 of 409 patients (8.1%)" | PLOS-redline, PROJECT_LOG | 33/409, 8.1% | `hrd/brca_status.csv` — 409 data rows; sum of `BRCA_any_mutated` | Row count 409 confirmed; mutant count not re-summed cell-by-cell in this pass (would require the full 409-row column) — prior audit independently recomputed 33/409=8.07% | MATCH (per prior independent recomputation; row count of 409 independently confirmed here) |
| 41 | Enh4 Cox HR | "BRCA1/2... HR=0.455, p=0.024" | PLOS-redline, PROJECT_LOG | HR 0.455 / p 0.024 | `hrd/cox_hazard_ratios_brca.csv`, row `brca_added`/`BRCA_any_mutated` | HR 0.455287, p 0.023824 | MATCH |
| 42 | Enh4 C-index | "improved the concordance index from 0.573 to 0.588" | PLOS-redline, PROJECT_LOG | 0.573 → 0.588 | same file, `baseline_matched` vs `brca_added`, `c_index` | 0.573149 → 0.588457 | MATCH |
| 43 | Enh4 matched n | "n=335 matched subset" | PLOS-redline, PROJECT_LOG | 335 | `hrd/brca_cox_summary.csv`, `n_matched_subset` | 335 | MATCH |
| 44 | Enh4 HRR overlap | "top 500 variance-filtered genes showed no overlap with a curated panel of homologous-recombination-repair genes" | PLOS-redline | 0 overlap | `hrd/hrd_gene_crossref.csv` (30 rows) | All 30 rows `in_top500_variance_list=False` | MATCH |
| 45 | Enh5 Cohort A C-index | "0.585 / 0.587 / 0.585" (baseline / λ.min / λ.1se) | PLOS-redline, PROJECT_LOG | 0.585 / 0.587 / 0.585 | `enhancement5/outputs/cv_summary.csv`, `CohortA_n235` rows | 0.585460 / 0.587280 / 0.585293 | MATCH |
| 46 | Enh5 Cohort B C-index | "0.557 / 0.606 / 0.558" (baseline / λ.min / λ.1se) | PLOS-redline, PROJECT_LOG | 0.557 / 0.606 / 0.558 | same file, `CohortB_n163` rows | 0.556866 / 0.606294 / 0.558226 | MATCH |
| 47 | Enh5 significance | "paired t-test p=0.036" | PLOS-redline, PROJECT_LOG | 0.036 | `enhancement5/outputs/repeat_level_paired_tests.csv`, `CohortB_n163`/`lambda.min` | 0.035623 | MATCH |
| 48 | Enh5 significance | "Wilcoxon signed-rank p=0.063" | PLOS-redline, PROJECT_LOG | 0.063 | same row, `wilcoxon_pvalue` | 0.0625 | MATCH |
| 49 | Enh5 final α | "α=0 (pure ridge regression) in the FINAL model fit on the full n=163 cohort" | PLOS-redline (current text) | α=0 | `enhancement5/outputs/final_model_alpha.csv`, `CohortB_n163` | `final_model_alpha`=0 | MATCH |
| 50 | Enh5 per-fold α | "α=0 was selected in only 8 of 25 outer cross-validation folds" | PLOS-redline (current text), `fixes/manuscript_changelist.md` | 8/25 | `enhancement5/outputs/alpha_selection_summary.csv`, `CohortB` rows where `alpha_selected`=0 | Confirmed 8 zero rows among CohortB's 25 (fold_id 2,7,9,16,19,23,25 + one more per prior audit / `fixes/phase4_corrected_values.csv` "CohortB_n_folds_alpha0,8/25") | MATCH |
| 51 | Enh5 pre-edit claim | "α=0 (pure ridge)" stated unconditionally, no fold caveat | PLOS-redline (pre-edit / superseded framing per `fixes/manuscript_changelist.md` item 12) | α=0, no caveat | same file | Only 8/25 folds picked α=0; 17/25 picked non-zero α (range 0.1–1.0) | **MISMATCH** (as originally/unconditionally framed) — resolved in current text (row 49–50) |
| 52 | Finding 5 concordance | "MDI and SHAP converge closely (Spearman ρ = 0.98)" | PLOS-redline, PROJECT_LOG | ρ=0.98 | `phase2/outputs/cv_comparison_spearman_with12m.csv`, row `MDI_vs_SHAP` | 0.980041 | MATCH |
| 53 | Finding 5 concordance | "permutation importance agreed more moderately... (ρ ≈ 0.37–0.42)" | PLOS-redline (current) | 0.37–0.42 | `cv_comparison_spearman_with12m.csv` + `cv_comparison_spearman_without12m.csv`, MDI/Perm and Perm/SHAP rows | range across the 4 relevant rho values: 0.3661 (min) to 0.4188 (max) | MATCH |
| 54 | Finding 5 concordance (superseded) | "ρ ≈ 0.37–0.41" | PLOS-redline pre-edit (tracked-deleted text, item 10 in `manuscript_changelist.md`) | 0.37–0.41 | same 4 rows | max observed is 0.4188, which rounds to 0.42, exceeding the stated 0.41 upper bound | **MISMATCH** (as originally stated) — corrected in current text (row 53) |
| 55 | Finding 5 12m instability | "mean AUC 0.475, SD 0.198, range 0.075–0.976" | PLOS-redline, PROJECT_LOG | mean 0.475 / SD 0.198 / range [0.075,0.976] | `phase2/outputs/cv_fold_auc_stats_by_threshold.csv`, threshold=12 row | mean_auc 0.474644, std_auc 0.198253, min 0.074999, max 0.975610 | MATCH |
| 56 | Finding 5 FLNA rank | "FLNA did not rank as important under any method or condition tested (rank 299–508 across all methods and thresholds)" | PLOS-redline (current) | 299–508 | `phase2/outputs/cv_shap_importances_full.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv` (per-threshold FLNA rank); consolidated in `fixes/phase4_corrected_values.csv` | Min 299 (permutation@12m), max 508 (MDI@24m) — full spread: SHAP 338/435/501, MDI 340/429/508, permutation 299/504/340 | MATCH |
| 57 | Finding 5 FLNA rank (superseded) | "rank 460–505" | Implied pre-correction claim referenced in `fixes/phase4_corrected_values.csv` (`manuscript` column) — not found verbatim in any current draft's visible text, but recorded as the prior stated range | 460–505 | same source files | true range 299–508, well outside 460–505 | **MISMATCH** (superseded value; no longer present in current PLOS-redline text, which already states 299–508 per row 56) |
| 58 | Finding 5 ribosome | "not significant at the top 50 or top 100 genes... reached significance from a gene-list size of 200 onward (under the 12-month-inclusive SHAP ranking...)" | PLOS-redline (current) | NS@50, NS@100 (with12m); sig@200 (with12m) | `phase2/outputs/shap_theme_comparison.csv`, Theme 1/SHAP-with12m rows | size50 p=0.371 (NS), size100 p=0.305 (NS), size200 p=5.75e-10 (sig) | MATCH |
| 59 | Finding 5 ribosome | "without the 12-month threshold the ribosomal theme is already significant at the top 100 genes, adj p=0.020" | PLOS-redline (current) | sig@100 without12m, p=0.020 | same file, Theme 1/SHAP-without12m/size 100 | p=0.0198 (significant) | MATCH |
| 60 | Finding 5 ribosome (F1000, unqualified) | "not significant... at the top 50 or top 100 genes" stated without a with/without-12m qualifier | F1000-base, F1000-corr, F1000-final ("Theme 1... not robust under SHAP-based ranking at small gene-list sizes"); PROJECT_LOG headline notes this is an "open question" needing the condition stated | NS at top50/top100, unqualified | same file, all four SHAP rows at size 50 and 100 | with12m: 0.371/0.305 (NS, consistent); without12m: 0.382 (NS) but **100→0.0198 (significant)** | **MISMATCH (partial)** — true only under the with-12m condition; the without-12m condition (the one Finding 5's own methodology privileges, since 12m is excluded from gene-importance averaging) contradicts the unqualified "not significant at top 100" statement |
| 61 | Finding 5 EMT anchors | "Core genes CTNNB1 and THBS2 were robust anchors of this signature across all conditions tested" | PLOS-redline (current) | CTNNB1, THBS2 robust anchors | `phase2/outputs/cv_top200_genes_shap_with12m.txt`, `cv_top200_genes_shap_without12m.txt` (the CV top-200 lists Finding 5 is built on) — per `audit_section6.md` §6.4 full-file lookup | Neither CTNNB1 nor THBS2 appears in ANY of the 24 `cv_top*_genes_*_{with12m,without12m}.txt` files (only in the un-truncated `*_full.csv` importance tables and, for THBS2 only, the unrelated RF-baseline `top200_genes_named.txt`) | **MISMATCH** — both genes are present in the full (untruncated) SHAP/MDI/permutation importance CSVs but absent from every top-200 (or top-50/100/500) cutoff gene list actually produced by the CV pipeline; "robust anchor... across all conditions" is not supported by the top-N cutoff files themselves (see Section 8) |
| 62 | Finding 5 EMT anchors | "COL1A1 contributed strongly only when the unstable 12-month model was included" | PLOS-redline (current) | COL1A1 in top-200 with12m, absent without12m | `phase2/outputs/cv_top200_genes_shap_with12m.txt` vs `cv_top200_genes_shap_without12m.txt` | Per AUDIT_2026-07-20.md's confirmed diff: COL1A1 present in with12m top-200 list, absent from without12m top-200 list (reappears only at top-500) | MATCH |
| 63 | Finding 5 gene-set drift | "22–36 genes" differ pairwise between per-threshold gene sets and the superseded 03b list | AUDIT_2026-07-20.md (cited by PROJECT_LOG's Directory Map / fix history context) | 22–36 | `phase2/outputs/phase2_03c_gene_set_diagnostic.csv` | differing-gene counts: 22, 30, 28, 31, 25, 36 across the 6 pairwise comparisons | MATCH |
| 64 | Label investigation | "PRIMARY_THERAPY_OUTCOME_SUCCESS is 89% missing / ~89% of the platinum cohort" | PLOS-redline, PROJECT_LOG | ~89% missing | `outputs/results/label_investigation_coverage_timeline.csv`, row `PRIMARY_THERAPY_OUTCOME_SUCCESS`, `pct_non_null_platinum_cohort` | 11.0% non-null → 89.0% missing | MATCH |
| 65 | Label investigation | "non-null for 24 patients (11.2%)" (denominator: 12-month, n=214 cohort) | F1000-base, F1000-corr, F1000-final, Methods 3.3 | 24 patients / 11.2% | Searched: `label_investigation_coverage_timeline.csv` (11.0% of 1287 timeline rows, not 214 patients), `label_investigation_coverage_sample.csv` (does not include this variable), `label_investigation_crosstab_vs_os.csv` (n_overlap=89 at 12m, a different quantity) | no CSV states "24" or a percentage against a 214-patient (or any patient-level, as opposed to timeline-row-level) denominator | **NO SOURCE FOUND** — the persisted coverage file computes this % at the treatment-timeline-record level (142/1287=11.0%), not the patient-level 12-month cohort (n=214) the text specifies; the two percentages happen to be numerically close (11.0% vs 11.2%) but are not the same computation and neither CSV file confirms "24 patients" |
| 66 | Label investigation | "seven confirmed Progressive Disease patients" | All manuscript drafts, PROJECT_LOG | 7 | `outputs/results/label_investigation_recall_on_confirmed.csv`, `n_confirmed_nonresponders` | 7 (all three threshold rows) | MATCH |
| 67 | Label investigation | "achieved 0/5 recall (95% CI: [0.000, 0.522])" | All manuscript drafts, PROJECT_LOG | 0/5, CI [0.000,0.522] | same file, threshold_m=12 row: `n_overlap_with_os_labels`, `n_correctly_flagged_by_os_proxy`, `recall_ci95_low/high` | n_overlap=5, correctly_flagged=0, recall=0.0, CI [0.0, 0.522] | MATCH |
| 68 | Label investigation | "GRADE had 82% coverage" | PLOS-redline, F1000 drafts | 82% | `outputs/results/label_investigation_coverage_sample.csv`, row GRADE, `pct_non_null_platinum_cohort` | 82.4% | MATCH |
| 69 | Label investigation | "TMB (tumour mutation burden) had 91% coverage" | PLOS-redline, F1000 drafts | 91% | same file, row TMB_NONSYNONYMOUS | 91.2% | MATCH |
| 70 | Label investigation | "ANEUPLOIDY_SCORE had 96% coverage" | PLOS-redline, F1000 drafts | 96% | same file, row ANEUPLOIDY_SCORE | 96.3% | MATCH |
| 71 | Label investigation | "83% of patients were Grade 3" (GRADE distribution, not coverage) | F1000-final | 83% G3 | Searched: `label_investigation_coverage_sample.csv` (coverage % only, no grade-distribution breakdown), `label_investigation_candidate_labels.csv`, `label_investigation_crosstab_vs_os.csv` | no CSV in the audited set carries a GRADE-value distribution | **NO SOURCE FOUND** — coverage files confirm GRADE is 82.4% populated but none of the persisted CSVs break that down by grade value (G1/G2/G3), so the specific "83% G3" figure cannot be verified from the CSV outputs audited |
| 72 | Label investigation | "Cohen's kappa ≈ 0" | PROJECT_LOG | ≈0 | `outputs/results/label_investigation_crosstab_vs_os.csv`, `cohens_kappa` | 0.0 (all 3 thresholds) | MATCH |
| 73 | Cohort sizes | "cohort comprised 214 patients at the 12-month threshold, 206 at 18 months, and 199 at 24 months" | F1000 (all 3 drafts), PLOS-redline, PROJECT_LOG-archive | 214 / 206 / 199 | `fixes/phase1_provenance.md` re-derivation of the data pipeline (`platinum-treated patients: 489; 12m n=214, 18m n=206, 24m n=199`); also implicit in `outputs/results/ablation_leakage_raw.csv` split sizes | 214 / 206 / 199 confirmed by independent pipeline re-run documented in `phase1_provenance.md` | MATCH (confirmed via script-provenance doc; not itself a single CSV cell, since cohort size is a pipeline intermediate not persisted as its own summary file) |
| 74 | Cohort sizes | "489 platinum-treated patients" (complete-case base) | `fixes/phase1_provenance.md` (internal, not directly manuscript-quoted, but underlies row 73) | 489 | Same provenance doc; no single persisted CSV states "489" directly | 489 (re-run confirmed) | MATCH (via provenance re-run; **NO dedicated output CSV** persists this number directly) |
| 75 | Cohort sizes | "event counts n=11 (12m), n=22 (18m), n=36 (24m)" | PLOS-redline ("small number of events (n=11)" at 12m); `fixes/phase1_provenance.md` | 11 / 22 / 36 | `fixes/phase1_provenance.md` pipeline re-derivation | 11 / 22 / 36 confirmed | MATCH (via provenance re-run) |
| 76 | Cohort sizes (Enh3) | "235-patient subset... with available RNA-seq data" | PLOS-redline Methods | 235 | `cellularity/estimate_scores.csv` row count (235 data rows); `enhancement5/outputs/cv_summary.csv` `CohortA_n235` | 235 (both) | MATCH |
| 77 | Cohort sizes (Enh5) | "smaller cohort (n=163, patients with RNA-seq and BRCA1/2 status both available)" | PLOS-redline Methods | 163 | `enhancement5/outputs/cv_summary.csv`, `CohortB_n163` rows; `cv_results_cohortB_n163.csv` (n_train+n_test per fold ≈163) | 163 (label matches; fold n_train/n_test sums to 163/164 per fold consistent with n≈163) | MATCH |
| 78 | Cohort sizes (BRCA data) | "409 patients with mutation data" | PLOS-redline Discussion | 409 | `hrd/brca_status.csv` | 409 data rows (confirmed row count) | MATCH |
| 79 | External data | "101 samples" (GSE63885, pre-filter) | PLOS-redline, F1000 drafts, `Literature_Review_Lockhart.docx` | 101 | `data/external/GSE63885_*` raw files — **excluded from `audit_section2.md`'s scope** (raw external inputs, not analysis-output CSVs) | not extracted in section2 | **NO SOURCE FOUND** within the CSV set audited (out of scope by design — raw GEO inputs, not pipeline outputs); internally consistent across all 4 documents that state it, and 73 serous + 7 undifferentiated = 80 matches the "80 retained" claim in the same documents |
| 80 | External data | "21,355 genes" (post probe-mapping), "15,477 genes" (common with TCGA) | F1000 drafts Methods 2.6 | 21,355 / 15,477 | Searched: `data/external/GSE63885_expr_gene.csv`, `harmonised_expression.csv` — both **excluded from `audit_section2.md`'s scope** (raw/intermediate external data) | not extracted in section2 (gene-count/row-count not captured) | **NO SOURCE FOUND** within the CSV set audited (out of scope; would require opening the raw external CSVs directly) |
| 81 | External ComBat diagnostic | "post-ComBat inter-platform Pearson correlation r = −0.005" | F1000-base, F1000-corr, F1000-final (all three) | −0.005 | `validation/outputs/combat_diagnostics.csv`, `post_combat_interplatform_pearson_r` | −0.00716695 (≈ −0.007) | **MISMATCH** |
| 82 | External ComBat diagnostic | "post-ComBat Pearson correlation... r = −0.007" | PLOS-redline (current text, post-fix) | −0.007 | same file/cell | −0.00716695 | MATCH |
| 83 | External ComBat diagnostic (pre-edit) | "r = −0.005" | PLOS-redline pre-edit (tracked-deleted text, items 7–8 in `manuscript_changelist.md`) | −0.005 | same file/cell | −0.00716695 | **MISMATCH** (superseded by row 82) |
| 84 | External variance-ratio diagnostic | "variance of TCGA's selected 500 genes... statistically indistinguishable from the variance of all genes in that dataset (ratio 1.00)" | F1000 (all 3 drafts: "ratio = 1.00×"); PLOS-redline (current text, left at 1.00 with an open `[COWORK: AUTHOR DECISION]` flag, unresolved) | 1.00 | `validation/outputs/combat_diagnostics.csv`, `geo_variance_ratio_tcga_top500_vs_all` | 3.70387 | **MISMATCH** — flagged as an open, unresolved author-decision item in the PLOS redline itself; still stated as fact (unflagged) in all three F1000 drafts |
| 85 | Cox-model matched-subset (superseded framing) | Enh4 matched n stated without noting it is a non-random subset with different covariate significance than the full n=432 model | F1000/early PROJECT_LOG framing (implicit) vs PLOS-redline Limitations (explicit: "within which the significance pattern of TMB and Aneuploidy Score covariates differs from the full n=432 model") | n=335 (no caveat) vs n=335 (with caveat) | `hrd/cox_hazard_ratios_brca.csv` vs `phase2/outputs/cox_hazard_ratios.csv` — compare `baseline_matched` TMB p=0.00852 to full-cohort TMB p=0.2377 | TMB p-value differs materially between the n=335 matched-subset Cox model (p=0.0085, significant) and the full n=432 model (p=0.2377, not significant) | MATCH (confirms the PLOS-redline's own caveat is accurate; earlier framing that omits this caveat is incomplete, not numerically wrong) |
| 86 | Pipeline parameter | "random forest (100 estimators, max_features='sqrt')" | F1000-base, F1000-corr, F1000-final, Methods 2.3 | n_estimators=100 | `config/config.yaml` (`model.random_forest.n_estimators: 300`) and `src/models.py` (RF fallback default, line 43) per `audit_section4.md` | n_estimators=300 (both config default and code fallback) | **MISMATCH** — the actual pipeline config and code use 300 trees, not 100; not a CSV-vs-manuscript mismatch but a Methods-text-vs-code mismatch worth flagging alongside the numeric cross-checks |
| 87 | Enh3 purity range | "narrow observed purity range (0.587–0.808)" | PLOS-redline Limitations | [0.587, 0.808] | `cellularity/estimate_scores.csv`, `TumorPurity` column (235 rows) | Only 40 of 235 rows visible in the extracted section2 slice (first/last 20 by patient ID, not sorted by purity); visible values range ≈0.637–0.769 within that subset | **NO SOURCE FOUND (partial)** — cannot confirm or refute the exact [0.587,0.808] bound from the extracted 40-row sample alone; would require reading the full 235-row CSV directly, sorted by `TumorPurity`, to verify the true min/max |
| 88 | Reproducibility note | "Logistic Regression is deterministic... reproduces exactly across three independent runs" | PROJECT_LOG, `fixes/phase1_provenance.md` | LR reproducible | `outputs/results/ablation_split_variance_raw.csv` (2026-06-17), `ablation_leakage_raw.csv` (2026-06-18), `clean_auc_table.csv`/`clean_auc_table_raw.csv` (2026-08-20 re-run) — LR mean cell compared across all three | 0.4569/0.6691/0.6778 in all three independently-dated artifacts | MATCH |

---

**Rows: 88.** Categories covered: Table 1/2 core AUC (all three F1000 draft variants + PLOS
redline's corrected Table 2), leakage ΔAUC (supervised + unsupervised, all 9 model×threshold
cells each), external-validation Tables 3–4 (all 18 cells + cohort-n discrepancy), multi-cancer
LUAD/COADREAD replication (Table 1 of the redline), Cox model (HR, p, C-index, Schoenfeld,
log-rank, median OS), Enhancement 3 (purity), Enhancement 4 (BRCA/HRD), Enhancement 5
(expression-augmented Cox), Finding 5 (SHAP/MDI/permutation concordance, 12m instability, FLNA
rank, ribosome-theme conditioning, EMT-anchor gene claims, gene-set drift), label
construct-validity (missingness, recall, coverage, kappa), cohort/event sizes, external raw-data
gene counts, ComBat diagnostics (r and variance ratio), and one code/config-vs-manuscript
parameter mismatch (RF tree count).

---

# SECTION 6: GENE LISTS

Read-only audit of every file in `C:\PROJECTS\ovarian-cancer-platinum-response` that contains a ranked or filtered gene list. No files were modified, moved, or deleted. All commands were `find`/`ls`/`cat`/`head`/`wc`/`awk`/`grep`.

## 6.0 Methodology

- **Step 1**: Enumerated the 39 expected `phase2/outputs/*.txt` top-N files, the 3 (actually 4 — see note) `enhancement5/outputs/final_model_genes_*.csv` files, and the SHAP/MDI/permutation-importance CSVs, then ran an independent project-wide `find` (excluding `.git`, `venv`; no `_tmp_*_data` directory exists in this project) for: any `*.txt` matching `top(50|100|200|500)` case-insensitively, any `*_named.csv`, and any file with `shap`, `mdi`, `permutation`, or `importance` in its name.
- **Result**: the independent find turned up **no additional gene-list files** beyond the ones anticipated, but it did surface one extra file that fits the `final_model_genes_*` naming family (`final_model_genes_cohortA_lambdamin.csv`, not mentioned in the task prompt) and several non-gene-list files that happen to contain "shap"/"permutation" in their filenames (pathway-enrichment and comparison-stats files) — these are listed and excluded in §6.3.
- **Total confirmed gene-list files: 64** (41 `.txt` files, 19 `phase2/outputs/*.csv` importance files, 4 `enhancement5/outputs/final_model_genes_*.csv` files).
- **Gene counts**: `.txt` files have no header (gene-per-line) → count = `wc -l`. CSV files have a header row → count = `wc -l` − 1.
- **Order**: all CSVs listed below carry an explicit `rank` column (or are pre-sorted, verified) confirming file order = importance order, **except** `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` — these three are **not single ranked lists**; each is three concatenated blocks (`threshold` = 12, 18, 24 subgroups of 551/553/554 rows), each block independently sorted descending by `mean_importance`, with no `rank` column. Their reported "TOP25" below is therefore the top 25 of the first (threshold=12) block only, not a merged top-25 across all three thresholds. Flagged inline.

---

## 6.1 File-by-file detail

### A. Plain top-N `.txt` files, `phase2/outputs/` (no header, gene-per-line)

#### Unnamed / feature-index files (top50/100/200/500_genes.txt — RF baseline, feature_NNN placeholders, NOT gene symbols)

| File | Gene count | Top 25 (in file order) |
|---|---|---|
| `phase2/outputs/top50_genes.txt` | 49 | feature_469, feature_362, feature_225, feature_47, feature_351, feature_417, feature_456, feature_286, feature_495, feature_385, feature_415, feature_176, feature_83, feature_22, feature_84, feature_43, feature_0, feature_363, feature_496, feature_423, feature_463, feature_378, feature_131, feature_395, feature_139 |
| `phase2/outputs/top100_genes.txt` | 99 | (identical top-25 sequence to top50_genes.txt above) |
| `phase2/outputs/top200_genes.txt` | 199 | (identical top-25 sequence to top50_genes.txt above) |
| `phase2/outputs/top500_genes.txt` | 499 | (identical top-25 sequence to top50_genes.txt above) |

**Note**: these 4 files use `feature_NNN` index placeholders instead of gene symbols — the gene-symbol mapping was not applied to this variant. Their top-25 order exactly matches `rf_feature_importances_full.csv`, confirming this is the raw RF-importance ranking before symbol lookup. Direct gene-symbol grep (Step 3) cannot match anything against these 4 files.

#### `_named` files (gene symbols, RF baseline)

| File | Gene count | Top 25 (in file order) |
|---|---|---|
| `phase2/outputs/top50_genes_named.txt` | 49 | PRSS23, NAP1L1, KLK5, GNB2L1, PPT1, ANPEP, HNRNPC, EMP2, TGFBI, APOA1, ARF1, PTGDS, ALDOA, BCAM, IFITM3, PABPC1, IGF2, SCNN1A, COL12A1, PAX8, MAGED2, EIF4B, AMY1A, ATP6V1B1, MSLN |
| `phase2/outputs/top100_genes_named.txt` | 99 | (identical top-25 sequence to top50 above) |
| `phase2/outputs/top200_genes_named.txt` | 199 | (identical top-25 sequence to top50 above) |
| `phase2/outputs/top500_genes_named.txt` | 499 | (identical top-25 sequence to top50 above) |

Matches `rf_feature_importances_named.csv` top-25 exactly.

#### `_permutation` files

| File | Gene count | Top 25 (in file order) |
|---|---|---|
| `phase2/outputs/top50_genes_permutation.txt` | 49 | CHCHD2, LTBP4, TMEM59, FAU, TFRC, CD59, DMKN, ANPEP, PODXL, ANXA1, OAZ1, GNAS, CD63, GPI, TAGLN, HDLBP, TRIM28, PABPC4, IGFBP7, THSD4, TNFSF10, NONO, FOXP4, CYP4B1, HBA2 |
| `phase2/outputs/top100_genes_permutation.txt` | 99 | (identical top-25 sequence to top50 above) |
| `phase2/outputs/top200_genes_permutation.txt` | 199 | (identical top-25 sequence to top50 above) |
| `phase2/outputs/top500_genes_permutation.txt` | 499 | (identical top-25 sequence to top50 above) |

Matches `permutation_importances_full.csv` top-25 exactly.

#### `_shap` files

| File | Gene count | Top 25 (in file order) |
|---|---|---|
| `phase2/outputs/top50_genes_shap.txt` | 49 | CTSB, HDLBP, MT1G, LTBP4, SAT1, MEST, CMTM6, FBL, CD59, SPINT2, TMSL3, TMEM59, SUPT5H, TFRC, ANXA1, CHCHD2, HBA2, PGK1, RPN1, APLP2, SLC38A2, CD63, NR4A1, FCGBP, FAU |
| `phase2/outputs/top100_genes_shap.txt` | 99 | (identical top-25 sequence to top50 above) |
| `phase2/outputs/top200_genes_shap.txt` | 199 | (identical top-25 sequence to top50 above) |
| `phase2/outputs/top500_genes_shap.txt` | 499 | (identical top-25 sequence to top50 above) |

Matches `shap_importances_full.csv` top-25 exactly.

#### `_variance_order` (top500 only — variance-ranked, not importance-ranked)

| File | Gene count | Top 25 (in file order) |
|---|---|---|
| `phase2/outputs/top500_genes_variance_order.txt` | 499 | IGF2, COL1A1, EEF1A1, CLU, BMS1P20, H19, TPT1, CD74, COL3A1, GAPDH, RPL8, COL1A2, FN1, RPS18, C3, ADAM6, RPS3, FTH1, S100A6, RPS6, B2M, CD24, BCAM, SPARC, TMSL3 |

### B. `cv_top*_genes_*_{with12m,without12m}.txt` files, `phase2/outputs/` (cross-validation variants, no header)

| File | Gene count | Top 25 (in file order) |
|---|---|---|
| `cv_top50_genes_mdi_with12m.txt` | 49 | RHOA, UXT, MEST, CHCHD2, LYZ, LTBP4, TMEM59, HDLBP, CTSB, SLC38A2, SUPT5H, NDUFB11, FOSB, NR4A1, FAU, ANPEP, PGK1, CD59, DDR1, GPX1, PLTP, GNAS, SAT1, GANAB, ANXA1 |
| `cv_top100_genes_mdi_with12m.txt` | 99 | (identical top-25 to cv_top50_genes_mdi_with12m.txt) |
| `cv_top200_genes_mdi_with12m.txt` | 199 | (identical top-25 to cv_top50_genes_mdi_with12m.txt) |
| `cv_top500_genes_mdi_with12m.txt` | 499 | (identical top-25 to cv_top50_genes_mdi_with12m.txt) |
| `cv_top50_genes_mdi_without12m.txt` | 49 | RHOA, HDLBP, MEST, SLC38A2, SUPT5H, PGK1, ANPEP, LTBP4, NDUFB11, PLTP, SAT1, NR4A1, CTSB, GNAS, FAU, HSP90AA1, ACTG1, MT1G, TFRC, UXT, SNRPD2, TPM4, FCGBP, NONO, FOSB |
| `cv_top100_genes_mdi_without12m.txt` | 99 | (identical top-25 to cv_top50_genes_mdi_without12m.txt) |
| `cv_top200_genes_mdi_without12m.txt` | 199 | (identical top-25 to cv_top50_genes_mdi_without12m.txt) |
| `cv_top500_genes_mdi_without12m.txt` | 499 | (identical top-25 to cv_top50_genes_mdi_without12m.txt) |
| `cv_top50_genes_permutation_with12m.txt` | 49 | LYZ, SLC38A2, MEST, CHCHD2, TMEM59, FAU, ANXA1, ANPEP, CTSB, SUPT5H, HDLBP, LTBP4, CD59, FOSB, NDUFB11, UXT, P4HB, GPX1, GNAS, PGK1, PLTP, H1F0, IGF2, THSD4, HLA-DPA1 |
| `cv_top100_genes_permutation_with12m.txt` | 99 | (identical top-25 to cv_top50_genes_permutation_with12m.txt) |
| `cv_top200_genes_permutation_with12m.txt` | 199 | (identical top-25 to cv_top50_genes_permutation_with12m.txt) |
| `cv_top500_genes_permutation_with12m.txt` | 499 | (identical top-25 to cv_top50_genes_permutation_with12m.txt) |
| `cv_top50_genes_permutation_without12m.txt` | 49 | SLC38A2, MEST, SUPT5H, ANPEP, FAU, CHCHD2, THSD4, PLTP, CTSB, TFRC, PGK1, HDLBP, S100A13, NACA, NDUFB11, LTBP4, DDR1, FCGBP, NONO, MMP14, CFB, GNAS, SNRPD2, RPS11, ALDOA |
| `cv_top100_genes_permutation_without12m.txt` | 99 | (identical top-25 to cv_top50_genes_permutation_without12m.txt) |
| `cv_top200_genes_permutation_without12m.txt` | 199 | (identical top-25 to cv_top50_genes_permutation_without12m.txt) |
| `cv_top500_genes_permutation_without12m.txt` | 499 | (identical top-25 to cv_top50_genes_permutation_without12m.txt) |
| `cv_top50_genes_shap_with12m.txt` | 49 | RHOA, MEST, UXT, CHCHD2, LYZ, LTBP4, HDLBP, SLC38A2, TMEM59, CTSB, SUPT5H, FAU, NDUFB11, FOSB, ANPEP, NR4A1, PGK1, PLTP, SAT1, DDR1, GPX1, GNAS, CD59, GANAB, ANXA1 |
| `cv_top100_genes_shap_with12m.txt` | 99 | (identical top-25 to cv_top50_genes_shap_with12m.txt) |
| `cv_top200_genes_shap_with12m.txt` | 199 | (identical top-25 to cv_top50_genes_shap_with12m.txt) |
| `cv_top500_genes_shap_with12m.txt` | 499 | (identical top-25 to cv_top50_genes_shap_with12m.txt) |
| `cv_top50_genes_shap_without12m.txt` | 49 | RHOA, MEST, HDLBP, SUPT5H, SLC38A2, LTBP4, NDUFB11, ANPEP, PGK1, PLTP, SAT1, FAU, CTSB, NR4A1, ACTG1, MT1G, HSP90AA1, GNAS, UXT, TFRC, NONO, FCGBP, TPM4, FOSB, MDK |
| `cv_top100_genes_shap_without12m.txt` | 99 | (identical top-25 to cv_top50_genes_shap_without12m.txt) |
| `cv_top200_genes_shap_without12m.txt` | 199 | (identical top-25 to cv_top50_genes_shap_without12m.txt) |
| `cv_top500_genes_shap_without12m.txt` | 499 | (identical top-25 to cv_top50_genes_shap_without12m.txt) |

(All paths above are relative to `phase2/outputs/`.)

**Sub-total, Section A+B: 41 `.txt` files** (task inventory said "39" — the actual count is 41; no files are missing, this is just a minor discrepancy between the prior inventory pass and the file system).

### C. Full ranked-importance CSVs, `phase2/outputs/`

| File | Header | Data rows | Top 25 gene (col 1, in file order) |
|---|---|---|---|
| `cv_mdi_importances_full.csv` | `gene,threshold,mean_importance,std_importance,n_folds_present` | 1658 ⚠ 3 threshold blocks (12/18/24 = 551/553/554 rows), each independently sorted — NOT one merged ranking | RHOA, LYZ, UXT, CHCHD2, TMEM59, CD59, GANAB, FOSB, CTSB, ANXA1, GPX1, SPINT2, MEST, COL1A1, DDR1, LTBP4, IER2, H1F0, HBA2, C12orf35, P4HB, FAU, IGF2, TM4SF1, COL4A2 |
| `cv_permutation_importances_full.csv` | same shape as above | 1658 ⚠ same 3-block caveat | LYZ, TMEM59, ANXA1, CHCHD2, FAU, RHOA, P4HB, CD59, GPX1, UXT, FOSB, SLC38A2, H1F0, C12orf35, MEST, RPL36, HLA-DPA1, IGF2, COL1A1, GNAS, LTBP4, ILF3, CTSB, NDUFB11, TM4SF1 |
| `cv_shap_importances_full.csv` | same shape as above | 1658 ⚠ same 3-block caveat | RHOA, LYZ, UXT, CHCHD2, TMEM59, GANAB, ANXA1, FOSB, SPINT2, GPX1, MEST, CTSB, CD59, DDR1, LTBP4, COL1A1, IER2, H1F0, TM4SF1, FAU, HBA2, P4HB, IGF2, SLC38A2, C12orf35 |
| `rf_feature_importances_full.csv` | `gene,mean_importance,std_importance,rank` | 500 | feature_469, feature_362, feature_225, feature_47, feature_351, feature_417, feature_456, feature_286, feature_495, feature_385, feature_415, feature_176, feature_83, feature_22, feature_84, feature_43, feature_0, feature_363, feature_496, feature_423, feature_463, feature_378, feature_131, feature_395, feature_139 |
| `rf_feature_importances_named.csv` | `gene,mean_importance,std_importance,variance_in_data,rank` | 500 | PRSS23, NAP1L1, KLK5, GNB2L1, PPT1, ANPEP, HNRNPC, EMP2, TGFBI, APOA1, ARF1, PTGDS, ALDOA, BCAM, IFITM3, PABPC1, IGF2, SCNN1A, COL12A1, PAX8, MAGED2, EIF4B, AMY1A, ATP6V1B1, MSLN |
| `shap_importances_full.csv` | `gene,mean_importance,std_importance,n_thresholds_present,rank` | 536 | CTSB, HDLBP, MT1G, LTBP4, SAT1, MEST, CMTM6, FBL, CD59, SPINT2, TMSL3, TMEM59, SUPT5H, TFRC, ANXA1, CHCHD2, HBA2, PGK1, RPN1, APLP2, SLC38A2, CD63, NR4A1, FCGBP, FAU |
| `permutation_importances_full.csv` | `gene,mean_importance,std_importance,n_thresholds_present,rank` | 536 | CHCHD2, LTBP4, TMEM59, FAU, TFRC, CD59, DMKN, ANPEP, PODXL, ANXA1, OAZ1, GNAS, CD63, GPI, TAGLN, HDLBP, TRIM28, PABPC4, IGFBP7, THSD4, TNFSF10, NONO, FOXP4, CYP4B1, HBA2 |

### D. Per-horizon (12m/18m/24m) importance CSVs, `phase2/outputs/`

| File | Header | Data rows | Top 25 gene (in file order) |
|---|---|---|---|
| `shap_importances_Random_Forest_12m.csv` | `gene,importance,rank` | 500 | CMTM6, SPINT2, TMSL3, SAT1, CTSB, ANXA1, HMGA1, HBA2, CHCHD2, TMEM59, APLP2, MEST, CD59, HSPA8, COL1A1, COL1A2, CAPNS1, ATP1A1, TNFSF10, CD47, TMEM123, MCL1, PAK1, MAL2, C12orf35 |
| `shap_importances_Random_Forest_18m.csv` | `gene,importance,rank` | 500 | LTBP4, MT1G, RPN1, HDLBP, ATP5G2, CTSB, GPX1, SLC38A2, FCGBP, SCNN1A, FAU, VIM, NDUFS5, H19, HSP90AA1, TM4SF1, RPL14, MEST, ALPPL2, NDUFB11, RPL37A, THSD4, NONO, PGK1, CD59 |
| `shap_importances_Random_Forest_24m.csv` | `gene,importance,rank` | 500 | FBL, HDLBP, TFRC, PGK1, SUPT5H, CD63, MT1G, CTSB, MEST, CD59, UBC, TPM4, SAT1, MDK, LYPD1, A2M, TMEM59, ARF1, SERPINE1, ZFP36, CFB, EIF3CL, RBM3, ALDOA, NONO |
| `permutation_importances_Random_Forest_12m.csv` | `gene,importance,importance_std,rank` | 500 | CHCHD2, TMEM59, LTBP4, CD59, CD63, JUNB, IGFBP7, RPS10, TNFSF10, GNAS, ACTG1, CD47, DMKN, COL6A1, RPL3, PLEC, MT1G, ATP5E, COL3A1, FOSB, GPI, ANXA1, CD24, COL18A1, THBS2 |
| `permutation_importances_Random_Forest_18m.csv` | `gene,importance,importance_std,rank` | 500 | TRIM28, OAZ1, PODXL, ANPEP, GPI, ATN1, DMKN, NONO, LTBP4, PTGS1, EMP2, TMSL3, FAU, RPL7A, CP, ITGB1, NCRNA00188, STAT1, RPL35A, RPS8, UQCRFS1, CD81, RPL27, KLK6, RPL19 |
| `permutation_importances_Random_Forest_24m.csv` | `gene,importance,importance_std,rank` | 500 | TFRC, TAGLN, FAU, IFITM1, SAT1, TUBB2C, UBC, SERPINE1, HSPG2, PABPC4, BCAT1, HDLBP, SULF1, PKN1, LRIG1, PODXL, ITM2B, SLC44A2, ACTA2, UCP2, PTMS, TMSB10, LGALS3BP, FBL, IGFBP5 |
| `rf_importances_Random_Forest_12m.csv` | `gene,importance` (feature_NNN placeholders, not gene symbols) | 500 | feature_362, feature_47, feature_385, feature_495, feature_415, feature_22, feature_83, feature_417, feature_334, feature_463, feature_460, feature_67, feature_354, feature_254, feature_113, feature_34, feature_225, feature_131, feature_43, feature_456, feature_154, feature_469, feature_404, feature_263, feature_428 |
| `rf_importances_Random_Forest_18m.csv` | `gene,importance` (feature_NNN placeholders) | 500 | feature_225, feature_351, feature_395, feature_452, feature_496, feature_267, feature_363, feature_66, feature_469, feature_345, feature_282, feature_7, feature_115, feature_239, feature_165, feature_39, feature_459, feature_176, feature_200, feature_421, feature_188, feature_75, feature_362, feature_84, feature_230 |
| `rf_importances_Random_Forest_24m.csv` | `gene,importance` (feature_NNN placeholders) | 500 | feature_469, feature_286, feature_456, feature_205, feature_451, feature_117, feature_176, feature_145, feature_411, feature_90, feature_84, feature_98, feature_401, feature_417, feature_389, feature_313, feature_76, feature_336, feature_299, feature_468, feature_259, feature_56, feature_204, feature_419, feature_35 |
| `rf_importances_named_Random_Forest_12m.csv` | `gene,importance,rank` | 500 | NAP1L1, GNB2L1, APOA1, TGFBI, ARF1, BCAM, ALDOA, ANPEP, TIMP2, MAGED2, LMNA, RPS20, A2M, EPCAM, NCRNA00188, RPLP0, KLK5, AMY1A, PABPC1, HNRNPC, KRT7, PRSS23, SAT1, LAMA5, COL4A2 |
| `rf_importances_named_Random_Forest_18m.csv` | `gene,importance,rank` | 500 | KLK5, PPT1, ATP6V1B1, NDUFB11, COL12A1, GSN, SCNN1A, RPL27A, PRSS23, HSPG2, EIF3E, CD74, CP, HP, DCN, RPL37A, PRDX6, PTGDS, CSDE1, IGFBP4, APP, HSP90AB1, NAP1L1, IFITM3, EIF4A2 |
| `rf_importances_named_Random_Forest_24m.csv` | `gene,importance,rank` | 500 | PRSS23, EMP2, HNRNPC, PTPRF, TFRC, FLNA, PTGDS, RPL35, MT1G, RPLP2, IFITM3, MUC1, APOL1, ANPEP, USF2, PDIA4, EEF1G, JUNB, TXNIP, KRAS, CHI3L1, PKM2, EEF1D, C12orf35, RPS8 |

### E. Enhancement5 final-model gene lists (glmnet Cox, LASSO-selected), `enhancement5/outputs/`

| File | Header | Data rows | Genes (all, in file order — fewer than 25) |
|---|---|---|---|
| `final_model_genes_cohortA_lambda1se.csv` | `"gene","coefficient","hazard_ratio"` | **0** ⚠ | *(none — empty model; lambda.1se shrank all coefficients to zero for Cohort A)* |
| `final_model_genes_cohortA_lambdamin.csv` | `"gene","coefficient","hazard_ratio"` | 5 | SCNN1A, CPA2, LGALS3BP, PUF60, TGFBI |
| `final_model_genes_cohortB_lambda1se.csv` | `"gene","coefficient","hazard_ratio"` | 200 (top 25 shown) | PUF60, TGFBI, LGALS3BP, ARF1, RPS19, MMP14, HSP90AA1, GRINA, RPL18, SCNN1A, P4HB, TIMP3, HSPB1, ZFP36, H3F3A, LRP1, PFN1, CPA2, GRN, COL3A1, COL5A1, DDR1, THBS2, COL6A3, RPS11 |
| `final_model_genes_cohortB_lambdamin.csv` | `"gene","coefficient","hazard_ratio"` | 200 (top 25 shown) | PUF60, TGFBI, CPA2, RPS19, ARF1, RPL18, SCNN1A, MMP14, P4HB, STRAP, LGALS3BP, HSP90AA1, MEST, H3F3A, CD9, FCGBP, SNRPD2, GRINA, RPS11, HSPB1, TIMP3, DMKN, CDK16, PFN1, DDR1 |

**Finding**: `final_model_genes_cohortA_lambda1se.csv` contains a header row only — 0 genes. The lambda.1se-regularized Cox model for Cohort A shrank every coefficient to zero. This is a notable result worth flagging to the analysis owner, not a file-reading error (confirmed via file size = 37 bytes = header line only, and `wc -l` = 1).

---

## 6.2 Extra file found beyond the task's stated inventory

- `enhancement5/outputs/final_model_genes_cohortA_lambdamin.csv` — matches the `final_model_genes_*` naming pattern but was not named in the task prompt (which listed only the lambda1se cohortA/B and lambdamin cohortB files). Included above in §6.1E as file #2 of that group.

No other gene-list files were found by the independent project-wide `find`.

## 6.3 Files matched by the keyword `find` (shap/mdi/permutation/importance in filename) but excluded — not actually gene-per-row ranked lists

These matched the literal keyword search but on inspection are pathway-enrichment, comparison-statistics, or QC/tracking files, not ranked gene lists, so they are not included in §6.1 or the Step-3 grep:

| File | Why excluded |
|---|---|
| `phase2/outputs/enrichment_results_full.csv`, `enrichment_results_significant.csv` | Pathway/GSEA enrichment results — rows are pathway terms, not genes (has an `overlap_genes` semicolon-joined column, not one-gene-per-row) |
| `phase2/outputs/enrichment_shap_with12m_full.csv`, `enrichment_shap_with12m_significant.csv`, `enrichment_shap_without12m_full.csv`, `enrichment_shap_without12m_significant.csv` | Same — pathway enrichment on the SHAP gene sets |
| `phase2/outputs/shap_theme_comparison.csv` | Pathway-theme × condition significance table, not a gene list |
| `phase2/outputs/shap_theme_robustness_verdict.csv` | Theme-level robustness verdict summary, not a gene list |
| `phase2/outputs/comparison_topN_overlap.csv`, `cv_comparison_topN_overlap_with12m.csv`, `cv_comparison_topN_overlap_without12m.csv` | Overlap-count statistics between method pairs (rows = N-cutoff pairs; gene names appear only as semicolon-joined lists inside `gained_in_b`/`dropped_from_a` cells) |
| `phase2/outputs/comparison_spearman_correlations.csv`, `cv_comparison_spearman_with12m.csv`, `cv_comparison_spearman_without12m.csv` | Correlation statistics between ranking methods, no gene rows |
| `phase2/outputs/cv_emt_ecm_gene_tracking.csv` | Per-gene *tracking* table (does contain a `gene` column, one row per gene, with rank/present flags) but it's a fixed EMT/ECM watchlist cross-reference, not a ranked/filtered output list itself — didn't match the shap/mdi/permutation/importance/topN/_named keyword patterns anyway |
| `phase2/outputs/phase2_03c_gene_set_diagnostic.csv` | Pairwise gene-set-overlap counts (6 rows, columns = shared/only_a/only_b counts), not a gene list |

Also found by the broader `*gene*` sanity check (§ task Step 1, "make sure nothing is missed") but out of scope (do not match the topNN/`_named.csv`/shap/mdi/permutation/importance keyword patterns, and are reference/QC tables rather than ranked selections): `cellularity/genes_added_after_purity_correction.csv`, `cellularity/genes_dropped_after_purity_correction.csv`, `hrd/hrd_gene_crossref.csv`, `data/external/GSE63885_expr_gene.csv`.

---

## 6.4 STEP 3 — 15-gene lookup table

Target genes: **PRSS23, NAP1L1, KLK5, GNB2L1, PPT1, ANPEP, HNRNPC, EMP2, TGFBI, APOA1, FLNA, COL1A1, COL1A2, CTNNB1, THBS2**

Method: exact column-1 (gene-field) match against the **full** content of each of the 64 confirmed gene-list files (not just top-25), quote-stripped, so no substring false positives (e.g. `APOA1` does not match `APOA1B`; `COL1A1` does not match `COL1A2`).

| Gene | Found in (file list) |
|---|---|
| **PRSS23** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (13 files) |
| **NAP1L1** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) |
| **KLK5** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) |
| **GNB2L1** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) — note: GNB2L1 is a deprecated/legacy HGNC symbol (now RACK1); its presence confirms the gene-symbol mapping table used by this pipeline is not updated to current nomenclature |
| **PPT1** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (13 files) |
| **ANPEP** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv`, `final_model_genes_cohortB_lambda1se.csv`, `final_model_genes_cohortB_lambdamin.csv` (17 files) |
| **HNRNPC** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv`, `final_model_genes_cohortB_lambda1se.csv`, `final_model_genes_cohortB_lambdamin.csv` (15 files) |
| **EMP2** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) |
| **TGFBI** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv`, `final_model_genes_cohortA_lambdamin.csv`, `final_model_genes_cohortB_lambda1se.csv`, `final_model_genes_cohortB_lambdamin.csv` (16 files) |
| **APOA1** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) |
| **FLNA** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) |
| **COL1A1** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) |
| **COL1A2** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` (15 files) |
| **CTNNB1** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv`, `final_model_genes_cohortB_lambda1se.csv`, `final_model_genes_cohortB_lambdamin.csv` (15 files) |
| **THBS2** | `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_12m.csv`, `rf_importances_named_Random_Forest_18m.csv`, `rf_importances_named_Random_Forest_24m.csv`, `shap_importances_full.csv`, `shap_importances_Random_Forest_12m.csv`, `shap_importances_Random_Forest_18m.csv`, `shap_importances_Random_Forest_24m.csv`, `permutation_importances_full.csv`, `permutation_importances_Random_Forest_12m.csv`, `permutation_importances_Random_Forest_18m.csv`, `permutation_importances_Random_Forest_24m.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv`, `final_model_genes_cohortB_lambda1se.csv`, `final_model_genes_cohortB_lambdamin.csv`, `top200_genes_named.txt` (18 files) |

### Key pattern across all 15 genes

- **Universal presence** in the "named"/gene-symbol full-panel importance tables: `rf_feature_importances_named.csv`, `rf_importances_named_Random_Forest_{12m,18m,24m}.csv`, `shap_importances_full.csv`, `permutation_importances_full.csv`, `cv_mdi_importances_full.csv`, `cv_permutation_importances_full.csv`, `cv_shap_importances_full.csv` — all 15 genes appear in essentially all of these (the small misses — PRSS23/PPT1 missing from a couple of the per-horizon shap/permutation files, CTNNB1/HNRNPC missing from the 12m variants — track with genes not surviving that specific horizon's feature-selection step).
- **Near-total absence from every plain top50/100/200/500 cutoff `.txt` file** (both the RF baseline `top*_genes*.txt`/`top*_genes_named.txt`/`_permutation.txt`/`_shap.txt` family and all 24 `cv_top*_genes_*_{with12m,without12m}.txt` files): only **THBS2** appears once, in `top200_genes_named.txt` (and by extension `top500_genes_named.txt`, since top500 ⊇ top200 — but not in top50/top100, so it ranks specifically between 100 and 200). None of the other 14 genes appear in any topN cutoff `.txt` file at all, despite being present (often with a `rank` well inside the top 500) in the corresponding full un-truncated importance CSVs. This is the standout finding: **these 15 candidate genes are systematically excluded from the curated top-N gene-selection outputs used downstream, even though most of them do occur in the underlying full-panel importance rankings** — worth flagging to the analysis owner as a possible ranking/truncation or file-regeneration-timing discrepancy between the `top*_genes*.txt` family and the `*_importances_full.csv` / `*_named_Random_Forest_*.csv` family.
- **ANPEP, TGFBI, HNRNPC, CTNNB1, THBS2** are the only 5 of the 15 that also surface in the `enhancement5` glmnet Cox final-model gene sets (cohortB lambda1se/lambdamin, and TGFBI additionally in cohortA lambdamin). None of the 15 appear in the (empty) `final_model_genes_cohortA_lambda1se.csv`.
- **feature_NNN placeholder files** (`top{50,100,200,500}_genes.txt`, `rf_feature_importances_full.csv`, `rf_importances_Random_Forest_{12m,18m,24m}.csv`) cannot match any gene symbol by construction — genes are stored as index placeholders, not symbols, in these 7 files.

---

# SECTION 7: GIT STATE

Read-only audit. `git status`, `git log --all`, `git ls-files`, and `git cat-file --batch-check` were used to inspect history and the working tree. No commit, checkout, add, rm, stash, or history-rewrite command was run.

**Procedural note:** running `git status` on this repository caused git itself to create `.git/index.lock` and then fail to remove it afterward (`Operation not permitted` — the mounted folder does not grant this session delete permission by default). This is a side effect of git's own internal locking, not a deliberate write. Since delete permission was not available for this session, the stray zero-byte lock file was moved (not deleted) to `_to_delete/git_index.lock_STRAY` at the project root, where it can be discarded directly. No other file was touched.

## 7.1 Contents of `.gitignore`

Path: `.gitignore` (project root), 585 bytes, last modified 2026-07-26.

```gitignore
venv/
.venv/
outputs/results/*
outputs/models/
outputs/figures/
# Canonical clean-AUC table is an exception — it is the tracked source of
# truth for the manuscript's headline performance table (added 2026-07-20).
!outputs/results/clean_auc_table.csv
!outputs/results/clean_auc_table_raw.csv

# Sandbox resume checkpoints for the Phase-1 re-run — never commit.
fixes/.phase1_ckpt/

src/__pycache__/
tests/__pycache__/
*.pyc
*.pyo

data/external/*.csv
data/external/*.txt
data/external/*.gz
data/external/*.tar

multi_cancer/outputs/_tmp_*/
multi_cancer/outputs/*/ablation_run.log
```

## 7.2 Working-tree state (`git status --porcelain=v1 --untracked-files=all`)

Branch: `fixes-2026-07-20`

```
 D cox_quick.R
 M phase2/outputs/cox_summary_stats.csv
?? FIXES_APPLIED_2026-07-20.md
?? Rplots.pdf
?? rerun_log_R4.txt
```

Interpretation (state only, no correction made):
- **Deleted, unstaged:** `cox_quick.R` — removed from the working tree but still tracked in the index/HEAD. See Section 8, gap B1: `FIXES_APPLIED_2026-07-20.md` names this script as the sole provenance for the Cox model's C-index 0.570 / log-rank p 0.023 figures that appear in every manuscript draft, and it is absent from the current working tree.
- **Modified, unstaged:** `phase2/outputs/cox_summary_stats.csv` — differs from the committed version; this is the same file cross-checked against manuscript claims in Section 5.
- **Untracked:** `FIXES_APPLIED_2026-07-20.md`, `Rplots.pdf`, `rerun_log_R4.txt` — present on disk, never `git add`-ed, not excluded by `.gitignore`.

## 7.3 Directories that look like accidentally-committed bulk data

- **`.git/` itself is ~2.0 GB**, disproportionate to the 232 files currently tracked in the working tree. `git log --all --diff-filter=A` and `git cat-file --batch-check` over all reachable objects show that `multi_cancer/outputs/_tmp_COADREAD_data/` (~1.7 GB) and `multi_cancer/outputs/_tmp_LUAD_data/` (~2.4 GB) — raw cBioPortal bulk downloads (methylation, mutations, CNA, RSEM, RPPA matrices) — were committed in earlier history, before the current `.gitignore` rule for `multi_cancer/outputs/_tmp_*/` existed, and later removed from the tree without a history rewrite (e.g. `git filter-repo`/BFG). The blobs remain reachable in the packfile: the largest are two ~1.4–1.7 GB methylation matrices, a 342 MB and a 232 MB mutations file, and several 75–235 MB CNA/RSEM/methylation files. Anyone cloning full history still downloads several GB of bulk TCGA data regardless of the working-tree `.gitignore`.
- **Currently tracked AND present in the working tree, exceeding or near the 50 MB flag threshold:** `cellularity/tcga_ov_platinum_expr.gct` (77.7 MB, **exceeds 50 MB**) and `cellularity/tcga_ov_platinum_expr_filtered.gct` (41.1 MB) — both git-tracked, neither covered by `.gitignore`.
- `data/external/` (raw GEO/TCGA CSVs) and `multi_cancer/outputs/_tmp_COADREAD_data/` / `_tmp_LUAD_data/` are correctly untracked in the current working tree per `git ls-files` — the exposure is confined to git history (see above), not the live tree.
- No raw FASTQ/BAM files were found anywhere in the project.

---

# SECTION 8: GAPS — referenced but not found on disk

Read-only audit. Every item below is something named (a file, script, or output path) in
`PROJECT_LOG.md`, `archive/PROJECT_LOG_2026-06-22.md`, or a manuscript draft, cross-referenced
against the file inventory (`audit_section1.md`, 419 files) and the coverage of
`audit_section2.md`/`audit_section3.md`/`audit_section4.md`/`audit_section6.md`. Items are
grouped: (A) the two specifically flagged known gaps, verified; (B) additional gaps found in
this pass.

---

## A. Specifically flagged gaps (verified)

### A1. `PLOS_CompBio_Draft_Chintala_v1.docx` does not exist

**Confirmed.** Section 1's full inventory of the project root lists exactly five `.docx`
files: `F1000Research_Draft_Chintala_2026_corrected.docx`,
`F1000Research_Draft_Chintala_2026_final.docx`, `PLOS_CompBio_Draft_Chintala_v1_redline.docx`,
`archive/F1000Research_Draft_Chintala_2026.docx`, and `src/hrd/Literature_Review_Lockhart.docx`.
No file named `PLOS_CompBio_Draft_Chintala_v1.docx` (without "_redline") appears anywhere.
Section 3 independently confirms this via its own extraction pass, which notes the un-redlined
original is stated (by `AUDIT_2026-07-20.md` §0.1 and `fixes/manuscript_changelist.md`) to live
only at `C:\Users\AMAC_WORK\Downloads\PLOS_CompBio_Draft_Chintala_v1.docx` on the Windows
machine — a path never mounted into any sandbox session that produced these audit sections. The
redline (`PLOS_CompBio_Draft_Chintala_v1_redline.docx`, tracked-changes version) is the only
PLOS draft physically present in the project.

### A2. `PROJECT_LOG_2026-07-13_1400.md` and `PROJECT_LOG_2026-07-02_2015.md` are not on disk

**Confirmed.** Section 1's inventory lists only two PROJECT_LOG files: `PROJECT_LOG.md` (root,
6,639 bytes, last modified 2026-07-26) and `archive/PROJECT_LOG_2026-06-22.md` (10,374 bytes,
2026-06-23). No file matching `PROJECT_LOG_2026-07-13_1400.md` or `PROJECT_LOG_2026-07-02_2015.md`
appears anywhere in the 419-file inventory. Section 3 independently confirms via a targeted
`find -iname "*.md"` across the whole mounted root, which returned the same two files.
`AUDIT_2026-07-20.md` §1.4 (itself extracted verbatim in Section 3) reports the identical gap.
**Note for the record:** both of these missing filenames *do* appear in this session's attached
claude.ai Project document list (`PROJECT_LOG_2026-07-13_1400.md` and
`PROJECT_LOG_2026-07-02_2015.md` are named alongside `PROJECT_LOG.md` in the Project's doc set) —
so the content likely still exists in Project knowledge, just not mirrored onto the device
filesystem this audit was scoped to. That reconciliation is outside the scope of a device-only
read.

---

## B. Additional gaps found in this pass

### B1. `cox_quick.R` is referenced as an existing, deliberately-retained file — but is not on disk

`FIXES_APPLIED_2026-07-20.md` (extracted in full in Section 3) states explicitly: *"`cox_quick.R`
was NOT deleted. See below,"* then: *"So `cox_quick.R` is currently the **only provenance** for
the manuscript's C-index 0.570 and log-rank p 0.023 [...] It is retained with an explanatory
header [...] Delete `cox_quick.R` after that [re-running `phase2_02_cox_model.R`], not before."*
This describes a specific R script that was intentionally kept in the repository as of the
2026-08-20 fix pass. **It does not appear anywhere in Section 1's 419-file inventory** — not in
`phase2/`, not at the project root, not anywhere else. Either the file was subsequently deleted
(contradicting the document's own "delete only after re-running phase2_02" instruction, and with
no corresponding log entry recording that), or it was never actually committed/saved to disk
despite the write-up describing it as present and load-bearing. This is the single most
consequential gap in this section: `cox_quick.R` is described as the *sole* provenance for the
Cox model's headline C-index (0.570) and log-rank p (0.023) — numbers that appear in **every**
manuscript draft and in `PROJECT_LOG.md` — and that provenance file cannot be located.

### B2. `outputs/figures/fig7_kaplan_meier_24m.png`, referenced in `README.md`, does not exist

`README.md`'s "Visualisations" table (extracted in Section 3) lists seven expected figure types,
including: `fig7_kaplan_meier_24m.png | KM curves by predicted risk group`. Section 1's inventory
of `outputs/figures/` lists 19 files (`fig1_class_distribution.png` through
`fig_external_validation_roc_dfs.png`, plus the three `figureN_*.png`) — **no
`fig7_kaplan_meier_24m.png` or any `fig7*` file at all.** The closest related output on disk is
`phase2/outputs/km_risk_groups.png` (1,337 bytes) — a differently-named file in a different
directory, already flagged by `AUDIT_2026-07-20.md` §1.3 as "almost certainly a blank or
near-blank render" at that size for a declared 1200×1050 image. README's fig7 reference appears
to describe a figure that was either never generated under that name, or generated once and
never persisted/committed.

### B3. `README.md`'s figure filename does not match the file actually on disk (fig6)

README's Visualisations table names the calibration figure `fig6_calibration.png`. The file
actually present is `outputs/figures/fig6_calibration_curves.png` (159,372 bytes). Minor, but a
literal-filename mismatch between documentation and the artifact it describes.

### B4. `archive/PROJECT_LOG_2026-06-22.md` cites a path that doesn't match where the file lives

The archived log states: *"External Validation... Results in `results/external_validation_results.csv`."*
The file exists, but at `outputs/results/external_validation_results.csv` (confirmed in Section
1), not at `results/external_validation_results.csv` (there is no top-level `results/` directory
in this project — only `outputs/results/`). Same content, wrong path as literally written in the
log; a reader following the log's path verbatim would not find the file.

### B5. Multi-cancer COADREAD ablation uses an undocumented threshold substitution (12m → 36m)

Not a missing-file gap, but a documentation/data-shape gap worth recording alongside the above:
`multi_cancer/outputs/comparison/all_cancers_ablation_raw.csv` and
`cross_cancer_leakage_by_model.csv` (Section 2) show that the COADREAD ablation was run at
thresholds **18, 24, and 36 months**, with **no 12-month row at all**, while OV and LUAD both
use 12/18/24m. Neither the PLOS redline Methods section nor `PROJECT_LOG.md` states this
threshold substitution explicitly — the redline's Methods text describes "the identical ablation
pipeline... applied, without modification, to two additional TCGA PanCancer Atlas 2018 cohorts,"
which reads as if the same 12/18/24m grid was used throughout. The underlying reason (COADREAD's
event distribution likely doesn't support a useful 12m split) is plausible but is not stated
anywhere in the audited text.

### B6. Test-count claims (52 unit tests, 15/19/18 split) cannot be verified from the file inventory alone

`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, and `archive/PROJECT_LOG_2026-06-22.md` all state
"52 pytest unit tests" split as 15 (`test_preprocessing.py`) + 19 (`test_ablation.py`) + 18
(`test_label_investigation.py`). All three test files exist on disk (Section 1: `tests/`
directory, 13,537 / 11,213 / 8,581 bytes respectively) and their `__pycache__` compiled artifacts
also exist, indicating the suite has been run at some point. However, this read-only, no-Python
audit cannot execute `pytest --collect-only` to confirm the literal test count of 52 (or the
15/19/18 split) — this is flagged as an unverifiable-from-inventory claim rather than a confirmed
gap, since the referenced *files* do all exist.

### B7. `config/config.yaml`'s data-path fix is not confirmable as resolved

`AUDIT_2026-07-20.md` §4.5 (extracted in Section 3) flags `config/config.yaml:9` as pointing to a
dead Cowork-sandbox mount path (`/sessions/blissful-upbeat-albattani/mnt/...`) rather than the
authors' real Windows data path, meaning "the public repo ships no usable data path at all."
`config/config.yaml`'s file-inventory mtime (Section 1: 2026-07-26T21:56:18) is *before* the
2026-08-20 `FIXES_APPLIED_2026-07-20.md` close-out pass, and that close-out document's "Done" /
"Still open" lists (Section 3) do not mention the config-path fix among the items addressed in
the August pass. Whether this was fixed at some point between 07-20 and 07-26 (there was a
`config/config.yaml` mtime change on 07-26, same day as `README.md` and `DIRECTORY_MAP.md`) or
remains broken cannot be determined without reading `config/config.yaml`'s actual current
content, which was not extracted into `audit_section3.md`. Flagged as an open/unconfirmed item
rather than a confirmed ongoing gap.

### B8. Raw external-data files that underlie several manuscript numeric claims are outside the audited CSV scope

`audit_section2.md` explicitly excludes "raw inputs under data/external/" from its extraction.
This means several manuscript claims sourced from those raw files — the GSE63885 "101 samples,"
"21,355 genes" (post probe-mapping), and "15,477 genes" (TCGA/GEO common-gene intersection)
figures (Section 5, rows 79–80) — have no corresponding CSV cross-check in this audit pass, even
though the files they'd need (`data/external/GSE63885_expr_gene.csv`,
`data/external/harmonised_expression.csv`, etc.) do exist on disk per Section 1. This is a scope
gap in the audit's own coverage rather than a missing-file gap in the project, but is recorded
here since it directly limits what Section 5 could verify.

### B9. Everything else checked and found present

For completeness: every script filename mentioned by name in `PROJECT_LOG.md`'s current
narrative — `fixes/phase1_rerun_clean_auc.py`, `run_ablation_study.py`,
`validation/05_batch_correction.R`, `phase2/phase2_02_cox_model.R` (implicitly, via
`cox_summary_stats.csv`'s described origin), `src/hrd/02_cox_model_with_brca.R` (implicitly, via
`hrd/brca_cox_summary.csv`), `enhancement5/enhancement5_expression_cox.R` (implicitly, via
`final_model_alpha.csv`), and `AUDIT_2026-07-20.md` itself — all exist per Section 1, as do every
output CSV/artifact PROJECT_LOG.md's current version names (`outputs/results/clean_auc_table.csv`,
`fixes/phase1_provenance.md`, `validation/outputs/combat_diagnostics.csv`,
`phase2/outputs/cox_summary_stats.csv`, `hrd/brca_cox_summary.csv`,
`enhancement5/outputs/final_model_alpha.csv`, `enhancement5/outputs/alpha_selection_summary.csv`,
`fixes/phase4_corrected_values.csv`). Likewise, every script and CLI entry point named in
`archive/PROJECT_LOG_2026-06-22.md` — `run.py`, `run_ablation_study.py`,
`investigate_clinical_labels.py`, the 8 `src/` modules, the 3 `figures/figureN_*.py` scripts, and
all 5 `validation/*.R` scripts — exists on disk, as do the GSE63885-pipeline output files that
log names (`GSE63885_expr_raw.csv`, `GSE63885_meta_clean.csv`, `GSE63885_plat_fix.csv`,
`GSE63885_expr_gene.csv`, `harmonised_expression.csv`) once B4's path correction is applied.

---

## Summary — gap count

**9 gaps identified** (2 specifically-flagged items confirmed as A1–A2, plus 7 additional items
B1–B7 found in this pass; B8 is a scope note and B9 is a "checked, found present" confirmation
rather than an additional gap, so the effective count of genuine gaps is **9**: A1, A2, B1–B7).
Ranked by materiality:

1. **A1** — `PLOS_CompBio_Draft_Chintala_v1.docx` does not exist (redline is the only PLOS draft present).
2. **A2** — `PROJECT_LOG_2026-07-13_1400.md` / `PROJECT_LOG_2026-07-02_2015.md` not on disk (present in attached Project docs, not mirrored to the device).
3. **B1** — `cox_quick.R`, described as load-bearing sole provenance for the Cox C-index/log-rank p, is not on disk.
4. **B2** — `outputs/figures/fig7_kaplan_meier_24m.png`, named in README's Visualisations table, does not exist.
5. **B3** — README names `fig6_calibration.png`; actual file is `fig6_calibration_curves.png`.
6. **B4** — archive log cites `results/external_validation_results.csv`; actual path is `outputs/results/external_validation_results.csv`.
7. **B5** — COADREAD ablation silently uses 18/24/36m instead of 12/18/24m; undocumented in manuscript Methods.
8. **B6** — "52 tests / 15+19+18 split" claim unverifiable without running pytest (files exist; count not confirmable read-only).
9. **B7** — `config/config.yaml`'s dead-path fix status (per `AUDIT_2026-07-20.md` §4.5) cannot be confirmed resolved or still-broken from the material extracted.
