#!/usr/bin/env python3
"""
manuscript_v5/apply_external_review_2026-10-29.py
Applies the approved revision of manuscript_v5_src.md for the external reviewer's points 1-6
(2026-10-29). Each edit is an exact replacement that must match once. The pre-review text is archived in
manuscript_v5/archive_pre_external_review_2026-10-29/.
Number sources: label_validity/outputs/15_reconstruction_provenance_summary.md (A15 scorecard),
15b_reconstruction_provenance_specfix_summary.md and a15b_*.csv (A15b), 16_controlled_label_comparison_summary.md
and a16_paired_differences.csv (A16), label_resource_v1_counts.csv (strict/broad counts), Table 3 (OR 0.64).
Run from manuscript_v5/: python apply_external_review_2026-10-29.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"

E = [
# ── title (point 5: not "validity") ──────────────────────────────────────────────────────────────────────
("Coverage, agreement and validity of candidate labels in TCGA-OV",
 "Coverage, agreement and provenance of candidate labels in TCGA-OV"),

# ── abstract (points 1-6; <= 300 words) ──────────────────────────────────────────────────────────────────
("""Machine-learning studies that predict response to platinum-based chemotherapy from The Cancer Genome Atlas ovarian cancer cohort (TCGA-OV) define "response" in different ways. In 489""",
 """Machine-learning studies that predict response to platinum-based chemotherapy from The Cancer Genome Atlas ovarian cancer cohort (TCGA-OV) define "response" in different ways, often without stating the definition. In 489"""),
("""we compared five candidate labels: TCGA's published platinum status, a platinum-free interval re-derived from the TCGA Clinical Data Resource, first-course response, and death before 18 or 24 months (overall-survival, OS, thresholds). We measured coverage and agreement, evaluated OS thresholds as tests for platinum resistance, tested associations with characteristics linked to platinum response and prognosis, and trained cross-validated expression classifiers on four of the labels. Platinum status was available for 277 patients (57%); the re-derived interval agreed with it closely (κ 0.97) and, combined with it, labelled 394. At 18 and 24 months the OS thresholds flagged 21% and 39% of platinum-resistant patients, largely because few patients die that early; of flagged""",
 """we compared TCGA's published platinum status, a platinum-free interval re-derived from the TCGA Clinical Data Resource, first-course response and, as candidate survival surrogates taken from our own earlier analyses, death before 18 or 24 months (overall-survival, OS, thresholds). Platinum status was available for 277 patients (57%). The re-derived interval agreed with it closely (κ 0.97); a patient-level audit of the 117 patients it added classed 78 as clean, and a strict combined label that adds only those covered 355 patients (99 resistant). At 18 and 24 months the OS thresholds flagged 21% and 39% of platinum-resistant patients; of flagged"""),
("""(highest κ 0.47, at 36 months). *BRCA1/2* variants and *CCNE1* amplification pointed the same way under every label, although only large differences between labels were detectable. In post hoc exploratory analyses, *BRCA1/2*, *CCNE1* and aneuploidy were associated mainly with the platinum-free interval, whereas age and bulky residual disease were associated with survival after progression, and a model of age, stage and residual disease predicted the OS labels (AUC 0.62–0.64) but not platinum status (0.48). Expression classifiers predicted every label modestly (AUC 0.61–0.68). OS thresholds thus appear to combine early platinum failure with prognostic factors acting after progression. Studies should state the label definition and class sizes and prefer platinum-specific labels, which the re-derived interval can extend.""",
 """(highest κ 0.47, at 36 months). *BRCA1/2* variants and *CCNE1* amplification pointed the same way under every label, so these markers do not resolve the comparison. Expression classifiers predicted every label modestly (AUC 0.61–0.68); trained in the same 134 patients with the same folds, platinum-trained and 24-month-OS-trained models did not differ detectably in predicting platinum status (difference in AUC −0.005, 95% CI −0.105 to +0.087). We release a versioned patient-level label table with the provenance of every re-derived call. Studies should state the label definition and class sizes, prefer platinum-specific labels, and treat OS thresholds as survival end-points rather than platinum-response labels."""),

