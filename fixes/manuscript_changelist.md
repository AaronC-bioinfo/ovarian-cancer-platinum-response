# Manuscript change list — PLOS_CompBio_Draft_Chintala_v1

**Redline file:** `PLOS_CompBio_Draft_Chintala_v1_redline.docx` (project root)
**Original:** `C:\Users\AMAC_WORK\Downloads\PLOS_CompBio_Draft_Chintala_v1.docx` — **untouched**
(never opened in this pass; the Downloads folder was never mounted).
**All edits are Word tracked changes** under author **`Cowork-audit`**.
Pass 1 edits carry date `2026-07-20`; pass 2 edits (this pass) carry date `2026-08-20`.
Validated: `office/validate.py --author "Cowork-audit"` → *All validations PASSED*, 165 → 165
paragraphs, no untracked edits. **Nothing was accepted.**

Legend: **REAL** = final corrected value, now filled from the author's Windows re-run;
**CONFIRMED** = value in the draft was already right, the pending flag was simply rejected;
**AUTHOR DECISION** = flagged for the author, argument deliberately *not* rewritten.

## Pass 2 — 2026-08-20 (this pass)

Source of every value below: the author's own Windows re-run (Python 3.14 / scikit-learn
1.9.0, R 4.6.0), verified by Cowork against the on-disk CSVs before editing.

| # | Location | Old | New | Kind | Source file |
|---|---|---|---|---|---|
| 1 | Table 2, Random Forest, 12m | `[COWORK: pending re-run]` | **0.400** | REAL | `outputs/results/clean_auc_table.csv` (0.4004) |
| 2 | Table 2, Random Forest, 18m | `[COWORK: pending re-run]` | **0.628** | REAL | same (0.6277) |
| 3 | Table 2, Random Forest, 24m | `[COWORK: pending re-run]` | **0.716** | REAL | same (0.7157) |
| 4 | Table 2, SVM (RBF), 12m | `[COWORK: pending re-run]` | **0.405** | REAL | same (0.4045) |
| 5 | Table 2, SVM (RBF), 18m | `[COWORK: pending re-run]` | **0.619** | REAL | same (0.6191) |
| 6 | Table 2, SVM (RBF), 24m | `[COWORK: pending re-run]` | **0.733** | REAL | same (0.7333) |
| 7 | Results, external validation | "r = −0.005" | **r = −0.007** | REAL | `validation/outputs/combat_diagnostics.csv` (−0.0071670) |
| 8 | Discussion, external validation | "r = −0.005" | **r = −0.007** | REAL | same |
| 9 | Abstract, Cox | "concordance index 0.570–0.588" + pending flag | value kept, **flag rejected** | CONFIRMED | `phase2/outputs/cox_summary_stats.csv` (0.5698) + `hrd/brca_cox_summary.csv` (0.5885) |
| 10 | Results, Cox KM | "log-rank p=0.023" + pending flag | value kept, **flag rejected** | CONFIRMED | `phase2/outputs/cox_summary_stats.csv` (0.023423) |
| 11 | Results, BRCA | "n=335 matched subset" + pending flag | value kept, **flag rejected** | CONFIRMED | `hrd/brca_cox_summary.csv` (n_matched_subset = 335) |
| 12 | Results, Enhancement 5, α | "α=0 (pure ridge …" + pending flag | rewritten: α=0 (ridge) is a property of the **FINAL** Cohort B model on the full n=163 cohort; **only 8 of 25** outer CV folds selected α=0 | REAL | `enhancement5/outputs/final_model_alpha.csv` (CohortB = 0) + `enhancement5/outputs/alpha_selection_summary.csv` (8/25) |
| 13 | Results, external validation | "(ratio 1.00)" + pending flag | value **left at 1.00**; pending flag replaced by `[COWORK: AUTHOR DECISION …]` | AUTHOR DECISION | `validation/outputs/combat_diagnostics.csv` (3.7039) |
| 14 | Abstract, "…rather than model or feature choice" | — | `[COWORK: AUTHOR DECISION …]` inserted | AUTHOR DECISION | same — this inference rests on the ~1.00 claim |
| 15 | Methods, external validation | — | `[COWORK: AUTHOR DECISION …]` inserted | AUTHOR DECISION | same — Methods describes the comparison that yields 3.70x |
| 16 | Results, ribosomal theme | `[COWORK: confirm framing …]` | **unchanged, left in place** | AUTHOR DECISION | `fixes/phase4_corrected_values.csv` |

