# Restructuring report: manuscript_v5_src.md → manuscript_v5_src_restructured.md

Inputs not modified (md5 of `manuscript_v5_src.md` unchanged). New files: `manuscript_v5_src_restructured.md`, `restructure_moved_to_S1Text.md`, `restructure_report.md`.

Checks: `python3 manuscript_v5/number_refs_v5.py manuscript_v5/manuscript_v5_src_restructured.md /tmp/test_out.md` runs and reports 45 references, with only `hanley` unused, as for the original. Title, author block, Abstract, everything from "Data and code availability" to the end (back matter, figure legends, all three tables, References heading, Supporting information list) and `[[ZENODO_DOI]]` are byte-identical to the original (checked by diff). No new numbers occur in the restructured main text (checked by script). `build_docx.py` was not run because it writes the existing .docx.

## 1. Word counts

Counting method: whitespace-separated tokens in section bodies, headings excluded. This gives 8,125 for the original Abstract→Conclusion, against the 8,232 quoted by the reviewer, so the counting conventions differ by about 1%.

| Section | Before | After | Target |
|---|---|---|---|
| Abstract (unchanged) | 299 | 299 | ≤ 300 |
| Introduction | 659 | 600 | ≤ 600 |
| Materials and methods | 3,322 | 2,299 | ≤ 2,300 |
| – Data and cohort | 150 | 124 | |
| – Labels | 1,016 | 675 | |
| – Coverage and agreement | 268 | 199 | |
| – Associations | 271 | 199 | |
| – Classifiers | 474 | 319 | |
| – Exploratory analyses | 382 | 210 | |
| – Supplementary analyses | 304 | 208 | |
| – Literature review | 96 | 95 | |
| – Pre-specification | 361 | 270 | |
| Results | 2,263 | 2,000 | ≤ 2,000 |
| – Studies label patients… | 140 | 140 | |
| – Platinum status covers… | 708 | 568 | |
| – OS thresholds agree… | 382 | 355 | |
| – Characteristics… | 417 | 358 | |
| – Exploratory: … | 179 | 178 | |
| – Classifiers trained… | 437 | 401 | |
| Discussion (incl. Limitations, Conclusion) | 1,582 | 1,300 | ≤ 1,300 |
| – Limitations | 437 | 349 | |
| – Conclusion | 136 | 136 | |
| **Total Abstract→Conclusion** | **8,125** | **6,498** | ≈ 6,500 |

Headings are unchanged except that the provenance audit now has its own run-in heading inside Labels ("*Provenance audit and combined labels.*"), and Classifiers has run-in headings "*All-patients analysis.*" and "*Controlled comparison.*". Only one A-number range remains in the main text (Pre-specification: "S1 Text gives each analysis's identifier (A1–A23)…"). The rest are replaced by descriptive names; `restructure_moved_to_S1Text.md` maps names to identifiers.

## 2. Numbers removed from the main text, and where each still appears

"Output 2" means `restructure_moved_to_S1Text.md` (to be added to S1 Text). Numbers that were only duplicated within the main text and still appear elsewhere in it are listed at the end.

