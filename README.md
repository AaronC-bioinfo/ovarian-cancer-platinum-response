# Outcome labels for platinum-response prediction in TCGA-OV

This repository contains the code, analysis outputs and patient-level label table for a study of the coverage, agreement and provenance of candidate platinum-response labels in The Cancer Genome Atlas ovarian cancer cohort (TCGA-OV). In 489 platinum-treated patients it compares:

- TCGA's published platinum status (2011 release);
- a platinum-free interval re-derived from the TCGA Clinical Data Resource (TCGA-CDR);
- the first-course response field;
- overall-survival (OS) thresholds at 18 and 24 months.

For each label, the study measures:

- coverage and agreement between labels;
- the OS thresholds evaluated as tests for platinum resistance;
- associations with characteristics linked to platinum response (*BRCA1/2*, *CCNE1*) and to prognosis;
- what cross-validated expression classifiers trained on each label predict.

A manuscript describing the study is in preparation; a preprint link will be added here.

> **Note on earlier versions.** The repository began as an expression classifier that defined platinum response as survival beyond 12, 18 or 24 months (release v1.0.0, Zenodo [10.5281/zenodo.20802754](https://doi.org/10.5281/zenodo.20802754)). The present study shows that those OS-threshold labels agree at best moderately with platinum status, so that interpretation is superseded. The earlier pipeline (`src/`, `run.py`, `run_ablation_study.py`) is kept because the current analyses reuse it. Its original description is in `docs/README_v1_classifier.md`.

## Main results (see the manuscript for details and caveats)

- **Platinum labels:** TCGA's platinum status is determinate for 277 of 489 platinum-treated patients. The re-derived platinum-free interval agrees with it in 268 of 272 shared patients (κ 0.97). Combined, the two label 394 patients (broad combined label). The provenance-filtered combined label (column `label_combined_strict`), which adds re-derived calls only where the record is unflagged, labels 355 (99 resistant). It is a candidate extension of platinum status, preferred over the broad label under the pre-specified A15 rule but not shown to be more accurate; document provenance and report results with and without the added patients.
- **OS thresholds (candidate survival surrogates, not platinum-response labels) as tests for platinum resistance:**
  - At 18 and 24 months they flag 21% and 39% of resistant patients.
  - Of the flagged patients who have a known status, 82% and 74% are resistant.
  - Across thresholds from 6 to 60 months, agreement with platinum status is at best moderate (highest κ 0.47).
- **Expression classifiers** trained on four of the labels predict them only modestly (cross-validated AUC about 0.6–0.7).
- **Same-patient comparison of training labels (A16):** in 134 patients with the same folds, platinum-trained and 24-month-OS-trained models did not differ detectably in predicting platinum status (difference in AUC −0.005; 95% interval from 500 bootstrap refits of the whole pipeline −0.18 to +0.16; conditional interval without refitting −0.105 to +0.087).

## Patient-level label resource

`label_validity/outputs/labels_full.csv` has one row per platinum-treated patient (TCGA barcode).

| Column | Meaning (1 = non-responder / resistant, 0 = responder / sensitive, blank = undetermined) |
|---|---|
| `in_rnaseq` | Patient has PanCancer Atlas RNA-seq data |
| `src_platinum_status_raw` | TCGA 2011 `PLATINUM_STATUS` as released (Resistant, Sensitive, Tooearly, Missing; "absent" = not in the 2011 release) |
| `label_platinum` | TCGA platinum status (Resistant = 1, Sensitive = 0) |
| `label_pfiplat6` | Re-derived interval: TCGA-CDR progression-free interval time minus the stop date of the last adjuvant platinum regimen; < 183 days with progression = 1, ≥ 183 days = 0 |
| `label_hybrid` | Broad combined label (sensitivity analysis): `label_platinum` where determinate, otherwise `label_pfiplat6` |
| `label_response` | First-course response: stable or progressive disease = 1, complete or partial response = 0 |
| `label_os18_all`, `label_os24_all` | Death before 18 / 24 months from diagnosis = 1; alive at the threshold = 0; censored earlier = blank |
| `label_os18`, `label_os24` | The same OS labels restricted to patients with RNA-seq data |

The provenance-filtered combined label (`label_combined_strict`; a candidate extension) is in the versioned patient-level table `label_validity/outputs/label_resource_v1.csv` (S11 Table; column definitions in `label_resource_v1_dictionary.csv`, class counts in `label_resource_v1_counts.csv`). It uses `label_platinum` where determinate and `label_pfiplat6` only where the re-derived call has an unflagged provenance record (355 patients, 99 resistant). Provenance of each re-derived call is in `a15b_provenance.csv`: whether the event is a recorded recurrence or progression or a death counted as progression, and flags for redacted records, ambiguous treatment courses and intervals near the 183-day cut-off. The `a15_*` files are the first A15 run, made before the near-threshold flag specified in the A15 header was added to the code (`label_validity/15b_reconstruction_provenance_specfix.py`).

## Repository layout

| Path | Contents |
|---|---|
| `label_validity/00_*.py` … `22_*.py`, `03b_pfi_cox.R` | Analyses. Each script's header states its predictions and decision rules, written before it was run unless marked post hoc, descriptive or exploratory. |
| `label_validity/outputs/` | All analysis outputs; `*_summary.md` files contain results and post-run prediction scorecards. |
| `label_validity/G5_literature_label_table.md`, `G6_literature_additions.md` | Literature extraction with verbatim quotations and page locations. |
| `label_validity/07_ablation_rerun_PRERUN.md`, `outputs/results_pinned_2026-10-29/` | Feature-selection leakage analysis rerun in the pinned environment. |
| `figures/v5/` | Figures and the script that draws them; `figure_values.md` lists every plotted value. |
| `manuscript_v5/SI/` | Supporting information (S1–S11 Tables, S1 Text with all pre-specified predictions and outcomes, S2 Text reporting checklists), built by `manuscript_v5/build_SI.py`. |
| `src/` | Shared data loading, preprocessing and model code. |

## Reproducing the analyses

1. Download the cBioPortal studies `ov_tcga_pan_can_atlas_2018` and `ov_tcga_pub`, and the TCGA-CDR supplementary table (Genomic Data Commons file `1b5f413e-a8d1-4d10-92eb-7c4ae739ed81`, `TCGA-CDR-SupplementalTableS1.xlsx`). Place them under one data root; see `data/README.md`.
2. Install the pinned environment: `pip install -r requirements.txt` (Python 3.14, scikit-learn 1.9.0). Random-forest results differ between scikit-learn versions (`label_validity/outputs/04a_rf_determinism*.txt`).
3. Run each script from the repository root, e.g. `python label_validity/08_brca_germline.py --data-root "<data root>"`. The run command for each script is given in its header.

## Pre-specification

The predictions for analyses A8–A10 were committed to this repository before those analyses were run (commits `d5bd844`, `e98b3d9`); the same applies to A15 and A16, with the commit identified in S1 Text. All predictions and outcomes, including those that failed, are reproduced in `manuscript_v5/SI/S1_Text.md`.

## License

MIT (see `LICENSE`).
