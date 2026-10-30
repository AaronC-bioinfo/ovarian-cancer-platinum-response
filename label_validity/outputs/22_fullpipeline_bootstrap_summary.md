# A22 — Full-pipeline (out-of-bag bootstrap) uncertainty for the controlled label comparison

Python 3.10.12; scikit-learn 1.7.2; numpy 2.2.6; pandas 2.3.3

Chunks run: 2026-10-30 04:31:41 UTC – 2026-10-30 04:41:25 UTC; skipped replicates: 0

```
           contrast  usable_replicates  oob_median  full_lo  full_hi  full_width  conditional_estimate  conditional_lo  conditional_hi  conditional_width  full_excludes_0
     primary_dAUC24                500       0.010   -0.183    0.157       0.340                -0.005          -0.105           0.087              0.193            False
             dAUC18                500       0.063   -0.145    0.244       0.390                 0.080          -0.045           0.201              0.246            False
reverse_OS24_target                500      -0.004   -0.233    0.218       0.451                -0.069          -0.236           0.081              0.317            False
```

P1 (full-pipeline interval for ΔAUC_24 wider than the conditional interval): held (0.340 vs 0.193).
Decision rule: full-pipeline interval for ΔAUC_24 excludes 0: False.

Notes (added after the run): the header's conditional width "0.192" is 0.1925 unrounded (printed 0.193 above). Chunks were run as replicates 0–20, 20–160, 160–300, 300–440 and 440–500 rather than the 100-replicate chunks shown in the header's run line; each replicate has its own seed, so the chunking does not affect the results. The fits used scikit-learn 1.7.2, in which random-forest fits differ slightly from the A16 environment (scikit-learn 1.9.0).
