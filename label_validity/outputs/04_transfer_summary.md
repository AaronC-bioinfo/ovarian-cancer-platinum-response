# A4 — label-transfer matrix (TCGA-OV → GSE63885)

sklearn 1.9.0; common genes 15994. Harness = validation/06_external_validation_v2.py, training label swapped.

C1 reproduction: 36/36 rows matched; max |Δ| = 0.16010 → **FAIL — stop and explain before interpreting**

## Variant P (primary): AUC by training label × model × GEO label

```
label                               clinical    dfs
train_label    model                               
label_platinum Logistic Regression     0.616  0.563
               Random Forest           0.712  0.588
               SVM                     0.689  0.616
label_pfiplat6 Logistic Regression     0.670  0.552
               Random Forest           0.745  0.625
               SVM                     0.706  0.610
label_response Logistic Regression     0.630  0.558
               Random Forest           0.547  0.561
               SVM                     0.627  0.574
label_os18     Logistic Regression     0.508  0.581
               Random Forest           0.421  0.555
               SVM                     0.550  0.545
label_os24     Logistic Regression     0.505  0.622
               Random Forest           0.484  0.645
               SVM                     0.575  0.610
```

Full table with 95% CIs: a4_transfer_results.csv.

## Predictions vs observed

- P1 mean dfs AUC (variant P) by training label: label_platinum 0.589, label_pfiplat6 0.596, label_response 0.564, label_os18 0.560, label_os24 0.626 → platinum > OS18 and > OS24: False
- P2 max variant-P AUC: 0.745 (predicted all < 0.70)
- P3 variant-P CIs excluding 0.5: 5 of 30 (predicted ≤ 3); label_platinum/Random Forest/clinical 0.712 [0.559, 0.843]; label_platinum/SVM/clinical 0.689 [0.509, 0.845]; label_pfiplat6/Random Forest/clinical 0.745 [0.591, 0.880]; label_pfiplat6/SVM/clinical 0.706 [0.541, 0.858]; label_os24/Random Forest/dfs 0.645 [0.522, 0.772]
- P4 clinical label CIs excluding 0.5: 4 (predicted 0)
- P5 platinum-trained mean AUC: variant S 0.642 vs variant P 0.631 (predicted S ≤ P)

**Decision rule: Transfer remains weak whatever the training label.** dfs CIs excluding 0.5 per label: label_platinum 0/3, label_pfiplat6 0/3, label_response 0/3, label_os18 0/3, label_os24 1/3
## Post-run notes (added after the run; header predictions unchanged)

### C1 failure — explained
- Only the 12 Random Forest rows differed from `validation/outputs/external_validation_v2_results.csv` (max |Δ| 0.160); all 24 LR and SVM rows matched exactly (Δ = 0.000), so data, gene selection, labels and patient alignment are identical.
- `validation/outputs/external_validation_v2_summary.md` records **"sklearn 1.7.2"**: the v2 external validation was run in an earlier session's VM, not in the pinned host environment (sklearn 1.9.0).
- `04a_rf_determinism_check.py` (same code, same data, 12m / variant S / clinical): host Python 3.14.5 + sklearn 1.9.0 + numpy 2.4.6 → AUC 0.4711 in 6/6 fits (n_jobs −1 and 1); VM Python 3.10.12 + sklearn 1.7.2 + numpy 2.2.6 → 0.6312 in 6/6 fits = the v2 value. Both environments are deterministic; RF output differs between the two sklearn versions. (`04a_rf_determinism.txt`, `04a_rf_determinism_VM.txt`.)
- Conclusion: the harness did not change; the reference file was produced under a different sklearn version. A4 (host, pinned 1.9.0) is interpretable. **Consequence for v2:** the RF rows of the v2 external validation (S1 Table, manuscript text) are from sklearn 1.7.2 and must be replaced by the pinned-environment values — the label_os12/18/24 rows of `a4_transfer_results.csv`.

### Prediction scorecard (variant P)
- P1 failed: mean dfs AUC platinum 0.589, pfiplat6 0.596, response 0.564, OS18 0.560, **OS24 0.626** (highest).
- P2 failed: max AUC 0.745 (pfiplat6 / RF / clinical).
- P3 failed: 5 of 30 CIs exclude 0.5 (predicted ≤ 3).
- P4 failed: 4 clinical-label CIs exclude 0.5 (predicted 0) — all four from platinum-trained models: platinum RF 0.712 [0.559, 0.843], platinum SVM 0.689 [0.509, 0.845], pfiplat6 RF 0.745 [0.591, 0.880], pfiplat6 SVM 0.706 [0.541, 0.858]. OS-trained models on the clinical label: 0.421–0.575, all CIs include 0.5.
- P5 failed narrowly: platinum-trained mean AUC variant S 0.642 vs P 0.631.
- **Pre-specified decision (dfs label): "Transfer remains weak whatever the training label"** — no platinum-trained model has a dfs CI excluding 0.5; the one dfs CI excluding 0.5 is OS24 / RF (0.645 [0.522, 0.772]).

### Not pre-specified (report as observed, not as a finding)
- On the GEO clinical label (SD/PD vs CR/PR; 10 non-responders, all DFS-resistant per G4), platinum-trained models scored 0.616–0.745 and OS-trained 0.421–0.575. The decision rule was set on the dfs label, the clinical label has 10 events, and the 30 variant-P AUCs are uncorrected; this pattern is descriptive only.
