#!/usr/bin/env python3
"""
label_validity/00_gate_pfi_coverage.py
──────────────────────────────────────
Q2 reorganisation, decision gate G1–G3
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §3).

Descriptive counts and cross-tabs only. No models, no p-values, no scipy.
Cohorts are rebuilt with the repo's own functions (src.data_loader,
src.preprocessing) — nothing re-implemented — and checked against the
documented sizes (fixes/phase1_provenance.md: 489 platinum; 214/206/199 with
11/22/36 events) before anything else is reported.

Inputs (read-only)
──────────────────
  <data-root>/TCGA-CDR-SupplementalTableS1.xlsx          sheet "TCGA-CDR"
  <data-root>/ov_tcga_pan_can_atlas_2018/                clinical, treatment, status, RSEM header
  <data-root>/ov_tcga_pub/ov_tcga_pub/data_clinical_patient.txt   (TCGA Nature 2011)
  phase2/outputs/cox_patients_with_risk.csv              (432 Cox cohort)

Outputs → label_validity/outputs/
  gate_patient_table.csv   one row per patient, every gate field + provenance
  gate_g1_coverage.csv
  gate_g2_platinum_sources.csv
  gate_g3_crosstabs.csv    long-form cross-tabs
  00_gate_summary.md       predictions vs observed, pass/fail per gate

Usage
─────
  python label_validity/00_gate_pfi_coverage.py
  python label_validity/00_gate_pfi_coverage.py --data-root "C:/PROJECTS/OV Data/Project data"

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before this script was run — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Disclosure: while inspecting column names before writing this header, the
following were already seen and are NOT predictions:
  * CDR OV: 587 patients; PFI non-null 587 (414 events / 173 censored);
    PFI.time non-null 582; treatment_outcome_first_course categories and
    counts across all 587 OV patients; 45 rows marked Redacted.
  * Category labels (no counts) of ov_tcga_pub PLATINUM_STATUS
    {Missing, Resistant, Sensitive, Tooearly}, PRIMARY_THERAPY_OUTCOME_SUCCESS,
    treatment REGIMEN_INDICATION and platinum AGENT strings.
  * outputs/results/label_investigation_coverage_timeline.csv: the "142"
    is ROWS of data_timeline_status.txt in the platinum cohort, not patients.
Nothing below about intersections, ov_tcga_pub counts, timeline coverage or
concordance had been looked at.

G1  PFI coverage (CDR PFI and PFI.time both non-null)
  P1.1  ≥ 460 of the 489 platinum patients have CDR PFI.
  P1.2  Each classification cohort (12/18/24m) has ≥ 190 patients with PFI.
  P1.3  ≥ 410 of the 432 Cox patients have PFI.
  RULE  PASS if every classification cohort has ≥ 120 patients with PFI.

G2  Platinum-specific sources
  P2.1  ov_tcga_pub PLATINUM_STATUS ∈ {Resistant, Sensitive} for ≥ 250
        patients overall and ≥ 150 in the 24m classification cohort.
  P2.2  ≥ 80 % of the 489 platinum patients have a first-line (REGIMEN_INDICATION
        == "Adjuvant") platinum row with a non-missing STOP_DATE.
  P2.3  Where both exist, PFI-from-last-first-line-platinum < 183 d agrees with
        PLATINUM_STATUS == Resistant in ≥ 80 % of patients.
  P2.4  Substring matching of platinum AGENT strings adds ≤ 20 patients to the
        489 exact-match platinum cohort.
  RULE  PASS if either source gives a usable platinum label (Resistant/Sensitive,
        or a determinate short/long PFI-from-platinum) for ≥ 150 patients in
        the 24m classification cohort.

G3  Response field vs PFI vs OS labels
  P3.1  Unique patients with PRIMARY_THERAPY_OUTCOME_SUCCESS in the pan-can
        timeline, within the 489 platinum cohort: 120–142.
  P3.2  Of PD patients with a determinate platinum label, ≥ 70 % are
        Resistant / short PFI-from-platinum.
  P3.3  Of CR patients with a determinate platinum label, ≥ 70 % are
        Sensitive / long PFI-from-platinum.
  P3.4  Where pan-can PTOS and CDR treatment_outcome_first_course both exist,
        category agreement ≥ 95 % (same TCGA clinical source).
  P3.5  OS-threshold labels (18m, 24m) flag < 50 % of Resistant patients as
        non-responders (sensitivity < 0.5).
  RULE  "High" concordance = P(Resistant or short | PD) ≥ 0.80 with ≥ 10 PD
        patients. If lower, report it as a property of the resource; do not
        pick the convenient field.

Fixed definitions (stated, not tuned)
  * 6 months = 183 days.
  * PFI-from-platinum (days) = CDR PFI.time − max STOP_DATE over platinum rows
    with REGIMEN_INDICATION == "Adjuvant". Both are days from diagnosis.
    short: PFI == 1 and value < 183; long: value ≥ 183;
    indeterminate: PFI == 0 and value < 183; negative values are counted
    separately ("event before end of first-line platinum") and also classed short.
  * CDR PFI.time is from diagnosis. It is reported only as a distribution and as
    descriptive cross-tabs at 6 and 12 months from diagnosis; no label is
    chosen from it here (that is A1's job).
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data_loader import load_clinical, load_treatment  # noqa: E402
from src.preprocessing import (  # noqa: E402
    build_labelled_survival,
    extract_survival,
    identify_platinum_patients,
)

SIX_MO = 183
EXPECTED = {"platinum": 489, 12: (214, 11), 18: (206, 22), 24: (199, 36)}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    p.add_argument("--config", default=str(ROOT / "config" / "config.yaml"))
    p.add_argument("--out-dir", default=str(ROOT / "label_validity" / "outputs"))
    return p.parse_args()


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fmt_prop(k: int, n: int) -> str:
    if n == 0:
        return "0/0"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {k / n:.3f} [{lo:.3f}, {hi:.3f}]"


def main() -> None:
    a = parse_args()
    root = Path(a.data_root)
    pc = root / "ov_tcga_pan_can_atlas_2018"
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cfg = yaml.safe_load(open(a.config))
    ccfg = cfg["clinical"]

    # ── Rebuild cohorts with repo functions ───────────────────────────────
    clinical = load_clinical(pc, cfg["data"]["clinical_file"])
    treatment = load_treatment(pc, cfg["data"]["treatment_file"])
    surv = extract_survival(clinical, ccfg["time_col"], ccfg["status_col"])
    plat_ids = set(identify_platinum_patients(treatment, ccfg["platinum_drugs"]))
    labelled = build_labelled_survival(surv, sorted(plat_ids), ccfg["time_col"], ccfg["thresholds"])
    # align_expression_to_labels() keeps labelled ∩ expression columns (12-char);
    # the header alone determines that membership.
    hdr = pd.read_csv(pc / cfg["data"]["expression_file"], sep="\t", comment="#", nrows=0)
    rna_ids = {c[:12] for c in hdr.columns if c.startswith("TCGA-")}
    cls = {}
    for thr, df in labelled.items():
        d = df[df["PATIENT_ID"].isin(rna_ids)].set_index("PATIENT_ID")
        cls[thr] = d["response"].astype(int)

    checks = [("platinum", len(plat_ids), EXPECTED["platinum"])]
    for thr in (12, 18, 24):
        checks.append((f"{thr}m n", len(cls[thr]), EXPECTED[thr][0]))
        checks.append((f"{thr}m events", int(cls[thr].sum()), EXPECTED[thr][1]))
    bad = [c for c in checks if c[1] != c[2]]
    if bad:
        raise SystemExit(f"Cohort reproduction FAILED, stopping: {bad}")

    cox = pd.read_csv(ROOT / "phase2" / "outputs" / "cox_patients_with_risk.csv")
    cox_ids = set(cox["PATIENT_ID"])
    if len(cox_ids) != 432:
        raise SystemExit(f"Cox cohort has {len(cox_ids)} patients, expected 432")

    # ── Sources ───────────────────────────────────────────────────────────
    cdr = pd.read_excel(root / "TCGA-CDR-SupplementalTableS1.xlsx", sheet_name="TCGA-CDR")
    cdr = cdr[cdr["type"] == "OV"].set_index("bcr_patient_barcode")
    pub = pd.read_csv(root / "ov_tcga_pub" / "ov_tcga_pub" / "data_clinical_patient.txt",
                      sep="\t", comment="#").set_index("PATIENT_ID")
    status = pd.read_csv(pc / "data_timeline_status.txt", sep="\t", comment="#", low_memory=False)

    # Platinum rows by substring (for P2.4 and first-line stop date)
    is_plat = treatment["AGENT"].astype(str).str.upper().str.contains("PLATIN")
    plat_sub_ids = set(treatment.loc[is_plat, "PATIENT_ID"].dropna())
    fl = treatment[is_plat & (treatment["REGIMEN_INDICATION"] == "Adjuvant")].copy()
    fl["STOP_DATE"] = pd.to_numeric(fl["STOP_DATE"], errors="coerce")
    fl_any = set(fl["PATIENT_ID"])
    fl_stop = fl.dropna(subset=["STOP_DATE"]).groupby("PATIENT_ID")["STOP_DATE"].max()

    # PTOS per patient from pan-can timeline (unique patients; flag conflicts)
    st = status.dropna(subset=["PRIMARY_THERAPY_OUTCOME_SUCCESS"])
    ptos_sets = st.groupby("PATIENT_ID")["PRIMARY_THERAPY_OUTCOME_SUCCESS"].agg(lambda s: sorted(set(s)))
    ptos = ptos_sets.apply(lambda v: v[0] if len(v) == 1 else "CONFLICT:" + "|".join(v))

    # ── Per-patient table ────────────────────────────────────────────────
    ids = sorted(plat_ids | plat_sub_ids | cox_ids | set(pub.index) | set(cdr.index))
    t = pd.DataFrame(index=pd.Index(ids, name="PATIENT_ID"))
    t["in_platinum_exact"] = t.index.isin(plat_ids)
    t["in_platinum_substring"] = t.index.isin(plat_sub_ids)
    t["in_cox432"] = t.index.isin(cox_ids)
    t["has_rnaseq"] = t.index.isin(rna_ids)
    for thr in (12, 18, 24):
        t[f"in_cls{thr}"] = t.index.isin(cls[thr].index)
        t[f"label_os{thr}"] = cls[thr].reindex(t.index)
    t["cdr_PFI"] = cdr["PFI"].reindex(t.index)
    t["cdr_PFI_time_d"] = pd.to_numeric(cdr["PFI.time"], errors="coerce").reindex(t.index)
    t["cdr_redaction"] = cdr["Redaction"].reindex(t.index)
    t["cdr_treatment_outcome_first_course"] = cdr["treatment_outcome_first_course"].reindex(t.index)
    t["has_cdr_pfi"] = t["cdr_PFI"].notna() & t["cdr_PFI_time_d"].notna()
    t["pub_platinum_status"] = pub["PLATINUM_STATUS"].reindex(t.index)
    t["pub_ptos"] = pub["PRIMARY_THERAPY_OUTCOME_SUCCESS"].reindex(t.index)
    t["pancan_ptos"] = ptos.reindex(t.index)
    t["has_firstline_platinum_row"] = t.index.isin(fl_any)
    t["firstline_platinum_stop_d"] = fl_stop.reindex(t.index)
    t["pfi_from_platinum_d"] = t["cdr_PFI_time_d"] - t["firstline_platinum_stop_d"]

    def pfi_plat_class(r):
        v, e = r["pfi_from_platinum_d"], r["cdr_PFI"]
        if pd.isna(v) or pd.isna(e):
            return pd.NA
        if v >= SIX_MO:
            return "long"
        if e == 1:
            return "short"
        return "indeterminate"

    t["pfi_plat6_class"] = t.apply(pfi_plat_class, axis=1)
    t["pfi_plat_negative"] = t["pfi_from_platinum_d"] < 0
    t.to_csv(out / "gate_patient_table.csv")

    # ── G1 ────────────────────────────────────────────────────────────────
    cohorts = {
        "platinum_exact_489": t["in_platinum_exact"],
        "cox_432": t["in_cox432"],
        "cls_12m": t["in_cls12"], "cls_18m": t["in_cls18"], "cls_24m": t["in_cls24"],
    }
    g1 = []
    for name, m in cohorts.items():
        sub = t[m]
        g1.append({
            "cohort": name, "n": len(sub),
            "in_cdr": int(sub["cdr_PFI"].notna().sum()),
            "has_cdr_pfi": int(sub["has_cdr_pfi"].sum()),
            "pfi_events": int((sub["cdr_PFI"] == 1).sum()),
            "redacted": int(sub["cdr_redaction"].notna().sum()),
        })
    g1 = pd.DataFrame(g1)
    g1.to_csv(out / "gate_g1_coverage.csv", index=False)
    g1_pass = bool((g1.loc[g1.cohort.str.startswith("cls"), "has_cdr_pfi"] >= 120).all())

    # ── G2 ────────────────────────────────────────────────────────────────
    det_ps = t["pub_platinum_status"].isin(["Resistant", "Sensitive"])
    det_pp = t["pfi_plat6_class"].isin(["short", "long"])
    g2 = []
    for name, m in {"all_patients": pd.Series(True, index=t.index), **cohorts}.items():
        sub = t[m]
        row = {"cohort": name, "n": len(sub)}
        for lab in ["Resistant", "Sensitive", "Tooearly", "Missing"]:
            row[f"pub_{lab}"] = int((sub["pub_platinum_status"] == lab).sum())
        row["pub_absent"] = int(sub["pub_platinum_status"].isna().sum())
        row["pub_determinate"] = int(det_ps[m].sum())
        row["has_firstline_platinum_row"] = int(sub["has_firstline_platinum_row"].sum())
        row["has_firstline_stop_date"] = int(sub["firstline_platinum_stop_d"].notna().sum())
        for c in ["short", "long", "indeterminate"]:
            row[f"pfi_plat6_{c}"] = int((sub["pfi_plat6_class"] == c).sum())
        row["pfi_plat_negative"] = int(sub["pfi_plat_negative"].fillna(False).sum())
        row["either_determinate"] = int((det_ps[m] | det_pp[m]).sum())
        g2.append(row)
    g2 = pd.DataFrame(g2)
    g2.to_csv(out / "gate_g2_platinum_sources.csv", index=False)
    g2_pass = int(g2.loc[g2.cohort == "cls_24m", "either_determinate"].iloc[0]) >= 150

    # ── G3 cross-tabs (platinum exact cohort) ─────────────────────────────
    P = t[t["in_platinum_exact"]].copy()
    P["cdr_pfi_from_dx_6m"] = pd.cut(P["cdr_PFI_time_d"], [-1e9, SIX_MO, 1e9], right=False,
                                     labels=["<6m_from_dx", ">=6m_from_dx"])
    P["cdr_pfi_from_dx_12m"] = pd.cut(P["cdr_PFI_time_d"], [-1e9, 365, 1e9], right=False,
                                      labels=["<12m_from_dx", ">=12m_from_dx"])
    pairs = [
        ("pancan_ptos", "pub_platinum_status"),
        ("pancan_ptos", "pfi_plat6_class"),
        ("pub_ptos", "pub_platinum_status"),
        ("pub_platinum_status", "pfi_plat6_class"),
        ("pancan_ptos", "cdr_treatment_outcome_first_course"),
        ("pancan_ptos", "pub_ptos"),
        ("pancan_ptos", "label_os18"), ("pancan_ptos", "label_os24"),
        ("pub_platinum_status", "label_os18"), ("pub_platinum_status", "label_os24"),
        ("pfi_plat6_class", "label_os18"), ("pfi_plat6_class", "label_os24"),
        ("pub_platinum_status", "cdr_pfi_from_dx_6m"),
        ("pub_platinum_status", "cdr_pfi_from_dx_12m"),
    ]
    rows = []
    for r, c in pairs:
        ct = pd.crosstab(P[r].astype("string").fillna("NA"), P[c].astype("string").fillna("NA"))
        for ri in ct.index:
            for ci in ct.columns:
                rows.append({"row_var": r, "col_var": c, "row": ri, "col": ci, "n": int(ct.loc[ri, ci])})
    g3 = pd.DataFrame(rows)
    g3.to_csv(out / "gate_g3_crosstabs.csv", index=False)

    def cnt(mask) -> int:
        return int(mask.sum())

    n_ptos = cnt(P["pancan_ptos"].notna())
    n_ptos_conf = cnt(P["pancan_ptos"].astype("string").str.startswith("CONFLICT").fillna(False))
    pd_ = P["pancan_ptos"] == "Progressive Disease"
    cr_ = P["pancan_ptos"] == "Complete Remission/Response"
    # Platinum label: ov_tcga_pub status first; PFI-from-platinum where status absent/indeterminate.
    res = (P["pub_platinum_status"] == "Resistant") | (~det_ps[P.index] & (P["pfi_plat6_class"] == "short"))
    sen = (P["pub_platinum_status"] == "Sensitive") | (~det_ps[P.index] & (P["pfi_plat6_class"] == "long"))
    det = res | sen
    pd_res = (cnt(pd_ & res), cnt(pd_ & det))
    cr_sen = (cnt(cr_ & sen), cnt(cr_ & det))
    # Each source separately
    pd_res_pub = (cnt(pd_ & (P["pub_platinum_status"] == "Resistant")), cnt(pd_ & det_ps[P.index]))
    pd_res_pp = (cnt(pd_ & (P["pfi_plat6_class"] == "short")), cnt(pd_ & det_pp[P.index]))
    cr_sen_pub = (cnt(cr_ & (P["pub_platinum_status"] == "Sensitive")), cnt(cr_ & det_ps[P.index]))
    cr_sen_pp = (cnt(cr_ & (P["pfi_plat6_class"] == "long")), cnt(cr_ & det_pp[P.index]))
    both_ps_pp = det_ps[P.index] & det_pp[P.index]
    agree_ps_pp = cnt(both_ps_pp & (((P["pub_platinum_status"] == "Resistant") & (P["pfi_plat6_class"] == "short"))
                                    | ((P["pub_platinum_status"] == "Sensitive") & (P["pfi_plat6_class"] == "long"))))
    # PTOS vs CDR first-course outcome
    m = P["pancan_ptos"].notna() & ~P["pancan_ptos"].astype("string").str.startswith("CONFLICT").fillna(False)
    cdr_out = P["cdr_treatment_outcome_first_course"].astype("string")
    both_out = m & cdr_out.notna() & ~cdr_out.str.startswith("[").fillna(True)
    agree_out = cnt(both_out & (P["pancan_ptos"].astype("string") == cdr_out))
    # OS sensitivity for Resistant
    os_sens = {}
    for thr in (18, 24):
        lab = P[f"label_os{thr}"]
        os_sens[thr] = (cnt(res & (lab == 1)), cnt(res & lab.notna()))
    g3_pass = pd_res[1] >= 10 and pd_res[1] > 0 and pd_res[0] / pd_res[1] >= 0.80

    # ── Summary ───────────────────────────────────────────────────────────
    def g(cohort, col, df):
        return int(df.loc[df.cohort == cohort, col].iloc[0])

    L = []
    L.append("# Gate G1–G3 summary — label_validity/00_gate_pfi_coverage.py\n")
    L.append("Cohort reproduction (repo functions): " + "; ".join(f"{a}={b}" for a, b, _ in checks)
             + " — all match fixes/phase1_provenance.md. Cox cohort 432 read from phase2/outputs.\n")
    L.append("## G1 — CDR PFI coverage\n")
    L.append("```\n" + g1.to_string(index=False) + "\n```")
    L.append("")
    L.append(f"- P1.1 ≥460/489 platinum with PFI → observed {g('platinum_exact_489','has_cdr_pfi',g1)}")
    L.append(f"- P1.2 each cls cohort ≥190 → observed " + ", ".join(
        f"{c}: {g(c,'has_cdr_pfi',g1)}/{g(c,'n',g1)}" for c in ("cls_12m", "cls_18m", "cls_24m")))
    L.append(f"- P1.3 ≥410/432 Cox → observed {g('cox_432','has_cdr_pfi',g1)}")
    L.append(f"- **G1 {'PASS' if g1_pass else 'FAIL'}** (rule: every cls cohort ≥120 with PFI)\n")
    L.append("## G2 — platinum-specific sources\n")
    L.append("```\n" + g2.to_string(index=False) + "\n```")
    L.append("")
    L.append(f"- P2.1 pub Resistant/Sensitive ≥250 overall, ≥150 in cls_24m → observed "
             f"{g('all_patients','pub_determinate',g2)} overall, {g('cls_24m','pub_determinate',g2)} in cls_24m")
    L.append(f"- P2.2 ≥80% of 489 with first-line platinum STOP_DATE → observed "
             f"{fmt_prop(g('platinum_exact_489','has_firstline_stop_date',g2), 489)}")
    L.append(f"- P2.3 PFI-from-platinum vs pub status agreement ≥0.80 → observed {fmt_prop(agree_ps_pp, cnt(both_ps_pp))}")
    extra = len(plat_sub_ids - plat_ids)
    extra_rna = len((plat_sub_ids - plat_ids) & rna_ids)
    L.append(f"- P2.4 substring match adds ≤20 to 489 → observed +{extra} patients ({extra_rna} with RNA-seq); "
             f"exact-match patients not found by substring: {len(plat_ids - plat_sub_ids)}")
    L.append(f"- **G2 {'PASS' if g2_pass else 'FAIL'}** (rule: ≥150 determinate in cls_24m from either source; "
             f"observed {g('cls_24m','either_determinate',g2)})\n")
    L.append("## G3 — response field vs platinum label vs OS labels (platinum cohort, n=489)\n")
    L.append(f"- P3.1 unique pan-can PTOS patients 120–142 → observed {n_ptos} ({n_ptos_conf} with conflicting values)")
    L.append(f"- P3.2 P(Resistant/short | PD) ≥0.70 → combined {fmt_prop(*pd_res)}; "
             f"pub status only {fmt_prop(*pd_res_pub)}; PFI-from-platinum only {fmt_prop(*pd_res_pp)}")
    L.append(f"- P3.3 P(Sensitive/long | CR) ≥0.70 → combined {fmt_prop(*cr_sen)}; "
             f"pub status only {fmt_prop(*cr_sen_pub)}; PFI-from-platinum only {fmt_prop(*cr_sen_pp)}")
    L.append(f"- P3.4 pan-can PTOS vs CDR first-course outcome agreement ≥0.95 → observed {fmt_prop(agree_out, cnt(both_out))}")
    for thr in (18, 24):
        L.append(f"- P3.5 OS{thr} sensitivity for Resistant <0.5 → observed {fmt_prop(*os_sens[thr])}")
    L.append(f"- **G3 {'PASS' if g3_pass else 'FAIL'}** (rule: P(Resistant/short | PD) ≥0.80 with ≥10 PD)\n")
    L.append("Full cross-tabs: gate_g3_crosstabs.csv. Per-patient provenance: gate_patient_table.csv.")
    L.append("Combined platinum label = ov_tcga_pub PLATINUM_STATUS where Resistant/Sensitive, "
             "else PFI-from-first-line-platinum short/long. Proportions with Wilson 95% CI.")
    (out / "00_gate_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
