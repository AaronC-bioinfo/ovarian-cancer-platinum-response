---
title: "S2 Text. Reporting checklists: STROBE (observational cohort) and STARD 2015 (OS thresholds as tests for platinum resistance)"
---

This study is a secondary analysis of publicly available TCGA data. STROBE is used for the study as a whole. STARD 2015 is applied to the one component that is a diagnostic-accuracy analysis: overall-survival (OS) thresholds (index test) evaluated against TCGA platinum status (reference standard). "Methods: X" refers to the subsection of the manuscript with that heading. Items that are not reported, or reported only in part, are marked as such.

# STROBE checklist

| Item | Recommendation (abbreviated) | Where reported |
|---|---|---|
| 1a | Indicate the study's design in the title or abstract | Abstract (analysis of 489 platinum-treated TCGA-OV patients); Methods: Data and cohort ("secondary analysis of publicly available data"). The title does not name the design. |
| 1b | Informative, balanced summary in the abstract | Abstract |
| 2 | Scientific background and rationale | Introduction, paragraphs 1–3 |
| 3 | Objectives, including pre-specified hypotheses | Introduction, final paragraph; pre-specified predictions in S1 Text |
| 4 | Key elements of study design | Methods: Data and cohort; Methods: Pre-specification |
| 5 | Setting, locations, periods of recruitment, follow-up, data collection | Methods: Data and cohort; TCGA 2011 [1] for recruitment and follow-up |
| 6a | Eligibility criteria, sources and methods of selection, follow-up | Methods: Data and cohort (platinum agent recorded in the treatment timeline); S4 Table (cohort flow) |
| 7 | Define outcomes, exposures, predictors, confounders, effect modifiers | Methods: Labels; Methods: Associations with characteristics linked to platinum response and prognosis; Table 2 |
| 8 | Data sources and measurement for each variable | Methods: Data and cohort; Methods: Labels; Methods: Associations with characteristics linked to platinum response and prognosis |
| 9 | Efforts to address potential sources of bias | Methods: Coverage and agreement (bounds for missing reference standard); Results (redaction and residual-coding sensitivity analyses); Limitations |
| 10 | How the study size was arrived at | Fixed by the public cohort; Methods: Data and cohort. No sample-size calculation; minimum detectable differences are reported (S3 Table). |
| 11 | Handling of quantitative variables | Methods: Associations with characteristics linked to platinum response and prognosis (rank-based tests; age per 10 years and Aneuploidy Score per SD in the exploratory Cox models) |
| 12a | All statistical methods, including those for confounding | Methods: Coverage and agreement; Associations with characteristics; Classifiers; Exploratory analyses. These association analyses are univariable, with no adjustment for confounding (the aim is label comparison); the exploratory clinical-only model is a multivariable logistic regression. |
| 12b | Methods for subgroups and interactions | Same-patient comparisons (Methods: Associations with characteristics linked to platinum response and prognosis); no interaction analyses |
| 12c | How missing data were addressed | Labels: undetermined patients excluded from each label; Methods: Coverage and agreement (bounds); Results: patients without a platinum status |
| 12d | Loss to follow-up | OS thresholds exclude patients censored before the threshold (Methods: Labels); inverse-probability-of-censoring-weighted sensitivity analysis (Methods: Coverage and agreement; S1 Text, A19); Limitations |
| 12e | Sensitivity analyses | Threshold sweep (6–60 months); combined reference label; exclusion of redacted TCGA-CDR records; any-vs-no residual coding; alternative carrier definitions (S3 Table); treatment-anchor alternatives (A18); IPCW (A19); decomposition restricted to patients at risk (A13b) |
| 13a | Numbers at each stage | Methods: Data and cohort; Results (coverage); Table 2; S4 Table |
| 13b | Reasons for non-participation | Methods: Data and cohort (no treatment record; no carboplatin/cisplatin) |
| 13c | Flow diagram | Not provided as a figure; flow given in text and S4 Table |
| 14a | Characteristics of participants | S4 Table (A14: age, stage, residual disease, Aneuploidy Score, sequencing and *BRCA1/2* status, for the cohort and the RNA-seq subset) |
| 14b | Number with missing data for each variable | S4 Table (denominators); Table 2 |
| 14c | Summarise follow-up time | Not reported separately; OS medians by group in Results and S4 Table |
| 15 | Numbers of outcome events | Table 2 (non-responders per label) |
| 16a | Unadjusted estimates with precision | Results; Tables 2–3; Figs 1–4 |
| 16b | Category boundaries for continuous variables | Methods: Labels (183 days; 18 and 24 months; 6–60 months) |
| 16c | Absolute risk | Not applicable |
| 17 | Other analyses | Results: exploratory section; Supporting information (S1–S2 Fig, S6–S11 Tables) |
| 18 | Key results | Discussion, paragraph 1 |
| 19 | Limitations | Limitations |
| 20 | Cautious interpretation | Discussion; Conclusion |
| 21 | Generalisability | Limitations (single resource) |
| 22 | Funding | Funding (submission form) |

