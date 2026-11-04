#!/usr/bin/env python3
"""
manuscript_v5/apply_review4_round6b_2026-10-30.py
Round 6b (2026-10-30, ~00:55 ET): fixes from the independent audit of round 6.
Sources: a22_fullpipeline_replicates.csv (out-of-bag n mean 49.0, range 38–59; OS24-target positives mean 6.6, min 1;
medians +0.010, +0.063, −0.004; distinct-patient share ≈ 0.63); a15b_resistant_event_source.csv (all 10 set-aside
calls are among the added patients, none with platinum status).
Run from manuscript_v5/: python apply_review4_round6b_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
("(the time string of one header, A18, was corrected after its run, as disclosed in S1 Text)",
 "(the time strings of two headers, A18 and A21, were corrected after their runs, and a bug in A22 was fixed before it produced any result; all are disclosed in S1 Text)"),
("did not change κ with platinum status, changed the sensitivity and PPV of the OS thresholds against the combined reference by at most 0.04,",
 "(none of whom had a platinum status, so κ with platinum status was unaffected) changed the sensitivity and PPV of the OS thresholds against the broad combined reference by at most 0.04,"),
("with no interval moving across 1 (S1 Text, analysis A21).", "with no interval moving across 1 (S1 Text, analysis A21; S11 Table)."),
("and the interval reflects the sampling of patients but not the refitting of models.",
 "and the conditional interval reflects the sampling of patients but not the refitting of models."),
("so that this comparison is particularly unstable, was +0.080 (−0.045 to +0.201); on the 24-month OS label, 24-month-OS-trained models scored no better than platinum-trained ones (difference −0.069, −0.236 to +0.081).",
 "so that this comparison is particularly unstable, was +0.080 (full-pipeline interval −0.15 to +0.24; conditional −0.045 to +0.201); on the 24-month OS label, 24-month-OS-trained models scored no better than platinum-trained ones (difference −0.069; full-pipeline −0.23 to +0.22; conditional −0.236 to +0.081)."),
("Refitting the whole pipeline in 500 bootstrap samples widened the intervals (out-of-bag median +0.01 for the primary contrast; −0.15 to +0.24 for 18-month-OS-trained models; −0.23 to +0.22 on the 24-month OS label; Fig 3B).",
 "The full-pipeline intervals are percentiles of out-of-bag differences, each from a single fit on about 63% of the distinct patients and evaluated on the remaining patients (on average 49, with as few as one positive for the 24-month OS label); they are centred on the out-of-bag differences (medians +0.01, +0.06 and −0.004) rather than on the estimates above, include test-set noise and are probably conservative (Fig 3B)."),
("and its out-of-bag estimates come from fits on about two-thirds of the patients.",
 "and its out-of-bag estimates come from fits on about 63% of the distinct patients."),
("which by a rule fixed before the run is the main uncertainty reported (analysis A22).",
 "which by a rule fixed before the run is the main uncertainty reported (analysis A22; run with scikit-learn 1.7.2, in which random-forest fits differ slightly from those in the A16 environment)."),
("(difference in AUC −0.005; 95% full-pipeline bootstrap interval −0.18 to +0.16).",
 "(difference in AUC −0.005; 95% range of out-of-bag differences when the whole pipeline was refitted in bootstrap samples, −0.18 to +0.16)."),
("(B) Controlled comparison in the same 134 patients with the same folds: difference in AUC between training labels (mean of three models) with 95% intervals from refitting the whole pipeline in 500 bootstrap samples (light bars) and from resampling patients without refitting the models (dark lines).",
 "(B) Controlled comparison in the same 134 patients: difference in AUC between training labels (mean of three models). Dots, estimates with the same folds for every label; light bars, 95% range of out-of-bag differences from refitting the whole pipeline in 500 bootstrap samples (centred on those differences, not on the dots); dark lines, 95% intervals from resampling patients without refitting the models."),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()

# Applied after the script above (same session) to keep the abstract within 300 words:
#   'although among patients with RNA-seq data it added only 2 resistant patients to platinum status.'
#   -> 'although it added only 2 resistant patients with RNA-seq data.'
