# A13 — Exploratory analyses of label structure (post hoc; no predictions)

## E1 Cohort flow

- PanCancer clinical patients: 585
- with any treatment-timeline record: 496
- no treatment-timeline record (excluded): 89; KM median OS 27.6 mo; determinate platinum status 5
- treatment record but no carboplatin/cisplatin (excluded): 7; KM median OS 51.4 mo; determinate platinum status 2
- platinum-treated cohort: 489; KM median OS 47.7 mo; determinate platinum status 277

## E2 Threshold sweep (reference: platinum status)

| t (mo) | n | sens [95% CI] | spec | PPV [95% CI] | κ (κmax) | Youden | PPV if no platinum information | spec if no platinum information | max sens allowed |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 276 | 0.02 [0.01, 0.08] | 1.00 | 1.00 [0.34, 1.00] | 0.03 (0.03) | 0.02 | 0.32 | 0.99 | 0.02 |
| 9 | 274 | 0.05 [0.02, 0.11] | 1.00 | 1.00 [0.51, 1.00] | 0.06 (0.06) | 0.05 | 0.31 | 0.99 | 0.05 |
| 12 | 274 | 0.10 [0.06, 0.19] | 1.00 | 1.00 [0.70, 1.00] | 0.14 (0.14) | 0.10 | 0.31 | 0.97 | 0.10 |
| 15 | 271 | 0.14 [0.08, 0.23] | 0.98 | 0.80 [0.55, 0.93] | 0.16 (0.23) | 0.13 | 0.31 | 0.94 | 0.18 |
| 18 | 268 | 0.21 [0.14, 0.31] | 0.98 | 0.82 [0.61, 0.93] | 0.24 (0.33) | 0.19 | 0.31 | 0.92 | 0.26 |
| 21 | 265 | 0.35 [0.25, 0.45] | 0.96 | 0.81 [0.65, 0.90] | 0.36 (0.51) | 0.31 | 0.32 | 0.86 | 0.43 |
| 24 | 259 | 0.39 [0.29, 0.49] | 0.94 | 0.74 [0.60, 0.85] | 0.37 (0.59) | 0.32 | 0.32 | 0.83 | 0.52 |
| 30 | 249 | 0.46 [0.36, 0.57] | 0.88 | 0.66 [0.53, 0.76] | 0.37 (0.76) | 0.34 | 0.33 | 0.77 | 0.71 |
| 36 | 243 | 0.64 [0.53, 0.74] | 0.83 | 0.65 [0.54, 0.75] | 0.47 (0.99) | 0.47 | 0.33 | 0.67 | 0.99 |
| 42 | 238 | 0.74 [0.64, 0.82] | 0.72 | 0.58 [0.48, 0.67] | 0.43 (0.80) | 0.46 | 0.34 | 0.56 | 1.00 |
| 48 | 233 | 0.85 [0.76, 0.91] | 0.63 | 0.54 [0.46, 0.63] | 0.42 (0.62) | 0.48 | 0.34 | 0.46 | 1.00 |
| 60 | 226 | 0.95 [0.88, 0.98] | 0.46 | 0.48 [0.41, 0.56] | 0.33 (0.40) | 0.41 | 0.35 | 0.31 | 1.00 |

## E3 OS-positive patients without a platinum status; bounds

- OS < 18 mo: 47 positive, of whom 25 undetermined (53%); PPV observed 0.82, bounds 0.38–0.91; sensitivity observed 0.21, bounds 0.09–0.39 (lower: undetermined OS-negative all resistant; upper: undetermined OS-positive all resistant)
- OS < 24 mo: 78 positive, of whom 35 undetermined (45%); PPV observed 0.74, bounds 0.41–0.86; sensitivity observed 0.39, bounds 0.17–0.57 (lower: undetermined OS-negative all resistant; upper: undetermined OS-positive all resistant)

## E4 Cox decomposition (HR [95% CI], p; n/events)