# ── introduction (points 1, 6) ───────────────────────────────────────────────────────────────────────────
("the response recorded after first-line therapy, and thresholds on overall survival (OS), the most complete outcome in the cohort.",
 "the response recorded after first-line therapy, and, as candidate surrogates, thresholds on overall survival (OS), the most complete outcome in the cohort."),
("found 12 different definitions of platinum resistance [@talijanovic].",
 "found 12 different definitions of platinum resistance [@talijanovic]. None of the TCGA-OV studies we reviewed used an OS threshold (Table 1); we evaluate the 18- and 24-month thresholds because our own earlier classifier analyses of this cohort used them, not because they are established practice."),
("evaluated OS thresholds as tests for platinum resistance, or compared what classifiers trained on each label learn.",
 "evaluated OS thresholds as tests for platinum resistance, compared what classifiers trained on each label learn, or released a patient-level label table with the provenance of each call."),
("(i) in how many patients they cover and which patients they call resistant,",
 "(i) in how many patients they cover, which patients they call resistant and, for the re-derived interval, which records support each call,"),

# ── methods: labels (points 1, 2) ────────────────────────────────────────────────────────────────────────
("A combined label used platinum status where it was determinate and this interval otherwise.",
 "A broad combined label used platinum status where it was determinate and this interval otherwise. After an external review we audited the provenance of every re-derived call (S1 Text, analysis A15). Each resistant call was traced to a recorded new tumour event (recurrence or progression) or to a death counted as progression. Each patient was flagged for a redacted TCGA-CDR record, an adjuvant platinum regimen without a stop date, a later-line regimen started before the recorded event (for sensitive patients, before day 183), or an interval within 150–215 days of the end of platinum. Patients with a recorded event, or an interval of at least 183 days, and no flag were classed clean. A strict combined label used platinum status where it was determinate and the re-derived interval only in clean patients. By a rule fixed before the audit was run, the strict label became the recommended label, and the broad label a sensitivity analysis, because more than 20% of the added patients were not clean."),
("These two thresholds are those used in our own earlier classifier analyses of this cohort;",
 "No study in Table 1 used an OS threshold. The 18- and 24-month thresholds are those used in our own earlier classifier analyses of this cohort, and we evaluate them as candidate survival surrogates for platinum resistance, not as established practice;"),

# ── methods: associations (point 5) ──────────────────────────────────────────────────────────────────────
("### Known-groups associations\n\nA platinum-response label should separate patients by characteristics known to be associated with platinum response.",
 "### Associations with characteristics linked to platinum response and prognosis\n\nWe asked whether the labels differ in their associations with characteristics known to be associated with platinum response."),

# ── methods: classifiers (point 4) ───────────────────────────────────────────────────────────────────────
("A pre-specified rule compared platinum status's own AUC with the AUC of OS-trained models for platinum status, judging a difference of 0.05 or more as evidence that the label mismatch matters.",
 "This all-patients analysis compares labels on different patient sets and class balances and is reported as descriptive; its pre-specified decision rule is reported in S1 Text. To compare training labels directly (analysis A16, added after external review), the same pipeline was trained with platinum status, OS at 18 months and OS at 24 months in the 134 patients with RNA-seq data in whom all three labels were determinate, using the same outer folds for every label (stratified five-fold cross-validation repeated 20 times). The primary quantity was the difference in AUC for platinum status between platinum-trained and 24-month-OS-trained models, averaged over the three models. Its 95% interval came from 2,000 bootstrap resamples of patients, stratified by the target label, using out-of-fold scores averaged over repeats."),

# ── methods: exploratory (point 3) ───────────────────────────────────────────────────────────────────────
("and Cox models of each were fitted for age, stage, residual disease, *BRCA1/2*, *CCNE1* and Aneuploidy Score.",
 "and univariable Cox models of each were fitted for age, stage, residual disease, *BRCA1/2*, *CCNE1* and Aneuploidy Score. The platinum-free interval was measured from the end of first-line platinum, with intervals below 1 day (including the 8 negative intervals) set to 1 day. Survival after progression was overall survival minus the TCGA-CDR progression-free interval, so patients whose progression event was their death were excluded from that model. The two models were not compared formally."),

