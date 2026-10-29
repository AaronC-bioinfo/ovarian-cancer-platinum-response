# A3 part 1 — known-groups validity

Platinum-treated patients (A1 cohort) with label and covariate non-missing. OR = odds of label = 1 (non-responder/resistant) when the covariate = 1. r > 0 = higher values in label = 1. BH within each label (6 tests).

```
         label       covariate   n  n_label1          effect  estimate  ci_lo  ci_hi     p  q_bh_within_label
label_platinum        brca_mut 191        59              OR     0.000  0.000  0.535 0.003              0.020
label_platinum        stage_iv 277        87              OR     1.016  0.456  2.166 1.000              1.000
label_platinum residual_subopt 252        82              OR     1.116  0.586  2.090 0.762              0.914
label_platinum      aneuploidy 265        82 rank-biserial r     0.125    NaN    NaN 0.103              0.207
label_platinum             tmb 255        79 rank-biserial r    -0.157    NaN    NaN 0.043              0.130
label_platinum             age 277        87 rank-biserial r     0.072    NaN    NaN 0.337              0.505
label_pfiplat6        brca_mut 272        82              OR     0.000  0.000  0.332 0.000              0.001
label_pfiplat6        stage_iv 388       115              OR     1.088  0.567  2.028 0.762              0.762
label_pfiplat6 residual_subopt 310        96              OR     1.251  0.709  2.184 0.415              0.498
label_pfiplat6      aneuploidy 373       109 rank-biserial r     0.211    NaN    NaN 0.001              0.004
label_pfiplat6             tmb 354       104 rank-biserial r    -0.057    NaN    NaN 0.397              0.498
label_pfiplat6             age 389       115 rank-biserial r     0.146    NaN    NaN 0.023              0.046
label_response        brca_mut 303        48              OR     1.231  0.345  3.580 0.782              0.782
label_response        stage_iv 424        65              OR     1.251  0.571  2.566 0.579              0.782
label_response residual_subopt 335        52              OR     2.549  1.314  4.912 0.003              0.021
label_response      aneuploidy 409        64 rank-biserial r    -0.031    NaN    NaN 0.696              0.782
label_response             tmb 391        63 rank-biserial r    -0.028    NaN    NaN 0.720              0.782
label_response             age 425        65 rank-biserial r     0.060    NaN    NaN 0.441              0.782
    label_os18        brca_mut 126        10              OR     0.000  0.000  5.593 1.000              1.000
    label_os18        stage_iv 206        22              OR     1.224  0.214  4.711 0.727              0.872
    label_os18 residual_subopt 180        17              OR     3.604  1.159 11.883 0.014              0.041
    label_os18      aneuploidy 198        22 rank-biserial r     0.416    NaN    NaN 0.001              0.009
    label_os18             tmb 199        21 rank-biserial r    -0.105    NaN    NaN 0.423              0.634
    label_os18             age 206        22 rank-biserial r     0.288    NaN    NaN 0.027              0.055
    label_os24        brca_mut 123        17              OR     0.000  0.000  2.806 0.354              0.425
    label_os24        stage_iv 199        36              OR     0.894  0.208  2.932 1.000              1.000
    label_os24 residual_subopt 174        30              OR     2.263  0.930  5.473 0.052              0.103
    label_os24      aneuploidy 191        36 rank-biserial r     0.326    NaN    NaN 0.002              0.014
    label_os24             tmb 192        34 rank-biserial r    -0.115    NaN    NaN 0.283              0.425
    label_os24             age 199        36 rank-biserial r     0.222    NaN    NaN 0.037              0.103
```

## Predictions vs observed

- P1 BRCA, label_platinum: OR 0.00 [0.00, 0.53], p = 0.0033, q = 0.0198 (cov=1: 0.0/16.0 label=1; cov=0: 59.0/175.0)
- P1 BRCA, label_pfiplat6: OR 0.00 [0.00, 0.33], p = 0.000122, q = 0.000732 (cov=1: 0.0/25.0 label=1; cov=0: 82.0/247.0)
- P2 BRCA, label_os18: OR 0.00 [0.00, 5.59], p = 1, q = 1 (cov=1: 0.0/10.0 label=1; cov=0: 10.0/116.0)
- P2 BRCA, label_os24: OR 0.00 [0.00, 2.81], p = 0.354, q = 0.425 (cov=1: 0.0/10.0 label=1; cov=0: 17.0/113.0)
- (BRCA, label_response: OR 1.23 [0.35, 3.58], p = 0.782, q = 0.782 (cov=1: 5.0/27.0 label=1; cov=0: 43.0/276.0))
- P3 residual, label_platinum: OR 1.12 [0.59, 2.09], p = 0.762, q = 0.914 (cov=1: 23.0/67.0 label=1; cov=0: 59.0/185.0)
- P4 age, label_os24: r = +0.222, medians 59 vs 57, p = 0.037, q = 0.103, n = 199; label_platinum: r = +0.072, medians 60 vs 58, p = 0.337, q = 0.505, n = 277
- P5 aneuploidy/TMB, smallest q: label_platinum 0.13, label_pfiplat6 0.00399, label_response 0.782, label_os18 0.00888, label_os24 0.0141
- P6 stage IV ORs: label_platinum 1.02 [0.46, 2.17], label_pfiplat6 1.09 [0.57, 2.03], label_response 1.25 [0.57, 2.57], label_os18 1.22 [0.21, 4.71], label_os24 0.89 [0.21, 2.93]

