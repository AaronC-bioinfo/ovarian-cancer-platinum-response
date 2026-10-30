# A21 — Event-type sensitivity of the re-derived interval label

Python 3.10.12; pandas 2.3.3

Patients whose resistant call is set aside: 10

```
label            label_pfiplat6  label_pfiplat6_rec
determinate          389.000000          379.000000
resistant            115.000000          105.000000
n_with_platinum      272.000000          272.000000
kappa_platinum         0.966209            0.966209
os18_n               375.000000          365.000000
os18_sens              0.268519            0.234694
os18_sens_lo           0.193949            0.161785
os18_sens_hi           0.358990            0.327618
os18_ppv               0.783784            0.741935
os18_ppv_lo            0.628049            0.567539
os18_ppv_hi            0.886135            0.862983
os24_n               360.000000          350.000000
os24_sens              0.439252            0.412371
os24_sens_lo           0.348941            0.319573
os24_sens_hi           0.533774            0.511845
os24_ppv               0.734375            0.701754
os24_ppv_lo            0.615171            0.573357
os24_ppv_hi            0.827036            0.804674
brca_or                0.370037            0.363598
brca_lo                0.140612            0.129066
brca_hi                0.867022            0.890512
brca_n               226.000000          218.000000
ccne1_or               1.762615            1.712692
ccne1_lo               0.976904            0.927169
ccne1_hi               3.152332            3.123952
ccne1_n              340.000000          331.000000
```

Decision rule — changes > 0.05: none; odds-ratio CIs changing side of 1: none

Note (added after the run): the header first gave its writing time as "00:29–00:33 ET", an estimate made before the run; the script was run at 00:30 ET, so the time string was corrected to 00:29–00:30 ET. Nothing else in the header was changed.
