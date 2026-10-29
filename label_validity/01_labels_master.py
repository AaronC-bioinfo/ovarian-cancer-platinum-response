#!/usr/bin/env python3
"""
label_validity/01_labels_master.py
──────────────────────────────────
Q2 analysis A1 — label construction
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4; label decision 2026-10-29).

One tidy table, one row per platinum-treated patient (exact-match cohort, n=489),
every label with its provenance. Downstream scripts (A2–A5) read only this file.

Input:  label_validity/outputs/gate_patient_table.csv
        (built by 00_gate_pfi_coverage.py from the raw sources: TCGA-CDR
        Supplemental Table S1, cBioPortal ov_tcga_pub and
        ov_tcga_pan_can_atlas_2018; OS-threshold cohorts rebuilt with
        src.preprocessing and checked against fixes/phase1_provenance.md)
Output: label_validity/outputs/labels_master.csv
        label_validity/outputs/01_labels_summary.md

Labels (1 = non-responder / resistant, 0 = responder / sensitive, NA = undetermined)
──────────────────────────────────────────────────────────────────────────────────
  label_platinum   PRIMARY (Aaron, 2026-10-29). ov_tcga_pub PLATINUM_STATUS:
                   Resistant → 1, Sensitive → 0; Tooearly, Missing, absent → NA.
                   The TCGA 2011 wording of this definition is NOT yet quoted
                   verbatim (open item); the field is used as published.
  label_pfiplat6   SENSITIVITY. PFI from end of first-line platinum =
                   CDR PFI.time − max STOP_DATE of platinum rows with
                   REGIMEN_INDICATION == "Adjuvant" (both days from diagnosis).
                   short (PFI==1 and < 183 d, incl. negative) → 1; ≥ 183 d → 0;
                   PFI==0 and < 183 d → NA.
  label_response   PD or SD → 1; CR or PR → 0, from the first-course response
                   field. Source order fixed in advance: CDR
                   treatment_outcome_first_course, else ov_tcga_pub
                   PRIMARY_THERAPY_OUTCOME_SUCCESS, else pan-can
                   data_timeline_status.txt. (The three copies agree: pub vs CDR
                   365/365, pan-can vs CDR 141/142 — 00b_posthoc_summary.md.)
  label_os12/18/24 Existing OS-threshold labels exactly as in the v2 paper
                   (src.preprocessing.assign_response_label), defined only
                   inside the OS cohorts. 12m is supplement-only.
  pfi_time_d, pfi_event        CDR PFI.time (days from diagnosis), CDR PFI.
  pfi_from_platinum_d          as above, continuous.

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS / CHECKS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
A1 is a construction step. Its counts inside the OS cohorts were already
observed in the gate, so they are ASSERTIONS (the script stops if any fails),
not predictions:
  C1  cls_24m: label_platinum 39 resistant / 95 sensitive.
  C2  cls_24m: label_pfiplat6 51 short / 121 long.
  C3  cls_24m: label_response determinate = 179.
  C4  label_os18/os24 event counts 22 / 36 inside their cohorts.
  C5  pan-can-only response values used as fallback: ≤ 1 patient.
New (not yet seen) — predictions:
  P1  platinum ∩ RNA-seq has 150–200 patients with a determinate label_platinum
      (more than the 134 in cls_24m, because the OS cohorts drop patients
      censored before the threshold).
  P2  In platinum ∩ RNA-seq, resistant prevalence of label_platinum is 0.25–0.35.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "outputs"

RESP = {"Complete Remission/Response": 0, "Complete Response": 0,
        "Partial Remission/Response": 0, "Partial Response": 0,
        "Stable Disease": 1, "Progressive Disease": 1}


def main() -> None:
    g = pd.read_csv(OUT / "gate_patient_table.csv", index_col=0)
    g = g[g["in_platinum_exact"]].copy()
    assert len(g) == 489, len(g)

    m = pd.DataFrame(index=g.index)
    m["in_rnaseq"] = g["has_rnaseq"]
    m["in_cox432"] = g["in_cox432"]
    for t in (12, 18, 24):
        m[f"in_cls{t}"] = g[f"in_cls{t}"]
        m[f"label_os{t}"] = g[f"label_os{t}"]

    m["label_platinum"] = g["pub_platinum_status"].map({"Resistant": 1, "Sensitive": 0})
    m["src_platinum_status_raw"] = g["pub_platinum_status"].fillna("absent")

    m["label_pfiplat6"] = g["pfi_plat6_class"].map({"short": 1, "long": 0})
    m["pfi_from_platinum_d"] = g["pfi_from_platinum_d"]
    m["firstline_platinum_stop_d"] = g["firstline_platinum_stop_d"]
    m["pfi_time_d"] = g["cdr_PFI_time_d"]
    m["pfi_event"] = g["cdr_PFI"]

    resp, src = pd.Series(np.nan, index=g.index), pd.Series(pd.NA, index=g.index, dtype="string")
    for name, col in (("cdr", "cdr_treatment_outcome_first_course"),
                      ("ov_tcga_pub", "pub_ptos"), ("pancan_timeline", "pancan_ptos")):
        v = g[col].map(RESP)
        fill = resp.isna() & v.notna()
        resp[fill] = v[fill]
        src[fill] = name
    m["label_response"] = resp
    m["src_label_response"] = src
    m["response_category_cdr"] = g["cdr_treatment_outcome_first_course"]

    for c in [c for c in m.columns if c.startswith("label_")]:
        m[c] = m[c].astype("Int64")
    m.to_csv(OUT / "labels_master.csv")

    # ── Assertions C1–C5 ─────────────────────────────────────────────────
    c24 = m[m["in_cls24"]]
    checks = {
        "C1 cls24 platinum 1/0": ((c24.label_platinum == 1).sum(), (c24.label_platinum == 0).sum()) == (39, 95),
        "C2 cls24 pfiplat6 1/0": ((c24.label_pfiplat6 == 1).sum(), (c24.label_pfiplat6 == 0).sum()) == (51, 121),
        "C3 cls24 response n": c24.label_response.notna().sum() == 179,
        "C4 os events": (m.loc[m.in_cls18, "label_os18"].sum(), m.loc[m.in_cls24, "label_os24"].sum()) == (22, 36),
        "C5 pancan fallback ≤1": (m.src_label_response == "pancan_timeline").sum() <= 1,
    }
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(f"Construction checks FAILED: {failed}")

    # ── Summary ──────────────────────────────────────────────────────────
    labels = ["label_platinum", "label_pfiplat6", "label_response", "label_os12", "label_os18", "label_os24"]
    groups = {"platinum_489": pd.Series(True, index=m.index), "platinum_rnaseq": m.in_rnaseq,
              "cls_12m": m.in_cls12, "cls_18m": m.in_cls18, "cls_24m": m.in_cls24, "cox_432": m.in_cox432}
    rows = []
    for gname, mask in groups.items():
        s = m[mask]
        r = {"cohort": gname, "n": len(s)}
        for lab in labels:
            r[f"{lab}_1"] = int((s[lab] == 1).sum())
            r[f"{lab}_0"] = int((s[lab] == 0).sum())
        rows.append(r)
    tab = pd.DataFrame(rows).set_index("cohort").T

    pr = m[m.in_rnaseq]
    n_det = int(pr.label_platinum.notna().sum())
    prev = float((pr.label_platinum == 1).sum() / n_det) if n_det else float("nan")
    L = ["# A1 — labels_master.csv summary", "",
         "All construction checks C1–C5 passed (script stops otherwise).", "",
         "Counts per label (rows: `<label>_1` = non-responder/resistant, `_0` = responder/sensitive):", "",
         "```", tab.to_string(), "```", "",
         f"- P1 platinum ∩ RNA-seq with determinate label_platinum: {n_det} (predicted 150–200); "
         f"platinum ∩ RNA-seq n = {len(pr)}",
         f"- P2 resistant prevalence in that set: {prev:.3f} (predicted 0.25–0.35)",
         f"- label_response source: {m.src_label_response.value_counts(dropna=False).to_dict()}",
         f"- PLATINUM_STATUS raw values (platinum ∩ RNA-seq): {pr.src_platinum_status_raw.value_counts().to_dict()}",
         "", "Open item: TCGA 2011 wording of PLATINUM_STATUS not yet quoted verbatim."]
    (OUT / "01_labels_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
