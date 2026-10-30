#!/usr/bin/env python3
"""
label_validity/13b_decomposition_at_risk.py
───────────────────────────────────────────
A13b — correction of the A13 E4 Cox decomposition (13_exploratory_label_structure.py), post hoc.

Written 2026-10-29 22:50–22:59 ET, BEFORE this script was run, after a second review of the revised manuscript
pointed out that A13 set every platinum-free interval below 1 day to 1 day (clip(lower=1)). Checked before
writing: 436 patients have an interval; 28 are below 1 day (19 negative: 8 with a progression event, 11
censored; 9 of 0 days: 4 events, 5 censored). Those patients were not at risk after the time origin (end of
first-line platinum), and 16 of them have no follow-up after it, so the A13 model of the platinum-free
interval used an unsuitable time origin for them. Not seen: any Cox result without those patients.

Analyses (lifelines CoxPHFitter, univariable, same covariates and coding as A13 E4):
  PRIMARY (at_risk): platinum-free interval from the end of first-line platinum, only patients with an
      interval > 0 days (at risk at the origin); event = TCGA-CDR PFI event.
  SENSITIVITY (clipped_as_A13): the A13 model (intervals < 1 day set to 1 day), recomputed here; it must
      reproduce label_validity/outputs/a13_os_decomposition_cox.csv (checked by the script).
  Survival after progression (OS.time − PFI.time, patients with a PFI event and a positive difference;
      event = OS) does not use the platinum time origin; it is recomputed unchanged and must also reproduce A13.

DECISION RULE (for the manuscript)
  * The manuscript reports the at-risk model of the platinum-free interval (Fig 4, S10 Table) and the
    clipped model as a sensitivity analysis.
  * For each covariate, if the 95% CI for the platinum-free interval excludes 1 in one model and includes 1
    in the other, the text says so explicitly for that covariate.
  No predictions are made.

Run (from the repo root): python label_validity/13b_decomposition_at_risk.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a13b_decomposition_cox.csv, a13b_ENVIRONMENT.txt, 13b_decomposition_at_risk_summary.md
"""
from __future__ import annotations

import argparse
import platform
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"
VARS = ["age10", "stage_iv", "residual_subopt", "resid_any", "brca_carrier", "ccne1_amp", "aneuploidy_sd"]


