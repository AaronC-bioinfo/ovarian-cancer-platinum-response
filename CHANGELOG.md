# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2.0.0] — 2026-11-04

### Changed
- The study is now a label-validity analysis: coverage, agreement and provenance of candidate
  platinum-response labels in TCGA-OV (`label_validity/`, analyses A1–A23), replacing the v1.0.0
  interpretation of overall-survival thresholds as platinum-response labels.
- Manuscript source, build scripts and supporting information in `manuscript_v5/`; figures in `figures/v5/`.

### Added
- Versioned patient-level label table with the provenance of each re-derived call
  (`label_validity/outputs/label_resource_v1.csv`, S11 Table).

### Removed
- Superseded drafts, audits, reviews and analyses are no longer part of the released tree
  (earlier tracked versions remain in the repository history).

## [1.0.0] — 2025-12-01

### Added
- Modular `src/` package: `data_loader`, `preprocessing`, `features`,
  `models`, `evaluation`, `visualization`, `pipeline`, `ablation`,
  `label_investigation`
- Three CLI entry points with `--help`: `run.py`, `run_ablation_study.py`,
  `investigate_clinical_labels.py`
- YAML-driven configuration with committed template (`config/config.template.yaml`);
  `config/config.yaml` gitignored
- 52 pytest unit tests; all pass without TCGA data on disk
- Paired ablation study: unsupervised vs. supervised feature-selection leakage
  across 30 repeated random splits × 3 thresholds × 3 models, with paired
  Wilcoxon and t-tests
- Bootstrap confidence intervals for ROC-AUC
- Nested cross-validation utility
- Clopper-Pearson exact binomial CIs on recall estimates for small n
- Label construct-validity investigation comparing `PRIMARY_THERAPY_OUTCOME_SUCCESS`
  against OS-threshold proxy labels
- Publication-quality figures (7 types, 300 DPI)
- `pyproject.toml` with entry points and packaging metadata
- `CITATION.cff` for academic citation
- `LICENSE` (MIT)
- `CONTRIBUTING.md`, `CHANGELOG.md`
- Regression tests for real-data bugs: NaN in RSEM expression, mixed-type
  gene name indices
