#!/usr/bin/env python3
"""
manuscript_v5/apply_review5_round7_2026-10-30.py
Round 7 (2026-10-30, ~01:15 ET): response to the fifth review (of revision 6). Exact replacements; each must match once.
Sources: A23 23_followup_checks_summary.md (IPCW variants ≤ 0.011, max weight 1.24, Cox exclusions 23; carboplatin/
cisplatin-only anchor: 0 changed, 2 undetermined, 1 of them among the 78 unflagged added; A1–A3: 0 changes among the 78;
2 unflagged added resistant calls with unrecorded event type); A22 summary and replicates (500/500 valid, 0 skipped,
out-of-bag n mean 49, min 1 OS24 positive; medians +0.010, +0.063, −0.004); config/config.yaml (SVC probability: true);
Lisowska 2014 (Frontiers full text: 97 tumours; 72 serous/undifferentiated with clinical data, 62 CR/PR and 10 SD/P;
Table 1: 33 resistant); validation/GSE63885_label_definitions.md (101 samples; 74 annotated serous/undifferentiated:
64/10 clinical, 34/40 DFS; Chen 34/41 consistent with one endometrioid sample); Wang C 2024 PDF (ROC plotter: relapse
status at six months); labels_full / clinical file (1 patient without OS time).
Run from manuscript_v5/: python apply_review5_round7_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
# 1: separate the CV estimate from the out-of-bag range
("(difference in AUC −0.005; 95% range of out-of-bag differences when the whole pipeline was refitted in bootstrap samples, −0.18 to +0.16).",
 "(difference in AUC −0.005, conditional 95% interval −0.105 to +0.087; out-of-bag refits of the whole pipeline ranged from −0.18 to +0.16)."),
("To capture the uncertainty of the whole procedure, the pipeline (gene filter, scaling and the three models for each training label) was also refitted in 500 bootstrap samples of the 134 patients, drawn within platinum-status groups, and evaluated on the patients not drawn; the 2.5th and 97.5th percentiles of these out-of-bag differences give the full-pipeline interval, which by a rule fixed before the run is the main uncertainty reported (analysis A22; run with scikit-learn 1.7.2, in which random-forest fits differ slightly from those in the A16 environment).",
 "As a sensitivity analysis of the whole procedure, the pipeline (gene filter, scaling and the three models for each training label) was also refitted in 500 bootstrap samples of the 134 patients, drawn within platinum-status groups with duplicates kept, and every model and label was evaluated on the same patients not drawn (analysis A22; scikit-learn 1.7.2, in which random-forest fits differ slightly from those in the A16 environment). All 500 samples gave a valid AUC for every contrast, and none had a single-class training label or out-of-bag target. SVM probabilities came from scikit-learn's internal five-fold Platt scaling. Because single fits on about 63% of the distinct patients, evaluated on the remainder, estimate a different quantity from the repeated cross-validation, the out-of-bag results are reported separately, with their own median and percentile range; the analysis's pre-specified rule, which made this range the main uncertainty, was therefore not followed (S1 Text)."),
("(difference in AUC −0.005; full-pipeline 95% interval −0.18 to +0.16, conditional interval −0.105 to +0.087).",
 "(difference in AUC −0.005; conditional 95% interval −0.105 to +0.087)."),
("was +0.080 (full-pipeline interval −0.15 to +0.24; conditional −0.045 to +0.201);", "was +0.080 (−0.045 to +0.201);"),
("(difference −0.069; full-pipeline −0.23 to +0.22; conditional −0.236 to +0.081).", "(difference −0.069, −0.236 to +0.081)."),
("The full-pipeline intervals are percentiles of out-of-bag differences, each from a single fit on about 63% of the distinct patients and evaluated on the remaining patients (on average 49, with as few as one positive for the 24-month OS label); they are centred on the out-of-bag differences (medians +0.01, +0.06 and −0.004) rather than on the estimates above, include test-set noise and are probably conservative (Fig 3B). No clear difference between training labels was demonstrated, and differences of up to about 0.16 AUC in favour of the platinum label or 0.18 in favour of the OS label remain compatible with the data (S1 Text).",
 "In the out-of-bag sensitivity analysis, the median differences were +0.01 (2.5th–97.5th percentiles −0.18 to +0.16), +0.06 (−0.15 to +0.24) and −0.004 (−0.23 to +0.22) for the three contrasts (Fig 3B); each replicate is a single fit evaluated on 49 patients on average (with as few as one positive for the 24-month OS label), so this range describes the variability of single refits, not a confidence interval for the estimates above. No clear difference between training labels was demonstrated (S1 Text)."),
("in those 134 patients (39 resistant), differences of up to about 0.16 AUC in favour of the platinum label, or 0.18 in favour of the OS label, could not be excluded when the whole pipeline was refitted.",
 "in those 134 patients (39 resistant), the conditional interval spans −0.105 to +0.087 and single refits of the whole pipeline varied more widely, so moderate differences in either direction cannot be excluded."),
("cannot exclude one of up to about 0.16 AUC in favour of the platinum label or 0.18 in favour of the OS label, and its out-of-bag estimates come from fits on about 63% of the distinct patients.",
 "cannot exclude a moderate one in either direction; its interval is conditional on the fitted models, and the out-of-bag refits, which vary more, estimate a different quantity."),
("Dots, estimates with the same folds for every label; light bars, 95% range of out-of-bag differences from refitting the whole pipeline in 500 bootstrap samples (centred on those differences, not on the dots); dark lines, 95% intervals from resampling patients without refitting the models.",
 "Dots and dark lines, cross-validated estimates (same folds for every label) with conditional 95% intervals from resampling patients without refitting the models; light bars, 2.5th–97.5th percentiles of out-of-bag differences from 500 bootstrap refits of the whole pipeline (a sensitivity analysis of a different quantity, not centred on the dots)."),
("all are disclosed in S1 Text)", "all are disclosed in S1 Text; the decision rule of A22 was not followed, for the reason given under Classifiers)"),
("(A13b, A18, A19, A21, and A22 with one prediction)", "(A13b, A18, A19, A21, A23, and A22 with one prediction)"),
# 2–3: IPCW population; OS accounting
("[@vock] (S1 Text, analysis A19).",
 "[@vock] (S1 Text, analysis A19). The censoring distribution was also estimated only in patients with a platinum status, and separately within each status group (analysis A23); the largest weight was 1.24, and no weights were truncated."),
("(8 and 17 of those with a platinum status; 69 and 87 in the cohort).",
 "(8 and 17 of those with a platinum status; 69 and 87 in the cohort, in which 1 further patient has no recorded survival time)."),
("The Kaplan–Meier weights assume censoring unrelated to outcome, and the Cox weights unrelated given age, stage and residual disease; the censoring distribution was estimated in the whole cohort rather than in patients with a status, and weighting does not address missing platinum status.",
 "The Kaplan–Meier weights assume censoring unrelated to outcome, and the Cox weights (which excluded 23 patients with missing covariates) unrelated given age, stage and residual disease; estimating the censoring distribution only in patients with a status, or within each status group, changed the estimates by at most 0.01. Weighting does not address missing platinum status."),
# 5–7: anchor drugs, anchors in the additions, unknown event types
("no platinum row carried a neoadjuvant indication.",
 "no platinum row carried a neoadjuvant indication. Restricting the anchor to carboplatin and cisplatin changed no call and left 2 patients undetermined, 1 of them among the unflagged added patients (analysis A23)."),
("(κ with the primary label about 0.97; S1 Text, analysis A18).",
 "(κ with the primary label about 0.97; S1 Text, analysis A18); none of the 78 unflagged added patients changed under any of them."),
("the remaining two are not explained by the available records (S11 Table).",
 "the remaining two are not explained by the available records (S11 Table). Two of the 12 unflagged resistant additions rest on a new tumour event of unrecorded type; \"unflagged\" means that no specified flag applied, not that the call was verified."),
# 8–9: external cohort
("genes z-scored within the cohort) was restricted to serous and undifferentiated tumours (80 samples).",
 "genes z-scored within GSE63885, using that cohort's own expression distribution, so this is a batch-level transfer assessment rather than a frozen pipeline applied to single new patients) was restricted to serous and undifferentiated tumours (80 samples)."),
("differences in transfer performance cannot be attributed to the training label alone.",
 "differences in transfer performance cannot be attributed to the training label alone. The original publication analysed 97 tumours, 72 of them serous or undifferentiated with clinical data (62 responders, 10 non-responders; 33 platinum-resistant) [@lisowska]; the deposited series has 101 samples, and our 74 annotated serous or undifferentiated samples include 2 more responders and 1 more resistant tumour, which cannot be identified because the publication lists no sample identifiers. Chen et al. reported 75 samples (34 resistant, 41 sensitive), consistent with including one endometrioid tumour excluded here."),
("Confine every data-dependent step, including gene selection, to training data.",
 "Confine every supervised data-dependent step, including gene selection, to training data, and report any normalisation done within an external cohort."),
# 10: Table 1 as an illustrative sample; Table 1 cells
("The proportion of TCGA patients labelled resistant ranged from 19% to 44% (S1 Table).",
 "In this illustrative sample, the proportion of TCGA patients labelled resistant ranged from 19% to 44% (S1 Table)."),
("| Definition not stated (counts equal to TCGA 2011 platinum status) |",
 "| TCGA label definition not stated (counts equal to TCGA 2011 platinum status); relapse within six months stated for the external ROC-plotter analysis |"),
("| No TCGA; GEO labels, definition not stated |", "| No TCGA response-classifier cohort; GEO labels, definition not stated |"),
# 11: Cox wording
("those two hazard ratios are averages over follow-up), and an added quadratic term did not improve the fit for either continuous covariate",
 "those two constant hazard ratios should be read with caution because proportional hazards was not supported), and an added quadratic term did not detect non-linearity for either continuous covariate"),
# references 5: GCIG context
("that clinical consensus has replaced with a continuous therapy-free interval [@wilson17]",
 "that clinical consensus has replaced, for trial design, with a continuous therapy-free interval [@wilson17]"),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
