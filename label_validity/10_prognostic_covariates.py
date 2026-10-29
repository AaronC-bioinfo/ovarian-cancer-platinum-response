#!/usr/bin/env python3
"""
label_validity/10_prognostic_covariates.py
──────────────────────────────────────────
Q2 analysis A10 — do the OS-threshold labels track prognostic covariates (aneuploidy, residual
disease) differently from platinum status, in the FULL platinum-treated cohort and in the same patients?

Written 2026-10-29 ~19:35 ET, BEFORE the run. Prompted by A8/A9: A3 tested the OS labels only in the
RNA-seq subset (label_os18 / label_os24), while the platinum labels were tested in the full cohort.
The v3 claim "OS labels track aneuploidy and residual disease, platinum status does not" therefore
compared different patients.

DISCLOSURE — what was seen before these predictions were written
  * A3 results (a3_known_groups.csv): aneuploidy rank-biserial r: platinum +0.13 (q 0.21), pfiplat6
    +0.21, response −0.03, OS18 (RNA-seq) +0.42, OS24 (RNA-seq) +0.33. Suboptimal residual OR:
    platinum 1.12, pfiplat6 1.25, response 2.55, OS18 3.60 [1.16, 11.88], OS24 2.26 [0.93, 5.47].
    Stage IV: no label associated.
  * A8/A9 results (BRCA, CCNE1, OS label metrics, missingness).
  NOT seen: any covariate test with OS labels in the full cohort; any same-patient comparison.

Population and labels
  Platinum-treated patients (A1, n = 489). label_platinum, label_pfiplat6, label_response from
  labels_master.csv. label_os18_all / label_os24_all recomputed for all 489 exactly as in A8.
  Covariates from a3_covariates.csv (A3): aneuploidy, tmb, age, stage_iv, residual_subopt.

Tests (fixed before running)
  T1  Each label × covariate in all determinate patients: Fisher exact with conditional OR (binary
      covariates) or Mann–Whitney U with rank-biserial r (continuous; r > 0 = higher in label = 1).
      BH across the 5 covariates within each label.
  T2  COMMON SET: patients with label_platinum, label_os18_all and label_os24_all all determinate and
      the covariate non-missing. Per-label statistic in the common set. Then differences,
      OS18 − platinum and OS24 − platinum:
        aneuploidy: difference in rank-biserial r;
        residual_subopt: difference in log OR (Haldane 0.5).
      95% percentile CIs from 2,000 bootstrap resamples of patients (numpy default_rng(42)).

PREDICTIONS
  R1  Full cohort: aneuploidy r > 0 with BH q < 0.05 for label_os18_all and label_os24_all.
  R2  Full cohort: residual_subopt OR > 1 for label_os18_all and label_os24_all; 95% CI excludes 1 for
      label_os18_all.
  R3  Common set: point estimate of r(OS24) − r(platinum) for aneuploidy > 0, with 95% CI including 0.
  R4  Common set: point estimate of log OR(OS18) − log OR(platinum) for residual > 0, with 95% CI
      including 0.

DECISION RULES (for the manuscript)
  * If a T2 difference CI excludes 0 (OS label > platinum), the manuscript states that the OS label
    tracks that covariate more strongly than platinum status in the same patients, with the CI, as
    evidence that the OS labels carry prognostic content beyond platinum response.
  * If the T2 CIs include 0, the manuscript reports the per-label associations descriptively and does
    NOT claim that the OS labels track these covariates differently from platinum status.

Inputs: label_validity/outputs/labels_master.csv, a3_covariates.csv;
        <data-root>/ov_tcga_pan_can_atlas_2018/data_clinical_patient.txt
Outputs → label_validity/outputs/a10_tests.csv, a10_diff.csv, 10_prognostic_covariates_summary.md
Run (from the repo root; no model fitting):
  python label_validity/10_prognostic_covariates.py --data-root "<...>/OV Data/Project data"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu
from scipy.stats.contingency import odds_ratio

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.preprocessing import assign_response_label, extract_survival  # noqa: E402

OUT_DEFAULT = ROOT / "label_validity" / "outputs"
LABELS = ["label_platinum", "label_pfiplat6", "label_response", "label_os18_all", "label_os24_all"]
BIN = ["residual_subopt", "stage_iv"]
CONT = ["aneuploidy", "tmb", "age"]
N_BOOT, SEED = 2000, 42


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.minimum(q, 1.0)


def rbc(x, y) -> float:
    """rank-biserial r; > 0 means higher x in y == 1."""
    a, b = x[y == 1], x[y == 0]
    u = mannwhitneyu(a, b).statistic
    return float(2 * u / (len(a) * len(b)) - 1)


def log_or_h(x, y) -> float:
    a = np.sum((x == 1) & (y == 1)) + 0.5; b = np.sum((x == 1) & (y == 0)) + 0.5
    c = np.sum((x == 0) & (y == 1)) + 0.5; d = np.sum((x == 0) & (y == 0)) + 0.5
    return float(np.log(a * d / (b * c)))


def test(lab, cov, d) -> dict:
    d = d[[lab, cov]].dropna()
    y = d[lab].to_numpy().astype(int); x = d[cov].to_numpy()
    if cov in BIN:
        x = x.astype(int)
        t = [[int(((x == 1) & (y == 1)).sum()), int(((x == 1) & (y == 0)).sum())],
             [int(((x == 0) & (y == 1)).sum()), int(((x == 0) & (y == 0)).sum())]]
        r = odds_ratio(t, kind="conditional"); ci = r.confidence_interval(0.95)
        return dict(label=lab, covariate=cov, n=len(d), stat="OR", value=float(r.statistic),
                    lo=float(ci.low), hi=float(ci.high), p=float(fisher_exact(t)[1]))
    return dict(label=lab, covariate=cov, n=len(d), stat="rank_biserial_r", value=rbc(x, y),
                lo=np.nan, hi=np.nan, p=float(mannwhitneyu(x[y == 1], x[y == 0]).pvalue))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    a = ap.parse_args()
    dr, out = Path(a.data_root), Path(a.out)

    m = pd.read_csv(OUT_DEFAULT / "labels_master.csv", index_col=0)
    clin = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_clinical_patient.txt", sep="\t", comment="#")
    surv = extract_survival(clin, "OS_MONTHS", "OS_STATUS")
    surv = surv[surv["PATIENT_ID"].isin(m.index)].set_index("PATIENT_ID")
    for thr in (18, 24):
        m[f"label_os{thr}_all"] = assign_response_label(surv, "OS_MONTHS", thr).reindex(m.index)
        chk = m[[f"label_os{thr}", f"label_os{thr}_all"]].dropna(subset=[f"label_os{thr}"])
        assert int((chk.iloc[:, 0] != chk.iloc[:, 1]).sum()) == 0
    m = m.join(pd.read_csv(OUT_DEFAULT / "a3_covariates.csv", index_col=0)[BIN + CONT])

    rows = []
    for lab in LABELS:
        rr = [dict(set="T1_all", **test(lab, c, m)) for c in BIN + CONT]
        q = bh([r["p"] for r in rr])
        for r, qq in zip(rr, q):
            r["q_bh"] = float(qq)
        rows += rr

    common = m.dropna(subset=["label_platinum", "label_os18_all", "label_os24_all"])
    for lab in ["label_platinum", "label_os18_all", "label_os24_all"]:
        for c in ["aneuploidy", "residual_subopt"]:
            rows.append(dict(set="T2_common", **test(lab, c, common), q_bh=np.nan))
    res = pd.DataFrame(rows); res.to_csv(out / "a10_tests.csv", index=False)

    rng = np.random.default_rng(SEED)
    diffs = []
    for cov, fn in [("aneuploidy", rbc), ("residual_subopt", log_or_h)]:
        d = common[["label_platinum", "label_os18_all", "label_os24_all", cov]].dropna()
        X = d[cov].to_numpy()
        if cov == "residual_subopt":
            X = X.astype(int)
        Y = {l: d[l].to_numpy().astype(int) for l in ["label_platinum", "label_os18_all", "label_os24_all"]}
        for os_lab in ["label_os18_all", "label_os24_all"]:
            est = fn(X, Y[os_lab]) - fn(X, Y["label_platinum"])
            bs = np.empty(N_BOOT)
            for i in range(N_BOOT):
                idx = rng.integers(0, len(d), len(d))
                bs[i] = fn(X[idx], Y[os_lab][idx]) - fn(X[idx], Y["label_platinum"][idx])
            lo, hi = np.percentile(bs, [2.5, 97.5])
            diffs.append(dict(covariate=cov, contrast=f"{os_lab} − label_platinum", n=len(d),
                              measure="Δ rank-biserial r" if cov == "aneuploidy" else "Δ log OR (Haldane)",
                              estimate=est, lo=lo, hi=hi, ci_includes_0=bool(lo <= 0 <= hi)))
    dd = pd.DataFrame(diffs); dd.to_csv(out / "a10_diff.csv", index=False)

    L = ["# A10 — Prognostic covariates by label, full cohort and same patients", "",
         f"Common set (platinum, OS18_all, OS24_all determinate): n = {len(common)}.", "",
         "## T1 — all determinate patients (BH across 5 covariates within label)", ""]
    for lab in LABELS:
        L.append(f"**{lab}**")
        for r in res[(res.set == "T1_all") & (res.label == lab)].itertuples():
            ci = f" [{r.lo:.2f}, {r.hi:.2f}]" if r.stat == "OR" else ""
            L.append(f"- {r.covariate}: {r.stat} {r.value:+.3f}{ci}; n {r.n}; p {r.p:.3g}; q {r.q_bh:.3g}")
        L.append("")
    L += ["## T2 — common set", ""]
    for r in res[res.set == "T2_common"].itertuples():
        ci = f" [{r.lo:.2f}, {r.hi:.2f}]" if r.stat == "OR" else ""
        L.append(f"- {r.label} × {r.covariate}: {r.stat} {r.value:+.3f}{ci}; n {r.n}; p {r.p:.3g}")
    L += ["", "Differences (2,000 bootstrap resamples):", ""]
    for r in dd.itertuples():
        L.append(f"- {r.covariate}, {r.contrast}: {r.measure} {r.estimate:+.3f} [{r.lo:+.3f}, {r.hi:+.3f}] "
                 f"(n {r.n}); CI includes 0: {r.ci_includes_0}")
    L += ["", "## Prediction scorecard", "", "(to be completed after the run)", ""]
    (out / "10_prognostic_covariates_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("A10 done")


if __name__ == "__main__":
    main()
