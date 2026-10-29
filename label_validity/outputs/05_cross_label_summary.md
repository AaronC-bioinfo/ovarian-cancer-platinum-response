# A5 — within-TCGA cross-label prediction

sklearn 1.9.0; 251 platinum-treated patients with RNA-seq; 15994 common genes; 5 × 5-fold CV, pooled out-of-fold AUC per repeat. Variant P preprocessing (as A4).

## Mean AUC over 3 models × 5 repeats (rows = training label, columns = test label)

```
test_label      label_platinum  label_pfiplat6  label_os18  label_os24
train_label                                                           
label_platinum           0.634           0.617       0.578       0.630
label_pfiplat6           0.593           0.608       0.592       0.623
label_os18               0.552           0.585       0.631       0.651
label_os24               0.597           0.618       0.675       0.682
```

## Per model: mean [min, max] over repeats

```
   train_label     test_label               model  mean   min   max
    label_os18     label_os18 Logistic Regression 0.668 0.647 0.688
    label_os18     label_os18       Random Forest 0.631 0.601 0.664
    label_os18     label_os18                 SVM 0.594 0.568 0.619
    label_os18     label_os24 Logistic Regression 0.675 0.630 0.696
    label_os18     label_os24       Random Forest 0.654 0.586 0.699
    label_os18     label_os24                 SVM 0.624 0.531 0.666
    label_os18 label_pfiplat6 Logistic Regression 0.597 0.580 0.634
    label_os18 label_pfiplat6       Random Forest 0.581 0.541 0.612
    label_os18 label_pfiplat6                 SVM 0.578 0.553 0.598
    label_os18 label_platinum Logistic Regression 0.574 0.560 0.603
    label_os18 label_platinum       Random Forest 0.542 0.493 0.597
    label_os18 label_platinum                 SVM 0.540 0.509 0.563
    label_os24     label_os18 Logistic Regression 0.707 0.636 0.751
    label_os24     label_os18       Random Forest 0.659 0.621 0.672
    label_os24     label_os18                 SVM 0.661 0.622 0.700
    label_os24     label_os24 Logistic Regression 0.708 0.627 0.756
    label_os24     label_os24       Random Forest 0.674 0.599 0.706
    label_os24     label_os24                 SVM 0.663 0.586 0.720
    label_os24 label_pfiplat6 Logistic Regression 0.603 0.568 0.641
    label_os24 label_pfiplat6       Random Forest 0.628 0.593 0.660
    label_os24 label_pfiplat6                 SVM 0.621 0.602 0.632
    label_os24 label_platinum Logistic Regression 0.593 0.561 0.620
    label_os24 label_platinum       Random Forest 0.603 0.572 0.650
    label_os24 label_platinum                 SVM 0.597 0.577 0.605
label_pfiplat6     label_os18 Logistic Regression 0.577 0.567 0.583
label_pfiplat6     label_os18       Random Forest 0.603 0.580 0.615
label_pfiplat6     label_os18                 SVM 0.596 0.562 0.624
label_pfiplat6     label_os24 Logistic Regression 0.585 0.581 0.593
label_pfiplat6     label_os24       Random Forest 0.651 0.630 0.680
label_pfiplat6     label_os24                 SVM 0.632 0.594 0.665
label_pfiplat6 label_pfiplat6 Logistic Regression 0.597 0.571 0.623
label_pfiplat6 label_pfiplat6       Random Forest 0.610 0.569 0.627
label_pfiplat6 label_pfiplat6                 SVM 0.616 0.590 0.634
label_pfiplat6 label_platinum Logistic Regression 0.594 0.569 0.614
label_pfiplat6 label_platinum       Random Forest 0.592 0.549 0.620
label_pfiplat6 label_platinum                 SVM 0.592 0.543 0.629
label_platinum     label_os18 Logistic Regression 0.560 0.539 0.600
label_platinum     label_os18       Random Forest 0.580 0.526 0.632
label_platinum     label_os18                 SVM 0.593 0.567 0.640
label_platinum     label_os24 Logistic Regression 0.612 0.597 0.637
label_platinum     label_os24       Random Forest 0.637 0.586 0.686
label_platinum     label_os24                 SVM 0.640 0.608 0.692
label_platinum label_pfiplat6 Logistic Regression 0.621 0.592 0.656
label_platinum label_pfiplat6       Random Forest 0.610 0.583 0.659
label_platinum label_pfiplat6                 SVM 0.619 0.583 0.654
label_platinum label_platinum Logistic Regression 0.650 0.620 0.686
label_platinum label_platinum       Random Forest 0.627 0.564 0.689
label_platinum label_platinum                 SVM 0.625 0.582 0.671
```

## Predictions vs observed

- P1 diagonal: OS24→OS24 0.682 (predicted 0.62–0.72); platinum→platinum 0.634 (predicted 0.52–0.65)
- P2 OS-trained → platinum: OS18 0.552, OS24 0.597, mean 0.575 (predicted ≤ 0.58)
- P3 platinum → OS24: 0.630 (predicted ≤ 0.60)
- P4 platinum→pfiplat6 0.617 vs pfiplat6→pfiplat6 0.608; pfiplat6→platinum 0.593 vs platinum→platinum 0.634 (predicted within 0.03)

Ceiling 0.634; label effect +0.060; platform effect +0.045 (vs A4 GEO dfs 0.589).
**Decision rule: label mismatch SUPPORTED; platform/cohort shift not supported.**
## Post-run notes (added after the run; header predictions unchanged)

Run by Aaron on the host (sklearn 1.9.0), 2026-10-29 16:35 ET. A VM dry run (sklearn 1.7.2, 1 repeat) was made after the predictions were committed, as a smoke test only; its numbers are not used.

### Scorecard
- P1 held: OS24→OS24 0.682 (0.62–0.72); platinum→platinum 0.634 (0.52–0.65).
- P2 held, barely: OS-trained → platinum 0.575 (≤ 0.58); OS18 0.552, OS24 0.597.
- P3 failed: platinum → OS24 0.630 (predicted ≤ 0.60) — close to OS24's own ceiling (0.682).
- P4 failed: pfiplat6→platinum 0.593 vs ceiling 0.634 (Δ 0.041 > 0.03); platinum→pfiplat6 0.617 exceeds pfiplat6→pfiplat6 0.608.

### Stability of the decision-rule quantities across the 5 repeats (mean of 3 models)
- Ceiling (platinum→platinum): 0.653, 0.645, 0.605, 0.679, 0.590.
- Label effect: 0.091, 0.074, 0.019, 0.084, 0.030 — ≥ 0.05 in 3 of 5 repeats; mean +0.060.
- Platform effect (vs A4 0.589): 0.064, 0.056, 0.016, 0.090, 0.001 — ≥ 0.05 in 3 of 5 repeats; mean +0.045.
- The pre-specified verdict on the means ("label mismatch supported; platform/cohort shift not supported") rests on a 0.015 difference between two small effects whose repeat-to-repeat ranges overlap. Reportable wording: both effects are small (≈ 0.05 AUC) and neither is robust; the binding constraint is the low within-TCGA ceiling for platinum status (0.634), so expression predicts platinum status only modestly even before any label or platform shift.
- The platform comparison is crude by design: A4 trained on all 145 labelled patients, A5 on ≈ 116 per fold, and they are scored on different cohorts.