## Decision rule (BRCA known-groups validity)

- label_platinum: **BRCA-valid**
- label_pfiplat6: **BRCA-valid**
- label_response: **not supported**
- label_os18: **direction only**
- label_os24: **direction only**

Supplement: label_os12 rows in a3_known_groups.csv (supplement = True). Covariates per patient: a3_covariates.csv.
## Post-run notes (added after the run; header predictions left unchanged)

- **Prediction scorecard:** P1 held (both platinum labels BRCA-valid; 0/16 and 0/25 BRCA mutants resistant). P2 failed as worded: OS-label ORs are also 0 (0/10 mutants non-responders), not "closer to 1"; their CIs include 1 because only 10 of the BRCA-sequenced OS-labelled patients are mutant and non-responders are rare (OS18: 10/126; OS24: 17/123), so fewer than 2 mutant non-responders would be expected even with no association — the BRCA test is uninformative for OS labels, not evidence against them. P3 failed (OR 1.12). P4 held (age r +0.22 for OS24, +0.07 for platinum). P5 failed: aneuploidy is BH-significant for label_pfiplat6 (q 0.004), label_os18 (q 0.009) and label_os24 (q 0.014), not for label_platinum (q 0.21) or label_response. P6 failed as worded (OS24 OR 0.89); every stage-IV CI includes 1.
- **Correction to the header's disclosure (P3):** TCGA 2011 SI Methods S1 (section "Surgical outcome is associated with OS, PFS, and platinum status") states verbatim: "We found no association between platinum status and surgical cytoreduction when defined traditionally as optimal or suboptimal." The association it reports is for microscopic residual disease vs more than microscopic ("P = 0.003, df=2, Odds ratio = 3.1"). The header summarised this loosely; the observed OR 1.12 for optimal vs suboptimal reproduces TCGA's own null. Microscopic-only was not pre-specified and is not tested here.
- **Pattern (descriptive):** residual disease is associated with label_response (OR 2.55, q 0.021) and label_os18 (OR 3.60, q 0.041) but not label_platinum; aneuploidy with OS labels and the PFI-from-platinum label but not the published platinum label.

## A3 part 2 — PFI Cox (03b_pfi_cox.R, run by Aaron on host R 4.6.0, 2026-10-29)

v2 Cox cohort (n = 432, 317 PFI events; BRCA subset 335, 28 mutant). Endpoint CDR PFI; formula unchanged from phase2/src/hrd. One pre-run bug fix (cox.zph could not rebuild the model frame; `coxph` now called via `do.call`) — no change to models or predictions.

| Model | Term | HR [95% CI] | p |
|---|---|---|---|
| baseline, full (n 432) | aneuploidy | 1.028 [1.012, 1.043] | 0.00045 |
| | log1p(TMB) | 0.897 [0.762, 1.056] | 0.19 |
| baseline, matched (n 335) | aneuploidy | 1.029 [1.010, 1.048] | 0.0028 |
| | log1p(TMB) | 0.693 [0.519, 0.926] | 0.013 |
| BRCA added (n 335) | BRCA_any_mutated | 0.499 [0.287, 0.869] | 0.014 |
| | aneuploidy | 1.026 [1.007, 1.045] | 0.0062 |
| | log1p(TMB) | 0.762 [0.565, 1.027] | 0.074 |

C-index: 0.560 (full baseline), 0.562 (matched baseline), 0.574 (BRCA added). Global Schoenfeld p: 0.958 / 0.634 / 0.722.

Scorecard: P1 held (aneuploidy HR > 1, p < 0.05; TMB CI includes 1 in the full cohort). P2 partly failed: BRCA HR 0.499 (p 0.014) is < 1 as predicted but not lower than the v2 OS estimate (0.455). P3 held (C-index 0.560). P4 held (global Schoenfeld p 0.958; the BRCA term also meets PH for PFI, p 0.68, unlike the borderline p 0.042 for OS in v2).
