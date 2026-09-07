# Audit Inventory — 2026-09-07 (Part 1 of 3)

Project: `C:\PROJECTS\ovarian-cancer-platinum-response`. See `AUDIT_INVENTORY_2026-09-07.md` for the manifest and Parts 2–3.

---

# SECTION 1: FILE INVENTORY

**Project root (as mounted):** `C:\PROJECTS\ovarian-cancer-platinum-response`
(seen from the Linux shell as `$HOME/mnt/ovarian-cancer-platinum-response`)
**Inventory generated:** 2026-09-07 (read-only `find`/`stat` pass; no script executed)
**Scope:** recursive listing of the project root, excluding `.git/` internals and
`multi_cancer/outputs/_tmp_*_data/` (both noted separately below), and excluding
`.pytest_cache/` (empty pytest cache dir, no files) and `venv/` (Python virtual
environment — summarized separately at the end of this section rather than
enumerated file-by-file, since it is 7,046 third-party package files / ~280MB
and gitignored, not project-authored content).

**Files listed below: 419** (all project-authored/output files outside venv and
the two `_tmp_*_data` staging dirs). Sizes in bytes; timestamps are local
last-modified time, second precision, ISO-8601 (`YYYY-MM-DDTHH:MM:SS`).

Any file over 52,428,800 bytes (50 MB) is flagged **`[>50MB]`**.

---

### (root)

| File | Size (bytes) | Last Modified |
|---|---|---|
| .gitignore | 585 | 2026-07-26T22:17:59 |
| AUDIT_2026-07-20.md | 39845 | 2026-07-20T23:26:34 |
| CHANGELOG.md | 1373 | 2026-06-22T19:41:17 |
| CITATION.cff | 1458 | 2026-06-22T20:30:02 |
| CONTRIBUTING.md | 1415 | 2026-06-22T19:41:17 |
| DIRECTORY_MAP.md | 3051 | 2026-07-26T22:17:07 |
| F1000Research_Draft_Chintala_2026_corrected.docx | 22303 | 2026-06-23T02:41:05 |
| F1000Research_Draft_Chintala_2026_final.docx | 782871 | 2026-06-23T03:26:51 |
| FIXES_APPLIED_2026-07-20.md | 10633 | 2026-08-20T04:23:13 |
| LICENSE | 1138 | 2026-06-22T19:41:17 |
| PLOS_CompBio_Draft_Chintala_v1_redline.docx | 28972 | 2026-08-20T04:17:22 |
| PROJECT_LOG.md | 6639 | 2026-07-26T22:15:37 |
| README.md | 14523 | 2026-07-26T21:56:12 |
| Rplots.pdf | 14359 | 2026-08-20T04:27:39 |
| diagnose_features.py | 8517 | 2026-06-23T01:42:07 |
| figure1_pipeline.py | 10635 | 2026-06-23T02:34:17 |
| figure2_ablation.py | 6607 | 2026-06-23T02:34:39 |
| figure3_validation.py | 5390 | 2026-06-23T02:34:34 |
| investigate_clinical_labels.py | 7554 | 2026-06-18T04:28:24 |
| paper.bib | 3668 | 2026-06-22T19:41:17 |
| paper.md | 5741 | 2026-06-22T20:56:21 |
| pyproject.toml | 2003 | 2026-06-22T19:41:17 |
| requirements.txt | 2007 | 2026-08-20T04:18:19 |
| rerun_log.txt | 5360 | 2026-08-20T03:51:05 |
| rerun_log_R.txt | 34078 | 2026-08-20T04:01:02 |
| rerun_log_R2.txt | 8314 | 2026-08-20T04:03:42 |
| rerun_log_R3.txt | 1858 | 2026-08-20T04:04:40 |
| rerun_log_R4.txt | 8384 | 2026-08-20T04:27:39 |
| run.py | 4754 | 2026-06-18T02:53:28 |
| run_ablation_study.py | 8176 | 2026-06-18T03:41:24 |
| validate_external.py | 9737 | 2026-06-22T23:21:53 |

### archive

| File | Size (bytes) | Last Modified |
|---|---|---|
| archive/F1000Research_Draft_Chintala_2026.docx | 22164 | 2026-06-23T02:19:38 |
| archive/PROJECT_LOG_2026-06-22.md | 10374 | 2026-06-23T02:44:57 |

### cellularity

| File | Size (bytes) | Last Modified |
|---|---|---|
| cellularity/cox_hazard_ratios_purity.csv | 467 | 2026-07-02T20:06:46 |
| cellularity/enrichment_corrected_all.csv | 729272 | 2026-07-02T20:13:36 |
| cellularity/enrichment_corrected_significant.csv | 198888 | 2026-07-02T20:13:36 |
| cellularity/estimate_score.gct | 16257 | 2026-07-02T20:03:22 |
| cellularity/estimate_scores.csv | 24192 | 2026-07-02T20:03:22 |
| cellularity/genes_added_after_purity_correction.csv | 73 | 2026-07-02T20:13:27 |
| cellularity/genes_dropped_after_purity_correction.csv | 67 | 2026-07-02T20:13:27 |
| cellularity/tcga_ov_platinum_expr.gct **[>50MB]** | 77690378 | 2026-07-02T19:58:53 |
| cellularity/tcga_ov_platinum_expr_filtered.gct | 41097633 | 2026-07-02T20:03:09 |

### config

| File | Size (bytes) | Last Modified |
|---|---|---|
| config/config.template.yaml | 2650 | 2026-06-22T19:41:17 |
| config/config.yaml | 1082 | 2026-07-26T21:56:18 |

### data

| File | Size (bytes) | Last Modified |
|---|---|---|
| data/README.md | 1417 | 2026-06-18T02:53:28 |

### data/external

| File | Size (bytes) | Last Modified |
|---|---|---|
| data/external/.gitkeep | 0 | 2026-06-23T01:43:41 |
| data/external/GSE63885_expr_gene.csv | 20482563 | 2026-06-22T22:11:11 |
| data/external/GSE63885_expr_raw.csv **[>50MB]** | 66299758 | 2026-06-22T22:01:11 |
| data/external/GSE63885_meta_clean.csv | 22651 | 2026-06-22T22:06:19 |
| data/external/GSE63885_meta_raw.csv | 239728 | 2026-06-22T22:01:11 |
| data/external/GSE63885_plat_fix.csv | 3080 | 2026-06-22T22:08:20 |
| data/external/GSE63885_series_matrix.txt **[>50MB]** | 66608488 | 2026-06-22T22:00:37 |
| data/external/GSE63885_series_matrix.txt.gz | 30104516 | 2026-06-22T22:00:36 |
| data/external/GSE9891_clinical_anns.csv | 11772 | 2026-06-22T22:08:19 |
| data/external/GSE9891_expr_raw.csv **[>50MB]** | 123952178 | 2026-06-22T22:01:28 |
| data/external/GSE9891_meta_clean.csv | 16684 | 2026-06-22T22:06:19 |
| data/external/GSE9891_meta_raw.csv | 388834 | 2026-06-22T22:01:28 |
| data/external/GSE9891_series_matrix.txt **[>50MB]** | 124422871 | 2026-06-22T22:00:40 |
| data/external/GSE9891_series_matrix.txt.gz | 51377752 | 2026-06-22T22:00:39 |
| data/external/harmonised_expression.csv | 22658000 | 2026-08-20T04:03:31 |
| data/external/harmonised_metadata.csv | 21507 | 2026-08-20T04:03:38 |
| data/external/tcga_corrected_expression.csv **[>50MB]** | 84680032 | 2026-08-20T04:03:38 |

### enhancement5

| File | Size (bytes) | Last Modified |
|---|---|---|
| enhancement5/enhancement5_expression_cox.R | 26402 | 2026-08-20T03:52:04 |
| enhancement5/repeat_level_paired_tests.R | 5061 | 2026-07-16T16:31:15 |

### enhancement5/outputs

| File | Size (bytes) | Last Modified |
|---|---|---|
| enhancement5/outputs/alpha_selection_summary.csv | 893 | 2026-08-20T04:00:38 |
| enhancement5/outputs/cv_results_cohortA_n235.csv | 2201 | 2026-08-20T04:00:38 |
| enhancement5/outputs/cv_results_cohortB_n163.csv | 2142 | 2026-08-20T04:00:38 |
| enhancement5/outputs/cv_summary.csv | 550 | 2026-08-20T04:00:38 |
| enhancement5/outputs/emt_ecm_overlap.csv | 2862 | 2026-08-20T04:01:02 |
| enhancement5/outputs/final_model_alpha.csv | 188 | 2026-08-20T04:01:02 |
| enhancement5/outputs/final_model_genes_cohortA_lambda1se.csv | 37 | 2026-08-20T04:01:02 |
| enhancement5/outputs/final_model_genes_cohortA_lambdamin.csv | 273 | 2026-08-20T04:01:02 |
| enhancement5/outputs/final_model_genes_cohortB_lambda1se.csv | 6495 | 2026-08-20T04:01:02 |
| enhancement5/outputs/final_model_genes_cohortB_lambdamin.csv | 9265 | 2026-08-20T04:01:02 |
| enhancement5/outputs/repeat_level_paired_tests.csv | 563 | 2026-07-16T16:32:17 |

### figures

| File | Size (bytes) | Last Modified |
|---|---|---|
| figures/figure1_pipeline.png | 445734 | 2026-06-23T02:40:24 |
| figures/figure1_pipeline.py | 10635 | 2026-06-23T02:40:21 |
| figures/figure2_ablation.png | 162466 | 2026-06-23T02:40:26 |
| figures/figure2_ablation.py | 6607 | 2026-06-23T02:40:21 |
| figures/figure3_validation.png | 243113 | 2026-06-23T02:40:27 |
| figures/figure3_validation.py | 5390 | 2026-06-23T02:40:21 |

### fixes

| File | Size (bytes) | Last Modified |
|---|---|---|
| fixes/manuscript_changelist.md | 7041 | 2026-08-20T04:18:00 |
| fixes/phase1_provenance.md | 7611 | 2026-07-21T00:12:33 |
| fixes/phase1_rerun_clean_auc.py | 6965 | 2026-07-21T00:09:49 |
| fixes/phase4_corrected_values.csv | 1668 | 2026-07-26T21:55:44 |
| fixes/run_windows_pass.ps1 | 3088 | 2026-07-26T23:16:08 |

### fixes/.phase1_ckpt

| File | Size (bytes) | Last Modified |
|---|---|---|
| fixes/.phase1_ckpt/thr_12.json | 7599 | 2026-07-21T00:10:10 |
| fixes/.phase1_ckpt/thr_18.json | 7529 | 2026-07-21T00:10:37 |
| fixes/.phase1_ckpt/thr_24.json | 7605 | 2026-07-21T00:10:58 |

### hrd

| File | Size (bytes) | Last Modified |
|---|---|---|
| hrd/brca_cox_summary.csv | 156 | 2026-08-20T03:52:45 |
| hrd/brca_status.csv | 9063 | 2026-07-02T21:27:16 |
| hrd/cox_hazard_ratios_brca.csv | 448 | 2026-08-20T03:52:45 |
| hrd/hrd_gene_crossref.csv | 622 | 2026-07-02T21:30:33 |

### multi_cancer

| File | Size (bytes) | Last Modified |
|---|---|---|
| multi_cancer/check_rsem_headers.py | 1524 | 2026-06-26T00:29:43 |
| multi_cancer/compare_ablation_results.py | 5359 | 2026-06-26T02:11:14 |
| multi_cancer/diagnose_coadread_ids.py | 3514 | 2026-06-26T00:18:37 |
| multi_cancer/diagnose_cohorts.py | 5316 | 2026-06-25T23:46:38 |
| multi_cancer/download_multi_cancer.ps1 | 3534 | 2026-06-25T23:03:46 |
| multi_cancer/run_multi_cancer_ablation.py | 8352 | 2026-06-26T02:01:59 |

### multi_cancer/outputs/BRCA

| File | Size (bytes) | Last Modified |
|---|---|---|
| multi_cancer/outputs/BRCA/ablation_run.log | 1810 | 2026-06-25T23:42:23 |

(BRCA/figures, BRCA/models, BRCA/results exist as empty subdirectories — no files.)

### multi_cancer/outputs/COADREAD

| File | Size (bytes) | Last Modified |
|---|---|---|
| multi_cancer/outputs/COADREAD/ablation_run.log | 1301560 | 2026-06-26T02:08:53 |
| multi_cancer/outputs/COADREAD/figures/fig8_leakage_ablation.png | 265227 | 2026-06-26T02:07:12 |
| multi_cancer/outputs/COADREAD/figures/fig9_supervised_leakage_ablation.png | 139409 | 2026-06-26T02:08:22 |
| multi_cancer/outputs/COADREAD/results/ablation_leakage_raw.csv | 32905 | 2026-06-26T02:07:11 |
| multi_cancer/outputs/COADREAD/results/ablation_leakage_significance.csv | 1012 | 2026-06-26T02:07:11 |
| multi_cancer/outputs/COADREAD/results/ablation_leakage_summary.csv | 622 | 2026-06-26T02:07:11 |
| multi_cancer/outputs/COADREAD/results/ablation_split_variance_raw.csv | 9258 | 2026-06-26T02:08:53 |
| multi_cancer/outputs/COADREAD/results/ablation_split_variance_summary.csv | 429 | 2026-06-26T02:08:53 |
| multi_cancer/outputs/COADREAD/results/ablation_supervised_leakage_raw.csv | 36458 | 2026-06-26T02:08:22 |
| multi_cancer/outputs/COADREAD/results/ablation_supervised_leakage_significance.csv | 1108 | 2026-06-26T02:08:22 |
| multi_cancer/outputs/COADREAD/results/ablation_supervised_leakage_summary.csv | 656 | 2026-06-26T02:08:22 |

### multi_cancer/outputs/LUAD

| File | Size (bytes) | Last Modified |
|---|---|---|
| multi_cancer/outputs/LUAD/ablation_run.log | 1043212 | 2026-06-26T02:05:07 |
| multi_cancer/outputs/LUAD/figures/fig8_leakage_ablation.png | 271911 | 2026-06-26T02:03:25 |
| multi_cancer/outputs/LUAD/figures/fig9_supervised_leakage_ablation.png | 138518 | 2026-06-26T02:04:36 |
| multi_cancer/outputs/LUAD/results/ablation_leakage_raw.csv | 34610 | 2026-06-26T02:03:25 |
| multi_cancer/outputs/LUAD/results/ablation_leakage_significance.csv | 1012 | 2026-06-26T02:03:25 |
| multi_cancer/outputs/LUAD/results/ablation_leakage_summary.csv | 621 | 2026-06-26T02:03:25 |
| multi_cancer/outputs/LUAD/results/ablation_split_variance_raw.csv | 10148 | 2026-06-26T02:05:07 |
| multi_cancer/outputs/LUAD/results/ablation_split_variance_summary.csv | 429 | 2026-06-26T02:05:07 |
| multi_cancer/outputs/LUAD/results/ablation_supervised_leakage_raw.csv | 38740 | 2026-06-26T02:04:36 |
| multi_cancer/outputs/LUAD/results/ablation_supervised_leakage_significance.csv | 1109 | 2026-06-26T02:04:36 |
| multi_cancer/outputs/LUAD/results/ablation_supervised_leakage_summary.csv | 656 | 2026-06-26T02:04:36 |

### multi_cancer/outputs/_tmp_COADREAD_data/ and multi_cancer/outputs/_tmp_LUAD_data/ — EXCLUDED FROM ITEMIZED LISTING PER SCOPE

Per the excluded-scope rule (`_tmp_*_data/` directories), these two staging
directories are **not itemized file-by-file** above. Summary instead:

| Directory | File count | Total size | Largest single file | Currently git-tracked? |
|---|---|---|---|---|
| `multi_cancer/outputs/_tmp_COADREAD_data/` | 39 | ≈ 1.73 GB | `data_methylation_hm450.txt` — 1,394,611,705 B **[>50MB]** | No (untracked; matched by `.gitignore` rule `multi_cancer/outputs/_tmp_*/`) |
| `multi_cancer/outputs/_tmp_LUAD_data/` | 39 | ≈ 2.44 GB | `data_methylation_hm450.txt` — 1,665,366,144 B **[>50MB]** | No (untracked; matched by `.gitignore` rule `multi_cancer/outputs/_tmp_*/`) |

Both directories are raw cBioPortal/TCGA bulk-download staging data (CNA,
methylation, RSEM, mutations, RPPA, clinical/timeline TXT files plus a
`LICENSE`/`README.md` from the source repo). Each contains 7 files individually
over 50MB, several in the 75–342MB range, plus one ~1.4–1.7GB methylation
matrix each. **Important caveat (see Section 4e / git-history note below): although
untracked in the current working tree, `git log` shows these exact paths were
`git add`-ed and committed in earlier commit(s) before the `.gitignore` rule was
added — the large blobs are still present in `.git` history/pack.**

### multi_cancer/outputs/comparison

| File | Size (bytes) | Last Modified |
|---|---|---|
| multi_cancer/outputs/comparison/all_cancers_ablation_raw.csv | 2095 | 2026-06-26T02:11:20 |
| multi_cancer/outputs/comparison/cross_cancer_leakage_by_model.csv | 454 | 2026-06-26T02:11:20 |
| multi_cancer/outputs/comparison/cross_cancer_leakage_summary.csv | 235 | 2026-06-26T02:11:20 |

### notebooks

| File | Size (bytes) | Last Modified |
|---|---|---|
| notebooks/analysis.ipynb | 15452 | 2026-06-18T02:53:28 |

### outputs/figures

| File | Size (bytes) | Last Modified |
|---|---|---|
| outputs/figures/fig1_class_distribution.png | 131337 | 2026-06-18T03:17:24 |
| outputs/figures/fig2_roc_12m.png | 175160 | 2026-06-18T03:17:24 |
| outputs/figures/fig2_roc_18m.png | 174303 | 2026-06-18T03:17:24 |
| outputs/figures/fig2_roc_24m.png | 169311 | 2026-06-18T03:17:24 |
| outputs/figures/fig3_confusion_12m.png | 118207 | 2026-06-18T03:17:25 |
| outputs/figures/fig3_confusion_18m.png | 135527 | 2026-06-18T03:17:25 |
| outputs/figures/fig3_confusion_24m.png | 132277 | 2026-06-18T03:17:25 |
| outputs/figures/fig4_cv_auc_heatmap.png | 115884 | 2026-06-18T03:17:25 |
| outputs/figures/fig5_feature_importance_12m.png | 212931 | 2026-06-18T03:17:26 |
| outputs/figures/fig5_feature_importance_18m.png | 209358 | 2026-06-18T03:17:26 |
| outputs/figures/fig5_feature_importance_24m.png | 202822 | 2026-06-18T03:17:27 |
| outputs/figures/fig6_calibration_curves.png | 159372 | 2026-06-18T03:17:27 |
| outputs/figures/fig8_leakage_ablation.png | 290469 | 2026-06-18T03:56:54 |
| outputs/figures/fig9_supervised_leakage_ablation.png | 151249 | 2026-06-18T03:56:54 |
| outputs/figures/fig_external_validation_roc_clinical.png | 242940 | 2026-06-22T23:22:02 |
| outputs/figures/fig_external_validation_roc_dfs.png | 251896 | 2026-06-22T23:22:02 |
| outputs/figures/figure1_pipeline.png | 445734 | 2026-06-23T02:34:55 |
| outputs/figures/figure2_ablation.png | 162466 | 2026-06-23T02:34:59 |
| outputs/figures/figure3_validation.png | 243113 | 2026-06-23T02:35:05 |

### outputs/models

| File | Size (bytes) | Last Modified |
|---|---|---|
| outputs/models/Logistic_Regression_12m.pkl | 4732 | 2026-06-18T03:17:17 |
| outputs/models/Logistic_Regression_18m.pkl | 4732 | 2026-06-18T03:17:20 |
| outputs/models/Logistic_Regression_24m.pkl | 4732 | 2026-06-18T03:17:22 |
| outputs/models/Random_Forest_12m.pkl | 452810 | 2026-06-18T03:17:19 |
| outputs/models/Random_Forest_18m.pkl | 601009 | 2026-06-18T03:17:20 |
| outputs/models/Random_Forest_24m.pkl | 771819 | 2026-06-18T03:17:22 |
| outputs/models/SVM_12m.pkl | 451500 | 2026-06-18T03:17:20 |
| outputs/models/SVM_18m.pkl | 572100 | 2026-06-18T03:17:22 |
| outputs/models/SVM_24m.pkl | 584160 | 2026-06-18T03:17:23 |

### outputs/results

| File | Size (bytes) | Last Modified |
|---|---|---|
| outputs/results/ablation_leakage_raw.csv | 34390 | 2026-06-18T04:33:27 |
| outputs/results/ablation_leakage_significance.csv | 996 | 2026-06-18T04:33:27 |
| outputs/results/ablation_leakage_summary.csv | 614 | 2026-06-18T04:33:27 |
| outputs/results/ablation_split_variance_raw.csv | 10068 | 2026-06-18T03:56:54 |
| outputs/results/ablation_split_variance_summary.csv | 422 | 2026-06-18T03:26:58 |
| outputs/results/ablation_supervised_leakage_raw.csv | 38164 | 2026-06-18T04:33:27 |
| outputs/results/ablation_supervised_leakage_significance.csv | 1112 | 2026-06-18T04:33:27 |
| outputs/results/ablation_supervised_leakage_summary.csv | 645 | 2026-06-18T04:33:27 |
| outputs/results/clean_auc_table.csv | 473 | 2026-08-20T03:51:03 |
| outputs/results/clean_auc_table_raw.csv | 10341 | 2026-08-20T03:51:03 |
| outputs/results/external_validation_results.csv | 815 | 2026-06-22T23:22:02 |
| outputs/results/label_investigation_candidate_labels.csv | 2585 | 2026-06-22T19:28:41 |
| outputs/results/label_investigation_coverage_sample.csv | 328 | 2026-06-22T19:28:41 |
| outputs/results/label_investigation_coverage_timeline.csv | 267 | 2026-06-22T19:28:41 |
| outputs/results/label_investigation_crosstab_vs_os.csv | 107 | 2026-06-22T19:28:42 |
| outputs/results/label_investigation_recall_on_confirmed.csv | 380 | 2026-07-26T21:54:21 |
| outputs/results/model_performance_summary.csv | 525 | 2026-06-18T03:17:23 |

### phase2

| File | Size (bytes) | Last Modified |
|---|---|---|
| phase2/phase2_00_diag.R | 730 | 2026-06-25T22:22:02 |
| phase2/phase2_01_inspect_clinical.R | 6128 | 2026-06-25T22:24:55 |
| phase2/phase2_02_cox_model.R | 9506 | 2026-08-20T04:12:45 |
| phase2/phase2_03_rf_feature_importance.py | 11838 | 2026-06-25T22:28:39 |
| phase2/phase2_03b_recover_gene_names.py | 9181 | 2026-06-25T22:31:12 |
| phase2/phase2_03c_permutation_shap_importance.py | 18900 | 2026-07-13T00:05:55 |
| phase2/phase2_03d_cv_permutation_shap_importance.py | 18728 | 2026-07-13T01:18:24 |
| phase2/phase2_04_pathway_enrichment.py | 7422 | 2026-06-25T22:32:52 |
| phase2/phase2_04b_pathway_enrichment_shap.py | 13475 | 2026-07-13T22:38:09 |

### phase2/outputs

| File | Size (bytes) | Last Modified |
|---|---|---|
| phase2/outputs/comparison_spearman_correlations.csv | 231 | 2026-07-13T00:10:21 |
| phase2/outputs/comparison_topN_overlap.csv | 9200 | 2026-07-13T00:10:21 |
| phase2/outputs/cox_hazard_ratios.csv | 146 | 2026-08-20T04:27:37 |
| phase2/outputs/cox_patients_with_risk.csv | 34684 | 2026-08-20T04:27:39 |
| phase2/outputs/cox_ph_test.csv | 161 | 2026-08-20T04:27:37 |
| phase2/outputs/cox_summary_stats.csv | 198 | 2026-08-20T04:27:39 |
| phase2/outputs/cv_comparison_spearman_with12m.csv | 217 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_comparison_spearman_without12m.csv | 215 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_comparison_topN_overlap_with12m.csv | 4010 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_comparison_topN_overlap_without12m.csv | 4272 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_emt_ecm_gene_tracking.csv | 1636 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_fold_auc_stats_by_threshold.csv | 410 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_fold_auc_summary.csv | 2818 | 2026-07-13T01:52:38 |
| phase2/outputs/cv_mdi_importances_full.csv | 93329 | 2026-07-13T01:52:38 |
| phase2/outputs/cv_permutation_importances_full.csv | 93837 | 2026-07-13T01:52:38 |
| phase2/outputs/cv_shap_importances_full.csv | 94124 | 2026-07-13T01:52:38 |
| phase2/outputs/cv_top100_genes_mdi_with12m.txt | 695 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top100_genes_mdi_without12m.txt | 687 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top100_genes_permutation_with12m.txt | 703 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top100_genes_permutation_without12m.txt | 684 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top100_genes_shap_with12m.txt | 689 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top100_genes_shap_without12m.txt | 681 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top200_genes_mdi_with12m.txt | 1381 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top200_genes_mdi_without12m.txt | 1388 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top200_genes_permutation_with12m.txt | 1399 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top200_genes_permutation_without12m.txt | 1395 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top200_genes_shap_with12m.txt | 1384 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top200_genes_shap_without12m.txt | 1385 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top500_genes_mdi_with12m.txt | 3491 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top500_genes_mdi_without12m.txt | 3485 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top500_genes_permutation_with12m.txt | 3484 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top500_genes_permutation_without12m.txt | 3490 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top500_genes_shap_with12m.txt | 3474 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top500_genes_shap_without12m.txt | 3484 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top50_genes_mdi_with12m.txt | 334 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top50_genes_mdi_without12m.txt | 332 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top50_genes_permutation_with12m.txt | 346 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top50_genes_permutation_without12m.txt | 336 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top50_genes_shap_with12m.txt | 331 | 2026-07-13T01:52:39 |
| phase2/outputs/cv_top50_genes_shap_without12m.txt | 330 | 2026-07-13T01:52:39 |
| phase2/outputs/enrichment_results_full.csv | 1039552 | 2026-06-25T22:33:16 |
| phase2/outputs/enrichment_results_significant.csv | 121210 | 2026-06-25T22:33:16 |
| phase2/outputs/enrichment_shap_with12m_full.csv | 2191262 | 2026-07-13T22:40:07 |
| phase2/outputs/enrichment_shap_with12m_significant.csv | 363871 | 2026-07-13T22:40:07 |
| phase2/outputs/enrichment_shap_without12m_full.csv | 2267956 | 2026-07-13T22:40:07 |
| phase2/outputs/enrichment_shap_without12m_significant.csv | 387726 | 2026-07-13T22:40:08 |
| phase2/outputs/km_risk_groups.png | 1337 | 2026-08-20T04:27:39 |
| phase2/outputs/permutation_importances_Random_Forest_12m.csv | 21161 | 2026-07-13T00:07:56 |
| phase2/outputs/permutation_importances_Random_Forest_18m.csv | 26350 | 2026-07-13T00:09:09 |
| phase2/outputs/permutation_importances_Random_Forest_24m.csv | 26609 | 2026-07-13T00:10:21 |
| phase2/outputs/permutation_importances_full.csv | 29612 | 2026-07-13T00:10:21 |
| phase2/outputs/phase2_03c_gene_set_diagnostic.csv | 195 | 2026-07-13T00:06:37 |
| phase2/outputs/phase2_03c_reconstruction_verification.csv | 200 | 2026-07-13T00:06:37 |
| phase2/outputs/rf_feature_importances_full.csv | 30063 | 2026-06-25T22:29:45 |
| phase2/outputs/rf_feature_importances_named.csv | 36410 | 2026-06-25T22:31:24 |
| phase2/outputs/rf_importances_Random_Forest_12m.csv | 16890 | 2026-06-25T22:29:45 |
| phase2/outputs/rf_importances_Random_Forest_18m.csv | 17184 | 2026-06-25T22:29:45 |
| phase2/outputs/rf_importances_Random_Forest_24m.csv | 17220 | 2026-06-25T22:29:45 |
| phase2/outputs/rf_importances_named_Random_Forest_12m.csv | 15878 | 2026-06-25T22:31:24 |
| phase2/outputs/rf_importances_named_Random_Forest_18m.csv | 16172 | 2026-06-25T22:31:24 |
| phase2/outputs/rf_importances_named_Random_Forest_24m.csv | 16208 | 2026-06-25T22:31:24 |
| phase2/outputs/shap_importances_Random_Forest_12m.csv | 15663 | 2026-07-13T00:10:21 |
| phase2/outputs/shap_importances_Random_Forest_18m.csv | 16257 | 2026-07-13T00:10:21 |
| phase2/outputs/shap_importances_Random_Forest_24m.csv | 16328 | 2026-07-13T00:10:21 |
| phase2/outputs/shap_importances_full.csv | 29902 | 2026-07-13T00:10:21 |
| phase2/outputs/shap_theme_comparison.csv | 5464 | 2026-07-13T22:40:08 |
| phase2/outputs/shap_theme_robustness_verdict.csv | 274 | 2026-07-13T22:40:08 |
| phase2/outputs/top100_genes.txt | 1273 | 2026-06-25T22:29:45 |
| phase2/outputs/top100_genes_named.txt | 695 | 2026-06-25T22:31:24 |
| phase2/outputs/top100_genes_permutation.txt | 688 | 2026-07-13T00:10:21 |
| phase2/outputs/top100_genes_shap.txt | 684 | 2026-07-13T00:10:21 |
| phase2/outputs/top200_genes.txt | 2555 | 2026-06-25T22:29:45 |
| phase2/outputs/top200_genes_named.txt | 1385 | 2026-06-25T22:31:24 |
| phase2/outputs/top200_genes_permutation.txt | 1377 | 2026-07-13T00:10:21 |
| phase2/outputs/top200_genes_shap.txt | 1378 | 2026-07-13T00:10:21 |
| phase2/outputs/top500_genes.txt | 6388 | 2026-06-25T22:29:45 |
| phase2/outputs/top500_genes_named.txt | 3479 | 2026-06-25T22:31:24 |
| phase2/outputs/top500_genes_permutation.txt | 3498 | 2026-07-13T00:10:21 |
| phase2/outputs/top500_genes_shap.txt | 3482 | 2026-07-13T00:10:21 |
| phase2/outputs/top500_genes_variance_order.txt | 3479 | 2026-06-25T22:31:24 |
| phase2/outputs/top50_genes.txt | 637 | 2026-06-25T22:29:45 |
| phase2/outputs/top50_genes_named.txt | 346 | 2026-06-25T22:31:24 |
| phase2/outputs/top50_genes_permutation.txt | 335 | 2026-07-13T00:10:21 |
| phase2/outputs/top50_genes_shap.txt | 335 | 2026-07-13T00:10:21 |

### src

| File | Size (bytes) | Last Modified |
|---|---|---|
| src/03_pathway_enrichment_corrected.py | 9591 | 2026-07-02T20:10:50 |
| src/__init__.py | 300 | 2026-06-18T02:53:28 |
| src/ablation.py | 21552 | 2026-06-18T04:28:24 |
| src/data_loader.py | 4018 | 2026-06-18T03:41:24 |
| src/evaluation.py | 4646 | 2026-06-18T02:53:28 |
| src/features.py | 2272 | 2026-06-18T02:53:28 |
| src/label_investigation.py | 13972 | 2026-07-26T21:54:01 |
| src/models.py | 5594 | 2026-06-18T02:53:28 |
| src/pipeline.py | 10797 | 2026-06-18T02:53:28 |
| src/preprocessing.py | 10507 | 2026-06-18T04:28:24 |
| src/py.typed | 0 | 2026-06-22T19:41:17 |
| src/visualization.py | 19134 | 2026-06-18T02:53:28 |

### src/__pycache__  (compiled bytecode cache — not source; listed for completeness)

| File | Size (bytes) | Last Modified |
|---|---|---|
| src/__pycache__/__init__.cpython-310.pyc | 489 | 2026-06-22T17:48:41 |
| src/__pycache__/__init__.cpython-314.pyc | 472 | 2026-06-25T23:41:06 |
| src/__pycache__/ablation.cpython-310.pyc | 15919 | 2026-06-22T17:48:41 |
| src/__pycache__/ablation.cpython-314.pyc | 23888 | 2026-06-25T23:41:06 |
| src/__pycache__/data_loader.cpython-310.pyc | 3836 | 2026-06-22T17:48:55 |
| src/__pycache__/data_loader.cpython-314.pyc | 5605 | 2026-06-25T23:41:08 |
| src/__pycache__/features.cpython-314.pyc | 3178 | 2026-07-13T00:06:32 |
| src/__pycache__/label_investigation.cpython-310.pyc | 12354 | 2026-07-26T21:54:18 |
| src/__pycache__/models.cpython-310.pyc | 4633 | 2026-06-22T17:48:41 |
| src/__pycache__/models.cpython-314.pyc | 7396 | 2026-06-25T23:41:07 |
| src/__pycache__/preprocessing.cpython-310.pyc | 7609 | 2026-06-22T17:48:41 |
| src/__pycache__/preprocessing.cpython-314.pyc | 11413 | 2026-06-25T23:41:08 |
| src/__pycache__/visualization.cpython-314.pyc | 22093 | 2026-06-25T23:41:08 |

### src/cellularity

| File | Size (bytes) | Last Modified |
|---|---|---|
| src/cellularity/00_install_estimate.R | 2023 | 2026-07-02T19:53:24 |
| src/cellularity/01_run_estimate.R | 6597 | 2026-07-02T20:02:40 |
| src/cellularity/02_cox_model_with_purity.R | 5633 | 2026-07-02T20:06:41 |
| src/cellularity/03_pathway_enrichment_corrected.py | 9591 | 2026-07-02T20:13:13 |

### src/hrd

| File | Size (bytes) | Last Modified |
|---|---|---|
| src/hrd/00_inspect_hrd_data.R | 4373 | 2026-07-02T20:24:19 |
| src/hrd/01_extract_brca_status.R | 4840 | 2026-07-02T21:27:04 |
| src/hrd/02_cox_model_with_brca.R | 5335 | 2026-08-20T03:52:04 |
| src/hrd/03_hrd_gene_crossref.py | 4640 | 2026-07-02T21:30:22 |
| src/hrd/Literature_Review_Lockhart.docx | 18853 | 2026-07-04T23:12:39 |

### tests

| File | Size (bytes) | Last Modified |
|---|---|---|
| tests/__init__.py | 0 | 2026-06-22T19:41:17 |
| tests/test_ablation.py | 13537 | 2026-06-18T04:28:24 |
| tests/test_label_investigation.py | 11213 | 2026-06-18T04:28:24 |
| tests/test_preprocessing.py | 8581 | 2026-06-18T04:28:24 |

### tests/__pycache__  (compiled bytecode / pytest cache — not source; listed for completeness)

| File | Size (bytes) | Last Modified |
|---|---|---|
| tests/__pycache__/test_ablation.cpython-310-pytest-9.1.0.pyc | 17302 | 2026-06-22T17:48:39 |
| tests/__pycache__/test_label_investigation.cpython-310-pytest-9.1.0.pyc | 12661 | 2026-06-22T17:48:41 |
| tests/__pycache__/test_preprocessing.cpython-310-pytest-9.1.0.pyc | 10869 | 2026-06-22T17:48:41 |

### validation

| File | Size (bytes) | Last Modified |
|---|---|---|
| validation/01_download_and_parse.R | 5146 | 2026-06-22T21:59:42 |
| validation/02_parse_metadata.R | 6140 | 2026-06-22T22:05:59 |
| validation/03_fix_labels.R | 3584 | 2026-06-22T22:08:14 |
| validation/04_probe_mapping.R | 4757 | 2026-06-22T22:10:02 |
| validation/05_batch_correction.R | 11638 | 2026-08-20T04:12:24 |
| validation/inspect_metadata.R | 478 | 2026-06-22T22:03:56 |
| validation/investigate_labels.R | 2713 | 2026-06-22T22:07:09 |

### validation/outputs

| File | Size (bytes) | Last Modified |
|---|---|---|
| validation/outputs/combat_diagnostics.csv | 310 | 2026-08-20T04:03:29 |

---

## Excluded from itemization (noted separately, not part of the 419-file count above)

### `.git/` internals
`.git/` is **2.0 GB** on disk (packfiles + objects). Not itemized — internal
git object store, not source content. See the git-history finding below.

### `.pytest_cache/` (4 files, tool-generated, gitignored by pytest itself)
`.pytest_cache/.gitignore`, `.pytest_cache/CACHEDIR.TAG`, `.pytest_cache/README.md`
(a pytest-authored boilerplate README, not a project doc), `.pytest_cache/v/cache/nodeids`.
Trivial size; excluded as non-project tool cache.

### `venv/` — Python virtual environment (gitignored, 7,046 files, ≈280 MB)
Top level: `venv/bin`, `venv/include`, `venv/lib`, `venv/lib64`, `venv/pyvenv.cfg`,
`venv/share` — standard third-party dependency tree (site-packages), not
project-authored code or data. Not itemized file-by-file; flagged here for
completeness of the audit's directory census. No single file within it was
checked individually against the 50MB threshold, but the whole tree (280MB)
is well under any single-file concern, and it is correctly gitignored (`venv/`,
`.venv/` in `.gitignore`), so it poses no git-hygiene risk.

### `multi_cancer/outputs/_tmp_COADREAD_data/` and `_tmp_LUAD_data/`
Excluded from itemization per the stated scope (`_tmp_*_data/`); summarized in
the table above within the `multi_cancer/outputs/` section.

---

## Git-history finding (relevant to file inventory / repo hygiene)

