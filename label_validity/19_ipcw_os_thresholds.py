#!/usr/bin/env python3
"""
label_validity/19_ipcw_os_thresholds.py
───────────────────────────────────────
A19 — censoring-adjusted (inverse probability of censoring weighted, IPCW) sensitivity analysis of the 18- and
24-month OS thresholds as tests for platinum resistance. Post hoc. Written 2026-10-29 23:57–23:58 ET, BEFORE
this script was run, in response to a fourth review (point 6: excluding patients censored before the threshold
can bias threshold labels; Vock et al. 2016). Known before writing: 69 of 489 platinum-treated patients are
censored before 18 months; the unweighted results (A11): 18 months sensitivity 18/84, specificity 180/184,
PPV 18/22; 24 months 32/83, 165/176, 32/43 (reference: TCGA platinum status). Not seen: any weighted result.

Population: the 489 platinum-treated patients; OS from PanCancer Atlas OS_MONTHS / OS_STATUS (as the labels).
Horizon status at t (18, 24 months): known if death before t (label 1) or OS_MONTHS ≥ t (label 0).
Weights: w = 1 / Ĝ(min(T, t)−), where Ĝ is the probability of remaining uncensored.
  IPCW-KM: Ĝ from the Kaplan–Meier estimator of the censoring distribution in all 489 patients (primary).
  IPCW-Cox: Ĝ from a Cox model of censoring on age (per 10 y), stage IV and residual disease > 1 cm, among
      patients with complete covariates (a3_covariates.csv); others are excluded from this variant.
Estimands among patients with a determinate platinum status and known horizon status, weighted by w:
  sensitivity, specificity, PPV of OS < t for platinum resistance. 95% percentile intervals for IPCW-KM from
  2,000 bootstrap resamples of the 489 patients (Ĝ re-estimated in each; numpy default_rng(42)).
Limits stated with the results: IPCW assumes censoring independent of the outcome given the model's covariates;
it does not address the missing platinum status (the bounds in A13 address that) or unmeasured informative censoring.

DECISION RULE (for the manuscript)
  * If any IPCW-KM or IPCW-Cox estimate differs from the unweighted estimate by more than 0.05, the manuscript
    reports the IPCW estimates in Results next to the unweighted ones; otherwise it reports them in one
    sentence, with the table in the Supporting information. Either way it states the limits above.
  No predictions are made.

Run (from the repo root): python label_validity/19_ipcw_os_thresholds.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a19_ipcw.csv, a19_ENVIRONMENT.txt, 19_ipcw_os_thresholds_summary.md
"""
from __future__ import annotations

import argparse
import platform
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"
NBOOT = 2000


def km_cens(time, cens):
    """KM survival of the censoring distribution; returns a function G(t-) (left limit)."""
    ut = np.unique(time[cens == 1])
    surv, s = [], 1.0
    for u in ut:
        s *= 1 - ((time == u) & (cens == 1)).sum() / (time >= u).sum(); surv.append(s)
    ut, surv = np.asarray(ut), np.asarray(surv)
    def G_left(x):
        idx = np.searchsorted(ut, x, side="left") - 1      # censoring times strictly before x
        return np.where(idx >= 0, surv[np.clip(idx, 0, None)], 1.0)
    return G_left


def metrics(y, r, w):
    tp = np.sum(w * ((y == 1) & (r == 1))); fn = np.sum(w * ((y == 0) & (r == 1)))
    fp = np.sum(w * ((y == 1) & (r == 0))); tn = np.sum(w * ((y == 0) & (r == 0)))
    return tp / (tp + fn), tn / (tn + fp), tp / (tp + fp)


