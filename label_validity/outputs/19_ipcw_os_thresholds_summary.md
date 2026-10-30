# A19 — IPCW sensitivity analysis of the OS thresholds as tests for platinum resistance

Python 3.10.12; lifelines 0.30.0; pandas 2.3.3; numpy 2.2.6

```
 threshold_months     measure  unweighted  ipcw_km  ipcw_km_lo  ipcw_km_hi  ipcw_cox  n_unweighted  n_cox  censored_before_t  censored_before_t_with_status
               18 sensitivity       0.214    0.206       0.126       0.294     0.191           268    245                 69                              8
               18 specificity       0.978    0.979       0.956       0.995     0.977           268    245                 69                              8
               18         PPV       0.818    0.815       0.641       0.956     0.801           268    245                 69                              8
               24 sensitivity       0.386    0.369       0.269       0.470     0.348           259    236                 87                             17
               24 specificity       0.938    0.940       0.904       0.972     0.945           259    236                 87                             17
               24         PPV       0.744    0.739       0.604       0.872     0.761           259    236                 87                             17
```

Largest |IPCW − unweighted|: 0.037. Decision rule — any difference > 0.05: False

IPCW assumes censoring independent of the outcome given the covariates; it does not address missing platinum status or unmeasured informative censoring.
