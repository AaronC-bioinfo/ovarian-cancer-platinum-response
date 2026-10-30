#!/usr/bin/env python3
"""
label_validity/23_followup_checks.py
────────────────────────────────────
A23 — follow-up checks requested by a fifth review of the revised manuscript. Post hoc.
Writing started 2026-10-30 01:05 ET, BEFORE this script was run (run time is recorded in the summary).
Known before writing: A18 (anchors), A19 (IPCW with the censoring distribution estimated in all 489 patients:
largest change 0.037), the provenance classes (a15b), and that oxaliplatin rows supply the anchor for 3 patients.
Not seen: any result below.
  C1  IPCW with the censoring distribution estimated only in patients with a determinate platinum status
      (Kaplan–Meier), and separately within each platinum-status group (stratified Kaplan–Meier); for each variant:
      sensitivity, specificity, PPV of OS < 18 / 24 months; maximum weight; Kish effective sample size
      (Σw)² / Σw². Also, for the A19 Cox variant, the number of patients excluded for missing covariates.
      No weight truncation.
  C2  Anchor restricted to carboplatin and cisplatin rows (AGENT contains CARBO or CISPLATIN; oxaliplatin
      excluded): changed and newly undetermined label_pfiplat6 calls overall, among the 117 added patients, among
      the 78 unflagged added patients, among the 4 discordant patients, and among the 2 resistant unflagged added
      patients with RNA-seq data.
  C3  A18 alternative anchors (A1–A3) among the 78 unflagged added patients and the 2 resistant ones with RNA-seq
      data: calls changed and calls becoming undetermined.
  C4  Unflagged added resistant calls whose new tumour event has no recorded type.
DECISION RULE (for the manuscript)
  * C1: if any estimate differs from the unweighted one by more than 0.05 under either new variant, report it in
    Results; otherwise one sentence in Methods/Results. C2–C4: reported in one or two sentences, details in S11.
  No predictions are made.
Run (from the repo root): python label_validity/23_followup_checks.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a23_ipcw_variants.csv, a23_anchor_checks.csv, 23_followup_checks_summary.md
"""
from __future__ import annotations

import argparse
import importlib.util
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
LV = ROOT / "label_validity"
OUT = LV / "outputs"