# ── methods: pre-specification and history (points 2, 4) ─────────────────────────────────────────────────
("were deposited in the public code repository before they were run (commits d5bd844 and e98b3d9);",
 "were deposited in the public code repository before they were run (commits d5bd844 and e98b3d9), as were those of the provenance audit and the controlled classifier comparison added after external review (commit d349b2b);"),
("and the paper was revised. The descriptive full-cohort tables",
 "and the paper was revised. After an external review, the OS thresholds were reframed as candidate surrogates, the survival decomposition was reported as associations only, the provenance audit was added, and the claim that the training label changes classifier performance was withdrawn when the controlled comparison detected no difference. In the provenance audit, the code omitted one pre-specified flag (an interval within 150–215 days); this was found when the results were scored, and a correction run that adds only that flag gives the strict label reported here (355 patients, against 367 as first run; S1 Text). The descriptive full-cohort tables"),

# ── results: coverage + provenance (points 2, 6) ─────────────────────────────────────────────────────────
("and the combined label for 394 (113 resistant). The OS thresholds were determinate for 419 patients at 18 months (47 non-responders) and 401 at 24 months (78 non-responders).",
 "and the broad combined label for 394 (113 resistant). The OS thresholds were determinate for 419 patients at 18 months (47 non-responders) and 401 at 24 months (78 non-responders).\n\nOf the 389 patients with a re-derived interval, 272 also had platinum status and 117 were added by the re-derivation (26 resistant). Of the 26 added resistant calls, 20 were dated by a recorded new tumour event (13 recurrences, 3 progressions and 4 of unrecorded type) and 6 by a death counted as progression. Of the 117 added patients, 78 were classed clean (12 resistant, 66 sensitive), 38 were flagged and 1 had a negative interval (S11 Table). In all four patients in whom the two platinum labels disagreed, the re-derived interval called resistant a patient TCGA had called sensitive. One of the four had an interval near the cut-off (154 days); the other three (18, 101 and 148 days) had a recorded recurrence and no flag, so the available records do not explain the disagreement. The strict combined label was determinate for 355 patients (99 resistant, 256 sensitive; 167 with RNA-seq data) and is the label we recommend. Against it, the OS thresholds had sensitivities of 0.23 at 18 months and 0.41 at 24 months and PPVs of 0.79 and 0.75, within 0.05 of their values against the broad combined label (S1 Text)."),

# ── results: associations (point 5) ──────────────────────────────────────────────────────────────────────
("First-course response was the only label with no *BRCA1/2* association and no association with aneuploidy (r = −0.03).",
 "First-course response showed no clear evidence of association with *BRCA1/2* (OR 0.64, 0.18–1.80) or with aneuploidy (r = −0.03). These markers therefore do not resolve the comparison between labels."),

# ── results: exploratory (point 3) ───────────────────────────────────────────────────────────────────────
("### Exploratory: OS combines the platinum-free interval with survival after progression",
 "### Exploratory: associations with the platinum-free interval and with survival after progression"),
("Any residual disease was associated with both. Consistent with this, a logistic regression",
 "Any residual disease was associated with both. A clearer association in one model than in the other is not evidence that the associations differ. Separately, a logistic regression"),

# ── results: classifiers (point 4) ───────────────────────────────────────────────────────────────────────
("By the pre-specified rule, the difference between platinum status's own AUC and that of OS-trained models (+0.06) indicated that the label mismatch matters, but the difference reached 0.05 in only three of five cross-validation repeats, so it is not robust.",
 "These all-patients comparisons use different patients and class balances for each label and are descriptive. In the controlled comparison (134 patients, 39 platinum-resistant, the same folds for every label), platinum-trained and 24-month-OS-trained models did not differ detectably in predicting platinum status (difference in AUC −0.005, 95% CI −0.105 to +0.087). The corresponding difference for 18-month-OS-trained models, which had only 7 positives, was +0.080 (−0.045 to +0.201); on the 24-month OS label, 24-month-OS-trained models scored no better than platinum-trained ones (difference −0.069, −0.236 to +0.081). No difference between training labels was detected, and a platinum-label advantage larger than about 0.09 AUC is unlikely (S1 Text)."),

