---
title: 'A Reproducible ML Pipeline for Ovarian Cancer Platinum-Response Prediction with Empirical Quantification of Feature-Selection Leakage'
tags:
  - Python
  - bioinformatics
  - machine learning
  - ovarian cancer
  - RNA-seq
  - feature selection
  - data leakage
  - reproducibility
authors:
  - name: Aaron Michael Anuroop Chintala
    affiliation: 1
affiliations:
  - name: School of Systems Biology, George Mason University, Manassas, VA, USA
    index: 1
date: 01 December 2025
bibliography: paper.bib
---

# Summary

`ovarian-cancer-platinum-response` is a modular, reproducible Python pipeline
for predicting platinum chemotherapy response in ovarian cancer patients using
bulk RNA-seq gene expression profiles from the TCGA Ovarian Serous
Cystadenocarcinoma cohort [@tcga2011]. The software trains and evaluates three
supervised classifiers — Logistic Regression, Random Forest, and Support Vector
Machine — across three survival thresholds (12, 18, and 24 months), and
provides evaluation tools including cross-validated ROC-AUC with bootstrap
confidence intervals, SHAP explainability [@lundberg2017], and Kaplan-Meier
survival stratification [@davidson2019].

Beyond the core prediction pipeline, the package includes a paired ablation
study that empirically quantifies AUC inflation from a widely documented but
poorly specified failure mode in genomic machine learning: computing feature
selection statistics on the full dataset before the train/test split. The key
contribution is the distinction between unsupervised variance-based filtering
(mean inflation: +0.01 AUC, non-significant across 30 repeated splits) and
supervised F-score-based selection (mean inflation: +0.22 AUC, up to +0.55 for
SVM, significant at p<0.0001 in 7 of 9 model/threshold combinations). A label
construct-validity investigation further examines whether the OS-threshold proxy
labels standard in this literature capture the clinical construct they are
assumed to represent.

# Statement of Need

Machine learning applied to cancer genomics regularly reports optimistic
performance, a problem attributed in part to feature selection leakage
[@vabalas2019; @teschendorff2019]. However, published guidance rarely
distinguishes between supervised selection methods — which directly use outcome
labels, creating a direct information pathway from test fold to training — and
unsupervised methods, which use only expression variance and create only an
indirect pathway. This distinction matters empirically: our ablation shows the
two conditions produce dramatically different inflation magnitudes (mean +0.22
vs. +0.01) on identical data and models. Existing genomic ML tools
[@zararsiz2017; @davis2007] do not include reproducible ablation frameworks
for quantifying this effect with paired statistical testing across repeated
splits.

A second unmet need is tooling to investigate label construct validity. TCGA-OV
lacks a direct platinum-response label; researchers use OS-threshold surrogates
without empirically verifying how well they capture the intended clinical
construct. The software's `label_investigation` module provides a reproducible
framework for this check, applicable to any TCGA cohort with partial clinical
response data alongside survival annotations.

# Architecture

The software is organised into eight source modules under `src/`: `data_loader`
(I/O), `preprocessing` (survival extraction, platinum-patient identification,
censoring-aware label assignment), `features` (train-only variance selection,
z-score scaling), `models` (classifier factories, CV utilities), `evaluation`
(metrics, results tables), `visualization` (seven figure types), `ablation`
(leakage conditions, bootstrap CIs, nested CV, paired significance tests), and
`label_investigation` (coverage, distribution, consistency, cross-tabulation,
exact binomial recall CIs).

All parameters are controlled via `config/config.yaml` (gitignored; a
committed template `config/config.template.yaml` is provided). Three CLI entry
points with `--help` (`run.py`, `run_ablation_study.py`,
`investigate_clinical_labels.py`) enable full pipeline reproducibility from a
single command.

# Testing

The package includes 52 unit tests across three modules. All tests use
synthetic data and pass without the TCGA dataset on disk, enabling CI/CD
integration. Three tests are regression tests for bugs that only surfaced on
real TCGA data (NaN values in RSEM matrices, mixed-type gene name indices) but
were not caught by earlier synthetic-data tests — documenting a real gap
between synthetic and real-data coverage.

# Results

On the platinum-treated TCGA-OV cohort (n=214/206/199 at 12/18/24m), Logistic
Regression achieved the highest test-set AUC at the 24-month endpoint
(mean ≈ 0.70 across 30 repeated correct splits). The ablation study confirmed
that unsupervised variance selection introduces negligible leakage while
supervised F-score selection inflates AUC by a mean of +0.22, with SVM
reaching AUC ≈ 1.00 under leaky conditions versus 0.45 under correct conditions
at the 12-month endpoint. The label investigation found that the OS-threshold
proxy had 0/5 recall (95% CI: [0.000, 0.522]) on the 7 clinically confirmed
Progressive Disease patients, consistent with the mechanistic argument that
overall survival and first-line treatment response are genuinely different
clinical constructs.

# Acknowledgements

The author thanks Dr. Christopher Lockhart (George Mason University) for
advising the course project from which this software was developed. TCGA-OV
data were obtained from the cBioPortal for Cancer Genomics [@cerami2012; @gao2013].

# References