`.git` is unexpectedly large (2.0 GB) relative to the 232 files currently
tracked by git. Investigation (`git log --all --diff-filter=A --name-only`,
`git cat-file --batch-check` over `git rev-list --objects --all`) shows that
although `multi_cancer/outputs/_tmp_COADREAD_data/` and `_tmp_LUAD_data/` are
**not tracked in the current working tree** (correctly matched by the
`multi_cancer/outputs/_tmp_*/` gitignore rule), those exact paths **were
`git add`-ed and committed in earlier commit(s)** before that gitignore rule
existed, and a later commit removed them from the tree without ever purging
the old blobs from history. The largest blobs still sitting in `.git`'s
object store:

| Size (bytes) | Path (as committed) |
|---|---|
| 1,665,366,144 | multi_cancer/outputs/_tmp_LUAD_data/data_methylation_hm450.txt |
| 1,394,611,705 | multi_cancer/outputs/_tmp_COADREAD_data/data_methylation_hm450.txt |
| 342,402,448 | multi_cancer/outputs/_tmp_COADREAD_data/data_mutations.txt |
| 234,036,793 | multi_cancer/outputs/_tmp_LUAD_data/data_methylation_hm27_hm450_merged.txt |
| 232,136,490 | multi_cancer/outputs/_tmp_LUAD_data/data_mutations.txt |
| 159,807,870 | multi_cancer/outputs/_tmp_COADREAD_data/data_methylation_hm27_hm450_merged.txt |
| 103,891,871 | multi_cancer/outputs/_tmp_COADREAD_data/data_mrna_seq_v2_rsem.txt |
| 77,690,378 | cellularity/tcga_ov_platinum_expr.gct (currently tracked, still in working tree) |
| 41,097,633 | cellularity/tcga_ov_platinum_expr_filtered.gct (currently tracked, still in working tree) |

(full ranked list runs to ~20 blobs over 25MB; the above is the top of it.)
**Practical implication:** anyone who clones or fetches this repository's full
history downloads these multi-hundred-MB-to-1.6GB blobs regardless of the
current `.gitignore`, since git history is immutable without a rewrite
(`git filter-repo` / BFG). This is a repo-hygiene / potential-bandwidth and
possibly data-provenance concern worth flagging to the project owner —
no history rewrite was performed as part of this read-only audit.

---

# SECTION 2: OUTPUT DATA

Full contents (or head/tail for files >200 rows) of every analysis-output CSV under outputs/results/, outputs/models/, outputs/figures/, phase2/outputs/, cellularity/, hrd/, enhancement5/outputs/, multi_cancer/outputs/ (incl. comparison/, BRCA/COADREAD/LUAD results/), validation/outputs/, and fixes/. Raw inputs under data/external/ are excluded.

## cellularity/ , enhancement5/outputs/ , fixes/ , hrd/

### ./cellularity/cox_hazard_ratios_purity.csv

```csv
"model","term","HR","p_value","c_index"
"baseline_n235","log_tmb",0.896201561211946,0.388915441444927,0.603370537364181
"baseline_n235","aneu",1.02876422280873,0.0195178166720705,0.603370537364181
"purity_corrected_n235","log_tmb",0.880109933730733,0.326647646266622,0.604479266760293
"purity_corrected_n235","aneu",1.02698214106898,0.0321659134465974,0.604479266760293
"purity_corrected_n235","TumorPurity",4.35916464300287,0.526412583235842,0.604479266760293
```

### ./cellularity/enrichment_corrected_all.csv

