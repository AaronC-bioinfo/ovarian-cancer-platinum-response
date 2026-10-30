# A16 — Controlled comparison of training labels (same patients, same folds)

Python 3.14.5; scikit-learn 1.9.0; numpy 2.4.6; pandas 3.0.3
Patients: 134 (platinum-resistant 39; OS18 7; OS24 18). 20 × 5-fold CV; 2000 stratified patient bootstraps.

## Mean AUC over 3 models and 20 repeats (min–max across model × repeat)

```
                                mean    min    max
train_label    test_label                         
label_os18     label_os18      0.573  0.155  0.813
               label_os24      0.588  0.318  0.741
               label_platinum  0.540  0.473  0.619
label_os24     label_os18      0.641  0.468  0.755
               label_os24      0.620  0.409  0.724
               label_platinum  0.619  0.541  0.666
label_platinum label_os18      0.593  0.399  0.721
               label_os24      0.655  0.453  0.770
               label_platinum  0.602  0.392  0.703
```

## Paired differences (mean over models; scores averaged over repeats)

- primary_dAUC24 (label_platinum − label_os24 on label_platinum): -0.005 [-0.105, +0.087]; CI includes 0: True; per-repeat mean -0.016 (range -0.107 to +0.071; ≥ 0.05 in 2/20)
- dAUC18 (label_platinum − label_os18 on label_platinum): +0.080 [-0.045, +0.201]; CI includes 0: True; per-repeat mean +0.063 (range -0.014 to +0.145; ≥ 0.05 in 13/20)
- reverse_OS24_target (label_os24 − label_platinum on label_os24): -0.069 [-0.236, +0.081]; CI includes 0: True; per-repeat mean -0.034 (range -0.169 to +0.045; ≥ 0.05 in 0/20)

## Prediction scorecard

~~(to be completed after the run)~~

Run 2026-10-29 21:57–21:59 ET on the Windows host (Python 3.14.5; scikit-learn 1.9.0; numpy 2.4.6; pandas 3.0.3; a16_ENVIRONMENT.txt), after the script with its predictions and decision rules was committed (d349b2b, 21:56:39 ET; now on GitHub main). Output modification times run from 21:57:04 (a16_ENVIRONMENT.txt) to 21:59:39 (a16_paired_differences.csv, this summary, a16_run_log.txt).

Correction to the script header: it says "Written 2026-10-29 ~22:10 ET, BEFORE the run". That time was a wrong estimate. The script was committed at 21:56:39 ET (d349b2b), so it was written before then. The commit timestamp is authoritative, and the run followed it.

Deviation: the script stopped with a UnicodeEncodeError at its final `print` (line 180), because the Windows cp1252 console cannot encode U+2212 (minus sign; traceback in a16_run_log.txt). This summary is written on line 179, before the print, and contains every pre-specified section; all outputs have modification times at or before the crash (21:59:39). No number is affected. Future runs set `PYTHONIOENCODING=utf-8`.

Environment check (run after the scorecard was first drafted, 2026-10-29 ~22:25 ET): the same script was rerun unchanged in the cloud-linked VM (Python 3.10.12; scikit-learn 1.7.2; numpy 2.2.6; pandas 2.3.3); outputs in `a16_env_check_vm/`. Logistic regression and SVM AUCs are identical in all 180 model × label × repeat cells each; Random Forest AUCs differ by up to 0.136 in single cells. Paired differences, Windows → VM: ΔAUC_24 −0.005 → −0.008 [−0.106, +0.086]; ΔAUC_18 +0.080 → +0.074 [−0.050, +0.194]; reverse on OS24 −0.069 → −0.072 [−0.236, +0.077]. Every interval still includes 0 and every prediction scores the same; the Windows run remains the reported result.

Population: 134 patients in whom platinum status, OS18 and OS24 are all determinate (platinum-resistant 39; OS18 7; OS24 18). With only 7 OS18 positives, the OS18-trained models are unstable (OS18-trained → OS18 AUC 0.155–0.813 across model × repeat).

- **Q1 — FAILED.** ΔAUC_24 (platinum-trained − OS24-trained, on platinum status): −0.005 [−0.105, +0.087]; predicted between 0 and +0.10. Per-repeat mean −0.016 (range −0.107 to +0.071; ≥ 0.05 in 2/20).
- **Q2 — held.** The 95% bootstrap interval for ΔAUC_24 includes 0.
- **Q3 — held.** ΔAUC_18 (platinum-trained − OS18-trained, on platinum status): +0.080 [−0.045, +0.201]; > 0, interval includes 0. Per-repeat mean +0.063 (range −0.014 to +0.145; ≥ 0.05 in 13/20).
- **Q4 — FAILED (opposite direction).** On the OS24 target, OS24-trained − platinum-trained: −0.069 [−0.236, +0.081]; predicted > 0. The interval includes 0. Per-repeat mean −0.034 (range −0.169 to +0.045; ≥ 0.05 in 0/20).

Decision (pre-specified rule): the ΔAUC_24 interval includes 0. The manuscript states that, in the same 134 patients with the same folds, no difference was detected between platinum-trained and OS24-trained models in predicting platinum status, and that a platinum-label advantage larger than +0.087 AUC (the interval's upper bound) is unlikely. It withdraws any claim that label choice changes classifier performance; A5 is reported as descriptive only.
