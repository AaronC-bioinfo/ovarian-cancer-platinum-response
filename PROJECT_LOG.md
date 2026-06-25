# Ovarian Cancer Platinum Response — Master Project Log

**Last updated:** 2026-06-22  
**Purpose:** Complete running log of all work done. Paste this into any new chat to resume exactly where we left off.

---

## Project Identity

- **GitHub:** `https://github.com/AaronC-bioinfo/ovarian-cancer-platinum-response`
- **Zenodo DOI (version-specific):** `10.5281/zenodo.20802753`
- **Zenodo DOI (concept/latest):** `10.5281/zenodo.20802754`
- **ORCID:** `0009-0009-0062-6453`
- **Author:** Aaron Michael Anuroop Chintala
- **Affiliation:** School of Systems Biology, George Mason University, Manassas, VA, USA
- **Local project path:** `C:\PROJECTS\ovarian-cancer-platinum-response`
- **GitHub username:** `AaronC-bioinfo`

---

## Current Status (as of 2026-06-22)

### ✅ COMPLETED: JOSS Submission
- Paper submitted to JOSS at `https://joss.theoj.org/papers/new`
- Status: **Submitted, review not yet started**
- All required files in repo: `paper.md`, `paper.bib`, `CITATION.cff`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`
- ORCID added to `paper.md` front matter
- Zenodo `archive:` field added to `paper.md` front matter

### ✅ COMPLETED: F1000Research Draft
- Full paper drafted, verified against all results CSVs, figures generated and embedded
- Final document: `F1000Research_Draft_Chintala_2026_final.docx` (local only, not in git)
- Figure scripts committed to GitHub: `figures/figure1_pipeline.py`, `figures/figure2_ablation.py`, `figures/figure3_validation.py`
- Figure PNGs committed to GitHub: `figures/figure1_pipeline.png`, `figures/figure2_ablation.png`, `figures/figure3_validation.png`
- Latest commit: `b06cb0a` — "Add figure generation scripts and rendered figures for F1000Research submission"
- **Status: Ready to submit to F1000Research**

### ✅ COMPLETED: External Validation (GSE63885)
- GSE9891 dropped — no survival/response data in GEO deposit
- GSE63885: downloaded, parsed, probe-mapped, batch-corrected, classifiers applied
- All R scripts complete in `validation/` subfolder
- Results in `results/external_validation_results.csv`

---

## What Has Been Built (Pipeline)

### Source modules (`src/`)
8 modules: `data_loader`, `preprocessing`, `features`, `models`, `evaluation`, `visualization`, `ablation`, `label_investigation`
- Note: paper describes 7 modules (visualization excluded as utility-only) — this is intentional

### CLI entry points
- `run.py` — full pipeline
- `run_ablation_study.py` — methods-critique ablation
- `investigate_clinical_labels.py` — label validity investigation

### Figure scripts (`figures/`)
- `figure1_pipeline.py` — pipeline architecture diagram (no data required)
- `figure2_ablation.py` — leakage ablation bar chart (reads `results/ablation_supervised_leakage_summary.csv` and `results/ablation_split_variance_summary.csv`)
- `figure3_validation.py` — external validation heatmap (reads `results/external_validation_results.csv`)
- All scripts use argparse; run from project root with `--out figures/figureN_name.png`

### Tests
- 52 unit tests across 3 modules (`test_preprocessing.py`, `test_ablation.py`, `test_label_investigation.py`)
- All pass without TCGA data on disk
- 3 regression tests for real-data bugs (NaN in RSEM, mixed-type gene indices)

---

## Key Research Findings

### Finding 1 — Feature Selection Leakage Ablation
- **Unsupervised variance selection:** mean AUC inflation +0.01, largely non-significant (3/9 significant but max ΔAUC = +0.053) → pipeline is clean
- **Supervised F-score selection:** mean inflation +0.22, up to +0.55 for SVM at 12m
- 7/9 model×threshold combinations significant at p<0.0001
- Run across 30 repeated random splits
- **Headline:** leakage magnitude depends almost entirely on supervised vs. unsupervised selection

### Finding 2 — Label Construct Validity
- `PRIMARY_THERAPY_OUTCOME_SUCCESS` is 89% missing in platinum cohort — only 7 confirmed Progressive Disease patients
- OS-threshold proxy showed **0/5 recall** (95% CI: [0.000, 0.522], Clopper-Pearson exact) on confirmed non-responders
- GRADE: 82% covered but 83% G3 — no variance, useless as covariate
- TMB (91%) and ANEUPLOIDY_SCORE (96%) are viable future covariates
- **Core point:** OS-threshold labels capture overall mortality trajectory; `PRIMARY_THERAPY_OUTCOME_SUCCESS` captures first-line drug response — genuinely different clinical constructs

### Finding 3 — External Validation Failure (GSE63885)
- All models AUC ~0.5 on GSE63885 (range 0.356–0.603) — near chance
- Post-ComBat inter-platform Pearson correlation r = −0.005
- RNA-seq trained classifiers cannot transfer to microarray cohorts even with ComBat
- Variance ratio of TCGA top-500 genes in GEO = 1.00× — feature selection is not the bottleneck; failure is platform-harmonisation

### Verified AUC Results (30 repeated clean splits, unsupervised variance selection)
| Model | 12m AUC | 18m AUC | 24m AUC |
|---|---|---|---|
| Logistic Regression | 0.542 | 0.658 | 0.712 |
| Random Forest | 0.411 | 0.609 | 0.709 |
| SVM (RBF) | 0.363 | 0.515 | 0.771 |

Source: `results/ablation_split_variance_summary.csv` — these are the authoritative clean-split numbers.

---

## Methods Correction (incorporated into F1000Research draft)

- **Wrong:** report named a pre-z-scored expression file
- **Correct:** actual pipeline used `data_mrna_seq_v2_rsem.txt` (raw expression) with StandardScaler applied post-split
- **Missing from report:** platinum-treated patient filtering via `data_timeline_treatment.txt` AGENT field
- **Cohort sizes confirmed:** 214/206/199 at 12/18/24m

---

## F1000Research Paper — Verification Summary

All numbers in the final draft verified against results CSVs on 2026-06-22:

| Item | Status |
|---|---|
| Table 1 core AUC values | ✅ Corrected to ablation_split_variance_summary.csv means |
| Table 2 ablation ΔAUC (all 9 rows) | ✅ Exact match to ablation_supervised_leakage_summary.csv |
| Table 3 & 4 external validation AUC | ✅ Exact match to external_validation_results.csv |
| DFS label count (40 sensitive, not 41) | ✅ Corrected in Abstract + Section 2.6 |
| Recall 0/5, CI [0.000, 0.522] | ✅ Clopper-Pearson confirmed correct |
| CI method: Clopper-Pearson | ✅ Confirmed (Wilson gives [0.000, 0.434] — does not match) |
| Unsupervised significance claim | ✅ Updated to "largely non-significant, max ΔAUC = +0.053" |
| Methods corrections (RSEM file, scaler, AGENT field) | ✅ All incorporated |
| ORCID, DOIs, GitHub URL | ✅ All correct |
| Figure 1 pipeline diagram | ✅ Generated and embedded |
| Figure 2 ablation bar chart | ✅ Generated and embedded |
| Figure 3 validation heatmap | ✅ Generated and embedded |

---

## Git Commit History (key commits)

| Commit | Description |
|---|---|
| Initial | Core pipeline, README, tests |
| `d355c3d` | Ablation study, label investigation, 52 tests, CI columns, `--help` |
| `3240156` | Removed config.yaml from tracking |
| `462ecea` | All JOSS files at project root, .gitignore fixed |
| `a9744d2` | README: 6 corrections |
| `aa60ed0` | Add Zenodo DOI badge and update CITATION.cff |
| `ba63d6c` | Add Zenodo archive DOI to paper.md front matter + ORCID |
| `3c4e0d0` | Add external validation pipeline and GSE63885 results |
| `b06cb0a` | Add figure generation scripts and rendered figures for F1000Research submission |

---

## Publication Strategy

### Phase 1: F1000Research (NOW — ready to submit)
- **Target:** F1000Research
- **Article type:** Research Article (methods critique + software)
- **Document:** `F1000Research_Draft_Chintala_2026_final.docx` (local)
- **Content:** Software description + 3 findings + figures
- **Figure scripts:** in `figures/` subfolder, reproducible from `results/` CSVs

### Phase 2: PLOS Computational Biology (3-4 months)
- Cox proportional hazards model replacing binary OS-threshold labels
- Covariates: TMB and ANEUPLOIDY_SCORE (both >90% coverage confirmed)
- Biological annotation of top RF feature importance genes (KEGG/Reactome, HRD/BRCA pathway)
- Cite F1000 paper and Zenodo DOI
- No duplicate reporting of binary classifier AUC as new results

### Key Rules for Phase 2
- F1000 paper must be cited explicitly
- Cox model reports C-index and hazard ratios — entirely new metrics
- Methods section in PLOS points to F1000 paper for full pipeline details

---

## External Validation Details

### Dataset: GSE63885 (Lisowska et al. 2014, Frontiers in Oncology)
- 80 serous + undifferentiated samples after filtering
- Platform: Affymetrix HG U133 Plus 2.0 (GPL570)
- Labels:
  - Clinical: CR/PR=0 vs P/SD=1 → 74 labeled (64 responders, 10 non-responders)
  - DFS: sensitive=0 vs resistant=1 → 74 labeled (40 sensitive, 34 resistant)

### R Scripts (`validation/`)
| Script | Status | Output |
|---|---|---|
| `01_download_and_parse.R` | ✅ | `GSE63885_expr_raw.csv` |
| `02_parse_metadata.R` | ✅ | `GSE63885_meta_clean.csv` |
| `03_fix_labels.R` | ✅ | `GSE63885_plat_fix.csv` |
| `04_probe_mapping.R` | ✅ | `GSE63885_expr_gene.csv` (21,355 genes × 80 samples) |
| `05_batch_correction.R` | ✅ | `harmonised_expression.csv` (15,477 genes × 80 samples) |

### R Library Path
- Personal library: `C:/Users/AMAC_WORK/R/library`
- Always add `.libPaths(c("C:/Users/AMAC_WORK/R/library", .libPaths()))` at top of every R script
- R executable: `C:\Program Files\R\R-4.6.0\bin\Rscript.exe`

---

## Future Work (Phase 2 prep)

- Attempt PTRC-HGSOC data access approval (after F1000 submitted)
- Cox proportional hazards modelling with TMB/ANEUPLOIDY_SCORE as covariates
- Biological interpretation: RF feature importance → KEGG/Reactome → HRD/BRCA literature
- PhD application deadlines (Aug–Jan) are the real time constraint

---

## Tools & Environment
- **Local machine:** Alienware m16 R2, Ubuntu + Windows, Python 3.12, VS Code
- **Execution:** Cowork (Anthropic desktop automation tool)
- **Dataset:** TCGA Ovarian Serous Cystadenocarcinoma PanCancer Atlas 2018
- **Package tooling:** `pyproject.toml`, `setuptools.build_meta`, `pip install -e ".[dev]"`
- **Version control:** GitHub (`AaronC-bioinfo`)

---

## How to Resume in a New Chat

1. Paste this entire file into the new chat
2. State what you want to work on next
3. Current immediate next action: **Submit F1000Research_Draft_Chintala_2026_final.docx to F1000Research at https://f1000research.com/articles/submit**
