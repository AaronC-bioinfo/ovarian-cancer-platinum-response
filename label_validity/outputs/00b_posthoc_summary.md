# POST HOC — response-field sources (not pre-registered)

Reads gate_patient_table.csv only. Categories mapped to CR/PR/SD/PD.

## Coverage of the response field by source

```
            cohort   n  pancan_n  pancan_CR  pancan_PR  pancan_SD  pancan_PD  pub_n  pub_CR  pub_PR  pub_SD  pub_PD  cdr_n  cdr_CR  cdr_PR  cdr_SD  cdr_PD  any_n
platinum_exact_489 489       142        116          8         11          7    366     257      53      22      34    424     300      59      26      39    425
           cls_12m 214        52         43          3          5          1    184     125      30      12      17    191     131      30      12      18    191
           cls_18m 206        45         38          3          4          0    179     122      30      11      16    184     126      30      11      17    184
           cls_24m 199        40         35          1          4          0    175     120      28      11      16    179     123      28      11      17    179
           cox_432 432       133        108          7         11          7    327     231      43      20      33    378     269      47      24      38    379
```

## Agreement between copies (platinum cohort, patients with both)

- pancan vs pub: 108/109 = 0.991 [0.950, 0.998]
- pancan vs cdr: 141/142 = 0.993 [0.961, 0.999]
- pub vs cdr: 365/365 = 1.000 [0.990, 1.000]

## G3 concordance repeated with each response source (platinum cohort)

### pancan
- P(Resistant | PD), pub status: 1/3 = 0.333 [0.061, 0.792]
- P(short | PD), PFI-from-platinum: 2/5 = 0.400 [0.118, 0.769]
- P(Sensitive | CR), pub status: 51/55 = 0.927 [0.827, 0.971]
- P(long | CR), PFI-from-platinum: 74/80 = 0.925 [0.846, 0.965]
- P(Resistant | PD or SD), pub status: 3/8 = 0.375 [0.137, 0.694]

Cross-tab vs pub PLATINUM_STATUS:
```
pub_platinum_status  Missing  Resistant  Sensitive  Tooearly  absent
resp_pancan                                                         
CR                         9          4         51        25      27
NA                        70         80        130        30      37
PD                         3          1          2         0       1
PR                         1          0          4         0       3
SD                         4          2          3         2       0
```
Cross-tab vs PFI-from-first-line-platinum:
```
pfi_plat6_class  NA  indeterminate  long  short
resp_pancan                                    
CR                8             28    74      6
NA               44             12   187    104
PD                0              2     3      2
PR                1              1     6      0
SD                0              4     4      3
```

### pub
- P(Resistant | PD), pub status: 15/18 = 0.833 [0.608, 0.942]
- P(short | PD), PFI-from-platinum: 16/27 = 0.593 [0.407, 0.755]
- P(Sensitive | CR), pub status: 156/191 = 0.817 [0.756, 0.865]
- P(long | CR), PFI-from-platinum: 181/220 = 0.823 [0.767, 0.868]
- P(Resistant | PD or SD), pub status: 20/28 = 0.714 [0.529, 0.847]

Cross-tab vs pub PLATINUM_STATUS:
```
pub_platinum_status  Missing  Resistant  Sensitive  Tooearly  absent
resp_pub                                                            
CR                        23         35        156        43       0
NA                        21          9         13        12      68
PD                        16         15          3         0       0
PR                        17         23         13         0       0
SD                        10          5          5         2       0
```
Cross-tab vs PFI-from-first-line-platinum:
```
pfi_plat6_class  NA  indeterminate  long  short
resp_pub                                       
CR               13             24   181     39
NA               28             16    53     26
PD                5              2    11     16
PR                5              1    20     27
SD                2              4     9      7
```

### cdr
- P(Resistant | PD), pub status: 15/18 = 0.833 [0.608, 0.942]
- P(short | PD), PFI-from-platinum: 18/30 = 0.600 [0.423, 0.754]
- P(Sensitive | CR), pub status: 156/191 = 0.817 [0.756, 0.865]
- P(long | CR), PFI-from-platinum: 205/251 = 0.817 [0.764, 0.860]
- P(Resistant | PD or SD), pub status: 20/28 = 0.714 [0.529, 0.847]

Cross-tab vs pub PLATINUM_STATUS:
```
pub_platinum_status  Missing  Resistant  Sensitive  Tooearly  absent
resp_cdr                                                            
CR                        24         35        156        45      40
NA                        20          9         14        10      12
PD                        16         15          3         0       5
PR                        17         23         12         0       7
SD                        10          5          5         2       4
```
Cross-tab vs PFI-from-first-line-platinum:
```
pfi_plat6_class  NA  indeterminate  long  short
resp_cdr                                       
CR               21             28   205     46
NA               16             12    23     14
PD                7              2    12     18
PR                6              1    24     28
SD                3              4    10      9
```

## CDR-PD patients with PFI-from-platinum ≥183 d (n=12)

```
             pub_platinum_status  cdr_PFI  cdr_PFI_time_d  firstline_platinum_stop_d  pfi_from_platinum_d
PATIENT_ID                                                                                               
TCGA-04-1342             Missing      1.0           563.0                      142.0                421.0
TCGA-04-1343             Missing      1.0           361.0                      170.0                191.0
TCGA-09-0367             Missing      1.0           547.0                       92.0                455.0
TCGA-09-2054             Missing      1.0           637.0                      161.0                476.0
TCGA-23-1123             Missing      1.0          1018.0                      250.0                768.0
TCGA-23-2081             Missing      1.0          2342.0                      173.0               2169.0
TCGA-25-1320           Sensitive      1.0           424.0                      181.0                243.0
TCGA-25-2042             Missing      1.0           396.0                      123.0                273.0
TCGA-29-1766           Sensitive      1.0           672.0                      189.0                483.0
TCGA-57-1582             Missing      1.0           731.0                      170.0                561.0
TCGA-61-2002             Missing      0.0           547.0                      129.0                418.0
TCGA-61-2096                 NaN      1.0           421.0                       79.0                342.0
```