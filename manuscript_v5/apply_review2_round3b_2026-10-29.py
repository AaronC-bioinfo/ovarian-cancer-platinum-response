#!/usr/bin/env python3
"""
manuscript_v5/apply_review2_round3b_2026-10-29.py
Round 3b: fixes from the independent audit of round 3 (apply_review2_round3_2026-10-29.py).
Sources: labels_master.csv (19 negative: 8 events / 11 censored; 9 zero: 4 / 5); a13b_decomposition_cox.csv
(max |dHR| at risk vs clipped 0.031); a15b_provenance.csv (35 record-flagged added patients: redacted 10, missing
stop date 1, later-line 14, near-threshold 15, 5 with two flags, 13 near-threshold only).
Run from manuscript_v5/: python apply_review2_round3b_2026-10-29.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
("the 28 patients with an interval of 0 days or less (12 with an event, 16 censored) were excluded (analysis A13b).",
 "the 28 patients with an interval of 0 days or less were excluded (analysis A13b): the 19 negative intervals described under Labels (8 with an event, 11 censored) and 9 intervals of 0 days (4 with an event, 5 censored)."),
("changed no hazard ratio by more than 0.03 and no conclusion.",
 "changed no hazard ratio by more than about 0.03 and no conclusion."),
("in those 134 patients (39 resistant), differences of up to about 0.09 AUC in favour of the platinum label, or 0.11 in favour of the OS label, could not be excluded.",
 "in those 134 patients (39 resistant), and within an analysis that does not refit the models, differences of up to about 0.09 AUC in favour of the platinum label, or 0.11 in favour of the OS label, could not be excluded."),
("cannot exclude one of up to about 0.09–0.11 AUC in either direction,",
 "cannot exclude one of up to about 0.09 AUC in favour of the platinum label or 0.11 in favour of the OS label,"),
("38 were flagged, for a record problem (35) or because",
 "38 were flagged, for a record problem (35; 13 of them only for an interval within 150–215 days) or because"),
("and the label without it (367 patients) is reported as a sensitivity analysis.",
 "and the label without it (367 patients; label table column label_combined_strict_asrun, with its OS-threshold test characteristics in S1 Text) is reported as a sensitivity analysis."),
("S10 Table. Exploratory analyses: decomposition of overall survival, clinical-only models and the redaction sensitivity analysis; Cox models of the progression-free interval.",
 "S10 Table. Exploratory analyses: decomposition of overall survival (platinum-free interval in patients at risk at the end of platinum, with the earlier model that set short intervals to 1 day as a sensitivity analysis), clinical-only models and the redaction sensitivity analysis; Cox models of the progression-free interval."),
("The exploratory decomposition, added after review, is consistent", "The exploratory decomposition, added after the main results were known, is consistent"),
("Any residual versus none was an alternative coding added after review.", "Any residual versus none was an alternative coding added after the main results were known."),
("Overall survival comprises the time to the end of first-line platinum, the platinum-free interval and survival after progression.",
 "For patients who progress after the end of first-line platinum, overall survival comprises the time to the end of platinum, the platinum-free interval and survival after progression."),
("light segment, responders.", "light segment, responders; dashed line, all 489 patients; colour denotes label family."),
("(D) Provenance of the 117 patients added by the re-derived interval: unflagged resistant or sensitive, flagged for a record problem, resistant call dated only by a death counted as progression, or negative interval.",
 "(D) Provenance of the 117 patients added by the re-derived interval: unflagged resistant or sensitive; flagged only for an interval within 150–215 days; flagged for another record problem (redacted TCGA-CDR record, adjuvant platinum without a stop date, or a later-line regimen before the event, with or without a near-threshold interval); resistant call dated only by a death counted as progression; or negative interval."),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
