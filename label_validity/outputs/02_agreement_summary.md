# A2 — label agreement

Population: platinum-treated patients with both labels determinate. κ 95% CI: 2,000-resample bootstrap (seed 42).
Coding: 1 = non-responder / resistant. Cells a1b1 … a0b0 are label_a × label_b.

```
       label_a        label_b   n  a1b1  a1b0  a0b1  a0b0  agreement  kappa  kappa_lo  kappa_hi
label_platinum label_pfiplat6 272    85     0     4   183      0.985  0.966     0.930     0.992
label_platinum label_response 255    20    58     8   169      0.741  0.257     0.137     0.380
label_platinum     label_os18 139     5    34     2    98      0.741  0.144     0.014     0.293
label_platinum     label_os24 134    11    28     7    88      0.739  0.248     0.073     0.416
label_pfiplat6 label_response 353    27    74    22   230      0.728  0.213     0.100     0.322
label_pfiplat6     label_os18 177    11    40     5   121      0.746  0.221     0.081     0.366
label_pfiplat6     label_os24 172    18    33    10   111      0.750  0.311     0.154     0.463
label_response     label_os18 184     7    21     8   148      0.842  0.245     0.060     0.440
label_response     label_os24 179    10    18    17   134      0.804  0.248     0.067     0.430
    label_os18     label_os24 199    22     0    14   163      0.930  0.720     0.567     0.848
```

## Predictions vs observed

- P1 κ(OS18, platinum) κ = 0.144 [0.014, 0.293], n = 139, agreement 0.741; κ(OS24, platinum) κ = 0.248 [0.073, 0.416], n = 134, agreement 0.739 — predicted both < 0.40
- P2 κ(OS18, pfiplat6) κ = 0.221 [0.081, 0.366], n = 177, agreement 0.746; κ(OS24, pfiplat6) κ = 0.311 [0.154, 0.463], n = 172, agreement 0.750 — predicted both < 0.40
- P3 sensitivity for platinum-resistant: OS18 5/39 = 0.128 [0.056, 0.267]; OS24 11/39 = 0.282 [0.165, 0.438] — predicted < 0.50
- P4 specificity for platinum-sensitive: OS18 98/100 = 0.980 [0.930, 0.994]; OS24 88/95 = 0.926 [0.856, 0.964] — predicted > 0.85
- P5 κ(platinum, pfiplat6) κ = 0.966 [0.930, 0.992], n = 272, agreement 0.985 — predicted ≥ 0.80
- P6 κ(platinum, response) κ = 0.257 [0.137, 0.380], n = 255, agreement 0.741 — predicted 0.30–0.60

**Decision rule: SUPPORTED** (OS-threshold labels vs the primary platinum label).

## OS labels as tests against each reference (sensitivity / specificity, Wilson 95% CI)

```
     reference   os_label   n  ref_pos  tp  sensitivity  sens_lo  sens_hi  ref_neg  tn  specificity  spec_lo  spec_hi
label_platinum label_os12 143       40   1        0.025    0.004    0.129      103 103        1.000    0.964    1.000
label_platinum label_os18 139       39   5        0.128    0.056    0.267      100  98        0.980    0.930    0.994
label_platinum label_os24 134       39  11        0.282    0.165    0.438       95  88        0.926    0.856    0.964
label_pfiplat6 label_os12 184       52   6        0.115    0.054    0.230      132 132        1.000    0.972    1.000
label_pfiplat6 label_os18 177       51  11        0.216    0.125    0.346      126 121        0.960    0.910    0.983
label_pfiplat6 label_os24 172       51  18        0.353    0.236    0.490      121 111        0.917    0.855    0.954
label_response label_os12 191       30   4        0.133    0.053    0.297      161 160        0.994    0.966    0.999
label_response label_os18 184       28   7        0.250    0.127    0.434      156 148        0.949    0.902    0.974
label_response label_os24 179       28  10        0.357    0.207    0.542      151 134        0.887    0.827    0.929
```

## Sensitivity check: platinum ∩ RNA-seq (pairs without OS labels)

```
       label_a        label_b   n  agreement  kappa  kappa_lo  kappa_hi
label_platinum label_pfiplat6 144      0.986  0.966     0.912     1.000
label_platinum label_response 136      0.772  0.300     0.122     0.470
label_pfiplat6 label_response 175      0.726  0.190     0.036     0.357
```

Supplement (12m): see rows with supplement = True in a2_pairwise_agreement.csv and a2_os_sens_spec.csv.