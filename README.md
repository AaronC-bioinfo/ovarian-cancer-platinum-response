# Ovarian Cancer Platinum Treatment Response Prediction

> **Predicting chemotherapy response in ovarian cancer patients using RNA-seq gene expression and machine learning.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5%2B-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/1243993955.svg)](https://doi.org/10.5281/zenodo.20802753)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Approach](#approach)
- [Pipeline Architecture](#pipeline-architecture)
- [Key Results](#key-results)
- [Repository Structure](#repository-structure)
- [How to Run](#how-to-run)
- [Configuration](#configuration)
- [Visualisations](#visualisations)
- [Commercial-Grade Features](#commercial-grade-features)
- [Future Improvements](#future-improvements)

---

## Project Overview

Ovarian cancer is the fifth leading cause of cancer death in women. The standard first-line treatment is **platinum-based chemotherapy** (carboplatin or cisplatin), yet up to 25% of patients are intrinsically resistant and relapse within months.

This project builds a **binary classification pipeline** that predicts whether a patient will respond to platinum therapy — defined as overall survival beyond a fixed time threshold (12, 18, or 24 months) — using bulk RNA-seq gene expression profiles from the TCGA dataset.

**Clinical impact:** Early identification of resistant patients could redirect them to alternative or experimental therapies before completing an ineffective treatment cycle.

---

## Problem Statement

| | |
|---|---|
| **Task** | Binary classification: platinum responder (0) vs. non-responder (1) |
| **Input** | RNA-seq expression of top 500 most variable genes (RSEM-normalised) |
| **Labels** | OS-based cutoffs at 12 / 18 / 24 months |
| **Challenge** | Class imbalance, small sample size (~200 labelled patients), high dimensionality |

---

## Dataset

**Source:** [TCGA Ovarian Serous Cystadenocarcinoma — PanCancer Atlas 2018](https://www.cbioportal.org/study/summary?id=ov_tcga_pan_can_atlas_2018)

| File | Content |
|------|---------|
| `data_clinical_patient.txt` | OS months, vital status, clinical covariates |
| `data_timeline_treatment.txt` | Drug names, treatment timeline per patient |
| `data_mrna_seq_v2_rsem.txt` | mRNA expression (genes × samples), ~20,500 genes |

**See `data/README.md` for download instructions.**

---

## Approach

### Label Engineering

Platinum response is defined as a **binary OS-based label** at each threshold:

```
response = 0  (Responder)      → OS ≥ threshold months
response = 1  (Non-responder)  → Died before threshold (event = 1, OS < threshold)
response = NaN (Ambiguous)     → Censored before threshold → excluded
```

Three thresholds are evaluated: **12m, 18m, 24m**.

### Feature Selection

- Top **500 most variable genes** are selected by training-set variance only (no leakage).
- Features are **z-score standardised** per gene (fit on train, applied to test).

### Models

All models use `class_weight='balanced'` to correct for label imbalance:

| Model | Regularisation | Notes |
|-------|---------------|-------|
| Logistic Regression (L2) | Ridge | Baseline linear model |
| Random Forest (300 trees) | Ensemble | Non-linear, feature importance |
| SVM (RBF kernel) | Soft-margin C=1 | Non-linear, robust to outliers |

### Evaluation

- **Primary metric:** ROC-AUC (insensitive to class imbalance)
- 5-fold stratified cross-validation on training set
- Hold-out test evaluation (20% stratified split)
- SHAP values for feature-level explainability
- Kaplan–Meier curves stratified by predicted risk group

---

## Pipeline Architecture

```
run.py
  │
  └── src/pipeline.py               ← Orchestrates all steps
        │
        ├── src/data_loader.py      ← Read raw .txt files
        ├── src/preprocessing.py    ← Survival labels, platinum patients
        ├── src/features.py         ← Gene selection, z-score scaling
        ├── src/models.py           ← Build, train, cross-validate, save
        ├── src/evaluation.py       ← Metrics, results table
        └── src/visualization.py    ← All publication-quality figures
```

All pipeline parameters are controlled via `config/config.yaml` — no hardcoded values in code.

---

## Key Results

> Results are means across 30 repeated random splits using
correct (train-only) feature selection. Single-split results
vary substantially — see the ablation study for the full
distribution and confidence intervals.

| Model               | 12m AUC | 18m AUC | 24m AUC |
|---------------------|---------|---------|---------|
| Logistic Regression | ~0.70   | ~0.70   | ~0.70   |
| Random Forest       | ~0.67   | ~0.68   | ~0.68   |
| SVM (RBF)           | ~0.45   | ~0.66   | ~0.67   |

> **Note on leakage:** Supervised F-score feature selection inflates
these AUCs by a mean of +0.22 (up to +0.55 for SVM), significant at
p<0.0001 in 7/9 model×threshold combinations. Unsupervised variance
selection shows negligible inflation (+0.01). See
`run_ablation_study.py` for the full analysis.

---

## Repository Structure

```
ovarian-cancer-platinum-response/
│
├── config/
│   ├── config.template.yaml      ← Committed template (copy to config.yaml)
│   └── config.yaml               ← Local only, gitignored
│
├── data/
│   ├── README.md                 ← Download instructions
│   └── raw/                      ← (not tracked) TCGA data goes here
│
├── notebooks/
│   └── analysis.ipynb            ← Clean, reproducible walkthrough
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py            ← I/O layer
│   ├── preprocessing.py          ← Survival labels, expression cleaning
│   ├── features.py               ← Gene selection, scaling
│   ├── models.py                 ← Model factory, training, CV, persistence
│   ├── evaluation.py             ← Metrics and results table
│   ├── visualization.py          ← All figure functions
│   ├── pipeline.py               ← End-to-end orchestrator
│   ├── ablation.py               ← Leakage ablation, bootstrap CIs, nested CV
│   └── label_investigation.py   ← Clinical label validity investigation
│
├── tests/
│   ├── __init__.py
│   ├── test_preprocessing.py     ← 15 unit tests
│   ├── test_ablation.py          ← 19 unit tests
│   └── test_label_investigation.py ← 18 unit tests
│
├── outputs/
│   ├── figures/                  ← Auto-generated plots (PNG, 300 DPI)
│   ├── models/                   ← Serialised model files (.pkl)
│   └── results/                  ← CSV performance summaries
│
├── .gitignore
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── investigate_clinical_labels.py  ← CLI: label validity investigation
├── paper.bib                       ← JOSS bibliography
├── paper.md                        ← JOSS submission document
├── pyproject.toml                  ← Package metadata and entry points
├── requirements.txt
├── run.py                          ← CLI: full pipeline
└── run_ablation_study.py           ← CLI: methods-critique ablation
```

---

## How to Run

### 1. Clone and install

```bash
git clone https://github.com/AaronC-bioinfo/ovarian-cancer-platinum-response.git
cd ovarian-cancer-platinum-response

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Download data

Follow the instructions in `data/README.md` to download the TCGA OV dataset from cBioPortal.

### 3. Configure paths

Copy the config template and fill in your local data path:

```bash
cp config/config.template.yaml config/config.yaml
```

Then edit `config/config.yaml` and set:

```yaml
data:
  data_dir: "path/to/your/ov_tcga_pan_can_atlas_2018"
```

Note: config/config.yaml is gitignored and never committed.
See config/config.template.yaml for all available options.

### 4. Run the full pipeline

```bash
python run.py
```

Optional arguments:

```bash
python run.py --data-dir /path/to/data         # override data directory
python run.py --thresholds 12 24               # run only 12m and 24m
python run.py --log-level DEBUG                # verbose logging
```

### 5. Run tests

```bash
pytest tests/ -v
```

### 6. Open the notebook

```bash
jupyter lab notebooks/analysis.ipynb
```

---

## Configuration

All parameters live in `config/config.yaml`. No changes to source code are needed for common experiments:

```yaml
clinical:
  thresholds: [12, 18, 24]       # survival cutoffs in months
  platinum_drugs:
    - CARBOPLATIN
    - CISPLATIN

features:
  top_n_genes: 500               # increase for potentially higher AUC

model:
  test_size: 0.20
  cv_folds: 5
  random_forest:
    n_estimators: 300
```

---

## Visualisations

| Figure | Description |
|--------|-------------|
| `fig1_class_distribution.png` | Class balance at each time threshold |
| `fig2_roc_{thr}m.png` | ROC curves for all 3 models per threshold |
| `fig3_confusion_{thr}m.png` | Normalised confusion matrices |
| `fig4_cv_auc_heatmap.png` | Cross-validated AUC across model × threshold |
| `fig5_feature_importance_{thr}m.png` | Top 20 genes by RF importance |
| `fig6_calibration.png` | Reliability diagram for RF models |
| `fig7_kaplan_meier_24m.png` | KM curves by predicted risk group |

---

## Commercial-Grade Features

| Feature | Implementation |
|---------|---------------|
| **Configuration** | YAML config; zero hardcoded parameters |
| **Logging** | Structured `logging` module throughout; configurable level |
| **Error handling** | Descriptive exceptions with user-friendly CLI messages |
| **No data leakage** | Gene variance computed on train split only |
| **Reproducibility** | Global seed propagated from config to all stochastic components |
| **Model persistence** | `pickle` serialisation per model per threshold |
| **Unit tests** | 52 pytest tests across 3 modules; all pass without TCGA data on disk |
| **Modularity** | Clean separation: loader / preprocessing / features / models / evaluation / viz |
| **CLI** | argparse entry point with help text and overrides |

---

## Future Improvements

1. **Hyperparameter tuning** — `GridSearchCV` / `Optuna` for C, n_estimators, top_n_genes
2. **SMOTE oversampling** — augment minority class using `imbalanced-learn`
3. **XGBoost / LightGBM** — gradient boosting often outperforms RF in genomics
4. **Multi-omic fusion** — combine RNA-seq with CNV or methylation features
5. **LASSO feature selection** — replace variance filter with L1-penalised logistic regression for sparser, more interpretable gene sets
6. **Nested cross-validation** — reduce optimistic bias in AUC estimation on small cohorts
7. **External validation** — test on an independent ovarian cancer cohort (e.g., ICGC OV)
8. **Survival modelling** — replace binary labels with Cox proportional hazards regression for continuous risk scoring
9. **Docker container** — `Dockerfile` for fully reproducible execution
10. **CI/CD** — GitHub Actions workflow for automated test runs

---

## Methods-Critique Ablation Study

`run_ablation_study.py` quantifies, with data rather than assertion, how much
two common evaluation mistakes inflate reported performance in genomic ML
papers:

1. **Feature-selection leakage** — computing gene-variance ranking on the
   full dataset before the train/test split, versus the correct train-only
   approach. Run across repeated random splits to report a distribution of
   the inflation, not a single anecdotal number.
2. **Single-split variance** — how much reported AUC swings purely from the
   luck of the random train/test split, motivating bootstrap confidence
   intervals and nested cross-validation over single hold-out reporting.

```bash
python run_ablation_study.py --n-repeats 30
```

Outputs:
- `outputs/results/ablation_leakage_summary.csv` — mean ± std AUC per
  model/threshold under leaky vs. correct conditions, plus the inflation delta
- `outputs/results/ablation_split_variance_summary.csv` — AUC range across
  repeated random splits
- `outputs/figures/fig8_leakage_ablation.png` — paired box plots visualising
  the inflation effect

This analysis requires no data beyond what’s already configured for the main
pipeline, and is intended as the empirical backbone of a methods-critique
framing for publication — see the project’s research roadmap for full context.

---

## Citation

If you use this software, please cite it using the metadata in
[CITATION.cff](CITATION.cff).

**Primary dataset:**
> The Cancer Genome Atlas Research Network. (2011). Integrated genomic
analyses of ovarian carcinoma. *Nature*, 474(7353), 609–615.
https://doi.org/10.1038/nature10166

**Data access:**
> Cerami, E., et al. (2012). The cBio Cancer Genomics Portal: An open
platform for exploring multidimensional cancer genomics data.
*Cancer Discovery*, 2(5), 401–404.
https://doi.org/10.1158/2159-8290.CD-12-0095

---

## License

MIT License — see [LICENSE](LICENSE) for details.
