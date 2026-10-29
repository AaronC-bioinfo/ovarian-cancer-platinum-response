# Gate G1–G3 summary — label_validity/00_gate_pfi_coverage.py

Cohort reproduction (repo functions): platinum=489; 12m n=214; 12m events=11; 18m n=206; 18m events=22; 24m n=199; 24m events=36 — all match fixes/phase1_provenance.md. Cox cohort 432 read from phase2/outputs.

## G1 — CDR PFI coverage

```
            cohort   n  in_cdr  has_cdr_pfi  pfi_events  redacted
platinum_exact_489 489     489          488         366        38
           cox_432 432     432          432         317        30
           cls_12m 214     214          214         183         7
           cls_18m 206     206          206         179         7
           cls_24m 199     199          199         174         7
```

- P1.1 ≥460/489 platinum with PFI → observed 488
- P1.2 each cls cohort ≥190 → observed cls_12m: 214/214, cls_18m: 206/206, cls_24m: 199/199
- P1.3 ≥410/432 Cox → observed 432
- **G1 PASS** (rule: every cls cohort ≥120 with PFI)

## G2 — platinum-specific sources

```
            cohort   n  pub_Resistant  pub_Sensitive  pub_Tooearly  pub_Missing  pub_absent  pub_determinate  has_firstline_platinum_row  has_firstline_stop_date  pfi_plat6_short  pfi_plat6_long  pfi_plat6_indeterminate  pfi_plat_negative  either_determinate
      all_patients 587             90            197            58          143          99              287                         467                      438              115             275                       47                 19                 404
platinum_exact_489 489             87            190            57           87          68              277                         466                      437              115             274                       47                 19                 394
           cox_432 432             74            169            55           78          56              243                         409                      384               98             243                       43                 18                 345
           cls_12m 214             40            103            11           53           7              143                         199                      185               52             132                        1                  4                 185
           cls_18m 206             39            100            10           51           6              139                         192                      178               51             126                        1                  4                 178
           cls_24m 199             39             95            10           50           5              134                         187                      173               51             121                        1                  4                 173
```

- P2.1 pub Resistant/Sensitive ≥250 overall, ≥150 in cls_24m → observed 287 overall, 134 in cls_24m
- P2.2 ≥80% of 489 with first-line platinum STOP_DATE → observed 437/489 = 0.894 [0.863, 0.918]
- P2.3 PFI-from-platinum vs pub status agreement ≥0.80 → observed 268/272 = 0.985 [0.963, 0.994]
- P2.4 substring match adds ≤20 to 489 → observed +1 patients (1 with RNA-seq); exact-match patients not found by substring: 0
- **G2 PASS** (rule: ≥150 determinate in cls_24m from either source; observed 173)

## G3 — response field vs platinum label vs OS labels (platinum cohort, n=489)

- P3.1 unique pan-can PTOS patients 120–142 → observed 142 (0 with conflicting values)
- P3.2 P(Resistant/short | PD) ≥0.70 → combined 1/5 = 0.200 [0.036, 0.624]; pub status only 1/3 = 0.333 [0.061, 0.792]; PFI-from-platinum only 2/5 = 0.400 [0.118, 0.769]
- P3.3 P(Sensitive/long | CR) ≥0.70 → combined 75/80 = 0.938 [0.862, 0.973]; pub status only 51/55 = 0.927 [0.827, 0.971]; PFI-from-platinum only 74/80 = 0.925 [0.846, 0.965]
- P3.4 pan-can PTOS vs CDR first-course outcome agreement ≥0.95 → observed 141/142 = 0.993 [0.961, 0.999]
- P3.5 OS18 sensitivity for Resistant <0.5 → observed 11/49 = 0.224 [0.130, 0.359]
- P3.5 OS24 sensitivity for Resistant <0.5 → observed 17/49 = 0.347 [0.229, 0.487]
- **G3 FAIL** (rule: P(Resistant/short | PD) ≥0.80 with ≥10 PD)

Full cross-tabs: gate_g3_crosstabs.csv. Per-patient provenance: gate_patient_table.csv.
Combined platinum label = ov_tcga_pub PLATINUM_STATUS where Resistant/Sensitive, else PFI-from-first-line-platinum short/long. Proportions with Wilson 95% CI.