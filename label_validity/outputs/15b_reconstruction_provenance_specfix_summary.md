# A15b — Provenance of the re-derived platinum-free-interval label (correction run: near-threshold intervals flagged, per A15's header)

Re-derived interval determinate: 389; overlap with platinum status: 272; added by reconstruction: 117 (26 resistant).

## Provenance class by group and label

```
provenance_class                             clean_resistant  clean_sensitive  flagged  negative_interval  All
group                        label_pfiplat6                                                                   
added_by_reconstruction      0.0                           0               66       25                  0   91
                             1.0                          12                0       13                  1   26
overlap_with_platinum_status 0.0                           0              143       40                  0  183
                             1.0                          61                0       21                  7   89
All                                                       73              209       99                  8  389
```

## Event source of resistant calls

```
event_source                  death_counted_as_progression  recorded_new_tumour_event:Progression of Disease  recorded_new_tumour_event:Recurrence  recorded_new_tumour_event:nan  All
group                                                                                                                                                                                 
added_by_reconstruction                                  6                                                 3                                    13                              4   26
overlap_with_platinum_status                             0                                                12                                    77                              0   89
All                                                      6                                                15                                    90                              4  115
```

Added resistant calls backed by a recorded new tumour event: 20/26.
Added patients classed clean: 78/117.
Strict combined label: 355 determinate (99 resistant / 256 sensitive).

## The disagreements between platinum status and the re-derived interval

```
                                     group  label_platinum  label_pfiplat6  pfi_from_platinum_d                          event_source provenance_class  redacted  adj_platinum_rows  adj_platinum_stop_missing  later_line_before_event  near_threshold  disagreement src_platinum_status_raw
PATIENT_ID                                                                                                                                                                                                                                                                                   
TCGA-24-2029  overlap_with_platinum_status             0.0             1.0                154.0  recorded_new_tumour_event:Recurrence          flagged     False                  1                      False                    False            True          True               Sensitive
TCGA-29-1774  overlap_with_platinum_status             0.0             1.0                101.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  3                      False                    False           False          True               Sensitive
TCGA-61-2009  overlap_with_platinum_status             0.0             1.0                 18.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
TCGA-61-2113  overlap_with_platinum_status             0.0             1.0                148.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
```

## OS thresholds as tests: broad vs strict combined reference

- label_os18_all vs label_hybrid (n 375): sensitivity 29/108 = 0.27 [0.19, 0.36]; PPV 29/37 = 0.78 [0.63, 0.89]
- label_os24_all vs label_hybrid (n 360): sensitivity 47/107 = 0.44 [0.35, 0.53]; PPV 47/64 = 0.73 [0.62, 0.83]
- label_os18_all vs label_combined_strict (n 340): sensitivity 22/94 = 0.23 [0.16, 0.33]; PPV 22/28 = 0.79 [0.60, 0.90]
- label_os24_all vs label_combined_strict (n 327): sensitivity 38/93 = 0.41 [0.31, 0.51]; PPV 38/51 = 0.75 [0.61, 0.84]

## Note

Correction run; no new predictions. A15's predictions and decision rule are scored in 15_reconstruction_provenance_summary.md.