def main() -> None:
    import lifelines
    from lifelines import CoxPHFitter
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    dr = Path(ap.parse_args().data_root)
    pub = dr / "ov_tcga_pub" / "ov_tcga_pub"
    f = pd.read_csv(OUT / "labels_full.csv", index_col=0)
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    cov = pd.read_csv(OUT / "a3_covariates.csv", index_col=0)
    cdr = pd.read_excel(dr / "TCGA-CDR-SupplementalTableS1.xlsx", sheet_name="TCGA-CDR")
    cdr = cdr[cdr["type"] == "OV"].set_index("bcr_patient_barcode")

    # shared covariate frame — copied unchanged from A13
    df = f.join(m[["pfi_from_platinum_d"]]).join(cov)
    df["age10"] = df["age"] / 10
    df["aneuploidy_sd"] = (df["aneuploidy"] - df["aneuploidy"].mean()) / df["aneuploidy"].std()
    rd = pd.read_csv(pub / "data_clinical_sample.txt", sep="\t", comment="#").drop_duplicates("PATIENT_ID").set_index("PATIENT_ID")["TUMOR_RESIDUAL_DISEASE"]
    df["resid_any"] = rd.reindex(df.index).map({"No Macroscopic disease": 0, "1-10 mm": 1, "11-20 mm": 1, ">20mm": 1})
    car = pd.read_csv(OUT / "a8_carriers.csv")
    car = car[car.trunc.astype(bool) & car.Mutation_Status.isin(["Germline", "Somatic"])]
    txt = (pub / "case_lists" / "cases_sequenced.txt").read_text(encoding="utf-8")
    seq = {x[:12] for x in txt.split("case_list_ids:")[1].split()}
    df["brca_carrier"] = np.where(df.index.isin(seq), df.index.isin(set(car.pid)).astype(float), np.nan)
    cna = pd.read_csv(pub / "data_cna.txt", sep="\t")
    cc = cna[cna.Hugo_Symbol == "CCNE1"].iloc[0].drop(["Hugo_Symbol", "Entrez_Gene_Id"])
    cc.index = cc.index.str[:12]; cc = pd.to_numeric(cc[~cc.index.duplicated()], errors="coerce")
    df["ccne1_amp"] = (cc.reindex(df.index) == 2).astype(float).where(cc.reindex(df.index).notna())

    c = cdr.reindex(df.index)
    df["os_d"], df["os_ev"] = pd.to_numeric(c["OS.time"], errors="coerce"), pd.to_numeric(c["OS"], errors="coerce")
    df["pfi_d"], df["pfi_ev"] = pd.to_numeric(c["PFI.time"], errors="coerce"), pd.to_numeric(c["PFI"], errors="coerce")
    df["pfiplat_clip_d"] = df["pfi_from_platinum_d"].clip(lower=1)            # A13 as run
    df["pfiplat_atrisk_d"] = df["pfi_from_platinum_d"].where(df["pfi_from_platinum_d"] > 0)  # A13b primary
    df["pps_d"] = df["os_d"] - df["pfi_d"]

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
        for analysis, outcome, d, t, e in [("at_risk", "PFI_from_platinum", df, "pfiplat_atrisk_d", "pfi_ev"),
                                           ("clipped_as_A13", "PFI_from_platinum", df, "pfiplat_clip_d", "pfi_ev"),
                                           ("unchanged", "survival_after_progression", prog, "pps_d", "os_ev")]:
            r = cox(d, t, e, v)
            if r:
                rows.append(dict(analysis=analysis, covariate=v, outcome=outcome, **r))
    cx = pd.DataFrame(rows); cx.to_csv(OUT / "a13b_decomposition_cox.csv", index=False)

    # reproduction check against A13
    a13 = pd.read_csv(OUT / "a13_os_decomposition_cox.csv")
    rep = []
    for an, oc in [("clipped_as_A13", "PFI_from_platinum"), ("unchanged", "survival_after_progression")]:
        x = cx[(cx.analysis == an)].merge(a13[a13.outcome == oc], on=["covariate", "outcome"], suffixes=("", "_a13"))
        rep.append((an, len(x), float((x.HR - x.HR_a13).abs().max()), bool((x.n == x.n_a13).all())))

    excl = df[df.pfi_from_platinum_d.notna() & ~(df.pfi_from_platinum_d > 0)]
    L = ["# A13b — Cox decomposition with the platinum-free interval restricted to patients at risk at the end of platinum", "",
         f"Python {platform.python_version()}; lifelines {lifelines.__version__}; pandas {pd.__version__}; numpy {np.__version__}", "",
         f"Patients with an interval: {int(df.pfi_from_platinum_d.notna().sum())}; excluded from the at-risk model (interval ≤ 0 days): {len(excl)} "
         f"(events {int((excl.pfi_ev == 1).sum())}, censored {int((excl.pfi_ev == 0).sum())}).", "",
         "Reproduction of A13 (analysis, covariates matched, max |ΔHR|, n identical): " + "; ".join(f"{a}: {k}, {d:.2e}, {s}" for a, k, d, s in rep), "",
         "| covariate | PFI, at risk (primary) | PFI, clipped as A13 (sensitivity) | survival after progression |", "|---|---|---|---|"]
    flips = []
    for v in VARS:
        cells = []
        for an in ["at_risk", "clipped_as_A13", "unchanged"]:
            r = cx[(cx.covariate == v) & (cx.analysis == an)]
            cells.append("—" if r.empty else f"{r.HR.iloc[0]:.2f} [{r.lo.iloc[0]:.2f}, {r.hi.iloc[0]:.2f}], p {r.p.iloc[0]:.3g} ({r.n.iloc[0]}/{r.events.iloc[0]})")
        L.append(f"| {v} | " + " | ".join(cells) + " |")
        a = cx[(cx.covariate == v) & (cx.analysis == "at_risk")].iloc[0]; b = cx[(cx.covariate == v) & (cx.analysis == "clipped_as_A13")].iloc[0]
        if (a.lo > 1 or a.hi < 1) != (b.lo > 1 or b.hi < 1):
            flips.append(v)
    L += ["", "Decision rule — covariates whose PFI 95% CI excludes 1 in one model but not the other: " + (", ".join(flips) if flips else "none"), ""]
    (OUT / "13b_decomposition_at_risk_summary.md").write_text("\n".join(L), encoding="utf-8")
    (OUT / "a13b_ENVIRONMENT.txt").write_text(L[2] + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
