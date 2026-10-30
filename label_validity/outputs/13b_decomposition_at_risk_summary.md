# A13b — Cox decomposition with the platinum-free interval restricted to patients at risk at the end of platinum

Python 3.10.12; lifelines 0.30.0; pandas 2.3.3; numpy 2.2.6

Patients with an interval: 436; excluded from the at-risk model (interval ≤ 0 days): 28 (events 12, censored 16).

Reproduction of A13 (analysis, covariates matched, max |ΔHR|, n identical): clipped_as_A13: 7, 2.22e-16, True; unchanged: 7, 0.00e+00, True

| covariate | PFI, at risk (primary) | PFI, clipped as A13 (sensitivity) | survival after progression |
|---|---|---|---|
| age10 | 1.09 [0.98, 1.20], p 0.0993 (408/316) | 1.08 [0.98, 1.19], p 0.114 (436/328) | 1.26 [1.12, 1.42], p 0.000174 (331/237) |
| stage_iv | 1.29 [0.96, 1.73], p 0.0895 (407/315) | 1.28 [0.96, 1.71], p 0.0904 (435/327) | 1.03 [0.74, 1.43], p 0.863 (331/237) |
| residual_subopt | 1.08 [0.82, 1.41], p 0.599 (322/261) | 1.11 [0.85, 1.44], p 0.45 (349/273) | 1.41 [1.03, 1.93], p 0.0311 (267/202) |
| resid_any | 1.64 [1.21, 2.23], p 0.00158 (322/261) | 1.67 [1.23, 2.26], p 0.000953 (349/273) | 1.66 [1.11, 2.48], p 0.0131 (267/202) |
| brca_carrier | 0.55 [0.38, 0.79], p 0.00141 (236/195) | 0.55 [0.38, 0.79], p 0.00132 (247/202) | 0.68 [0.44, 1.06], p 0.0904 (201/152) |
| ccne1_amp | 1.58 [1.19, 2.09], p 0.00145 (356/285) | 1.56 [1.19, 2.06], p 0.00143 (384/297) | 1.18 [0.86, 1.63], p 0.297 (294/218) |
| aneuploidy_sd | 1.23 [1.10, 1.38], p 0.000373 (390/301) | 1.20 [1.07, 1.35], p 0.00131 (418/313) | 1.03 [0.90, 1.17], p 0.706 (317/225) |

Decision rule — covariates whose PFI 95% CI excludes 1 in one model but not the other: none
