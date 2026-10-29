# A8 — BRCA1/2 germline + somatic known-groups test

Sequenced platinum-treated patients: 272; primary carriers: 55 (germline truncating 44); common set n = 180.

## T1 — each label, all determinate patients (carriers non-responding vs non-carriers)

**primary_trunc_germ_som**
- label_platinum: 7/37 vs 54/149; OR 0.41 [0.14, 1.04], p 0.051 — direction only
- label_pfiplat6: 8/47 vs 64/179; OR 0.37 [0.14, 0.87], p 0.014 — BRCA-valid
- label_response: 5/51 vs 28/192; OR 0.64 [0.18, 1.80], p 0.493 — direction only
- label_os18_all: 1/51 vs 23/195; OR 0.15 [0.00, 0.97], p 0.034 — BRCA-valid
- label_os24_all: 3/50 vs 43/192; OR 0.22 [0.04, 0.75], p 0.008 — BRCA-valid

**any_nonsilent_germ_som**
- label_platinum: 8/41 vs 53/145; OR 0.42 [0.16, 1.02], p 0.058 — direction only
- label_pfiplat6: 9/51 vs 63/175; OR 0.38 [0.15, 0.86], p 0.016 — BRCA-valid
- label_response: 5/55 vs 28/188; OR 0.57 [0.16, 1.61], p 0.371 — direction only
- label_os18_all: 1/55 vs 23/191; OR 0.14 [0.00, 0.88], p 0.021 — BRCA-valid
- label_os24_all: 3/54 vs 43/188; OR 0.20 [0.04, 0.67], p 0.003 — BRCA-valid

**germline_trunc**
- label_platinum: 7/29 vs 54/157; OR 0.61 [0.21, 1.59], p 0.389 — direction only
- label_pfiplat6: 8/38 vs 64/188; OR 0.52 [0.19, 1.24], p 0.131 — direction only
- label_response: 5/40 vs 28/203; OR 0.89 [0.25, 2.57], p 1.000 — direction only
- label_os18_all: 1/41 vs 23/205; OR 0.20 [0.00, 1.30], p 0.144 — direction only
- label_os24_all: 3/40 vs 43/202; OR 0.30 [0.06, 1.02], p 0.047 — direction only

**somatic_pancan_A3**
- label_platinum: 0/10 vs 40/117; OR 0.00 [0.00, 0.92], p 0.030 — BRCA-valid
- label_pfiplat6: 0/11 vs 49/147; OR 0.00 [0.00, 0.84], p 0.018 — BRCA-valid
- label_response: 2/13 vs 20/159; OR 1.26 [0.13, 6.45], p 0.674 — not supported
- label_os18_all: 0/12 vs 15/156; OR 0.00 [0.00, 3.80], p 0.604 — direction only
- label_os24_all: 0/12 vs 29/155; OR 0.00 [0.00, 1.68], p 0.129 — direction only

## T2 — common set (primary definition)

- label_platinum: 7/37 vs 52/143; OR 0.41 [0.14, 1.04], p 0.050 — direction only
- label_os18_all: 0/37 vs 12/143; OR 0.00 [0.00, 1.35], p 0.130 — direction only
- label_os24_all: 1/37 vs 28/143; OR 0.11 [0.00, 0.75], p 0.011 — BRCA-valid
- label_pfiplat6: 7/37 vs 52/140; OR 0.40 [0.14, 1.01], p 0.049 — direction only

Difference in log OR (Haldane), 2,000 bootstrap resamples:

- label_platinum − label_os18_all: +1.12 [-0.16, +2.00] (ratio of ORs 3.06; n 180, carriers 37); CI includes 0: True
- label_platinum − label_os24_all: +0.95 [-0.52, +2.71] (ratio of ORs 2.57; n 180, carriers 37); CI includes 0: True
- label_pfiplat6 − label_os24_all: +0.85 [-0.66, +2.56] (ratio of ORs 2.33; n 177, carriers 37); CI includes 0: True

## T3 — BRCA1 vs BRCA2 (primary rule)

- BRCA1_primary, label_platinum: 4/17 vs 57/169; OR 0.61 [0.14, 2.08], p 0.589 — direction only
- BRCA1_primary, label_pfiplat6: 4/25 vs 68/201; OR 0.37 [0.09, 1.17], p 0.109 — direction only
- BRCA2_primary, label_platinum: 3/21 vs 58/165; OR 0.31 [0.06, 1.12], p 0.082 — direction only
- BRCA2_primary, label_pfiplat6: 4/24 vs 68/202; OR 0.40 [0.09, 1.25], p 0.108 — direction only

## T4 — CCNE1 amplification

- label_platinum: 22/56 vs 65/221; OR 1.55 [0.80, 2.97], p 0.197
- label_pfiplat6: 28/70 vs 74/270; OR 1.76 [0.98, 3.15], p 0.056
- label_response: 13/80 vs 43/290; OR 1.11 [0.52, 2.26], p 0.727
- label_os18_all: 12/79 vs 26/285; OR 1.78 [0.78, 3.89], p 0.144
- label_os24_all: 22/78 vs 45/276; OR 2.01 [1.06, 3.75], p 0.022

## Prediction scorecard

Run 2026-10-29 ~19:30 ET in the cloud-linked VM (no model fitting), after the predictions were pushed to GitHub (commit d5bd844, 19:22 ET). One earlier dry run to a scratch folder outside the repo checked that the script runs; its output was not inspected.

Note: the A8 cohort is the sequenced patients who are also platinum-treated (272 of the 316 sequenced tumours). The header's exploratory tabulation was not restricted to platinum-treated patients in the same way and used OS labels from the RNA-seq subset only.

- **P1 — held.** label_platinum: OR 0.41 [0.14, 1.04] ("direction only").
- **P2 — held.** label_pfiplat6: OR 0.37 [0.14, 0.87] ("BRCA-valid").
- **P3 — FAILED.** OS labels in the full platinum cohort: OS18 OR 0.15 [0.00, 0.97]; OS24 OR 0.22 [0.04, 0.75]. Both CIs exclude 1, so BRCA is at least as strongly associated with the OS labels as with platinum status.
- **P4 — held.** Common set: log-OR difference platinum − OS18 +1.12 [−0.16, +2.00]; platinum − OS24 +0.95 [−0.52, +2.71]; pfiplat6 − OS24 +0.85 [−0.66, +2.56]. All CIs include 0, and the point estimates favour a STRONGER association with the OS labels.
- **P5 — held.** BRCA2 OR 0.31 vs BRCA1 OR 0.61 for label_platinum (point estimates; both CIs include 1).
- **P6 — held.** CCNE1 amplification, label_platinum: OR 1.55 [0.80, 2.97]. CCNE1 points the same way for every label (OS24 OR 2.01 [1.06, 3.75]).

Decision (pre-specified rule): BRCA does not separate the platinum labels from the OS labels. The manuscript withdraws "Only the platinum labels show known-groups validity" and reports BRCA (germline + somatic truncating, primary) and CCNE1 as associated in the expected direction under every label. A3's somatic-only result becomes a secondary analysis.
