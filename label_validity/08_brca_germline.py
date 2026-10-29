#!/usr/bin/env python3
"""
label_validity/08_brca_germline.py
──────────────────────────────────
Q2 analysis A8 — BRCA1/2 known-groups test with germline + somatic variants, for every
label, including a direct same-patient comparison between label families.

Written 2026-10-29 ~19:30 ET, BEFORE the run. Prompted by the v3 peer review
(review_v3/PEER_REVIEW.md, major concern 1): A3 used somatic BRCA1/2 only (hrd/brca_status.csv,
PanCancer MAF), but the TCGA 2011 release (ov_tcga_pub data_mutations.txt) also carries
germline calls (Mutation_Status == "Germline": 51 BRCA1/2 rows).

DISCLOSURE — what was seen before these predictions were written
  * Count of germline/somatic BRCA rows in ov_tcga_pub (BRCA1 26 germline / 11 somatic; BRCA2 25 / 10;
    germline rows all truncating or splice).
  * One exploratory tabulation (main session, 2026-10-29 ~18:55 ET), carrier = any non-silent
    germline or somatic BRCA1/2, patients in ov_tcga_pub cases_sequenced, OS labels from the
    RNA-seq subset only (labels_master), sample OR / Fisher p:
      platinum 8/41 vs 53/145 (OR 0.42, p 0.058); pfiplat6 9/51 vs 63/175 (0.38, 0.016);
      os18 1/32 vs 11/98 (0.26, 0.29); os24 3/31 vs 19/95 (0.43, 0.28); response 5/55 vs 28/188 (0.57, 0.37).
    The reviewer reported the same tabulation.
  NOT seen: the truncating-only primary definition; OS labels in the full platinum cohort; the
  common-set comparison and bootstrap differences; BRCA1 vs BRCA2; CCNE1.
  Predictions P1–P3 are therefore informed by the exploratory tabulation; P4–P6 are not.

Population
  Platinum-treated patients (A1, n = 489) ∩ ov_tcga_pub case list `cases_sequenced` (316 tumours;
  patient = first 12 characters of the barcode).

Carrier definitions (BRCA1 or BRCA2; ov_tcga_pub data_mutations.txt)
  PRIMARY   germline or somatic truncating/splice variant: Variant_Classification in
            {Frame_Shift_Del, Frame_Shift_Ins, Nonsense_Mutation, Splice_Site}.
  SECONDARY (a) any non-silent germline or somatic (the exploratory definition);
            (b) germline only (truncating/splice); (c) BRCA1 only (primary rule);
            (d) BRCA2 only (primary rule); (e) somatic only, as in A3 (PanCancer hrd/brca_status.csv),
            restricted to the same sequenced patients, for comparison.
  Non-carriers: sequenced patients with no qualifying variant.

Labels (1 = non-responder / resistant)
  label_platinum, label_pfiplat6, label_response from labels_master.csv (A1).
  label_os18_all, label_os24_all: OS < 18 / 24 months, recomputed for ALL platinum-treated patients
  with src.preprocessing.extract_survival / assign_response_label (OS_MONTHS, OS_STATUS from
  ov_tcga_pan_can_atlas_2018; censored before the threshold → undetermined). A8 checks that these equal
  label_os18 / label_os24 wherever labels_master defines them (RNA-seq subset).

Tests (fixed before running)
  T1  Per label, all sequenced patients with the label determinate: 2×2 of carrier × label;
      conditional odds ratio with exact 95% CI (scipy odds_ratio, kind="conditional"); Fisher exact p.
  T2  COMMON SET: sequenced patients with label_platinum, label_os18_all and label_os24_all all determinate.
      Same OR per label in the common set. Difference in log OR, platinum − OS18 and platinum − OS24
      (and pfiplat6 − OS24 when pfiplat6 is also determinate in the common set), with 0.5 added to
      every cell (Haldane). 95% percentile CI from 2,000 bootstrap resamples of patients
      (numpy default_rng(42)).
  T3  BRCA1 vs BRCA2 separately (T1, platinum and pfiplat6 only).
  T4  CCNE1 amplification (GISTIC = 2 in ov_tcga_pub data_cna.txt; first CCNE1 row; patients in
      cases_cna ∩ platinum-treated) vs each label (T1 method). Secondary anchor: CCNE1 amplification
      is associated with primary platinum resistance (Etemadmoghadam 2009).

PREDICTIONS
  P1  label_platinum, primary carrier definition: OR < 1, 95% CI includes 1.
  P2  label_pfiplat6: OR < 1, 95% CI excludes 1.
  P3  label_os18_all and label_os24_all: OR < 1, 95% CI includes 1.
  P4  Common set: the bootstrap 95% CI of log OR(platinum) − log OR(OS24) includes 0, and likewise
      for OS18.
  P5  BRCA2 carriers have a lower OR than BRCA1 carriers for label_platinum (point estimates).
  P6  CCNE1 amplification: OR > 1 for label_platinum; 95% CI includes 1.

DECISION RULES (for the manuscript)
  * The primary BRCA definition in the manuscript becomes germline + somatic truncating/splice
    (this script). The A3 somatic-only result is reported as a secondary analysis.
  * If both T2 differences have 95% CIs that include 0, the manuscript does NOT claim that BRCA
    separates the platinum labels from the OS labels. BRCA is reported as associated with a
    favourable outcome under every label (convergent evidence), and the Results heading
    "Only the platinum labels show known-groups validity" is withdrawn.
  * If a difference CI excludes 0 with platinum more strongly associated (log-OR difference < 0),
    the discriminant claim is kept for that comparison and stated with the CI.
  * The A3 verdict labels ("BRCA-valid" etc.) are applied to T1 unchanged:
    "BRCA-valid" if OR < 1 and CI excludes 1; "direction only" if OR < 1 and CI includes 1;
    "not supported" if OR ≥ 1.

Inputs
  label_validity/outputs/labels_master.csv, hrd/brca_status.csv
  <data-root>/ov_tcga_pub/ov_tcga_pub/{data_mutations.txt, data_cna.txt,
      case_lists/cases_sequenced.txt, case_lists/cases_cna.txt}
  <data-root>/ov_tcga_pan_can_atlas_2018/{data_clinical_patient.txt, data_timeline_treatment.txt}
Outputs → label_validity/outputs/a8_brca_tests.csv, a8_brca_diff.csv, a8_carriers.csv,
          08_brca_germline_summary.md
Run (from the repo root; no model fitting, so the scikit-learn version does not matter):
  python label_validity/08_brca_germline.py --data-root "<...>/OV Data/Project data"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
from scipy.stats.contingency import odds_ratio

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.preprocessing import assign_response_label, extract_survival  # noqa: E402

TRUNC = {"Frame_Shift_Del", "Frame_Shift_Ins", "Nonsense_Mutation", "Splice_Site"}
N_BOOT, SEED = 2000, 42


def case_ids(path: Path) -> set[str]:
    txt = path.read_text(encoding="utf-8")
    ids = txt.split("case_list_ids:")[1].split()
    return {x[:12] for x in ids}


def or_test(x: pd.Series, y: pd.Series) -> dict:
    """x = exposure (0/1), y = label (0/1); both aligned, no missing."""
    a = int(((x == 1) & (y == 1)).sum()); b = int(((x == 1) & (y == 0)).sum())
    c = int(((x == 0) & (y == 1)).sum()); d = int(((x == 0) & (y == 0)).sum())
    res = odds_ratio([[a, b], [c, d]], kind="conditional")
    ci = res.confidence_interval(0.95)
    return dict(exp_pos=a, exp_n=a + b, unexp_pos=c, unexp_n=c + d, n=a + b + c + d,
                OR=float(res.statistic), lo=float(ci.low), hi=float(ci.high),
                p=float(fisher_exact([[a, b], [c, d]])[1]))


def verdict(r: dict) -> str:
    if r["OR"] >= 1:
        return "not supported"
    return "BRCA-valid" if r["hi"] < 1 else "direction only"


def log_or_h(x: np.ndarray, y: np.ndarray) -> float:
    a = np.sum((x == 1) & (y == 1)) + 0.5; b = np.sum((x == 1) & (y == 0)) + 0.5
    c = np.sum((x == 0) & (y == 1)) + 0.5; d = np.sum((x == 0) & (y == 0)) + 0.5
    return float(np.log(a * d / (b * c)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    ap.add_argument("--out", default=str(ROOT / "label_validity" / "outputs"))
    a = ap.parse_args()
    dr, out = Path(a.data_root), Path(a.out)
    pub = dr / "ov_tcga_pub" / "ov_tcga_pub"
    pc = dr / "ov_tcga_pan_can_atlas_2018"

    m = pd.read_csv(ROOT / "label_validity" / "outputs" / "labels_master.csv", index_col=0)
    plat_ids = set(m.index)

    # OS labels for all platinum-treated patients (same rule as A1/src)
    clin = pd.read_csv(pc / "data_clinical_patient.txt", sep="\t", comment="#")
    surv = extract_survival(clin, "OS_MONTHS", "OS_STATUS")
    surv = surv[surv["PATIENT_ID"].isin(plat_ids)].set_index("PATIENT_ID")
    for thr in (18, 24):
        m[f"label_os{thr}_all"] = assign_response_label(surv, "OS_MONTHS", thr).reindex(m.index)
        chk = m[[f"label_os{thr}", f"label_os{thr}_all"]].dropna(subset=[f"label_os{thr}"])
        mism = int((chk[f"label_os{thr}"] != chk[f"label_os{thr}_all"]).sum())
        assert mism == 0, f"OS{thr}: {mism} mismatches with labels_master"

    # carriers
    seq = case_ids(pub / "case_lists" / "cases_sequenced.txt") & plat_ids
    mut = pd.read_csv(pub / "data_mutations.txt", sep="\t", comment="#", low_memory=False)
    mut = mut[mut["Hugo_Symbol"].isin(["BRCA1", "BRCA2"]) & (mut["Variant_Classification"] != "Silent")].copy()
    mut["pid"] = mut["Tumor_Sample_Barcode"].str[:12]
    mut = mut[mut["pid"].isin(seq)]
    mut["trunc"] = mut["Variant_Classification"].isin(TRUNC)
    mut[["pid", "Hugo_Symbol", "Mutation_Status", "Variant_Classification", "trunc"]].to_csv(
        out / "a8_carriers.csv", index=False)

    def carriers(rows: pd.DataFrame) -> pd.Series:
        s = pd.Series(0, index=sorted(seq), dtype=int)
        s[s.index.isin(set(rows["pid"]))] = 1
        return s

    tr = mut[mut["trunc"] & mut["Mutation_Status"].isin(["Germline", "Somatic"])]
    defs = {
        "primary_trunc_germ_som": carriers(tr),
        "any_nonsilent_germ_som": carriers(mut[mut["Mutation_Status"].isin(["Germline", "Somatic"])]),
        "germline_trunc": carriers(tr[tr["Mutation_Status"] == "Germline"]),
        "BRCA1_primary": carriers(tr[tr["Hugo_Symbol"] == "BRCA1"]),
        "BRCA2_primary": carriers(tr[tr["Hugo_Symbol"] == "BRCA2"]),
    }
    a3 = pd.read_csv(ROOT / "hrd" / "brca_status.csv").set_index("PATIENT_ID")["BRCA_any_mutated"]
    defs["somatic_pancan_A3"] = a3.reindex(sorted(seq))

    labels = ["label_platinum", "label_pfiplat6", "label_response", "label_os18_all", "label_os24_all"]
    rows = []
    for dname, x in defs.items():
        labs = labels if dname in ("primary_trunc_germ_som", "any_nonsilent_germ_som",
                                   "germline_trunc", "somatic_pancan_A3") else ["label_platinum", "label_pfiplat6"]
        for lab in labs:
            d = pd.DataFrame({"x": x, "y": m[lab].reindex(x.index)}).dropna()
            r = or_test(d["x"].astype(int), d["y"].astype(int))
            rows.append(dict(set="T1_all", carrier_def=dname, label=lab, **r, verdict=verdict(r)))

    # T2 common set (primary definition)
    x = defs["primary_trunc_germ_som"]
    cs = pd.DataFrame({"x": x, **{l: m[l].reindex(x.index) for l in labels}})
    common = cs.dropna(subset=["label_platinum", "label_os18_all", "label_os24_all"])
    for lab in ["label_platinum", "label_os18_all", "label_os24_all", "label_pfiplat6"]:
        d = common[["x", lab]].dropna()
        r = or_test(d["x"].astype(int), d[lab].astype(int))
        rows.append(dict(set="T2_common", carrier_def="primary_trunc_germ_som", label=lab, **r, verdict=verdict(r)))

    rng = np.random.default_rng(SEED)
    pairs = [("label_platinum", "label_os18_all"), ("label_platinum", "label_os24_all"),
             ("label_pfiplat6", "label_os24_all")]
    diffs = []
    for l1, l2 in pairs:
        d = common[["x", l1, l2]].dropna()
        X, Y1, Y2 = d["x"].to_numpy(), d[l1].to_numpy(), d[l2].to_numpy()
        est = log_or_h(X, Y1) - log_or_h(X, Y2)
        bs = np.empty(N_BOOT)
        for i in range(N_BOOT):
            idx = rng.integers(0, len(d), len(d))
            bs[i] = log_or_h(X[idx], Y1[idx]) - log_or_h(X[idx], Y2[idx])
        lo, hi = np.percentile(bs, [2.5, 97.5])
        diffs.append(dict(label_1=l1, label_2=l2, n=len(d), carriers=int(X.sum()),
                          logOR_diff=est, lo=lo, hi=hi, ratio_of_ORs=float(np.exp(est)),
                          ci_includes_0=bool(lo <= 0 <= hi)))
    diffs = pd.DataFrame(diffs)
    diffs.to_csv(out / "a8_brca_diff.csv", index=False)

    # T4 CCNE1
    cna = pd.read_csv(pub / "data_cna.txt", sep="\t")
    ccne = cna[cna["Hugo_Symbol"] == "CCNE1"].iloc[0].drop(["Hugo_Symbol", "Entrez_Gene_Id"])
    ccne.index = ccne.index.str[:12]
    ccne = ccne[~ccne.index.duplicated()]
    cna_ids = case_ids(pub / "case_lists" / "cases_cna.txt") & plat_ids
    amp = (pd.to_numeric(ccne, errors="coerce") == 2).astype(int).reindex(sorted(cna_ids)).dropna()
    for lab in labels:
        d = pd.DataFrame({"x": amp, "y": m[lab].reindex(amp.index)}).dropna()
        r = or_test(d["x"].astype(int), d["y"].astype(int))
        rows.append(dict(set="T4_CCNE1_amp", carrier_def="CCNE1_GISTIC2", label=lab, **r, verdict=""))

    res = pd.DataFrame(rows)
    res.to_csv(out / "a8_brca_tests.csv", index=False)

    def g(s, dname, lab):
        return res[(res.set == s) & (res.carrier_def == dname) & (res.label == lab)].iloc[0]

    def fo(r):
        return (f"{r.exp_pos}/{r.exp_n} vs {r.unexp_pos}/{r.unexp_n}; OR {r.OR:.2f} "
                f"[{r.lo:.2f}, {r.hi:.2f}], p {r.p:.3f}" + (f" — {r.verdict}" if r.verdict else ""))

    P = "primary_trunc_germ_som"
    L = ["# A8 — BRCA1/2 germline + somatic known-groups test", "",
         f"Sequenced platinum-treated patients: {len(seq)}; primary carriers: {int(defs[P].sum())} "
         f"(germline truncating {int(defs['germline_trunc'].sum())}); common set n = {len(common)}.", "",
         "## T1 — each label, all determinate patients (carriers non-responding vs non-carriers)", ""]
    for dname in ["primary_trunc_germ_som", "any_nonsilent_germ_som", "germline_trunc", "somatic_pancan_A3"]:
        L.append(f"**{dname}**")
        for lab in labels:
            L.append(f"- {lab}: {fo(g('T1_all', dname, lab))}")
        L.append("")
    L += ["## T2 — common set (primary definition)", ""]
    for lab in ["label_platinum", "label_os18_all", "label_os24_all", "label_pfiplat6"]:
        L.append(f"- {lab}: {fo(g('T2_common', P, lab))}")
    L += ["", "Difference in log OR (Haldane), 2,000 bootstrap resamples:", ""]
    for r in diffs.itertuples():
        L.append(f"- {r.label_1} − {r.label_2}: {r.logOR_diff:+.2f} [{r.lo:+.2f}, {r.hi:+.2f}] "
                 f"(ratio of ORs {r.ratio_of_ORs:.2f}; n {r.n}, carriers {r.carriers}); CI includes 0: {r.ci_includes_0}")
    L += ["", "## T3 — BRCA1 vs BRCA2 (primary rule)", ""]
    for dname in ["BRCA1_primary", "BRCA2_primary"]:
        for lab in ["label_platinum", "label_pfiplat6"]:
            L.append(f"- {dname}, {lab}: {fo(g('T1_all', dname, lab))}")
    L += ["", "## T4 — CCNE1 amplification", ""]
    for lab in labels:
        L.append(f"- {lab}: {fo(g('T4_CCNE1_amp', 'CCNE1_GISTIC2', lab))}")
    L += ["", "## Prediction scorecard", "", "(to be completed after the run)", ""]
    (out / "08_brca_germline_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("A8 done")


if __name__ == "__main__":
    main()