| covariate | PFI from platinum | survival after progression | OS |
|---|---|---|---|
| age10 | 1.08 [0.98, 1.19], p 0.114 (436/328) | 1.26 [1.12, 1.42], p 0.000174 (331/237) | 1.22 [1.10, 1.36], p 0.000241 (488/282) |
| stage_iv | 1.28 [0.96, 1.71], p 0.0904 (435/327) | 1.03 [0.74, 1.43], p 0.863 (331/237) | 1.30 [0.96, 1.74], p 0.085 (487/281) |
| residual_subopt | 1.11 [0.85, 1.44], p 0.45 (349/273) | 1.41 [1.03, 1.93], p 0.0311 (267/202) | 1.48 [1.12, 1.96], p 0.00532 (378/240) |
| resid_any | 1.67 [1.23, 2.26], p 0.000953 (349/273) | 1.66 [1.11, 2.48], p 0.0131 (267/202) | 2.21 [1.52, 3.21], p 3.07e-05 (378/240) |
| brca_carrier | 0.55 [0.38, 0.79], p 0.00132 (247/202) | 0.68 [0.44, 1.06], p 0.0904 (201/152) | 0.50 [0.34, 0.75], p 0.000778 (271/178) |
| ccne1_amp | 1.56 [1.19, 2.06], p 0.00143 (384/297) | 1.18 [0.86, 1.63], p 0.297 (294/218) | 1.46 [1.09, 1.95], p 0.0111 (421/260) |
| aneuploidy_sd | 1.20 [1.07, 1.35], p 0.00131 (418/313) | 1.03 [0.90, 1.17], p 0.706 (317/225) | 1.17 [1.04, 1.32], p 0.0109 (470/270) |

## E5 Clinical-only logistic regression (age, stage IV, residual > 1 cm), 5×5 CV

- label_platinum: AUC 0.479 (range 0.469–0.493); n 252 (82 positive)
- label_pfiplat6: AUC 0.517 (range 0.503–0.530); n 309 (96 positive)
- label_hybrid: AUC 0.487 (range 0.478–0.498); n 314 (95 positive)
- label_response: AUC 0.542 (range 0.510–0.561); n 334 (52 positive)
- label_os18_all: AUC 0.641 (range 0.620–0.653); n 327 (34 positive)
- label_os24_all: AUC 0.622 (range 0.607–0.632); n 317 (60 positive)

## E6 Any residual vs none (R0)

- label_platinum: 74/200 vs 8/52; OR 3.22 [1.40, 8.35], p 0.00269
- label_pfiplat6: 86/244 vs 10/66; OR 3.04 [1.44, 7.03], p 0.00152
- label_hybrid: 85/248 vs 10/67; OR 2.96 [1.41, 6.85], p 0.00246
- label_response: 44/265 vs 8/70; OR 1.54 [0.67, 3.99], p 0.355
- label_os18_all: 31/260 vs 3/68; OR 2.93 [0.87, 15.43], p 0.0763
- label_os24_all: 54/251 vs 6/67; OR 2.78 [1.12, 8.29], p 0.0216

## E7 Minimum detectable difference (80% power) for same-patient comparisons

- BRCA log OR: label_platinum − label_os18_all: estimate +1.12, SE 0.55, MDE 1.54 (ratio of ORs 4.7)
- BRCA log OR: label_platinum − label_os24_all: estimate +0.95, SE 0.82, MDE 2.31 (ratio of ORs 10.0)
- BRCA log OR: label_pfiplat6 − label_os24_all: estimate +0.85, SE 0.82, MDE 2.30 (ratio of ORs 10.0)
- Δ rank-biserial r: label_os18_all − label_platinum: estimate -0.06, SE 0.14, MDE 0.40
- Δ rank-biserial r: label_os24_all − label_platinum: estimate +0.11, SE 0.10, MDE 0.28
- Δ log OR (Haldane): label_os18_all − label_platinum: estimate +0.37, SE 0.49, MDE 1.37 (ratio of ORs 3.9)
- Δ log OR (Haldane): label_os24_all − label_platinum: estimate +0.50, SE 0.37, MDE 1.03 (ratio of ORs 2.8)

## E8 Excluding TCGA-CDR 'Redacted' patients from the re-derived interval

- Redacted among platinum-treated: 38; re-derived interval determinate 389 → 358 (108 resistant); κ with platinum status 0.964 (n 251)