# ── discussion (points 2, 3, 4, 5) ───────────────────────────────────────────────────────────────────────
("The exploratory decomposition, added after review, suggests a reason. Overall survival comprises the time to the end of first-line platinum, the platinum-free interval and survival after progression. Characteristics linked to platinum response — *BRCA1/2*, *CCNE1* and aneuploidy — were associated mainly with the first part, whereas age and bulky residual disease were associated with the second, and clinical characteristics alone predicted the OS labels but not platinum status. Any residual disease was associated with both parts. If confirmed, this would mean that an OS-threshold label mixes early platinum failure with prognostic factors that act after progression, and that a classifier trained on it is asked to learn both. This also explains why markers of platinum response cannot validate the labels against one another:",
 "The exploratory decomposition, added after review, is consistent with this picture but does not establish it. Overall survival comprises the time to the end of first-line platinum, the platinum-free interval and survival after progression. *BRCA1/2*, *CCNE1* and aneuploidy were associated more clearly with the platinum-free interval, and age and bulky residual disease more clearly with survival after progression, but the two models were not compared formally, and a clearer association in one model is not evidence of a difference. Clinical characteristics alone predicted the OS labels but not platinum status. An OS-threshold label may therefore mix early platinum failure with other prognostic information; this would need confirmation in another cohort. Markers of platinum response cannot settle which label is better:"),
("First-course response behaved differently from all other labels — it agreed weakly with each of them and showed no *BRCA1/2* association —",
 "First-course response behaved differently from all other labels — it agreed weakly with each of them and showed no clear evidence of a *BRCA1/2* association —"),
("By our pre-specified rule, OS-trained models predicted platinum status less well than models trained on platinum status, although the difference was small and unstable.",
 "When the labels were trained in the same patients with the same folds, no difference was detected between platinum-trained and 24-month-OS-trained models, so this study does not show that the choice of training label changes classifier performance; with 39 resistant patients, differences smaller than about 0.09 AUC could not be excluded."),
("re-deriving the interval from TCGA-CDR recovers about half of them, and where both labels are available they agree closely.",
 "re-deriving the interval from TCGA-CDR recovers about half of them, and where both labels are available they agree closely. In the patients it adds, two-thirds of calls rest on clean records, and the strict combined label keeps only those."),
("Prefer a platinum-specific label, and extend TCGA's platinum status with the platinum-free interval re-derived from TCGA-CDR where status is missing. If an OS threshold is used, report it as a survival end-point that combines early platinum failure with other prognostic factors, and expect low sensitivity for platinum resistance at short thresholds and poor specificity at long ones.",
 "Prefer a platinum-specific label. Where TCGA's platinum status is missing, extend it with the platinum-free interval re-derived from TCGA-CDR only where the record is clean, as in the strict combined label we release (S11 Table), and report each patient's provenance. If an OS threshold is used, report it as a survival end-point rather than a platinum-response label, and expect low sensitivity for platinum resistance at short thresholds and poor specificity at long ones."),

# ── limitations (points 2, 4) ────────────────────────────────────────────────────────────────────────────
("The same-patient comparisons of labels were underpowered, and their wide intervals do not establish that the labels are equivalent.",
 "The same-patient comparisons of labels were underpowered, and their wide intervals do not establish that the labels are equivalent; the controlled classifier comparison likewise detected no difference but cannot exclude one smaller than about 0.09 AUC."),
("and their close agreement shows consistency rather than independent truth.",
 "and their close agreement shows consistency rather than independent truth. The provenance audit checks the records behind each re-derived call, not the clinical events themselves, and it does not explain the three disagreements with clean records."),
