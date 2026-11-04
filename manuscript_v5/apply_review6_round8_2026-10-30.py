#!/usr/bin/env python3
"""
manuscript_v5/apply_review6_round8_2026-10-30.py
Round 8 (2026-10-30, ~09:05 ET): response to the sixth review (of revision 7; minor revision). Wording only; no new analysis.
Sources: a23_anchor_checks.csv (carbo/cis: 0 changed, 2 undetermined, 1 of them among the 78; A1–A3: 0 changed and 0
undetermined among the 78); a21_event_type.csv; label_validity/PLATINUM_STATUS_definition.md (SI pp. 2–3).
Run from manuscript_v5/: python apply_review6_round8_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
('define "response" in different, often unstated, ways.', 'define "response" in different, variably reported ways.'),
("(difference in AUC −0.005, conditional 95% interval −0.105 to +0.087; out-of-bag refits of the whole pipeline: median +0.01, 2.5th–97.5th percentiles −0.18 to +0.16).",
 "(difference in AUC −0.005, 95% conditional interval −0.105 to +0.087), and refitting the whole pipeline left the comparison inconclusive."),
("with no interval crossing 1 (S11 Table).", "and none of these comparisons changed whether its interval included 1 (S11 Table)."),
("changed no call and left 2 patients undetermined).",
 "changed no resistant or sensitive classification among patients determinate under both rules, but left 2 patients, 1 of them among the 78 unflagged additions, undetermined)."),
("none among the 78 unflagged added patients (S1 Text; S11 Table).",
 "and all 78 unflagged added patients remained determinate and unchanged (S1 Text; S11 Table)."),
("those without a determinate status did not differ in overall survival from those with one",
 "no overall-survival difference was detected between those without a determinate status and those with one"),
("but not platinum status (0.48),", "whereas discrimination was near chance for platinum status (0.48),"),
("24-month-OS-trained models scored no better than platinum-trained ones", "no improvement of 24-month-OS-trained over platinum-trained models was demonstrated"),
("Markers of platinum response cannot settle which label is better:", "These marker analyses did not distinguish the labels in this cohort:"),
("Confine every supervised data-dependent step, including gene selection, to training data, and report any normalisation done within an external cohort.",
 "Within cross-validation, estimate feature selection and preprocessing from training data only, and describe separately any normalisation that uses an external cohort's predictor distribution."),
("[@tcga2011, Supplementary Methods S1];", "[@tcga2011, Supplementary Methods S1, pp. 2–3];"),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()

# Applied after the script above (same session), Fig 3 legend:
#   'Dots and dark lines, cross-validated estimates (same folds for every label) with conditional 95% intervals from resampling patients without refitting the models; light bars, 2.5th–97.5th percentiles of out-of-bag differences from 500 bootstrap refits of the whole pipeline (a sensitivity analysis of a different quantity, not centred on the dots).'
#   -> 'For each contrast, the upper row (circles, solid lines) gives the cross-validated estimate (same folds for every label) with its conditional 95% interval from resampling patients without refitting the models; the lower row (squares, dashed lines) gives the median and 2.5th–97.5th percentile range of out-of-bag differences from 500 bootstrap refits of the whole pipeline, a sensitivity analysis of a different quantity.'
