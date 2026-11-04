#!/usr/bin/env python3
"""
manuscript_v5/apply_external_review_round2_2026-10-29.py
Second round of the external-review revision: fixes from the independent audit of round 1
(apply_external_review_2026-10-29.py). Exact replacements, each must match once.
Number sources: labels_master.csv pfi_from_platinum_d (436 with an interval; 28 < 1 day; 19 negative; 9 zero);
a15b_provenance.csv (38 added flagged; 3 of them with no record flag, event = death counted as progression);
a16_paired_differences.csv (per_repeat_mean −0.0162; boot_lo −0.105, boot_hi +0.087); label_resource_v1_counts.csv
(strict, RNA-seq 167 / 43); 11 summary (212 without status; 117 added). Earlier release: Zenodo 10.5281/zenodo.20802754.
Run from manuscript_v5/: python apply_external_review_round2_2026-10-29.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"

E = [
# audit must-fix 1: number of floored intervals
("with intervals below 1 day (including the 8 negative intervals) set to 1 day.",
 "with the 28 intervals below 1 day (19 negative and 9 of 0 days) set to 1 day."),
("(blue; intervals below 1 day, including the 8 negative intervals, set to 1 day)",
 "(blue; the 28 intervals below 1 day, 19 of them negative, set to 1 day)"),
# audit 3: definition of clean
("a later-line regimen started before the recorded event (for sensitive patients, before day 183), or an interval within 150–215 days of the end of platinum. Patients with a recorded event, or an interval of at least 183 days, and no flag were classed clean.",
 "a later-line regimen started after the end of platinum but before the recorded event (for sensitive patients, within 183 days of the end of platinum), or an interval within 150–215 days of the end of platinum. Resistant patients whose event was a recorded new tumour event, and sensitive patients, were classed clean if they had no flag; resistant calls dated only by a death counted as progression were never classed clean, and negative intervals formed a separate class."),
("because more than 20% of the added patients were not clean.",
 "because more than 20% of the added patients were not clean. The strict label is used for the recommendation, the label table and the evaluation of OS thresholds against a combined reference; the other analyses use platinum status, the re-derived interval or the broad combined label, as stated."),
("38 were flagged and 1 had a negative interval (S11 Table).",
 "38 were not classed clean because of a flag (35) or because their only event was a death counted as progression (3), and 1 had a negative interval (S11 Table)."),
# minor: label count
("each coded 1 for non-response or resistance and 0 otherwise (Table 2).",
 "each coded 1 for non-response or resistance and 0 otherwise, together with two combinations of the platinum labels (Table 2)."),
# audit 4: broad vs strict
("the re-derived interval (0.52) or the combined label (0.49).",
 "the re-derived interval (0.52) or the broad combined label (0.49)."),
("cover just over half of treated patients, or about four-fifths when combined.",
 "cover just over half of treated patients, or about four-fifths when combined (nearly three-quarters with the strict combined label)."),
("re-deriving the interval from TCGA-CDR recovers about half of them, and where both labels are available they agree closely. In the patients it adds, two-thirds of calls rest on clean records, and the strict combined label keeps only those.",
 "re-deriving the interval from TCGA-CDR recovers about half of them (117 of 212), and where both labels are available they agree closely. Two-thirds of the added calls (78) rest on clean records, and the strict combined label keeps only those."),
("the primary label is available for only 145 patients with RNA-seq data (41 resistant),",
 "platinum status is available for only 145 patients with RNA-seq data (41 resistant; the strict combined label for 167, 43 resistant),"),
# audit 5: leftover label-effect claim
("models trained on the platinum labels scored higher (0.67 and 0.71) than OS-trained models (0.49 and 0.52), a comparison that was not pre-specified (S1 Fig, S7 Table).",
 "models trained on the platinum labels had AUCs of 0.67 and 0.71 and OS-trained models 0.49 and 0.52; this comparison was not pre-specified, has no interval and is descriptive only (S1 Fig, S7 Table)."),
# audit 6: A16 interval wording
("(stratified five-fold cross-validation repeated 20 times).",
 "(five-fold cross-validation stratified on platinum status, repeated 20 times)."),
("using out-of-fold scores averaged over repeats.",
 "using out-of-fold scores averaged over repeats; models were not refitted within the bootstrap. The same script rerun in a second software environment gave the same conclusions (S1 Text)."),
("No difference between training labels was detected, and a platinum-label advantage larger than about 0.09 AUC is unlikely (S1 Text).",
 "The estimate is the AUC difference for out-of-fold scores averaged over the 20 repeats (the mean of the per-repeat differences was −0.016), and the interval reflects the sampling of patients but not the refitting of models. No difference between training labels was detected; the interval excludes an advantage larger than about 0.09 AUC for the platinum label or about 0.11 for the OS label (S1 Text)."),
("with 39 resistant patients, differences smaller than about 0.09 AUC could not be excluded. With a standard, untuned pipeline and 41 resistant patients,",
 "in those 134 patients (39 resistant), differences of up to about 0.09 AUC in favour of the platinum label, or 0.11 in favour of the OS label, could not be excluded. With a standard, untuned pipeline and 41 resistant patients in the all-patients analysis,"),
("detected no difference but cannot exclude one smaller than about 0.09 AUC.",
 "detected no difference but cannot exclude one of up to about 0.09–0.11 AUC in either direction, and its interval does not include the variability from refitting models."),
# audit 7: cite the earlier release
("because our own earlier classifier analyses of this cohort used them, not because they are established practice.",
 "because our own earlier classifier of this cohort used them [@chintala2026], not because they are established practice."),
("The 18- and 24-month thresholds are those used in our own earlier classifier analyses of this cohort, and we evaluate them",
 "The 18- and 24-month thresholds are those used in our own earlier classifier of this cohort, which defined platinum response as survival beyond 12, 18 or 24 months [@chintala2026]; the present study supersedes that interpretation, and we evaluate them"),
# audit 8: leftover decomposition wording
("Age and residual disease > 1 cm showed the opposite pattern: they were associated with shorter survival after progression",
 "Age and residual disease > 1 cm were associated with shorter survival after progression"),
("An OS-threshold label may therefore mix early platinum failure with other prognostic information; this would need confirmation in another cohort.",
 "An OS-threshold label may mix early platinum failure with other prognostic information; the decomposition raises this possibility but does not test it, and it would need confirmation in another cohort."),
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
