#!/usr/bin/env python3
"""
manuscript_v5/apply_review4_round6_2026-10-30.py
Round 6 (2026-10-30, ~00:42 ET): adds A21 (event-type sensitivity) and A22 (full-pipeline bootstrap), done at Aaron's
request after round 5. Sources: label_validity/outputs/21_event_type_sensitivity_summary.md, a21_event_type.csv
(κ 0.9662 both; OS sens/PPV changes 0.034/0.042/0.027/0.033; BRCA OR 0.370→0.364; CCNE1 1.763→1.713);
22_fullpipeline_bootstrap_summary.md, a22_fullpipeline_replicates.csv (500/500 usable; ΔAUC24 −0.183 to +0.157, median +0.010;
ΔAUC18 −0.145 to +0.244; reverse −0.233 to +0.218). A22's decision rule makes the full-pipeline interval the main
uncertainty for the controlled comparison.
Run from manuscript_v5/: python apply_review4_round6_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
("(difference in AUC −0.005; 95% conditional bootstrap interval, without model refitting, −0.105 to +0.087).",
 "(difference in AUC −0.005; 95% interval from refitting the whole pipeline in 500 bootstrap samples, −0.18 to +0.16)."),
("The same script rerun in a second software environment gave the same conclusions, which checks computational consistency only (S1 Text).",
 "The same script rerun in a second software environment gave the same conclusions, which checks computational consistency only (S1 Text). To capture the uncertainty of the whole procedure, the pipeline (gene filter, scaling and the three models for each training label) was also refitted in 500 bootstrap samples of the 134 patients, drawn within platinum-status groups, and evaluated on the patients not drawn; the 2.5th and 97.5th percentiles of these out-of-bag differences give the full-pipeline interval, which by a rule fixed before the run is the main uncertainty reported (analysis A22)."),
("(difference in AUC −0.005; 95% conditional bootstrap interval −0.105 to +0.087).",
 "(difference in AUC −0.005; full-pipeline 95% interval −0.18 to +0.16, conditional interval −0.105 to +0.087)."),
("No clear difference between training labels was demonstrated. Within this conditional analysis, advantages larger than about 0.09 AUC for the platinum label or about 0.11 for the OS label were not supported, but these bounds do not describe the variability of the training procedure itself (S1 Text).",
 "Refitting the whole pipeline in 500 bootstrap samples widened the intervals (out-of-bag median +0.01 for the primary contrast; −0.15 to +0.24 for 18-month-OS-trained models; −0.23 to +0.22 on the 24-month OS label; Fig 3B). No clear difference between training labels was demonstrated, and differences of up to about 0.16 AUC in favour of the platinum label or 0.18 in favour of the OS label remain compatible with the data (S1 Text)."),
("in those 134 patients (39 resistant), and within an analysis that does not refit the models, differences of up to about 0.09 AUC in favour of the platinum label, or 0.11 in favour of the OS label, could not be excluded.",
 "in those 134 patients (39 resistant), differences of up to about 0.16 AUC in favour of the platinum label, or 0.18 in favour of the OS label, could not be excluded when the whole pipeline was refitted."),
("cannot exclude one of up to about 0.09 AUC in favour of the platinum label or 0.11 in favour of the OS label, and its interval does not include the variability from refitting models.",
 "cannot exclude one of up to about 0.16 AUC in favour of the platinum label or 0.18 in favour of the OS label, and its out-of-bag estimates come from fits on about two-thirds of the patients."),
("post hoc analyses with decision rules but no predictions (A13b, A18, A19);",
 "post hoc analyses with decision rules (A13b, A18, A19, A21, and A22 with one prediction);"),
("except the exploratory clinical-only models and the fold recount in A20 (Python 3.10, scikit-learn 1.7.2);",
 "except the exploratory clinical-only models, the fold recount in A20 and the full-pipeline bootstrap in A22 (Python 3.10, scikit-learn 1.7.2);"),
("4 by a new tumour event of unrecorded type and 6 by a death counted as progression.",
 "4 by a new tumour event of unrecorded type and 6 by a death counted as progression. Setting aside the 10 calls dated only by a death or by an event of unrecorded type did not change κ with platinum status, changed the sensitivity and PPV of the OS thresholds against the combined reference by at most 0.04, and changed the *BRCA1/2* and *CCNE1* odds ratios by at most 0.05, with no interval moving across 1 (S1 Text, analysis A21)."),
("difference in AUC between training labels (mean of three models) with 95% bootstrap intervals that resample patients but do not refit models.",
 "difference in AUC between training labels (mean of three models) with 95% intervals from refitting the whole pipeline in 500 bootstrap samples (light bars) and from resampling patients without refitting the models (dark lines)."),
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
#   '(difference in AUC −0.005; 95% interval from refitting the whole pipeline in 500 bootstrap samples, −0.18 to +0.16).'
#   -> '(difference in AUC −0.005; 95% full-pipeline bootstrap interval −0.18 to +0.16).'