Total data rows: 4073 (header + 4073 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
library,term,p_value,z_score,combined_score,overlap_genes,adj_p_value
```
FIRST 20 DATA ROWS:
```csv
Reactome_2022,Eukaryotic Translation Elongation R-HSA-156842,1.022780432506075e-97,169.69095816464238,37896.781196034775,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;EEF1B2;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;EEF1A1;EEF1G;EEF1D;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;EEF2;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,1.0749422345638849e-94
Reactome_2022,L13a-mediated Translational Silencing Of Ceruloplasmin Expression R-HSA-156827,6.9138056762584705e-96,104.10160427807487,22810.1864496805,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;PABPC1;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;EIF4B;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;EIF4G1;RPS23,3.633204882873826e-93
GO_Biological_Process_2023,Cytoplasmic Translation (GO:0002181),8.088020602860676e-96,146.5287137105319,32083.602578066446,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS9;RPS7;RPS8;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;UBA52;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,2.1950887916163875e-92
Reactome_2022,Peptide Chain Elongation R-HSA-156902,1.0974284033332321e-93,170.3672839506173,36466.68167438696,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;EEF1A1;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;EEF2;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,3.84465750634409e-91
Reactome_2022,GTP Hydrolysis And Joining Of 60S Ribosomal Subunit R-HSA-72706,2.1280416484642426e-93,96.60697518443997,20614.499832639438,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;EIF4B;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;EIF4G1;RPS23,5.591429431339797e-91
Reactome_2022,Cap-dependent Translation Initiation R-HSA-72737,3.8833092532968175e-92,83.75466284074605,17628.77698748328,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;PABPC1;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;EIF4B;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;EIF4G1;RPS23,8.16271605042991e-90
Reactome_2022,Formation Of A Pool Of Free 40S Subunits R-HSA-72689,7.036694294530272e-91,113.20930232558139,23500.451696741744,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;RPS23,1.2325942839252194e-88
Reactome_2022,Nonsense Mediated Decay (NMD) Independent Of Exon Junction Complex (EJC) R-HSA-975956,5.115582530525208e-90,127.73611111111111,26262.591335072324,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;PABPC1;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;EIF4G1;RPS23,7.680681770831419e-88
Reactome_2022,Eukaryotic Translation Termination R-HSA-72764,5.881651028811798e-87,123.40783410138249,24503.003777512815,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.1816152312812e-85
Reactome_2022,Selenocysteine Synthesis R-HSA-2408557,5.881651028811798e-87,123.40783410138249,24503.003777512815,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.1816152312812e-85
Reactome_2022,Viral mRNA Translation R-HSA-192823,5.881651028811798e-87,123.40783410138249,24503.003777512815,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.1816152312812e-85
Reactome_2022,SRP-dependent Cotranslational Protein Targeting To Membrane R-HSA-1799339,4.6572549362412144e-86,83.37454100367196,16381.754292806174,RPL4;RPL5;RPL30;TRAM1;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;SRP14;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;SSR2;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPN1;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,4.449795398172288e-84
Reactome_2022,Response Of EIF2AK4 (GCN2) To Amino Acid Deficiency R-HSA-9633012,7.40977208084676e-83,92.51785714285714,17496.215076782715,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.489725380808287e-81
Reactome_2022,Nonsense Mediated Decay (NMD) Enhanced By Exon Junction Complex (EJC) R-HSA-975957,1.2348497579179113e-80,69.6026936026936,12806.607337611564,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;PABPC1;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;EIF4G1;RPS23,9.983285350551728e-79
Reactome_2022,Selenoamino Acid Metabolism R-HSA-2408522,4.791483253462815e-78,64.04358508181416,11401.98668416583,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;AHCY;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,3.597034928135299e-76
GO_Biological_Process_2023,Macromolecule Biosynthetic Process (GO:0009059),2.3586353930086278e-76,34.141503046716316,5945.346162391077,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;EEF1B2;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS9;RPS7;RPS8;RPS5;PABPC4;RPL22;RPS6;RPL13A;RPSA;RPS3A;EEF1A1;EEF1G;EEF1D;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;APOE;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;EEF2;RPS25;COL5A1;RPS29;RPL27A;RPS20;FAU;RPS21;EIF4G2;RPS24;EIF4G1;RPS23,3.200668228312708e-73
Reactome_2022,Influenza Infection R-HSA-168255,2.557490540769008e-73,38.42440901594283,6422.627873637293,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;HSP90AA1;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;CANX;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;SLC25A6;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;ISG15;RPL23A;RPS25;RPS29;RPL27A;RPS20;CALR;FAU;RPS21;RPS24;RPS23;HSPA1A,1.7919483722321514e-71
KEGG_2021_Human,Ribosome,1.7247330190609442e-71,36.929587653725584,6017.250485494068,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;UBA52;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,4.4670585193678455e-69
Reactome_2022,Influenza Viral RNA Transcription And Replication R-HSA-168273,1.2413515774162127e-70,42.94985153414714,6913.412361339616,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;HSP90AA1;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,8.154128174152747e-69
GO_Biological_Process_2023,Peptide Biosynthetic Process (GO:0043043),1.7247330190609442e-71,36.929587653725584,6017.250485494068,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS9;RPS7;RPS8;RPS5;PABPC4;RPL22;RPS6;RPL13A;RPSA;RPS3A;EEF1A1;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;EIF4G1;RPS23,1.5603084712438007e-68
```
LAST 20 DATA ROWS:
```csv
Reactome_2022,Factors Involved In Megakaryocyte Development And Platelet Production R-HSA-983231,0.9684122097219359,0.28746381652193276,0.009226854287114401,RNASE1,0.975840107783082
Reactome_2022,G Alpha (Q) Signaling Events R-HSA-416476,0.9705507907542545,0.3689041881812966,0.01102711544697744,APP;ANXA1,0.9770583152133347
GO_Biological_Process_2023,Dephosphorylation (GO:0016311),0.9761377921383013,0.2656545968649628,0.006415962857719506,PPP1CB,0.9783005789746492
GO_Biological_Process_2023,Protein Glycosylation (GO:0006486),0.9761377921383013,0.2656545968649628,0.006415962857719506,TMEM59,0.9783005789746492
Reactome_2022,Sensory Perception R-HSA-9709957,0.9728868977589245,0.5705231229679536,0.015682222560846733,GSN;SCNN1A;ATP2B4;APOA1;MSN;MYH9;APOE;AGRN;HSPG2,0.97847285123888
Reactome_2022,GPCR Ligand Binding R-HSA-500792,0.9740545003658487,0.5118412095589553,0.013455292825866492,C3;APP;PYY;ANXA1;SST;GNAS,0.9787105926238117
GO_Biological_Process_2023,Protein Polyubiquitination (GO:0000209),0.9782574479403496,0.3455966724039013,0.007597045807192908,IFI27;CTNNB1,0.9800630172425652
GO_Biological_Process_2023,Cilium Organization (GO:0044782),0.9791849933783344,0.34250275438035327,0.007204440198008911,GSN;FLNA,0.9806302848814759
Reactome_2022,Metabolism Of Steroids R-HSA-8957322,0.9795241339392932,0.25508912561966035,0.005277386596400349,DHCR24,0.983266346485384
GO_Biological_Process_2023,Cilium Assembly (GO:0060271),0.9850186281217579,0.3209351930543752,0.004844428863933912,GSN;FLNA,0.9860318628791201
GO_Biological_Process_2023,Peptidyl-Serine Modification (GO:0018209),0.9853052365984427,0.23483330296957552,0.0034764254719329684,GAS6,0.9860318628791201
Reactome_2022,Chromatin Modifying Enzymes R-HSA-3247509,0.9832769157914805,0.3278197535906337,0.005528514180210618,CCND1;RPS2,0.9860916397870668
GO_Biological_Process_2023,Double-Strand Break Repair (GO:0006302),0.9860366789242562,0.23199692798771196,0.003262277083651256,NUCKS1,0.9864001277554113
Reactome_2022,Transport To Golgi And Subsequent Modification R-HSA-948021,0.9845355521909135,0.23773928224547253,0.003705230815251475,CD59,0.9864126457127265
Reactome_2022,GPCR Downstream Signaling R-HSA-388396,0.9881734953035376,0.5026811970247362,0.005980395243551116,C3;ITGB1;APP;PYY;ANXA1;SST;PPP1R1B;GNAS,0.9891146129181124
Reactome_2022,Signaling By GPCR R-HSA-372790,0.9961178015291767,0.44933920704845814,0.0017478188718143305,C3;ITGB1;APP;PYY;ANXA1;SST;PPP1R1B;GNAS,0.9961178015291767
GO_Biological_Process_2023,Organelle Assembly (GO:0070925),0.9974661099086422,0.24071285140562249,0.0006107139772641407,GSN;FLNA,0.9974661099086422
KEGG_2021_Human,Neuroactive ligand-receptor interaction,0.9918550515506577,0.34220708868596195,0.002798672151920821,C3;PYY;SST,0.9995737679051375
KEGG_2021_Human,Cytokine-cytokine receptor interaction,0.9994575881582693,0.1309148910065028,7.102905238229487e-05,TNFSF10,0.9999837675634693
KEGG_2021_Human,Olfactory transduction,0.9999837675634693,0.08701229337946964,1.4124329933188304e-06,CALM2,0.9999837675634693
```

### ./cellularity/enrichment_corrected_significant.csv

Total data rows: 885 (header + 885 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
library,term,p_value,z_score,combined_score,overlap_genes,adj_p_value
```
FIRST 20 DATA ROWS:
```csv
Reactome_2022,Eukaryotic Translation Elongation R-HSA-156842,1.022780432506075e-97,169.69095816464238,37896.781196034775,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;EEF1B2;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;EEF1A1;EEF1G;EEF1D;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;EEF2;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,1.0749422345638849e-94
Reactome_2022,L13a-mediated Translational Silencing Of Ceruloplasmin Expression R-HSA-156827,6.9138056762584705e-96,104.10160427807487,22810.1864496805,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;PABPC1;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;EIF4B;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;EIF4G1;RPS23,3.633204882873826e-93
GO_Biological_Process_2023,Cytoplasmic Translation (GO:0002181),8.088020602860676e-96,146.5287137105319,32083.602578066446,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS9;RPS7;RPS8;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;UBA52;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,2.1950887916163875e-92
Reactome_2022,Peptide Chain Elongation R-HSA-156902,1.0974284033332321e-93,170.3672839506173,36466.68167438696,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;EEF1A1;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;EEF2;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,3.84465750634409e-91
Reactome_2022,GTP Hydrolysis And Joining Of 60S Ribosomal Subunit R-HSA-72706,2.1280416484642426e-93,96.60697518443997,20614.499832639438,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;EIF4B;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;EIF4G1;RPS23,5.591429431339797e-91
Reactome_2022,Cap-dependent Translation Initiation R-HSA-72737,3.8833092532968175e-92,83.75466284074605,17628.77698748328,EIF4A2;RPL4;EIF4A1;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;PABPC1;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;EIF4B;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;EIF4G1;RPS23,8.16271605042991e-90
Reactome_2022,Formation Of A Pool Of Free 40S Subunits R-HSA-72689,7.036694294530272e-91,113.20930232558139,23500.451696741744,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;EIF3K;RPS29;EIF3L;RPL27A;EIF3H;RPS20;EIF3E;FAU;RPS21;RPS24;RPS23,1.2325942839252194e-88
Reactome_2022,Nonsense Mediated Decay (NMD) Independent Of Exon Junction Complex (EJC) R-HSA-975956,5.115582530525208e-90,127.73611111111111,26262.591335072324,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;PABPC1;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;EIF4G1;RPS23,7.680681770831419e-88
Reactome_2022,Eukaryotic Translation Termination R-HSA-72764,5.881651028811798e-87,123.40783410138249,24503.003777512815,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.1816152312812e-85
Reactome_2022,Selenocysteine Synthesis R-HSA-2408557,5.881651028811798e-87,123.40783410138249,24503.003777512815,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.1816152312812e-85
Reactome_2022,Viral mRNA Translation R-HSA-192823,5.881651028811798e-87,123.40783410138249,24503.003777512815,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPL7A;RPS14;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPS3A;RPSA;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.1816152312812e-85
Reactome_2022,SRP-dependent Cotranslational Protein Targeting To Membrane R-HSA-1799339,4.6572549362412144e-86,83.37454100367196,16381.754292806174,RPL4;RPL5;RPL30;TRAM1;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;SRP14;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;SSR2;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPN1;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,4.449795398172288e-84
Reactome_2022,Response Of EIF2AK4 (GCN2) To Amino Acid Deficiency R-HSA-9633012,7.40977208084676e-83,92.51785714285714,17496.215076782715,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,6.489725380808287e-81
Reactome_2022,Nonsense Mediated Decay (NMD) Enhanced By Exon Junction Complex (EJC) R-HSA-975957,1.2348497579179113e-80,69.6026936026936,12806.607337611564,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;PABPC1;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;EIF4G1;RPS23,9.983285350551728e-79
Reactome_2022,Selenoamino Acid Metabolism R-HSA-2408522,4.791483253462815e-78,64.04358508181416,11401.98668416583,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;AHCY;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,3.597034928135299e-76
GO_Biological_Process_2023,Macromolecule Biosynthetic Process (GO:0009059),2.3586353930086278e-76,34.141503046716316,5945.346162391077,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;EEF1B2;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS9;RPS7;RPS8;RPS5;PABPC4;RPL22;RPS6;RPL13A;RPSA;RPS3A;EEF1A1;EEF1G;EEF1D;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;APOE;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;EEF2;RPS25;COL5A1;RPS29;RPL27A;RPS20;FAU;RPS21;EIF4G2;RPS24;EIF4G1;RPS23,3.200668228312708e-73
Reactome_2022,Influenza Infection R-HSA-168255,2.557490540769008e-73,38.42440901594283,6422.627873637293,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;HSP90AA1;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;CANX;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;SLC25A6;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;ISG15;RPL23A;RPS25;RPS29;RPL27A;RPS20;CALR;FAU;RPS21;RPS24;RPS23;HSPA1A,1.7919483722321514e-71
KEGG_2021_Human,Ribosome,1.7247330190609442e-71,36.929587653725584,6017.250485494068,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;UBA52;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,4.4670585193678455e-69
Reactome_2022,Influenza Viral RNA Transcription And Replication R-HSA-168273,1.2413515774162127e-70,42.94985153414714,6913.412361339616,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS12;RPS9;HSP90AA1;RPS7;RPS8;RPL23;RPS5;RPL22;RPS6;RPL13A;RPSA;RPS3A;RPL37A;RPL27;RPL26;RPL29;RPL28;UBA52;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL15;RPS2;RPL18;RPS27A;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;RPS23,8.154128174152747e-69
GO_Biological_Process_2023,Peptide Biosynthetic Process (GO:0043043),1.7247330190609442e-71,36.929587653725584,6017.250485494068,RPL4;RPL5;RPL30;RPL3;RPL32;RPL31;RPL34;RPLP1;RPLP0;RPL10A;RPL8;RPL6;RPL7;RPS4X;RPS14;RPL7A;RPS17;RPS16;RPL18A;RPS19;RPS18;RPL36;RPL35;RPLP2;RPL38;RPL37;RPS11;RPS10;RPS13;RPS9;RPS7;RPS8;RPS5;PABPC4;RPL22;RPS6;RPL13A;RPSA;RPS3A;EEF1A1;RPL37A;RPL24;RPL27;RPL26;RPL29;RPL28;RPL10;RPL12;RPL11;RPS15A;RPL14;RPS3;RPL13;RPL15;RPS2;RPL18;RPS27A;RPL17;RPL19;RPL41;RPL35A;RPL23A;RPS25;RPS29;RPL27A;RPS20;FAU;RPS21;RPS24;EIF4G1;RPS23,1.5603084712438007e-68
```
LAST 20 DATA ROWS:
```csv
GO_Biological_Process_2023,Negative Regulation Of Morphogenesis Of An Epithelium (GO:1905331),0.0059328116851476344,26.100401606425702,133.823467686336,TACSTD2;SULF1,0.047080850624241756
Reactome_2022,MyD88-independent TLR4 Cascade R-HSA-166166,0.017927984757630317,2.7545638945233266,11.07718229059532,APP;JUN;UBB;UBC;FOS;RPS27A;UBA52,0.04710577995067366
Reactome_2022,Dectin-1 Mediated Noncanonical NF-kB Signaling R-HSA-5607761,0.01808225984730525,3.5072150072150072,14.073836344642054,UBB;PSMD3;UBC;RPS27A;UBA52,0.04739265610852324
GO_Biological_Process_2023,Cell-Matrix Adhesion (GO:0007160),0.006061381316945464,3.123078161474684,15.945867333054817,ITGB1;CD63;COL3A1;ITGB4;FN1;EMP2;THY1;MSLN,0.04796090056615157
GO_Biological_Process_2023,Regulation Of Type II Interferon Production (GO:0032649),0.006123090843767418,3.4467545638945234,17.563586801207208,ISG15;HLA-A;CD47;GAS6;HLA-DRB1;HLA-DPA1;HSPD1,0.04830833880809527
GO_Biological_Process_2023,Regulation Of Wound Healing (GO:0061041),0.006186730331773237,4.67965367965368,23.797670052686616,ITGB1;CLDN4;ANXA1;SERPINE1;CLDN1,0.04838843262372497
GO_Biological_Process_2023,Positive Regulation Of Smooth Muscle Cell Proliferation (GO:0048661),0.006186730331773237,4.67965367965368,23.797670052686616,JUN;IGFBP5;STAT1;MMP2;THBS1,0.04838843262372497
GO_Biological_Process_2023,Regulation Of Signal Transduction By P53 Class Mediator (GO:1901796),0.006186730331773237,4.67965367965368,23.797670052686616,RPL5;RPL11;RPS20;RPL37;RPL17,0.04838843262372497
Reactome_2022,Degradation Of Beta-Catenin By Destruction Complex R-HSA-195253,0.018696947110537213,3.0242914979757085,12.03485053989489,UBB;PSMD3;UBC;CTNNB1;RPS27A;UBA52,0.048760524598448166
Reactome_2022,Cyclin A:Cdk2-associated Events At S Phase Entry R-HSA-69656,0.018696947110537213,3.0242914979757085,12.03485053989489,CCND1;UBB;PSMD3;UBC;RPS27A;UBA52,0.048760524598448166
Reactome_2022,Negative Regulation Of MAPK Pathway R-HSA-5675221,0.01883771080535323,4.242153443766347,16.84938603480476,UBB;UBC;RPS27A;UBA52,0.048885022361546286
Reactome_2022,Dual Incision In GG-NER R-HSA-5696400,0.01883771080535323,4.242153443766347,16.84938603480476,UBB;UBC;RPS27A;UBA52,0.048885022361546286
Reactome_2022,RHOBTB1 GTPase Cycle R-HSA-9013422,0.01896828932905573,5.879275653923541,23.31124963704241,CCT2;HNRNPC;VIM,0.04898199529444121
Reactome_2022,Post-chaperonin Tubulin Folding Pathway R-HSA-389977,0.01896828932905573,5.879275653923541,23.31124963704241,TUBA1B;TUBA1A;TUBB,0.04898199529444121
GO_Biological_Process_2023,Response To Epidermal Growth Factor (GO:0070849),0.006317508693985948,6.040322580645161,30.59079295607524,EEF1A1;ZFP36;ERBB2;ZFP36L1,0.04912813351139789
GO_Biological_Process_2023,Prostaglandin Metabolic Process (GO:0006693),0.006317508693985948,6.040322580645161,30.59079295607524,CD74;GSTP1;PTGDS;PTGS1,0.04912813351139789
Reactome_2022,Pre-NOTCH Transcription And Translation R-HSA-1912408,0.019277136070105953,3.445507708665603,13.605743310257864,NOTCH2;NOTCH3;JUN;CCND1;ELF3,0.049415292706539896
Reactome_2022,Asymmetric Localization Of PCP Proteins R-HSA-4608870,0.019277136070105953,3.445507708665603,13.605743310257864,UBB;PSMD3;UBC;RPS27A;UBA52,0.049415292706539896
Reactome_2022,Regulation Of Actin Dynamics For Phagocytic Cup Formation R-HSA-2029482,0.019277136070105953,3.445507708665603,13.605743310257864,HSP90AA1;HSP90AB1;MYH9;RNASE1;ACTG1,0.049415292706539896
Reactome_2022,Cell Surface Interactions At Vascular Wall R-HSA-202733,0.01949472625755282,2.5001935733643053,9.844790462468355,ITGB1;GRB7;CD74;EPCAM;BSG;FN1;CD47;GAS6,0.04985147760751341
```

### ./cellularity/estimate_scores.csv

Total data rows: 235 (header + 235 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
"PATIENT_ID","SAMPLE_BARCODE","StromalScore","ImmuneScore","ESTIMATEScore","TumorPurity"
```
FIRST 20 DATA ROWS:
```csv
"TCGA.04.1348","TCGA.04.1348.01",749.782782904445,824.024969012093,1573.80775191654,0.670433139486241
"TCGA.04.1362","TCGA.04.1362.01",707.871682001396,232.6803173453,940.551999346695,0.736409005717871
"TCGA.04.1364","TCGA.04.1364.01",501.562211108073,309.916861125706,811.479072233779,0.749094008604845
"TCGA.04.1365","TCGA.04.1365.01",505.279657633976,670.620254272337,1175.89991190631,0.712602398466881
"TCGA.04.1514","TCGA.04.1514.01",785.468350199962,353.89043595002,1139.35878614998,0.71635520993724
"TCGA.09.0364","TCGA.09.0364.01",507.14690113522,428.683020580363,935.829921715582,0.736877767565578
"TCGA.09.0366","TCGA.09.0366.01",554.534274647006,884.982411229271,1439.51668587628,0.684927925564307
"TCGA.09.0367","TCGA.09.0367.01",989.769553284576,384.331859625016,1374.10141290959,0.691892511579114
"TCGA.09.0369","TCGA.09.0369.01",536.750093903649,556.802099377248,1093.5521932809,0.721030470425232
"TCGA.09.1659","TCGA.09.1659.01",685.425239676633,780.090811764421,1465.51605144105,0.682142270149754
"TCGA.09.1662","TCGA.09.1662.01",615.38653687146,1199.17790501652,1814.56444188798,0.643798544144728
"TCGA.09.1666","TCGA.09.1666.01",431.720885798618,1073.44722343252,1505.16810923114,0.677874704214532
"TCGA.09.1667","TCGA.09.1667.01",892.875474829165,979.467293277533,1872.3427681067,0.637285704737604
"TCGA.09.1668","TCGA.09.1668.01",604.385814171906,840.348476825405,1444.73429099731,0.684369693429957
"TCGA.09.1669","TCGA.09.1669.01",744.978101452713,956.567279475476,1701.54538092819,0.656403868544447
"TCGA.09.1673","TCGA.09.1673.01",193.474853632769,705.993336549126,899.468190181895,0.740475529646315
"TCGA.09.1674","TCGA.09.1674.01",930.666634779535,835.972676371544,1766.63931115108,0.649165604040205
"TCGA.09.2044","TCGA.09.2044.01",604.886301237534,895.187723457062,1500.0740246946,0.678424245443035
"TCGA.09.2051","TCGA.09.2051.01",334.325312625435,545.488821167685,879.814133793119,0.742411397386333
"TCGA.09.2054","TCGA.09.2054.01",561.649866915484,623.326834840086,1184.97670175557,0.711667019708158
```
LAST 20 DATA ROWS:
```csv
"TCGA.61.2002","TCGA.61.2002.01",742.369458344013,724.027454938991,1466.396913283,0.682047717549786
"TCGA.61.2003","TCGA.61.2003.01",818.556033589671,859.780514482064,1678.33654807174,0.658970167813328
"TCGA.61.2008","TCGA.61.2008.01",1063.0737003864,375.923053671814,1438.99675405822,0.684983531118408
"TCGA.61.2009","TCGA.61.2009.01",692.485413037446,759.742001744861,1452.22741478231,0.683567301164667
"TCGA.61.2012","TCGA.61.2012.01",691.123895025972,842.568614994538,1533.69251002051,0.674790545575687
"TCGA.61.2088","TCGA.61.2088.01",-164.597740519398,773.547919491482,608.950178972084,0.76845441704179
"TCGA.61.2092","TCGA.61.2092.01",312.677430643849,869.640793450428,1182.31822409428,0.711941111287022
"TCGA.61.2094","TCGA.61.2094.01",604.455268175746,739.564752481277,1344.02002065702,0.695073821232141
"TCGA.61.2095","TCGA.61.2095.01",660.057552850836,732.08792902282,1392.14548187366,0.689977752955864
"TCGA.61.2098","TCGA.61.2098.01",451.584703715679,418.649208068823,870.233911784503,0.743352782464979
"TCGA.61.2101","TCGA.61.2101.01",721.29513376825,727.805834772549,1449.1009685408,0.683902193544271
"TCGA.61.2102","TCGA.61.2102.01",511.89282583015,888.682911663396,1400.57573749355,0.689081510811982
"TCGA.61.2104","TCGA.61.2104.01",518.767235607469,1145.69030549228,1664.45754109974,0.660501176154531
"TCGA.61.2109","TCGA.61.2109.01",858.672355996056,167.24425756379,1025.91661355985,0.72787404925544
"TCGA.61.2110","TCGA.61.2110.01",545.454061677939,641.190888280542,1186.64494995848,0.711494966385492
"TCGA.61.2113","TCGA.61.2113.01",688.534007358513,754.818471850408,1443.35247920892,0.684517572715037
"TCGA.OY.A56P","TCGA.OY.A56P.01",486.20669927116,304.127034428599,790.333733699759,0.751146611624598
"TCGA.OY.A56Q","TCGA.OY.A56Q.01",205.723944607578,494.143593215893,699.867537823472,0.759846319976848
"TCGA.VG.A8LO","TCGA.VG.A8LO.01",355.240143122089,840.585930188265,1195.82607331035,0.710547315988186
"TCGA.WR.A838","TCGA.WR.A838.01",704.830253610171,595.993875647386,1300.82412925756,0.699618359138022
```

### ./cellularity/genes_added_after_purity_correction.csv

```csv
gene
APH1A
ATP2B4
ISYNA1
PYY
SEPT2
SERPINE1
SPINK1
SSR2
SUPT5H
```

### ./cellularity/genes_dropped_after_purity_correction.csv

```csv
gene
ALPPL2
C1R
C7
COL12A1
IER2
IFITM2
IGFBP4
ITGA3
PKN1
```

### ./enhancement5/outputs/alpha_selection_summary.csv

```csv
"cohort","fold_id","alpha_selected"
"CohortA",1,0.6
"CohortA",2,0
"CohortA",3,0.5
"CohortA",4,0.2
"CohortA",5,0.2
"CohortA",6,0
"CohortA",7,0.7
"CohortA",8,0.5
"CohortA",9,0.2
"CohortA",10,0.8
"CohortA",11,0.6
"CohortA",12,0.4
"CohortA",13,1
"CohortA",14,0.7
"CohortA",15,0.2
"CohortA",16,0.1
"CohortA",17,0.4
"CohortA",18,0.9
"CohortA",19,0.4
"CohortA",20,0.5
"CohortA",21,0.7
"CohortA",22,0.2
"CohortA",23,0.7
"CohortA",24,0.3
"CohortA",25,0.4
"CohortB",1,0.3
"CohortB",2,0
"CohortB",3,0.9
"CohortB",4,0.5
"CohortB",5,0.1
"CohortB",6,0.1
"CohortB",7,0
"CohortB",8,0.4
"CohortB",9,0
"CohortB",10,0.2
"CohortB",11,0.2
"CohortB",12,0
"CohortB",13,0.8
"CohortB",14,0.3
"CohortB",15,0.7
"CohortB",16,0
"CohortB",17,1
"CohortB",18,0.2
"CohortB",19,0
"CohortB",20,0.3
"CohortB",21,0.7
"CohortB",22,0.1
"CohortB",23,0
"CohortB",24,1
"CohortB",25,0
```

### ./enhancement5/outputs/cv_results_cohortA_n235.csv

```csv
"cohort","fold_id","repeat_id","inner_fold","n_train","n_test","alpha_selected","cindex_baseline","cindex_full_lambdamin","cindex_full_lambda1se"
"CohortA",1,1,1,187,48,0.6,0.600389863547758,0.598440545808967,0.600389863547758
"CohortA",2,1,2,188,47,0,0.546577946768061,0.678707224334601,0.546577946768061
"CohortA",3,1,3,188,47,0.5,0.625984251968504,0.596456692913386,0.625984251968504
"CohortA",4,1,4,188,47,0.2,0.507320644216691,0.508784773060029,0.508784773060029
"CohortA",5,1,5,189,46,0.2,0.604116222760291,0.604116222760291,0.604116222760291
"CohortA",6,2,1,187,48,0,0.608885017421603,0.658536585365854,0.60191637630662
"CohortA",7,2,2,188,47,0.7,0.615618661257606,0.539553752535497,0.617647058823529
"CohortA",8,2,3,188,47,0.5,0.597014925373134,0.597014925373134,0.597014925373134
"CohortA",9,2,4,188,47,0.2,0.541749502982107,0.576540755467197,0.543737574552684
"CohortA",10,2,5,189,46,0.8,0.59327731092437,0.589915966386555,0.59327731092437
"CohortA",11,3,1,187,48,0.6,0.606451612903226,0.585483870967742,0.604838709677419
"CohortA",12,3,2,188,47,0.4,0.725382932166302,0.715536105032823,0.725382932166302
"CohortA",13,3,3,188,47,1,0.492125984251969,0.490157480314961,0.490157480314961
"CohortA",14,3,4,188,47,0.7,0.543010752688172,0.577060931899642,0.543010752688172
"CohortA",15,3,5,189,46,0.2,0.612903225806452,0.564516129032258,0.612903225806452
"CohortA",16,4,1,187,48,0.1,0.689380530973451,0.686725663716814,0.689380530973451
"CohortA",17,4,2,188,47,0.4,0.394904458598726,0.424628450106157,0.394904458598726
"CohortA",18,4,3,188,47,0.9,0.68213058419244,0.676975945017182,0.680412371134021
"CohortA",19,4,4,188,47,0.4,0.512647554806071,0.524451939291737,0.510961214165261
"CohortA",20,4,5,189,46,0.5,0.665198237885463,0.669603524229075,0.665198237885463
"CohortA",21,5,1,187,48,0.7,0.572664359861592,0.572664359861592,0.572664359861592
"CohortA",22,5,2,188,47,0.2,0.515116279069767,0.511627906976744,0.519767441860465
"CohortA",23,5,3,188,47,0.7,0.606796116504854,0.561488673139159,0.608414239482201
"CohortA",24,5,4,188,47,0.3,0.54392523364486,0.542056074766355,0.54392523364486
"CohortA",25,5,5,189,46,0.4,0.632936507936508,0.630952380952381,0.630952380952381
```

### ./enhancement5/outputs/cv_results_cohortB_n163.csv

```csv
"cohort","fold_id","repeat_id","inner_fold","n_train","n_test","alpha_selected","cindex_baseline","cindex_full_lambdamin","cindex_full_lambda1se"
"CohortB",1,1,1,130,33,0.3,0.530805687203791,0.540284360189573,0.530805687203791
"CohortB",2,1,2,130,33,0,0.575107296137339,0.407725321888412,0.55793991416309
"CohortB",3,1,3,130,33,0.9,0.532188841201717,0.570815450643777,0.536480686695279
"CohortB",4,1,4,130,33,0.5,0.53072625698324,0.608938547486033,0.525139664804469
"CohortB",5,1,5,132,31,0.1,0.543269230769231,0.586538461538462,0.548076923076923
"CohortB",6,2,1,130,33,0.1,0.597510373443983,0.66804979253112,0.597510373443983
"CohortB",7,2,2,130,33,0,0.666666666666667,0.646153846153846,0.666666666666667
"CohortB",8,2,3,130,33,0.4,0.577272727272727,0.518181818181818,0.586363636363636
"CohortB",9,2,4,130,33,0,0.638636363636364,0.690909090909091,0.638636363636364
"CohortB",10,2,5,132,31,0.2,0.433673469387755,0.520408163265306,0.438775510204082
"CohortB",11,3,1,130,33,0.2,0.502673796791444,0.679144385026738,0.491978609625668
"CohortB",12,3,2,130,33,0,0.75,0.6875,0.7625
"CohortB",13,3,3,130,33,0.8,0.507692307692308,0.512820512820513,0.507692307692308
"CohortB",14,3,4,130,33,0.3,0.535087719298246,0.635964912280702,0.548245614035088
"CohortB",15,3,5,132,31,0.7,0.40625,0.616071428571429,0.410714285714286
"CohortB",16,4,1,130,33,0,0.701357466063348,0.714932126696833,0.710407239819005
"CohortB",17,4,2,130,33,1,0.543478260869565,0.619565217391304,0.543478260869565
"CohortB",18,4,3,130,33,0.2,0.497560975609756,0.492682926829268,0.492682926829268
"CohortB",19,4,4,130,33,0,0.472477064220183,0.577981651376147,0.481651376146789
"CohortB",20,4,5,132,31,0.3,0.517094017094017,0.628205128205128,0.521367521367521
"CohortB",21,5,1,130,33,0.7,0.585714285714286,0.657142857142857,0.59047619047619
"CohortB",22,5,2,130,33,0.1,0.549180327868853,0.60655737704918,0.549180327868853
"CohortB",23,5,3,130,33,0,0.542600896860987,0.596412556053812,0.52914798206278
"CohortB",24,5,4,130,33,1,0.620512820512821,0.620512820512821,0.620512820512821
"CohortB",25,5,5,132,31,0,0.564102564102564,0.753846153846154,0.569230769230769
```

### ./enhancement5/outputs/cv_summary.csv

```csv
"cohort","model","lambda","mean_cindex","sd_cindex","n_folds"
"CohortA_n235","baseline",NA,0.585460348740399,0.0713973392153677,25
"CohortA_n235","full_expression","lambda.min",0.587279875172405,0.0691503969633265,25
"CohortA_n235","full_expression","lambda.1se",0.585292794931868,0.0710847833555504,25
"CohortB_n163","baseline",NA,0.556865576616048,0.077127308537942,25
"CohortB_n163","full_expression","lambda.min",0.606293796263613,0.0778847268236035,25
"CohortB_n163","full_expression","lambda.1se",0.558226466340368,0.0786986900521491,25
```

### ./enhancement5/outputs/emt_ecm_overlap.csv

```csv
"gene","source","cohortA_lambdamin_selected","cohortA_lambdamin_coef","cohortA_lambdamin_HR","cohortA_lambda1se_selected","cohortA_lambda1se_coef","cohortA_lambda1se_HR","cohortB_lambdamin_selected","cohortB_lambdamin_coef","cohortB_lambdamin_HR","cohortB_lambda1se_selected","cohortB_lambda1se_coef","cohortB_lambda1se_HR"
"CTNNB1","explicit_anchor",FALSE,NA,NA,FALSE,NA,NA,TRUE,-4.10324718104409e-05,0.99995896837001,TRUE,3.21655198413993e-38,1
"THBS2","explicit_anchor;msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.0143473128558783,1.01445072954092,TRUE,1.04401897915346e-37,1
"COL1A1","explicit_anchor;msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"COL1A2","explicit_anchor;msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"THBS1","explicit_anchor;msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"FLNA","explicit_anchor;msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"NOTCH2","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"TAGLN","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"LRP1","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.0165245949780163,1.01666188125518,TRUE,1.09409912788876e-37,1
"IGFBP4","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"COL12A1","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.0161054468935787,1.01623583866884,TRUE,9.84399988515385e-38,1
"IGFBP2","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"FSTL1","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"SAT1","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.0152795210778451,1.01539684977379,TRUE,7.72456505018085e-38,1
"DCN","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"ACTA2","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"MMP14","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.0237486010545479,1.02403284475046,TRUE,1.4746743668158e-37,1
"COL4A2","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.0140636049205442,1.01416296264175,TRUE,8.08658385687655e-38,1
"ANPEP","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.00924660019340993,1.00928948206959,TRUE,4.26923635508395e-38,1
"MGP","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"SERPINH1","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"COL6A3","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,TRUE,0.0119774608573174,1.01204947788142,TRUE,1.02371896257719e-37,1
"TGFBI","msigdb_emt24_top200",TRUE,0.00409285018943933,1.00410123733932,FALSE,NA,NA,TRUE,0.0302829936814908,1.03074618734178,TRUE,1.64600949667327e-37,1
"VIM","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
"MYL9","msigdb_emt24_top200",FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA,FALSE,NA,NA
```

### ./enhancement5/outputs/final_model_alpha.csv

```csv
"cohort","final_model_alpha","lambda_min","lambda_1se","manuscript_claim"
"CohortA_n235",0.9,0.136240983996742,0.238084988779298,NA
"CohortB_n163",0,3.97206643238032,197.690682330493,0
```

### ./enhancement5/outputs/final_model_genes_cohortA_lambda1se.csv

```csv
"gene","coefficient","hazard_ratio"
```

### ./enhancement5/outputs/final_model_genes_cohortA_lambdamin.csv

```csv
"gene","coefficient","hazard_ratio"
"SCNN1A",0.0539734333067406,1.05545656179189
"CPA2",-0.0388169542393752,0.961926769649527
"LGALS3BP",-0.0255025877074466,0.974819856413876
"PUF60",-0.00638623250519025,0.993634116137518
"TGFBI",0.00409285018943933,1.00410123733932
```

### ./enhancement5/outputs/final_model_genes_cohortB_lambda1se.csv

Total data rows: 200 (header + 200 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
"gene","coefficient","hazard_ratio"
```
FIRST 20 DATA ROWS:
```csv
"PUF60",-2.08583896757509e-37,1
"TGFBI",1.64600949667327e-37,1
"LGALS3BP",-1.57324073945976e-37,1
"ARF1",-1.56177785969181e-37,1
"RPS19",1.49433751289965e-37,1
"MMP14",1.4746743668158e-37,1
"HSP90AA1",-1.38106750267331e-37,1
"GRINA",-1.3072131981036e-37,1
"RPL18",1.29971690618815e-37,1
"SCNN1A",1.26205859436441e-37,1
"P4HB",-1.24059460754812e-37,1
"TIMP3",1.20447319031871e-37,1
"HSPB1",-1.20136308999554e-37,1
"ZFP36",1.13417192307862e-37,1
"H3F3A",-1.12101334400743e-37,1
"LRP1",1.09409912788876e-37,1
"PFN1",-1.09332875950313e-37,1
"CPA2",1.08640917720097e-37,1
"GRN",-1.0852930302203e-37,1
"COL3A1",1.06967122560572e-37,1
```
LAST 20 DATA ROWS:
```csv
"TAGLN2",7.86151920078512e-39,1
"CALM2",7.41429449979495e-39,1
"CANX",-7.38559704679348e-39,1
"NDUFS5",-7.26598325917985e-39,1
"COX4I1",-6.0768334966598e-39,1
"CLIC1",-6.01484832226758e-39,1
"PSMD3",-5.99368626859859e-39,1
"PKN1",-5.33256864596417e-39,1
"PPP1R1B",-5.0676898961297e-39,1
"AP2M1",-4.59464091028962e-39,1
"TRIM28",4.59293294031962e-39,1
"CD59",4.03270938540547e-39,1
"KIAA1522",2.64540669410286e-39,1
"RPS10",-2.48201402363646e-39,1
"APH1A",-2.08113558049168e-39,1
"PTMS",4.71107702773313e-40,1
"NUMA1",-2.06838972652647e-40,1
"PSME1",-1.74121365780307e-40,1
"MUC1",1.35992491687248e-40,1
"ALDOA",-5.59366051829228e-41,1
```

### ./enhancement5/outputs/final_model_genes_cohortB_lambdamin.csv

Total data rows: 200 (header + 200 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
"gene","coefficient","hazard_ratio"
```
FIRST 20 DATA ROWS:
```csv
"PUF60",-0.0369160008608169,0.963757086714749
"TGFBI",0.0302829936814908,1.03074618734178
"CPA2",0.0290073381240534,1.02943214854822
"RPS19",0.0282510936399447,1.028653940459
"ARF1",-0.0270438950704162,0.973318516701811
"RPL18",0.0243710802039928,1.02467048228211
"SCNN1A",0.0238898481708826,1.02417749665241
"MMP14",0.0237486010545479,1.02403284475046
"P4HB",-0.0235192256124747,0.97675519577145
"STRAP",0.0231438900363609,1.02341378800034
"LGALS3BP",-0.0231259655843728,0.97713939008637
"HSP90AA1",-0.0219662286370645,0.978273272115076
"MEST",0.0210899280277036,1.02131389225194
"H3F3A",-0.0199475399565973,0.980250095920505
"CD9",0.0197977876373247,1.01999506355991
"FCGBP",0.0192849470147656,1.01947210276574
"SNRPD2",0.0190504309541356,1.01923304821644
"GRINA",-0.018817705454604,0.981358242192522
"RPS11",0.0184316554052396,1.01860256681093
"HSPB1",-0.0180329390952328,0.98212868139533
```
LAST 20 DATA ROWS:
```csv
"HNRNPC",-0.00136726737822461,0.998633666905963
"LTBP4",0.00126554563937507,1.00126634678018
"CRABP2",0.00116755928783182,1.00116824115052
"NUMA1",-0.00116659802052301,0.998834082190411
"NDUFS5",-0.00112397818750244,0.998876653239388
"RPN1",-0.00109934728867368,0.998901256772179
"CFL1",-0.00109363207651349,0.998906965721102
"COX4I1",-0.00107878094599023,0.998921800728989
"APH1A",0.00101403869989297,1.00101455301096
"PSMD3",-0.000882717944997038,0.999117671535879
"SQSTM1",-0.000774094860310666,0.999226204673822
"APOE",0.000668309224725092,1.00066853259309
"IFI27",-0.000582922411315175,0.999417247454946
"OAZ1",0.000425945155833451,1.00042603588335
"SLC38A2",0.000418635990349744,1.00041872363063
"PPP1R1B",-0.000154370286871821,0.999845641627608
"ATP5E",0.000145661082330461,1.00014567169142
"PRDX2",-0.000144735331115082,0.999855275142538
"FAU",-9.99655460586973e-05,0.99990003945033
"CTNNB1",-4.10324718104409e-05,0.99995896837001
```

### ./enhancement5/outputs/repeat_level_paired_tests.csv

```csv
"cohort","lambda","n_repeats","mean_difference","sd_difference","t_statistic","paired_t_pvalue","wilcoxon_pvalue"
"CohortA_n235","lambda.min",5,0.00181952643200618,0.0128393105955781,0.316884988375054,0.767180565569544,1
"CohortA_n235","lambda.1se",5,-0.00016755380853084,0.0007080237056517,-0.529165482417127,0.624695164685077,0.8125
"CohortB_n163","lambda.min",5,0.0494282196475653,0.0354565105521539,3.11719504873929,0.0356230753039491,0.0625
"CohortB_n163","lambda.1se",5,0.00136088972432011,0.00292733792392225,1.03952533412454,0.357265268306515,0.3125
```

### ./fixes/phase4_corrected_values.csv

```csv
category,item,value,n_total,manuscript
FLNA_rank,SHAP_12m,338,551,460-505
FLNA_rank,SHAP_18m,435,553,460-505
FLNA_rank,SHAP_24m,501,554,460-505
FLNA_rank,MDI_12m,340,551,460-505
FLNA_rank,MDI_18m,429,553,460-505
FLNA_rank,MDI_24m,508,554,460-505
FLNA_rank,permutation_12m,299,551,460-505
FLNA_rank,permutation_18m,504,553,460-505
FLNA_rank,permutation_24m,340,554,460-505
FLNA_rank,TRUE_RANGE_all_methods,299-508,,460-505
permutation_spearman,with12m_MDI_vs_Permutation,0.4063,557,0.37-0.41
permutation_spearman,with12m_Permutation_vs_SHAP,0.3661,557,0.37-0.41
permutation_spearman,without12m_MDI_vs_Permutation,0.4188,556,0.37-0.41
permutation_spearman,without12m_Permutation_vs_SHAP,0.38,556,0.37-0.41
permutation_spearman,TRUE_RANGE,0.3661-0.4188,,0.37-0.41
ribosome_significance,SHAP-with12m_top50,p=0.371 sig=False,,NS at top50/100
ribosome_significance,SHAP-with12m_top100,p=0.305 sig=False,,NS at top50/100
ribosome_significance,SHAP-with12m_top200,p=5.75e-10 sig=True,,NS at top50/100
ribosome_significance,SHAP-with12m_top500,p=1.95e-51 sig=True,,NS at top50/100
ribosome_significance,SHAP-without12m_top50,p=0.382 sig=False,,NS at top50/100
ribosome_significance,SHAP-without12m_top100,p=0.0198 sig=True,,NS at top50/100
ribosome_significance,SHAP-without12m_top200,p=1.7e-15 sig=True,,NS at top50/100
ribosome_significance,SHAP-without12m_top500,p=5.05e-50 sig=True,,NS at top50/100
enh5_alpha_perfold,CohortA_n_folds_alpha0,2/25,25,B: pure ridge alpha=0
enh5_alpha_perfold,CohortA_alpha_range,0.0-1.0,25,
enh5_alpha_perfold,CohortB_n_folds_alpha0,8/25,25,B: pure ridge alpha=0
enh5_alpha_perfold,CohortB_alpha_range,0.0-1.0,25,
```

### ./hrd/brca_cox_summary.csv

```csv
"metric","value","manuscript_value"
"n_matched_subset",335,335
"n_brca_mutant",28,NA
"c_index_baseline",0.5731,0.573
"c_index_brca_added",0.5885,0.588
```

### ./hrd/brca_status.csv

Total data rows: 409 (header + 409 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
"PATIENT_ID","BRCA1_mutated","BRCA2_mutated","BRCA_any_mutated"
```
FIRST 20 DATA ROWS:
```csv
"TCGA-04-1331",0,1,1
"TCGA-04-1335",1,0,1
"TCGA-04-1336",0,0,0
"TCGA-04-1341",0,0,0
"TCGA-04-1342",0,0,0
"TCGA-04-1343",0,0,0
"TCGA-04-1346",0,0,0
"TCGA-04-1348",0,0,0
"TCGA-04-1349",0,0,0
"TCGA-04-1353",0,0,0
"TCGA-04-1356",0,1,1
"TCGA-04-1357",1,0,1
"TCGA-04-1360",0,0,0
"TCGA-04-1361",0,0,0
"TCGA-04-1362",0,0,0
"TCGA-04-1367",0,0,0
"TCGA-04-1369",0,0,0
"TCGA-04-1516",0,0,0
"TCGA-04-1542",0,0,0
"TCGA-04-1638",0,0,0
```
LAST 20 DATA ROWS:
```csv
"TCGA-61-2092",0,0,0
"TCGA-61-2094",0,0,0
"TCGA-61-2095",0,0,0
"TCGA-61-2096",1,0,1
"TCGA-61-2101",0,0,0
"TCGA-61-2102",0,0,0
"TCGA-61-2104",0,0,0
"TCGA-61-2109",0,0,0
"TCGA-61-2110",0,0,0
"TCGA-61-2111",0,0,0
"TCGA-61-2113",0,0,0
"TCGA-61-2610",0,0,0
"TCGA-61-2611",0,0,0
"TCGA-61-2612",0,0,0
"TCGA-61-2613",0,0,0
"TCGA-61-2614",0,0,0
"TCGA-OY-A56P",0,0,0
"TCGA-OY-A56Q",0,0,0
"TCGA-VG-A8LO",0,0,0
"TCGA-WR-A838",0,0,0
```

### ./hrd/cox_hazard_ratios_brca.csv

```csv
"model","term","HR","p_value","c_index"
"baseline_matched","log_tmb",0.651739910110537,0.00851779663894772,0.573149055029564
"baseline_matched","aneu",1.01221809712324,0.253298823462507,0.573149055029564
"brca_added","log_tmb",0.714203539659389,0.0438471232266475,0.588457213334784
"brca_added","aneu",1.01089356916671,0.304307511250683,0.588457213334784
"brca_added","BRCA_any_mutated",0.455286973626157,0.0238238469018231,0.588457213334784
```

### ./hrd/hrd_gene_crossref.csv

```csv
gene,in_rf_importance_list,in_top500_variance_list
ATM,False,False
ATR,False,False
ATRX,False,False
BARD1,False,False
BRCA1,False,False
BRCA2,False,False
BRIP1,False,False
CHEK1,False,False
CHEK2,False,False
FANCA,False,False
FANCC,False,False
FANCD2,False,False
FANCE,False,False
FANCF,False,False
FANCG,False,False
FANCI,False,False
FANCL,False,False
FANCM,False,False
MRE11,False,False
NBN,False,False
PALB2,False,False
PPP2R2A,False,False
RAD50,False,False
RAD51,False,False
RAD51B,False,False
RAD51C,False,False
RAD51D,False,False
RAD54L,False,False
XRCC2,False,False
XRCC3,False,False
```



## multi_cancer/outputs/ (COADREAD/results/, LUAD/results/, comparison/)

### ./multi_cancer/outputs/COADREAD/results/ablation_leakage_raw.csv

Total data rows: 540 (header + 540 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,condition,auc,seed
```
FIRST 20 DATA ROWS:
```csv
18,Logistic Regression,leaky_full_data_variance,0.2368421052631579,42
18,Random Forest,leaky_full_data_variance,0.27631578947368424,42
18,SVM,leaky_full_data_variance,0.5526315789473684,42
18,Logistic Regression,correct_train_only_variance,0.31578947368421056,42
18,Random Forest,correct_train_only_variance,0.1578947368421053,42
18,SVM,correct_train_only_variance,0.5526315789473684,42
18,Logistic Regression,leaky_full_data_variance,0.5263157894736842,43
18,Random Forest,leaky_full_data_variance,0.6447368421052632,43
18,SVM,leaky_full_data_variance,0.5,43
18,Logistic Regression,correct_train_only_variance,0.39473684210526316,43
18,Random Forest,correct_train_only_variance,0.5,43
18,SVM,correct_train_only_variance,0.5,43
18,Logistic Regression,leaky_full_data_variance,0.2894736842105263,44
18,Random Forest,leaky_full_data_variance,0.7631578947368421,44
18,SVM,leaky_full_data_variance,0.6842105263157895,44
18,Logistic Regression,correct_train_only_variance,0.2894736842105263,44
18,Random Forest,correct_train_only_variance,0.6842105263157895,44
18,SVM,correct_train_only_variance,0.6842105263157895,44
18,Logistic Regression,leaky_full_data_variance,0.7894736842105263,45
18,Random Forest,leaky_full_data_variance,0.9473684210526316,45
```
LAST 20 DATA ROWS:
```csv
36,Random Forest,correct_train_only_variance,0.7142857142857143,68
36,SVM,correct_train_only_variance,0.5714285714285714,68
36,Logistic Regression,leaky_full_data_variance,0.5238095238095238,69
36,Random Forest,leaky_full_data_variance,0.6428571428571428,69
36,SVM,leaky_full_data_variance,0.4285714285714286,69
36,Logistic Regression,correct_train_only_variance,0.5238095238095238,69
36,Random Forest,correct_train_only_variance,0.5238095238095238,69
36,SVM,correct_train_only_variance,0.33333333333333337,69
36,Logistic Regression,leaky_full_data_variance,0.7619047619047619,70
36,Random Forest,leaky_full_data_variance,0.8095238095238095,70
36,SVM,leaky_full_data_variance,0.47619047619047616,70
36,Logistic Regression,correct_train_only_variance,0.6666666666666666,70
36,Random Forest,correct_train_only_variance,0.8095238095238095,70
36,SVM,correct_train_only_variance,0.3333333333333333,70
36,Logistic Regression,leaky_full_data_variance,0.2857142857142857,71
36,Random Forest,leaky_full_data_variance,0.6666666666666666,71
36,SVM,leaky_full_data_variance,0.5238095238095238,71
36,Logistic Regression,correct_train_only_variance,0.47619047619047616,71
36,Random Forest,correct_train_only_variance,0.6190476190476191,71
36,SVM,correct_train_only_variance,0.47619047619047616,71
```

### ./multi_cancer/outputs/COADREAD/results/ablation_leakage_significance.csv

```csv
threshold_m,model,leaky_condition,correct_condition,mean_inflation,wilcoxon_p,ttest_p,n_pairs,significant_at_05
18,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,0.0237,0.4235,0.3222,30,False
18,Random Forest,leaky_full_data_variance,correct_train_only_variance,0.0355,0.0874,0.0963,30,False
18,SVM,leaky_full_data_variance,correct_train_only_variance,0.0491,0.0627,0.0507,30,False
24,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,0.0443,0.1104,0.0699,30,False
24,Random Forest,leaky_full_data_variance,correct_train_only_variance,0.0141,0.5087,0.4652,30,False
24,SVM,leaky_full_data_variance,correct_train_only_variance,-0.0036,0.6654,0.9073,30,False
36,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,-0.0167,0.5148,0.4219,30,False
36,Random Forest,leaky_full_data_variance,correct_train_only_variance,0.0024,0.5128,0.9119,30,False
36,SVM,leaky_full_data_variance,correct_train_only_variance,0.0095,0.3826,0.5604,30,False
```

### ./multi_cancer/outputs/COADREAD/results/ablation_leakage_summary.csv

```csv
threshold_m,model,mean_correct_train_only_variance,mean_leaky_full_data_variance,std_correct_train_only_variance,std_leaky_full_data_variance,auc_inflation
18,Logistic Regression,0.4579,0.4816,0.1467,0.1393,0.0237
18,Random Forest,0.5447,0.5803,0.1568,0.1595,0.0355
18,SVM,0.4754,0.5246,0.1423,0.1226,0.0491
24,Logistic Regression,0.4969,0.5411,0.1974,0.1954,0.0443
24,Random Forest,0.5172,0.5312,0.1866,0.1745,0.0141
24,SVM,0.399,0.3953,0.1578,0.1729,-0.0036
36,Logistic Regression,0.5524,0.5357,0.153,0.1912,-0.0167
36,Random Forest,0.6024,0.6048,0.1663,0.1933,0.0024
36,SVM,0.4381,0.4476,0.1412,0.1305,0.0095
```

### ./multi_cancer/outputs/COADREAD/results/ablation_split_variance_raw.csv

Total data rows: 270 (header + 270 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,auc,seed
```
FIRST 20 DATA ROWS:
```csv
18,Logistic Regression,0.31578947368421056,42
18,Random Forest,0.1578947368421053,42
18,SVM,0.5526315789473684,42
18,Logistic Regression,0.39473684210526316,43
18,Random Forest,0.5,43
18,SVM,0.5,43
18,Logistic Regression,0.2894736842105263,44
18,Random Forest,0.6842105263157895,44
18,SVM,0.6842105263157895,44
18,Logistic Regression,0.5,45
18,Random Forest,0.8157894736842105,45
18,SVM,0.2894736842105263,45
18,Logistic Regression,0.4736842105263158,46
18,Random Forest,0.75,46
18,SVM,0.4210526315789474,46
18,Logistic Regression,0.5263157894736843,47
18,Random Forest,0.34210526315789475,47
18,SVM,0.44736842105263164,47
18,Logistic Regression,0.4736842105263158,48
18,Random Forest,0.5526315789473685,48
```
LAST 20 DATA ROWS:
```csv
36,Random Forest,0.5714285714285714,65
36,SVM,0.47619047619047616,65
36,Logistic Regression,0.47619047619047616,66
36,Random Forest,0.6666666666666666,66
36,SVM,0.3333333333333333,66
36,Logistic Regression,0.47619047619047616,67
36,Random Forest,0.5238095238095237,67
36,SVM,0.47619047619047616,67
36,Logistic Regression,0.6190476190476191,68
36,Random Forest,0.7142857142857143,68
36,SVM,0.5714285714285714,68
36,Logistic Regression,0.5238095238095238,69
36,Random Forest,0.5238095238095238,69
36,SVM,0.33333333333333337,69
36,Logistic Regression,0.6666666666666666,70
36,Random Forest,0.8095238095238095,70
36,SVM,0.3333333333333333,70
36,Logistic Regression,0.47619047619047616,71
36,Random Forest,0.6190476190476191,71
36,SVM,0.47619047619047616,71
```

### ./multi_cancer/outputs/COADREAD/results/ablation_split_variance_summary.csv

```csv
threshold_m,model,mean,std,min,max
18,Logistic Regression,0.4579,0.1467,0.1053,0.8421
18,Random Forest,0.5447,0.1568,0.1579,0.8684
18,SVM,0.4754,0.1423,0.1053,0.7895
24,Logistic Regression,0.4969,0.1974,0.0938,0.875
24,Random Forest,0.5172,0.1866,0.1875,0.875
24,SVM,0.399,0.1578,0.0938,0.75
36,Logistic Regression,0.5524,0.153,0.2857,0.9524
36,Random Forest,0.6024,0.1663,0.2857,1.0
36,SVM,0.4381,0.1412,0.1905,0.8095
```

### ./multi_cancer/outputs/COADREAD/results/ablation_supervised_leakage_raw.csv

Total data rows: 540 (header + 540 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,condition,auc,seed
```
FIRST 20 DATA ROWS:
```csv
18,Logistic Regression,supervised_leaky_full_data_fscore,0.868421052631579,42
18,Random Forest,supervised_leaky_full_data_fscore,0.6052631578947368,42
18,SVM,supervised_leaky_full_data_fscore,0.9473684210526316,42
18,Logistic Regression,supervised_correct_train_only_fscore,0.4210526315789474,42
18,Random Forest,supervised_correct_train_only_fscore,0.4210526315789474,42
18,SVM,supervised_correct_train_only_fscore,0.13157894736842107,42
18,Logistic Regression,supervised_leaky_full_data_fscore,0.5,43
18,Random Forest,supervised_leaky_full_data_fscore,0.736842105263158,43
18,SVM,supervised_leaky_full_data_fscore,0.9736842105263158,43
18,Logistic Regression,supervised_correct_train_only_fscore,0.4736842105263158,43
18,Random Forest,supervised_correct_train_only_fscore,0.4605263157894737,43
18,SVM,supervised_correct_train_only_fscore,0.4736842105263158,43
18,Logistic Regression,supervised_leaky_full_data_fscore,0.9473684210526316,44
18,Random Forest,supervised_leaky_full_data_fscore,0.9210526315789473,44
18,SVM,supervised_leaky_full_data_fscore,1.0,44
18,Logistic Regression,supervised_correct_train_only_fscore,0.736842105263158,44
18,Random Forest,supervised_correct_train_only_fscore,0.6842105263157896,44
18,SVM,supervised_correct_train_only_fscore,0.9210526315789473,44
18,Logistic Regression,supervised_leaky_full_data_fscore,0.9473684210526316,45
18,Random Forest,supervised_leaky_full_data_fscore,0.9736842105263158,45
```
LAST 20 DATA ROWS:
```csv
36,Random Forest,supervised_correct_train_only_fscore,0.6666666666666667,68
36,SVM,supervised_correct_train_only_fscore,0.3333333333333333,68
36,Logistic Regression,supervised_leaky_full_data_fscore,1.0,69
36,Random Forest,supervised_leaky_full_data_fscore,0.8571428571428572,69
36,SVM,supervised_leaky_full_data_fscore,1.0,69
36,Logistic Regression,supervised_correct_train_only_fscore,0.5238095238095237,69
36,Random Forest,supervised_correct_train_only_fscore,0.5476190476190477,69
36,SVM,supervised_correct_train_only_fscore,0.47619047619047616,69
36,Logistic Regression,supervised_leaky_full_data_fscore,1.0,70
36,Random Forest,supervised_leaky_full_data_fscore,1.0,70
36,SVM,supervised_leaky_full_data_fscore,1.0,70
36,Logistic Regression,supervised_correct_train_only_fscore,0.5238095238095238,70
36,Random Forest,supervised_correct_train_only_fscore,0.8095238095238095,70
36,SVM,supervised_correct_train_only_fscore,0.4761904761904762,70
36,Logistic Regression,supervised_leaky_full_data_fscore,1.0,71
36,Random Forest,supervised_leaky_full_data_fscore,1.0,71
36,SVM,supervised_leaky_full_data_fscore,1.0,71
36,Logistic Regression,supervised_correct_train_only_fscore,0.8095238095238095,71
36,Random Forest,supervised_correct_train_only_fscore,0.8095238095238095,71
36,SVM,supervised_correct_train_only_fscore,0.6190476190476191,71
```

### ./multi_cancer/outputs/COADREAD/results/ablation_supervised_leakage_significance.csv

```csv
threshold_m,model,leaky_condition,correct_condition,mean_inflation,wilcoxon_p,ttest_p,n_pairs,significant_at_05
18,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.307,0.0,0.0,30,True
18,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2228,0.0,0.0,30,True
18,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.4026,0.0,0.0,30,True
24,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.3099,0.0,0.0,30,True
24,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2312,0.0,0.0,30,True
24,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.4182,0.0,0.0,30,True
36,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.4016,0.0,0.0,30,True
36,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2611,0.0,0.0,30,True
36,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.4135,0.0,0.0,30,True
```

### ./multi_cancer/outputs/COADREAD/results/ablation_supervised_leakage_summary.csv

```csv
threshold_m,model,mean_supervised_correct_train_only_fscore,mean_supervised_leaky_full_data_fscore,std_supervised_correct_train_only_fscore,std_supervised_leaky_full_data_fscore,auc_inflation
18,Logistic Regression,0.5912,0.8982,0.1941,0.1192,0.307
18,Random Forest,0.5759,0.7987,0.1704,0.1542,0.2228
18,SVM,0.5807,0.9833,0.2071,0.0342,0.4026
24,Logistic Regression,0.5964,0.9062,0.1706,0.1076,0.3099
24,Random Forest,0.5823,0.8135,0.1513,0.1147,0.2313
24,SVM,0.5734,0.9917,0.2269,0.0182,0.4182
36,Logistic Regression,0.5714,0.973,0.1734,0.0427,0.4016
36,Random Forest,0.6262,0.8873,0.1493,0.1054,0.2611
36,SVM,0.5817,0.9952,0.1891,0.0145,0.4135
```

### ./multi_cancer/outputs/LUAD/results/ablation_leakage_raw.csv

Total data rows: 540 (header + 540 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,condition,auc,seed
```
FIRST 20 DATA ROWS:
```csv
12,Logistic Regression,leaky_full_data_variance,0.4479166666666667,42
12,Random Forest,leaky_full_data_variance,0.33333333333333337,42
12,SVM,leaky_full_data_variance,0.625,42
12,Logistic Regression,correct_train_only_variance,0.5416666666666666,42
12,Random Forest,correct_train_only_variance,0.265625,42
12,SVM,correct_train_only_variance,0.59375,42
12,Logistic Regression,leaky_full_data_variance,0.78125,43
12,Random Forest,leaky_full_data_variance,0.6354166666666666,43
12,SVM,leaky_full_data_variance,0.3958333333333333,43
12,Logistic Regression,correct_train_only_variance,0.7395833333333334,43
12,Random Forest,correct_train_only_variance,0.5729166666666666,43
12,SVM,correct_train_only_variance,0.40624999999999994,43
12,Logistic Regression,leaky_full_data_variance,0.40625,44
12,Random Forest,leaky_full_data_variance,0.41145833333333337,44
12,SVM,leaky_full_data_variance,0.71875,44
12,Logistic Regression,correct_train_only_variance,0.35416666666666663,44
12,Random Forest,correct_train_only_variance,0.30208333333333337,44
12,SVM,correct_train_only_variance,0.71875,44
12,Logistic Regression,leaky_full_data_variance,0.625,45
12,Random Forest,leaky_full_data_variance,0.33333333333333337,45
```
LAST 20 DATA ROWS:
```csv
24,Random Forest,correct_train_only_variance,0.554945054945055,68
24,SVM,correct_train_only_variance,0.34065934065934067,68
24,Logistic Regression,leaky_full_data_variance,0.5384615384615384,69
24,Random Forest,leaky_full_data_variance,0.5384615384615384,69
24,SVM,leaky_full_data_variance,0.42857142857142855,69
24,Logistic Regression,correct_train_only_variance,0.5604395604395604,69
24,Random Forest,correct_train_only_variance,0.6263736263736264,69
24,SVM,correct_train_only_variance,0.4505494505494505,69
24,Logistic Regression,leaky_full_data_variance,0.3626373626373626,70
24,Random Forest,leaky_full_data_variance,0.4505494505494505,70
24,SVM,leaky_full_data_variance,0.5054945054945055,70
24,Logistic Regression,correct_train_only_variance,0.31868131868131866,70
24,Random Forest,correct_train_only_variance,0.5384615384615384,70
24,SVM,correct_train_only_variance,0.41758241758241754,70
24,Logistic Regression,leaky_full_data_variance,0.5384615384615383,71
24,Random Forest,leaky_full_data_variance,0.5714285714285715,71
24,SVM,leaky_full_data_variance,0.5274725274725274,71
24,Logistic Regression,correct_train_only_variance,0.49450549450549447,71
24,Random Forest,correct_train_only_variance,0.5659340659340659,71
24,SVM,correct_train_only_variance,0.5274725274725274,71
```

### ./multi_cancer/outputs/LUAD/results/ablation_leakage_significance.csv

```csv
threshold_m,model,leaky_condition,correct_condition,mean_inflation,wilcoxon_p,ttest_p,n_pairs,significant_at_05
12,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,0.0028,0.6319,0.7791,30,False
12,Random Forest,leaky_full_data_variance,correct_train_only_variance,0.0056,0.5304,0.6988,30,False
12,SVM,leaky_full_data_variance,correct_train_only_variance,0.0059,0.8197,0.5595,30,False
18,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,-0.0067,0.5304,0.5875,30,False
18,Random Forest,leaky_full_data_variance,correct_train_only_variance,0.0108,0.2368,0.2461,30,False
18,SVM,leaky_full_data_variance,correct_train_only_variance,-0.0041,0.8626,0.8332,30,False
24,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,0.0311,0.0029,0.0034,30,True
24,Random Forest,leaky_full_data_variance,correct_train_only_variance,-0.0132,0.2097,0.2836,30,False
24,SVM,leaky_full_data_variance,correct_train_only_variance,0.0022,0.9223,0.7997,30,False
```

### ./multi_cancer/outputs/LUAD/results/ablation_leakage_summary.csv

```csv
threshold_m,model,mean_correct_train_only_variance,mean_leaky_full_data_variance,std_correct_train_only_variance,std_leaky_full_data_variance,auc_inflation
12,Logistic Regression,0.5962,0.599,0.1514,0.1466,0.0028
12,Random Forest,0.4918,0.4974,0.1477,0.1451,0.0056
12,SVM,0.4979,0.5038,0.1409,0.1277,0.0059
18,Logistic Regression,0.6921,0.6854,0.109,0.1155,-0.0067
18,Random Forest,0.6007,0.6115,0.1372,0.1243,0.0108
18,SVM,0.4904,0.4863,0.1902,0.1997,-0.0041
24,Logistic Regression,0.5575,0.5886,0.127,0.1182,0.0311
24,Random Forest,0.5731,0.5599,0.1051,0.1089,-0.0132
24,SVM,0.4344,0.4366,0.103,0.0912,0.0022
```

### ./multi_cancer/outputs/LUAD/results/ablation_split_variance_raw.csv

Total data rows: 270 (header + 270 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,auc,seed
```
FIRST 20 DATA ROWS:
```csv
12,Logistic Regression,0.5416666666666666,42
12,Random Forest,0.265625,42
12,SVM,0.59375,42
12,Logistic Regression,0.7395833333333334,43
12,Random Forest,0.5729166666666666,43
12,SVM,0.40624999999999994,43
12,Logistic Regression,0.35416666666666663,44
12,Random Forest,0.30208333333333337,44
12,SVM,0.71875,44
12,Logistic Regression,0.5729166666666666,45
12,Random Forest,0.4322916666666667,45
12,SVM,0.5104166666666666,45
12,Logistic Regression,0.53125,46
12,Random Forest,0.5520833333333333,46
12,SVM,0.5208333333333334,46
12,Logistic Regression,0.6354166666666667,47
12,Random Forest,0.34895833333333337,47
12,SVM,0.42708333333333326,47
12,Logistic Regression,0.42708333333333337,48
12,Random Forest,0.53125,48
```
LAST 20 DATA ROWS:
```csv
24,Random Forest,0.5494505494505494,65
24,SVM,0.5164835164835164,65
24,Logistic Regression,0.5824175824175823,66
24,Random Forest,0.48351648351648346,66
24,SVM,0.32967032967032966,66
24,Logistic Regression,0.5054945054945055,67
24,Random Forest,0.5384615384615384,67
24,SVM,0.42857142857142855,67
24,Logistic Regression,0.7582417582417583,68
24,Random Forest,0.554945054945055,68
24,SVM,0.34065934065934067,68
24,Logistic Regression,0.5604395604395604,69
24,Random Forest,0.6263736263736264,69
24,SVM,0.4505494505494505,69
24,Logistic Regression,0.31868131868131866,70
24,Random Forest,0.5384615384615384,70
24,SVM,0.41758241758241754,70
24,Logistic Regression,0.49450549450549447,71
24,Random Forest,0.5659340659340659,71
24,SVM,0.5274725274725274,71
```

### ./multi_cancer/outputs/LUAD/results/ablation_split_variance_summary.csv

```csv
threshold_m,model,mean,std,min,max
12,Logistic Regression,0.5962,0.1514,0.3333,0.9167
12,Random Forest,0.4918,0.1477,0.2448,0.75
12,SVM,0.4979,0.1409,0.25,0.75
18,Logistic Regression,0.6921,0.109,0.4123,0.8509
18,Random Forest,0.6007,0.1372,0.2719,0.8772
18,SVM,0.4904,0.1902,0.0526,0.7193
24,Logistic Regression,0.5575,0.127,0.3187,0.8462
24,Random Forest,0.5731,0.1051,0.3846,0.7802
24,SVM,0.4344,0.103,0.2747,0.6923
```

### ./multi_cancer/outputs/LUAD/results/ablation_supervised_leakage_raw.csv

Total data rows: 540 (header + 540 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,condition,auc,seed
```
FIRST 20 DATA ROWS:
```csv
12,Logistic Regression,supervised_leaky_full_data_fscore,0.48958333333333337,42
12,Random Forest,supervised_leaky_full_data_fscore,0.671875,42
12,SVM,supervised_leaky_full_data_fscore,1.0,42
12,Logistic Regression,supervised_correct_train_only_fscore,0.42708333333333337,42
12,Random Forest,supervised_correct_train_only_fscore,0.39583333333333337,42
12,SVM,supervised_correct_train_only_fscore,0.5729166666666667,42
12,Logistic Regression,supervised_leaky_full_data_fscore,1.0,43
12,Random Forest,supervised_leaky_full_data_fscore,0.9895833333333334,43
12,SVM,supervised_leaky_full_data_fscore,1.0,43
12,Logistic Regression,supervised_correct_train_only_fscore,0.5625,43
12,Random Forest,supervised_correct_train_only_fscore,0.6614583333333334,43
12,SVM,supervised_correct_train_only_fscore,0.65625,43
12,Logistic Regression,supervised_leaky_full_data_fscore,0.7916666666666667,44
12,Random Forest,supervised_leaky_full_data_fscore,0.7083333333333334,44
12,SVM,supervised_leaky_full_data_fscore,1.0,44
12,Logistic Regression,supervised_correct_train_only_fscore,0.3333333333333333,44
12,Random Forest,supervised_correct_train_only_fscore,0.5416666666666666,44
12,SVM,supervised_correct_train_only_fscore,0.35416666666666663,44
12,Logistic Regression,supervised_leaky_full_data_fscore,1.0,45
12,Random Forest,supervised_leaky_full_data_fscore,0.9479166666666666,45
```
LAST 20 DATA ROWS:
```csv
24,Random Forest,supervised_correct_train_only_fscore,0.6813186813186813,68
24,SVM,supervised_correct_train_only_fscore,0.6538461538461537,68
24,Logistic Regression,supervised_leaky_full_data_fscore,0.989010989010989,69
24,Random Forest,supervised_leaky_full_data_fscore,0.901098901098901,69
24,SVM,supervised_leaky_full_data_fscore,0.8461538461538463,69
24,Logistic Regression,supervised_correct_train_only_fscore,0.7582417582417582,69
24,Random Forest,supervised_correct_train_only_fscore,0.6153846153846154,69
24,SVM,supervised_correct_train_only_fscore,0.6593406593406592,69
24,Logistic Regression,supervised_leaky_full_data_fscore,0.9010989010989011,70
24,Random Forest,supervised_leaky_full_data_fscore,0.8076923076923077,70
24,SVM,supervised_leaky_full_data_fscore,0.9120879120879121,70
24,Logistic Regression,supervised_correct_train_only_fscore,0.4505494505494505,70
24,Random Forest,supervised_correct_train_only_fscore,0.532967032967033,70
24,SVM,supervised_correct_train_only_fscore,0.5494505494505495,70
24,Logistic Regression,supervised_leaky_full_data_fscore,0.912087912087912,71
24,Random Forest,supervised_leaky_full_data_fscore,0.8571428571428571,71
24,SVM,supervised_leaky_full_data_fscore,0.8681318681318682,71
24,Logistic Regression,supervised_correct_train_only_fscore,0.5714285714285714,71
24,Random Forest,supervised_correct_train_only_fscore,0.5824175824175823,71
24,SVM,supervised_correct_train_only_fscore,0.5824175824175823,71
```

### ./multi_cancer/outputs/LUAD/results/ablation_supervised_leakage_significance.csv

```csv
threshold_m,model,leaky_condition,correct_condition,mean_inflation,wilcoxon_p,ttest_p,n_pairs,significant_at_05
12,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2382,0.0,0.0,30,True
12,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2887,0.0,0.0,30,True
12,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.4493,0.0,0.0,30,True
18,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.3175,0.0,0.0,30,True
18,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2301,0.0,0.0,30,True
18,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.4042,0.0,0.0,30,True
24,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.3875,0.0,0.0,30,True
24,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2383,0.0,0.0,30,True
24,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.3269,0.0,0.0,30,True
```

### ./multi_cancer/outputs/LUAD/results/ablation_supervised_leakage_summary.csv

```csv
threshold_m,model,mean_supervised_correct_train_only_fscore,mean_supervised_leaky_full_data_fscore,std_supervised_correct_train_only_fscore,std_supervised_leaky_full_data_fscore,auc_inflation
12,Logistic Regression,0.5486,0.7868,0.1351,0.157,0.2382
12,Random Forest,0.5672,0.8559,0.1269,0.1092,0.2887
12,SVM,0.5385,0.9878,0.1478,0.0311,0.4493
18,Logistic Regression,0.6365,0.9541,0.1115,0.0505,0.3175
18,Random Forest,0.627,0.8572,0.1375,0.1175,0.2301
18,SVM,0.5224,0.9266,0.1148,0.0674,0.4042
24,Logistic Regression,0.5711,0.9586,0.1232,0.0312,0.3875
24,Random Forest,0.5892,0.8275,0.1069,0.0749,0.2383
24,SVM,0.5775,0.9044,0.1275,0.0599,0.3269
```

### ./multi_cancer/outputs/comparison/all_cancers_ablation_raw.csv

```csv
threshold_m,model,mean_supervised_correct_train_only_fscore,mean_supervised_leaky_full_data_fscore,std_supervised_correct_train_only_fscore,std_supervised_leaky_full_data_fscore,auc_inflation,cancer,cancer_name
12,Logistic Regression,0.5496,0.5455,0.2005,0.2789,-0.0041,OV,Ovarian (HGSOC)
12,Random Forest,0.603,0.8232,0.2208,0.1394,0.2201,OV,Ovarian (HGSOC)
12,SVM,0.4476,0.9996,0.2114,0.0022,0.552,OV,Ovarian (HGSOC)
18,Logistic Regression,0.7311,0.7956,0.1049,0.1935,0.0645,OV,Ovarian (HGSOC)
18,Random Forest,0.6691,0.8925,0.1175,0.061,0.2235,OV,Ovarian (HGSOC)
18,SVM,0.6605,0.9989,0.1433,0.003,0.3384,OV,Ovarian (HGSOC)
24,Logistic Regression,0.6779,0.8973,0.0926,0.0929,0.2193,OV,Ovarian (HGSOC)
24,Random Forest,0.7326,0.8494,0.0914,0.0913,0.1168,OV,Ovarian (HGSOC)
24,SVM,0.6681,0.9486,0.1058,0.0395,0.2805,OV,Ovarian (HGSOC)
12,Logistic Regression,0.5486,0.7868,0.1351,0.157,0.2382,LUAD,Lung Adeno
12,Random Forest,0.5672,0.8559,0.1269,0.1092,0.2887,LUAD,Lung Adeno
12,SVM,0.5385,0.9878,0.1478,0.0311,0.4493,LUAD,Lung Adeno
18,Logistic Regression,0.6365,0.9541,0.1115,0.0505,0.3175,LUAD,Lung Adeno
18,Random Forest,0.627,0.8572,0.1375,0.1175,0.2301,LUAD,Lung Adeno
18,SVM,0.5224,0.9266,0.1148,0.0674,0.4042,LUAD,Lung Adeno
24,Logistic Regression,0.5711,0.9586,0.1232,0.0312,0.3875,LUAD,Lung Adeno
24,Random Forest,0.5892,0.8275,0.1069,0.0749,0.2383,LUAD,Lung Adeno
24,SVM,0.5775,0.9044,0.1275,0.0599,0.3269,LUAD,Lung Adeno
18,Logistic Regression,0.5912,0.8982,0.1941,0.1192,0.307,COADREAD,Colorectal
18,Random Forest,0.5759,0.7987,0.1704,0.1542,0.2228,COADREAD,Colorectal
18,SVM,0.5807,0.9833,0.2071,0.0342,0.4026,COADREAD,Colorectal
24,Logistic Regression,0.5964,0.9062,0.1706,0.1076,0.3099,COADREAD,Colorectal
24,Random Forest,0.5823,0.8135,0.1513,0.1147,0.2313,COADREAD,Colorectal
24,SVM,0.5734,0.9917,0.2269,0.0182,0.4182,COADREAD,Colorectal
36,Logistic Regression,0.5714,0.973,0.1734,0.0427,0.4016,COADREAD,Colorectal
36,Random Forest,0.6262,0.8873,0.1493,0.1054,0.2611,COADREAD,Colorectal
36,SVM,0.5817,0.9952,0.1891,0.0145,0.4135,COADREAD,Colorectal
```

### ./multi_cancer/outputs/comparison/cross_cancer_leakage_by_model.csv

```csv
model,threshold_m,Ovarian (HGSOC),Lung Adeno,Colorectal
Logistic Regression,12,-0.0041,0.2382,
Logistic Regression,18,0.0645,0.3175,0.307
Logistic Regression,24,0.2193,0.3875,0.3099
Logistic Regression,36,,,0.4016
Random Forest,12,0.2201,0.2887,
Random Forest,18,0.2235,0.2301,0.2228
Random Forest,24,0.1168,0.2383,0.2313
Random Forest,36,,,0.2611
SVM,12,0.552,0.4493,
SVM,18,0.3384,0.4042,0.4026
SVM,24,0.2805,0.3269,0.4182
SVM,36,,,0.4135
```

### ./multi_cancer/outputs/comparison/cross_cancer_leakage_summary.csv

```csv
Cancer,N_combos,Sup_mean_inf,Sup_max_inf,Sup_min_inf,Unsup_mean_inf,Worst_case
Ovarian (HGSOC),9,0.2234,0.552,-0.0041,0.0106,SVM@12m
Lung Adeno,9,0.3201,0.4493,0.2301,0.0038,SVM@12m
Colorectal,9,0.3298,0.4182,0.2228,0.0176,SVM@24m
```

## outputs/results/ , validation/outputs/

### ./outputs/results/ablation_leakage_raw.csv

Total data rows: 540 (header + 540 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,condition,auc,seed
```
FIRST 20 DATA ROWS:
```csv
12,Logistic Regression,leaky_full_data_variance,0.4756097560975609,42
12,Random Forest,leaky_full_data_variance,0.6219512195121951,42
12,SVM,leaky_full_data_variance,0.5609756097560976,42
12,Logistic Regression,correct_train_only_variance,0.4756097560975609,42
12,Random Forest,correct_train_only_variance,0.4756097560975609,42
12,SVM,correct_train_only_variance,0.4512195121951219,42
18,Logistic Regression,leaky_full_data_variance,0.6776315789473684,42
18,Random Forest,leaky_full_data_variance,0.6414473684210527,42
18,SVM,leaky_full_data_variance,0.6644736842105263,42
18,Logistic Regression,correct_train_only_variance,0.6973684210526316,42
18,Random Forest,correct_train_only_variance,0.611842105263158,42
18,SVM,correct_train_only_variance,0.3355263157894737,42
24,Logistic Regression,leaky_full_data_variance,0.8658008658008659,42
24,Random Forest,leaky_full_data_variance,0.7554112554112554,42
24,SVM,leaky_full_data_variance,0.8138528138528138,42
24,Logistic Regression,correct_train_only_variance,0.9134199134199136,42
24,Random Forest,correct_train_only_variance,0.8246753246753247,42
24,SVM,correct_train_only_variance,0.8528138528138529,42
12,Logistic Regression,leaky_full_data_variance,0.5609756097560976,43
12,Random Forest,leaky_full_data_variance,0.7926829268292683,43
```
LAST 20 DATA ROWS:
```csv
24,Random Forest,correct_train_only_variance,0.696969696969697,70
24,SVM,correct_train_only_variance,0.6623376623376622,70
12,Logistic Regression,leaky_full_data_variance,0.4390243902439024,71
12,Random Forest,leaky_full_data_variance,0.2926829268292683,71
12,SVM,leaky_full_data_variance,0.3658536585365853,71
12,Logistic Regression,correct_train_only_variance,0.4634146341463415,71
12,Random Forest,correct_train_only_variance,0.323170731707317,71
12,SVM,correct_train_only_variance,0.3658536585365853,71
18,Logistic Regression,leaky_full_data_variance,0.6578947368421053,71
18,Random Forest,leaky_full_data_variance,0.6842105263157895,71
18,SVM,leaky_full_data_variance,0.6776315789473685,71
18,Logistic Regression,correct_train_only_variance,0.6710526315789473,71
18,Random Forest,correct_train_only_variance,0.6611842105263157,71
18,SVM,correct_train_only_variance,0.7105263157894737,71
24,Logistic Regression,leaky_full_data_variance,0.6536796536796536,71
24,Random Forest,leaky_full_data_variance,0.6298701298701299,71
24,SVM,leaky_full_data_variance,0.5757575757575757,71
24,Logistic Regression,correct_train_only_variance,0.670995670995671,71
24,Random Forest,correct_train_only_variance,0.7164502164502164,71
24,SVM,correct_train_only_variance,0.6017316017316017,71
```

### ./outputs/results/ablation_leakage_significance.csv

```csv
threshold_m,model,leaky_condition,correct_condition,mean_inflation,wilcoxon_p,ttest_p,n_pairs,significant_at_05
12,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,0.0028,0.6937,0.7993,30,False
12,Random Forest,leaky_full_data_variance,correct_train_only_variance,0.0203,0.3441,0.4586,30,False
12,SVM,leaky_full_data_variance,correct_train_only_variance,0.0528,0.0345,0.0148,30,True
18,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,0.0086,0.8209,0.5374,30,False
18,Random Forest,leaky_full_data_variance,correct_train_only_variance,0.0439,0.0031,0.0029,30,True
18,SVM,leaky_full_data_variance,correct_train_only_variance,0.0195,0.5164,0.148,30,False
24,Logistic Regression,leaky_full_data_variance,correct_train_only_variance,-0.0039,0.4404,0.6072,30,False
24,Random Forest,leaky_full_data_variance,correct_train_only_variance,-0.0089,0.2989,0.3694,30,False
24,SVM,leaky_full_data_variance,correct_train_only_variance,-0.0397,0.0001,0.0,30,True
```

### ./outputs/results/ablation_leakage_summary.csv

```csv
threshold_m,model,mean_correct_train_only_variance,mean_leaky_full_data_variance,std_correct_train_only_variance,std_leaky_full_data_variance,auc_inflation
12,Logistic Regression,0.4569,0.4598,0.2237,0.2394,0.0028
12,Random Forest,0.4085,0.4289,0.1913,0.2011,0.0203
12,SVM,0.3862,0.439,0.1451,0.1765,0.0528
18,Logistic Regression,0.6691,0.6776,0.1023,0.1223,0.0086
18,Random Forest,0.6008,0.6446,0.1073,0.1177,0.0439
18,SVM,0.5857,0.6053,0.1495,0.1527,0.0195
24,Logistic Regression,0.6778,0.6739,0.0941,0.0941,-0.0039
24,Random Forest,0.7252,0.7162,0.1042,0.0952,-0.0089
24,SVM,0.7333,0.6937,0.0836,0.0996,-0.0397
```

### ./outputs/results/ablation_split_variance_raw.csv

Total data rows: 270 (header + 270 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,auc,seed
```
FIRST 20 DATA ROWS:
```csv
12,Logistic Regression,0.4756097560975609,42
12,Random Forest,0.4756097560975609,42
12,SVM,0.4512195121951219,42
12,Logistic Regression,0.6097560975609756,43
12,Random Forest,0.4268292682926829,43
12,SVM,0.3780487804878049,43
12,Logistic Regression,0.4146341463414634,44
12,Random Forest,0.2073170731707317,44
12,SVM,0.5121951219512195,44
12,Logistic Regression,0.2317073170731707,45
12,Random Forest,0.3048780487804878,45
12,SVM,0.2926829268292683,45
12,Logistic Regression,0.975609756097561,46
12,Random Forest,0.6402439024390244,46
12,SVM,0.1829268292682926,46
12,Logistic Regression,0.6097560975609756,47
12,Random Forest,0.4329268292682927,47
12,SVM,0.4756097560975609,47
12,Logistic Regression,0.3902439024390244,48
12,Random Forest,0.4878048780487805,48
```
LAST 20 DATA ROWS:
```csv
24,Random Forest,0.7207792207792206,65
24,SVM,0.8398268398268398,65
24,Logistic Regression,0.6493506493506493,66
24,Random Forest,0.7034632034632033,66
24,SVM,0.632034632034632,66
24,Logistic Regression,0.670995670995671,67
24,Random Forest,0.6731601731601732,67
24,SVM,0.6493506493506493,67
24,Logistic Regression,0.5541125541125541,68
24,Random Forest,0.6147186147186148,68
24,SVM,0.6580086580086579,68
24,Logistic Regression,0.7142857142857142,69
24,Random Forest,0.6839826839826839,69
24,SVM,0.7359307359307359,69
24,Logistic Regression,0.6623376623376623,70
24,Random Forest,0.7099567099567099,70
24,SVM,0.6623376623376622,70
24,Logistic Regression,0.670995670995671,71
24,Random Forest,0.6471861471861472,71
24,SVM,0.6017316017316017,71
```

### ./outputs/results/ablation_split_variance_summary.csv

```csv
threshold_m,model,mean,std,min,max
12,Logistic Regression,0.5415,0.2782,0.2317,0.9756
12,Random Forest,0.411,0.1656,0.2073,0.6402
12,SVM,0.3634,0.13,0.1829,0.5122
18,Logistic Regression,0.6579,0.1061,0.5395,0.7763
18,Random Forest,0.6092,0.0975,0.4671,0.7039
18,SVM,0.5145,0.1432,0.3355,0.6842
24,Logistic Regression,0.7117,0.1336,0.5887,0.9134
24,Random Forest,0.7087,0.084,0.6126,0.8247
24,SVM,0.7714,0.061,0.684,0.8528
```

### ./outputs/results/ablation_supervised_leakage_raw.csv

Total data rows: 540 (header + 540 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,condition,auc,seed
```
FIRST 20 DATA ROWS:
```csv
12,Logistic Regression,supervised_leaky_full_data_fscore,0.5,42
12,Random Forest,supervised_leaky_full_data_fscore,0.951219512195122,42
12,SVM,supervised_leaky_full_data_fscore,1.0,42
12,Logistic Regression,supervised_correct_train_only_fscore,0.6951219512195121,42
12,Random Forest,supervised_correct_train_only_fscore,0.7317073170731707,42
12,SVM,supervised_correct_train_only_fscore,0.4390243902439024,42
18,Logistic Regression,supervised_leaky_full_data_fscore,1.0,42
18,Random Forest,supervised_leaky_full_data_fscore,0.8749999999999999,42
18,SVM,supervised_leaky_full_data_fscore,1.0,42
18,Logistic Regression,supervised_correct_train_only_fscore,0.9013157894736842,42
18,Random Forest,supervised_correct_train_only_fscore,0.694078947368421,42
18,SVM,supervised_correct_train_only_fscore,0.875,42
24,Logistic Regression,supervised_leaky_full_data_fscore,0.9870129870129872,42
24,Random Forest,supervised_leaky_full_data_fscore,0.8744588744588745,42
24,SVM,supervised_leaky_full_data_fscore,0.9783549783549784,42
24,Logistic Regression,supervised_correct_train_only_fscore,0.8181818181818182,42
24,Random Forest,supervised_correct_train_only_fscore,0.829004329004329,42
24,SVM,supervised_correct_train_only_fscore,0.7835497835497836,42
12,Logistic Regression,supervised_leaky_full_data_fscore,0.4756097560975609,43
12,Random Forest,supervised_leaky_full_data_fscore,0.8597560975609756,43
```
LAST 20 DATA ROWS:
```csv
24,Random Forest,supervised_correct_train_only_fscore,0.8160173160173161,70
24,SVM,supervised_correct_train_only_fscore,0.7272727272727272,70
12,Logistic Regression,supervised_leaky_full_data_fscore,0.3658536585365853,71
12,Random Forest,supervised_leaky_full_data_fscore,0.8597560975609757,71
12,SVM,supervised_leaky_full_data_fscore,1.0,71
12,Logistic Regression,supervised_correct_train_only_fscore,0.524390243902439,71
12,Random Forest,supervised_correct_train_only_fscore,0.7439024390243902,71
12,SVM,supervised_correct_train_only_fscore,0.2317073170731707,71
18,Logistic Regression,supervised_leaky_full_data_fscore,0.7368421052631579,71
18,Random Forest,supervised_leaky_full_data_fscore,0.881578947368421,71
18,SVM,supervised_leaky_full_data_fscore,1.0,71
18,Logistic Regression,supervised_correct_train_only_fscore,0.875,71
18,Random Forest,supervised_correct_train_only_fscore,0.7894736842105263,71
18,SVM,supervised_correct_train_only_fscore,0.6907894736842105,71
24,Logistic Regression,supervised_leaky_full_data_fscore,0.9393939393939394,71
24,Random Forest,supervised_leaky_full_data_fscore,0.7987012987012987,71
24,SVM,supervised_leaky_full_data_fscore,0.9696969696969696,71
24,Logistic Regression,supervised_correct_train_only_fscore,0.6060606060606061,71
24,Random Forest,supervised_correct_train_only_fscore,0.7121212121212122,71
24,SVM,supervised_correct_train_only_fscore,0.6796536796536796,71
```

### ./outputs/results/ablation_supervised_leakage_significance.csv

```csv
threshold_m,model,leaky_condition,correct_condition,mean_inflation,wilcoxon_p,ttest_p,n_pairs,significant_at_05
12,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,-0.0041,0.8797,0.9164,30,False
12,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2201,0.0,0.0,30,True
12,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.552,0.0,0.0,30,True
18,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.0645,0.0877,0.078,30,False
18,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2235,0.0,0.0,30,True
18,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.3384,0.0,0.0,30,True
24,Logistic Regression,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2193,0.0,0.0,30,True
24,Random Forest,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.1168,0.0,0.0,30,True
24,SVM,supervised_leaky_full_data_fscore,supervised_correct_train_only_fscore,0.2805,0.0,0.0,30,True
```

### ./outputs/results/ablation_supervised_leakage_summary.csv

```csv
threshold_m,model,mean_supervised_correct_train_only_fscore,mean_supervised_leaky_full_data_fscore,std_supervised_correct_train_only_fscore,std_supervised_leaky_full_data_fscore,auc_inflation
12,Logistic Regression,0.5496,0.5455,0.2005,0.2789,-0.0041
12,Random Forest,0.603,0.8232,0.2208,0.1394,0.2201
12,SVM,0.4476,0.9996,0.2114,0.0022,0.552
18,Logistic Regression,0.7311,0.7956,0.1049,0.1935,0.0645
18,Random Forest,0.6691,0.8925,0.1175,0.061,0.2235
18,SVM,0.6605,0.9989,0.1433,0.003,0.3384
24,Logistic Regression,0.6779,0.8973,0.0926,0.0929,0.2193
24,Random Forest,0.7326,0.8494,0.0914,0.0913,0.1168
24,SVM,0.6681,0.9486,0.1058,0.0395,0.2805
```

### ./outputs/results/clean_auc_table.csv

```csv
threshold_m,model,mean,std,min,max,n_splits
12,Logistic Regression,0.4569,0.2237,0.122,0.9756,30
12,Random Forest,0.4004,0.2003,0.0793,0.8537,30
12,SVM,0.4045,0.1545,0.1463,0.7073,30
18,Logistic Regression,0.6691,0.1023,0.5197,0.9079,30
18,Random Forest,0.6277,0.1054,0.4539,0.9112,30
18,SVM,0.6191,0.1236,0.3355,0.9145,30
24,Logistic Regression,0.6778,0.0941,0.4416,0.9134,30
24,Random Forest,0.7157,0.1082,0.5173,0.9113,30
24,SVM,0.7333,0.0836,0.6017,0.9437,30
```

### ./outputs/results/clean_auc_table_raw.csv

Total data rows: 270 (header + 270 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
threshold_m,model,auc,seed
```
FIRST 20 DATA ROWS:
```csv
12,Logistic Regression,0.47560975609756095,42
12,Random Forest,0.47560975609756095,42
12,SVM,0.4512195121951219,42
12,Logistic Regression,0.6097560975609756,43
12,Random Forest,0.4268292682926829,43
12,SVM,0.3780487804878049,43
12,Logistic Regression,0.4146341463414634,44
12,Random Forest,0.2073170731707317,44
12,SVM,0.5121951219512195,44
12,Logistic Regression,0.23170731707317072,45
12,Random Forest,0.3048780487804878,45
12,SVM,0.2926829268292683,45
12,Logistic Regression,0.975609756097561,46
12,Random Forest,0.6402439024390244,46
12,SVM,0.18292682926829268,46
12,Logistic Regression,0.6097560975609756,47
12,Random Forest,0.4329268292682927,47
12,SVM,0.47560975609756095,47
12,Logistic Regression,0.3902439024390244,48
12,Random Forest,0.4878048780487805,48
```
LAST 20 DATA ROWS:
```csv
24,Random Forest,0.7380952380952381,65
24,SVM,0.8398268398268398,65
24,Logistic Regression,0.6493506493506493,66
24,Random Forest,0.712121212121212,66
24,SVM,0.632034632034632,66
24,Logistic Regression,0.670995670995671,67
24,Random Forest,0.6688311688311688,67
24,SVM,0.6493506493506493,67
24,Logistic Regression,0.5541125541125541,68
24,Random Forest,0.6233766233766234,68
24,SVM,0.6580086580086579,68
24,Logistic Regression,0.7142857142857142,69
24,Random Forest,0.738095238095238,69
24,SVM,0.7359307359307359,69
24,Logistic Regression,0.6623376623376623,70
24,Random Forest,0.6883116883116883,70
24,SVM,0.6623376623376622,70
24,Logistic Regression,0.670995670995671,71
24,Random Forest,0.696969696969697,71
24,SVM,0.6017316017316017,71
```

### ./outputs/results/external_validation_results.csv

```csv
model,threshold,label_set,n_samples,n_class0,n_class1,auc
Logistic Regression,12m,clinical,74,64,10,0.5031
Logistic Regression,18m,clinical,74,64,10,0.4937
Logistic Regression,24m,clinical,74,64,10,0.4906
Random Forest,12m,clinical,74,64,10,0.5117
Random Forest,18m,clinical,74,64,10,0.5805
Random Forest,24m,clinical,74,64,10,0.3563
SVM (RBF),12m,clinical,74,64,10,0.4313
SVM (RBF),18m,clinical,74,64,10,0.4766
SVM (RBF),24m,clinical,74,64,10,0.6031
Logistic Regression,12m,dfs,74,40,34,0.5257
Logistic Regression,18m,dfs,74,40,34,0.5574
Logistic Regression,24m,dfs,74,40,34,0.4559
Random Forest,12m,dfs,74,40,34,0.6
Random Forest,18m,dfs,74,40,34,0.5022
Random Forest,24m,dfs,74,40,34,0.4441
SVM (RBF),12m,dfs,74,40,34,0.4125
SVM (RBF),18m,dfs,74,40,34,0.4596
SVM (RBF),24m,dfs,74,40,34,0.5007
```

### ./outputs/results/label_investigation_candidate_labels.csv

```csv
PATIENT_ID,candidate_response
TCGA-04-1336,0.0
TCGA-04-1346,0.0
TCGA-04-1347,0.0
TCGA-04-1351,0.0
TCGA-04-1361,
TCGA-04-1365,0.0
TCGA-04-1367,1.0
TCGA-04-1516,0.0
TCGA-09-1666,0.0
TCGA-09-1667,0.0
TCGA-09-1668,0.0
TCGA-09-1669,0.0
TCGA-09-1670,0.0
TCGA-09-1674,0.0
TCGA-09-1675,0.0
TCGA-09-2043,0.0
TCGA-09-2044,0.0
TCGA-09-2049,0.0
TCGA-09-2050,0.0
TCGA-09-2051,0.0
TCGA-09-2053,0.0
TCGA-09-2055,0.0
TCGA-13-0901,0.0
TCGA-20-0991,0.0
TCGA-20-1682,0.0
TCGA-20-1683,
TCGA-20-1684,0.0
TCGA-20-1685,0.0
TCGA-20-1686,0.0
TCGA-20-1687,0.0
TCGA-23-1023,0.0
TCGA-23-1024,0.0
TCGA-23-1026,0.0
TCGA-23-1028,0.0
TCGA-23-1029,0.0
TCGA-23-1030,0.0
TCGA-23-1110,0.0
TCGA-23-1118,0.0
TCGA-23-1119,0.0
TCGA-23-1120,0.0
TCGA-23-2077,0.0
TCGA-23-2078,0.0
TCGA-23-2079,0.0
TCGA-23-2643,0.0
TCGA-24-0966,
TCGA-24-0968,
TCGA-24-1413,0.0
TCGA-24-1416,0.0
TCGA-24-1417,0.0
TCGA-24-1418,0.0
TCGA-24-1419,0.0
TCGA-24-1423,0.0
TCGA-24-1424,0.0
TCGA-24-1425,0.0
TCGA-24-1426,0.0
TCGA-24-1427,
TCGA-24-1428,0.0
TCGA-24-1469,0.0
TCGA-24-1470,0.0
TCGA-24-1842,0.0
TCGA-24-1843,0.0
TCGA-24-1847,0.0
TCGA-24-1849,0.0
TCGA-24-1850,0.0
TCGA-24-1920,0.0
TCGA-24-2280,0.0
TCGA-24-2281,0.0
TCGA-29-1693,0.0
TCGA-29-1698,0.0
TCGA-29-1707,0.0
TCGA-29-1711,0.0
TCGA-29-1763,0.0
TCGA-29-1764,0.0
TCGA-29-1769,0.0
TCGA-29-1770,0.0
TCGA-29-1771,0.0
TCGA-29-1774,1.0
TCGA-29-1775,0.0
TCGA-29-1776,
TCGA-29-1777,1.0
TCGA-29-1778,0.0
TCGA-29-1781,0.0
TCGA-29-1784,0.0
TCGA-29-2425,0.0
TCGA-29-2427,0.0
TCGA-29-2428,0.0
TCGA-29-2431,0.0
TCGA-29-2434,0.0
TCGA-29-2436,0.0
TCGA-31-1944,0.0
TCGA-31-1950,
TCGA-31-1953,1.0
TCGA-36-1568,
TCGA-36-1569,
TCGA-36-1570,
TCGA-36-1574,0.0
TCGA-36-1576,0.0
TCGA-36-1577,0.0
TCGA-36-1581,0.0
TCGA-36-2529,0.0
TCGA-36-2530,0.0
TCGA-36-2534,
TCGA-36-2537,
TCGA-36-2538,0.0
TCGA-36-2540,0.0
TCGA-36-2542,0.0
TCGA-36-2544,
TCGA-36-2551,0.0
TCGA-3P-A9WA,0.0
TCGA-42-2587,0.0
TCGA-42-2589,0.0
TCGA-42-2591,0.0
TCGA-57-1992,0.0
TCGA-59-2348,0.0
TCGA-59-2351,0.0
TCGA-59-2363,0.0
TCGA-5X-AA5U,0.0
TCGA-61-1721,0.0
TCGA-61-1722,
TCGA-61-1725,
TCGA-61-1727,0.0
TCGA-61-1728,0.0
TCGA-61-1733,
TCGA-61-1734,0.0
TCGA-61-1737,0.0
TCGA-61-1895,
TCGA-61-1899,0.0
TCGA-61-1900,
TCGA-61-1903,0.0
TCGA-61-1904,0.0
TCGA-61-1907,
TCGA-61-1910,0.0
TCGA-61-1911,0.0
TCGA-61-1913,0.0
TCGA-61-1914,0.0
TCGA-61-1915,0.0
TCGA-61-1995,
TCGA-61-2000,
TCGA-61-2002,1.0
TCGA-61-2003,1.0
TCGA-61-2008,0.0
TCGA-61-2009,0.0
TCGA-61-2017,0.0
TCGA-61-2018,0.0
TCGA-61-2087,0.0
TCGA-61-2092,0.0
TCGA-61-2094,0.0
TCGA-61-2096,1.0
TCGA-61-2097,0.0
TCGA-61-2098,0.0
TCGA-61-2104,0.0
TCGA-61-2111,0.0
TCGA-OY-A56P,0.0
TCGA-OY-A56Q,0.0
```

### ./outputs/results/label_investigation_coverage_sample.csv

```csv
column,n_total_rows,n_non_null,pct_non_null,n_platinum_cohort_rows,n_non_null_platinum_cohort,pct_non_null_platinum_cohort
GRADE,585,480,82.1,489,403,82.4
MSI_SCORE_MANTIS,585,436,74.5,489,371,75.9
MSI_SENSOR_SCORE,585,512,87.5,489,436,89.2
TMB_NONSYNONYMOUS,585,523,89.4,489,446,91.2
ANEUPLOIDY_SCORE,585,552,94.4,489,471,96.3
```

### ./outputs/results/label_investigation_coverage_timeline.csv

```csv
column,n_total_rows,n_non_null,pct_non_null,n_platinum_cohort_rows,n_non_null_platinum_cohort,pct_non_null_platinum_cohort
PRIMARY_THERAPY_OUTCOME_SUCCESS,1470,154,10.5,1287,142,11.0
CLINICAL_STAGE,1470,566,38.5,1287,488,37.9
TUMOR_STATUS,1470,203,13.8,1287,191,14.8
```

### ./outputs/results/label_investigation_crosstab_vs_os.csv

```csv
threshold_m,n_overlap,n_agree,pct_agree,cohens_kappa
12,89,84,94.4,0.0
18,77,75,97.4,0.0
24,67,65,97.0,0.0
```

### ./outputs/results/label_investigation_recall_on_confirmed.csv

```csv
threshold_m,n_confirmed_nonresponders,n_overlap_with_os_labels,n_correctly_flagged_by_os_proxy,recall,recall_ci95_low,recall_ci95_high,missed_patient_ids
12,7,5,0,0.0,0.0,0.522,"['TCGA-04-1367', 'TCGA-29-1774', 'TCGA-29-1777', 'TCGA-61-2002', 'TCGA-61-2096']"
18,7,2,0,0.0,0.0,0.842,"['TCGA-04-1367', 'TCGA-61-2096']"
24,7,2,0,0.0,0.0,0.842,"['TCGA-04-1367', 'TCGA-61-2096']"
```

### ./outputs/results/model_performance_summary.csv

```csv
model,threshold_m,roc_auc,accuracy,precision_class1,recall_class1,f1_class1
Logistic Regression (12m),12,0.4756,0.9535,0.0,0.0,0.0
Random Forest (12m),12,0.4756,0.9535,0.0,0.0,0.0
SVM (12m),12,0.4512,0.9535,0.0,0.0,0.0
Logistic Regression (18m),18,0.6974,0.8571,0.25,0.25,0.25
Random Forest (18m),18,0.6118,0.9048,0.0,0.0,0.0
SVM (18m),18,0.3355,0.9048,0.5,0.25,0.3333
Logistic Regression (24m),24,0.9134,0.9,0.7143,0.7143,0.7143
SVM (24m),24,0.8528,0.875,0.6667,0.5714,0.6154
Random Forest (24m),24,0.8247,0.825,0.0,0.0,0.0
```

### ./validation/outputs/combat_diagnostics.csv

```csv
metric,value,manuscript_value
post_combat_interplatform_pearson_r,-0.00716695212226685,-0.005
geo_variance_ratio_tcga_top500_vs_all,3.70387222510639,1
n_common_genes,15994,NA
n_tcga_selected_genes,500,500
mean_var_selected_genes_in_geo,1.06572255744786,NA
mean_var_all_genes_in_geo,0.287731998480926,NA
```

## phase2/outputs/ (part 1 of full listing)

### ./phase2/outputs/comparison_spearman_correlations.csv

```csv
pair,n_common_genes,spearman_rho,p_value
MDI_vs_Permutation,488,-0.0077454325317924235,0.8644864256281065
MDI_vs_SHAP,488,0.0502017557573033,0.26836007247629445
Permutation_vs_SHAP,536,-0.058298961786594335,0.17775040124356467
```

### ./phase2/outputs/comparison_topN_overlap.csv

```csv
pair,top_n,overlap_count,only_in_a,only_in_b,gained_in_b,dropped_from_a
MDI_vs_Permutation,10,1,9,9,ANXA1;CD59;CHCHD2;DMKN;FAU;LTBP4;PODXL;TFRC;TMEM59,APOA1;EMP2;GNB2L1;HNRNPC;KLK5;NAP1L1;PPT1;PRSS23;TGFBI
MDI_vs_Permutation,50,4,46,46,ACTA2;ANXA1;BCAT1;C1QB;CD59;CD63;CHCHD2;CLIC1;COL3A1;CP;CST3;CYP4B1;DMKN;FAU;FBL;FOSB;FOXP4;GNAS;GPI;HBA2;HDLBP;HSPD1;IFITM2;IGFBP7;LTBP4;MSN;NONO;OAZ1;PABPC4;PODXL;RPL27;RPL3;RPL7A;RPS10;SCARA3;SFRP2;SPON1;TAGLN;TAGLN2;THBS2;THSD4;TMEM59;TNFSF10;TPM4;TRAM1;TRIM28,A2M;ALDOA;AMY1A;APOA1;APP;ARF1;ATP6V1B1;BCAM;COL12A1;DCN;EIF4B;EPCAM;FLNA;GNB2L1;GSN;HNRNPC;HP;HSP90AB1;HSPG2;IFITM3;IGF2;IGFBP4;KLK5;LMNA;LRIG1;MAGED2;MSLN;MT1G;NAP1L1;NDUFB11;PABPC1;PAX8;PPT1;PRDX2;PRSS23;PTGDS;PTPRF;RBM3;RPL27A;RPLP0;RPLP2;SCNN1A;TGFBI;TIMP2;TMEM123;TXNIP
MDI_vs_Permutation,100,20,80,80,ACTA2;ACTG1;ANXA1;AP2M1;APEX1;ATN1;ATP5E;BCAT1;C1QB;C1S;C4A;CD24;CD47;CD59;CD63;CD81;CHCHD2;CLIC1;COL18A1;COL3A1;COL6A1;CST3;CYP4B1;DMKN;FAU;FBL;FN1;FOSB;FOXP4;GIPC1;GPI;GSTP1;HBA2;HDLBP;HLA-DRA;HSPA5;HSPD1;IFITM2;IGFBP7;ITGB1;JUNB;KLK6;LTBP4;LY6E;MSN;NDUFB7;NONO;OAZ1;P4HB;PABPC4;PODXL;PPP1R1B;PUF60;PYY;RPL27;RPL3;RPL35A;RPL41;RPL7A;RPS10;RPS9;SCARA3;SERPINA5;SERPINE1;SFRP2;SLC25A6;SPON1;SULF1;TAGLN;TAGLN2;THBS1;THBS2;THSD4;TMEM59;TNFSF10;TPM4;TRAM1;TRIM28;UBC;ZFP36L1,A2M;ACTN4;ALDOA;AMY1A;APOA1;APOL1;APP;ATP6V1B1;BCAM;CAPNS1;CD74;CHI3L1;COL12A1;COL1A1;CSDE1;DCN;DNAJB1;EEF1D;EEF1G;EIF3CL;EIF3E;EIF4A2;EIF4B;EPCAM;FLNA;GLUL;GNB2L1;GRN;GSN;HLA-DPA1;HNRNPC;HP;HSP90AB1;IFITM3;IGFBP4;KLK5;KRAS;KRT7;KRT8;LAMA5;LMNA;LRIG1;MAGED2;MIF;MT1G;MUC1;MUC16;NAP1L1;NDUFB11;ODC1;PAX8;PCBP2;PDIA4;PLD3;PPT1;PRDX2;PRDX6;PRSS23;PTGDS;PTPRF;RBM3;RPL24;RPL27A;RPL35;RPL36;RPL37A;RPL8;RPLP0;RPLP2;RPS20;RPS23;RPS29;RPS4X;SCNN1A;SERF2;SNRPD2;TGFBI;TIMP2;TMEM123;TXNIP
MDI_vs_Permutation,200,71,129,129,ACTG1;ALPPL2;ANXA1;ANXA2;APEX1;APLP2;ATN1;ATP5E;B2M;BCAT1;BSG;BTG2;C1QB;C4A;CANX;CCT2;CD24;CD59;CD63;CD81;CFB;CFL1;CHCHD2;CLIC1;CLU;COL18A1;COL3A1;COL6A1;CPA2;CRIP1;CRIP2;CST3;CTRC;CYP4B1;EEF1B2;EEF2;ENO1;FAM60A;FAU;FBL;FN1;FOSB;FOXP4;GAPDH;GIPC1;GPI;GPX3;GSTP1;HBA2;HLA-B;HLA-C;HLA-DRA;HLA-E;HMGN2;HSPB1;HSPD1;IFITM1;IFITM2;ISYNA1;ITGB1;KLK10;KLK7;LGALS3BP;LTBP4;LUM;LY6E;MDK;MEST;MFGE8;MMP7;MT2A;MYH9;NDUFB7;NONO;OAZ1;P4HB;PABPC4;PEA15;PERP;PODXL;PPP1R1B;PQBP1;PRDX1;PSAP;PTGES3;PTMS;PUF60;PYY;RPL12;RPL13A;RPL18;RPL19;RPL27;RPL29;RPL3;RPL30;RPL35A;RPL38;RPL5;RPL7A;RPN2;RPS10;RPS11;RPS18;RPS5;RPS6;S100A13;S100A4;SCARA3;SERPINA5;SERPINE1;SFRP2;SLC25A6;SNRNP200;SPARC;SPON1;STAT1;SULF1;TAGLN2;THSD4;TIMP1;TMEM59;TMSB10;TPM4;TRAM1;TRIM28;UBC;UXT;VTCN1,A2M;ACTN4;AGRN;ALDOA;AMY1A;APOE;APP;ATP1A1;ATP5G2;BCAM;BMS1P20;BST2;BTF3;C12orf35;CAPNS1;CAPS;CD9;CHI3L1;CMTM6;COL12A1;COL1A1;COL4A2;CRABP2;CTNNB1;DCN;DHCR24;DNAJB1;ECH1;EEF1A1P9;EIF3CL;EIF3E;EIF4B;EIF4G2;EPCAM;ERGIC3;FLNA;FOS;FSTL1;GANAB;GLUL;GNB2L1;GPX1;GRN;GSN;H19;H3F3B;HNRNPC;HSP90AB1;HSPA1A;IFI6;IFITM3;IGFBP2;IGFBP4;IGJ;JUP;KIAA1522;KLK5;KRAS;KRT7;KRT8;LDHB;LMNA;LYZ;MAGED2;MGP;MIF;MMP11;MT1G;MUC1;MUC16;MYL12B;MYL6;MYL9;NDRG1;NPC2;PAX8;PCBP2;PDIA4;PKM2;PLD3;PRDX2;PRDX6;PTGDS;PTMA;PTPRF;RBM3;RPL13;RPL24;RPL27A;RPL31;RPL32;RPL35;RPL36;RPL37A;RPL7;RPL8;RPLP0;RPLP2;RPN1;RPS12;RPS15A;RPS19;RPS20;RPS21;RPS23;RPS25;RPS29;RPS4X;SCGB2A1;SCNN1A;SERF2;SLC34A2;SNRPD2;SORL1;SRP14;STRAP;TAPBP;TGFBI;TIMP2;TMEM123;TUBA1B;TXNIP;UBA1;UBA2;UBA52;USF2;VIM;XBP1;YWHAE
MDI_vs_SHAP,10,0,10,10,CD59;CMTM6;CTSB;FBL;HDLBP;LTBP4;MEST;MT1G;SAT1;SPINT2,ANPEP;APOA1;EMP2;GNB2L1;HNRNPC;KLK5;NAP1L1;PPT1;PRSS23;TGFBI
MDI_vs_SHAP,50,6,44,44,ACTG1;ANXA1;APLP2;ATP5G2;CD59;CD63;CHCHD2;CMTM6;CP;CTSB;EIF3CL;FAU;FBL;FCGBP;GPX1;H19;HBA2;HDLBP;HMGA1;HSP90AA1;HSPA8;JUNB;LTBP4;LYZ;MDK;MEST;NDUFS5;NONO;NR4A1;PAK1;PGK1;RPN1;SAT1;SERPINE1;SFRP2;SLC38A2;SPINT2;SUPT5H;TM4SF1;TMEM59;TMSL3;TPM4;UBC;UCP2,A2M;ALDOA;AMY1A;APOA1;APP;ARF1;ATP6V1B1;BCAM;COL12A1;DCN;EIF4B;EMP2;EPCAM;FLNA;GNB2L1;GSN;HNRNPC;HP;HSP90AB1;HSPG2;IFITM3;IGFBP4;ITM2B;KLK5;LMNA;LRIG1;MAGED2;MSLN;NAP1L1;PABPC1;PAX8;PPT1;PRDX2;PRSS23;PTGDS;PTPRF;RBM3;RPL27A;RPLP0;RPLP2;TGFBI;TIMP2;TMEM123;TXNIP
MDI_vs_SHAP,100,20,80,80,ACTG1;ALPPL2;ANXA1;APLP2;ATP1A1;ATP5G2;C12orf35;CALM2;CD47;CD59;CD63;CFB;CHCHD2;CMTM6;COL1A2;CPA2;CTSB;ERBB2;FAU;FBL;FCGBP;FN1;FOSB;GIPC1;GPI;GPX1;H19;H3F3B;HBA2;HDLBP;HMGA1;HSP90AA1;HSPA8;IFITM2;IGFBP3;JUNB;LAMC1;LTBP4;LYPD1;LYZ;MAL2;MCL1;MDK;MEST;MMP7;MYL9;NACA;NDUFS5;NONO;NR4A1;PAK1;PFN1;PGK1;PODXL;RPL14;RPL18;RPN1;RPS24;RRBP1;S100A13;SEPT2;SERPINE1;SFRP2;SLC38A2;SPINT2;SPON1;SUPT5H;TACSTD2;THSD4;TM4SF1;TMEM59;TMSL3;TNFSF10;TPM4;TUBA1A;TUBB2C;UBC;UCP2;VIM;ZFP36,ACTN4;AMY1A;APOA1;APOL1;APP;ATP6V1B1;BCAM;CD74;CHI3L1;COL12A1;CSDE1;DCN;DNAJB1;EEF1D;EEF1G;EIF3E;EIF4A2;EIF4B;EMP2;EPCAM;FLNA;GLUL;GNB2L1;GRN;GSN;HLA-DPA1;HNRNPC;HP;HSP90AB1;HSPG2;IFITM3;IGFBP4;ITM2B;KLK5;KRAS;KRT7;KRT8;LAMA5;LMNA;LRIG1;MAGED2;MIF;MMP14;MSLN;MUC1;MUC16;NAP1L1;NCRNA00188;NOTCH2;ODC1;PABPC1;PAX8;PCBP2;PDIA4;PLD3;PLEC;PPT1;PRDX2;PRSS23;PTGDS;PTPRF;RBM3;RPL23A;RPL24;RPL27A;RPL35;RPL37A;RPL8;RPLP0;RPLP2;RPS20;RPS23;RPS29;RPS4X;RPS8;SERF2;TGFBI;TIMP2;TXNIP;UQCRFS1
MDI_vs_SHAP,200,79,121,121,ACTG1;ALPPL2;ANXA1;APLP2;ATP5E;BSG;C1QB;CALM2;CD59;CD63;CD81;CDK16;CEL;CFB;CHCHD2;COL3A1;COL5A1;CPA2;CRABP1;CRIP1;CST3;CTSB;CTSD;EEF2;EIF3K;ERBB2;FAU;FBL;FCGBP;FN1;FOSB;FOXP4;GIPC1;GPI;GSTP1;HBA2;HMGA1;HPN;HSP90AA1;HSPA8;HSPB1;IER2;IFITM1;IFITM2;IGFBP3;ILF3;LAMC1;LGALS3BP;LSR;LTBP4;LYPD1;MAL2;MCL1;MDK;MEST;MMP7;MYCL1;NACA;NDUFS5;NONO;NOTUM;NR4A1;PAK1;PAM;PDIA3;PFN1;PGK1;PHB2;PLXNB2;PODXL;PRDX1;PRSS1;PSMD3;PSMD8;PTGES3;PTGS1;PUF60;PYY;RPL10A;RPL13A;RPL14;RPL18;RPL18A;RPS18;RPS24;RRBP1;S100A13;SEPT2;SERPINE1;SFRP2;SLC25A3;SLC2A1;SLC38A2;SNRNP200;SPINT2;SPON1;SRRM2;SSR2;STAT1;STMN1;SUPT5H;TACSTD2;TAGLN2;THSD4;TM4SF1;TMBIM6;TMEM59;TMSB10;TMSL3;TPI1;TPM4;TRIM28;TSC22D1;TUBA1A;TUBB2C;UBB;UBC;UCP2;UXT;VTCN1;ZFP36,ACTA2;AMY1A;AP2M1;APOA1;APOL1;APP;BCAM;BMS1P20;BST2;C1S;CAPS;CD74;CHI3L1;COL12A1;COL4A2;CSDE1;DCN;DHCR24;DNAJB1;ECH1;EEF1A1P9;EEF1D;EEF1G;EIF3E;EIF3L;EIF4A2;EIF4G2;EMP2;EPCAM;ERGIC3;FLNA;FOLR1;FOS;FSTL1;GANAB;GNB2L1;GRN;GSN;HLA-DPA1;HLA-DRB5;HNRNPC;HP;HSPA5;IFI6;IFITM3;IGFBP2;IGFBP4;IGFBP7;IGJ;ITM2B;JUP;KLK5;KLK6;KRT7;KRT8;LAMA5;LMNA;LTF;MAGED2;MGP;MMP11;MSLN;MSN;MUC1;MUC16;MYL12B;NAP1L1;NCRNA00188;NDRG1;ODC1;PAX8;PCBP2;PDIA4;PLD3;PLEC;PTGDS;RPL13;RPL23A;RPL24;RPL27A;RPL31;RPL32;RPL34;RPL35;RPL41;RPL7;RPL8;RPLP2;RPS12;RPS15A;RPS19;RPS21;RPS23;RPS25;RPS27A;RPS29;RPS4X;RPS8;RPS9;SCGB2A1;SERF2;SERPINH1;SLC34A2;SLPI;SQSTM1;SRP14;ST14;TAGLN;TAPBP;TGFBI;THBS1;TIMP2;TUBA1B;UBA1;UBA2;UBA52;UQCRFS1;USF2;XBP1;YWHAE;ZFP36L1
Permutation_vs_SHAP,10,2,8,8,CMTM6;CTSB;FBL;HDLBP;MEST;MT1G;SAT1;SPINT2,ANPEP;ANXA1;CHCHD2;DMKN;FAU;PODXL;TFRC;TMEM59
Permutation_vs_SHAP,50,16,34,34,ACTG1;APLP2;ATP5G2;CMTM6;CTSB;EIF3CL;FCGBP;GPX1;H19;HMGA1;HSP90AA1;HSPA8;IGF2;JUNB;LYZ;MDK;MEST;MT1G;NDUFB11;NDUFS5;NR4A1;PAK1;PGK1;RPN1;SAT1;SCNN1A;SERPINE1;SLC38A2;SPINT2;SUPT5H;TM4SF1;TMSL3;UBC;UCP2,ACTA2;BCAT1;C1QB;CLIC1;COL3A1;CST3;CYP4B1;DMKN;EMP2;FOSB;FOXP4;GNAS;GPI;HSPD1;IFITM2;IGFBP7;ITM2B;MSN;OAZ1;PABPC4;PODXL;RPL27;RPL3;RPL7A;RPS10;SCARA3;SPON1;TAGLN;TAGLN2;THBS2;THSD4;TNFSF10;TRAM1;TRIM28
Permutation_vs_SHAP,100,35,65,65,A2M;ALDOA;ALPPL2;APLP2;ATP1A1;ATP5G2;C12orf35;CALM2;CAPNS1;CFB;CMTM6;COL1A1;COL1A2;CPA2;CTSB;EIF3CL;ERBB2;FCGBP;GPX1;H19;H3F3B;HMGA1;HSP90AA1;HSPA8;IGFBP3;LAMC1;LYPD1;LYZ;MAL2;MCL1;MDK;MEST;MMP7;MT1G;MYL9;NACA;NDUFB11;NDUFS5;NR4A1;PAK1;PFN1;PGK1;PRDX6;RPL14;RPL18;RPL36;RPN1;RPS24;RRBP1;S100A13;SCNN1A;SEPT2;SLC38A2;SNRPD2;SPINT2;SUPT5H;TACSTD2;TM4SF1;TMEM123;TMSL3;TUBA1A;TUBB2C;UCP2;VIM;ZFP36,ACTA2;AP2M1;APEX1;ATN1;ATP5E;BCAT1;C1QB;C1S;C4A;CD24;CD81;CLIC1;COL18A1;COL3A1;COL6A1;CST3;CYP4B1;DMKN;EMP2;FOXP4;GSTP1;HLA-DRA;HSPA5;HSPD1;HSPG2;IGFBP7;ITGB1;ITM2B;KLK6;LY6E;MMP14;MSLN;MSN;NCRNA00188;NDUFB7;NOTCH2;OAZ1;P4HB;PABPC1;PABPC4;PLEC;PPP1R1B;PUF60;PYY;RPL23A;RPL27;RPL3;RPL35A;RPL41;RPL7A;RPS10;RPS8;RPS9;SCARA3;SERPINA5;SLC25A6;SULF1;TAGLN;TAGLN2;THBS1;THBS2;TRAM1;TRIM28;UQCRFS1;ZFP36L1
Permutation_vs_SHAP,200,87,113,113,A2M;ACTN4;AGRN;ALDOA;APOE;ATP1A1;ATP5G2;BTF3;C12orf35;CALM2;CAPNS1;CD9;CDK16;CEL;CMTM6;COL1A1;COL5A1;CRABP1;CRABP2;CTNNB1;CTSB;CTSD;EIF3CL;EIF3K;EIF4B;ERBB2;FCGBP;GLUL;GPX1;H19;H3F3B;HMGA1;HPN;HSP90AA1;HSP90AB1;HSPA1A;HSPA8;IER2;IGFBP3;ILF3;KIAA1522;KRAS;LAMC1;LDHB;LSR;LYPD1;LYZ;MAL2;MCL1;MIF;MT1G;MYCL1;MYL6;MYL9;NACA;NDUFS5;NOTUM;NPC2;NR4A1;PAK1;PAM;PDIA3;PFN1;PGK1;PHB2;PKM2;PLXNB2;PRDX2;PRDX6;PRSS1;PSMD3;PSMD8;PTGS1;PTMA;PTPRF;RBM3;RPL10A;RPL14;RPL18A;RPL36;RPL37A;RPLP0;RPN1;RPS20;RPS24;RRBP1;SCNN1A;SEPT2;SLC25A3;SLC2A1;SLC38A2;SNRPD2;SORL1;SPINT2;SRRM2;SSR2;STMN1;STRAP;SUPT5H;TACSTD2;TM4SF1;TMBIM6;TMEM123;TMSL3;TPI1;TSC22D1;TUBA1A;TUBB2C;TXNIP;UBB;UCP2;VIM;ZFP36,ACTA2;ANXA2;AP2M1;APEX1;APOA1;APOL1;ATN1;B2M;BCAT1;BTG2;C1S;C4A;CANX;CCT2;CD24;CD74;CFL1;CLIC1;CLU;COL18A1;COL6A1;CRIP2;CSDE1;CTRC;CYP4B1;EEF1B2;EEF1D;EEF1G;EIF3L;EIF4A2;EMP2;ENO1;FAM60A;FOLR1;GAPDH;GPX3;HLA-B;HLA-C;HLA-DPA1;HLA-DRA;HLA-DRB5;HLA-E;HMGN2;HP;HSPA5;HSPD1;IGFBP7;ISYNA1;ITGB1;ITM2B;KLK10;KLK6;KLK7;LAMA5;LTF;LUM;LY6E;MFGE8;MSLN;MSN;MT2A;MYH9;NAP1L1;NCRNA00188;NDUFB7;OAZ1;ODC1;P4HB;PABPC4;PEA15;PERP;PLEC;PPP1R1B;PQBP1;PSAP;PTMS;RPL12;RPL19;RPL23A;RPL27;RPL29;RPL3;RPL30;RPL34;RPL35A;RPL38;RPL41;RPL5;RPL7A;RPN2;RPS10;RPS11;RPS27A;RPS5;RPS6;RPS8;RPS9;S100A4;SCARA3;SERPINA5;SERPINH1;SLC25A6;SLPI;SPARC;SQSTM1;ST14;SULF1;TAGLN;THBS1;TIMP1;TRAM1;UQCRFS1;ZFP36L1
```

### ./phase2/outputs/cox_hazard_ratios.csv

```csv
"Variable","HR","HR_95CI_low","HR_95CI_hi","p_value"
"log(TMB + 1)",0.894,0.7423,1.0768,0.2377
"Aneuploidy Score",1.0213,1.0038,1.0391,0.01686
```

### ./phase2/outputs/cox_patients_with_risk.csv

Total data rows: 432 (header + 432 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
"PATIENT_ID","os_time","os_event","tmb","log_tmb","aneu","lp","risk_group"
```
FIRST 20 DATA ROWS:
```csv
"TCGA-04-1331",43.92280633,1,4.5,1.70474809223843,7,-0.230621843726959,"Low"
"TCGA-04-1336",49.1501463,0,2.233333333,1.17351359673813,7,-0.171100341057578,"Low"
"TCGA-04-1338",46.61866719,0,0,0,14,0.107892659295388,"High"
"TCGA-04-1342",18.5093862,1,5.7,1.90210752639692,12,-0.147371775775626,"Low"
"TCGA-04-1343",11.86836309,1,3.066666667,1.40282366315307,23,0.140368366387351,"High"
"TCGA-04-1347",63.08971957,0,0,0,21,0.255400800753746,"High"
"TCGA-04-1348",48.75563008,1,1.966666667,1.08743898818234,5,-0.20360140278749,"Low"
"TCGA-04-1349",21.56688694,1,1.966666667,1.08743898818234,27,0.259995613224494,"High"
"TCGA-04-1350",63.97738107,1,0,0,24,0.318618575664472,"High"
"TCGA-04-1356",49.28165171,1,2.933333333,1.36948724271876,16,-0.00340463766055149,"Medium"
"TCGA-04-1361",32.51471217,0,4,1.6094379124341,8,-0.198870342550677,"Low"
"TCGA-04-1362",44.31732255,1,2.333333333,1.20397280422594,16,0.0151402199795648,"Medium"
"TCGA-04-1364",33.66538449,1,0,0,31,0.46612671712283,"High"
"TCGA-04-1365",76.5690239,0,0,0,9,0.00252970111084619,"Medium"
"TCGA-04-1367",103.3961272,0,3.9,1.58923520511658,10,-0.154461572277684,"Low"
"TCGA-04-1514",56.54732551,1,0,0,14,0.107892659295388,"High"
"TCGA-04-1516",41.58858533,0,1.766666667,1.01764322625492,10,-0.0904182660093841,"Medium"
"TCGA-04-1517",19.98882204,1,0,0,30,0.445054125485922,"High"
"TCGA-04-1530",119.0781471,1,0,0,18,0.192183025843021,"High"
"TCGA-04-1536",29.09557156,1,0,0,12,0.0657474760215713,"Medium"
```
LAST 20 DATA ROWS:
```csv
"TCGA-61-2088",4.767071046,0,0.6,0.470003629245736,22,0.223812425322952,"High"
"TCGA-61-2092",51.71450176,0,1.966666667,1.08743898818234,1,-0.287891769335124,"Low"
"TCGA-61-2094",71.73620015,0,2.333333333,1.20397280422594,10,-0.111295329841885,"Low"
"TCGA-61-2095",61.64316008,1,6.6,2.02814824729229,2,-0.372219766612331,"Low"
"TCGA-61-2096",58.38840122,0,3.9,1.58923520511658,7,-0.217679347188409,"Low"
"TCGA-61-2098",65.52256962,0,0,0,20,0.234328209116838,"High"
"TCGA-61-2101",55.49528224,1,1.466666667,0.90286771167715,22,0.175312712190324,"High"
"TCGA-61-2102",6.476641352,1,2.233333333,1.17351359673813,18,0.0606981669484142,"Medium"
"TCGA-61-2104",76.86491107,0,2.266666667,1.18377009711046,12,-0.0668865595915297,"Medium"
"TCGA-61-2109",20.67922543,1,2.7,1.30833281965018,9,-0.144060808498114,"Low"
"TCGA-61-2110",44.51458066,1,3.033333333,1.39459316385194,16,-0.0062175991011266,"Medium"
"TCGA-61-2113",22.22441398,1,7.633333333,2.15563067999877,28,0.161384006688267,"High"
"TCGA-61-2610",51.91175987,1,3.033333333,1.39459316385194,8,-0.174798332196393,"Low"
"TCGA-61-2611",15.87927804,1,2.233333333,1.17351359673813,13,-0.0446647912361276,"Medium"
"TCGA-61-2612",6.345135944,1,1.233333333,0.803495237579557,24,0.228591959671873,"High"
"TCGA-61-2613",31.06815268,1,2.6,1.28093384546206,8,-0.162063516441306,"Low"
"TCGA-OY-A56P",39.68175691,0,1.1,0.741937344729377,27,0.298706911468962,"High"
"TCGA-OY-A56Q",18.93677878,0,1.733333333,1.00552186548015,28,0.290246506117978,"High"
"TCGA-VG-A8LO",0.789032449,1,2.366666667,1.21392313527811,8,-0.154555385476778,"Low"
"TCGA-WR-A838",9.99441102,1,1.433333333,0.889262059349249,20,0.134691957164697,"High"
```

### ./phase2/outputs/cox_ph_test.csv

```csv
"","chisq","df","p"
"log_tmb",0.4131315564742,1,0.520384315229547
"aneu",3.26714905583697,1,0.0706803556004864
"GLOBAL",3.44666104209407,2,0.178470756369452
```

### ./phase2/outputs/cox_summary_stats.csv

```csv
"metric","value","manuscript_value"
"n_complete_cases",432,432
"n_events",242,242
"c_index",0.5698,0.57
"c_index_se",0.0214,NA
"km_logrank_p",0.02342,0.023
"schoenfeld_global_p",0.1785,0.178
```

### ./phase2/outputs/cv_comparison_spearman_with12m.csv

```csv
pair,n_common_genes,spearman_rho,p_value
MDI_vs_Permutation,557,0.40631788308856004,1.4834444673293265e-23
MDI_vs_SHAP,557,0.9800408702979122,0.0
Permutation_vs_SHAP,557,0.36614595507239306,4.1068794495776612e-19
```

### ./phase2/outputs/cv_comparison_spearman_without12m.csv

```csv
pair,n_common_genes,spearman_rho,p_value
MDI_vs_Permutation,556,0.4188045245302132,5.0604197829922025e-25
MDI_vs_SHAP,556,0.9748958599145235,0.0
Permutation_vs_SHAP,556,0.3799923969795972,1.5329219500384974e-20
```

### ./phase2/outputs/cv_comparison_topN_overlap_with12m.csv

```csv
pair,top_n,overlap_count,only_in_a,only_in_b,gained_in_b,dropped_from_a
MDI_vs_Permutation,10,6,4,4,ANPEP;ANXA1;FAU;SUPT5H,HDLBP;LTBP4;RHOA;UXT
MDI_vs_Permutation,50,32,18,18,ALDOA;CALR;CFB;CLIC1;COL6A3;CTNNB1;FGFR1;HLA-DPA1;ILF3;LRP1;MMP14;NACA;PSMD8;RPL36;RPL41;RPS19;S100A13;THSD4,ACTG1;APLP2;COL4A2;CP;DDR1;DMKN;GANAB;HBA2;HSPG2;IER2;MDK;MT1G;NR4A1;RHOA;SAT1;SNRPD2;TMSL3;TPM4
MDI_vs_Permutation,100,63,37,37,ACTB;ASS1;CAPNS1;CD9;CEL;CFB;FGFR1;FOXP4;H19;H3F3B;HNRNPA1;HNRNPC;HPN;ILF3;ISYNA1;LRP1;LSR;PDIA6;PSMD3;PSMD8;PSME1;RPL17;RPL27;RPL28;RPL31;RPL38;RPL41;RPL7;RPS10;RPS17;RPS19;RPS29;RPS4X;SERPINH1;STAT1;UQCRFS1;ZFP36,ARL4C;ATP5E;ATP5G2;CALM2;COL4A2;CP;CRABP1;DDR1;DMKN;FBL;GPI;HBA2;HSPA1A;HSPA8;JUNB;MDK;MMP7;NCL;NDUFS5;NR4A1;PAK1;PFN1;PKM2;PKN1;PUF60;RHOA;RPS20;SAT1;SCNN1A;SEPT2;SLC38A1;TAGLN2;THBS2;TMSL3;TPM4;VTCN1;YBX1
MDI_vs_Permutation,200,119,81,81,ACTN4;AGRN;APOE;ASS1;CAPNS1;CCND1;CD9;CEL;CLNS1A;COL12A1;COL6A1;COX6B1;CRABP2;CSDE1;CYR61;EIF1;EIF3E;EIF4G1;EPCAM;ERGIC3;FGFR1;FOXP4;HLA-A;HLA-C;HLA-DRB1;HLA-DRB5;HNRNPA1;HNRNPC;HSP90AB1;HSPD1;IFI6;IGFBP7;IMPDH2;ISYNA1;MMP10;MMP2;MSN;MYH9;NDUFB7;NME2;NORAD;PDIA3;PDIA6;PPP1CB;PQBP1;PRDX1;PRDX6;PRSS1;PSMD3;PSME1;RPL17;RPL18A;RPL26;RPL31;RPL34;RPL35;RPL35A;RPL38;RPL4;RPL41;RPL7;RPS13;RPS14;RPS19;RPS23;RPS29;RPS4X;RPS7;RPS9;S100A1;S100A16;SERPINH1;SLC25A5;SLC2A1;SOD2;SPINK1;TECR;THY1;TPI1;USF2;YAP1,APH1A;ARL4C;ATP5E;ATP5G2;ATP5G3;CALM2;CANX;CDK16;CHI3L1;CMTM6;CP;CPNE1;CSRP1;CST3;DDR1;DMKN;EIF3CL;EIF4A1;EMP2;ENO1;FBL;GIPC1;GLTSCR2;GRN;H3F3A;HBA2;HLA-E;HMGA1;HSPA1A;HSPA8;HSPB1;IFITM2;ITM2B;JUN;JUNB;KIAA1522;LGALS3BP;LMNA;LTF;LUM;LYPD1;MFGE8;MUC5B;NDUFS5;NR4A1;PAK1;PHB2;PKN1;PRDX2;PRSS23;PTMS;PUF60;PYY;RNASE1;RPL11;RPL14;RPS12;RPS20;RPS24;RPS5;S100A6;SCNN1A;SEPT2;SLC38A1;SPON1;SSR2;TACSTD2;TAGLN2;TAPBP;TGM2;THBS2;TMEM123;TMSL3;TNFAIP2;TNFSF10;TUBB;TUBB2C;UBC;UCP2;YBX1;YWHAE
MDI_vs_SHAP,10,10,0,0,,
MDI_vs_SHAP,50,49,1,1,THSD4,C12orf35
MDI_vs_SHAP,100,91,9,9,CFB;HMGA1;LRP1;LYPD1;MMP11;RNASE1;SYNGR2;UBC;ZFP36,ATP5E;CALM2;CAP1;HLA-DQB1;MARCKSL1;MMP7;RPS11;RPS20;YBX1
MDI_vs_SHAP,200,193,7,7,CCND1;GRINA;LRIG1;PAM;RPSA;RRBP1;TSC22D1,GSN;RPL27;RPS17;RPS3A;SPON1;ST14;TUBB
Permutation_vs_SHAP,10,6,4,4,HDLBP;LTBP4;RHOA;UXT,ANPEP;ANXA1;FAU;SUPT5H
Permutation_vs_SHAP,50,32,18,18,ACTG1;APLP2;COL4A2;CP;DDR1;DMKN;GANAB;HBA2;HSPG2;IER2;MDK;MT1G;NR4A1;RHOA;SAT1;SNRPD2;TMSL3;TPM4,ALDOA;C12orf35;CALR;CFB;CLIC1;COL6A3;CTNNB1;FGFR1;HLA-DPA1;ILF3;LRP1;MMP14;NACA;PSMD8;RPL36;RPL41;RPS19;S100A13
Permutation_vs_SHAP,100,62,38,38,ARL4C;ATP5G2;COL4A2;CP;CRABP1;DDR1;DMKN;FBL;GPI;HBA2;HMGA1;HSPA1A;HSPA8;JUNB;LYPD1;MDK;MMP11;NCL;NDUFS5;NR4A1;PAK1;PFN1;PKM2;PKN1;PUF60;RHOA;RNASE1;SAT1;SCNN1A;SEPT2;SLC38A1;SYNGR2;TAGLN2;THBS2;TMSL3;TPM4;UBC;VTCN1,ACTB;ASS1;CAP1;CAPNS1;CD9;CEL;FGFR1;FOXP4;H19;H3F3B;HLA-DQB1;HNRNPA1;HNRNPC;HPN;ILF3;ISYNA1;LSR;MARCKSL1;PDIA6;PSMD3;PSMD8;PSME1;RPL17;RPL27;RPL28;RPL31;RPL38;RPL41;RPL7;RPS10;RPS11;RPS17;RPS19;RPS29;RPS4X;SERPINH1;STAT1;UQCRFS1
Permutation_vs_SHAP,200,115,85,85,APH1A;ARL4C;ATP5E;ATP5G2;ATP5G3;CALM2;CANX;CDK16;CHI3L1;CMTM6;CP;CPNE1;CSRP1;CST3;DDR1;DMKN;EIF3CL;EIF4A1;EMP2;ENO1;FBL;GIPC1;GLTSCR2;GRINA;GRN;H3F3A;HBA2;HLA-E;HMGA1;HSPA1A;HSPA8;HSPB1;IFITM2;ITM2B;JUN;JUNB;KIAA1522;LGALS3BP;LMNA;LRIG1;LTF;LUM;LYPD1;MFGE8;MUC5B;NDUFS5;NR4A1;PAK1;PAM;PHB2;PKN1;PRDX2;PRSS23;PTMS;PUF60;PYY;RNASE1;RPL11;RPL14;RPS12;RPS20;RPS24;RPS5;RPSA;RRBP1;S100A6;SCNN1A;SEPT2;SLC38A1;SSR2;TACSTD2;TAGLN2;TAPBP;TGM2;THBS2;TMEM123;TMSL3;TNFAIP2;TNFSF10;TSC22D1;TUBB2C;UBC;UCP2;YBX1;YWHAE,ACTN4;AGRN;APOE;ASS1;CAPNS1;CD9;CEL;CLNS1A;COL12A1;COL6A1;COX6B1;CRABP2;CSDE1;CYR61;EIF1;EIF3E;EIF4G1;EPCAM;ERGIC3;FGFR1;FOXP4;GSN;HLA-A;HLA-C;HLA-DRB1;HLA-DRB5;HNRNPA1;HNRNPC;HSP90AB1;HSPD1;IFI6;IGFBP7;IMPDH2;ISYNA1;MMP10;MMP2;MSN;MYH9;NDUFB7;NME2;NORAD;PDIA3;PDIA6;PPP1CB;PQBP1;PRDX1;PRDX6;PRSS1;PSMD3;PSME1;RPL17;RPL18A;RPL26;RPL27;RPL31;RPL34;RPL35;RPL35A;RPL38;RPL4;RPL41;RPL7;RPS13;RPS14;RPS17;RPS19;RPS23;RPS29;RPS3A;RPS4X;RPS7;RPS9;S100A1;S100A16;SERPINH1;SLC25A5;SLC2A1;SOD2;SPINK1;ST14;TECR;THY1;TPI1;USF2;YAP1
```

### ./phase2/outputs/cv_comparison_topN_overlap_without12m.csv

```csv
pair,top_n,overlap_count,only_in_a,only_in_b,gained_in_b,dropped_from_a
MDI_vs_Permutation,10,5,5,5,CHCHD2;CTSB;FAU;TFRC;THSD4,HDLBP;LTBP4;NDUFB11;PGK1;RHOA
MDI_vs_Permutation,50,34,16,16,CLIC1;DDR1;FGFR1;HPN;JUNB;PSMD8;RPL27;RPL31;RPL41;RPS11;RPS19;S100A13;SFRP2;ST14;TMSB10;ZFP36,ACTG1;DMKN;HSP90AA1;IGF2;MDK;NR4A1;PAK1;PFN1;PKM2;PUF60;RHOA;SAT1;SCNN1A;SEPT2;TPM4;VTCN1
MDI_vs_Permutation,100,62,38,38,AP2M1;CAP1;CCND1;CD9;COL6A3;COX6B1;CPA2;CRABP2;CST3;FGFR1;H19;HNRNPA1;HNRNPC;HPN;HSP90AB1;IMPDH2;LSR;NME2;P4HB;PRDX6;PSMD3;PSMD8;PSME1;RPL27;RPL31;RPL38;RPL41;RPL7A;RPS13;RPS16;RPS17;RPS19;RPS29;RPS4X;S100A16;SFRP2;UCP2;USF2,ARL4C;ATP5G2;CALM2;COL4A2;CP;DMKN;EEF2;EIF3CL;ENO1;GANAB;GIPC1;H3F3A;H3F3B;KIAA1522;LYPD1;NCL;NDUFS5;NR4A1;PAK1;PKM2;PKN1;PUF60;RHOA;RNASE1;RPL14;RPS12;RPS20;RPS24;SCNN1A;SEPT2;SLC38A1;TAPBP;THBS2;TMSL3;TNFAIP2;TPM4;TXNIP;VTCN1
MDI_vs_Permutation,200,120,80,80,ASS1;ATP5B;CAND1;CCND1;CEL;CLNS1A;CRIP2;CSDE1;CST3;CTGF;CYR61;ECH1;EEF1G;EIF3E;EIF3K;EPCAM;ERGIC3;FGFR1;FOXP4;FTH1;H1F0;HLA-A;HLA-C;HLA-DPA1;HNRNPA1;HSP90AB1;HSPD1;IFI6;IFITM2;IMPDH2;JUN;KLK10;KRT19;LMNA;MMP10;MXRA5;MYL6;NCRNA00188;NME2;NORAD;ODC1;PDIA6;PDXDC1;PPP1CB;PRDX6;PRKCSH;PRSS1;PSMD8;PTMA;RPL17;RPL18A;RPL24;RPL27A;RPL35A;RPL37A;RPL38;RPL4;RPL7;RPS13;RPS14;RPS21;RPS3A;RPS4X;RPS9;S100A16;SCGB2A1;SEPP1;SERPINH1;SFRP2;SLC25A5;SLC2A1;SLPI;SOD2;SPINT2;SPOCK2;TMEM123;TUBA1A;USF2;YWHAZ;ZFP36L1,APEX1;APH1A;ARL4C;CALM2;CANX;CD63;COL5A1;COL5A2;CP;CSRP1;DUSP1;EIF3CL;ENO1;ERBB2;GANAB;GAPDH;GIPC1;GPI;GRINA;H3F3A;H3F3B;HSPA5;HSPA8;HSPB1;IFI27;ITM2B;KIAA1522;LGALS3BP;LRIG1;LYPD1;MFGE8;MMP7;MUC1;MUC5B;MYCL1;NDUFC2;NDUFS5;NR4A1;NUMA1;PABPC4;PAK1;PKN1;PPP1R1B;PRDX2;PTGS1;PTMS;PTPRF;PUF60;RHOA;RNASE1;RPL10A;RPL11;RPL14;RPL36;RPN1;RPN2;RPS12;RPS20;RPS24;RPS5;RPSA;RRBP1;S100A6;SCNN1A;SERPINE1;SLC38A1;SLC40A1;SQSTM1;SRRM2;STRAP;TAPBP;TGFBI;TIMP1;TIMP3;TMSL3;TNFAIP2;TPM4;TSC22D1;TUBB2C;TXNIP
MDI_vs_SHAP,10,10,0,0,,
MDI_vs_SHAP,50,46,4,4,CP;LRP1;PKN1;RNASE1,CTNNB1;IGF2;NACA;PAK1
MDI_vs_SHAP,100,87,13,13,ANXA1;CPA2;CSRP1;HSPA1A;HSPA8;HSPB1;ITM2B;LSR;P4HB;PTMS;SERPINE1;TAGLN2;UBC,ARL4C;COL4A2;EEF2;EIF3CL;H3F3B;RPL18;RPL28;RPS10;RPS20;ST14;TAPBP;TNFAIP2;UQCRFS1
MDI_vs_SHAP,200,187,13,13,CDK16;CFL1;EEF1B2;EIF4A1;GRN;HLA-A;HLA-DRB5;HSP90AB1;IER2;KRAS;LDHA;RPS6;S100A16,AGRN;COL1A1;COL5A2;COX6B1;GAPDH;HSP90B1;HSPA5;PTPRF;RPL26;RPL31;RPL41;RPS29;SLC40A1
Permutation_vs_SHAP,10,5,5,5,HDLBP;LTBP4;NDUFB11;PGK1;RHOA,CHCHD2;CTSB;FAU;TFRC;THSD4
Permutation_vs_SHAP,50,32,18,18,ACTG1;CP;DMKN;HSP90AA1;LRP1;MDK;NR4A1;PFN1;PKM2;PKN1;PUF60;RHOA;RNASE1;SAT1;SCNN1A;SEPT2;TPM4;VTCN1,CLIC1;CTNNB1;DDR1;FGFR1;HPN;JUNB;NACA;PSMD8;RPL27;RPL31;RPL41;RPS11;RPS19;S100A13;SFRP2;ST14;TMSB10;ZFP36
Permutation_vs_SHAP,100,60,40,40,ANXA1;ATP5G2;CALM2;CP;CSRP1;DMKN;ENO1;GANAB;GIPC1;H3F3A;HSPA1A;HSPA8;HSPB1;ITM2B;KIAA1522;LYPD1;NCL;NDUFS5;NR4A1;PAK1;PKM2;PKN1;PTMS;PUF60;RHOA;RNASE1;RPL14;RPS12;RPS24;SCNN1A;SEPT2;SERPINE1;SLC38A1;TAGLN2;THBS2;TMSL3;TPM4;TXNIP;UBC;VTCN1,AP2M1;CAP1;CCND1;CD9;COL6A3;COX6B1;CRABP2;CST3;FGFR1;H19;HNRNPA1;HNRNPC;HPN;HSP90AB1;IMPDH2;NME2;PRDX6;PSMD3;PSMD8;PSME1;RPL18;RPL27;RPL28;RPL31;RPL38;RPL41;RPL7A;RPS10;RPS13;RPS16;RPS17;RPS19;RPS29;RPS4X;S100A16;SFRP2;ST14;UCP2;UQCRFS1;USF2
Permutation_vs_SHAP,200,115,85,85,APEX1;APH1A;ARL4C;CALM2;CANX;CD63;CDK16;CFL1;COL5A1;CP;CSRP1;DUSP1;EEF1B2;EIF3CL;EIF4A1;ENO1;ERBB2;GANAB;GIPC1;GPI;GRINA;GRN;H3F3A;H3F3B;HLA-DRB5;HSPA8;HSPB1;IER2;IFI27;ITM2B;KIAA1522;KRAS;LDHA;LGALS3BP;LRIG1;LYPD1;MFGE8;MMP7;MUC1;MUC5B;MYCL1;NDUFC2;NDUFS5;NR4A1;NUMA1;PABPC4;PAK1;PKN1;PPP1R1B;PRDX2;PTGS1;PTMS;PUF60;RHOA;RNASE1;RPL10A;RPL11;RPL14;RPL36;RPN1;RPN2;RPS12;RPS20;RPS24;RPS5;RPS6;RPSA;RRBP1;S100A6;SCNN1A;SERPINE1;SLC38A1;SQSTM1;SRRM2;STRAP;TAPBP;TGFBI;TIMP1;TIMP3;TMSL3;TNFAIP2;TPM4;TSC22D1;TUBB2C;TXNIP,AGRN;ASS1;ATP5B;CAND1;CCND1;CEL;CLNS1A;COL1A1;COX6B1;CRIP2;CSDE1;CST3;CTGF;CYR61;ECH1;EEF1G;EIF3E;EIF3K;EPCAM;ERGIC3;FGFR1;FOXP4;FTH1;H1F0;HLA-C;HLA-DPA1;HNRNPA1;HSP90B1;HSPD1;IFI6;IFITM2;IMPDH2;JUN;KLK10;KRT19;LMNA;MMP10;MXRA5;MYL6;NCRNA00188;NME2;NORAD;ODC1;PDIA6;PDXDC1;PPP1CB;PRDX6;PRKCSH;PRSS1;PSMD8;PTMA;RPL17;RPL18A;RPL24;RPL26;RPL27A;RPL31;RPL35A;RPL37A;RPL38;RPL4;RPL41;RPL7;RPS13;RPS14;RPS21;RPS29;RPS3A;RPS4X;RPS9;SCGB2A1;SEPP1;SERPINH1;SFRP2;SLC25A5;SLC2A1;SLPI;SOD2;SPINT2;SPOCK2;TMEM123;TUBA1A;USF2;YWHAZ;ZFP36L1
```

### ./phase2/outputs/cv_emt_ecm_gene_tracking.csv

```csv
gene,method,scenario,present,rank,in_top50,in_top100
COL1A1,mdi,with12m,True,32,True,True
COL1A2,mdi,with12m,True,272,False,False
THBS1,mdi,with12m,True,173,False,False
THBS2,mdi,with12m,True,80,False,True
FLNA,mdi,with12m,True,493,False,False
CTNNB1,mdi,with12m,True,52,False,True
COL1A1,mdi,without12m,True,198,False,False
COL1A2,mdi,without12m,True,305,False,False
THBS1,mdi,without12m,True,257,False,False
THBS2,mdi,without12m,True,90,False,True
FLNA,mdi,without12m,True,505,False,False
CTNNB1,mdi,without12m,True,48,True,True
COL1A1,permutation,with12m,True,29,True,True
COL1A2,permutation,with12m,True,275,False,False
THBS1,permutation,with12m,True,112,False,False
THBS2,permutation,with12m,True,363,False,False
FLNA,permutation,with12m,True,462,False,False
CTNNB1,permutation,with12m,True,33,True,True
COL1A1,permutation,without12m,True,148,False,False
COL1A2,permutation,without12m,True,211,False,False
THBS1,permutation,without12m,True,318,False,False
THBS2,permutation,without12m,True,109,False,False
FLNA,permutation,without12m,True,496,False,False
CTNNB1,permutation,without12m,True,49,True,True
COL1A1,shap,with12m,True,41,True,True
COL1A2,shap,with12m,True,292,False,False
THBS1,shap,with12m,True,177,False,False
THBS2,shap,with12m,True,66,False,True
FLNA,shap,with12m,True,502,False,False
CTNNB1,shap,with12m,True,73,False,True
COL1A1,shap,without12m,True,209,False,False
COL1A2,shap,without12m,True,348,False,False
THBS1,shap,without12m,True,248,False,False
THBS2,shap,without12m,True,69,False,True
FLNA,shap,without12m,True,503,False,False
CTNNB1,shap,without12m,True,72,False,True
```

### ./phase2/outputs/cv_fold_auc_stats_by_threshold.csv

```csv
threshold,n_folds,mean_auc,std_auc,min_auc,max_auc,single_split_auc,single_split_within_fold_range
12,25,0.4746443089430894,0.19825262416140235,0.07499999999999996,0.975609756097561,0.4756097560975609,True
18,25,0.6431711711711712,0.1286146355434617,0.4444444444444445,0.875,0.611842105263158,True
24,25,0.7395525568181818,0.12206445853302578,0.44805194805194803,0.9653679653679653,0.8246753246753247,True
```

### ./phase2/outputs/cv_fold_auc_summary.csv

```csv
threshold,fold_id,repeat,split,n_train,n_test,n_events_test,auc
12,1,1,1,171,43,2,0.3475609756097561
12,2,1,2,171,43,2,0.4634146341463415
12,3,1,3,171,43,2,0.6890243902439024
12,4,1,4,171,43,3,0.35
12,5,1,5,172,42,2,0.575
12,6,2,1,171,43,2,0.43292682926829273
12,7,2,2,171,43,2,0.42073170731707316
12,8,2,3,171,43,2,0.4451219512195122
12,9,2,4,171,43,3,0.29166666666666663
12,10,2,5,172,42,2,0.07499999999999996
12,11,3,1,171,43,2,0.25
12,12,3,2,171,43,2,0.524390243902439
12,13,3,3,171,43,2,0.5914634146341463
12,14,3,4,171,43,3,0.5375
12,15,3,5,172,42,2,0.46875
12,16,4,1,171,43,2,0.2682926829268293
12,17,4,2,171,43,2,0.5548780487804879
12,18,4,3,171,43,2,0.5975609756097562
12,19,4,4,171,43,3,0.47916666666666663
12,20,4,5,172,42,2,0.74375
12,21,5,1,171,43,2,0.6524390243902439
12,22,5,2,171,43,2,0.225609756097561
12,23,5,3,171,43,2,0.975609756097561
12,24,5,4,171,43,3,0.22499999999999998
12,25,5,5,172,42,2,0.68125
18,1,1,1,164,42,5,0.5783783783783784
18,2,1,2,165,41,4,0.5709459459459459
18,3,1,3,165,41,4,0.47635135135135137
18,4,1,4,165,41,4,0.5743243243243243
18,5,1,5,165,41,5,0.763888888888889
18,6,2,1,164,42,5,0.8378378378378378
18,7,2,2,165,41,4,0.7939189189189189
18,8,2,3,165,41,4,0.5202702702702703
18,9,2,4,165,41,4,0.5033783783783783
18,10,2,5,165,41,5,0.6527777777777777
18,11,3,1,164,42,5,0.4972972972972973
18,12,3,2,165,41,4,0.48310810810810806
18,13,3,3,165,41,4,0.652027027027027
18,14,3,4,165,41,4,0.8445945945945946
18,15,3,5,165,41,5,0.538888888888889
18,16,4,1,164,42,5,0.7054054054054054
18,17,4,2,165,41,4,0.7027027027027027
18,18,4,3,165,41,4,0.875
18,19,4,4,165,41,4,0.668918918918919
18,20,4,5,165,41,5,0.4444444444444445
18,21,5,1,164,42,5,0.7297297297297297
18,22,5,2,165,41,4,0.5202702702702703
18,23,5,3,165,41,4,0.6925675675675675
18,24,5,4,165,41,4,0.6689189189189189
18,25,5,5,165,41,5,0.7833333333333333
24,1,1,1,159,40,7,0.7294372294372294
24,2,1,2,159,40,7,0.8852813852813852
24,3,1,3,159,40,7,0.6818181818181818
24,4,1,4,159,40,8,0.712890625
24,5,1,5,160,39,7,0.7522321428571428
24,6,2,1,159,40,7,0.5584415584415584
24,7,2,2,159,40,7,0.8008658008658008
24,8,2,3,159,40,7,0.9047619047619048
24,9,2,4,159,40,8,0.638671875
24,10,2,5,160,39,7,0.7477678571428572
24,11,3,1,159,40,7,0.5735930735930735
24,12,3,2,159,40,7,0.8658008658008659
24,13,3,3,159,40,7,0.44805194805194803
24,14,3,4,159,40,8,0.7578125
24,15,3,5,160,39,7,0.890625
24,16,4,1,159,40,7,0.9653679653679653
24,17,4,2,159,40,7,0.6601731601731602
24,18,4,3,159,40,7,0.7619047619047619
24,19,4,4,159,40,8,0.673828125
24,20,4,5,160,39,7,0.7857142857142857
24,21,5,1,159,40,7,0.6623376623376623
24,22,5,2,159,40,7,0.7705627705627706
24,23,5,3,159,40,7,0.6341991341991342
24,24,5,4,159,40,8,0.89453125
24,25,5,5,160,39,7,0.7321428571428571
```

### ./phase2/outputs/cv_mdi_importances_full.csv

Total data rows: 1658 (header + 1658 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,threshold,mean_importance,std_importance,n_folds_present
```
FIRST 20 DATA ROWS:
```csv
RHOA,12,0.06400761916328025,0.0,1
LYZ,12,0.023020358567323106,0.01058957754444409,25
UXT,12,0.018837774156963055,0.012449174658928041,4
CHCHD2,12,0.018369978400219443,0.010758509106016948,10
TMEM59,12,0.016932891201085588,0.008814285801717395,25
CD59,12,0.011476627180529553,0.0035939559447667065,24
GANAB,12,0.01129506626362816,0.011092626652945237,21
FOSB,12,0.01123838706641688,0.0053332838445671925,25
CTSB,12,0.010784827626675288,0.007082769221345417,25
ANXA1,12,0.010757660172154864,0.0047147494775828915,25
GPX1,12,0.010564882667931848,0.006955363236045875,25
SPINT2,12,0.010282566595831877,0.008743380632001713,25
MEST,12,0.009811986884806695,0.011258482716361528,25
COL1A1,12,0.009435455994946473,0.003930141477503212,25
DDR1,12,0.00940342974419375,0.0012892633420679492,2
LTBP4,12,0.009165749156387931,0.004647827790968895,24
IER2,12,0.008129327568263407,0.007210075697734721,19
H1F0,12,0.007918391357120623,0.008385569481744203,21
HBA2,12,0.007864481720694141,0.0062931599594231195,16
C12orf35,12,0.007763899950778521,0.0074118494203514245,20
```
LAST 20 DATA ROWS:
```csv
NAP1L1,24,0.0008982536753635082,0.0005842975511913007,25
EEF1A1,24,0.0008963150628612412,0.0005481794224047281,25
LCN2,24,0.0008939136026248043,0.0007273652479544083,25
MYL12B,24,0.0008926193857030741,0.0005294639036090376,25
PRSS23,24,0.0008846878436564304,4.287194092656289e-07,2
WFDC2,24,0.0008737604581876259,0.0005131462732412734,25
ELF3,24,0.0008673517627754002,0.0005136857537047392,25
EEF1G,24,0.0008669396457238474,0.0006136429794457373,25
UBB,24,0.0008656641321247318,0.0005071175476117726,25
YAP1,24,0.0008598451483644226,0.00035497502284949145,16
S100A9,24,0.0008452789056505476,0.000361956481155447,19
PAM,24,0.0008306109757072048,0.00047900788345127583,4
CTRC,24,0.000825396574468559,0.0004939861045009502,15
CYP4B1,24,0.0008207994765896911,0.00031623748907339216,3
POSTN,24,0.0007987312517729675,0.0,1
ATP2B4,24,0.0007902174947124817,0.0003741529615341069,16
SPP1,24,0.0007859146720924448,0.0004288645429401175,25
CD24,24,0.0007509949562453629,0.00036660271259976327,25
RPL29,24,0.0006999251530261562,0.00047791338038111924,25
RPL22,24,0.000640084999067154,0.0002571841588125961,25
```

### ./phase2/outputs/cv_permutation_importances_full.csv

Total data rows: 1658 (header + 1658 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,threshold,mean_importance,std_importance,n_folds_present
```
FIRST 20 DATA ROWS:
```csv
LYZ,12,0.0469719512195122,0.037163143488160515,25
TMEM59,12,0.02154634146341464,0.021999094403798002,25
ANXA1,12,0.019245528455284554,0.020094709176861396,25
CHCHD2,12,0.015253048780487815,0.01424562321969255,10
FAU,12,0.01187886178861788,0.011256888472801898,25
RHOA,12,0.01158536585365857,0.0,1
P4HB,12,0.010586178861788626,0.018610085906357304,25
CD59,12,0.00999936483739837,0.019834663293740937,24
GPX1,12,0.00952459349593496,0.02014113938321369,25
UXT,12,0.009321646341463432,0.011820270826585325,4
FOSB,12,0.009215447154471541,0.013782337559020457,25
SLC38A2,12,0.00890497967479675,0.012468496255931561,20
H1F0,12,0.008776374370886566,0.0156597277438971,21
C12orf35,12,0.008742378048780492,0.019781784787624247,20
MEST,12,0.00849857723577236,0.03396927787985436,25
RPL36,12,0.007976422764227645,0.014938173284753817,25
HLA-DPA1,12,0.00788373983739838,0.010966514422469308,25
IGF2,12,0.007616260162601627,0.013833330146881042,25
COL1A1,12,0.007415853658536591,0.018024666658129664,25
GNAS,12,0.0070404471544715476,0.01364610170625228,25
```
LAST 20 DATA ROWS:
```csv
TUBB2C,24,-0.0013566017316017313,0.005713715213268841,25
PLTP,24,-0.0013591800356506176,0.005571039221338459,17
PERP,24,-0.001362029897186159,0.0041772147007343155,10
GIPC1,24,-0.0014181998556998534,0.007267921188881797,6
LYPD1,24,-0.0014446699134199078,0.0043662931060713915,25
PUF60,24,-0.0014685808982683975,0.006126106145561431,25
APH1A,24,-0.0016018161525973968,0.0025100854710680956,20
RPL11,24,-0.00162219291125541,0.005494103793704467,25
APEX1,24,-0.0016661170860389567,0.0052219682509767685,20
XBP1,24,-0.001699472402597397,0.0029372555761503663,25
HSPA8,24,-0.0017087391774891726,0.002923360401362819,25
EIF3CL,24,-0.0018723281926406894,0.005811244713087312,25
CHCHD2,24,-0.0018898057960557767,0.005092254566467283,9
NDUFS5,24,-0.0019483225108225069,0.00496070564600352,25
SLC38A1,24,-0.0020399305555555487,0.004989000687565791,6
NUMA1,24,-0.0020649082904942192,0.005285443608535497,24
MUC5B,24,-0.002218481217247658,0.00608851885100029,19
ARL4C,24,-0.002922077922077909,0.0031385281385281237,2
NR4A1,24,-0.00489921536796534,0.010673996118890727,5
RHOA,24,-0.01060606060606053,0.0,1
```

### ./phase2/outputs/cv_shap_importances_full.csv

Total data rows: 1658 (header + 1658 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,threshold,mean_importance,std_importance,n_folds_present
```
FIRST 20 DATA ROWS:
```csv
RHOA,12,0.040092232966453104,0.0,1
LYZ,12,0.015750997924146484,0.008312592807961641,25
UXT,12,0.012177330805850851,0.007684447135380539,4
CHCHD2,12,0.011861122764147039,0.0076417830068534415,10
TMEM59,12,0.011045850533977266,0.0053749032650130535,25
GANAB,12,0.007682353142231772,0.00793805016684694,21
ANXA1,12,0.007558228338187117,0.003100988020094219,25
FOSB,12,0.007068280159022897,0.002843799152896844,25
SPINT2,12,0.006535440087647765,0.005691778079377649,25
GPX1,12,0.006487550680533491,0.004315826877823806,25
MEST,12,0.006463162483680004,0.007647658973310092,25
CTSB,12,0.006454780966297901,0.004991058118594359,25
CD59,12,0.006414387374791209,0.002148022151063369,24
DDR1,12,0.005884511828272801,0.00035948914894371126,2
LTBP4,12,0.005798392589919253,0.0032298811773872516,24
COL1A1,12,0.005731405363357332,0.002124345358561091,25
IER2,12,0.005561370720774933,0.005375449475927912,19
H1F0,12,0.0050106906001334784,0.005335667175428053,21
TM4SF1,12,0.004962337746809379,0.0036306976905378864,25
FAU,12,0.004955684443056085,0.0048140836538732796,25
```
LAST 20 DATA ROWS:
```csv
GLUL,24,0.00042439737499954213,0.00020854029552876035,20
EEF1G,24,0.0004213841085174919,0.00028445222923402475,25
NAP1L1,24,0.0004071865640937128,0.000332427821417733,25
UBB,24,0.00040356853425968004,0.00019421267848417713,25
S100A9,24,0.0004017631383927867,0.0002096038482004876,19
MYL12B,24,0.0004002729462136522,0.00024221544846498303,25
B2M,24,0.00039250080622504874,0.00021005838156832926,25
IFITM2,24,0.00038925124925779243,0.0002400572914563764,20
RPL32,24,0.0003843727198935377,0.00022508728057078254,25
PRSS23,24,0.00038386855010405377,8.807994852927061e-05,2
CD24,24,0.0003814489726999275,0.0002104102703147949,25
LGALS1,24,0.0003759186019789212,0.0002519427810995544,25
ATP2B4,24,0.00036108697107437807,0.00011363604247737076,16
PPT1,24,0.0003610764367167849,0.00022450693158916166,20
ITGA3,24,0.0003579000616145094,0.0001873354976610567,18
PAM,24,0.000337437495199324,0.00019262912628364374,4
ADAR,24,0.00032983476362716697,0.0002002507942602898,5
CYP4B1,24,0.00032181005083317676,6.725719202605635e-05,3
RPL22,24,0.00031750625028104947,0.00011911002625180488,25
RPL29,24,0.00029323870052205646,0.00017094359544356726,25
```

### ./phase2/outputs/enrichment_results_full.csv

Total data rows: 5824 (header + 5824 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
database,rank,term,p_value,z_score,combined_score,overlap_genes,n_overlap,adj_p_value,gene_list,n_genes_submitted
```
FIRST 20 DATA ROWS:
```csv
KEGG_2021_Human,1,Proteoglycans in cancer,0.00015693240089955412,10.972222222222221,96.1133246688316,IGF2;FLNA;HSPG2;EIF4B;DCN,5,0.014594713283658533,top50,50
KEGG_2021_Human,2,Vibrio cholerae infection,0.006950299465156898,17.276041666666668,85.84414194819459,ARF1;ATP6V1B1,2,0.22399843956498602,top50,50
KEGG_2021_Human,3,Ribosome,0.007225756114999549,8.151681537405628,40.18863284587075,RPL27A;RPLP0;RPLP2,3,0.22399843956498602,top50,50
KEGG_2021_Human,4,Coronavirus disease,0.02024165428659951,5.496887484901979,21.43793102563893,RPL27A;RPLP0;RPLP2,3,0.35614861047401125,top50,50
KEGG_2021_Human,5,Salmonella infection,0.02432234530488415,5.112610275038921,19.00029925474201,ARF1;HSP90AB1;FLNA,3,0.35614861047401125,top50,50
KEGG_2021_Human,6,Hematopoietic cell lineage,0.025470075176232815,8.527920962199312,31.299610767204847,TFRC;ANPEP,2,0.35614861047401125,top50,50
KEGG_2021_Human,7,HIF-1 signaling pathway,0.030421664588174364,7.72702492211838,26.987409356009476,TFRC;ALDOA,2,0.35614861047401125,top50,50
KEGG_2021_Human,8,Oxidative phosphorylation,0.04369185304054307,6.303753180661578,19.734489511742076,NDUFB11;ATP6V1B1,2,0.35614861047401125,top50,50
KEGG_2021_Human,9,Phagosome,0.0554491879134877,5.5,15.907585158720506,TFRC;ATP6V1B1,2,0.35614861047401125,top50,50
KEGG_2021_Human,10,Renin-angiotensin system,0.05597578058787951,18.4860853432282,53.29235549319145,ANPEP,1,0.35614861047401125,top50,50
KEGG_2021_Human,11,mTOR signaling pathway,0.0567455048100272,5.427083333333333,15.571272642043727,EIF4B;ATP6V1B1,2,0.35614861047401125,top50,50
KEGG_2021_Human,12,Vitamin digestion and absorption,0.05833855301300996,17.68145519077196,50.24171555062859,APOA1,1,0.35614861047401125,top50,50
KEGG_2021_Human,13,PI3K-Akt signaling pathway,0.05856469776358275,3.5641025641025643,10.113580091620108,HSP90AB1;IGF2;EIF4B,3,0.35614861047401125,top50,50
KEGG_2021_Human,14,Collecting duct acid secretion,0.06539215225886762,15.638932496075354,42.652889831563165,ATP6V1B1,1,0.35614861047401125,top50,50
KEGG_2021_Human,15,Fatty acid elongation,0.06539215225886762,15.638932496075354,42.652889831563165,PPT1,1,0.35614861047401125,top50,50
KEGG_2021_Human,16,Pentose phosphate pathway,0.0723939657090184,14.019000703729768,36.80874147674154,ALDOA,1,0.35614861047401125,top50,50
KEGG_2021_Human,17,NOD-like receptor signaling pathway,0.07523531338174881,4.602188081936685,11.90647986328784,HSP90AB1;TXNIP,2,0.35614861047401125,top50,50
KEGG_2021_Human,18,RNA transport,0.07884713359091254,4.475996376811594,11.37012436768999,PABPC1;EIF4B,2,0.35614861047401125,top50,50
KEGG_2021_Human,19,Fructose and mannose metabolism,0.0793443657059371,12.70280612244898,32.18837516559274,ALDOA,1,0.35614861047401125,top50,50
KEGG_2021_Human,20,Starch and sucrose metabolism,0.08624372197430759,11.612244897959183,28.456712045041098,AMY1A,1,0.35614861047401125,top50,50
```
LAST 20 DATA ROWS:
```csv
MSigDB_Hallmark_2020,28,Cholesterol Homeostasis,0.03805558843062846,4.231572174161721,13.83177100318916,ECH1;CD9;CTNNB1,3,0.06387902343712634,top200,200
MSigDB_Hallmark_2020,29,Angiogenesis,0.05019950084615693,5.872251931075461,17.568310863627904,APP;FSTL1,2,0.07965559760367037,top200,200
MSigDB_Hallmark_2020,30,Xenobiotic Metabolism,0.0508439984704279,2.5779092702169626,7.679574154313181,JUP;IGFBP4;ECH1;APOE;PTGDS,5,0.07965559760367037,top200,200
MSigDB_Hallmark_2020,31,TNF-alpha Signaling via NF-kB,0.1410458258534753,2.0412328196584757,3.9981023755392973,FOS;JUNB;SAT1;SQSTM1,4,0.19497511220921585,top200,200
MSigDB_Hallmark_2020,32,G2-M Checkpoint,0.1410458258534753,2.0412328196584757,3.9981023755392973,NOTCH2;NUMA1;NCL;ODC1,4,0.19497511220921585,top200,200
MSigDB_Hallmark_2020,33,Inflammatory Response,0.1410458258534753,2.0412328196584757,3.9981023755392973,BST2;MMP14;TNFSF10;TAPBP,4,0.19497511220921585,top200,200
MSigDB_Hallmark_2020,34,KRAS Signaling Up,0.1410458258534753,2.0412328196584757,3.9981023755392973,MMP11;SLPI;JUP;IGF2,4,0.19497511220921585,top200,200
MSigDB_Hallmark_2020,35,UV Response Dn,0.17504405095072287,2.1232314504806133,3.7001928537556354,NOTCH2;COL1A1;COL1A2,3,0.23505915413382783,top200,200
MSigDB_Hallmark_2020,36,IL-6/JAK/STAT3 Signaling,0.21620527648032148,2.342840166369578,3.5881228977337716,CD9;A2M,2,0.2822679998493086,top200,200
MSigDB_Hallmark_2020,37,Notch Signaling,0.2752009537742224,3.204571243313341,4.1347099266061775,NOTCH2,1,0.34957958992941757,top200,200
MSigDB_Hallmark_2020,38,Bile Acid Metabolism,0.30861705753518287,1.8080808080808082,2.1256775548508937,APOA1;DHCR24,2,0.37061733467722674,top200,200
MSigDB_Hallmark_2020,39,Adipogenesis,0.3233044834418361,1.5153443788811873,1.711067359910169,ECH1;APOE;ALDOA,3,0.37061733467722674,top200,200
MSigDB_Hallmark_2020,40,Oxidative Phosphorylation,0.3233044834418361,1.5153443788811873,1.711067359910169,LDHB;ECH1;UQCRFS1,3,0.37061733467722674,top200,200
MSigDB_Hallmark_2020,41,heme Metabolism,0.3233044834418361,1.5153443788811873,1.711067359910169,PRDX2;BCAM;TFRC,3,0.37061733467722674,top200,200
MSigDB_Hallmark_2020,42,Pancreas Beta Cells,0.3312915354401823,2.54619250096637,2.8129227654318845,SRP14,1,0.37073100394496594,top200,200
MSigDB_Hallmark_2020,43,Wnt-beta Catenin Signaling,0.34462567794504406,2.4217428606446867,2.5798740539583482,CTNNB1,1,0.376683880544583,top200,200
MSigDB_Hallmark_2020,44,Apical Surface,0.3576952382847675,2.308869931050602,2.373689018141451,APP,1,0.38208354998600164,top200,200
MSigDB_Hallmark_2020,45,E2F Targets,0.5967065753140588,1.0,0.516329785050999,TFRC;NAP1L1,2,0.6096784573861036,top200,200
MSigDB_Hallmark_2020,46,KRAS Signaling Dn,0.5967065753140588,1.0,0.516329785050999,IGFBP2;ATP6V1B1,2,0.6096784573861036,top200,200
MSigDB_Hallmark_2020,47,DNA Repair,0.7797997353776313,0.6627432464335098,0.164836268730291,BCAM,1,0.7797997353776313,top200,200
```

### ./phase2/outputs/enrichment_results_significant.csv

Total data rows: 580 (header + 580 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
database,rank,term,p_value,z_score,combined_score,overlap_genes,n_overlap,adj_p_value,gene_list,n_genes_submitted
```
FIRST 20 DATA ROWS:
```csv
KEGG_2021_Human,1,Proteoglycans in cancer,0.00015693240089955412,10.972222222222221,96.1133246688316,IGF2;FLNA;HSPG2;EIF4B;DCN,5,0.014594713283658533,top50,50
Reactome_2022,1,Amyloid Fiber Formation R-HSA-977225,4.33192372416157e-08,37.13013698630137,629.529183362933,APP;GSN;APOA1;TGFBI;HSPG2;ITM2B,6,1.4425306001458029e-05,top50,50
Reactome_2022,2,Regulation Of IGF Transport And Uptake By IGFBPs R-HSA-381426,6.094647345778435e-07,23.115384615384617,330.7969820894124,APP;IGFBP4;IGF2;APOA1;MSLN;PRSS23,6,0.00010147587830721094,top50,50
Reactome_2022,3,Metabolism Of Proteins R-HSA-392499,1.6796001125505657e-06,4.971913475383844,66.11130885672671,APP;GSN;IGFBP4;RPLP0;IGF2;APOA1;MSLN;HSPG2;PRSS23;RPL27A;ANPEP;RPLP2;TGFBI;PABPC1;HNRNPC;EIF4B;ITM2B,17,0.0001864356124931128,top50,50
Reactome_2022,4,Post-translational Protein Phosphorylation R-HSA-8957275,6.6648558636472086e-06,21.836083608360838,260.25690496341264,APP;IGFBP4;APOA1;MSLN;PRSS23,5,0.00044655849608119566,top50,50
Reactome_2022,5,L13a-mediated Translational Silencing Of Ceruloplasmin Expression R-HSA-156827,7.303530312980346e-06,21.40992448759439,253.21844668535684,RPL27A;RPLP0;RPLP2;PABPC1;EIF4B,5,0.00044655849608119566,top50,50
Reactome_2022,6,NLRP3 Inflammasome R-HSA-844456,8.046099028490012e-06,97.89034369885434,1148.2853674678522,APP;HSP90AB1;TXNIP,3,0.00044655849608119566,top50,50
Reactome_2022,7,Cap-dependent Translation Initiation R-HSA-72737,1.035242363897835e-05,19.85885885885886,227.94573901847133,RPL27A;RPLP0;RPLP2;PABPC1;EIF4B,5,0.0004825269554863375,top50,50
Reactome_2022,8,Cellular Responses To Stimuli R-HSA-8953897,1.1592239170842943e-05,6.619834710743802,75.23557811011119,PRDX2;HSP90AB1;RPL27A;LMNA;RPLP0;APOA1;MT1G;TXNIP;RPLP2;ATP6V1B1,10,0.0004825269554863375,top50,50
Reactome_2022,9,Platelet Degranulation R-HSA-114608,1.4884754838316752e-05,18.36111111111111,204.0869270968184,APP;IGF2;APOA1;FLNA;MAGED2,5,0.0005256410254920351,top50,50
Reactome_2022,10,Response To Elevated Platelet Cytosolic Ca2+ R-HSA-76005,1.799731603382954e-05,17.622222222222224,192.52785157536061,APP;IGF2;APOA1;FLNA;MAGED2,5,0.0005256410254920351,top50,50
Reactome_2022,11,Inflammasomes R-HSA-622312,1.8942018936649912e-05,70.68085106382979,768.592613095972,APP;HSP90AB1;TXNIP,3,0.0005256410254920351,top50,50
Reactome_2022,12,Deregulated CDK5 Triggers Neurodegenerative Pathways In Alzheimers Disease Models R-HSA-8862803,1.8942018936649912e-05,70.68085106382979,768.592613095972,APP;PRDX2;LMNA,3,0.0005256410254920351,top50,50
Reactome_2022,13,Defective Intrinsic Pathway For Apoptosis R-HSA-9734009,2.867422295491e-05,60.57446808510638,633.5793754459056,APP;PRDX2;LMNA,3,0.00073450124953731,top50,50
Reactome_2022,14,Cellular Responses To Stress R-HSA-2262752,6.580039922630074e-05,5.922519070913009,57.02725298535634,PRDX2;HSP90AB1;RPL27A;LMNA;RPLP0;APOA1;TXNIP;RPLP2;ATP6V1B1,9,0.0015651094958827247,top50,50
Reactome_2022,15,Nonsense Mediated Decay (NMD) Independent Of Exon Junction Complex (EJC) R-HSA-975956,8.212184135698631e-05,19.626482213438734,184.6323345485555,RPL27A;RPLP0;RPLP2;PABPC1,4,0.0018231048781250962,top50,50
Reactome_2022,16,GTP Hydrolysis And Joining Of 60S Ribosomal Subunit R-HSA-72706,0.00015848493118390697,16.434782608695652,143.80189971009636,RPL27A;RPLP0;RPLP2;EIF4B,4,0.003104440122602413,top50,50
Reactome_2022,17,Degradation Of Extracellular Matrix R-HSA-1474228,0.00015848493118390697,16.434782608695652,143.80189971009636,COL12A1;TIMP2;HSPG2;DCN,4,0.003104440122602413,top50,50
Reactome_2022,18,Nonsense Mediated Decay (NMD) Enhanced By Exon Junction Complex (EJC) R-HSA-975957,0.00017596171244768462,15.97584541062802,138.1150837500777,RPL27A;RPLP0;RPLP2;PABPC1,4,0.0032552916802821657,top50,50
Reactome_2022,19,"Nucleotide-binding Domain, Leucine Rich Repeat Containing NLR Signaling Pathways R-HSA-168643",0.000315376219123607,25.404255319148938,204.80261014345277,APP;HSP90AB1;TXNIP,3,0.0055273832088505856,top50,50
```
LAST 20 DATA ROWS:
```csv
MSigDB_Hallmark_2020,8,Protein Secretion,5.059661151459745e-05,8.032659952261746,79.45606763154184,ARF1;PPT1;GNAS;ATP1A1;ERGIC3;AP2M1;ATP6V1B1,7,0.00029725509264826,top200,200
MSigDB_Hallmark_2020,9,Hypoxia,0.00019001668226546373,4.837614100490667,41.45060631295679,HSPA5;HDLBP;MIF;FOS;TGFBI;ALDOA;CP;NDRG1;DCN,9,0.0007442320055397329,top200,200
MSigDB_Hallmark_2020,10,Estrogen Response Late,0.00019001668226546373,4.837614100490667,41.45060631295679,XBP1;ST14;IGFBP4;SCNN1A;CD9;EMP2;FOS;PRSS23;LTF,9,0.0007442320055397329,top200,200
MSigDB_Hallmark_2020,11,Myogenesis,0.00019001668226546373,4.837614100490667,41.45060631295679,EIF4A2;COL1A1;APP;TAGLN;GSN;COL4A2;COL6A3;IGFBP7;AGRN,9,0.0007442320055397329,top200,200
MSigDB_Hallmark_2020,12,Complement,0.00019001668226546373,4.837614100490667,41.45060631295679,MMP14;COL4A2;HSPA5;C1S;LRP1;TIMP2;CP;HSPA1A;LTF,9,0.0007442320055397329,top200,200
MSigDB_Hallmark_2020,13,Interferon Alpha Response,0.00043082901286403295,6.698425286054152,51.91145138175452,IFITM3;BST2;CD74;C1S;TXNIP;CD47,6,0.0015576125849699654,top200,200
MSigDB_Hallmark_2020,14,IL-2/STAT5 Signaling,0.0009042939507854836,4.277705061082025,29.97968028880589,IFITM3;XBP1;MUC1;ODC1;TNFSF10;LRIG1;NDRG1;PLEC,8,0.0029267075793617263,top200,200
MSigDB_Hallmark_2020,15,Estrogen Response Early,0.0009340556104345935,4.255208333333333,29.684225172013964,XBP1;MUC1;IGFBP4;SCNN1A;KRT8;LRIG1;FOS;PRSS23,8,0.0029267075793617263,top200,200
MSigDB_Hallmark_2020,16,Fatty Acid Metabolism,0.0010764928571620567,4.719589609854854,32.25389663123081,ECH1;ODC1;DHCR24;MIF;ALDOA;GLUL;PRDX6,7,0.0031621977679135416,top200,200
MSigDB_Hallmark_2020,17,Interferon Gamma Response,0.004067400402162354,3.684635829149776,20.28300352206346,IFITM3;BST2;CD74;C1S;TNFSF10;TXNIP;TAPBP,7,0.010620434383423926,top200,200
MSigDB_Hallmark_2020,18,Glycolysis,0.004067400402162354,3.684635829149776,20.28300352206346,HSPA5;HDLBP;MIF;TGFBI;ALDOA;AGRN;DCN,7,0.010620434383423926,top200,200
MSigDB_Hallmark_2020,19,Reactive Oxygen Species Pathway,0.012951499605550441,6.539615978812624,28.42472661929245,PRDX2;JUNB;PRDX6,3,0.03203792007688794,top200,200
MSigDB_Hallmark_2020,20,Mitotic Spindle,0.015151192505367015,3.141979595107099,13.163876618045636,NOTCH2;YWHAE;GSN;NUMA1;FLNA;ACTN4,6,0.03310079848846099,top200,200
MSigDB_Hallmark_2020,21,Apical Junction,0.015493990781832804,3.1256244021681368,13.025424015927582,JUP;MSN;ACTN4;TGFBI;MYL9;MYL12B,6,0.03310079848846099,top200,200
MSigDB_Hallmark_2020,22,Allograft Rejection,0.015493990781832804,3.1256244021681368,13.025424015927582,CD74;RPS9;RPS19;FLNA;CD47;TAPBP,6,0.03310079848846099,top200,200
MSigDB_Hallmark_2020,23,TGF-beta Signaling,0.016816102196470534,5.896984174380412,24.09164757699128,CTNNB1;JUNB;THBS1,3,0.03436333927104848,top200,200
MSigDB_Hallmark_2020,24,Androgen Response,0.018073322130463105,4.188775510204081,16.81088959163861,KRT8;DHCR24;SAT1;NDRG1,4,0.03539358917215691,top200,200
MSigDB_Hallmark_2020,25,Pperoxisome,0.020556458565384676,4.020408163265306,15.617597552926842,CRABP2;ECH1;DHCR24;PABPC1,4,0.03833818528813848,top200,200
MSigDB_Hallmark_2020,26,PI3K/AKT/mTOR  Signaling,0.021208357818970226,3.980400080824409,15.337914209660529,ARF1;CALR;SQSTM1;AP2M1,4,0.03833818528813848,top200,200
MSigDB_Hallmark_2020,27,Unfolded Protein Response,0.02688001683194322,3.686762778505898,13.332706188429968,EIF4A2;XBP1;HSPA5;CALR,4,0.04679114041116042,top200,200
```

### ./phase2/outputs/enrichment_shap_with12m_full.csv

Total data rows: 10458 (header + 10458 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
database,rank,term,p_value,z_score,combined_score,overlap_genes,n_overlap,adj_p_value,gene_list,scenario,size,n_genes_submitted
```
FIRST 20 DATA ROWS:
```csv
KEGG_2021_Human,1,Ferroptosis,0.00014657115641659294,33.4468085106383,295.2684100827493,TFRC;SAT1;CP,3,0.010828335662069234,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,2,Proteoglycans in cancer,0.00015693240089955412,10.972222222222221,96.1133246688316,COL1A1;IGF2;HSPG2;RHOA;ACTG1,5,0.010828335662069234,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,3,Platelet activation,0.0002599994355607027,14.369565217391305,118.61833381941406,COL1A1;GNAS;RHOA;ACTG1,4,0.011959974035792324,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,4,ECM-receptor interaction,0.0013893445250705149,14.917396745932416,98.14040765115749,COL1A1;COL4A2;HSPG2,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,5,Focal adhesion,0.0015886471428271653,8.719046568086515,56.19314326541343,COL1A1;COL4A2;RHOA;ACTG1,4,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,6,Dilated cardiomyopathy,0.0017838028065180675,13.628689087165409,86.25607933742052,TPM4;GNAS;ACTG1,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,7,PI3K-Akt signaling pathway,0.001862148814727307,6.240369309137217,39.22711237773203,COL1A1;NR4A1;HSP90AA1;COL4A2;IGF2,5,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,8,Hematopoietic cell lineage,0.0019479426217578455,13.200797872340425,82.3859356912581,TFRC;ANPEP;CD59,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,9,Amoebiasis,0.002121212982648662,12.798839458413926,78.78667603753651,COL1A1;COL4A2;GNAS,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,10,Protein digestion and absorption,0.002181029234164079,12.670212765957446,77.64253659479164,COL1A1;COL4A2;SLC38A2,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,11,Salmonella infection,0.003447530150958652,6.9937888198757765,39.65546242307768,HSP90AA1;PODXL;RHOA;ACTG1,4,0.04325083280293582,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,12,Relaxin signaling pathway,0.0041187773755245296,10.042553191489361,55.15569972379198,COL1A1;COL4A2;GNAS,3,0.04736593981853209,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,13,Fluid shear stress and atherosclerosis,0.005072238171854362,9.299436795994994,49.137973919606814,HSP90AA1;RHOA;ACTG1,3,0.05384375905506938,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,14,Cocaine addiction,0.006682897030368853,17.64450354609929,88.36726791367238,GNAS;FOSB,2,0.059946332886978246,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,15,Oxytocin signaling pathway,0.006734164844589255,8.369310976468931,41.85125407551329,GNAS;RHOA;ACTG1,3,0.059946332886978246,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,16,Vibrio cholerae infection,0.006950299465156898,17.276041666666668,85.84414194819459,GNAS;ACTG1,2,0.059946332886978246,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,17,Glutathione metabolism,0.008955160836496808,15.071969696969697,71.07225417227201,GPX1;ANPEP,2,0.06875639455582058,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,18,Protein processing in endoplasmic reticulum,0.008968225376846163,7.51595744680851,35.43073044803733,HSP90AA1;GANAB;P4HB,3,0.06875639455582058,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,19,Pathways in cancer,0.010266134723991405,4.103084072665822,18.78763091040504,HSP90AA1;COL4A2;IGF2;GNAS;RHOA,5,0.07218989727198206,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,20,NOD-like receptor signaling pathway,0.010462303952461168,7.090126703322974,32.33081172672363,HSP90AA1;RHOA;CTSB,3,0.07218989727198206,SHAP_with12m_top50,with12m,50,50
```
LAST 20 DATA ROWS:
```csv
MSigDB_Hallmark_2020,30,Xenobiotic Metabolism,0.0046255521368885385,2.5259853505406347,13.580100225543946,MT2A;AHCY;JUP;PTGES3;SERPINE1;ECH1;TMBIM6;SPINT2;APOE;PTGDS;BCAT1;CFB,12,0.0075550684902512795,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,31,PI3K/AKT/mTOR  Signaling,0.00484745727525393,3.2525354119520578,17.333740173542928,ARF1;CFL1;SLC2A1;CALR;PFN1;SQSTM1;AP2M1;HSP90B1,8,0.007662109886691696,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,32,Notch Signaling,0.007971195406910945,5.608294930875576,27.098836980107382,NOTCH2;APH1A;NOTCH3;CCND1,4,0.012205892966832384,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,33,Cholesterol Homeostasis,0.010475384097409076,3.4708263872350558,15.822550469971569,ECH1;MAL2;CD9;CTNNB1;S100A11;ACTG1,6,0.015554358205243781,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,34,TGF-beta Signaling,0.011068822496125156,4.009688723974438,18.058125986560793,SERPINE1;CTNNB1;JUNB;THBS1;RHOA,5,0.015952126538533312,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,35,Inflammatory Response,0.029308469849829922,2.074113856068743,7.321370386955588,BST2;IFITM1;BTG2;MMP14;SERPINE1;HPN;TNFSF10;TIMP1;LY6E;TAPBP,10,0.03989208396226851,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,36,heme Metabolism,0.029308469849829922,2.074113856068743,7.321370386955588,SELENBP1;PRDX2;BCAM;BTG2;TFRC;BSG;UCP2;SLC2A1;HDGF;CTSB,10,0.03989208396226851,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,37,Adipogenesis,0.06464483434956346,1.853051257717448,5.075224023958898,NDUFB7;GPX3;APLP2;ECH1;UCP2;UBC;APOE;CYC1;ALDOA,9,0.08335781271391078,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,38,KRAS Signaling Up,0.06464483434956346,1.853051257717448,5.075224023958898,MMP11;SPON1;SLPI;JUP;IGFBP3;IGF2;SPP1;CFB;MMP10,9,0.08335781271391078,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,39,Apical Surface,0.09705771960273352,2.8648476223192816,6.6821122037109575,APP;HSPB1;THY1,3,0.12194431437266519,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,40,IL-6/JAK/STAT3 Signaling,0.17333099873778088,1.8866109599689078,3.3063842355764335,JUN;STAT1;CD9;A2M,4,0.2123304734537816,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,41,Hedgehog Signaling,0.22698728149273847,2.2993149066855656,3.4095650726373203,MYH9;THY1,2,0.2679993611299758,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,42,Mitotic Spindle,0.23148950997896622,1.4278651115618661,2.089281816243083,UXT;NOTCH2;YWHAE;GSN;NUMA1;MYH9;ACTN4,7,0.2679993611299758,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,43,KRAS Signaling Dn,0.23518311282834609,1.4203932779114863,2.055864254779462,CPA2;BTG2;IGFBP2;MX1;KRT5;KLK7;ATP6V1B1,7,0.2679993611299758,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,44,E2F Targets,0.3840049274819742,1.2086898451521348,1.1568369232691817,ILF3;TFRC;TUBB;STMN1;HMGA1;NAP1L1,6,0.4276418510594712,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,45,Myc Targets V2,0.4274492922819714,1.3944348823866897,1.1851575544562791,NPM1;HSPD1,2,0.4654447849292577,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,46,Pancreas Beta Cells,0.6371302636481142,1.0,0.4507811487933908,SST,1,0.6786822373642956,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,47,Wnt-beta Catenin Signaling,0.6550827855909762,0.951121755706535,0.4023184736155008,CTNNB1,1,0.6829586488076136,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,48,DNA Repair,0.7276712445071681,0.794686486264526,0.2526355385251821,BCAM;IMPDH2;SUPT5H,3,0.7428310621010674,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,49,Bile Acid Metabolism,0.7736407907197486,0.7079225994888646,0.18168664166283727,APOA1;DHCR24,2,0.7736407907197486,SHAP_with12m_top500,with12m,500,500
```

### ./phase2/outputs/enrichment_shap_with12m_significant.csv

Total data rows: 1476 (header + 1476 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
database,rank,term,p_value,z_score,combined_score,overlap_genes,n_overlap,adj_p_value,gene_list,scenario,size,n_genes_submitted
```
FIRST 20 DATA ROWS:
```csv
KEGG_2021_Human,1,Ferroptosis,0.00014657115641659294,33.4468085106383,295.2684100827493,TFRC;SAT1;CP,3,0.010828335662069234,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,2,Proteoglycans in cancer,0.00015693240089955412,10.972222222222221,96.1133246688316,COL1A1;IGF2;HSPG2;RHOA;ACTG1,5,0.010828335662069234,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,3,Platelet activation,0.0002599994355607027,14.369565217391305,118.61833381941406,COL1A1;GNAS;RHOA;ACTG1,4,0.011959974035792324,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,4,ECM-receptor interaction,0.0013893445250705149,14.917396745932416,98.14040765115749,COL1A1;COL4A2;HSPG2,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,5,Focal adhesion,0.0015886471428271653,8.719046568086515,56.19314326541343,COL1A1;COL4A2;RHOA;ACTG1,4,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,6,Dilated cardiomyopathy,0.0017838028065180675,13.628689087165409,86.25607933742052,TPM4;GNAS;ACTG1,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,7,PI3K-Akt signaling pathway,0.001862148814727307,6.240369309137217,39.22711237773203,COL1A1;NR4A1;HSP90AA1;COL4A2;IGF2,5,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,8,Hematopoietic cell lineage,0.0019479426217578455,13.200797872340425,82.3859356912581,TFRC;ANPEP;CD59,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,9,Amoebiasis,0.002121212982648662,12.798839458413926,78.78667603753651,COL1A1;COL4A2;GNAS,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,10,Protein digestion and absorption,0.002181029234164079,12.670212765957446,77.64253659479164,COL1A1;COL4A2;SLC38A2,3,0.03009820343146429,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,11,Salmonella infection,0.003447530150958652,6.9937888198757765,39.65546242307768,HSP90AA1;PODXL;RHOA;ACTG1,4,0.04325083280293582,SHAP_with12m_top50,with12m,50,50
KEGG_2021_Human,12,Relaxin signaling pathway,0.0041187773755245296,10.042553191489361,55.15569972379198,COL1A1;COL4A2;GNAS,3,0.04736593981853209,SHAP_with12m_top50,with12m,50,50
Reactome_2022,1,Extracellular Matrix Organization R-HSA-1474244,7.509633225610684e-06,11.272682607271536,133.01003366035474,COL1A1;DDR1;COL4A2;LTBP4;P4HB;HSPG2;CTSB,7,0.002801093193152785,SHAP_with12m_top50,with12m,50,50
Reactome_2022,2,Collagen Formation R-HSA-1474290,7.537475624460895e-05,20.084934277047523,190.66704706762619,COL1A1;COL4A2;P4HB;CTSB,4,0.01405739203961957,SHAP_with12m_top50,with12m,50,50
Reactome_2022,3,Binding And Uptake Of Ligands By Scavenger Receptors R-HSA-2173782,0.00014657115641659294,33.4468085106383,295.2684100827493,COL1A1;HSP90AA1;COL4A2,3,0.015752448024751273,SHAP_with12m_top50,with12m,50,50
Reactome_2022,4,Signal Transduction R-HSA-162582,0.00021471456591390145,3.362909230658372,28.403807348189922,HSP90AA1;ANXA1;TPM4;TFRC;IGF2;LTBP4;SPINT2;RHOA;ACTG1;TMEM59;NR4A1;COL4A2;GNAS;FOSB;P4HB;PLTP,16,0.015752448024751273,SHAP_with12m_top50,with12m,50,50
Reactome_2022,5,Regulation Of IGF Transport And Uptake By IGFBPs R-HSA-381426,0.0002520741213679085,14.491048593350383,120.06974757642793,APLP2;IGF2;P4HB;CP,4,0.015752448024751273,SHAP_with12m_top50,with12m,50,50
Reactome_2022,6,Disease R-HSA-1643685,0.00025339058484854593,3.7168201283117126,30.777420642384875,HSP90AA1;TPM4;SUPT5H;CP;HSPG2;THSD4;ACTG1;NR4A1;GANAB;SNRPD2;PGK1;GNAS;FAU,13,0.015752448024751273,SHAP_with12m_top50,with12m,50,50
Reactome_2022,7,Assembly Of Collagen Fibrils And Other Multimeric Structures R-HSA-2022090,0.0003911590889551034,23.5177304964539,184.52943128485038,COL1A1;COL4A2;CTSB,3,0.020843191454321938,SHAP_with12m_top50,with12m,50,50
Reactome_2022,8,Infectious Disease R-HSA-5663205,0.0005568808852724408,4.380559540889527,32.824229987311384,HSP90AA1;GANAB;SNRPD2;PGK1;GNAS;FAU;SUPT5H;HSPG2;ACTG1,9,0.024143616001323864,SHAP_with12m_top50,with12m,50,50
```
LAST 20 DATA ROWS:
```csv
MSigDB_Hallmark_2020,17,Glycolysis,1.2080980660608848e-05,3.7152699996605913,42.07126491257376,TPI1;HSPA5;IGFBP3;HDLBP;ENO1;MIF;DCN;LDHA;CLDN3;COL5A1;ELF3;STMN1;PGK1;TGFBI;ALDOA;AGRN;PAM,17,3.4821650139401974e-05,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,18,Estrogen Response Late,4.551923375608182e-05,3.4703557312252964,34.69444971558032,XBP1;ST14;EMP2;LSR;FOS;PRSS23;ASS1;SERPINA5;KRT19;ZFP36;CCND1;MDK;SCNN1A;CD9;MEST;LTF,16,0.00012391346966933385,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,19,IL-2/STAT5 Signaling,0.00015205952013831083,3.24675033617212,28.542956665335332,IFITM3;XBP1;AHCY;AHNAK;CD81;ODC1;NDRG1;MUC1;SYNGR2;COL6A1;TNFSF10;SPP1;LRIG1;TGM2;PLEC,15,0.0003921534993040648,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,20,Estrogen Response Early,0.00016069795575379561,3.2290331568682085,28.208782013846974,XBP1;KRT8;SLC2A1;FOS;PRSS23;THSD4;KRT19;MUC1;KRT18;CCND1;ELF3;PODXL;SCNN1A;LRIG1;TGM2,15,0.0003937099915967993,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,21,Reactive Oxygen Species Pathway,0.00020253908941845664,6.578093306288032,55.94390535095862,PRDX2;GPX3;PRDX1;SOD2;JUNB;PRDX6;FTL,7,0.0004725912086430655,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,22,Oxidative Phosphorylation,0.0005298566553190931,2.9912385503783354,22.56262537515248,GPI;SLC25A3;NDUFB7;COX4I1;ECH1;NDUFC2;PHB2;COX6B1;LDHB;LDHA;UQCRFS1;CYC1;SLC25A5;SLC25A6,14,0.001128825048288503,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,23,Allograft Rejection,0.0005298566553190931,2.9912385503783354,22.56262537515248,CD74;NPM1;RPS9;STAT1;RPS3A;HLA-A;THY1;HLA-E;TAPBP;RPS19;HLA-DRA;TIMP1;CD47;BCAT1,14,0.001128825048288503,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,24,Fatty Acid Metabolism,0.0006356808021644386,3.2597125533348303,23.99413781159843,LDHA;HSP90AA1;APEX1;ECH1;ODC1;PSME1;DHCR24;MIF;CEL;ALDOA;GLUL;PRDX6,12,0.001297848304419062,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,25,Protein Secretion,0.0006708698952104698,4.090104642179928,29.886130140531545,CD63;ARF1;KRT18;PPT1;GNAS;ATP1A1;PAM;AP2M1;ATP6V1B1,9,0.0013149049946125208,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,26,UV Response Dn,0.0010078261155940607,3.275627719605763,22.601699023552147,NOTCH2;COL1A1;COL3A1;COL1A2;IGFBP5;ANXA2;DUSP1;SERPINE1;COL5A2;ERBB2;LAMC1,11,0.0018993646024657296,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,27,Androgen Response,0.003602570774643932,3.4301873453517144,19.298603039264496,KRT19;CCND1;TSC22D1;KRT8;DHCR24;SAT1;NDRG1;SLC38A2,8,0.006537998813242692,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,28,Pperoxisome,0.00457541037692627,3.2865853658536586,17.705028894470345,CRABP2;PRDX1;ECH1;CRABP1;DHCR24;CEL;PABPC1;SOD2,8,0.0075550684902512795,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,29,G2-M Checkpoint,0.0046255521368885385,2.5259853505406347,13.580100225543946,NOTCH2;HSPA8;MT2A;SLC38A1;ILF3;CCND1;NUMA1;NCL;STMN1;ODC1;HMGA1;HMGN2,12,0.0075550684902512795,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,30,Xenobiotic Metabolism,0.0046255521368885385,2.5259853505406347,13.580100225543946,MT2A;AHCY;JUP;PTGES3;SERPINE1;ECH1;TMBIM6;SPINT2;APOE;PTGDS;BCAT1;CFB,12,0.0075550684902512795,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,31,PI3K/AKT/mTOR  Signaling,0.00484745727525393,3.2525354119520578,17.333740173542928,ARF1;CFL1;SLC2A1;CALR;PFN1;SQSTM1;AP2M1;HSP90B1,8,0.007662109886691696,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,32,Notch Signaling,0.007971195406910945,5.608294930875576,27.098836980107382,NOTCH2;APH1A;NOTCH3;CCND1,4,0.012205892966832384,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,33,Cholesterol Homeostasis,0.010475384097409076,3.4708263872350558,15.822550469971569,ECH1;MAL2;CD9;CTNNB1;S100A11;ACTG1,6,0.015554358205243781,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,34,TGF-beta Signaling,0.011068822496125156,4.009688723974438,18.058125986560793,SERPINE1;CTNNB1;JUNB;THBS1;RHOA,5,0.015952126538533312,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,35,Inflammatory Response,0.029308469849829922,2.074113856068743,7.321370386955588,BST2;IFITM1;BTG2;MMP14;SERPINE1;HPN;TNFSF10;TIMP1;LY6E;TAPBP,10,0.03989208396226851,SHAP_with12m_top500,with12m,500,500
MSigDB_Hallmark_2020,36,heme Metabolism,0.029308469849829922,2.074113856068743,7.321370386955588,SELENBP1;PRDX2;BCAM;BTG2;TFRC;BSG;UCP2;SLC2A1;HDGF;CTSB,10,0.03989208396226851,SHAP_with12m_top500,with12m,500,500
```

### ./phase2/outputs/enrichment_shap_without12m_full.csv

Total data rows: 10502 (header + 10502 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
database,rank,term,p_value,z_score,combined_score,overlap_genes,n_overlap,adj_p_value,gene_list,scenario,size,n_genes_submitted
```
FIRST 20 DATA ROWS:
```csv
KEGG_2021_Human,1,Salmonella infection,3.521953018078585e-05,11.058922558922559,113.39719434402478,HSP90AA1;PODXL;PKN1;PFN1;RHOA;ACTG1,6,0.005001173285671591,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,2,Ferroptosis,0.00014657115641659294,33.4468085106383,295.2684100827493,TFRC;SAT1;CP,3,0.010406552105578098,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,3,NOD-like receptor signaling pathway,0.001079913030441522,9.714075165806927,66.35563094900988,HSP90AA1;PKN1;RHOA;CTSB,4,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,4,Dilated cardiomyopathy,0.0017838028065180675,13.628689087165409,86.25607933742052,TPM4;GNAS;ACTG1,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,5,Rap1 signaling pathway,0.0018644048515252163,8.334318277754326,52.37963511920258,GNAS;PFN1;RHOA;ACTG1,4,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,6,Hematopoietic cell lineage,0.0019479426217578455,13.200797872340425,82.3859356912581,TFRC;ANPEP;CD59,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,7,"Parathyroid hormone synthesis, secretion and action",0.0023667454978385074,12.299318322660607,74.36462396066707,MMP14;GNAS;RHOA,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,8,HIF-1 signaling pathway,0.0025619933727431465,11.949417904456041,71.30181411758254,TFRC;PGK1;ALDOA,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,9,Platelet activation,0.003686751554553751,10.460172322841569,58.60844537950275,GNAS;RHOA;ACTG1,3,0.05816874674962585,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,10,Yersinia infection,0.004871849321860696,9.439187043505875,50.256890616051635,PKN1;RHOA;ACTG1,3,0.06547798367302904,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,11,Fluid shear stress and atherosclerosis,0.005072238171854362,9.299436795994994,49.137973919606814,HSP90AA1;RHOA;ACTG1,3,0.06547798367302904,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,12,Cocaine addiction,0.006682897030368853,17.64450354609929,88.36726791367238,GNAS;FOSB,2,0.06579616827015197,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,13,Oxytocin signaling pathway,0.006734164844589255,8.369310976468931,41.85125407551329,GNAS;RHOA;ACTG1,3,0.06579616827015197,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,14,Vibrio cholerae infection,0.006950299465156898,17.276041666666668,85.84414194819459,GNAS;ACTG1,2,0.06579616827015197,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,15,Cholesterol metabolism,0.006950299465156898,17.276041666666668,85.84414194819459,LRP1;PLTP,2,0.06579616827015197,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,16,Glutathione metabolism,0.008955160836496808,15.071969696969697,71.07225417227201,GPX1;ANPEP,2,0.07947705242390916,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,17,Cortisol synthesis and secretion,0.011523761866123172,13.152777777777779,58.70537343689256,NR4A1;GNAS,2,0.08571833246629307,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,18,Glycolysis / Gluconeogenesis,0.012210781302115073,12.746794871794872,56.15518906635068,PGK1;ALDOA,2,0.08571833246629307,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,19,Amyotrophic lateral sclerosis,0.012871288261686096,4.731884057971015,20.59673750232504,GPX1;NDUFB11;PFN1;ACTG1,4,0.08571833246629307,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,20,Amphetamine addiction,0.012915373039423325,12.365049751243781,53.77976800231812,GNAS;FOSB,2,0.08571833246629307,SHAP_without12m_top50,without12m,50,50
```
LAST 20 DATA ROWS:
```csv
MSigDB_Hallmark_2020,30,PI3K/AKT/mTOR  Signaling,0.00484745727525393,3.2525354119520578,17.333740173542928,ARF1;CFL1;SLC2A1;CALR;PFN1;SQSTM1;AP2M1;HSP90B1,8,0.00791751354958142,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,31,Notch Signaling,0.007971195406910945,5.608294930875576,27.098836980107382,NOTCH2;APH1A;NOTCH3;CCND1,4,0.012599631449633428,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,32,TGF-beta Signaling,0.011068822496125156,4.009688723974438,18.058125986560793,SERPINE1;CTNNB1;JUNB;THBS1;RHOA,5,0.016949134447191646,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,33,G2-M Checkpoint,0.012147044967521652,2.2984062063816664,10.137509811385552,NOTCH2;HSPA8;MT2A;SLC38A1;CCND1;NUMA1;NCL;STMN1;ODC1;HMGA1;HMGN2,11,0.01750603539436944,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,34,heme Metabolism,0.012147044967521652,2.2984062063816664,10.137509811385552,C3;SELENBP1;PRDX2;BCAM;BTG2;TFRC;BSG;UCP2;SLC2A1;HDGF;CTSB,11,0.01750603539436944,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,35,Adipogenesis,0.029308469849829922,2.074113856068743,7.321370386955588,C3;NDUFB7;GPX3;APLP2;ECH1;UCP2;UBC;APOE;CYC1;ALDOA,10,0.03881391953085584,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,36,Inflammatory Response,0.029308469849829922,2.074113856068743,7.321370386955588,BST2;IFITM1;BTG2;MMP14;SERPINE1;HPN;TNFSF10;TIMP1;LY6E;TAPBP,10,0.03881391953085584,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,37,Xenobiotic Metabolism,0.029308469849829922,2.074113856068743,7.321370386955588,MT2A;JUP;PTGES3;SERPINE1;ECH1;SPINT2;APOE;PTGDS;BCAT1;CFB,10,0.03881391953085584,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,38,Apical Surface,0.09705771960273352,2.8648476223192816,6.6821122037109575,APP;HSPB1;THY1,3,0.12515337527720902,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,39,KRAS Signaling Up,0.12965160523268623,1.6351626016260163,3.3404808503516494,MMP11;SPON1;SLPI;JUP;IGFBP3;IGF2;CFB;MMP10,8,0.16289560657440066,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,40,IL-6/JAK/STAT3 Signaling,0.17333099873778088,1.8866109599689078,3.3063842355764335,JUN;STAT1;CD9;A2M,4,0.2123304734537816,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,41,Hedgehog Signaling,0.22698728149273847,2.2993149066855656,3.4095650726373203,MYH9;THY1,2,0.2679993611299758,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,42,Mitotic Spindle,0.23148950997896622,1.4278651115618661,2.089281816243083,UXT;NOTCH2;YWHAE;GSN;NUMA1;MYH9;ACTN4,7,0.2679993611299758,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,43,KRAS Signaling Dn,0.23518311282834609,1.4203932779114863,2.055864254779462,CPA2;BTG2;IGFBP2;MX1;KRT5;KLK7;ATP6V1B1,7,0.2679993611299758,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,44,Myc Targets V2,0.4274492922819714,1.3944348823866897,1.1851575544562791,NPM1;HSPD1,2,0.4760230754958318,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,45,E2F Targets,0.5626004121727441,1.0,0.5751856503053476,TFRC;TUBB;STMN1;HMGA1;NAP1L1,5,0.6126093376992102,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,46,Pancreas Beta Cells,0.6371302636481142,1.0,0.4507811487933908,SST,1,0.6786822373642956,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,47,Wnt-beta Catenin Signaling,0.6550827855909762,0.951121755706535,0.4023184736155008,CTNNB1,1,0.6829586488076136,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,48,DNA Repair,0.7276712445071681,0.794686486264526,0.2526355385251821,BCAM;IMPDH2;SUPT5H,3,0.7428310621010674,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,49,Bile Acid Metabolism,0.7736407907197486,0.7079225994888646,0.18168664166283727,APOA1;DHCR24,2,0.7736407907197486,SHAP_without12m_top500,without12m,500,500
```

### ./phase2/outputs/enrichment_shap_without12m_significant.csv

Total data rows: 1538 (header + 1538 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
database,rank,term,p_value,z_score,combined_score,overlap_genes,n_overlap,adj_p_value,gene_list,scenario,size,n_genes_submitted
```
FIRST 20 DATA ROWS:
```csv
KEGG_2021_Human,1,Salmonella infection,3.521953018078585e-05,11.058922558922559,113.39719434402478,HSP90AA1;PODXL;PKN1;PFN1;RHOA;ACTG1,6,0.005001173285671591,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,2,Ferroptosis,0.00014657115641659294,33.4468085106383,295.2684100827493,TFRC;SAT1;CP,3,0.010406552105578098,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,3,NOD-like receptor signaling pathway,0.001079913030441522,9.714075165806927,66.35563094900988,HSP90AA1;PKN1;RHOA;CTSB,4,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,4,Dilated cardiomyopathy,0.0017838028065180675,13.628689087165409,86.25607933742052,TPM4;GNAS;ACTG1,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,5,Rap1 signaling pathway,0.0018644048515252163,8.334318277754326,52.37963511920258,GNAS;PFN1;RHOA;ACTG1,4,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,6,Hematopoietic cell lineage,0.0019479426217578455,13.200797872340425,82.3859356912581,TFRC;ANPEP;CD59,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,7,"Parathyroid hormone synthesis, secretion and action",0.0023667454978385074,12.299318322660607,74.36462396066707,MMP14;GNAS;RHOA,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
KEGG_2021_Human,8,HIF-1 signaling pathway,0.0025619933727431465,11.949417904456041,71.30181411758254,TFRC;PGK1;ALDOA,3,0.04547538236619085,SHAP_without12m_top50,without12m,50,50
Reactome_2022,1,EPHB-mediated Forward Signaling R-HSA-3928662,1.5162945853924684e-06,57.73913043478261,773.6605222140159,PKN1;RNASE1;RHOA;ACTG1,4,0.0006095504233277723,SHAP_without12m_top50,without12m,50,50
Reactome_2022,2,Sema3A PAK Dependent Axon Repulsion R-HSA-399954,8.046099028490012e-06,97.89034369885434,1148.2853674678522,HSP90AA1;PKN1;RNASE1,3,0.0015806237982084392,SHAP_without12m_top50,without12m,50,50
Reactome_2022,3,RHO GTPase Cycle R-HSA-9012999,1.2501349009930615e-05,8.585505333773233,96.9275563322676,TMEM59;HSP90AA1;TPM4;TFRC;PKN1;RNASE1;RHOA;ACTG1,8,0.0015806237982084392,SHAP_without12m_top50,without12m,50,50
Reactome_2022,4,Regulation Of Actin Dynamics For Phagocytic Cup Formation R-HSA-2029482,1.732412185617266e-05,29.823088455772115,326.9627671034966,HSP90AA1;PKN1;RNASE1;ACTG1,4,0.0015806237982084392,SHAP_without12m_top50,without12m,50,50
Reactome_2022,5,Semaphorin Interactions R-HSA-373755,1.9659499977716905e-05,28.82608695652174,312.3868594993703,HSP90AA1;PKN1;RNASE1;RHOA,4,0.0015806237982084392,SHAP_without12m_top50,without12m,50,50
Reactome_2022,6,Signaling By Rho GTPases R-HSA-194315,2.7060603609260663e-05,6.676973305166123,70.22461022668759,TMEM59;HSP90AA1;TPM4;TFRC;PKN1;PFN1;RNASE1;RHOA;ACTG1,9,0.0018130604418204643,SHAP_without12m_top50,without12m,50,50
Reactome_2022,7,"Signaling By Rho GTPases, Miro GTPases And RHOBTB3 R-HSA-9716542",3.279542095761281e-05,6.507474429583006,67.19111591446564,TMEM59;HSP90AA1;TPM4;TFRC;PKN1;PFN1;RNASE1;RHOA;ACTG1,9,0.0018833941749943357,SHAP_without12m_top50,without12m,50,50
Reactome_2022,8,VEGFR2 Mediated Vascular Permeability R-HSA-5218920,4.122055222407173e-05,52.994680851063826,535.0646948580581,HSP90AA1;PKN1;RNASE1,3,0.0020713327492596044,SHAP_without12m_top50,without12m,50,50
Reactome_2022,9,Fcgamma Receptor (FCGR) Dependent Phagocytosis R-HSA-2029480,6.60236323201855e-05,20.814038763750656,200.34548463287032,HSP90AA1;PKN1;RNASE1;ACTG1,4,0.0029490555769682856,SHAP_without12m_top50,without12m,50,50
Reactome_2022,10,EPH-Ephrin Signaling R-HSA-2682334,7.869565920366472e-05,19.853073463268366,187.61000681193661,PKN1;RNASE1;RHOA;ACTG1,4,0.003130312986553908,SHAP_without12m_top50,without12m,50,50
Reactome_2022,11,VEGFA-VEGFR2 Pathway R-HSA-4420097,8.565533047784326e-05,19.40498290180752,181.73114029905219,HSP90AA1;PKN1;RNASE1;RHOA,4,0.003130312986553908,SHAP_without12m_top50,without12m,50,50
Reactome_2022,12,RHOH GTPase Cycle R-HSA-9013407,9.903955378900077e-05,38.524177949709866,355.1925837792589,TMEM59;TFRC;PKN1,3,0.003317825051931526,SHAP_without12m_top50,without12m,50,50
```
LAST 20 DATA ROWS:
```csv
MSigDB_Hallmark_2020,18,Estrogen Response Late,4.551923375608182e-05,3.4703557312252964,34.69444971558032,XBP1;ST14;EMP2;LSR;FOS;PRSS23;ASS1;SERPINA5;KRT19;ZFP36;CCND1;MDK;SCNN1A;CD9;MEST;LTF,16,0.00012391346966933385,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,19,Estrogen Response Early,0.00016069795575379561,3.2290331568682085,28.208782013846974,XBP1;KRT8;SLC2A1;FOS;PRSS23;THSD4;KRT19;MUC1;KRT18;CCND1;ELF3;PODXL;SCNN1A;LRIG1;TGM2,15,0.00041443157010189396,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,20,Fatty Acid Metabolism,0.00017495701739962544,3.56319478864264,30.825092036918832,HSP90AA1;ECH1;ODC1;DHCR24;MIF;CEL;PRDX6;LDHA;APEX1;PSME1;ALDOA;GLUL;S100A10,13,0.00042864469262908234,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,21,Reactive Oxygen Species Pathway,0.00020253908941845664,6.578093306288032,55.94390535095862,PRDX2;GPX3;PRDX1;SOD2;JUNB;PRDX6;FTL,7,0.0004725912086430655,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,22,Oxidative Phosphorylation,0.0005298566553190931,2.9912385503783354,22.56262537515248,GPI;SLC25A3;NDUFB7;COX4I1;ECH1;NDUFC2;PHB2;COX6B1;LDHB;LDHA;UQCRFS1;CYC1;SLC25A5;SLC25A6,14,0.001180135277756162,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,23,Protein Secretion,0.0006708698952104698,4.090104642179928,29.886130140531545,CD63;ARF1;KRT18;GNAS;ATP1A1;ERGIC3;PAM;AP2M1;ATP6V1B1,9,0.0014292445593614357,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,24,IL-2/STAT5 Signaling,0.0015547004102043312,2.771875206994767,17.92425456152768,IFITM3;XBP1;AHNAK;CD81;S100A1;ODC1;NDRG1;MUC1;SYNGR2;TNFSF10;LRIG1;TGM2;PLEC,13,0.003174180004167176,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,25,Allograft Rejection,0.0016259464139164038,2.7569095960206,17.70395047894754,CD74;NPM1;RPS9;STAT1;RPS3A;HLA-A;THY1;HLA-E;TAPBP;RPS19;TIMP1;CD47;BCAT1,13,0.0031868549712761513,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,26,Cholesterol Homeostasis,0.0024850933195517504,4.118282825224789,24.699175014651566,ECH1;MAL2;CD9;CTNNB1;CLU;S100A11;ACTG1,7,0.004683445102232145,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,27,UV Response Dn,0.0033897521776855414,2.9494364910143163,16.773440794623088,NOTCH2;COL1A1;COL3A1;COL1A2;IGFBP5;ANXA2;DUSP1;SERPINE1;COL5A2;ERBB2,10,0.006151772470614501,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,28,Androgen Response,0.003602570774643932,3.4301873453517144,19.298603039264496,KRT19;CCND1;TSC22D1;KRT8;DHCR24;SAT1;NDRG1;SLC38A2,8,0.006304498855626881,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,29,Pperoxisome,0.00457541037692627,3.2865853658536586,17.705028894470345,CRABP2;PRDX1;ECH1;CRABP1;DHCR24;CEL;PABPC1;SOD2,8,0.007730865809289215,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,30,PI3K/AKT/mTOR  Signaling,0.00484745727525393,3.2525354119520578,17.333740173542928,ARF1;CFL1;SLC2A1;CALR;PFN1;SQSTM1;AP2M1;HSP90B1,8,0.00791751354958142,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,31,Notch Signaling,0.007971195406910945,5.608294930875576,27.098836980107382,NOTCH2;APH1A;NOTCH3;CCND1,4,0.012599631449633428,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,32,TGF-beta Signaling,0.011068822496125156,4.009688723974438,18.058125986560793,SERPINE1;CTNNB1;JUNB;THBS1;RHOA,5,0.016949134447191646,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,33,G2-M Checkpoint,0.012147044967521652,2.2984062063816664,10.137509811385552,NOTCH2;HSPA8;MT2A;SLC38A1;CCND1;NUMA1;NCL;STMN1;ODC1;HMGA1;HMGN2,11,0.01750603539436944,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,34,heme Metabolism,0.012147044967521652,2.2984062063816664,10.137509811385552,C3;SELENBP1;PRDX2;BCAM;BTG2;TFRC;BSG;UCP2;SLC2A1;HDGF;CTSB,11,0.01750603539436944,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,35,Adipogenesis,0.029308469849829922,2.074113856068743,7.321370386955588,C3;NDUFB7;GPX3;APLP2;ECH1;UCP2;UBC;APOE;CYC1;ALDOA,10,0.03881391953085584,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,36,Inflammatory Response,0.029308469849829922,2.074113856068743,7.321370386955588,BST2;IFITM1;BTG2;MMP14;SERPINE1;HPN;TNFSF10;TIMP1;LY6E;TAPBP,10,0.03881391953085584,SHAP_without12m_top500,without12m,500,500
MSigDB_Hallmark_2020,37,Xenobiotic Metabolism,0.029308469849829922,2.074113856068743,7.321370386955588,MT2A;JUP;PTGES3;SERPINE1;ECH1;SPINT2;APOE;PTGDS;BCAT1;CFB,10,0.03881391953085584,SHAP_without12m_top500,without12m,500,500
```

### ./phase2/outputs/permutation_importances_Random_Forest_12m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,importance_std,rank
```
FIRST 20 DATA ROWS:
```csv
CHCHD2,0.0839430894308943,0.043135904528613045,1
TMEM59,0.03861788617886176,0.03570531411445127,2
LTBP4,0.035975609756097524,0.028787979595397244,3
CD59,0.031910569105691074,0.02679614239784609,4
CD63,0.027642276422764216,0.013334324769802217,5
JUNB,0.019308943089430874,0.01114184558834613,6
IGFBP7,0.017886178861788633,0.004434435818957609,7
RPS10,0.01788617886178858,0.004434435818957604,8
TNFSF10,0.017479674796747956,0.01840974288491747,9
GNAS,0.01727642276422763,0.013085706181154365,10
ACTG1,0.016260162601625994,0.010945456925070119,11
CD47,0.015853658536585356,0.011633404895328608,12
DMKN,0.015447154471544702,0.013147123275444076,13
COL6A1,0.01443089430894308,0.012740190198548636,14
RPL3,0.013821138211382126,0.008896775865137931,15
PLEC,0.013821138211382126,0.007029112384467722,16
MT1G,0.01341463414634144,0.008680551424415685,17
ATP5E,0.0128048780487805,0.008382760417602154,18
COL3A1,0.012398373983739818,0.008973065062863448,19
FOSB,0.011788617886178838,0.013071492025051635,20
```
LAST 20 DATA ROWS:
```csv
A2M,-0.014227642276422777,0.010716606769482991,481
STMN1,-0.014227642276422788,0.018716852736945268,482
RPL36,-0.014634146341463428,0.010395700693125556,483
UBB,-0.014837398373983755,0.008720909736961359,484
PKM2,-0.01504065040650408,0.012957217439438404,485
RPS25,-0.016260162601626032,0.01149767123880566,486
PTGS1,-0.017073170731707332,0.0069344398818016245,487
GRINA,-0.017073170731707332,0.011177013890136204,488
SLC38A2,-0.019105691056910585,0.011962552007774125,489
TXNIP,-0.020528455284552865,0.015058493042269493,490
MAL2,-0.02052845528455288,0.028922557118364455,491
CLNS1A,-0.022357723577235793,0.013573827526068305,492
IGFBP3,-0.023373983739837418,0.012405036194851336,493
CRABP2,-0.02459349593495937,0.009766677867263393,494
H3F3B,-0.025203252032520346,0.010411584125907081,495
NOTUM,-0.025406504065040674,0.0147760173729072,496
SEPT2,-0.02601626016260165,0.013537256752314411,497
CMTM6,-0.02764227642276425,0.038265400323540526,498
CDK16,-0.03130081300813012,0.02280049375996774,499
UCP2,-0.03556910569105694,0.030205330985798914,500
```

### ./phase2/outputs/permutation_importances_Random_Forest_18m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,importance_std,rank
```
FIRST 20 DATA ROWS:
```csv
TRIM28,0.019517543859649208,0.007153292293991272,1
OAZ1,0.018859649122807118,0.008945648269461022,2
PODXL,0.018311403508772015,0.007140675506651283,3
ANPEP,0.017214912280701815,0.012357315064809063,4
GPI,0.01502192982456148,0.011096252857851631,5
ATN1,0.015021929824561474,0.01191144821135716,6
DMKN,0.01425438596491236,0.010619561414739688,7
NONO,0.01425438596491235,0.00991703425841669,8
LTBP4,0.01381578947368427,0.013679359801535692,9
PTGS1,0.012390350877193054,0.005548939003894737,10
EMP2,0.012280701754386048,0.008275422045663679,11
TMSL3,0.011732456140350952,0.007290636056964604,12
FAU,0.011513157894736914,0.014532128810834962,13
RPL7A,0.011293859649122932,0.0031417870135733612,14
CP,0.010855263157894812,0.009577209091362998,15
ITGB1,0.010745614035087784,0.0034950389145853604,16
NCRNA00188,0.010307017543859728,0.002361914389094115,17
STAT1,0.010087719298245685,0.007497947805824023,18
RPL35A,0.00986842105263166,0.004652018297279919,19
RPS8,0.00953947368421059,0.0027324420601704093,20
```
LAST 20 DATA ROWS:
```csv
SORL1,-0.012938596491227975,0.0076408997325369985,481
TM4SF1,-0.013048245614035007,0.020161429632954295,482
HMGA1,-0.013157894736842042,0.006952134861468143,483
RPS23,-0.01337719298245607,0.009606664962197151,484
JUNB,-0.013706140350877116,0.01107673246046035,485
IFI27,-0.01381578947368414,0.008719690943890825,486
RPL14,-0.014912280701754311,0.016659451346762014,487
H3F3B,-0.015679824561403436,0.006450686877229256,488
CALM2,-0.016885964912280605,0.006673300023992518,489
SEPP1,-0.016885964912280605,0.005285952102278044,490
MCL1,-0.016995614035087654,0.012073857206987502,491
SPINT2,-0.017434210526315705,0.013298318665031032,492
MAGED2,-0.017543859649122716,0.006374755199012541,493
LGALS1,-0.017872807017543773,0.008437284475092385,494
FCGBP,-0.024561403508771874,0.02002230212370761,495
CD9,-0.026206140350877132,0.017926541760962738,496
ATP5G2,-0.028618421052631515,0.024662279141745486,497
APOE,-0.03037280701754378,0.013203958112974463,498
MYL9,-0.030701754385964848,0.015272355567087838,499
MT1G,-0.03114035087719291,0.018564085469358164,500
```

### ./phase2/outputs/permutation_importances_Random_Forest_24m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,importance_std,rank
```
FIRST 20 DATA ROWS:
```csv
TFRC,0.017099567099567108,0.013451877401624292,1
TAGLN,0.015512265512265507,0.007137024452577237,2
FAU,0.01464646464646467,0.006837528001846269,3
IFITM1,0.014430014430014453,0.006920391808532054,4
SAT1,0.013997113997114004,0.014080174849498459,5
TUBB2C,0.01334776334776337,0.007885511088382818,6
UBC,0.013059163059163045,0.009309596250083997,7
SERPINE1,0.012626262626262649,0.007224020344336507,8
HSPG2,0.012626262626262636,0.004611400052315983,9
PABPC4,0.012409812409812437,0.007177391120026473,10
BCAT1,0.011688311688311692,0.0042415406801440516,11
HDLBP,0.010966810966810991,0.021456126214679194,12
SULF1,0.010533910533910543,0.006140814669827774,13
PKN1,0.01031746031746034,0.0036512499073246872,14
LRIG1,0.010317460317460336,0.00577245669234332,15
PODXL,0.010173160173160183,0.00675634479573417,16
ITM2B,0.010101010101010104,0.0060794731408198915,17
SLC44A2,0.009668109668109682,0.005021562089842788,18
ACTA2,0.009668109668109659,0.00505256606060942,19
UCP2,0.00909090909090909,0.008278100726847589,20
```
LAST 20 DATA ROWS:
```csv
H19,-0.005483405483405442,0.0034782022491180163,481
DSP,-0.005844155844155815,0.0072038152733365475,482
RPS13,-0.005844155844155815,0.0036283667996191084,483
CAP1,-0.005988455988455943,0.0032435449917732964,484
ITM2C,-0.00606060606060607,0.003131678847649468,485
GPI,-0.006277056277056255,0.0033694933416553107,486
FLNA,-0.006421356421356398,0.0041251925999777105,487
MAL2,-0.006854256854256846,0.0032145266103817366,488
YAP1,-0.007215007215007189,0.00396497306321332,489
PTGS1,-0.007359307359307317,0.0058240796740578905,490
HSP90AA1,-0.0073593073593073615,0.008560051919171068,491
CD63,-0.007647907647907634,0.005234735107421952,492
MARCKSL1,-0.007792207792207769,0.003647683884491932,493
RPS16,-0.008080808080808058,0.006321268719714145,494
HDGF,-0.008152958152958127,0.005718092366832469,495
EEF1A1P9,-0.008441558441558387,0.004043623742915435,496
CRABP1,-0.00937950937950937,0.005252604537720432,497
HPN,-0.00945165945165943,0.004951093351889684,498
OVGP1,-0.009668109668109623,0.004496518456243245,499
TACSTD2,-0.011038961038960996,0.004448214326637316,500
```

### ./phase2/outputs/permutation_importances_full.csv

Total data rows: 536 (header + 536 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,mean_importance,std_importance,n_thresholds_present,rank
```
FIRST 20 DATA ROWS:
```csv
CHCHD2,0.027421233855765337,0.0489543020659216,3,1
LTBP4,0.016933833413294273,0.017690063566126422,3,2
TMEM59,0.012486087879220125,0.022779667049634772,3,3
FAU,0.012039657378232503,0.0023875014470220524,3,4
TFRC,0.01123618705855552,0.008292071575346302,2,5
CD59,0.010929095805540008,0.01844666528274226,3,6
DMKN,0.010525814104119657,0.007514746192953341,3,7
ANPEP,0.009364578451548955,0.006955940663479971,3,8
PODXL,0.008207591688015338,0.011216514916575925,3,9
ANXA1,0.007754824515094109,0.0029993590119187993,3,10
OAZ1,0.0074430039128370665,0.009913171532344833,3,11
GNAS,0.0074092404885088,0.009341664057915417,3,12
CD63,0.007286134620858652,0.018259207141766237,3,13
GPI,0.006776746467054583,0.011434763554317325,3,14
TAGLN,0.006523094352041751,0.008044796234128328,3,15
HDLBP,0.006515395411415985,0.004276245991036686,3,16
TRIM28,0.006385304539990075,0.011626765551877088,3,17
PABPC4,0.00636613630034686,0.006211187200746013,3,18
IGFBP7,0.005888960205391543,0.010390474702687271,3,19
THSD4,0.005864802126034505,0.0011629009051013237,3,20
```
LAST 20 DATA ROWS:
```csv
MCL1,-0.007722068320592034,0.008068576653176235,3,517
UBB,-0.00786107375484781,0.007949540506369888,3,518
HMGA1,-0.00788465682560674,0.008829558994602353,3,519
ATP5G2,-0.008048372193109006,0.017954046780324456,3,520
CRABP2,-0.008621080756831689,0.013832788558346737,3,521
UCP2,-0.00878951582578026,0.023622565116176098,3,522
SORL1,-0.008908322635857892,0.005699667946342073,2,523
CD9,-0.00904803042960935,0.014866757886076967,3,524
MAL2,-0.009127570712936552,0.010451331782003736,3,525
CLNS1A,-0.009378158688171505,0.011642549317311858,3,526
CDK16,-0.010046905265133745,0.01840696755203658,3,527
CMTM6,-0.010195871083226662,0.016210631971365075,3,528
APOE,-0.010871872802232207,0.016888631739585255,3,529
H3F3B,-0.010982189552471941,0.01706199735403381,3,530
IGJ,-0.011403508771929733,,1,531
MYL9,-0.011514435262830613,0.01695375793227047,3,532
LYZ,-0.012280701754385882,,1,533
IGFBP3,-0.013057605905006391,0.014589561448583224,2,534
SEPT2,-0.014926989730423595,0.01568259664200916,2,535
NOTUM,-0.01686991869918697,0.012072554800745997,2,536
```

### ./phase2/outputs/phase2_03c_gene_set_diagnostic.csv

```csv
pair,shared,only_a,only_b
12m_vs_18m,478,22,22
12m_vs_24m,470,30,30
18m_vs_24m,472,28,28
12m_vs_phase2_03b_list,469,31,31
18m_vs_phase2_03b_list,475,25,25
24m_vs_phase2_03b_list,464,36,36
```

### ./phase2/outputs/phase2_03c_reconstruction_verification.csv

```csv
threshold,reported_auc,recomputed_auc,diff
12,0.4756,0.47560975609756095,9.75609756093121e-06
18,0.6118,0.611842105263158,4.2105263157954376e-05
24,0.8247,0.8246753246753247,2.467532467531619e-05
```

### ./phase2/outputs/rf_feature_importances_full.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,mean_importance,std_importance,rank
```
FIRST 20 DATA ROWS:
```csv
feature_469,0.010284553451426892,0.0027413617506455005,1
feature_362,0.010197727625222272,0.00900516381251425,2
feature_225,0.009799069204657493,0.006419244438499581,3
feature_47,0.006539286138688663,0.00756689153237032,4
feature_351,0.006397863138669347,0.00786351874892296,5
feature_417,0.00624722521201746,0.004786964460921714,6
feature_456,0.0061865459138647555,0.00424655166726283,7
feature_286,0.005680688501006813,0.005205066825614002,8
feature_495,0.005607484277285254,0.0063434990505666705,9
feature_385,0.005458295039352908,0.006947260192984201,10
feature_415,0.005430224521563072,0.006232372081939163,11
feature_176,0.00541528474809871,0.0022133448023745617,12
feature_83,0.005210223607656276,0.005511072331631208,13
feature_22,0.005154829942792728,0.005819274062616207,14
feature_84,0.004941468718646151,0.0020854875101506284,15
feature_43,0.004929107724966168,0.002218206011518437,16
feature_0,0.004901798361682685,0.00031745084351008133,17
feature_363,0.004899535095098221,0.0035997300684515753,18
feature_496,0.0047476041225184736,0.004030671560794947,19
feature_423,0.004649463628606265,0.0008498195151098073,20
```
LAST 20 DATA ROWS:
```csv
feature_161,0.000614250605121827,0.00035671755013078803,481
feature_14,0.0005855909620068455,0.0005403142560810748,482
feature_399,0.0005848867607757701,0.00043007036857615463,483
feature_270,0.00057791831603923,0.0003099688062369786,484
feature_376,0.0005705660470796461,0.00048517385537699605,485
feature_27,0.0005667109905136458,0.000577790002015754,486
feature_121,0.000551668820832969,0.0002278581754779323,487
feature_481,0.0005508324645881797,0.0004591480720269664,488
feature_408,0.0005343946456686965,0.00038484025697549417,489
feature_265,0.0005251959736044502,0.00031055151596341875,490
feature_214,0.0005156208419042199,0.00033979762998589567,491
feature_444,0.000509889281747709,0.00045635244908414784,492
feature_178,0.0005089181181357474,0.0002703527581874985,493
feature_3,0.0004880926088894075,0.00028969534954420534,494
feature_68,0.00048376370358241575,0.00022432701343860504,495
feature_339,0.0004786022818698125,0.00047083741487994295,496
feature_160,0.0004713252189407471,0.00031899615910267894,497
feature_235,0.0004659325217005149,3.210148821703833e-05,498
feature_475,0.0004198147124472353,0.00021233287993656767,499
feature_297,0.00033351510519146166,0.0002407314275141305,500
```

### ./phase2/outputs/rf_feature_importances_named.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,mean_importance,std_importance,variance_in_data,rank
```
FIRST 20 DATA ROWS:
```csv
PRSS23,0.010284553451426892,0.0027413617506455005,14334765.179382369,1
NAP1L1,0.010197727625222272,0.00900516381251425,20985274.504566997,2
KLK5,0.009799069204657493,0.006419244438499581,51072156.340279885,3
GNB2L1,0.006539286138688663,0.00756689153237032,416035740.04054374,4
PPT1,0.006397863138669347,0.00786351874892296,21722710.569126055,5
ANPEP,0.00624722521201746,0.004786964460921714,16542342.98231921,6
HNRNPC,0.0061865459138647555,0.00424655166726283,14846170.294782845,7
EMP2,0.005680688501006813,0.005205066825614002,33063797.554845598,8
TGFBI,0.005607484277285254,0.0063434990505666705,13195019.599627726,9
APOA1,0.005458295039352908,0.006947260192984201,18415921.822647057,10
ARF1,0.005430224521563072,0.006232372081939163,16585525.183135867,11
PTGDS,0.00541528474809871,0.0022133448023745617,71449608.6658708,12
ALDOA,0.005210223607656276,0.005511072331631208,211945710.13002852,13
BCAM,0.005154829942792728,0.005819274062616207,1008786432.2621472,14
IFITM3,0.004941468718646151,0.0020854875101506284,210911071.16115457,15
PABPC1,0.004929107724966168,0.002218206011518437,451833856.68229353,16
IGF2,0.004901798361682685,0.00031745084351008133,24533398096.4799,17
SCNN1A,0.004899535095098221,0.0035997300684515753,20681437.05286823,18
COL12A1,0.0047476041225184736,0.004030671560794947,13146809.257254882,19
PAX8,0.004649463628606265,0.0008498195151098073,15904086.086431863,20
```
LAST 20 DATA ROWS:
```csv
NACA,0.000614250605121827,0.00035671755013078803,81752693.42645623,481
C3,0.0005855909620068455,0.0005403142560810748,2039212337.8789022,482
GAS5,0.0005848867607757701,0.00043007036857615463,17754961.878126014,483
TIMP3,0.00057791831603923,0.0003099688062369786,36658638.20427623,484
CDK16,0.0005705660470796461,0.00048517385537699605,19102831.021681905,485
FTL,0.0005667109905136458,0.000577790002015754,878129272.7711498,486
PABPC4,0.000551668820832969,0.0002278581754779323,130863969.80232932,487
PLP2,0.0005508324645881797,0.0004591480720269664,13968690.842342142,488
MYCL1,0.0005343946456686965,0.00038484025697549417,17100717.232329063,489
SEPP1,0.0005251959736044502,0.00031055151596341875,38117851.56555844,490
CCT2,0.0005156208419042199,0.00033979762998589567,53965757.70960396,491
CCND1,0.000509889281747709,0.00045635244908414784,15166429.554011302,492
RPL6,0.0005089181181357474,0.0002703527581874985,68986419.10675271,493
CLU,0.0004880926088894075,0.00028969534954420534,5014037029.57069,494
TMSB10,0.00048376370358241575,0.00022432701343860504,274278122.4092843,495
MFGE8,0.0004786022818698125,0.00047083741487994295,23884601.414602675,496
SPOCK2,0.0004713252189407471,0.00031899615910267894,85025664.74035195,497
ATN1,0.0004659325217005149,3.210148821703833e-05,47138166.850752205,498
NUCKS1,0.0004198147124472353,0.00021233287993656767,14132172.523040691,499
EEF1B2,0.00033351510519146166,0.0002407314275141305,30743861.480119284,500
```

### ./phase2/outputs/rf_importances_Random_Forest_12m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance
```
FIRST 20 DATA ROWS:
```csv
feature_362,0.02265609823508357
feature_47,0.01720361735680148
feature_385,0.015281436508690356
feature_495,0.014577288245064823
feature_415,0.01421942029753417
feature_22,0.013343028674931702
feature_83,0.013003763767758645
feature_417,0.012030276160867256
feature_334,0.010571707579503507
feature_463,0.010508564402830977
feature_460,0.009496827640375547
feature_67,0.009073607736827343
feature_354,0.0086452018024571
feature_254,0.008576641070325582
feature_113,0.008558920394224257
feature_34,0.008543196185456611
feature_225,0.008343039533724826
feature_131,0.008279241680765303
feature_43,0.00787001779482403
feature_456,0.007591321327044717
```
LAST 20 DATA ROWS:
```csv
feature_122,0.0
feature_155,0.0
feature_273,0.0
feature_133,0.0
feature_339,0.0
feature_290,0.0
feature_233,0.0
feature_149,0.0
feature_376,0.0
feature_78,0.0
feature_384,0.0
feature_173,0.0
feature_39,0.0
feature_433,0.0
feature_44,0.0
feature_41,0.0
feature_450,0.0
feature_192,0.0
feature_491,0.0
feature_27,0.0
```

### ./phase2/outputs/rf_importances_Random_Forest_18m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance
```
FIRST 20 DATA ROWS:
```csv
feature_225,0.018287240735696056
feature_351,0.01748211897829499
feature_395,0.011798763926624132
feature_452,0.010999168579053531
feature_496,0.010447417483375177
feature_267,0.010243811174224123
feature_363,0.009975557275333512
feature_66,0.009424508690035997
feature_469,0.009408063889298077
feature_345,0.008578177270225076
feature_282,0.008098784995945013
feature_7,0.008028415108726383
feature_115,0.007231536347167906
feature_239,0.007109130833616482
feature_165,0.006783361851213716
feature_39,0.006718073358539661
feature_459,0.006544333796666529
feature_176,0.006483204208208456
feature_200,0.006477040894101453
feature_421,0.006452944830311918
```
LAST 20 DATA ROWS:
```csv
feature_425,0.00013693967445579464
feature_109,0.00012957791868737327
feature_245,0.0001250226164692499
feature_265,0.00011595155898953373
feature_172,0.00010896667973418387
feature_3,0.00010595474601369496
feature_436,0.00010056018716141179
feature_23,9.910353151988289e-05
feature_157,8.699419412794052e-05
feature_149,8.318568820936512e-05
feature_31,5.094829993343915e-05
feature_433,4.775456563037289e-05
feature_356,4.188236128588663e-05
feature_185,1.38700363314763e-19
feature_164,1.1425392614482976e-19
feature_292,0.0
feature_187,0.0
feature_209,0.0
feature_364,0.0
feature_432,0.0
```

### ./phase2/outputs/rf_importances_Random_Forest_24m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance
```
FIRST 20 DATA ROWS:
```csv
feature_469,0.013993336553236476
feature_286,0.013040434230645841
feature_456,0.01054081284477899
feature_205,0.010385278165349324
feature_451,0.0094065474404372
feature_117,0.0074404750600450195
feature_176,0.007429462345845638
feature_145,0.00722239724624912
feature_411,0.0069269739807191
feature_90,0.006896161718876527
feature_84,0.00681940059642745
feature_98,0.006691504998069662
feature_401,0.006545853798766303
feature_417,0.006403614503042358
feature_389,0.006113847581085485
feature_313,0.006083365154515097
feature_76,0.005677279658859927
feature_336,0.005542837455668902
feature_299,0.005532784182962008
feature_468,0.00534705588831104
```
LAST 20 DATA ROWS:
```csv
feature_238,0.00032249924140507043
feature_339,0.00031698360698365237
feature_231,0.00031261779731751155
feature_237,0.0003026973322878338
feature_332,0.0002956864149959739
feature_114,0.0002800679350541007
feature_418,0.00027480549859565146
feature_361,0.0002704472550433836
feature_383,0.00026538534583566293
feature_68,0.0002514103820205108
feature_118,0.00023736156403741414
feature_273,0.0002352396468453636
feature_136,0.00020891856459153354
feature_71,0.00019168761498257396
feature_85,0.00016100521791574167
feature_427,0.00015734430732170513
feature_218,0.00011096510299665914
feature_49,9.702321014894935e-20
feature_357,0.0
feature_128,0.0
```

### ./phase2/outputs/rf_importances_named_Random_Forest_12m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,rank
```
FIRST 20 DATA ROWS:
```csv
NAP1L1,0.02265609823508357,1
GNB2L1,0.01720361735680148,2
APOA1,0.015281436508690356,3
TGFBI,0.014577288245064823,4
ARF1,0.01421942029753417,5
BCAM,0.013343028674931702,6
ALDOA,0.013003763767758645,7
ANPEP,0.012030276160867256,8
TIMP2,0.010571707579503507,9
MAGED2,0.010508564402830977,10
LMNA,0.009496827640375547,11
RPS20,0.009073607736827343,12
A2M,0.0086452018024571,13
EPCAM,0.008576641070325582,14
NCRNA00188,0.008558920394224257,15
RPLP0,0.008543196185456611,16
KLK5,0.008343039533724826,17
AMY1A,0.008279241680765303,18
PABPC1,0.00787001779482403,19
HNRNPC,0.007591321327044717,20
```
LAST 20 DATA ROWS:
```csv
YWHAZ,0.0,481
MYH9,0.0,482
PTMS,0.0,483
KRT19,0.0,484
MFGE8,0.0,485
OAZ1,0.0,486
SLC2A1,0.0,487
MEST,0.0,488
CDK16,0.0,489
RPL28,0.0,490
HDGF,0.0,491
IGFBP5,0.0,492
RPL37A,0.0,493
PRDX1,0.0,494
RPS24,0.0,495
RPS14,0.0,496
GRINA,0.0,497
CD63,0.0,498
SLC38A2,0.0,499
FTL,0.0,500
```

### ./phase2/outputs/rf_importances_named_Random_Forest_18m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,rank
```
FIRST 20 DATA ROWS:
```csv
KLK5,0.018287240735696056,1
PPT1,0.01748211897829499,2
ATP6V1B1,0.011798763926624132,3
NDUFB11,0.010999168579053531,4
COL12A1,0.010447417483375177,5
GSN,0.010243811174224123,6
SCNN1A,0.009975557275333512,7
RPL27A,0.009424508690035997,8
PRSS23,0.009408063889298077,9
HSPG2,0.008578177270225076,10
EIF3E,0.008098784995945013,11
CD74,0.008028415108726383,12
CP,0.007231536347167906,13
HP,0.007109130833616482,14
DCN,0.006783361851213716,15
RPL37A,0.006718073358539661,16
PRDX6,0.006544333796666529,17
PTGDS,0.006483204208208456,18
CSDE1,0.006477040894101453,19
IGFBP4,0.006452944830311918,20
```
LAST 20 DATA ROWS:
```csv
ARL6IP1,0.00013693967445579464,481
YBX1,0.00012957791868737327,482
TACSTD2,0.0001250226164692499,483
SEPP1,0.00011595155898953373,484
HSPA1A,0.00010896667973418387,485
CLU,0.00010595474601369496,486
THBS2,0.00010056018716141179,487
SPARC,9.910353151988289e-05,488
UBB,8.699419412794052e-05,489
MEST,8.318568820936512e-05,490
ACTB,5.094829993343915e-05,491
PRDX1,4.775456563037289e-05,492
JUN,4.188236128588663e-05,493
NDRG1,1.38700363314763e-19,494
RPL26,1.1425392614482976e-19,495
SLC44A2,0.0,496
COL6A2,0.0,497
TMBIM6,0.0,498
COL18A1,0.0,499
CAPNS1,0.0,500
```

### ./phase2/outputs/rf_importances_named_Random_Forest_24m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,rank
```
FIRST 20 DATA ROWS:
```csv
PRSS23,0.013993336553236476,1
EMP2,0.013040434230645841,2
HNRNPC,0.01054081284477899,3
PTPRF,0.010385278165349324,4
TFRC,0.0094065474404372,5
FLNA,0.0074404750600450195,6
PTGDS,0.007429462345845638,7
RPL35,0.00722239724624912,8
MT1G,0.0069269739807191,9
RPLP2,0.006896161718876527,10
IFITM3,0.00681940059642745,11
MUC1,0.006691504998069662,12
APOL1,0.006545853798766303,13
ANPEP,0.006403614503042358,14
USF2,0.006113847581085485,15
PDIA4,0.006083365154515097,16
EEF1G,0.005677279658859927,17
JUNB,0.005542837455668902,18
TXNIP,0.005532784182962008,19
KRAS,0.00534705588831104,20
```
LAST 20 DATA ROWS:
```csv
ATP1A1,0.00032249924140507043,481
MFGE8,0.00031698360698365237,482
DMKN,0.00031261779731751155,483
MIF,0.0003026973322878338,484
BSG,0.0002956864149959739,485
RPS17,0.0002800679350541007,486
IFIT1,0.00027480549859565146,487
EIF3K,0.0002704472550433836,488
COX4I1,0.00026538534583566293,489
TMSB10,0.0002514103820205108,490
RPS2,0.00023736156403741414,491
PTMS,0.0002352396468453636,492
RPL12,0.00020891856459153354,493
LY6E,0.00019168761498257396,494
DLK1,0.00016100521791574167,495
EIF3H,0.00015734430732170513,496
THSD4,0.00011096510299665914,497
RPL41,9.702321014894935e-20,498
ZFP36,0.0,499
RPL27,0.0,500
```

### ./phase2/outputs/shap_importances_Random_Forest_12m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,rank
```
FIRST 20 DATA ROWS:
```csv
CMTM6,0.012260195094085956,1
SPINT2,0.010397873885392843,2
TMSL3,0.009208776724112772,3
SAT1,0.007208247883507199,4
CTSB,0.007057632659196924,5
ANXA1,0.006961517748542709,6
HMGA1,0.006838368437133599,7
HBA2,0.006340445796018227,8
CHCHD2,0.005972569384365827,9
TMEM59,0.005958762614458236,10
APLP2,0.00588545652114014,11
MEST,0.005552044350366983,12
CD59,0.005170267091778166,13
HSPA8,0.004472727329066071,14
COL1A1,0.004362774477416889,15
COL1A2,0.004298776136280919,16
CAPNS1,0.004231863677196921,17
ATP1A1,0.0041220374258514715,18
TNFSF10,0.004094047780798495,19
CD47,0.003994590728647504,20
```
LAST 20 DATA ROWS:
```csv
NPM1,0.0,481
TRAM1,0.0,482
RPS27A,0.0,483
SST,0.0,484
FOLR1,0.0,485
RPL6,0.0,486
GNB2L1,0.0,487
RPS3A,0.0,488
GPX3,0.0,489
RPS16,0.0,490
RPS14,0.0,491
RPL30,0.0,492
RPL37A,0.0,493
MSLN,0.0,494
RPS7,0.0,495
FSTL1,0.0,496
RPL26,0.0,497
SLPI,0.0,498
DHCR24,0.0,499
EIF4G1,0.0,500
```

### ./phase2/outputs/shap_importances_Random_Forest_18m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,rank
```
FIRST 20 DATA ROWS:
```csv
LTBP4,0.01035137763082799,1
MT1G,0.010316380781329007,2
RPN1,0.00909615895435402,3
HDLBP,0.007413575042522428,4
ATP5G2,0.0062539955258896825,5
CTSB,0.006126257048856688,6
GPX1,0.005856334322178176,7
SLC38A2,0.005782627734735807,8
FCGBP,0.004947369755099208,9
SCNN1A,0.004847364742803007,10
FAU,0.004732970516195154,11
VIM,0.004537016704806337,12
NDUFS5,0.004147759498582311,13
H19,0.004029530413686922,14
HSP90AA1,0.004029406905338983,15
TM4SF1,0.003957823945305472,16
RPL14,0.003932100268363479,17
MEST,0.003928386156551022,18
ALPPL2,0.003835267534061166,19
NDUFB11,0.003743051754262073,20
```
LAST 20 DATA ROWS:
```csv
CHI3L1,0.00010838515558558631,481
FSTL1,0.00010624768450373854,482
SLC34A2,0.00010601020423643093,483
SNRNP200,0.00010313107289170768,484
RPL23,8.872826831882576e-05,485
EEF1A1,8.485825392910288e-05,486
IGFBP2,7.912358178349236e-05,487
FOLR1,7.235786160681547e-05,488
CLU,6.290158031254455e-05,489
PLD3,5.3428359706668115e-05,490
PDIA6,3.8462203323715014e-05,491
BCAT1,2.6031938994735914e-05,492
TIMP2,1.7579854241685705e-05,493
EEF1B2,0.0,494
CLIC1,0.0,495
RPL23A,0.0,496
RPS25,0.0,497
RPS7,0.0,498
ANXA2,0.0,499
COL6A2,0.0,500
```

### ./phase2/outputs/shap_importances_Random_Forest_24m.csv

Total data rows: 500 (header + 500 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,importance,rank
```
FIRST 20 DATA ROWS:
```csv
FBL,0.008159230410601398,1
HDLBP,0.006562985656795943,2
TFRC,0.00627253434942502,3
PGK1,0.0051071215477224525,4
SUPT5H,0.005049816308876583,5
CD63,0.004945188965163865,6
MT1G,0.0049438983474907605,7
CTSB,0.004718221686728946,8
MEST,0.004530496346694092,9
CD59,0.004444941130531487,10
UBC,0.004270343677823451,11
TPM4,0.004152358010769885,12
SAT1,0.004062305523265913,13
MDK,0.0040209484102439385,14
LYPD1,0.003978724741188861,15
A2M,0.003969433157401217,16
TMEM59,0.0038931151789964548,17
ARF1,0.0038492973772468165,18
SERPINE1,0.0037148732928640967,19
ZFP36,0.0037074517693557484,20
```
LAST 20 DATA ROWS:
```csv
CTRC,0.00017033451813555607,481
XBP1,0.00016473070362735807,482
AHCY,0.0001629619023183218,483
RPL36,0.00016199832120914105,484
KLK5,0.00015357108088376076,485
ADAM6,0.0001396066924021305,486
NME2,0.00013645853088841342,487
RPL27,0.00013595023476520426,488
CLDN1,0.00013308700057215224,489
EEF1G,0.00011934918475502347,490
RPL24,0.00011359511510010126,491
DPYSL3,0.00011071210226225789,492
MMP11,0.00010722454448022175,493
EGR1,0.00010003227447629337,494
ATN1,9.254799884286343e-05,495
PFDN5,8.350857529073406e-05,496
RPL35A,5.087647182874145e-05,497
TUBB,0.0,498
TIMP2,0.0,499
HLA-C,0.0,500
```

### ./phase2/outputs/shap_importances_full.csv

Total data rows: 536 (header + 536 data rows). Showing first 20 and last 20 data rows.

HEADER:
```csv
gene,mean_importance,std_importance,n_thresholds_present,rank
```
FIRST 20 DATA ROWS:
```csv
CTSB,0.00596737046492752,0.0011777710450000048,3,1
HDLBP,0.005688862929075575,0.0022904873879866982,3,2
MT1G,0.005294432700768059,0.004856178696677638,3,3
LTBP4,0.004886248104517081,0.004896291470891466,3,4
SAT1,0.004871057438073261,0.0020558043656724984,3,5
MEST,0.004670308951204033,0.0008208088424665737,3,6
CMTM6,0.004457442967609329,0.006757970213244686,3,7
FBL,0.0044572124974227275,0.0052354439409654195,2,8
CD59,0.004384954917697976,0.0008169586646237274,3,9
SPINT2,0.004310299093762518,0.005284797352704694,3,10
TMSL3,0.0040150460109493235,0.004505525803155626,3,11
TMEM59,0.003988215662879415,0.001924759575064407,3,12
SUPT5H,0.00383739768038952,0.001714618867680191,2,13
TFRC,0.0036739100340029136,0.0036750097503824423,2,14
ANXA1,0.0035899411903152125,0.0030830870524759845,3,15
CHCHD2,0.0035405735406318453,0.0021186243504664397,3,16
HBA2,0.003412313875846575,0.0041410038739243225,2,17
PGK1,0.0033998542908674333,0.0017883952434788926,3,18
RPN1,0.0033511496677936484,0.004978933629467204,3,19
APLP2,0.0032135884158354736,0.0023721519057746865,3,20
```
LAST 20 DATA ROWS:
```csv
CLDN1,0.0002777402220489418,0.0002045705476534349,2,517
AHCY,0.0002757227628878796,0.00015423589459563443,3,518
ADAM6,0.0002726896156244288,0.00014300668745862105,3,519
NEAT1,0.00026543605692746336,0.00015323821360765003,3,520
ITGA3,0.0002579529708766852,,1,521
S100A4,0.0002462151756032187,0.00011412703747922475,3,522
RPS25,0.00023633621873542297,0.000280356711957255,3,523
RPS27A,0.0002123743751226688,0.00018419409280104302,3,524
LMNA,0.00021126378135418673,0.00018301647581110412,3,525
FOLR1,0.0002084343833967001,0.00030054074246004935,3,526
TGFBI,0.00019525894860591652,4.117366655661247e-06,2,527
GNB2L1,0.00018846229767269154,0.00016576700914106276,3,528
CAND1,0.00018346622105481225,,1,529
CTRC,0.00017033451813555607,,1,530
TOMM20,0.00015987027101644957,,1,531
RPS7,8.69167944602885e-05,0.0001505443040362408,3,532
PFDN5,8.350857529073406e-05,,1,533
FSTL1,5.312384225186927e-05,7.512845819796238e-05,2,534
TIMP2,5.859951413895235e-06,1.0149733578751627e-05,3,535
ATHL1,0.0,,1,536
```

### ./phase2/outputs/shap_theme_comparison.csv

```csv
theme,database,term,condition,size,adj_p_value,n_overlap,significant,term_returned
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,original-MDI,50,0.0001788464665724,6.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,original-MDI,100,2.481311505265821e-06,10.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,original-MDI,200,1.6216863504303406e-17,24.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,original-MDI,500,,,False,False
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-with12m,50,1.7493211283471415e-05,7.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-with12m,100,1.3978479259048237e-08,12.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-with12m,200,6.976512274899251e-12,19.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-with12m,500,1.003814101434201e-31,48.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-without12m,50,9.058984414654839e-06,7.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-without12m,100,9.178432444874326e-06,9.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-without12m,200,4.190812469803922e-10,17.0,True,True
Theme 2 - ECM/EMT,MSigDB_Hallmark_2020,Epithelial Mesenchymal Transition,SHAP-without12m,500,1.758311061301762e-29,46.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,original-MDI,50,0.3561486104740112,1.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,original-MDI,100,0.1574090900314895,3.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,original-MDI,200,1.433655628936107e-06,10.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,original-MDI,500,,,False,False
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-with12m,50,0.03009820343146429,3.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-with12m,100,0.003012255826229276,5.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-with12m,200,0.0029733725480222952,6.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-with12m,500,2.3161858740249344e-09,17.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-without12m,50,0.32418655568788207,1.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-without12m,100,0.1776444166478673,2.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-without12m,200,0.05197537703328508,4.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,ECM-receptor interaction,SHAP-without12m,500,8.726691778654751e-07,14.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,original-MDI,50,0.4481225891866183,1.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,original-MDI,100,0.1901648808226077,4.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,original-MDI,200,5.261865862696479e-05,12.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,original-MDI,500,,,False,False
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-with12m,50,0.03009820343146429,4.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-with12m,100,0.0007219826177358848,8.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-with12m,200,5.480503367006328e-06,13.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-with12m,500,2.2530601543835693e-09,25.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-without12m,50,0.22821184989347149,2.0,False,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-without12m,100,0.03451922734670759,5.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-without12m,200,0.0034136230455477446,9.0,True,True
Theme 2 - ECM/EMT,KEGG_2021_Human,Focal adhesion,SHAP-without12m,500,2.3537966083572042e-07,22.0,True,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,original-MDI,50,0.223998439564986,3.0,False,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,original-MDI,100,1.0574037155715614e-11,14.0,True,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,original-MDI,200,1.0417746939506187e-24,28.0,True,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,original-MDI,500,,,False,False
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-with12m,50,0.37109046336035323,1.0,False,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-with12m,100,0.3048735519420804,2.0,False,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-with12m,200,5.748788748704645e-10,16.0,True,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-with12m,500,1.9528194527256266e-51,59.0,True,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-without12m,50,0.381846708675146,1.0,False,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-without12m,100,0.01978340784461419,5.0,True,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-without12m,200,1.7038502789853788e-15,21.0,True,True
Theme 1 - Ribosome/Translation,KEGG_2021_Human,Ribosome,SHAP-without12m,500,5.045648337815003e-50,58.0,True,True
```

### ./phase2/outputs/shap_theme_robustness_verdict.csv

```csv
theme,condition,n_sizes_significant,n_sizes_tested,robust_across_all_sizes
Theme 2 - ECM/EMT,SHAP-with12m,4,4,True
Theme 2 - ECM/EMT,SHAP-without12m,4,4,True
Theme 1 - Ribosome/Translation,SHAP-with12m,2,4,False
Theme 1 - Ribosome/Translation,SHAP-without12m,3,4,False
```


