#!/usr/bin/env python3
"""
manuscript_v5/apply_review2_round3_2026-10-29.py
Round 3: response to the second review of the revised manuscript (2026-10-29, ~22:55 ET).
Part 1: exact targeted replacements (each must match once). Part 2: vocabulary change
("strict" -> "provenance-filtered"; "clean" -> "unflagged"), each pattern with an expected count.
Decisions (Aaron, 2026-10-29): descriptive title; drop "external review" wording; decomposition re-run with
patients at risk at the end of platinum (A13b) as the reported analysis.
Number sources: a13b_decomposition_cox.csv / 13b summary (408 at risk; 28 excluded: 12 events, 16 censored;
HRs); label_resource_v1_counts.csv (RNA-seq 145/41 -> 167/43; as-run 367/104); a15b_provenance.csv.
Run from manuscript_v5/: python apply_review2_round3_2026-10-29.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"

T = [
# title (review point 5)
("# Which outcome label should a platinum-response classifier use? Coverage, agreement and provenance of candidate labels in TCGA-OV",
 "# Coverage, agreement and provenance of candidate platinum-response labels in TCGA-OV"),
# abstract (point 3)
("covered 355 patients (99 resistant).",
 "covered 355 patients (99 resistant), although among patients with RNA-seq data it added only 2 resistant patients to platinum status."),
# intro (point 6)
("but a classifier still needs a binary label.",
 "but a binary classifier, such as those studied here, still needs a dichotomous label."),
# methods: provenance audit (points 2, 6)
("After an external review we audited the provenance of every re-derived call (S1 Text, analysis A15).",
 "We then audited the provenance of every re-derived call (S1 Text, analysis A15; added after the main results were known)."),
("and negative intervals formed a separate class.",
 "and negative intervals formed a separate class (unflagged patients are labelled clean_resistant or clean_sensitive in the label table). The 150–215-day flag was specified before the audit was run, to mark calls that a dating error of about a month could reverse; it does not imply that such records are wrong, and the label without it (367 patients) is reported as a sensitivity analysis."),
("and the re-derived interval only in clean patients.",
 "and the re-derived interval only in clean patients. Published platinum status was kept as the reference wherever it was determinate and only the re-derived additions were filtered, so the combined label does not apply uniform quality requirements: it is a conservative extension of platinum status, and the accuracy of the added calls is not verified."),
# methods: A16 (points 4, 6)
("(analysis A16, added after external review)", "(analysis A16, added after the main results were known)"),
("The same script rerun in a second software environment gave the same conclusions (S1 Text).",
 "The same script rerun in a second software environment gave the same conclusions, which checks computational consistency only (S1 Text)."),
# methods: decomposition (point 1)
("The platinum-free interval was measured from the end of first-line platinum, with the 28 intervals below 1 day (19 negative and 9 of 0 days) set to 1 day.",
 "The platinum-free interval was measured from the end of first-line platinum, and only the 408 patients at risk at that time (interval above 0 days) were included; the 28 patients with an interval of 0 days or less (12 with an event, 16 censored) were excluded (analysis A13b). An earlier version of this model set those intervals to 1 day; it is reported as a sensitivity analysis (S10 Table)."),
# methods: history (point 6)
("as were those of the provenance audit and the controlled classifier comparison added after external review (commit d349b2b);",
 "as were those of the provenance audit and the controlled classifier comparison, added in a later revision (commit d349b2b);"),
("After an external review, the OS thresholds were reframed as candidate surrogates, the survival decomposition was reported as associations only,",
 "In later revisions, the OS thresholds were reframed as candidate surrogates, the survival decomposition was reported as associations only and restricted to patients at risk at the end of platinum,"),
# results: coverage (points 2, 3, 5)
("The strict combined label was determinate for 355 patients (99 resistant, 256 sensitive; 167 with RNA-seq data) and is the label we recommend.",
 "The strict combined label was determinate for 355 patients (99 resistant, 256 sensitive; Fig 1A) and is the label we recommend; without the 150–215-day flag it would cover 367 (104 resistant). Its practical gain for expression classifiers is small: among patients with RNA-seq data it adds 22 patients to platinum status, only 2 of them resistant (145 to 167 patients; 41 to 43 resistant)."),
("38 were not classed clean because of a flag (35) or because their only event was a death counted as progression (3), and 1 had a negative interval (S11 Table).",
 "38 were flagged, for a record problem (35) or because their only event was a death counted as progression (3), and 1 had a negative interval (Fig 1D, S11 Table)."),
# results: BRCA (point 6)
("*BRCA1/2* carriers were less often labelled non-responders under every label except first-course response (Fig 2A, Table 3):",
 "*BRCA1/2* carriers were less often labelled non-responders under every label, although the evidence was imprecise for first-course response (OR 0.64, 0.18–1.80; Fig 2A, Table 3):"),
# results: decomposition numbers (point 1)
("When overall survival was divided into the platinum-free interval and survival after progression (S10 Table), *BRCA1/2* carriers had a longer platinum-free interval (hazard ratio 0.55, 95% CI 0.38–0.79), and *CCNE1* amplification (1.56, 1.19–2.06) and higher Aneuploidy Score (1.20 per SD, 1.07–1.35) a shorter one,",
 "When overall survival was divided into the platinum-free interval (408 patients at risk at the end of platinum) and survival after progression (S10 Table), *BRCA1/2* carriers had a longer platinum-free interval (hazard ratio 0.55, 95% CI 0.38–0.79), and *CCNE1* amplification (1.58, 1.19–2.09) and higher Aneuploidy Score (1.23 per SD, 1.10–1.38) a shorter one,"),
("but not clearly with the platinum-free interval (1.08, 0.98–1.19; and 1.11, 0.85–1.44).",
 "but not clearly with the platinum-free interval (1.09, 0.98–1.20; and 1.08, 0.82–1.41). Setting the excluded intervals to 1 day instead changed no hazard ratio by more than 0.03 and no conclusion."),
# results: classifiers (points 4, 5)
("Within TCGA, expression classifiers predicted each label modestly (Fig 3):", "Within TCGA, expression classifiers predicted each label modestly (Fig 3A):"),
("In the controlled comparison (134 patients, 39 platinum-resistant, the same folds for every label),",
 "In the controlled comparison (134 patients, 39 platinum-resistant, the same folds for every label; Fig 3B),"),
("No difference between training labels was detected; the interval excludes an advantage larger than about 0.09 AUC for the platinum label or about 0.11 for the OS label (S1 Text).",
 "No clear difference between training labels was demonstrated. Within this conditional analysis, advantages larger than about 0.09 AUC for the platinum label or about 0.11 for the OS label were not supported, but these bounds do not describe the variability of the training procedure itself (S1 Text)."),
# discussion (points 2, 6)
("The two platinum labels agree almost perfectly but cover just over half of treated patients, or about four-fifths when combined (nearly three-quarters with the strict combined label).",
 "The two platinum labels agree almost perfectly. Platinum status covers just over half of treated patients (277), the re-derived interval 389, and the combined labels about four-fifths (broad) or nearly three-quarters (provenance-filtered)."),
("and report each patient's provenance.",
 "and report each patient's provenance. This is a conservative extension: the accuracy of the added calls is not verified, and the filter also removes borderline patients whose records may be correct."),
# limitations (points 2, 6)
("and it does not explain the three disagreements with clean records.",
 "and it does not explain the three disagreements with clean records. The 150–215-day flag removes borderline patients whose records may be correct, which may make the filtered population less representative."),
("and, after external review, that the strict combined label would cover", "and, in the later analyses, that the strict combined label would cover"),
# figure legends (points 1, 5)
("The combined label shown is the broad one, which uses platinum status where available and the re-derived platinum-free interval otherwise; the recommended strict label covers 355 patients (Table 2).",
 "Numbers give patients labelled (non-responders or resistant). The broad combined label uses platinum status where available and the re-derived platinum-free interval otherwise; the strict combined label (recommended) adds re-derived calls only for clean patients."),
("vertical lines, 18 and 24 months.",
 "vertical lines, 18 and 24 months. (D) Provenance of the 117 patients added by the re-derived interval: clean resistant or sensitive, flagged for a record problem, resistant call dated only by a death counted as progression, or negative interval."),
("**Fig 3. What classifiers trained on each label predict within TCGA.** Mean cross-validated AUC (three models, five repeats of five-fold cross-validation, 251 patients with RNA-seq data) for each training label (rows) against each label in held-out patients (columns).",
 "**Fig 3. What classifiers trained on each label predict within TCGA.** (A) Mean cross-validated AUC (three models, five repeats of five-fold cross-validation, 251 patients with RNA-seq data) for each training label (rows) against each label in held-out patients (columns); descriptive, because each label has its own patients and class balance. (B) Controlled comparison in the same 134 patients with the same folds: difference in AUC between training labels (mean of three models) with 95% bootstrap intervals that resample patients but do not refit models."),
("(blue; the 28 intervals below 1 day, 19 of them negative, set to 1 day)",
 "(blue; 408 patients at risk at the end of platinum, with an interval above 0 days)"),
]

# vocabulary (review point 2): (pattern, replacement, expected count after part 1)
V = [
("Strict combined label (recommended)", "Provenance-filtered combined label (recommended)", 1),
("strict combined label", "provenance-filtered combined label", 8),
("strict label", "provenance-filtered label", 3),
("the strict and broad combined labels", "the provenance-filtered and broad combined labels", 1),
("classed 78 as clean", "classed 78 as unflagged", 1),
("were classed clean if", "were classed unflagged if", 1),
("were never classed clean", "were never classed unflagged", 1),
("only in clean patients", "only in unflagged patients", 1),
("only for clean patients", "only for unflagged patients", 1),
("were not clean", "could not be classed unflagged", 1),
("78 were classed clean", "78 were unflagged", 1),
("rest on clean records", "rest on unflagged records", 1),
("with clean records", "with unflagged records", 1),
("a clean record", "an unflagged record", 1),
("the record is clean", "the record is unflagged", 1),
("clean resistant or sensitive", "unflagged resistant or sensitive", 1),
]


def main() -> None:
    s = P.read_text(encoding="utf-8")
    assert "\r" not in s
    for i, (a, b) in enumerate(T):
        n = s.count(a)
        assert n == 1, f"targeted {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    for a, b, k in V:
        n = s.count(a)
        assert n == k, f"vocabulary {a!r}: {n} matches, expected {k}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8")
    print(f"applied {len(T)} targeted edits and {len(V)} vocabulary patterns")


if __name__ == "__main__":
    main()

# Applied after the script above (2026-10-29, same session), as a one-line addition to manuscript_v5_src.md:
# after "…and the re-derived interval only in unflagged patients." the clause
# "(it is called the strict combined label in the analysis summaries in S1 Text, and label_combined_strict in the label table)"
# was inserted. Recorded here so the edit history stays complete.