def main() -> None:
    import lifelines
    from lifelines import CoxPHFitter
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    dr = Path(ap.parse_args().data_root)
    f = pd.read_csv(OUT / "labels_full.csv", index_col=0)
    clin = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_clinical_patient.txt", sep="\t", comment="#").set_index("PATIENT_ID").reindex(f.index)
    T = pd.to_numeric(clin.OS_MONTHS, errors="coerce").to_numpy()
    D = clin.OS_STATUS.astype(str).str.startswith("1").astype(int).to_numpy()
    R = f.label_platinum.to_numpy()
    cov = pd.read_csv(OUT / "a3_covariates.csv", index_col=0).reindex(f.index)
    X = pd.DataFrame({"age10": cov["age"] / 10, "stage_iv": cov["stage_iv"], "residual_subopt": cov["residual_subopt"]}, index=f.index)
    ok = ~np.isnan(T)

    rows = []
    rng = np.random.default_rng(42)
    for t in (18, 24):
        y = np.where((D == 1) & (T < t), 1.0, np.where(T >= t, 0.0, np.nan))
        assert np.array_equal(np.nan_to_num(y, nan=-1), np.nan_to_num(f[f"label_os{t}_all"].to_numpy(), nan=-1)), "label mismatch"
        use = ok & ~np.isnan(y) & ~np.isnan(R)
        # unweighted
        se0, sp0, pp0 = metrics(y[use], R[use], np.ones(use.sum()))
        # IPCW-KM
        G = km_cens(T[ok], 1 - D[ok])
        w = 1 / G(np.minimum(T, t))
        se1, sp1, pp1 = metrics(y[use], R[use], w[use])
        # IPCW-Cox
        d = X.assign(T=T, C=1 - D)[ok].dropna()
        cph = CoxPHFitter().fit(d, "T", "C")
        tm = np.minimum(T, t)
        Sx = np.full(len(T), np.nan)
        for i in np.where(f.index.isin(d.index))[0]:
            s = cph.predict_survival_function(X.iloc[[i]], times=[max(tm[i] - 1e-6, 0)])
            Sx[i] = float(s.iloc[0, 0])
        usec = use & ~np.isnan(Sx)
        se2, sp2, pp2 = metrics(y[usec], R[usec], 1 / Sx[usec])
        # bootstrap IPCW-KM
        bs = np.empty((NBOOT, 3)); idx_all = np.where(ok)[0]
        for b in range(NBOOT):
            ii = rng.choice(idx_all, len(idx_all), replace=True)
            Gb = km_cens(T[ii], 1 - D[ii]); wb = 1 / Gb(np.minimum(T[ii], t))
            ub = ~np.isnan(y[ii]) & ~np.isnan(R[ii])
            bs[b] = metrics(y[ii][ub], R[ii][ub], wb[ub])
        lo, hi = np.nanpercentile(bs, 2.5, axis=0), np.nanpercentile(bs, 97.5, axis=0)
        for nm, v0, v1, v2, l, h in zip(["sensitivity", "specificity", "PPV"], [se0, sp0, pp0], [se1, sp1, pp1], [se2, sp2, pp2], lo, hi):
            rows.append(dict(threshold_months=t, measure=nm, unweighted=v0, ipcw_km=v1, ipcw_km_lo=l, ipcw_km_hi=h, ipcw_cox=v2,
                             n_unweighted=int(use.sum()), n_cox=int(usec.sum()),
                             censored_before_t=int((ok & np.isnan(y)).sum()),
                             censored_before_t_with_status=int((ok & np.isnan(y) & ~np.isnan(R)).sum())))
    res = pd.DataFrame(rows); res.to_csv(OUT / "a19_ipcw.csv", index=False)
    diff = np.maximum((res.ipcw_km - res.unweighted).abs(), (res.ipcw_cox - res.unweighted).abs())
    env = f"Python {platform.python_version()}; lifelines {lifelines.__version__}; pandas {pd.__version__}; numpy {np.__version__}"
    (OUT / "a19_ENVIRONMENT.txt").write_text(env + "\n", encoding="utf-8")
    L = ["# A19 — IPCW sensitivity analysis of the OS thresholds as tests for platinum resistance", "", env, "",
         "```", res.round(3).to_string(index=False), "```", "",
         f"Largest |IPCW − unweighted|: {diff.max():.3f}. Decision rule — any difference > 0.05: {bool((diff > 0.05).any())}", "",
         "IPCW assumes censoring independent of the outcome given the covariates; it does not address missing platinum status or unmeasured informative censoring.", ""]
    (OUT / "19_ipcw_os_thresholds_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