# STARD 2015 checklist (OS thresholds vs platinum status)

| Item | Recommendation (abbreviated) | Where reported |
|---|---|---|
| 1 | Identify as a study of diagnostic accuracy in title or abstract | Abstract (sensitivity and positive predictive value of OS thresholds); not in title, because this is a secondary aim |
| 2 | Structured summary | Abstract (unstructured, as required by the journal) |
| 3 | Scientific and clinical background, including intended use | Introduction, paragraph 2 (OS thresholds as surrogate labels for platinum response) |
| 4 | Study objectives and hypotheses | Introduction, final paragraph; S1 Text (A2, A9 predictions) |
| 5 | Prospective or retrospective | Retrospective secondary analysis (Methods: Data and cohort) |
| 6 | Eligibility criteria | Methods: Data and cohort |
| 7 | Basis for identifying potentially eligible participants | Treatment timeline (carboplatin or cisplatin recorded) |
| 8 | Where and when participants were identified | TCGA 2011 [1] |
| 9 | Consecutive, random or convenience series | TCGA cohort as released; not applicable |
| 10a | Index test, in sufficient detail to allow replication | Methods: Labels (OS thresholds) |
| 10b | Reference standard, in sufficient detail | Methods: Labels (platinum status, verbatim TCGA definition) |
| 11 | Rationale for choosing the reference standard | Introduction, paragraph 2; Methods: Labels |
| 12a | Definition and rationale for index-test positivity cut-offs | Methods: Labels (18 and 24 months, our earlier analyses); all thresholds 6–60 months examined |
| 12b | Definition of reference-standard cut-off | Methods: Labels (six months) |
| 13a | Whether index-test results were available to assessors of the reference standard | Not applicable: both derived from registry records; no blinding possible |
| 13b | Whether clinical information was available to assessors | Not applicable |
| 14 | Methods for estimating diagnostic accuracy | Methods: Coverage and agreement (sensitivity, specificity, PPV and NPV with Wilson intervals; κ and κmax); NPV values in S2 Table |
| 15 | Handling of indeterminate results | Methods: Labels (undetermined excluded); Methods: Coverage and agreement (bounds) |
| 16 | Handling of missing data | Methods: Coverage and agreement (bounds); S4 Table |
| 17 | Analyses of variability, pre-specified or exploratory | Threshold sweep, reference bounds and combined reference (exploratory, added after review; Results; S2 and S4 Tables) |
| 18 | Intended sample size | Not applicable (public cohort) |
| 19 | Flow of participants | Not provided as a diagram; text and S4 Table |
| 20 | Baseline characteristics | S4 Table (A14) |
| 21a | Distribution of severity in those with the target condition | Not reported; refractory and resistant disease not separated (Limitations) |
| 21b | Distribution of alternative diagnoses | Not applicable |
| 22 | Time interval between index test and reference standard | Not applicable in the usual sense: reference determined from first-line follow-up; index determined at 18 or 24 months from diagnosis |
| 23 | Cross-tabulation of index test by reference standard | S2 Table (true and false positives and negatives) |
| 24 | Estimates of diagnostic accuracy and precision | Results; Fig 1C; S2 Table |
| 25 | Adverse events | Not applicable |
| 26 | Limitations | Limitations |
| 27 | Implications for practice | Discussion (recommendations) |
| 28 | Registration | Not registered; predictions for three analyses deposited publicly before they were run (Methods: Pre-specification and analysis history) |
| 29 | Where the full protocol can be accessed | S1 Text; code repository |
| 30 | Sources of funding | Funding (submission form) |
