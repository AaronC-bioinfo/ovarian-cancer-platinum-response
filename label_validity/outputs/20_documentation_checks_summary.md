# A20 — Descriptive checks (fold counts, discordant patients, Cox assumptions)

Python 3.10.12; scikit-learn 1.7.2; lifelines 0.30.0; pandas 2.3.3

## C1 A16 folds

```
                patients  train_pos_min  train_pos_max  test_pos_min  test_pos_max  test_folds_without_positive  folds
label                                                                                                                 
label_os18           134              3              7             0             4                           22    100
label_os24           134             11             18             0             7                            3    100
label_platinum       134             31             32             7             8                            0    100
```

## C2 Discordant patients

```
              label_platinum src_platinum_status_raw  label_pfiplat6  pfi_from_platinum_d                          event_source provenance_class  redacted  adj_platinum_rows  adj_platinum_stop_missing  later_line_before_event  near_threshold  label_A1  label_A2  label_A3
PATIENT_ID                                                                                                                                                                                                                                                                     
TCGA-24-2029             0.0               Sensitive             1.0                154.0  recorded_new_tumour_event:Recurrence          flagged     False                  1                      False                    False            True       1.0       1.0       1.0
TCGA-29-1774             0.0               Sensitive             1.0                101.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  3                      False                    False           False       0.0       0.0       1.0
TCGA-61-2009             0.0               Sensitive             1.0                 18.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False       1.0       1.0       1.0
TCGA-61-2113             0.0               Sensitive             1.0                148.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False       1.0       1.0       1.0
```

## C3 Cox checks (A13b models)

```
                   outcome       covariate   n  events    HR  ph_test_p  quadratic_term_p
         PFI_from_platinum           age10 408     316 1.087      0.040             0.676
         PFI_from_platinum        stage_iv 407     315 1.289      0.570               NaN
         PFI_from_platinum residual_subopt 322     261 1.075      0.916               NaN
         PFI_from_platinum       resid_any 322     261 1.641      0.229               NaN
         PFI_from_platinum    brca_carrier 236     195 0.546      0.998               NaN
         PFI_from_platinum       ccne1_amp 356     285 1.579      0.481               NaN
         PFI_from_platinum   aneuploidy_sd 390     301 1.231      0.267             0.713
survival_after_progression           age10 331     237 1.259      0.155             0.567
survival_after_progression        stage_iv 331     237 1.029      0.760               NaN
survival_after_progression residual_subopt 267     202 1.411      0.342               NaN
survival_after_progression       resid_any 267     202 1.661      0.736               NaN
survival_after_progression    brca_carrier 201     152 0.681      0.309               NaN
survival_after_progression       ccne1_amp 294     218 1.184      0.168               NaN
survival_after_progression   aneuploidy_sd 317     225 1.026      0.022             0.281
```
