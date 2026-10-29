#!/usr/bin/env python3
"""
label_validity/00b_gate_posthoc_response_sources.py
───────────────────────────────────────────────────
POST HOC — NOT PRE-REGISTERED. Written 2026-10-29 after 00_gate_pfi_coverage.py
had run and its output had been read.

Why: pre-registered G3 used the response field from the pan-can
data_timeline_status.txt (142 patients, 5 PD with a platinum label) and failed
on power, not on concordance. The cross-tabs showed the same field is
populated far more widely in two other copies of the TCGA clinical data:
  * ov_tcga_pub data_clinical_patient.txt  PRIMARY_THERAPY_OUTCOME_SUCCESS
  * TCGA-CDR treatment_outcome_first_course
This script quantifies coverage and agreement of the three copies and repeats
the G3 concordance with each. It does not replace the G3 verdict in
00_gate_summary.md; it is reported beside it.

Reads only label_validity/outputs/gate_patient_table.csv. No new inputs.
Output: label_validity/outputs/00b_posthoc_summary.md, 00b_posthoc_table.csv
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent / "outputs"

CANON = {  # map each source's categories to CR / PR / SD / PD
    "Complete Remission/Response": "CR", "Complete Response": "CR",
    "Partial Remission/Response": "PR", "Partial Response": "PR",
    "Stable Disease": "SD", "Progressive Disease": "PD",
}


def wilson(k, n):
    if n == 0:
        return "0/0"
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return f"{k}/{n} = {p:.3f} [{max(0, c - h):.3f}, {min(1, c + h):.3f}]"


def main() -> None:
    t = pd.read_csv(OUT / "gate_patient_table.csv", index_col=0)
    src = {"pancan": "pancan_ptos", "pub": "pub_ptos", "cdr": "cdr_treatment_outcome_first_course"}
    for k, c in src.items():
        t[f"resp_{k}"] = t[c].map(CANON)

    cohorts = {"platinum_exact_489": "in_platinum_exact", "cls_12m": "in_cls12",
               "cls_18m": "in_cls18", "cls_24m": "in_cls24", "cox_432": "in_cox432"}
    rows = []
    for name, col in cohorts.items():
        s = t[t[col]]
        r = {"cohort": name, "n": len(s)}
        for k in src:
            v = s[f"resp_{k}"]
            r[f"{k}_n"] = int(v.notna().sum())
            for cat in ("CR", "PR", "SD", "PD"):
                r[f"{k}_{cat}"] = int((v == cat).sum())
        r["any_n"] = int(s[[f"resp_{k}" for k in src]].notna().any(axis=1).sum())
        rows.append(r)
    cov = pd.DataFrame(rows)
    cov.to_csv(OUT / "00b_posthoc_table.csv", index=False)

    P = t[t["in_platinum_exact"]]
    L = ["# POST HOC — response-field sources (not pre-registered)\n",
         "Reads gate_patient_table.csv only. Categories mapped to CR/PR/SD/PD.\n",
         "## Coverage of the response field by source\n", "```", cov.to_string(index=False), "```\n",
         "## Agreement between copies (platinum cohort, patients with both)\n"]
    for a, b in (("pancan", "pub"), ("pancan", "cdr"), ("pub", "cdr")):
        m = P[f"resp_{a}"].notna() & P[f"resp_{b}"].notna()
        L.append(f"- {a} vs {b}: {wilson(int((P.loc[m, f'resp_{a}'] == P.loc[m, f'resp_{b}']).sum()), int(m.sum()))}")
    m = P["resp_pub"].notna() & P["resp_cdr"].notna() & (P["resp_pub"] != P["resp_cdr"])
    if m.any():
        L.append("\n  pub≠cdr disagreements:\n```\n"
                 + pd.crosstab(P.loc[m, "resp_pub"], P.loc[m, "resp_cdr"]).to_string() + "\n```")

    L.append("\n## G3 concordance repeated with each response source (platinum cohort)\n")
    ps = P["pub_platinum_status"]
    pp = P["pfi_plat6_class"]
    for k in src:
        r = P[f"resp_{k}"]
        L.append(f"### {k}")
        for lab, num, den in (
            ("P(Resistant | PD), pub status", (r == "PD") & (ps == "Resistant"), (r == "PD") & ps.isin(["Resistant", "Sensitive"])),
            ("P(short | PD), PFI-from-platinum", (r == "PD") & (pp == "short"), (r == "PD") & pp.isin(["short", "long"])),
            ("P(Sensitive | CR), pub status", (r == "CR") & (ps == "Sensitive"), (r == "CR") & ps.isin(["Resistant", "Sensitive"])),
            ("P(long | CR), PFI-from-platinum", (r == "CR") & (pp == "long"), (r == "CR") & pp.isin(["short", "long"])),
            ("P(Resistant | PD or SD), pub status", r.isin(["PD", "SD"]) & (ps == "Resistant"), r.isin(["PD", "SD"]) & ps.isin(["Resistant", "Sensitive"])),
        ):
            L.append(f"- {lab}: {wilson(int(num.sum()), int(den.sum()))}")
        L.append("")
        L.append("Cross-tab vs pub PLATINUM_STATUS:\n```\n"
                 + pd.crosstab(r.fillna("NA"), ps.fillna("absent")).to_string() + "\n```")
        L.append("Cross-tab vs PFI-from-first-line-platinum:\n```\n"
                 + pd.crosstab(r.fillna("NA"), pp.fillna("NA")).to_string() + "\n```\n")

    # PD patients classed long by PFI-from-platinum: what does CDR say?
    q = P[(P["resp_cdr"] == "PD") & (pp == "long")]
    L.append(f"## CDR-PD patients with PFI-from-platinum ≥183 d (n={len(q)})\n")
    L.append("```\n" + q[["pub_platinum_status", "cdr_PFI", "cdr_PFI_time_d",
                          "firstline_platinum_stop_d", "pfi_from_platinum_d"]].to_string() + "\n```")
    (OUT / "00b_posthoc_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
