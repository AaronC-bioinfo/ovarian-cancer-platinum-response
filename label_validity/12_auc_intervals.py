#!/usr/bin/env python3
"""
label_validity/12_auc_intervals.py
──────────────────────────────────
A12 — descriptive: approximate 95% intervals for the within-TCGA cross-validated AUCs of A5
(no refitting). Added 2026-10-29 in response to the v3 reviews (no CI on within-TCGA AUCs).

For each train → test cell of a5_cross_label_repeats.csv: mean AUC over 3 models × 5 repeats,
the range over those 15 values, and a Hanley–McNeil (1982) normal-approximation 95% interval for
the mean AUC, using the cell's numbers of positive and negative patients. The Hanley–McNeil interval
treats the mean AUC as one AUC from n_pos and n_neg patients; it ignores between-repeat and
between-model variation and is reported only as an indication of precision.
Output → label_validity/outputs/a12_auc_intervals.csv
Run: python label_validity/12_auc_intervals.py
"""
import math
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parent / "outputs"


def hanley_mcneil(a: float, n1: int, n0: int) -> tuple[float, float, float]:
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    se = math.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))
    return se, a - 1.96 * se, a + 1.96 * se


r = pd.read_csv(OUT / "a5_cross_label_repeats.csv")
rows = []
for (tr, te), s in r.groupby(["train_label", "test_label"]):
    n, n1 = int(s.n.iloc[0]), int(s.n_pos.iloc[0])
    m = float(s.auc.mean())
    se, lo, hi = hanley_mcneil(m, n1, n - n1)
    rows.append(dict(train_label=tr, test_label=te, n=n, n_pos=n1, mean_auc=m, min_auc=float(s.auc.min()),
                     max_auc=float(s.auc.max()), hm_se=se, hm_lo=lo, hm_hi=hi))
d = pd.DataFrame(rows)
d.to_csv(OUT / "a12_auc_intervals.csv", index=False)
print(d[d.train_label == d.test_label].round(3).to_string(index=False))
print(d[(d.train_label != d.test_label) & (d.test_label == "label_platinum")].round(3).to_string(index=False))