### Methods
| Removed number (original context) | Still appears in |
|---|---|
| 27.6 months and 47.7 months (median OS of the 89 excluded patients vs the cohort; Data and cohort) | 27.6: Limitations (main text). 47.7 (cohort): S4 Table, sheet A13_cohort_flow (47.70). 47.7 still appears in Results as a different quantity (patients with a status) |
| Oxaliplatin anchors 3 patients, 2 with a determinate interval | S1 Text A18 (Note 2); Output 2 |
| Carboplatin/cisplatin-only anchor: no call changed; 2 undetermined, 1 of them among unflagged added patients | S1 Text A23 (C2–C3 table); S11 Table, sheet A23_anchor_checks; Output 2 |
| 60 of 389 with several adjuvant rows; 8 overlapping; 7 tied stop dates; 1 without stop date; 1 starting after a later-line regimen; 6 with other/no indication; 23 with no adjuvant row | S1 Text A18 (summary table); S11 Table, sheet A18_anchor_counts; Output 2 |
| Alternative anchors: first-regimen anchor labels 18 more patients; latest-before-later-line anchor leaves one undetermined | S1 Text A18 (determinate 407 vs 389; 388); S11 Table, A18_anchor_summary; Output 2 (verbatim) |
| Largest IPCW weight 1.24, none truncated | Output 2 (S1 Text A23 prints max weights, e.g. 1.235) |
| scikit-learn 1.7.2; Python 3.14.5, NumPy 2.4.6; Python 3.10; R 4.6.0, survival 3.8.6; lifelines 0.30.0 (scikit-learn 1.9.0 is kept in Classifiers) | Output 2 (Software environments); S1 Text A3 part 2, A13b, A20 and A22 summaries print versions |
| SVM Platt scaling "five-fold" | Output 2 |
| A22: all 500 samples valid, none single-class | S1 Text A22 (usable_replicates 500; skipped 0); Output 2 |
| Decomposition exclusions: 19 negative intervals (8 with an event, 11 censored), 9 of 0 days (4 / 5); 53 without an interval (52 + 1); 436 entering | S1 Text A13b ("Patients with an interval: 436; excluded … 28 (events 12, censored 16)"); S10 Table A13b_decomposition (n 436); Output 2. (8 and 11 also remain in Labels) |
| GPL570; hgu133plus2.db | S7 Table README; Output 2 |
| Lisowska/GEO reconciliation: 97, 72, 62, 10, 33 (publication); 101 (series); 74; 2 more responders, 1 more resistant; Chen et al. 75 (34/41) | Output 2 (verbatim). 101, 74 and the Chen 34/41 reconstruction are also in S7 Table (sheet GSE63885_label_definitions); 34/41 is in Table 1 (Chen row). The main text points to S1 Text for the reconciliation |
| A-number groupings of the three specification levels (A1–A7; A8–A10, A15, A16; A13b, A18, A19, A21, A23, A22; A20) | Output 2 ("Analyses by level of specification"); S1 Text status lines |

### Results
| Removed number | Still appears in |
|---|---|
| CIs 0.92–3.09 (OR 1.70), 1.41–4.91 (OR 2.63), 0.23–0.96 (OR 0.49), patients without a status | S4 Table, sheet A9_group_tests (0.916–3.089; 1.413–4.908; 0.232–0.961). The ORs and counts stay in the main text |
| κ 0.964 vs 0.966 (without/with redacted records); replaced by "with almost unchanged κ" | S10 Table, A13_redaction (0.9638); 0.966 in S1 Text A18/A21 and S11 A21_event_type; Output 2 |
| Broad combined label 394 (113 resistant); OS 18 months 419 (47); OS 24 months 401 (78) | Table 2; S2 Table A11_coverage |
| 13 recurrences, 3 progressions, 4 unrecorded (among the 20 added resistant calls) | S11 Table, A15b_event_source; Output 2 |
| 90 / 15 / 4 / 6 of 115 resistant calls | S11 Table, A15b_event_source; Output 2 (115 also in Table 2) |
| "three adjuvant platinum rows" (101-day discordant patient) | S11 Table, A20_discordant_patients (adj_platinum_rows 3); Output 2 |
| The 10 set-aside calls had no platinum status, so κ was unaffected | S11 Table, A21_event_type (n_with_platinum 272, κ identical); Output 2 |
| OS thresholds vs the provenance-filtered label: sensitivity 0.23 and 0.41, PPV 0.79 and 0.75, "within 0.05" of broad | S11 Table, A15b_os_test_strict (0.234, 0.409, 0.786, 0.745); Output 2 |
| Censored before threshold in the cohort: 69 and 87 | S2 Table, A19_ipcw (censored_before_t); Output 2 |
| 1 further patient without a recorded survival time | **Output 2 only** (not found in an existing S table) |
| Cox censoring weights excluded 23 patients | S1 Text A23 ("A19 Cox-variant exclusions … {18: 23, 24: 23}"); S2 Table A19_ipcw (n 268→245, 259→236); Output 2 |
| Same-patient contrasts: aneuploidy −0.06 (−0.35 to +0.21), +0.11 (−0.09 to +0.31); residual > 1 cm +0.37 (−0.66 to +1.25), +0.50 (−0.23 to +1.21) | S5 Table, A10_same_patient_diff; estimates also in S3 Table A13_min_detectable |
| 18-month OS positives: 3 to 7 per training fit, none in 22 of 100 held-out folds | S1 Text A20 (C1); S6 Table A20_A16_fold_counts; Output 2 |
| Mean of per-repeat differences −0.016 | S1 Text A16 summary; Output 2 |
| Duplicate of first-course *BRCA1/2* OR 0.64 (0.18–1.80) | Still once in Results and in Table 3 |

