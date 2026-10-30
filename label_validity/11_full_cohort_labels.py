#!/usr/bin/env python3
"""
label_validity/11_full_cohort_labels.py
───────────────────────────────────────
A11 — descriptive extension of A1/A2 to the full platinum-treated cohort (no new predictions).

Why: A8–A10 showed that the OS-threshold labels must be compared with the platinum labels in the
same, full cohort (489 platinum-treated patients), not only in the RNA-seq subset used by A2. This
script derives no new kind of result. It (1) writes the per-patient label table used by the
reframed manuscript and its figures, and (2) recomputes A2's agreement and sensitivity/specificity
with the full-cohort OS labels, using A2's code and settings unchanged (κ with 2,000-resample
percentile bootstrap, seed 42; Wilson 95% intervals). It adds PPV/NPV with Wilson intervals.
Written 2026-10-29 ~20:00 ET after A8–A10 had been run; A9 had already reported point estimates
of the same sensitivity/specificity/PPV.

Labels (1 = non-responder / resistant)
  label_platinum, label_pfiplat6, label_response   from labels_master.csv (A1)
  label_os18_all, label_os24_all                   OS < 18 / 24 months for all platinum-treated patients,
                                                   recomputed with src.preprocessing exactly as in A8–A10
  label_hybrid                                     label_platinum where determinate, else label_pfiplat6 (A9 Part C)

Outputs → label_validity/outputs/labels_full.csv, a11_coverage.csv, a11_kappa_full.csv,
          a11_os_test_full.csv, 11_full_cohort_labels_summary.md
Run (from the repo root; no model fitting):
  python label_validity/11_full_cohort_labels.py --data-root "<...>/OV Data/Project data"
"""

from __future__ import annotations

import argparse
import itertools
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.preprocessing import assign_response_label, extract_survival  # noqa: E402

OUT = ROOT / "label_validity" / "outputs"
SEED, B = 42, 2000
LABELS = ["label_platinum", "label_pfiplat6", "label_response", "label_os18_all", "label_os24_all"]


# ── copied unchanged from 02_label_agreement.py ─────────────────────────────
def kappa(a: np.ndarray, b: np.ndarray) -> float:
    po = np.mean(a == b)
    pa1, pb1 = a.mean(), b.mean()
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def boot_kappa(a, b, rng) -> tuple[float, float]:
    n = len(a)
    ks = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        k = kappa(a[i], b[i])
        if not math.isnan(k):
            ks.append(k)
    return float(np.percentile(ks, 2.5)), float(np.percentile(ks, 97.5))


def wilson(k: int, n: int) -> tuple[float, float, float]:
    if n == 0:
        return (float("nan"),) * 3
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)
# ─────────────────────────────────────────────────────────────────────────────


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    a = ap.parse_args()
    dr = Path(a.data_root)

    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    clin = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_clinical_patient.txt", sep="\t", comment="#")
    surv = extract_survival(clin, "OS_MONTHS", "OS_STATUS")
    surv = surv[surv["PATIENT_ID"].isin(m.index)].set_index("PATIENT_ID")
    for thr in (18, 24):
        m[f"label_os{thr}_all"] = assign_response_label(surv, "OS_MONTHS", thr).reindex(m.index)
        chk = m[[f"label_os{thr}", f"label_os{thr}_all"]].dropna(subset=[f"label_os{thr}"])
        assert int((chk.iloc[:, 0] != chk.iloc[:, 1]).sum()) == 0
    m["label_hybrid"] = m["label_platinum"].where(m["label_platinum"].notna(), m["label_pfiplat6"])
    keep = ["in_rnaseq", "src_platinum_status_raw"] + LABELS + ["label_hybrid", "label_os18", "label_os24"]
    m[keep].to_csv(OUT / "labels_full.csv")

    cov = []
    for lab in LABELS + ["label_hybrid"]:
        s = m[lab]
        cov.append(dict(label=lab, determinate=int(s.notna().sum()), pos=int((s == 1).sum()),
                        neg=int((s == 0).sum()), of=len(m),
                        determinate_rnaseq=int(s[m.in_rnaseq.astype(bool)].notna().sum())))
    cov = pd.DataFrame(cov); cov.to_csv(OUT / "a11_coverage.csv", index=False)

    rng = np.random.default_rng(SEED)
    rows = []
    for x, y in itertools.combinations(LABELS, 2):
        s = m[[x, y]].dropna()
        aa, bb = s[x].to_numpy(int), s[y].to_numpy(int)
        lo, hi = boot_kappa(aa, bb, rng)
        rows.append(dict(label_a=x, label_b=y, n=len(s), agreement=float(np.mean(aa == bb)),
                         kappa=kappa(aa, bb), kappa_lo=lo, kappa_hi=hi))
    kp = pd.DataFrame(rows); kp.to_csv(OUT / "a11_kappa_full.csv", index=False)

    tests = []
    for ref in ["label_platinum", "label_hybrid"]:
        for t in ["label_os18_all", "label_os24_all"]:
            s = m[[ref, t]].dropna()
            r, tt = s[ref].to_numpy(int), s[t].to_numpy(int)
            tp = int(((r == 1) & (tt == 1)).sum()); fn = int(((r == 1) & (tt == 0)).sum())
            tn = int(((r == 0) & (tt == 0)).sum()); fp = int(((r == 0) & (tt == 1)).sum())
            row = dict(reference=ref, os_label=t, n=len(s), tp=tp, fn=fn, tn=tn, fp=fp)
            for name, k, n in [("sensitivity", tp, tp + fn), ("specificity", tn, tn + fp),
                               ("ppv", tp, tp + fp), ("npv", tn, tn + fn)]:
                p, lo, hi = wilson(k, n)
                row.update({name: p, f"{name}_lo": lo, f"{name}_hi": hi})
            tests.append(row)
    ts = pd.DataFrame(tests); ts.to_csv(OUT / "a11_os_test_full.csv", index=False)

    L = ["# A11 — Full-cohort label table, coverage, agreement and OS-as-test (descriptive)", "",
         "## Coverage (of 489 platinum-treated patients)", ""]
    for r in cov.itertuples():
        L.append(f"- {r.label}: {r.determinate} determinate ({r.pos} non-responder / {r.neg} responder); "
                 f"{r.determinate_rnaseq} with RNA-seq")
    L += ["", "## Cohen's κ (full cohort; 2,000-resample bootstrap, seed 42)", ""]
    for r in kp.itertuples():
        L.append(f"- {r.label_a} × {r.label_b}: κ {r.kappa:.3f} [{r.kappa_lo:.3f}, {r.kappa_hi:.3f}], "
                 f"agreement {r.agreement:.3f}, n {r.n}")
    L += ["", "## OS labels as a test for platinum resistance (Wilson 95% CI)", ""]
    for r in ts.itertuples():
        L.append(f"- {r.os_label} vs {r.reference} (n {r.n}): sensitivity {r.tp}/{r.tp + r.fn} = {r.sensitivity:.2f} "
                 f"[{r.sensitivity_lo:.2f}, {r.sensitivity_hi:.2f}]; specificity {r.tn}/{r.tn + r.fp} = {r.specificity:.2f} "
                 f"[{r.specificity_lo:.2f}, {r.specificity_hi:.2f}]; PPV {r.tp}/{r.tp + r.fp} = {r.ppv:.2f} "
                 f"[{r.ppv_lo:.2f}, {r.ppv_hi:.2f}]; NPV {r.npv:.2f} [{r.npv_lo:.2f}, {r.npv_hi:.2f}]")
    (OUT / "11_full_cohort_labels_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