("and that the 24-month threshold would have a sensitivity of 0.30 or less; all outcomes are reported in S1 Text.",
 "and that the 24-month threshold would have a sensitivity of 0.30 or less, and, after external review, that the strict combined label would cover at least 370 patients, that at least two of the four disagreements would carry a flag or a near-threshold interval, and that platinum-trained models would predict platinum status better than 24-month-OS-trained models (and the reverse on the OS label); all outcomes are reported in S1 Text."),

# ── conclusion (points 1, 3, 4, 6) ───────────────────────────────────────────────────────────────────────
("In TCGA-OV, platinum-specific labels are consistent but cover only part of the cohort; overall-survival thresholds cover more of it but agree at best moderately with platinum status, and exploratory analyses suggest that they combine early platinum failure with prognostic factors acting after progression; expression predicts all of them modestly.",
 "In TCGA-OV, platinum-specific labels are consistent but cover only part of the cohort, and the re-derived interval extends them with records that can be checked patient by patient. Overall-survival thresholds, evaluated here as candidate surrogates, cover more of the cohort but agree at best moderately with platinum status. Expression predicts all of the labels modestly, and in the same patients the training label made no detectable difference to classifier performance."),
("is a precondition for comparing models of platinum response built on these data.",
 "is a precondition for comparing models of platinum response built on these data. The versioned patient-level label table released with this paper (S11 Table; Zenodo, [[ZENODO_DOI]]) gives each patient's labels and the provenance of each re-derived call."),

# ── data availability (point 6) ──────────────────────────────────────────────────────────────────────────
("and are archived at Zenodo ([[ZENODO_DOI]]).",
 "and are archived at Zenodo ([[ZENODO_DOI]]). The patient-level label table (version 1.0, with a data dictionary) is provided as S11 Table and in the Zenodo record."),

# ── figure legends (points 2, 3) ─────────────────────────────────────────────────────────────────────────
("The combined label uses platinum status where available and the re-derived platinum-free interval otherwise.",
 "The combined label shown is the broad one, which uses platinum status where available and the re-derived platinum-free interval otherwise; the recommended strict label covers 355 patients (Table 2)."),
("**Fig 4. Where characteristics act: platinum-free interval versus survival after progression (exploratory).** Hazard ratios (95% CI, log scale) from univariable Cox models of the platinum-free interval from the end of first-line platinum (blue) and of survival after progression among patients who progressed (orange). Times from TCGA-CDR.",
 "**Fig 4. Associations with the platinum-free interval and with survival after progression (exploratory).** Hazard ratios (95% CI, log scale) from univariable Cox models of the platinum-free interval from the end of first-line platinum (blue; intervals below 1 day, including the 8 negative intervals, set to 1 day) and of survival after progression among patients who progressed (orange; patients whose progression event was their death excluded). Times from TCGA-CDR. The two models were not compared formally."),

# ── table 2 (points 2, 6) ────────────────────────────────────────────────────────────────────────────────
("| Combined platinum label | Platinum status where determinate, otherwise platinum-free interval | As above | 394 (113 / 281) | 189 |",
 "| Strict combined label (recommended) | Platinum status where determinate, otherwise platinum-free interval in patients with a clean record | As above, with provenance audit | 355 (99 / 256) | 167 (43 / 124) |\n| Broad combined label (sensitivity analysis) | Platinum status where determinate, otherwise platinum-free interval | As above | 394 (113 / 281) | 189 (51 / 138) |"),

# ── supporting information list (point 6) ────────────────────────────────────────────────────────────────
("S1 Text. Pre-specified predictions and decision rules for each analysis, with observed outcomes.",
 "S11 Table. Patient-level label table (version 1.0): every label, the strict and broad combined labels, provenance class, event source and flags for the 489 platinum-treated patients, with a data dictionary and class counts.\n\nS1 Text. Pre-specified predictions and decision rules for each analysis, with observed outcomes."),
]


def main() -> None:
    s = P.read_text(encoding="utf-8")
    assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a)
        assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8")
    print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
