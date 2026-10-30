# A10 — Prognostic covariates by label, full cohort and same patients

Common set (platinum, OS18_all, OS24_all determinate): n = 259.

## T1 — all determinate patients (BH across 5 covariates within label)

**label_platinum**
- residual_subopt: OR +1.116 [0.59, 2.09]; n 252; p 0.762; q 0.952
- stage_iv: OR +1.016 [0.46, 2.17]; n 277; p 1; q 1
- aneuploidy: rank_biserial_r +0.125; n 265; p 0.103; q 0.258
- tmb: rank_biserial_r -0.157; n 255; p 0.0432; q 0.216
- age: rank_biserial_r +0.072; n 277; p 0.337; q 0.562

**label_pfiplat6**
- residual_subopt: OR +1.251 [0.71, 2.18]; n 310; p 0.415; q 0.518
- stage_iv: OR +1.088 [0.57, 2.03]; n 388; p 0.762; q 0.762
- aneuploidy: rank_biserial_r +0.211; n 373; p 0.00133; q 0.00665
- tmb: rank_biserial_r -0.057; n 354; p 0.397; q 0.518
- age: rank_biserial_r +0.146; n 389; p 0.0229; q 0.0572

**label_response**
- residual_subopt: OR +2.549 [1.31, 4.91]; n 335; p 0.0035; q 0.0175
- stage_iv: OR +1.251 [0.57, 2.57]; n 424; p 0.579; q 0.72
- aneuploidy: rank_biserial_r -0.031; n 409; p 0.696; q 0.72
- tmb: rank_biserial_r -0.028; n 391; p 0.72; q 0.72
- age: rank_biserial_r +0.060; n 425; p 0.441; q 0.72

**label_os18_all**
- residual_subopt: OR +2.858 [1.30, 6.29]; n 328; p 0.00473; q 0.0118
- stage_iv: OR +1.753 [0.76, 3.79]; n 418; p 0.138; q 0.173
- aneuploidy: rank_biserial_r +0.205; n 404; p 0.0223; q 0.0372
- tmb: rank_biserial_r -0.075; n 379; p 0.419; q 0.419
- age: rank_biserial_r +0.261; n 419; p 0.00348; q 0.0118

**label_os24_all**
- residual_subopt: OR +2.410 [1.28, 4.50]; n 318; p 0.0038; q 0.00633
- stage_iv: OR +1.551 [0.78, 2.97]; n 400; p 0.175; q 0.218
- aneuploidy: rank_biserial_r +0.253; n 386; p 0.000586; q 0.00147
- tmb: rank_biserial_r -0.078; n 361; p 0.309; q 0.309
- age: rank_biserial_r +0.277; n 401; p 0.000145; q 0.000727

## T2 — common set

- label_platinum × aneuploidy: rank_biserial_r +0.114; n 248; p 0.151
- label_platinum × residual_subopt: OR +1.137 [0.59, 2.18]; n 236; p 0.754
- label_os18_all × aneuploidy: rank_biserial_r +0.057; n 248; p 0.663
- label_os18_all × residual_subopt: OR +1.612 [0.52, 4.62]; n 236; p 0.422
- label_os24_all × aneuploidy: rank_biserial_r +0.221; n 248; p 0.0226
- label_os24_all × residual_subopt: OR +1.869 [0.82, 4.12]; n 236; p 0.106

Differences (2,000 bootstrap resamples):

- aneuploidy, label_os18_all − label_platinum: Δ rank-biserial r -0.057 [-0.347, +0.206] (n 248); CI includes 0: True
- aneuploidy, label_os24_all − label_platinum: Δ rank-biserial r +0.107 [-0.094, +0.305] (n 248); CI includes 0: True
- residual_subopt, label_os18_all − label_platinum: Δ log OR (Haldane) +0.370 [-0.663, +1.253] (n 236); CI includes 0: True
- residual_subopt, label_os24_all − label_platinum: Δ log OR (Haldane) +0.501 [-0.232, +1.209] (n 236); CI includes 0: True

## Prediction scorecard

Run 2026-10-29 ~19:32 ET (VM; no model fitting), after the predictions were pushed (commit e98b3d9). One earlier dry run, output not inspected.

- **R1 — held.** Aneuploidy, full cohort: OS18_all r +0.205 (q 0.037); OS24_all r +0.253 (q 0.0015).
- **R2 — held.** Residual disease, full cohort: OS18_all OR 2.86 [1.30, 6.29]; OS24_all OR 2.41 [1.28, 4.50].
- **R3 — held.** Common set (n 248): Δr aneuploidy, OS24 − platinum +0.107 [−0.094, +0.305]. Also OS18 − platinum −0.057 [−0.347, +0.206].
- **R4 — held.** Common set (n 236): Δ log OR residual, OS18 − platinum +0.37 [−0.66, +1.25]. Also OS24 − platinum +0.50 [−0.23, +1.21].

Decision (pre-specified rule): all four difference CIs include 0. The manuscript reports the per-label associations descriptively and does NOT claim that the OS labels track aneuploidy or residual disease differently from platinum status. The v3 sentence "the OS labels instead tracked aneuploidy and residual disease" is withdrawn as a contrast between labels.

Not pre-specified (observation only): age is associated with both OS labels in the full cohort (r +0.26, +0.28; q ≤ 0.012) but not with platinum status (r +0.07, q 0.56). No same-patient difference test was run for age, so this is reported, if at all, as an observation.
