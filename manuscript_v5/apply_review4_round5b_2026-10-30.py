#!/usr/bin/env python3
"""
manuscript_v5/apply_review4_round5b_2026-10-30.py
Round 5b: fixes from the independent audit of round 5. Exact replacements; each must match once.
Sources: treatment timeline (agents matching "PLATIN": carboplatin 659 rows, cisplatin 165, oxaliplatin 7 (4 adjuvant;
the anchor for 3 patients, 2 with a determinate interval), 3 combination rows); a18_anchor_summary.csv / a18_anchor_counts.csv;
a19_ipcw.csv (censored before t with a platinum status: 8 and 17); a20_discordant.csv (TCGA-29-1774: A1 0, A2 0, A3 1);
Cocchi 2026 (PMC13443249; abstract and conclusions, checked 2026-10-30); Villalobos 2018 p. 4.
Run from manuscript_v5/: python apply_review4_round5b_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
# must-fix 1: platinum rows
("Platinum rows were treatment-timeline rows with carboplatin or cisplatin as the agent; no platinum row carried a neoadjuvant indication.",
 "Platinum rows were treatment-timeline rows whose agent name contains \"platin\" (carboplatin and cisplatin, and oxaliplatin, which supplies the anchor for 3 patients, 2 of them with a determinate interval); no platinum row carried a neoadjuvant indication."),
# should-fix 6 + minor: anchor counts and κ
("the latest stop date was used. With alternative anchors — the earliest adjuvant stop date, the end of the first platinum regimen whatever its indication, or the latest adjuvant stop date before any later-line regimen — 0 to 5 of the 389 calls changed (κ with the primary label at least 0.97; S1 Text, analysis A18).",
 "the latest stop date was used; 1 patient had an adjuvant platinum row without a stop date, 1 had an adjuvant row starting after a later-line regimen, 6 had a platinum row with another or no indication, and 23 cohort patients had no adjuvant platinum row. With alternative anchors — the earliest adjuvant stop date, the end of the first platinum regimen whatever its indication (which also labels 18 patients without an adjuvant row), or the latest stop date among adjuvant rows starting before any later-line regimen (which leaves one patient undetermined) — 0 to 5 of the calls determinate under both anchors changed (κ with the primary label about 0.97; S1 Text, analysis A18)."),
# should-fix 3
("and one of these (101 days, three adjuvant platinum rows) became sensitive under the alternative anchors, so two disagreements remain unexplained by the available records (S11 Table).",
 "and one of these (101 days, three adjuvant platinum rows) became sensitive under two of the three alternative anchors, which themselves create other disagreements; the remaining two are not explained by the available records (S11 Table)."),
("and two disagreements with unflagged records remain unexplained.", "and at least two disagreements with unflagged records remain unexplained."),
# should-fix 4, 5
("These values also exclude the 69 and 87 patients censored before each threshold; with inverse-probability-of-censoring weights, sensitivity, specificity and PPV changed by at most 0.04 (S1 Text), but weighting assumes censoring unrelated to outcome given age, stage and residual disease, and it does not address missing platinum status.",
 "These values also exclude patients censored before each threshold (8 and 17 of those with a platinum status; 69 and 87 in the cohort). With inverse-probability-of-censoring weights, sensitivity, specificity and PPV changed by at most 0.04 (S1 Text). The Kaplan–Meier weights assume censoring unrelated to outcome, and the Cox weights unrelated given age, stage and residual disease; the censoring distribution was estimated in the whole cohort rather than in patients with a status, and weighting does not address missing platinum status."),
# should-fix 7
("(difference in AUC −0.005, 95% CI −0.105 to +0.087)", "(difference in AUC −0.005; 95% conditional bootstrap interval −0.105 to +0.087)"),
# should-fix 8
("Predictions and decision rules were written into the header of each analysis script before it was run.",
 "Where an analysis had predictions or a decision rule, they were written into its script header before it was run (the time string of one header, A18, was corrected after its run, as disclosed in S1 Text)."),
("which may have been informed by them; and exploratory analyses without predictions.",
 "which may have been informed by them; post hoc analyses with decision rules but no predictions (A13b, A18, A19); and exploratory or descriptive analyses without predictions (including A20)."),
("except the exploratory clinical-only models (Python 3.10, scikit-learn 1.7.2);",
 "except the exploratory clinical-only models and the fold recount in A20 (Python 3.10, scikit-learn 1.7.2);"),
# should-fix 9: Cocchi
("and showed that patient selection, platinum-sensitivity definitions, data sources and analytical pipelines change the genes reported [@cocchi];",
 "and reported that variability in patient selection, platinum-sensitivity definitions, data sources and analytical pipelines limits the reproducibility of the genes reported [@cocchi];"),
("showed that patient selection, platinum-sensitivity definitions, data sources and analytical pipelines all change which genes TCGA-OV studies report [@cocchi].",
 "reported that the genes identified by TCGA-OV studies vary with analytical pipelines and cohort definitions [@cocchi]."),
# should-fix 11
("these comparisons could detect only a ratio of odds ratios of about 4.7 and 10 with 80% power, so they do not show that the labels behave alike (S3 Table).",
 "the approximate minimum detectable ratios of odds ratios were about 4.7 and 10, so these comparisons do not show that the labels behave alike (S3 Table)."),
# should-fix 12
("A classifier learns whatever its label measures.", "A classifier is trained to predict whatever its label records."),
("They are nonetheless well below the figures commonly reported [@wangq; @chen; @li; @gao];",
 "They are nonetheless well below the figures reported in several studies [@wangq; @chen; @li; @gao], although those used other cohorts, data types and designs;"),
# minor: Villalobos wording, PH consequence
("in patients whose disease recurred 1–6 months after the last platinum dose", "in patients whose treatment failed 1 to 6 months after the last platinum dose"),
("(age for the platinum-free interval, Aneuploidy Score for survival after progression), and an added quadratic term",
 "(age for the platinum-free interval, Aneuploidy Score for survival after progression; those two hazard ratios are averages over follow-up), and an added quadratic term"),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
