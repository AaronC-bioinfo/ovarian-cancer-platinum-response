#!/usr/bin/env python3
"""
manuscript_v5/apply_review3_round4_2026-10-29.py
Round 4: response to the third review (2026-10-29, ~23:20 ET; minor revision).
Sources: a15b_provenance.csv with each added patient counted once (order: negative interval, death-dated
resistant call, other record flag, near-threshold only): 1 / 6 / 20 / 12, unflagged 78; the 12 near-only patients are
exactly the patients in a15_label_combined_strict (367) and not in a15b (355), checked by ID. labels_master.csv:
53 of 489 without a re-derived interval (52 no first-line platinum stop date, 1 no PFI time); 436 with one.
The analysis-history sentences removed from Methods are moved verbatim into the S1 Text introduction (build_SI.py).
Run from manuscript_v5/: python apply_review3_round4_2026-10-29.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
HIST_OLD = ("The study's interpretation changed during the work. An earlier draft concluded, from somatic *BRCA1/2* variants and from OS labels analysed only in patients with RNA-seq data, that OS thresholds measure survival rather than platinum response; the publicly deposited analyses with germline variants and the full cohort did not support that conclusion, and the paper was revised. In later revisions, the OS thresholds were reframed as candidate surrogates, the survival decomposition was reported as associations only and restricted to patients at risk at the end of platinum, the provenance audit was added, and the claim that the training label changes classifier performance was withdrawn when the controlled comparison detected no difference. In the provenance audit, the code omitted one pre-specified flag (an interval within 150–215 days); this was found when the results were scored, and a correction run that adds only that flag gives the provenance-filtered label reported here (355 patients, against 367 as first run; S1 Text). The descriptive full-cohort tables (agreement, coverage, threshold sweep, cohort characteristics) and the exploratory analyses above were added afterwards. All predictions and their outcomes, including those that failed, are listed in S1 Text.")
E = [
# point 5: shorten the revision history
("### Pre-specification and analysis history", "### Pre-specification"),
("The scripts for the analyses of *BRCA1/2* and *CCNE1*, of patients without a platinum status, and of prognostic characteristics in the full cohort were deposited in the public code repository before they were run (commits d5bd844 and e98b3d9), as were those of the provenance audit and the controlled classifier comparison, added in a later revision (commit d349b2b);",
 "The scripts for the analyses of *BRCA1/2* and *CCNE1*, of patients without a platinum status, of prognostic characteristics in the full cohort, of provenance and of the controlled classifier comparison were deposited in the public code repository before they were run (commits d5bd844, e98b3d9 and d349b2b);"),
(HIST_OLD,
 "The descriptive full-cohort tables and the analyses labelled exploratory were added after the main results were known. One material deviation occurred: the provenance-audit code omitted one pre-specified flag (an interval within 150–215 days), and the reported label comes from a correction run that adds only that flag (S1 Text). All predictions and their outcomes, including those that failed, and the development history of the analyses are given in S1 Text."),
("Several pre-specified predictions failed, including the predictions that *BRCA1/2* would show no clear association with the OS thresholds, that patients without a platinum status would have shorter survival and would more often be resistant by the re-derived interval, and that the 24-month threshold would have a sensitivity of 0.30 or less, and, in the later analyses, that the provenance-filtered combined label would cover at least 370 patients, that at least two of the four disagreements would carry a flag or a near-threshold interval, and that platinum-trained models would predict platinum status better than 24-month-OS-trained models (and the reverse on the OS label); all outcomes are reported in S1 Text.",
 "Several pre-specified predictions failed, including that *BRCA1/2* would show no clear association with the OS thresholds and that platinum-trained classifiers would predict platinum status better than OS-trained ones; all predictions and outcomes are listed in S1 Text."),
("An earlier version of this model set those intervals to 1 day; it is reported as a sensitivity analysis (S10 Table).",
 "A model that sets those intervals to 1 day is reported as a sensitivity analysis (S10 Table)."),
# point 1: counts
("38 were flagged, for a record problem (35; 13 of them only for an interval within 150–215 days) or because their only event was a death counted as progression (3), and 1 had a negative interval (Fig 1D, S11 Table).",
 "and 39 were not. Counting each patient once, 1 had a negative interval, 6 had a resistant call dated only by a death counted as progression, 20 had another record problem (a redacted TCGA-CDR record, adjuvant platinum without a stop date, or a later-line regimen before the event), and 12 were flagged only for an interval within 150–215 days (Fig 1D, S11 Table); these 12 are exactly the patients that the label without that flag adds."),
("78 were unflagged (12 resistant, 66 sensitive), and 39 were not.", "78 were unflagged (12 resistant, 66 sensitive) and 39 were not."),
("(D) Provenance of the 117 patients added by the re-derived interval:",
 "(D) Provenance of the 117 patients added by the re-derived interval, each counted once (in the order negative interval, resistant call dated only by a death, other record problem, interval within 150–215 days only):"),
# point 2: population and flow of the Cox analysis
("(4 with an event, 5 censored).",
 "(4 with an event, 5 censored). Of the 489 patients, 53 had no re-derived interval (52 without a recorded stop date for first-line platinum and 1 without a TCGA-CDR progression-free interval time), so 436 entered this step and 408 were analysed; each model's sample size and number of events, after missing covariate values, are given in S10 Table."),
("were exploratory and were added after the main results were known.",
 "were exploratory and were added after the main results were known. The decomposition describes patients who were event-free and under observation at the end of first-line platinum, not the whole platinum-treated cohort."),
# point 3: abstract qualifier
("with the same folds, platinum-trained and 24-month-OS-trained models did not differ detectably in predicting platinum status (difference in AUC −0.005, 95% CI −0.105 to +0.087).",
 "with the same folds, platinum-trained and 24-month-OS-trained models did not differ detectably in predicting platinum status (difference in AUC −0.005; 95% conditional bootstrap interval, without model refitting, −0.105 to +0.087)."),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
