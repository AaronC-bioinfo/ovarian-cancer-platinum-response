#!/usr/bin/env python3
"""
label_validity/09_platinum_missingness.py
─────────────────────────────────────────
Q2 analysis A9 — who lacks a determinate TCGA platinum status, and what the OS-threshold labels
capture.

Written 2026-10-29 ~19:40 ET, BEFORE the run. Prompted by the v3 peer review
(review_v3/PEER_REVIEW.md, major concerns 2–3): most early deaths appear to lack a platinum status,
so the primary label may be missing selectively among the patients most likely to be resistant.

DISCLOSURE — what was seen before these predictions were written
  * src_platinum_status_raw counts in the 489 platinum-treated patients: Sensitive 190, Resistant 87,
    Missing 87, Tooearly 57, absent from ov_tcga_pub 68.
  * In the RNA-seq OS cohorts (labels_master): of 22 patients with label_os18 = 1, 13 Missing,
    2 absent, 5 Resistant, 2 Sensitive; of 36 with label_os24 = 1, 16 Missing, 2 absent, 11 Resistant,
    7 Sensitive. Cross-tabs of label_os18/24 × label_platinum (PPV 5/7 and 11/18).
  * The 19 patients with a negative PFI-from-platinum interval: 10 Tooearly, 7 Resistant, 2 Missing.
  NOT seen: survival by status group; OS labels in the full cohort by status; pfiplat6, response,
  residual, stage or age by status group; the hybrid label; κmax/PABAK.
  Q2 and Q6 are therefore partly informed by the RNA-seq-subset counts above.

Populations
  PRIMARY: platinum-treated patients (A1, n = 489) present in the TCGA 2011 release (ov_tcga_pub),
    i.e. src_platinum_status_raw != "absent". Groups: DETERMINATE (Resistant, Sensitive) vs
    UNDETERMINED (Missing, Tooearly), with Missing and Tooearly also reported separately.
  SECONDARY: all 489, with "absent" added to UNDETERMINED.

Part A — comparison of DETERMINATE vs UNDETERMINED (primary population)
  A1  Overall survival (OS_MONTHS, OS_STATUS, PanCancer clinical): Kaplan–Meier median per group;
      two-sided log-rank test (chi-square, 1 df), implemented here.
  A2  Death before 18 and before 24 months (label_os18_all / label_os24_all as in A8: censored before
      the threshold excluded): proportion per group; Fisher exact OR (undetermined vs determinate).
  A3  Re-derived interval (label_pfiplat6, where determinate): proportion resistant per group; Fisher OR.
  A4  First-course response (label_response, PD/SD = 1): proportion per group; Fisher OR.
  A5  Descriptive only: suboptimal residual disease, stage IV, age (a3_covariates.csv); Fisher /
      Mann–Whitney p reported without a prediction.
Part B — what the OS-threshold labels capture (against label_platinum)
  In the RNA-seq subset (label_os18/24, as in A2) and in the full cohort (label_os18_all/24_all):
  sensitivity, specificity, PPV, NPV, LR+, Cohen's κ, maximum attainable κ given the marginals,
  and PABAK (2·p_o − 1).
Part C — descriptive: a "hybrid" platinum label = label_platinum where determinate, otherwise
  label_pfiplat6. Coverage and prevalence in the 489, and Part B metrics of OS labels against it.

PREDICTIONS
  Q1  UNDETERMINED patients have shorter OS than DETERMINATE: lower KM median and log-rank p < 0.05.
  Q2  Death before 18 months is more common in UNDETERMINED (Fisher OR > 1, p < 0.05).
  Q3  Among patients with label_pfiplat6 determinate, the resistant proportion is higher in UNDETERMINED
      (OR > 1).
  Q4  First-course PD/SD is more common in UNDETERMINED (OR > 1).
  Q6  Full cohort: PPV of label_os18_all and label_os24_all for platinum resistance ≥ 0.60, and
      sensitivity ≤ 0.30.

DECISION RULES (for the manuscript)
  * If Q1 holds and Q3 or Q4 holds: the manuscript states that TCGA platinum status is missing
    selectively among patients with poor outcomes ("valid but incomplete"). All agreement and
    sensitivity analyses of OS labels against platinum status are described as conditional on a
    determinate status, and the hybrid label is reported as a sensitivity analysis.
  * If Q1 fails: missingness is described as not associated with survival, and the framing does not
    rest on selective missingness.
  * Part B results replace the "OS labels miss most resistant patients" framing with the full set of
    sensitivity / PPV / LR+ / κmax, whatever they show.

Inputs
  label_validity/outputs/labels_master.csv, a3_covariates.csv
  <data-root>/ov_tcga_pan_can_atlas_2018/data_clinical_patient.txt
Outputs → label_validity/outputs/a9_group_tests.csv, a9_os_label_metrics.csv, a9_km.csv,
          09_platinum_missingness_summary.md
Run (from the repo root; no model fitting):
  python label_validity/09_platinum_missingness.py --data-root "<...>/OV Data/Project data"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import chi2, fisher_exact, mannwhitneyu
from scipy.stats.contingency import odds_ratio

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.preprocessing import assign_response_label, extract_survival  # noqa: E402

OUT_DEFAULT = ROOT / "label_validity" / "outputs"


def km_median(t: np.ndarray, e: np.ndarray) -> float:
    order = np.argsort(t)
    t, e = t[order], e[order]
    s, n = 1.0, len(t)
    for i, ti in enumerate(np.unique(t)):
        at_risk = np.sum(t >= ti)
        d = np.sum((t == ti) & (e == 1))
        if at_risk > 0:
            s *= 1 - d / at_risk
        if s <= 0.5:
            return float(ti)
    return float("nan")


def logrank(t1, e1, t2, e2) -> tuple[float, float]:
    t = np.concatenate([t1, t2]); e = np.concatenate([e1, e2])
    g = np.concatenate([np.ones(len(t1)), np.zeros(len(t2))])
    O_E, V = 0.0, 0.0
    for ti in np.unique(t[e == 1]):
        r = t >= ti
        n, n1 = r.sum(), (r & (g == 1)).sum()
        d = ((t == ti) & (e == 1)).sum()
        d1 = ((t == ti) & (e == 1) & (g == 1)).sum()
        O_E += d1 - d * n1 / n
        if n > 1:
            V += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
    stat = O_E ** 2 / V
    return float(stat), float(chi2.sf(stat, 1))


def fisher_row(name, x, y) -> dict:
    a = int(((x == 1) & (y == 1)).sum()); b = int(((x == 1) & (y == 0)).sum())
    c = int(((x == 0) & (y == 1)).sum()); d = int(((x == 0) & (y == 0)).sum())
    res = odds_ratio([[a, b], [c, d]], kind="conditional"); ci = res.confidence_interval(0.95)
    return dict(test=name, undet_pos=a, undet_n=a + b, det_pos=c, det_n=c + d,
                OR=float(res.statistic), lo=float(ci.low), hi=float(ci.high),
                p=float(fisher_exact([[a, b], [c, d]])[1]))


def label_metrics(name, os_lab, ref) -> dict:
    d = pd.DataFrame({"t": os_lab, "r": ref}).dropna()
    tp = int(((d.t == 1) & (d.r == 1)).sum()); fp = int(((d.t == 1) & (d.r == 0)).sum())
    fn = int(((d.t == 0) & (d.r == 1)).sum()); tn = int(((d.t == 0) & (d.r == 0)).sum())
    n = tp + fp + fn + tn
    po = (tp + tn) / n
    p_t, p_r = (tp + fp) / n, (tp + fn) / n
    pe = p_t * p_r + (1 - p_t) * (1 - p_r)
    kappa = (po - pe) / (1 - pe)
    po_max = 1 - abs(p_t - p_r)
    sens = tp / (tp + fn) if tp + fn else np.nan
    spec = tn / (tn + fp) if tn + fp else np.nan
    return dict(comparison=name, n=n, tp=tp, fp=fp, fn=fn, tn=tn, sensitivity=sens, specificity=spec,
                ppv=tp / (tp + fp) if tp + fp else np.nan, npv=tn / (tn + fn) if tn + fn else np.nan,
                lr_pos=sens / (1 - spec) if spec < 1 else np.inf, kappa=kappa,
                kappa_max=(po_max - pe) / (1 - pe), pabak=2 * po - 1, prevalence_ref=p_r)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    a = ap.parse_args()
    dr, out = Path(a.data_root), Path(a.out)

    m = pd.read_csv(OUT_DEFAULT / "labels_master.csv", index_col=0)
    cov = pd.read_csv(OUT_DEFAULT / "a3_covariates.csv", index_col=0)
    clin = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_clinical_patient.txt", sep="\t", comment="#")
    surv = extract_survival(clin, "OS_MONTHS", "OS_STATUS")
    surv = surv[surv["PATIENT_ID"].isin(m.index)].set_index("PATIENT_ID")
    m["os_months"] = surv["OS_MONTHS"].reindex(m.index)
    m["os_event"] = surv["event"].reindex(m.index)
    for thr in (18, 24):
        m[f"label_os{thr}_all"] = assign_response_label(surv, "OS_MONTHS", thr).reindex(m.index)
    m = m.join(cov[["residual_subopt", "stage_iv", "age"]])

    st = m["src_platinum_status_raw"]
    m["undet_primary"] = np.where(st.isin(["Resistant", "Sensitive"]), 0,
                                  np.where(st.isin(["Missing", "Tooearly"]), 1, np.nan))
    m["undet_all"] = np.where(st.isin(["Resistant", "Sensitive"]), 0, 1)

    rows, km = [], []
    for pop, gcol in [("primary_in_2011_release", "undet_primary"), ("secondary_all_489", "undet_all")]:
        d = m.dropna(subset=[gcol])
        # A1 survival
        s = d.dropna(subset=["os_months", "os_event"])
        u, k = s[s[gcol] == 1], s[s[gcol] == 0]
        stat, p = logrank(u.os_months.to_numpy(), u.os_event.to_numpy(), k.os_months.to_numpy(), k.os_event.to_numpy())
        for grp, sub in [("undetermined", u), ("determinate", k)] + (
                [(lvl, s[st.reindex(s.index) == lvl]) for lvl in ["Missing", "Tooearly", "Resistant", "Sensitive", "absent"]]
                if pop == "secondary_all_489" else []):
            if len(sub):
                km.append(dict(population=pop, group=grp, n=len(sub), deaths=int(sub.os_event.sum()),
                               km_median_months=km_median(sub.os_months.to_numpy(), sub.os_event.to_numpy())))
        rows.append(dict(population=pop, test="A1_logrank_OS", undet_n=len(u), det_n=len(k), stat=stat, p=p))
        for name, col in [("A2_death_lt18", "label_os18_all"), ("A2_death_lt24", "label_os24_all"),
                          ("A3_pfiplat6_resistant", "label_pfiplat6"), ("A4_response_PDSD", "label_response"),
                          ("A5_residual_subopt", "residual_subopt"), ("A5_stage_iv", "stage_iv")]:
            dd = d[[gcol, col]].dropna()
            rows.append(dict(population=pop, **fisher_row(name, dd[gcol].astype(int), dd[col].astype(int))))
        dd = d[[gcol, "age"]].dropna()
        x1, x0 = dd[dd[gcol] == 1].age, dd[dd[gcol] == 0].age
        rows.append(dict(population=pop, test="A5_age_mannwhitney", undet_n=len(x1), det_n=len(x0),
                         stat=float(x1.median() - x0.median()), p=float(mannwhitneyu(x1, x0).pvalue)))
    res = pd.DataFrame(rows); res.to_csv(out / "a9_group_tests.csv", index=False)
    kmdf = pd.DataFrame(km); kmdf.to_csv(out / "a9_km.csv", index=False)

    # Part B / C
    m["label_hybrid"] = m["label_platinum"].where(m["label_platinum"].notna(), m["label_pfiplat6"])
    met = [label_metrics("os18_rnaseq vs platinum", m.label_os18, m.label_platinum),
           label_metrics("os24_rnaseq vs platinum", m.label_os24, m.label_platinum),
           label_metrics("os18_all vs platinum", m.label_os18_all, m.label_platinum),
           label_metrics("os24_all vs platinum", m.label_os24_all, m.label_platinum),
           label_metrics("os18_all vs hybrid", m.label_os18_all, m.label_hybrid),
           label_metrics("os24_all vs hybrid", m.label_os24_all, m.label_hybrid)]
    metdf = pd.DataFrame(met); metdf.to_csv(out / "a9_os_label_metrics.csv", index=False)

    def fr(r):
        return (f"{int(r.undet_pos)}/{int(r.undet_n)} vs {int(r.det_pos)}/{int(r.det_n)}; "
                f"OR {r.OR:.2f} [{r.lo:.2f}, {r.hi:.2f}], p {r.p:.3g}")
    L = ["# A9 — Who lacks a determinate platinum status; what OS labels capture", ""]
    for pop in ["primary_in_2011_release", "secondary_all_489"]:
        L += [f"## Part A — {pop} (undetermined vs determinate)", ""]
        r = res[(res.population == pop) & (res.test == "A1_logrank_OS")].iloc[0]
        L.append(f"- A1 OS log-rank: n {int(r.undet_n)} vs {int(r.det_n)}; chi² {r.stat:.2f}, p {r.p:.3g}")
        for g in kmdf[kmdf.population == pop].itertuples():
            L.append(f"  - KM median OS, {g.group}: {g.km_median_months:.1f} months (n {g.n}, deaths {g.deaths})")
        for t in ["A2_death_lt18", "A2_death_lt24", "A3_pfiplat6_resistant", "A4_response_PDSD",
                  "A5_residual_subopt", "A5_stage_iv"]:
            L.append(f"- {t}: {fr(res[(res.population == pop) & (res.test == t)].iloc[0])}")
        r = res[(res.population == pop) & (res.test == "A5_age_mannwhitney")].iloc[0]
        L.append(f"- A5 age: median difference {r.stat:+.1f} years, p {r.p:.3g}")
        L.append("")
    L += ["## Part B/C — OS labels against platinum status and the hybrid label", ""]
    for r in metdf.itertuples():
        L.append(f"- {r.comparison}: n {r.n}; sens {r.tp}/{r.tp + r.fn} = {r.sensitivity:.2f}; "
                 f"spec {r.specificity:.2f}; PPV {r.tp}/{r.tp + r.fp} = {r.ppv:.2f}; NPV {r.npv:.2f}; "
                 f"LR+ {r.lr_pos:.2f}; κ {r.kappa:.3f} (κmax {r.kappa_max:.3f}); PABAK {r.pabak:.3f}")
    hy = m["label_hybrid"]
    L += ["", f"Hybrid label coverage: {int(hy.notna().sum())}/489 "
              f"({int((hy == 1).sum())} resistant / {int((hy == 0).sum())} sensitive); "
              f"platinum status alone: {int(m.label_platinum.notna().sum())}/489.",
          "", "## Prediction scorecard", "", "(to be completed after the run)", ""]
    (out / "09_platinum_missingness_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("A9 done")


if __name__ == "__main__":
    main()
