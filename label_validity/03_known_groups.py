#!/usr/bin/env python3
"""
label_validity/03_known_groups.py
─────────────────────────────────
Q2 analysis A3, part 1 — known-groups validity of each response label
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A3).

Question: does each label separate patients along characteristics that a
platinum-response label should track (somatic BRCA1/2), and along ones an
overall-survival label might track instead (age, stage, residual disease)?

Population: platinum-treated patients (A1 cohort: exact carboplatin/cisplatin
match, n = 489) with the label determinate and the covariate non-missing.
The Cox part (03b_pfi_cox.R) keeps the v2 Cox cohort instead (phase2
definition, n = 432 / BRCA subset 335); the one-patient difference
(TCGA-29-1711, oxaliplatin only) is stated in both scripts.

Inputs
  label_validity/outputs/labels_master.csv           (A1)
  hrd/brca_status.csv                                 BRCA_any_mutated (somatic, non-silent; v2 Enhancement 4)
  <data-root>/ov_tcga_pan_can_atlas_2018/data_clinical_sample.txt   ANEUPLOIDY_SCORE, TMB_NONSYNONYMOUS (first sample per patient, as phase2)
  <data-root>/TCGA-CDR-SupplementalTableS1.xlsx       age_at_initial_pathologic_diagnosis, clinical_stage
  <data-root>/ov_tcga_pub/ov_tcga_pub/data_clinical_sample.txt     TUMOR_RESIDUAL_DISEASE (TCGA 2011)

Labels (1 = non-responder / resistant): label_platinum (primary), label_pfiplat6,
label_response, label_os18, label_os24; label_os12 in the supplement.

Tests (fixed before running)
  BRCA_any_mutated (1 vs 0)            Fisher exact; conditional OR of being label = 1 if mutant, 95% CI
  Stage IV vs I–III (CDR clinical_stage) Fisher exact; OR of label = 1 if stage IV
  Suboptimal residual (11–20 mm, >20 mm) vs optimal (no macroscopic, 1–10 mm)
                                        Fisher exact; OR of label = 1 if suboptimal
                                        (optimal ≤ 1 cm as defined in TCGA 2011 SI Methods S1)
  Aneuploidy score, TMB, age           Mann–Whitney U, two-sided; rank-biserial r
                                        (r > 0 = higher in label = 1)
  Multiplicity: Benjamini–Hochberg across the 6 tests within each label (one
  family per label). Raw p and BH q both reported.

Outputs → label_validity/outputs/a3_known_groups.csv, 03_known_groups_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already known (not predictions): TCGA 2011 SI Methods S1 reports that platinum
status was associated with residual disease among optimally debulked patients
and that microscopic residual disease was "independently associated with
platinum status (P = 0.005)". v2: BRCA HR 0.455 for OS (n = 335); aneuploidy
HR 1.021 for OS.

  P1  BRCA: OR < 1 (mutant → sensitive/responder) for label_platinum and
      label_pfiplat6, with the 95% CI excluding 1 for label_platinum.
  P2  BRCA: for label_os18 and label_os24 the OR is closer to 1 than for
      label_platinum, and the CI includes 1.
  P3  Residual: OR > 1 (suboptimal → resistant) for label_platinum, CI excluding 1.
  P4  Age: |r| ≥ 0.15 with older age → non-responder for label_os24; |r| < 0.15
      for label_platinum.
  P5  Aneuploidy and TMB: no BH-significant association (q ≥ 0.05) for any label.
  P6  Stage IV: OR > 1 for all labels; CI may include 1.

DECISION RULE (known-groups validity of each label, pre-specified):
  "BRCA-valid"   if OR(BRCA) < 1 and its 95% CI excludes 1;
  "direction only" if OR(BRCA) < 1 and the CI includes 1;
  "not supported" if OR(BRCA) ≥ 1.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu
from scipy.stats.contingency import odds_ratio

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"
LABELS = ["label_platinum", "label_pfiplat6", "label_response", "label_os18", "label_os24", "label_os12"]
BIN = ["brca_mut", "stage_iv", "residual_subopt"]
CONT = ["aneuploidy", "tmb", "age"]


def bh(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.minimum(q, 1.0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    a = ap.parse_args()
    dr = Path(a.data_root)

    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)

    brca = pd.read_csv(ROOT / "hrd" / "brca_status.csv").set_index("PATIENT_ID")
    m["brca_mut"] = brca["BRCA_any_mutated"].reindex(m.index)

    s = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_clinical_sample.txt", sep="\t", comment="#")
    s = s.drop_duplicates("PATIENT_ID").set_index("PATIENT_ID")
    m["aneuploidy"] = pd.to_numeric(s["ANEUPLOIDY_SCORE"], errors="coerce").reindex(m.index)
    m["tmb"] = pd.to_numeric(s["TMB_NONSYNONYMOUS"], errors="coerce").reindex(m.index)

    cdr = pd.read_excel(dr / "TCGA-CDR-SupplementalTableS1.xlsx", sheet_name="TCGA-CDR")
    cdr = cdr[cdr["type"] == "OV"].set_index("bcr_patient_barcode")
    m["age"] = pd.to_numeric(cdr["age_at_initial_pathologic_diagnosis"], errors="coerce").reindex(m.index)
    st = cdr["clinical_stage"].reindex(m.index).astype("string")
    m["stage_iv"] = np.where(st.str.startswith("Stage IV").fillna(False), 1,
                             np.where(st.str.startswith("Stage I").fillna(False), 0, np.nan))

    pub = pd.read_csv(dr / "ov_tcga_pub" / "ov_tcga_pub" / "data_clinical_sample.txt", sep="\t", comment="#")
    pub = pub.drop_duplicates("PATIENT_ID").set_index("PATIENT_ID")
    rd = pub["TUMOR_RESIDUAL_DISEASE"].reindex(m.index)
    m["residual_subopt"] = rd.map({"No Macroscopic disease": 0, "1-10 mm": 0, "11-20 mm": 1, ">20mm": 1})

    m[["brca_mut", "aneuploidy", "tmb", "age", "stage_iv", "residual_subopt"]].to_csv(OUT / "a3_covariates.csv")

    rows = []
    for lab in LABELS:
        fam = []
        for cov in BIN + CONT:
            d = m[[lab, cov]].dropna()
            y = d[lab].astype(int)
            r = {"label": lab, "covariate": cov, "n": len(d), "n_label1": int(y.sum())}
            if cov in BIN:
                x = d[cov].astype(int)
                t = np.array([[((x == 1) & (y == 1)).sum(), ((x == 1) & (y == 0)).sum()],
                              [((x == 0) & (y == 1)).sum(), ((x == 0) & (y == 0)).sum()]])
                orr = odds_ratio(t, kind="conditional")
                ci = orr.confidence_interval(0.95)
                r |= {"test": "Fisher", "cov1_label1": int(t[0, 0]), "cov1_label0": int(t[0, 1]),
                      "cov0_label1": int(t[1, 0]), "cov0_label0": int(t[1, 1]),
                      "effect": "OR", "estimate": orr.statistic, "ci_lo": ci.low, "ci_hi": ci.high,
                      "p": fisher_exact(t)[1]}
            else:
                x1, x0 = d.loc[y == 1, cov], d.loc[y == 0, cov]
                u = mannwhitneyu(x1, x0, alternative="two-sided")
                r |= {"test": "Mann-Whitney", "median_label1": float(x1.median()), "median_label0": float(x0.median()),
                      "effect": "rank-biserial r", "estimate": 2 * u.statistic / (len(x1) * len(x0)) - 1,
                      "ci_lo": np.nan, "ci_hi": np.nan, "p": u.pvalue}
            fam.append(r)
        q = bh([r["p"] for r in fam])
        for r, qq in zip(fam, q):
            r["q_bh_within_label"] = qq
        rows += fam
    res = pd.DataFrame(rows)
    res["supplement"] = res["label"] == "label_os12"
    res.to_csv(OUT / "a3_known_groups.csv", index=False)

    def g(lab, cov):
        return res[(res.label == lab) & (res.covariate == cov)].iloc[0]

    def fo(r):
        if r.effect == "OR":
            return (f"OR {r.estimate:.2f} [{r.ci_lo:.2f}, {r.ci_hi:.2f}], p = {r.p:.3g}, q = {r.q_bh_within_label:.3g} "
                    f"(cov=1: {r.cov1_label1}/{r.cov1_label1 + r.cov1_label0} label=1; cov=0: {r.cov0_label1}/{r.cov0_label1 + r.cov0_label0})")
        return (f"r = {r.estimate:+.3f}, medians {r.median_label1:.3g} vs {r.median_label0:.3g}, "
                f"p = {r.p:.3g}, q = {r.q_bh_within_label:.3g}, n = {r.n}")

    def verdict(lab):
        r = g(lab, "brca_mut")
        if r.estimate < 1 and r.ci_hi < 1:
            return "BRCA-valid"
        if r.estimate < 1:
            return "direction only"
        return "not supported"

    main_labels = [l for l in LABELS if l != "label_os12"]
    tab = res[~res.supplement][["label", "covariate", "n", "n_label1", "effect", "estimate", "ci_lo", "ci_hi", "p", "q_bh_within_label"]]
    L = ["# A3 part 1 — known-groups validity", "",
         "Platinum-treated patients (A1 cohort) with label and covariate non-missing. OR = odds of label = 1 "
         "(non-responder/resistant) when the covariate = 1. r > 0 = higher values in label = 1. BH within each label (6 tests).", "",
         "```", tab.round(3).to_string(index=False), "```", "",
         "## Predictions vs observed", "",
         f"- P1 BRCA, label_platinum: {fo(g('label_platinum','brca_mut'))}",
         f"- P1 BRCA, label_pfiplat6: {fo(g('label_pfiplat6','brca_mut'))}",
         f"- P2 BRCA, label_os18: {fo(g('label_os18','brca_mut'))}",
         f"- P2 BRCA, label_os24: {fo(g('label_os24','brca_mut'))}",
         f"- (BRCA, label_response: {fo(g('label_response','brca_mut'))})",
         f"- P3 residual, label_platinum: {fo(g('label_platinum','residual_subopt'))}",
         f"- P4 age, label_os24: {fo(g('label_os24','age'))}; label_platinum: {fo(g('label_platinum','age'))}",
         "- P5 aneuploidy/TMB, smallest q: "
         + ", ".join(f"{l} {res[(res.label == l) & res.covariate.isin(['aneuploidy', 'tmb'])].q_bh_within_label.min():.3g}" for l in main_labels),
         "- P6 stage IV ORs: " + ", ".join(f"{l} {g(l, 'stage_iv').estimate:.2f} [{g(l, 'stage_iv').ci_lo:.2f}, {g(l, 'stage_iv').ci_hi:.2f}]" for l in main_labels),
         "", "## Decision rule (BRCA known-groups validity)", ""]
    L += [f"- {l}: **{verdict(l)}**" for l in main_labels]
    L += ["", "Supplement: label_os12 rows in a3_known_groups.csv (supplement = True). Covariates per patient: a3_covariates.csv."]
    (OUT / "03_known_groups_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
