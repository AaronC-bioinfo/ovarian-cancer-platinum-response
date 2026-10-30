# A18 — Sensitivity of the re-derived interval label to the treatment anchor

Python 3.10.12; pandas 2.3.3; numpy 2.2.6

Reproduction of labels_master (A0): intervals identical True; labels identical True.

```
anchor  determinate  resistant  anchor_differs_from_A0  n_both_A0  changed_vs_A0  pct_changed  kappa_A0  n_both_platinum  agree_platinum  kappa_platinum
    A0          389        115                       0        389              0        0.000     1.000              272             268           0.966
    A1          389        110                      55        389              5        1.285     0.969              272             267           0.957
    A2          407        121                      56        389              5        1.285     0.969              276             270           0.950
    A3          388        114                       0        388              0        0.000     1.000              272             268           0.966
```

```
                                                                                  item   n
                                              patients with label_pfiplat6 determinate 389
                                                         with >1 Adjuvant platinum row  60
                                               with overlapping Adjuvant platinum rows   8
                               with >1 Adjuvant platinum row sharing the max STOP_DATE   7
                                       with an Adjuvant platinum row missing STOP_DATE   1
  with an Adjuvant platinum row starting on/after the first Recurrence/Progression row   1
                                  with any platinum row of indication Other or missing   6
                                     cohort patients without any Adjuvant platinum row  23
```

Decision rule — alternatives changing > 5% of calls: none

Note (added after the run): the header first gave its writing time as "23:56–00:05 ET", an estimate made before the run; the script was run at 23:57 ET, so the time string was corrected to 23:55–23:57 ET. Nothing else in the header was changed.

Note 2 (added 2026-10-30 after the run, from an independent audit): the header says platinum rows are "carboplatin, cisplatin; as in the cohort definition". The code matches AGENT containing "PLATIN", as labels_master does, which also includes oxaliplatin (7 rows, 4 adjuvant; the anchor for 3 patients, 2 with a determinate interval). The cohort itself is defined by carboplatin or cisplatin. The results above use the code as written; the header wording is inaccurate and was not changed.