### Discussion
| Removed number | Still appears in |
|---|---|
| Somatic-only *BRCA1/2*: 12 carriers with an OS label; 44 of 55 germline | 12: S3 Table A8_tests (somatic_pancan_A3, exp_n 12); Output 2. 44/55: Methods (main text) |
| "134 patients (39 resistant)" in the classifier paragraph | Results (main text), Abstract, Fig 3 legend |
| Provenance-filtered 167 (43 resistant) in Limitations | Results (main text); Table 2 |

## 3. Citations

No citation dropped: all 45 references used in the original remain (`hanley` was already unused). Citations moved:
- The Methods background sentence on *BRCA1/2* and *CCNE1* (pennington, yang, etemad) was removed; the same claim with the same three citations remains in the Discussion, so reference numbering changes.
- The TCGA-2011 citation for "germline variants account for most *BRCA1/2* alterations in HGSOC" left the main text with that sentence (now in Output 2). `tcga2011` is still cited elsewhere.
- The Discussion repetition of Cocchi et al.'s finding (also stated in the Introduction) was removed; `cocchi` is still cited in both places.
- The Lisowska count reconciliation moved to Output 2, written there as "[Lisowska et al.]". It needs S1 Text's citation format when inserted. `lisowska` is still cited in Methods.

## 4. Places where shortening may have changed meaning (please check)

1. **Pointer that depends on Output 2.** Supplementary analyses now says "S1 Text reconciles these counts with the original publication and with Chen et al." This is true only once Output 2 is added to S1 Text. The same applies to "software environments and development history" in Pre-specification. The anchor/oxaliplatin, decomposition-exclusion and "1 further patient" details are already in S1 Text summaries, except "1 further patient", which is only in Output 2.
2. **Platinum status definition.** The phrase "TCGA measured the platinum-free interval from the last primary platinum dose" was removed. The quotation and Table 2 ("from last primary platinum dose") keep the reference point.
3. **Pre-specification levels.** Level 1 is no longer enumerated in the main text. Level 2 is "the five deposited analyses". Post hoc analyses are named descriptively, and "(A22) with one prediction" was dropped. The A-number lists are in Output 2. The four-item structure ("three levels … alongside exploratory or descriptive analyses") follows the original.
4. **Exploratory analyses opener.** Now "Three analyses were exploratory (see Pre-specification)"; Pre-specification states that "the descriptive full-cohort tables and the exploratory analyses were added after the main results were known". "At the request of internal reviewers" moved to Output 2. The sentence listing the threshold sweep, bounds, minimum detectable differences and alternative residual coding as added "at the same time" was removed. Each is still marked exploratory where described (Coverage and agreement; Associations; Table 3 footnote).
5. **Use of the provenance-filtered label.** Methods no longer says it "is used in the label table and in the evaluation of OS thresholds against a combined reference; the other analyses use … as stated". Results instead points to S11 Table for its OS-threshold test characteristics.
6. **Results, redaction.** "κ 0.964 versus 0.966" became "with almost unchanged κ" (numbers in S10/S11).
7. **Results, missing status.** CIs were removed for three of the four comparisons (S4 Table) but kept for the 18-month one, which reads slightly inconsistently.
8. **Discussion, classifier paragraph.** "In those 134 patients (39 resistant), the conditional interval spans …" became "given the conditional interval (−0.105 to +0.087) and the wider variation of single refits …".
9. **Limitations.** The clause that the out-of-bag refits "estimate a different quantity" was removed there; it remains in Methods and Results. "The 150–215-day flag removes borderline patients whose records may be correct" is now split: the borderline-removal half is in the Recommendations, the representativeness half in Limitations. Only one failed prediction is now given as an example ("platinum-trained classifiers would predict platinum status better …"); the *BRCA1/2* example moved to Output 2.
10. **Recommendations.** "This is a conservative extension: the accuracy of the added calls is not verified" was removed from the Discussion; the same statement is in Methods. "Not a label shown to be more accurate" and the borderline-patients caveat are kept.
11. **Introduction.** "Most patients respond initially" was removed ("Many patients relapse…"), as was "In measurement terms".
12. **Methods, first sentence.** "for TCGA-OV" was dropped (the study identifiers follow). In Exploratory analyses, "Times were TCGA-CDR days from diagnosis (PFI.time, OS.time) and treatment-timeline stop dates" moved to Output 2; the PFI definition still says "both in days from diagnosis".
13. **Coverage and agreement.** The IPCW variants (censoring distribution estimated in patients with a status and within status groups) are now described only in Results, where their effect (≤ 0.01) is reported.
14. **Output 2 overlaps S1 Text.** It partly repeats the existing "Analysis history" paragraph at the top of S1 Text (A15/A15b deviation, header time strings, A22 bug). Merge rather than append.
