# A15 — Provenance of the re-derived platinum-free-interval label

Re-derived interval determinate: 389; overlap with platinum status: 272; added by reconstruction: 117 (26 resistant).

## Provenance class by group and label

```
provenance_class                             clean_resistant  clean_sensitive  flagged  negative_interval  All
group                        label_pfiplat6                                                                   
added_by_reconstruction      0.0                           0               73       18                  0   91
                             1.0                          17                0        8                  1   26
overlap_with_platinum_status 0.0                           0              160       23                  0  183
                             1.0                          75                0        7                  7   89
All                                                       92              233       56                  8  389
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
Added patients classed clean: 90/117.
Strict combined label: 367 determinate (104 resistant / 263 sensitive).

## The disagreements between platinum status and the re-derived interval

```
                                     group  label_platinum  label_pfiplat6  pfi_from_platinum_d                          event_source provenance_class  redacted  adj_platinum_rows  adj_platinum_stop_missing  later_line_before_event  near_threshold  disagreement src_platinum_status_raw
PATIENT_ID                                                                                                                                                                                                                                                                                   
TCGA-24-2029  overlap_with_platinum_status             0.0             1.0                154.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False            True          True               Sensitive
TCGA-29-1774  overlap_with_platinum_status             0.0             1.0                101.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  3                      False                    False           False          True               Sensitive
TCGA-61-2009  overlap_with_platinum_status             0.0             1.0                 18.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
TCGA-61-2113  overlap_with_platinum_status             0.0             1.0                148.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
```

## OS thresholds as tests: broad vs strict combined reference

- label_os18_all vs label_hybrid (n 375): sensitivity 29/108 = 0.27 [0.19, 0.36]; PPV 29/37 = 0.78 [0.63, 0.89]
- label_os24_all vs label_hybrid (n 360): sensitivity 47/107 = 0.44 [0.35, 0.53]; PPV 47/64 = 0.73 [0.62, 0.83]
- label_os18_all vs label_combined_strict (n 349): sensitivity 24/99 = 0.24 [0.17, 0.34]; PPV 24/30 = 0.80 [0.63, 0.90]
- label_os24_all vs label_combined_strict (n 335): sensitivity 40/98 = 0.41 [0.32, 0.51]; PPV 40/53 = 0.75 [0.62, 0.85]

## Prediction scorecard

~~(to be completed after the run)~~

Run 2026-10-29 ~22:00 ET in the cloud-linked VM (no model fitting), after the script with its predictions and decision rules was committed (d349b2b, 21:56:39 ET; now on GitHub main). All outputs have modification time 22:00:17 ET. The script does not record package versions; the VM's current interpreter is Python 3.10.12, pandas 2.3.3, numpy 2.2.6 (checked ~22:15 ET, after the run).

Correction to the script header: it says "Written 2026-10-29 ~22:15 ET, BEFORE the run". That time was a wrong estimate. The script was committed at 21:56:39 ET (d349b2b), so it was written before then. The commit timestamp is authoritative, and the run followed it.

Deviation (found when filling this scorecard): the header lists "interval within 150–215 days (near the 183-day cut-off)" among the flags, and defines "clean" as "no flag". The code (line 114) builds `any_flag` from the redacted record, the missing adjuvant stop date and the later-line flag only; `near_threshold` is computed but does not enter `provenance_class`. As implemented, 12 added patients with an interval of 150–215 days (5 resistant, 7 sensitive) are classed clean and enter the strict label. Under the header's definition:
- added patients not clean would be 39/117 (33%) instead of 27/117 (23%);
- the strict combined label would cover 355 patients (99 resistant / 256 sensitive) instead of 367 (104 / 263).
P1 and P4 do not depend on this (P4 counts flags and near-threshold intervals separately). P2 fails under either definition. The decision rule outcome is the same under either definition.

Resolution (Aaron, 2026-10-29, before the 15b run): the manuscript follows the header's definition. `15b_reconstruction_provenance_specfix.py` is this script with near_threshold added to any_flag and nothing else changed; it was run at 22:25 ET (outputs `a15b_*`, `15b_reconstruction_provenance_specfix_summary.md`). It gives 78/117 added patients clean and a strict combined label of 355 (99 resistant / 256 sensitive). Against that label, OS18 sensitivity is 0.23 [0.16, 0.33] and PPV 0.79 [0.60, 0.90]; OS24 sensitivity 0.41 [0.31, 0.51] and PPV 0.75 [0.61, 0.84]. These are still within 0.05 of the broad-label values, so P3 holds under either definition. The as-run label (367) is kept unchanged as `a15_label_combined_strict.csv`.

- **P1 — held (narrowly).** 20/26 resistant calls among the added patients (77%) are backed by a recorded new tumour event (Recurrence 13, Progression of Disease 3, type missing 4); threshold ≥ 75%. The other 6 are deaths counted as progression; none is unclear.
- **P2 — FAILED (narrowly).** The strict combined label covers 367 of 489 patients (104 resistant / 263 sensitive); predicted ≥ 370.
- **P3 — held.** Broad → strict combined reference: OS18 sensitivity 0.27 → 0.24, PPV 0.78 → 0.80; OS24 sensitivity 0.44 → 0.41, PPV 0.73 → 0.75. All within 0.05.
- **P4 — FAILED.** 1 of the 4 disagreements has a flag or a near-threshold interval: TCGA-24-2029 (154 d). The other three, TCGA-29-1774 (101 d), TCGA-61-2009 (18 d) and TCGA-61-2113 (148 d), are clean resistant calls (recorded Recurrence, no flag) that TCGA's platinum status records as Sensitive. They are not reconstruction artefacts that this audit can detect, and the available data do not explain them.

Decision (pre-specified rule): P1 held, but 27/117 (23%) of the added patients are not clean (> 20%; 33% under the header's definition). The manuscript therefore recommends the STRICT combined label (355, per the resolution above) as primary and reports the broad combined label (394) as a sensitivity analysis. It reports the provenance classes of the added patients and of the 4 disagreements, and the per-patient provenance table is released with the label resource.
