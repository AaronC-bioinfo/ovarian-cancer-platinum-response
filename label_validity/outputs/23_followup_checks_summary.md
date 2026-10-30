# A23 — Follow-up checks (IPCW population, anchor drugs, anchors in added patients, unknown event types)

Run 2026-10-30 05:05:10 UTC

## C1 IPCW variants

```
 threshold_months                 variant   n  sensitivity  specificity   ppv  max_weight     ess
               18              unweighted 268        0.214        0.978 0.818       1.000 268.000
               18               km_all489 268        0.206        0.979 0.815       1.172 267.934
               18         km_status_known 268        0.211        0.979 0.818       1.031 267.991
               18 km_stratified_by_status 268        0.211        0.979 0.820       1.039 267.986
               24              unweighted 259        0.386        0.938 0.744       1.000 259.000
               24               km_all489 259        0.369        0.940 0.739       1.235 258.789
               24         km_status_known 259        0.375        0.940 0.742       1.073 258.922
               24 km_stratified_by_status 259        0.379        0.940 0.744       1.077 258.923
```

A19 Cox-variant exclusions for missing covariates (patients with status and OS label): {18: 23, 24: 23}

Largest |change| from unweighted under the two new variants: 0.011; decision rule (> 0.05): False

## C2–C3 Anchor checks

```
                                 group         anchor   n  changed  became_undetermined  became_determinate
                       all determinate carbo_cis_only 389        0                    2                   0
                       all determinate             A1 389        5                    0                   0
                       all determinate             A2 389        5                    0                   0
                       all determinate             A3 389        0                    1                   0
                           added (117) carbo_cis_only 117        0                    1                   0
                           added (117)             A1 117        2                    0                   0
                           added (117)             A2 117        2                    0                   0
                           added (117)             A3 117        0                    1                   0
                  unflagged added (78) carbo_cis_only  78        0                    1                   0
                  unflagged added (78)             A1  78        0                    0                   0
                  unflagged added (78)             A2  78        0                    0                   0
                  unflagged added (78)             A3  78        0                    0                   0
                        discordant (4) carbo_cis_only   4        0                    0                   0
                        discordant (4)             A1   4        1                    0                   0
                        discordant (4)             A2   4        1                    0                   0
                        discordant (4)             A3   4        0                    0                   0
unflagged added resistant with RNA-seq carbo_cis_only   2        0                    0                   0
unflagged added resistant with RNA-seq             A1   2        0                    0                   0
unflagged added resistant with RNA-seq             A2   2        0                    0                   0
unflagged added resistant with RNA-seq             A3   2        0                    0                   0
```

## C4 Unflagged added resistant calls with an unrecorded event type: 2

Note (added after the run): the header's "Writing started 2026-10-30 01:05 ET" is the time the script was saved (05:05:09 UTC), one second before the run (05:05:10 UTC); writing began at about 01:04 ET. The time string was not changed.
