#!/usr/bin/env python3
"""
label_validity/20_documentation_checks.py
─────────────────────────────────────────
A20 — descriptive checks requested by a fourth review; no predictions, no decision rules.
Written 2026-10-30 ~00:00 ET.
  C1  A16 folds (review point 12): for each repeat and fold of the A16 design (StratifiedKFold, 5 folds,
      shuffle, random_state = repeat, stratified on platinum status, patients sorted by ID), the numbers of
      positives in the training and held-out parts for each training label. Patients and order are taken from
      a16_oof_scores.csv. Fold assignment is recomputed here with scikit-learn 1.7.2; the A16 environment check
      (a16_env_check_vm/, scikit-learn 1.7.2) reproduced the Windows logistic-regression AUCs exactly in all 180
      cells, which requires identical folds.
  C2  The four patients in whom TCGA platinum status and the re-derived interval disagree (review point 2).
  C3  A13b Cox models (review point 16): proportional-hazards test (lifelines proportional_hazard_test, rank
      transform) for each univariable model; for continuous covariates (age per 10 y, Aneuploidy Score per SD)
      the P value of an added quadratic term (functional form).
Run (from the repo root): python label_validity/20_documentation_checks.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a20_a16_fold_counts.csv, a20_discordant.csv, a20_cox_checks.csv, 20_documentation_checks_summary.md
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
    import sklearn
    import lifelines
    from lifelines import CoxPHFitter
    from lifelines.statistics import proportional_hazard_test
    from sklearn.model_selection import StratifiedKFold
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    dr = Path(ap.parse_args().data_root)
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)

    # C1
    ids = sorted(pd.read_csv(OUT / "a16_oof_scores.csv", usecols=["patient"]).patient.unique())
    y = {l: m.loc[ids, l].astype(int).values for l in ["label_platinum", "label_os18", "label_os24"]}
    rows = []
    for rep in range(20):
        for k, (tr, te) in enumerate(StratifiedKFold(5, shuffle=True, random_state=rep).split(ids, y["label_platinum"])):
            for l, v in y.items():
                rows.append(dict(repeat=rep, fold=k, label=l, n_train=len(tr), train_pos=int(v[tr].sum()), n_test=len(te), test_pos=int(v[te].sum())))
    fc = pd.DataFrame(rows); fc.to_csv(OUT / "a20_a16_fold_counts.csv", index=False)
    fsum = fc.groupby("label").agg(patients=("n_test", lambda s: int(s.iloc[:5].sum())), train_pos_min=("train_pos", "min"), train_pos_max=("train_pos", "max"),
                                   test_pos_min=("test_pos", "min"), test_pos_max=("test_pos", "max"),
                                   test_folds_without_positive=("test_pos", lambda s: int((s == 0).sum())), folds=("test_pos", "size"))

    # C2
    pv = pd.read_csv(OUT / "a15b_provenance.csv", index_col=0)
    an = pd.read_csv(OUT / "a18_anchor_labels.csv", index_col=0)
    dc = pv[pv.disagreement.astype(bool)].join(an[["label_A1", "label_A2", "label_A3"]])
    dc = dc[["label_platinum", "src_platinum_status_raw", "label_pfiplat6", "pfi_from_platinum_d", "event_source", "provenance_class",
             "redacted", "adj_platinum_rows", "adj_platinum_stop_missing", "later_line_before_event", "near_threshold", "label_A1", "label_A2", "label_A3"]]
    dc.to_csv(OUT / "a20_discordant.csv")

    # C3 — covariate frame and times copied unchanged from A13b
    pub = dr / "ov_tcga_pub" / "ov_tcga_pub"
    f = pd.read_csv(OUT / "labels_full.csv", index_col=0); cov = pd.read_csv(OUT / "a3_covariates.csv", index_col=0)
    cdr = pd.read_excel(dr / "TCGA-CDR-SupplementalTableS1.xlsx", sheet_name="TCGA-CDR"); cdr = cdr[cdr["type"] == "OV"].set_index("bcr_patient_barcode")
    df = f.join(m[["pfi_from_platinum_d"]]).join(cov)
    df["age10"] = df["age"] / 10
    df["aneuploidy_sd"] = (df["aneuploidy"] - df["aneuploidy"].mean()) / df["aneuploidy"].std()
    rd = pd.read_csv(pub / "data_clinical_sample.txt", sep="\t", comment="#").drop_duplicates("PATIENT_ID").set_index("PATIENT_ID")["TUMOR_RESIDUAL_DISEASE"]
    df["resid_any"] = rd.reindex(df.index).map({"No Macroscopic disease": 0, "1-10 mm": 1, "11-20 mm": 1, ">20mm": 1})
    car = pd.read_csv(OUT / "a8_carriers.csv"); car = car[car.trunc.astype(bool) & car.Mutation_Status.isin(["Germline", "Somatic"])]
    seq = {x[:12] for x in (pub / "case_lists" / "cases_sequenced.txt").read_text(encoding="utf-8").split("case_list_ids:")[1].split()}
    df["brca_carrier"] = np.where(df.index.isin(seq), df.index.isin(set(car.pid)).astype(float), np.nan)
    cna = pd.read_csv(pub / "data_cna.txt", sep="\t")
    cc = cna[cna.Hugo_Symbol == "CCNE1"].iloc[0].drop(["Hugo_Symbol", "Entrez_Gene_Id"])
    cc.index = cc.index.str[:12]; cc = pd.to_numeric(cc[~cc.index.duplicated()], errors="coerce")
    df["ccne1_amp"] = (cc.reindex(df.index) == 2).astype(float).where(cc.reindex(df.index).notna())
    c = cdr.reindex(df.index)
    df["os_d"], df["os_ev"] = pd.to_numeric(c["OS.time"], errors="coerce"), pd.to_numeric(c["OS"], errors="coerce")
    df["pfi_d"], df["pfi_ev"] = pd.to_numeric(c["PFI.time"], errors="coerce"), pd.to_numeric(c["PFI"], errors="coerce")
    df["pfiplat_atrisk_d"] = df["pfi_from_platinum_d"].where(df["pfi_from_platinum_d"] > 0)
    df["pps_d"] = df["os_d"] - df["pfi_d"]
    prog = df[(df.pfi_ev == 1) & (df.pps_d > 0)]
    a13b = pd.read_csv(OUT / "a13b_decomposition_cox.csv")
    out = []
    for oc, d, t, e, an_ in [("PFI_from_platinum", df, "pfiplat_atrisk_d", "pfi_ev", "at_risk"), ("survival_after_progression", prog, "pps_d", "os_ev", "unchanged")]:
        for v in VARS:
            dd = d[[t, e, v]].dropna(); dd = dd[dd[t] > 0]
            cph = CoxPHFitter().fit(dd, t, e)
            ref = a13b[(a13b.analysis == an_) & (a13b.covariate == v)].iloc[0]
            assert abs(float(np.exp(cph.params_[v])) - ref.HR) < 1e-9 and len(dd) == ref.n
            ph = proportional_hazard_test(cph, dd, time_transform="rank")
            q = np.nan
            if v in ("age10", "aneuploidy_sd"):
                d2 = dd.assign(sq=dd[v] ** 2); q = float(CoxPHFitter().fit(d2, t, e).summary.loc["sq", "p"])
            out.append(dict(outcome=oc, covariate=v, n=len(dd), events=int(dd[e].sum()), HR=ref.HR, ph_test_p=float(ph.p_value[0]), quadratic_term_p=q))
    cx = pd.DataFrame(out); cx.to_csv(OUT / "a20_cox_checks.csv", index=False)

    env = f"Python {platform.python_version()}; scikit-learn {sklearn.__version__}; lifelines {lifelines.__version__}; pandas {pd.__version__}"
    L = ["# A20 — Descriptive checks (fold counts, discordant patients, Cox assumptions)", "", env, "",
         "## C1 A16 folds", "", "```", fsum.to_string(), "```", "", "## C2 Discordant patients", "", "```", dc.to_string(), "```", "",
         "## C3 Cox checks (A13b models)", "", "```", cx.round(3).to_string(index=False), "```", ""]
    (OUT / "20_documentation_checks_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