Values **verified but not edited** (draft already correct): BRCA HR 0.455 / p=0.024 and
C-index 0.573 → 0.588, checked against `hrd/cox_hazard_ratios_brca.csv`
(HR 0.455287, p 0.023824, c-index 0.573149 → 0.588457).

Tracked-change totals in the redline XML after pass 2: **31 `<w:ins>`**, **26 `<w:del>`**,
all authored `Cowork-audit`. Pass-1 flags that are now obsolete were **rejected in place**
(a `<w:del>` nested inside the original `<w:ins>`) rather than deleted outright, so the full
audit trail of what was flagged and when survives in the markup.

## Pass 1 — 2026-07-20 (unchanged, for reference)

| # | Location | Old | New | Kind | Source |
|---|---|---|---|---|---|
| 1 | Table 2, Logistic Regression, 12m | 0.542 | **0.457** | REAL | `outputs/results/clean_auc_table.csv`; `fixes/phase1_provenance.md` |
| 2 | Table 2, Logistic Regression, 18m | 0.658 | **0.669** | REAL | same |
| 3 | Table 2, Logistic Regression, 24m | 0.712 | **0.678** | REAL | same |
| 4–9 | Table 2, RF & SVM (6 cells) | 0.411 / 0.609 / 0.709 / 0.363 / 0.515 / 0.771 | `[COWORK: pending re-run]` | PENDING | now resolved — see pass 2, items 1–6 |
| 10 | Results, feature-importance | "ρ ≈ 0.37–0.41" | ρ ≈ **0.37–0.42** | REAL | `phase2/outputs/cv_comparison_spearman_without12m.csv` (0.4188) |
| 11 | Results, EMT anchors | "FLNA did not rank as important under any method or condition tested" | + " **(rank 299–508 across all methods and thresholds)**" | REAL (insertion) | `phase2/outputs/cv_{shap,mdi,permutation}_importances_full.csv` |
| 12 | Results, ribosomal theme | "…significance from a gene-list size of 200 onward" | + note: significant at top-100 **without** 12m (adj p=0.020) + `[COWORK: confirm framing]` | FRAMING (insertion) | `fixes/phase4_corrected_values.csv`; `shap_theme_comparison.csv` |
| 13–18 | Six R-derived values | — | `[COWORK: pending Windows re-run]` | PENDING (R) | all resolved in pass 2 |

## Notes for the author

- **LR row is final.** Logistic Regression is deterministic and reproduced exactly across
  three independent runs a month apart; 0.457 / 0.669 / 0.678 can be published as-is.
- **RF/SVM are now final** at 0.400/0.628/0.716 and 0.405/0.619/0.733, and `requirements.txt`
  pins `scikit-learn==1.9.0` so they are reproducible. Note the direction of travel: RF and
  SVM both *fell* at 12m and 18m and *rose* at 24m relative to the pre-audit draft.
- **The variance-ratio contradiction is the one substantive open item.** The manuscript
  asserts a ratio of ~1.00 and uses it to rule out feature selection as the cause of external
  validation failure. The computed value is 3.70x, which does not support that inference.
  Three sentences are flagged (Abstract, Methods, Results). Cowork did **not** rewrite the
  argument — this needs the author and Lockhart.
- **`[COWORK: confirm framing]` on the ribosome sentence** remains an inline tracked insertion
  rather than a Word margin comment (the comment helper cannot write its auxiliary files in
  the audit sandbox). Fully visible in Word's markup view.
- Numbers **not** changed because they were already verified against committed outputs:
  Aneuploidy HR 1.021 (CI 1.004–1.039, p=0.017), TMB HR 0.894, Schoenfeld global p=0.178,
  median OS 52.0/51.9/39.4, BRCA 33/409 (8.1%), HR 0.455 p=0.024, C-index 0.573→0.588,
  SHAP–MDI ρ=0.98, Enh5 Table 3 C-indices, recall 0/5 CI [0.000, 0.522].
