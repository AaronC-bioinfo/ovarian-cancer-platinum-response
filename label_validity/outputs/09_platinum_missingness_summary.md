# A9 — Who lacks a determinate platinum status; what OS labels capture

## Part A — primary_in_2011_release (undetermined vs determinate)

- A1 OS log-rank: n 144 vs 276; chi² 0.81, p 0.37
  - KM median OS, undetermined: 47.5 months (n 144, deaths 71)
  - KM median OS, determinate: 47.7 months (n 276, deaths 189)
- A2_death_lt18: 16/96 vs 22/268; OR 2.23 [1.04, 4.70], p 0.0307
- A2_death_lt24: 24/95 vs 43/259; OR 1.70 [0.92, 3.09], p 0.0684
- A3_pfiplat6_resistant: 13/68 vs 89/272; OR 0.49 [0.23, 0.96], p 0.0376
- A4_response_PDSD: 28/114 vs 28/255; OR 2.63 [1.41, 4.91], p 0.00147
- A5_residual_subopt: 37/127 vs 67/252; OR 1.13 [0.68, 1.87], p 0.627
- A5_stage_iv: 25/143 vs 41/277; OR 1.22 [0.68, 2.17], p 0.482
- A5 age: median difference -1.0 years, p 0.509

## Part A — secondary_all_489 (undetermined vs determinate)

- A1 OS log-rank: n 212 vs 276; chi² 0.05, p 0.83
  - KM median OS, undetermined: 48.8 months (n 212, deaths 93)
  - KM median OS, determinate: 47.7 months (n 276, deaths 189)
  - KM median OS, Missing: 39.0 months (n 87, deaths 61)
  - KM median OS, Tooearly: nan months (n 57, deaths 10)
  - KM median OS, Resistant: 32.9 months (n 87, deaths 77)
  - KM median OS, Sensitive: 58.2 months (n 189, deaths 112)
  - KM median OS, absent: 54.3 months (n 68, deaths 22)
- A2_death_lt18: 25/151 vs 22/268; OR 2.21 [1.15, 4.30], p 0.0148
- A2_death_lt24: 35/142 vs 43/259; OR 1.64 [0.96, 2.80], p 0.0644
- A3_pfiplat6_resistant: 26/117 vs 89/272; OR 0.59 [0.34, 0.99], p 0.0399
- A4_response_PDSD: 37/170 vs 28/255; OR 2.25 [1.28, 4.01], p 0.00363
- A5_residual_subopt: 37/127 vs 67/252; OR 1.13 [0.68, 1.87], p 0.627
- A5_stage_iv: 33/211 vs 41/277; OR 1.07 [0.63, 1.81], p 0.8
- A5 age: median difference +0.0 years, p 0.263

## Part B/C — OS labels against platinum status and the hybrid label

- os18_rnaseq vs platinum: n 139; sens 5/39 = 0.13; spec 0.98; PPV 5/7 = 0.71; NPV 0.74; LR+ 6.41; κ 0.144 (κmax 0.239); PABAK 0.482
- os24_rnaseq vs platinum: n 134; sens 11/39 = 0.28; spec 0.93; PPV 11/18 = 0.61; NPV 0.76; LR+ 3.83; κ 0.248 (κmax 0.549); PABAK 0.478
- os18_all vs platinum: n 268; sens 18/84 = 0.21; spec 0.98; PPV 18/22 = 0.82; NPV 0.73; LR+ 9.86; κ 0.241 (κmax 0.328); PABAK 0.478
- os24_all vs platinum: n 259; sens 32/83 = 0.39; spec 0.94; PPV 32/43 = 0.74; NPV 0.76; LR+ 6.17; κ 0.370 (κmax 0.594); PABAK 0.521
- os18_all vs hybrid: n 375; sens 29/108 = 0.27; spec 0.97; PPV 29/37 = 0.78; NPV 0.77; LR+ 8.96; κ 0.297 (κmax 0.426); PABAK 0.536
- os24_all vs hybrid: n 360; sens 47/107 = 0.44; spec 0.93; PPV 47/64 = 0.73; NPV 0.80; LR+ 6.54; κ 0.421 (κmax 0.677); PABAK 0.572

Hybrid label coverage: 394/489 (113 resistant / 281 sensitive); platinum status alone: 277/489.

## Prediction scorecard

Run 2026-10-29 ~19:30 ET (VM; no model fitting), after the predictions were pushed (commit d5bd844). One earlier dry run, output not inspected.

- **Q1 — FAILED.** No OS difference between undetermined and determinate (log-rank p 0.37; KM medians 47.5 vs 47.7 months). The undetermined group is heterogeneous: Missing has a median of 39.0 months (Resistant 32.9, Sensitive 58.2), while Tooearly has 10 deaths among 57 patients and the median is not reached.
- **Q2 — held.** Death before 18 months: 16/96 vs 22/268, OR 2.23 [1.04, 4.70].
- **Q3 — FAILED (opposite direction).** Resistant by re-derived interval: 13/68 vs 89/272, OR 0.49 [0.23, 0.96]. pfiplat6 is determinate for only 68 of 144 undetermined patients.
- **Q4 — held.** First-course PD/SD: 28/114 vs 28/255, OR 2.63 [1.41, 4.91].
- **Q6 — partly failed.** OS18 (full cohort): PPV 18/22 = 0.82, sensitivity 0.21 — held. OS24: PPV 32/43 = 0.74, but sensitivity 32/83 = 0.39 > 0.30 — failed.

Decision (pre-specified rule): Q1 failed, so the manuscript does NOT claim that platinum status is missing selectively among poor-outcome patients. Instead, it describes the undetermined group as heterogeneous: early deaths and first-course PD/SD are over-represented in it, but overall survival does not differ. Part B metrics replace the "OS labels miss most resistant patients" framing. In the full cohort, OS labels are specific (0.94–0.98) with high PPV (0.74–0.82) and LR+ 6–10, but insensitive (0.21–0.39). κ is bounded by κmax (OS18: 0.24 of a possible 0.33).
