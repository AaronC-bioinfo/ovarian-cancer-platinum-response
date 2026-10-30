# A16 — Controlled comparison of training labels (same patients, same folds)

Python 3.10.12; scikit-learn 1.7.2; numpy 2.2.6; pandas 2.3.3
Patients: 134 (platinum-resistant 39; OS18 7; OS24 18). 20 × 5-fold CV; 2000 stratified patient bootstraps.

## Mean AUC over 3 models and 20 repeats (min–max across model × repeat)

```
                                mean    min    max
train_label    test_label                         
label_os18     label_os18      0.579  0.155  0.813
               label_os24      0.588  0.318  0.741
               label_platinum  0.542  0.473  0.618
label_os24     label_os18      0.647  0.468  0.771
               label_os24      0.622  0.409  0.709
               label_platinum  0.619  0.541  0.667
label_platinum label_os18      0.599  0.399  0.736
               label_os24      0.656  0.453  0.757
               label_platinum  0.602  0.392  0.703
```

## Paired differences (mean over models; scores averaged over repeats)

- primary_dAUC24 (label_platinum − label_os24 on label_platinum): -0.008 [-0.106, +0.086]; CI includes 0: True; per-repeat mean -0.016 (range -0.098 to +0.075; ≥ 0.05 in 1/20)
- dAUC18 (label_platinum − label_os18 on label_platinum): +0.074 [-0.050, +0.194]; CI includes 0: True; per-repeat mean +0.060 (range -0.013 to +0.142; ≥ 0.05 in 13/20)
- reverse_OS24_target (label_os24 − label_platinum on label_os24): -0.072 [-0.236, +0.077]; CI includes 0: True; per-repeat mean -0.035 (range -0.153 to +0.058; ≥ 0.05 in 1/20)

## Prediction scorecard

(to be completed after the run)
