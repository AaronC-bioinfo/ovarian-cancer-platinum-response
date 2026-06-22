# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
