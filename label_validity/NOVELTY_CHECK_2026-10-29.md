# Novelty check — Q2 paper (2026-10-29)

Scope: targeted web searches (6 queries, standard + extended) and full-text reads of the closest hits. Not a systematic PubMed review; repeat with PubMed + forward citations of TCGA 2011 (doi:10.1038/nature10166) and Liu et al. 2018 (TCGA-CDR) before submission to a journal.

## Closest prior work (must be cited and positioned)

| Work | What it does | What it does not do |
|---|---|---|
| **Cocchi S, Talijanovic M, Høgdall EV, Lopacinska-Jørgensen J. Assessing the Impact of Patient Selection and Analytical Methods on mRNA Biomarker Identification in Ovarian Cancer Using TCGA Data. *Cancer Control* 2026;33:10732748261468094. doi:10.1177/10732748261468094** | Compares TCGA-OV platinum-sensitivity cohorts built by different patient-selection strategies and PFI categories (6 vs 12 months; refractory / resistant / partially sensitive / sensitive), cross-tabulated against the original TCGA platinum status; conclusion (verbatim): "The observed variability in identified DEGs is strongly driven by differences in analytical pipelines and cohort definitions." | All labels PFI-based — no OS-threshold labels, no first-course response field; no agreement statistic (counts only); no known-groups validity (BRCA, residual disease); no classifier training or transfer (external comparison is of published DEG lists). |
| Wang Q et al. Predictive Value of Machine Learning for Platinum Chemotherapy Responses in Ovarian Cancer: Systematic Review and Meta-Analysis. *J Med Internet Res* 2024;26:e48527. doi:10.2196/48527 | 19 studies / 39 models; pooled C-index 0.806 (training), 0.831 (validation); PROBAST: "4 models had a low risk of bias in outcomes". | Does not tabulate or compare outcome definitions across studies; attributes heterogeneity to methods and variables. |
| Yousefi S, Shaban A, Amgad M, Chandradevan R, Cooper LAD. Learning Clinical Outcomes from Heterogeneous Genomic Data Sources. arXiv:1904.01637 (2019) | States that in TCGA "OS is a noisy signal due to deaths from non-cancer causes" and prefers PFI. | No OV, no platinum response, no agreement measure between labels. |
| Bayer I, Groth P, Schneckener S. Prediction errors in learning drug response from gene expression data – influence of labeling, sample size, and machine learning algorithm. *PLoS ONE* 2013;8:e70294. doi:10.1371/journal.pone.0070294 | Shows label choice affects drug-response prediction. | Cell lines (IC50), not patient clinical labels. |
| Liu J et al. 2018, Cell 173:400 (TCGA-CDR) | Endpoint-quality recommendations across TCGA (PFI preferred to OS). | No comparison with treatment-response labels used in ML. |
| Clinical literature on the 6-month definition (Markman et al. 1998, J Cancer Res Clin Oncol 124:326; systematic review of phase III PROC trials, 2024–25) | Questions the clinical validity of the < 6-month platinum-free-interval definition. | Not about genomic ML labels. |

## What the Q2 paper adds beyond these (supported claims)

1. Agreement between the three label families used in TCGA-OV response-prediction studies — OS thresholds, published platinum status / PFI from platinum, first-course response — quantified in the same patients (κ, sensitivity/specificity).
2. Known-groups validity of each label (somatic BRCA, aneuploidy, residual disease, age, stage).
3. Classifier behaviour by training label: within-TCGA cross-label CV and transfer to GSE63885.
4. A literature table pinning down which label each study actually used (e.g., Li 2022's TCGA counts equal TCGA 2011 platinum status).
5. Published gene lists evaluated as fixed inputs against random same-size sets (supplementary).

## Wording allowed

- Allowed: "To our knowledge, no study has quantified agreement between the overall-survival-threshold, platinum-status and first-course-response labels used in TCGA-OV response-prediction studies, or tested their known-groups validity." Follow immediately with Cocchi et al. 2026 as the closest work (PFI-based cohort definitions drive DEG variability).
- Not allowed: "first systematic audit", "first study of label validity in TCGA-OV" — Cocchi 2026 examined label/cohort definitions in the same resource; the search was not systematic.
- Framing: an empirical construct-validity audit of one resource; extends Cocchi et al. from PFI cohort definitions and DEG lists to the full set of label constructs and to classifier behaviour.
