#!/usr/bin/env python3
"""
label_validity/13_exploratory_label_structure.py
────────────────────────────────────────────────
A13 — EXPLORATORY, POST HOC. Written 2026-10-29 ~21:00 ET AFTER the v4 red-team review
(review_v4/METHODS_ATTACK.md, CODE_ATTACK.md), whose scratch analyses had already shown most of these
results (review_v4/scratch_methods/). There are no predictions and no decision rules: every quantity
below is reported whatever it shows, and the manuscript labels it exploratory.

Purpose: answer the reviewers' questions about what the OS-threshold labels measure, re-implementing
the red-team analyses as one documented script that reads only committed inputs.
  E1  Cohort flow: TCGA-OV patients in the PanCancer clinical file → treatment record → platinum agent.
  E2  Threshold sweep: OS < t months (t = 6 … 60) as a test for platinum resistance (reference:
      platinum status; and the combined label). n, sensitivity, specificity, PPV, NPV (Wilson 95% CI),
      κ, κmax, Youden, plus the values expected with NO platinum information (independence:
      PPV = prevalence of resistance; specificity = 1 − P(OS label positive)) and the maximum
      sensitivity the label's prevalence allows.
  E3  Reference missingness: among OS-positive patients, how many lack a determinate platinum status,
      and best/worst-case bounds on sensitivity and PPV if all of them were resistant / sensitive.
  E4  Decomposition of OS into PFI-from-platinum and survival after progression (Cox, lifelines):
      age (per 10 y), stage IV, residual > 1 cm, any residual, BRCA1/2 carrier (A8 primary),
      CCNE1 amplification, Aneuploidy Score (per SD). Times from TCGA-CDR (days).
  E5  Clinical-only classifier: 5 × 5-fold stratified CV logistic regression (age, stage IV,
      residual > 1 cm; complete cases; seed 42) predicting each label; mean AUC (pooled out-of-fold per repeat).
  E6  Residual disease coded as any residual vs none (R0): Fisher conditional OR for each label.
  E7  Minimum detectable differences for the same-patient comparisons in A8/A10: 80% power, two-sided
      α 0.05, SE taken from the bootstrap 95% CI width (SE ≈ width / 3.92); MDE = 2.80 × SE.
  E8  Sensitivity: excluding the TCGA-CDR "Redacted" patients from the re-derived interval —
      coverage and κ with platinum status.

Inputs: label_validity/outputs/{labels_full.csv, labels_master.csv, a3_covariates.csv, a8_carriers.csv,
        a8_brca_diff.csv, a10_diff.csv}; <data-root>/ov_tcga_pan_can_atlas_2018/{data_clinical_patient.txt,
        data_timeline_treatment.txt}; <data-root>/ov_tcga_pub/ov_tcga_pub/{data_clinical_sample.txt,
        data_cna.txt, case_lists/cases_cna.txt}; <data-root>/TCGA-CDR-SupplementalTableS1.xlsx
Outputs → label_validity/outputs/a13_*.csv, 13_exploratory_label_structure_summary.md
Run (from the repo root): python label_validity/13_exploratory_label_structure.py --data-root "<...>/OV Data/Project data"
Requires lifelines for E4.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"
TRUNC = {"Frame_Shift_Del", "Frame_Shift_Ins", "Nonsense_Mutation", "Splice_Site"}
LABELS = ["label_platinum", "label_pfiplat6", "label_hybrid", "label_response", "label_os18_all", "label_os24_all"]


def wilson(k, n):
    if n == 0:
        return (np.nan,) * 3
    z = 1.959963984540054; p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def kappa(a, b):
    po = np.mean(a == b); pa, pb = a.mean(), b.mean(); pe = pa * pb + (1 - pa) * (1 - pb)
    return (po - pe) / (1 - pe)


def kmax(a, b):
    pa, pb = a.mean(), b.mean(); pe = pa * pb + (1 - pa) * (1 - pb)
    return (min(pa, pb) + min(1 - pa, 1 - pb) - pe) / (1 - pe)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    dr = Path(ap.parse_args().data_root)
    pc, pub = dr / "ov_tcga_pan_can_atlas_2018", dr / "ov_tcga_pub" / "ov_tcga_pub"
    L = ["# A13 — Exploratory analyses of label structure (post hoc; no predictions)", ""]

    f = pd.read_csv(OUT / "labels_full.csv", index_col=0)
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    cov = pd.read_csv(OUT / "a3_covariates.csv", index_col=0)
    clin = pd.read_csv(pc / "data_clinical_patient.txt", sep="\t", comment="#").set_index("PATIENT_ID")
    tr = pd.read_csv(pc / "data_timeline_treatment.txt", sep="\t")
    cdr = pd.read_excel(dr / "TCGA-CDR-SupplementalTableS1.xlsx", sheet_name="TCGA-CDR")
    cdr = cdr[cdr["type"] == "OV"].set_index("bcr_patient_barcode")

    # ── E1 cohort flow ──────────────────────────────────────────────────────
    all_ids = set(clin.index)
    tr_ids = set(tr.PATIENT_ID) & all_ids
    plat_ids = set(f.index)
    no_tr = sorted(all_ids - tr_ids)
    tr_noplat = sorted(tr_ids - plat_ids)
    os_m = pd.to_numeric(clin["OS_MONTHS"], errors="coerce")
    os_e = clin["OS_STATUS"].astype(str).str.startswith("1")
    pubc = pd.read_csv(pub / "data_clinical_patient.txt", sep="\t", comment="#").set_index("PATIENT_ID") \
        if (pub / "data_clinical_patient.txt").exists() else None

    def km_median(ids):
        t = os_m.reindex(ids).dropna(); e = os_e.reindex(t.index).astype(int).to_numpy(); t = t.to_numpy()
        s = 1.0
        for ti in np.unique(t[e == 1]):
            s *= 1 - ((t == ti) & (e == 1)).sum() / (t >= ti).sum()
            if s <= 0.5:
                return float(ti)
        return float("nan")
    flow = pd.DataFrame([
        dict(step="PanCancer clinical patients", n=len(all_ids)),
        dict(step="with any treatment-timeline record", n=len(tr_ids)),
        dict(step="no treatment-timeline record (excluded)", n=len(no_tr), km_median_os=km_median(no_tr)),
        dict(step="treatment record but no carboplatin/cisplatin (excluded)", n=len(tr_noplat), km_median_os=km_median(tr_noplat)),
        dict(step="platinum-treated cohort", n=len(plat_ids), km_median_os=km_median(sorted(plat_ids)))])
    if pubc is not None and "PLATINUM_STATUS" in pubc.columns:
        ps = pubc["PLATINUM_STATUS"]
        flow["determinate_platinum_status"] = [np.nan, np.nan,
                                               int(ps.reindex(no_tr).isin(["Resistant", "Sensitive"]).sum()),
                                               int(ps.reindex(tr_noplat).isin(["Resistant", "Sensitive"]).sum()),
                                               int(ps.reindex(sorted(plat_ids)).isin(["Resistant", "Sensitive"]).sum())]
    flow.to_csv(OUT / "a13_cohort_flow.csv", index=False)
    L += ["## E1 Cohort flow", ""] + [f"- {r.step}: {r.n}" + (f"; KM median OS {r.km_median_os:.1f} mo" if pd.notna(getattr(r, 'km_median_os', np.nan)) else "")
                                      + (f"; determinate platinum status {int(r.determinate_platinum_status)}" if "determinate_platinum_status" in flow and pd.notna(r.determinate_platinum_status) else "")
                                      for r in flow.itertuples()] + [""]

    # ── E2 threshold sweep ─────────────────────────────────────────────────
    om = os_m.reindex(f.index); oe = os_e.reindex(f.index)
    rows = []
    for ref in ["label_platinum", "label_hybrid"]:
        for t in [6, 9, 12, 15, 18, 21, 24, 30, 36, 42, 48, 60]:
            lab = pd.Series(np.where(oe & (om < t), 1.0, np.where(om >= t, 0.0, np.nan)), index=f.index)
            d = pd.DataFrame({"t": lab, "r": f[ref]}).dropna()
            a, r = d.t.to_numpy(int), d.r.to_numpy(int)
            tp = int(((a == 1) & (r == 1)).sum()); fp = int(((a == 1) & (r == 0)).sum())
            fn = int(((a == 0) & (r == 1)).sum()); tn = int(((a == 0) & (r == 0)).sum())
            se, sel, seh = wilson(tp, tp + fn); sp, spl, sph = wilson(tn, tn + fp); pp, ppl, pph = wilson(tp, tp + fp)
            prev_r, prev_t = r.mean(), a.mean()
            rows.append(dict(reference=ref, threshold_months=t, os_label_determinate=int(lab.notna().sum()),
                             os_label_positive=int((lab == 1).sum()), n=len(d), tp=tp, fp=fp, fn=fn, tn=tn,
                             sensitivity=se, sens_lo=sel, sens_hi=seh, specificity=sp, spec_lo=spl, spec_hi=sph,
                             ppv=pp, ppv_lo=ppl, ppv_hi=pph, npv=tn / (tn + fn), kappa=kappa(a, r), kappa_max=kmax(a, r),
                             youden=se + sp - 1, null_ppv=prev_r, null_specificity=1 - prev_t,
                             max_sensitivity=min(1.0, prev_t / prev_r)))
    sw = pd.DataFrame(rows); sw.to_csv(OUT / "a13_threshold_sweep.csv", index=False)
    L += ["## E2 Threshold sweep (reference: platinum status)", "",
          "| t (mo) | n | sens [95% CI] | spec | PPV [95% CI] | κ (κmax) | Youden | PPV if no platinum information | spec if no platinum information | max sens allowed |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sw[sw.reference == "label_platinum"].itertuples():
        L.append(f"| {r.threshold_months} | {r.n} | {r.sensitivity:.2f} [{r.sens_lo:.2f}, {r.sens_hi:.2f}] | {r.specificity:.2f} | "
                 f"{r.ppv:.2f} [{r.ppv_lo:.2f}, {r.ppv_hi:.2f}] | {r.kappa:.2f} ({r.kappa_max:.2f}) | {r.youden:.2f} | "
                 f"{r.null_ppv:.2f} | {r.null_specificity:.2f} | {r.max_sensitivity:.2f} |")
    L.append("")

    # ── E3 reference missingness ───────────────────────────────────────────
    rows = []
    for t, col in [(18, "label_os18_all"), (24, "label_os24_all")]:
        pos = f[f[col] == 1]; neg = f[f[col] == 0]
        st_pos = pos.label_platinum; st_neg = neg.label_platinum
        R1, S1, U1 = int((st_pos == 1).sum()), int((st_pos == 0).sum()), int(st_pos.isna().sum())
        R0, S0, U0 = int((st_neg == 1).sum()), int((st_neg == 0).sum()), int(st_neg.isna().sum())
        rows.append(dict(threshold_months=t, os_positive=len(pos), pos_resistant=R1, pos_sensitive=S1, pos_undetermined=U1,
                         os_negative=len(neg), neg_resistant=R0, neg_sensitive=S0, neg_undetermined=U0,
                         ppv_observed=R1 / (R1 + S1), ppv_lower=R1 / (R1 + S1 + U1), ppv_upper=(R1 + U1) / (R1 + S1 + U1),
                         sens_observed=R1 / (R1 + R0),
                         sens_lower=R1 / (R1 + R0 + U0), sens_upper=(R1 + U1) / (R1 + U1 + R0)))
    mi = pd.DataFrame(rows); mi.to_csv(OUT / "a13_reference_missingness.csv", index=False)
    L += ["## E3 OS-positive patients without a platinum status; bounds", ""]
    for r in mi.itertuples():
        L.append(f"- OS < {r.threshold_months} mo: {r.os_positive} positive, of whom {r.pos_undetermined} undetermined "
                 f"({r.pos_undetermined / r.os_positive:.0%}); PPV observed {r.ppv_observed:.2f}, bounds {r.ppv_lower:.2f}–{r.ppv_upper:.2f}; "
                 f"sensitivity observed {r.sens_observed:.2f}, bounds {r.sens_lower:.2f}–{r.sens_upper:.2f} "
                 f"(lower: undetermined OS-negative all resistant; upper: undetermined OS-positive all resistant)")
    L.append("")

    # ── shared covariate frame ─────────────────────────────────────────────
    df = f.join(m[["pfi_from_platinum_d"]]).join(cov)
    df["age10"] = df["age"] / 10
    df["aneuploidy_sd"] = (df["aneuploidy"] - df["aneuploidy"].mean()) / df["aneuploidy"].std()
    rd = pd.read_csv(pub / "data_clinical_sample.txt", sep="\t", comment="#").drop_duplicates("PATIENT_ID").set_index("PATIENT_ID")["TUMOR_RESIDUAL_DISEASE"]
    df["resid_any"] = rd.reindex(df.index).map({"No Macroscopic disease": 0, "1-10 mm": 1, "11-20 mm": 1, ">20mm": 1})
    car = pd.read_csv(OUT / "a8_carriers.csv")
    car = car[car.trunc.astype(bool) & car.Mutation_Status.isin(["Germline", "Somatic"])]
    seq = set(pd.read_csv(OUT / "a8_carriers.csv").pid)  # carriers only; sequenced set from case list below
    txt = (pub / "case_lists" / "cases_sequenced.txt").read_text(encoding="utf-8")
    seq = {x[:12] for x in txt.split("case_list_ids:")[1].split()}
    df["brca_carrier"] = np.where(df.index.isin(seq), df.index.isin(set(car.pid)).astype(float), np.nan)
    cna = pd.read_csv(pub / "data_cna.txt", sep="\t")
    cc = cna[cna.Hugo_Symbol == "CCNE1"].iloc[0].drop(["Hugo_Symbol", "Entrez_Gene_Id"])
    cc.index = cc.index.str[:12]; cc = pd.to_numeric(cc[~cc.index.duplicated()], errors="coerce")
    df["ccne1_amp"] = (cc.reindex(df.index) == 2).astype(float).where(cc.reindex(df.index).notna())

    # ── E4 Cox decomposition ───────────────────────────────────────────────
    from lifelines import CoxPHFitter
    c = cdr.reindex(df.index)
    df["os_d"], df["os_ev"] = pd.to_numeric(c["OS.time"], errors="coerce"), pd.to_numeric(c["OS"], errors="coerce")
    df["pfi_d"], df["pfi_ev"] = pd.to_numeric(c["PFI.time"], errors="coerce"), pd.to_numeric(c["PFI"], errors="coerce")
    df["pfiplat_d"] = df["pfi_from_platinum_d"].clip(lower=1)
    df["pps_d"] = df["os_d"] - df["pfi_d"]
    VARS = ["age10", "stage_iv", "residual_subopt", "resid_any", "brca_carrier", "ccne1_amp", "aneuploidy_sd"]

    def cox(d, t, e, v):
        dd = d[[t, e, v]].dropna(); dd = dd[dd[t] > 0]
        if dd[e].sum() < 10:
            return None
        s = CoxPHFitter().fit(dd, t, e).summary.loc[v]
        return dict(n=len(dd), events=int(dd[e].sum()), HR=float(np.exp(s["coef"])),
                    lo=float(np.exp(s["coef lower 95%"])), hi=float(np.exp(s["coef upper 95%"])), p=float(s["p"]))
    prog = df[(df.pfi_ev == 1) & (df.pps_d > 0)]
    rows = []
    for v in VARS:
        for name, d, t, e in [("PFI_from_platinum", df, "pfiplat_d", "pfi_ev"),
                              ("survival_after_progression", prog, "pps_d", "os_ev"), ("OS", df, "os_d", "os_ev")]:
            r = cox(d, t, e, v)
            if r:
                rows.append(dict(covariate=v, outcome=name, **r))
    cx = pd.DataFrame(rows); cx.to_csv(OUT / "a13_os_decomposition_cox.csv", index=False)
    L += ["## E4 Cox decomposition (HR [95% CI], p; n/events)", "",
          "| covariate | PFI from platinum | survival after progression | OS |", "|---|---|---|---|"]
    for v in VARS:
        cells = []
        for o in ["PFI_from_platinum", "survival_after_progression", "OS"]:
            r = cx[(cx.covariate == v) & (cx.outcome == o)]
            cells.append("—" if r.empty else f"{r.HR.iloc[0]:.2f} [{r.lo.iloc[0]:.2f}, {r.hi.iloc[0]:.2f}], p {r.p.iloc[0]:.3g} ({r.n.iloc[0]}/{r.events.iloc[0]})")
        L.append(f"| {v} | " + " | ".join(cells) + " |")
    L.append("")

    # ── E5 clinical-only classifier ────────────────────────────────────────
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold
    from sklearn.preprocessing import StandardScaler
    rows = []
    for lab in LABELS:
        d = df[[lab, "age", "stage_iv", "residual_subopt"]].dropna()
        X, y = d[["age", "stage_iv", "residual_subopt"]].to_numpy(float), d[lab].to_numpy(int)
        aucs = []
        for rep in range(5):
            oof = np.zeros(len(y))
            for trn, tst in StratifiedKFold(5, shuffle=True, random_state=42 + rep).split(X, y):
                sc = StandardScaler().fit(X[trn])
                mdl = LogisticRegression(class_weight="balanced", max_iter=1000).fit(sc.transform(X[trn]), y[trn])
                oof[tst] = mdl.predict_proba(sc.transform(X[tst]))[:, 1]
            aucs.append(roc_auc_score(y, oof))
        rows.append(dict(label=lab, n=len(y), n_pos=int(y.sum()), mean_auc=float(np.mean(aucs)),
                         min_auc=float(np.min(aucs)), max_auc=float(np.max(aucs))))
    ck = pd.DataFrame(rows); ck.to_csv(OUT / "a13_clinical_only_auc.csv", index=False)
    L += ["## E5 Clinical-only logistic regression (age, stage IV, residual > 1 cm), 5×5 CV", ""]
    L += [f"- {r.label}: AUC {r.mean_auc:.3f} (range {r.min_auc:.3f}–{r.max_auc:.3f}); n {r.n} ({r.n_pos} positive)" for r in ck.itertuples()] + [""]

    # ── E6 residual: any vs none ───────────────────────────────────────────
    rows = []
    for lab in LABELS:
        d = df[[lab, "resid_any"]].dropna(); x, y = d.resid_any.to_numpy(int), d[lab].to_numpy(int)
        t = [[int(((x == 1) & (y == 1)).sum()), int(((x == 1) & (y == 0)).sum())],
             [int(((x == 0) & (y == 1)).sum()), int(((x == 0) & (y == 0)).sum())]]
        o = odds_ratio(t, kind="conditional"); ci = o.confidence_interval(0.95)
        rows.append(dict(label=lab, n=len(d), any_resid_pos=t[0][0], any_resid_n=t[0][0] + t[0][1],
                         none_pos=t[1][0], none_n=t[1][0] + t[1][1], OR=float(o.statistic), lo=float(ci.low),
                         hi=float(ci.high), p=float(fisher_exact(t)[1])))
    rr = pd.DataFrame(rows); rr.to_csv(OUT / "a13_residual_any.csv", index=False)
    L += ["## E6 Any residual vs none (R0)", ""]
    L += [f"- {r.label}: {r.any_resid_pos}/{r.any_resid_n} vs {r.none_pos}/{r.none_n}; OR {r.OR:.2f} [{r.lo:.2f}, {r.hi:.2f}], p {r.p:.3g}" for r in rr.itertuples()] + [""]

    # ── E7 minimum detectable differences ──────────────────────────────────
    rows = []
    for fn_, lab1, lab2, est, lo, hi, kind in (
            [(r.label_1, r.label_1, r.label_2, r.logOR_diff, r.lo, r.hi, "BRCA log OR") for r in pd.read_csv(OUT / "a8_brca_diff.csv").itertuples()] +
            [(r.covariate, r.contrast, "", r.estimate, r.lo, r.hi, r.measure) for r in pd.read_csv(OUT / "a10_diff.csv").itertuples()]):
        se = (hi - lo) / 3.92
        rows.append(dict(comparison=f"{kind}: {lab1} {('− ' + lab2) if lab2 else ''}".strip(), estimate=est, se=se, mde_80=2.80 * se,
                         mde_ratio_of_or=float(np.exp(2.80 * se)) if "log OR" in kind else np.nan))
    md = pd.DataFrame(rows); md.to_csv(OUT / "a13_min_detectable.csv", index=False)
    L += ["## E7 Minimum detectable difference (80% power) for same-patient comparisons", ""]
    L += [f"- {r.comparison}: estimate {r.estimate:+.2f}, SE {r.se:.2f}, MDE {r.mde_80:.2f}"
          + (f" (ratio of ORs {r.mde_ratio_of_or:.1f})" if pd.notna(r.mde_ratio_of_or) else "") for r in md.itertuples()] + [""]

    # ── E8 CDR redaction ───────────────────────────────────────────────────
    red = cdr["Redaction"].reindex(df.index).eq("Redacted")
    p6 = df["label_pfiplat6"].where(~red)
    d = pd.DataFrame({"a": df.label_platinum, "b": p6}).dropna()
    L += ["## E8 Excluding TCGA-CDR 'Redacted' patients from the re-derived interval", "",
          f"- Redacted among platinum-treated: {int(red.sum())}; re-derived interval determinate {int(df.label_pfiplat6.notna().sum())} → "
          f"{int(p6.notna().sum())} ({int((p6 == 1).sum())} resistant); κ with platinum status "
          f"{kappa(d.a.to_numpy(int), d.b.to_numpy(int)):.3f} (n {len(d)})", ""]
    pd.DataFrame([dict(redacted=int(red.sum()), pfi_determinate_before=int(df.label_pfiplat6.notna().sum()),
                       pfi_determinate_after=int(p6.notna().sum()), pfi_resistant_after=int((p6 == 1).sum()),
                       kappa_after=kappa(d.a.to_numpy(int), d.b.to_numpy(int)), n_kappa=len(d))]).to_csv(OUT / "a13_redaction.csv", index=False)

    (OUT / "13_exploratory_label_structure_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