def load19():
    spec = importlib.util.spec_from_file_location("a19", LV / "19_ipcw_os_thresholds.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    dr = Path(ap.parse_args().data_root)
    a19 = load19()
    f = pd.read_csv(OUT / "labels_full.csv", index_col=0)
    clin = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_clinical_patient.txt", sep="\t", comment="#").set_index("PATIENT_ID").reindex(f.index)
    T = pd.to_numeric(clin.OS_MONTHS, errors="coerce").to_numpy()
    D = clin.OS_STATUS.astype(str).str.startswith("1").astype(int).to_numpy()
    R = f.label_platinum.to_numpy()
    cov = pd.read_csv(OUT / "a3_covariates.csv", index_col=0).reindex(f.index)
    ok = ~np.isnan(T); known = ok & ~np.isnan(R)
    rows = []
    for t in (18, 24):
        y = np.where((D == 1) & (T < t), 1.0, np.where(T >= t, 0.0, np.nan))
        use = known & ~np.isnan(y)
        tm = np.minimum(T, t)
        variants = {"unweighted": np.ones(len(T))}
        G = a19.km_cens(T[ok], 1 - D[ok]); variants["km_all489"] = 1 / G(tm)
        Gk = a19.km_cens(T[known], 1 - D[known]); variants["km_status_known"] = 1 / Gk(tm)
        ws = np.full(len(T), np.nan)
        for g in (0, 1):
            sel = known & (R == g); Gg = a19.km_cens(T[sel], 1 - D[sel]); ws[sel] = 1 / Gg(tm[sel])
        variants["km_stratified_by_status"] = ws
        for nm, w in variants.items():
            ww = w[use]; se, sp, pp = a19.metrics(y[use], R[use], ww)
            rows.append(dict(threshold_months=t, variant=nm, n=int(use.sum()), sensitivity=se, specificity=sp, ppv=pp,
                             max_weight=float(np.max(ww)), ess=float(ww.sum() ** 2 / (ww ** 2).sum())))
    iv = pd.DataFrame(rows); iv.to_csv(OUT / "a23_ipcw_variants.csv", index=False)
    a19r = pd.read_csv(OUT / "a19_ipcw.csv")
    cox_excl = {int(r.threshold_months): int(r.n_unweighted - r.n_cox) for r in a19r.drop_duplicates("threshold_months").itertuples()}
    base = iv[iv.variant == "unweighted"].set_index("threshold_months")
    dmax = max(abs(r[m] - base.loc[r.threshold_months, m]) for _, r in iv[iv.variant.isin(["km_status_known", "km_stratified_by_status"])].iterrows() for m in ["sensitivity", "specificity", "ppv"])

    # C2–C4
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    tr = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_timeline_treatment.txt", sep="\t")
    tr = tr[tr.PATIENT_ID.isin(m.index)].copy(); tr["STOP_DATE"] = pd.to_numeric(tr.STOP_DATE, errors="coerce")
    ag = tr.AGENT.astype(str).str.upper()
    adj_cc = tr[(ag.str.contains("CARBO") | ag.str.contains("CISPLATIN")) & ~ag.str.contains("OXALI") & (tr.REGIMEN_INDICATION == "Adjuvant")]
    anc = adj_cc.groupby("PATIENT_ID").STOP_DATE.max().reindex(m.index)
    iv_cc = m.pfi_time_d - anc
    lab_cc = pd.Series(np.where((m.pfi_event == 1) & (iv_cc < 183), 1.0, np.where(iv_cc >= 183, 0.0, np.nan)), index=m.index)
    pv = pd.read_csv(OUT / "a15b_provenance.csv", index_col=0).reindex(m.index)
    res = pd.read_csv(OUT / "label_resource_v1.csv", index_col=0).reindex(m.index)
    an = pd.read_csv(OUT / "a18_anchor_labels.csv", index_col=0).reindex(m.index)
    L0 = m.label_pfiplat6
    groups = {"all determinate": L0.notna(), "added (117)": pv.group.eq("added_by_reconstruction"),
              "unflagged added (78)": pv.group.eq("added_by_reconstruction") & pv.provenance_class.astype(str).str.startswith("clean"),
              "discordant (4)": pv.disagreement.fillna(False).astype(bool),
              "unflagged added resistant with RNA-seq": pv.group.eq("added_by_reconstruction") & pv.provenance_class.eq("clean_resistant") & res.in_rnaseq.astype(bool)}
    rows = []
    for gname, gm in groups.items():
        for alt, lab in [("carbo_cis_only", lab_cc), ("A1", an.label_A1), ("A2", an.label_A2), ("A3", an.label_A3)]:
            base_ = L0[gm]; new = lab[gm]
            rows.append(dict(group=gname, anchor=alt, n=int(gm.sum()), changed=int(((base_ != new) & base_.notna() & new.notna()).sum()),
                             became_undetermined=int((base_.notna() & new.isna()).sum()), became_determinate=int((base_.isna() & new.notna()).sum())))
    ac = pd.DataFrame(rows); ac.to_csv(OUT / "a23_anchor_checks.csv", index=False)
    c4 = int((groups["unflagged added (78)"] & pv.event_source.astype(str).eq("recorded_new_tumour_event:nan")).sum())
    L = ["# A23 — Follow-up checks (IPCW population, anchor drugs, anchors in added patients, unknown event types)", "",
         f"Run {time.strftime('%Y-%m-%d %H:%M:%S %Z')}", "", "## C1 IPCW variants", "", "```", iv.round(3).to_string(index=False), "```", "",
         f"A19 Cox-variant exclusions for missing covariates (patients with status and OS label): {cox_excl}", "",
         f"Largest |change| from unweighted under the two new variants: {dmax:.3f}; decision rule (> 0.05): {dmax > 0.05}", "",
         "## C2–C3 Anchor checks", "", "```", ac.to_string(index=False), "```", "",
         f"## C4 Unflagged added resistant calls with an unrecorded event type: {c4}", ""]
    (OUT / "23_followup_checks_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
