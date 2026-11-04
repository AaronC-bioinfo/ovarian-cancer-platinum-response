#!/usr/bin/env python3
"""
manuscript_v5/apply_review5_round7b_2026-10-30.py
Round 7b (2026-10-30, ~01:55 ET): fixes from the independent audit of round 7 + the restructure.
Sources: labels_full.csv and the PanCancer clinical file (TCGA-24-0968: deceased, no OS time, platinum-sensitive);
a23_anchor_checks.csv; a23_ipcw_variants.csv; a22 summary (median +0.010; 2.5th–97.5th percentiles −0.183, +0.157);
a13_redaction.csv; a13_cohort_flow.csv (47.7).
Run from manuscript_v5/: python apply_review5_round7b_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
('define "response" in different ways, often without stating the definition.', 'define "response" in different, often unstated, ways.'),
("out-of-bag refits of the whole pipeline ranged from −0.18 to +0.16).",
 "out-of-bag refits of the whole pipeline: median +0.01, 2.5th–97.5th percentiles −0.18 to +0.16)."),
("(8 and 17 of those with a platinum status; S2 Table).",
 "(8 and 17 of those with a platinum status) and 1 platinum-sensitive patient who died without a recorded survival time (S2 Table)."),
('(platinum rows: treatment-timeline agent names containing "platin").',
 '(platinum rows: treatment-timeline agent names containing "platin", which includes oxaliplatin; restricting the anchor to carboplatin and cisplatin, the cohort\'s agents, changed no call and left 2 patients undetermined).'),
("Any predictions or decision rule were written into the script header before the analysis was run.",
 "Any predictions or decision rule were written into the script header before the analysis was run (exceptions are disclosed in S1 Text)."),
("(PPV equal to the prevalence of resistance; specificity equal to the proportion not flagged) the highest sensitivity",
 "(PPV equal to the prevalence of resistance; specificity equal to the proportion not flagged) and the highest sensitivity"),
("with almost unchanged κ; S10 Table)", "with almost unchanged κ with platinum status; S10 Table)"),
("whose survival was poorer (median 27.6 months)", "whose survival was poorer (median 27.6 months, against 47.7 in the cohort)"),
("Three analyses were exploratory (see Pre-specification).", "Three analyses were exploratory, added after the main results were known (S1 Text)."),
("S1 Text. Pre-specified predictions and decision rules for each analysis, with observed outcomes.",
 "S1 Text. Pre-specified predictions and decision rules for each analysis, with observed outcomes, and the analysis history and deviations."),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
