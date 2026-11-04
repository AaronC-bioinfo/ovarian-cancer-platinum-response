#!/usr/bin/env python3
"""
manuscript_v5/apply_review4_round5_2026-10-30.py
Round 5: response to the fourth (in-depth) review (2026-10-29, ~23:50 ET). Exact replacements; each must match once.
Sources:
- primary-source checks of the cited papers (verbatim quotes from the PDFs in OV Data/Project data/Literature and
  PMC; recorded in PROJECT_LOG);
- A18 18_anchor_sensitivity_summary.md / a18_anchor_counts.csv;
- A19 19_ipcw_os_thresholds_summary.md / a19_ipcw.csv;
- A20 20_documentation_checks_summary.md (a20_a16_fold_counts.csv, a20_discordant.csv, a20_cox_checks.csv);
- a15b_resistant_event_source.csv; validation/GSE63885_label_definitions.md; validation/04_probe_mapping.R;
- 08/10 scripts (Haldane +0.5); 16 script (per-model AUC differences averaged).
Run from manuscript_v5/: python apply_review4_round5_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
# ── abstract (review points 1, 2, 10; "every label") ──
("The re-derived interval agreed with it closely (κ 0.97); a patient-level audit of the 117 patients it added classed 78 as unflagged, and a provenance-filtered combined label that adds only those covered 355 patients",
 "The re-derived interval agreed closely with it where both were available (κ 0.97); a patient-level audit of the 117 patients it added classed 78 as unflagged, and a provenance-filtered candidate extension that adds only those covered 355 patients"),
("Expression classifiers predicted every label modestly (AUC 0.61–0.68);",
 "Expression classifiers trained on four of the labels predicted them modestly (AUC 0.61–0.68);"),
("Studies should state the label definition and class sizes, prefer platinum-specific labels, and treat OS thresholds as survival end-points rather than platinum-response labels.",
 "Studies should state label definitions and class sizes, prefer platinum-specific labels, document provenance, and treat OS thresholds as survival end-points."),
# ── introduction (source corrections; points 7–9) ──
("Survival-defined groups have been used as proxies for chemoresistance, for example short-term survivors with resistant disease [@yangsyc],",
 "Composite groups that combine a survival window with platinum resistance have also been used, for example short-term survivors defined by overall survival of 6 months to 2 years, primary platinum resistance and progression within six months of completing platinum [@yangsyc],"),
("None of the TCGA-OV studies we reviewed used an OS threshold (Table 1);",
 "None of the TCGA-OV studies in our non-systematic review used an OS threshold (Table 1);"),
("most closely, Cocchi et al. cross-tabulated re-derived platinum-free-interval categories against TCGA's platinum status and showed that patient selection and interval definitions change the genes reported [@cocchi]; the TCGA-CDR recommends the progression-free interval as generally more informative than OS in pan-cancer analyses [@liu],",
 "most closely, Cocchi et al. compared platinum-free-interval categories derived from that re-annotation with the original TCGA annotation and showed that patient selection, platinum-sensitivity definitions, data sources and analytical pipelines change the genes reported [@cocchi]; the TCGA-CDR considers the progression-free interval generally the more informative end-point in pan-cancer analyses while recommending all four of its end-points, including OS, for TCGA-OV [@liu],"),
("To our knowledge, however, no study has quantified agreement", "In the literature we reviewed, however, no study had quantified agreement"),
("compared what classifiers trained on each label learn,", "compared which outcomes classifiers trained on each label predict,"),
# ── methods: labels (points 1, 3, 4) ──
("minus the stop date of the last platinum regimen recorded with an adjuvant indication, both measured in days from diagnosis.",
 "minus the stop date of the last platinum regimen recorded with an adjuvant indication, both measured in days from diagnosis. Platinum rows were treatment-timeline rows with carboplatin or cisplatin as the agent; no platinum row carried a neoadjuvant indication. When several adjuvant platinum rows were recorded (60 of the 389 patients with a determinate interval, 8 of them with overlapping rows and 7 with tied stop dates), the latest stop date was used. With alternative anchors — the earliest adjuvant stop date, the end of the first platinum regimen whatever its indication, or the latest adjuvant stop date before any later-line regimen — 0 to 5 of the 389 calls changed (κ with the primary label at least 0.97; S1 Text, analysis A18)."),
("By a rule fixed before the audit was run, the provenance-filtered label became the recommended label, and the broad label a sensitivity analysis, because more than 20% of the added patients could not be classed unflagged.",
 "By a rule fixed before the audit was run, the provenance-filtered label became the preferred of the two combined labels, and the broad label a sensitivity analysis, because more than 20% of the added patients could not be classed unflagged; it is a candidate extension, not a label shown to be more accurate."),
("The provenance-filtered label is used for the recommendation, the label table and the evaluation of OS thresholds against a combined reference;",
 "The provenance-filtered label is used in the label table and in the evaluation of OS thresholds against a combined reference;"),
# ── methods: coverage (point 6) ──
("and bounds on sensitivity and PPV obtained by assigning all OS-labelled patients without a status to resistant or to sensitive.",
 "and bounds on sensitivity and PPV obtained by assigning all OS-labelled patients without a status to resistant or to sensitive. Because patients censored before a threshold have no OS label, the same measures were re-estimated with inverse-probability-of-censoring weights (Kaplan–Meier, and a Cox model of censoring on age, stage IV and residual disease) [@vock] (S1 Text, analysis A19)."),
# ── methods: associations (point 15) ──
("were estimated with 95% intervals from 2,000 bootstrap resamples.",
 "were estimated with 95% intervals from 2,000 bootstrap resamples; 0.5 was added to every cell of each table (Haldane correction), so no resample was discarded."),
("The smallest difference detectable with 80% power was derived from each interval in an exploratory analysis added after review.",
 "The smallest difference detectable with 80% power was derived approximately from each interval in an exploratory analysis; it describes sensitivity, not power."),
# ── methods: classifiers (points 11, 12) ──
("We report the mean AUC over three models and five repeats and its range.",
 "We report the mean AUC over three models and five repeats and its range; these AUCs describe which outcomes the classifiers predict, not what biological information they use."),
("averaged over the three models. Its 95% interval",
 "averaged over the three models; each model's difference was computed from its own predicted probabilities, which were never pooled across models. Its 95% interval"),
# ── methods: exploratory Cox (point 16) ──
("A model that sets those intervals to 1 day is reported as a sensitivity analysis (S10 Table).",
 "A model that sets those intervals to 1 day is reported as a sensitivity analysis (S10 Table). Times were TCGA-CDR days from diagnosis (PFI.time, OS.time) and treatment-timeline stop dates. A rank-based test of proportional hazards gave P < 0.05 in 2 of the 14 models (age for the platinum-free interval, Aneuploidy Score for survival after progression), and an added quadratic term did not improve the fit for either continuous covariate (P ≥ 0.28; S1 Text, analysis A20)."),
# ── methods: supplementary analyses (points 13, 14) ──
("transfer of the TCGA-trained classifiers to an independent microarray cohort, GSE63885 [@lisowska]; the 10 genes of Chen et al.",
 "transfer of the TCGA-trained classifiers to an independent microarray cohort, GSE63885 [@lisowska]; a gene-set transfer experiment, in which the 10 genes of Chen et al."),
("used as fixed inputs to the same pipeline and compared with 1,000 random gene sets of the same size;",
 "used as fixed inputs to our pipeline and compared with 1,000 random gene sets of the same size (both sets were selected in data that included TCGA-OV patients, which favours them in TCGA, and the experiment neither replicates nor tests the original models);"),
# ── methods: literature review (point 9) ──
("identified in an initial literature search and an additional targeted search (neither systematic)",
 "identified in an initial literature search and an additional targeted search (neither systematic; databases, dates and search terms were not recorded, so the selection cannot be reproduced and \"none\" below means none in this sample)"),
# ── methods: pre-specification levels (point 17) ──
("the other headers are archived with the code but were not timestamped externally.",
 "the other headers are archived with the code but were not timestamped externally. Three levels of specification apply: predictions for the initial label analyses (A1–A7), written before those analyses but after the authors' earlier work on the same cohort; secondary predictions written after earlier results of this study had been seen (A8–A10, A15, A16), which may have been informed by them; and exploratory analyses without predictions. No hypothesis was fixed before any inspection of TCGA-OV data, and commit timestamps establish only the order of writing and running."),
# ── results: provenance (points 2, 4) ──
("One of the four had an interval near the cut-off (154 days); the other three (18, 101 and 148 days) had a recorded recurrence and no flag, so the available records do not explain the disagreement.",
 "One of the four had an interval near the cut-off (154 days); the other three (18, 101 and 148 days) had a recorded recurrence and no flag, and one of these (101 days, three adjuvant platinum rows) became sensitive under the alternative anchors, so two disagreements remain unexplained by the available records (S11 Table). Across all 115 resistant re-derived calls, 90 were dated by a recorded recurrence, 15 by a recorded progression, 4 by a new tumour event of unrecorded type and 6 by a death counted as progression."),
("and is the label we recommend;", "and is the preferred of the two combined labels under the pre-specified rule;"),
("The published and re-derived platinum labels agreed in 268 of 272 patients",
 "Where both were available, the published and re-derived platinum labels agreed in 268 of 272 patients"),
# ── results: OS as tests (points 5, 6, source) ──
("The informative quantity is the PPV: of the flagged patients with a determinate status,",
 "The PPV is informative alongside these values: of the flagged patients with a determinate status,"),
("and between 0.41 and 0.86 at 24 months.",
 "and between 0.41 and 0.86 at 24 months. These values also exclude the 69 and 87 patients censored before each threshold; with inverse-probability-of-censoring weights, sensitivity, specificity and PPV changed by at most 0.04 (S1 Text), but weighting assumes censoring unrelated to outcome given age, stage and residual disease, and it does not address missing platinum status."),
# ── results: classifiers (points 12, 13) ──
("The corresponding difference for 18-month-OS-trained models, which had only 7 positives, was",
 "The corresponding difference for 18-month-OS-trained models, which had only 7 positives (3 to 7 per training fit, and none in 22 of the 100 held-out folds), so that this comparison is particularly unstable, was"),
("As fixed inputs to the same pipeline, the 10 genes of Chen et al.", "In the gene-set transfer experiment, the 10 genes of Chen et al."),
# ── discussion (points 1, 2, 10, 13; source) ──
("but at no cut-off do they agree better than moderately with platinum status.",
 "but at no examined cut-off between 6 and 60 months do they agree better than moderately with platinum status."),
("Within TCGA, expression predicted every label with cross-validated AUCs near", "Within TCGA, expression predicted each training label with cross-validated AUCs near"),
("inflated AUC by about 0.2 here.", "inflated AUC by about 0.2 in our pipeline, which shows that it can inflate such figures but not that it explains any particular published result."),
("Villalobos et al. re-annotated the cohort's treatment outcomes and found median overall survival of 27 months in platinum-resistant patients [@villalobos], which fits our finding that most resistant patients survive beyond the usual OS thresholds;",
 "Villalobos et al. re-annotated the cohort's treatment outcomes into platinum-sensitive, -resistant and -refractory groups (212, 91 and 28 patients) and found median overall survival of 27.0 months in patients whose disease recurred 1–6 months after the last platinum dose and 11.6 months in refractory patients [@villalobos]; our resistant category includes both, and the longer of these medians fits our finding that many resistant patients survive beyond the usual OS thresholds;"),
("showed that platinum-free-interval definitions alone change which genes TCGA-OV studies report [@cocchi].",
 "showed that patient selection, platinum-sensitivity definitions, data sources and analytical pipelines all change which genes TCGA-OV studies report [@cocchi]. Our label table differs from both in its sources (the TCGA-CDR progression-free interval and the PanCancer Atlas treatment timeline), in recording the provenance and flags of each re-derived call, and in placing platinum, survival and response labels side by side in the same patients; it does not supersede their annotations."),
("and where both labels are available they agree closely.",
 "and where both labels are available they agree closely, which shows consistency with the published reference rather than accuracy in the patients without it."),
("Prefer a platinum-specific label. Where TCGA's platinum status is missing, extend it with the platinum-free interval re-derived from TCGA-CDR only where the record is unflagged, as in the provenance-filtered combined label we release (S11 Table), and report each patient's provenance.",
 "Prefer a platinum-specific label. If TCGA's platinum status is extended with the platinum-free interval re-derived from TCGA-CDR, document the provenance of each added call and report results with and without the added patients; the provenance-filtered candidate extension we release (S11 Table) is one such option, not a label shown to be more accurate."),
# ── limitations (points 2, 6; source) ──
("All analyses use one resource, and platinum status is available",
 "The label analyses use one resource (TCGA-OV), with GSE63885 used only for external transfer, and platinum status is available"),
("and it does not explain the three disagreements with unflagged records.",
 "and two disagreements with unflagged records remain unexplained."),
("Excluding patients censored before an OS threshold can bias threshold labels [@vock].",
 "Excluding patients censored before an OS threshold can bias threshold labels [@vock]; a weighted analysis changed the estimates little, but it rests on assumptions about censoring that cannot be checked."),
# ── conclusion (source) ──
("Expression predicts all of the labels modestly,", "Expression predicts each of the four training labels modestly,"),
# ── figure legends, table 2 (point 1) ──
("the provenance-filtered combined label (recommended) adds re-derived calls only for unflagged patients.",
 "the provenance-filtered combined label (preferred under the pre-specified rule) adds re-derived calls only for unflagged patients."),
("| Provenance-filtered combined label (recommended) |", "| Provenance-filtered combined label (candidate extension) |"),
# ── table 1 (source checks) ──
("| AUC 0.752 (PTRC → TCGA), 0.613 (TCGA CV) |", "| AUC 0.752 (PTRC → TCGA), 0.835 (TCGA → PTRC), 0.613 (TCGA five-fold CV); multimodal, primary tumours |"),
("| 287 TCGA in a pooled 404 (pooled counts as printed: 71 sensitive / 333 resistant) | GSE63885, n = 75 | Random 8:2 split of pooled data; five-fold CV for hyperparameters |",
 "| 287 TCGA in a pooled 404 from four datasets, including the GSE63885 validation set (pooled counts as printed: 71 sensitive / 333 resistant) | GSE63885, n = 75 | Random 8:2 split of TCGA, GSE15622 and GSE51373 (GSE63885 held out); five-fold CV for hyperparameters |"),
("| TCGA AUCs not reported numerically |", "| TCGA AUCs not reported numerically in the main text or Fig 4 |"),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()

# Applied after the script above (2026-10-30, same session), to the S-list in manuscript_v5_src.md:
#   'S8 Table. Published gene sets as fixed inputs, with the random-gene-set null distribution.'
#   -> 'S8 Table. Gene-set transfer experiment: published gene sets as fixed inputs, with the random-gene-set null distribution.'
#   'S2 Table. Pairwise agreement and OS-threshold test characteristics: full cohort, patients with RNA-seq data, against the combined label, and at every threshold from 6 to 60 months.'
#   -> 'S2 Table. Pairwise agreement and OS-threshold test characteristics: full cohort, patients with RNA-seq data, against the combined label, at every threshold from 6 to 60 months, and with inverse-probability-of-censoring weights.'
#   'provenance class, event source and flags for the 489 platinum-treated patients, with a data dictionary and class counts.'
#   -> 'provenance class, event source and flags for the 489 platinum-treated patients, with a data dictionary, class counts, the four discordant patients and the treatment-anchor sensitivity analysis.'
