#!/usr/bin/env python3
"""
label_validity/15b_reconstruction_provenance_specfix.py
───────────────────────────────────────────────────────
A15b — correction run of A15 (15_reconstruction_provenance.py, committed d349b2b) so that the code matches
A15's pre-registered definition.

Written 2026-10-29 ~22:35 ET, AFTER the A15 run (22:00 ET) and after its results were seen. While filling the
A15 scorecard we found that A15's header lists "interval within 150–215 days (near the 183-day cut-off)" among
the flags and defines "clean" as "no flag", but the code left near_threshold out of any_flag. Aaron decided
(2026-10-29) that the manuscript follows the header's definition. This script is A15 with exactly one change to
the analysis: near_threshold enters any_flag. Outputs carry the prefix a15b_ so A15's outputs are kept unchanged.
No new predictions are made; A15's P1–P4 and decision rule are scored in 15_reconstruction_provenance_summary.md.

Run (from the repo root; no model fitting): python label_validity/15b_reconstruction_provenance_specfix.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a15b_provenance.csv, a15b_class_by_group.csv, a15b_resistant_event_source.csv,
          a15b_os_test_strict.csv, a15b_label_combined_strict.csv, 15b_reconstruction_provenance_specfix_summary.md
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"


def wilson(k, n):
    if n == 0:
        return (np.nan,) * 3
    z = 1.959963984540054; p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()
    dr, W = Path(args.data_root), Path(args.out)
    f = pd.read_csv(OUT / "labels_full.csv", index_col=0)
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    df = f.join(m[["pfi_from_platinum_d", "firstline_platinum_stop_d", "pfi_time_d", "pfi_event"]])
    cdr = pd.read_excel(dr / "TCGA-CDR-SupplementalTableS1.xlsx", sheet_name="TCGA-CDR")
    cdr = cdr[cdr["type"] == "OV"].set_index("bcr_patient_barcode").reindex(df.index)
    num = lambda s: pd.to_numeric(s, errors="coerce")
    df["nte_type"] = cdr["new_tumor_event_type"]
    df["nte_d"] = num(cdr["new_tumor_event_dx_days_to"])
    df["death_d"] = num(cdr["death_days_to"])
    df["redacted"] = cdr["Redaction"].eq("Redacted")
    tr = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_timeline_treatment.txt", sep="\t")
    tr = tr[tr.PATIENT_ID.isin(df.index)]
    is_plat = tr["AGENT"].astype(str).str.upper().str.contains("PLATIN")
    adj = tr[is_plat & (tr["REGIMEN_INDICATION"] == "Adjuvant")]
    df["adj_platinum_rows"] = adj.groupby("PATIENT_ID").size().reindex(df.index).fillna(0).astype(int)
    df["adj_platinum_stop_missing"] = adj.STOP_DATE.isna().groupby(adj.PATIENT_ID).any().reindex(df.index).fillna(False)
    later = tr[tr["REGIMEN_INDICATION"].isin(["Progression", "Recurrence"])]
    df["first_later_line_start_d"] = num(later.groupby("PATIENT_ID").START_DATE.min()).reindex(df.index)

    d = df[df.label_pfiplat6.notna()].copy()
    res = d.label_pfiplat6 == 1
    d["event_source"] = pd.NA
    nte_match = (d.nte_d - d.pfi_time_d).abs() <= 1
    death_match = (d.death_d - d.pfi_time_d).abs() <= 1
    d.loc[res & nte_match, "event_source"] = "recorded_new_tumour_event:" + d.loc[res & nte_match, "nte_type"].astype(str)
    d.loc[res & ~nte_match & death_match, "event_source"] = "death_counted_as_progression"
    d.loc[res & d.event_source.isna(), "event_source"] = "unclear"
    d["negative_interval"] = d.pfi_from_platinum_d < 0
    end_plat = d.firstline_platinum_stop_d
    limit = np.where(res, d.pfi_time_d, end_plat + 183)
    d["later_line_before_event"] = d.first_later_line_start_d.notna() & (d.first_later_line_start_d < limit) & (d.first_later_line_start_d > end_plat)
    d["near_threshold"] = d.pfi_from_platinum_d.between(150, 215)
    d["any_flag"] = d.redacted | d.adj_platinum_stop_missing | d.later_line_before_event | d.near_threshold  # A15b: the only change (per A15's header)
    cls = np.where(d.negative_interval, "negative_interval",
          np.where(d.any_flag | (res & ~d.event_source.astype(str).str.startswith("recorded")), "flagged",
          np.where(res, "clean_resistant", "clean_sensitive")))
    d["provenance_class"] = cls
    d["group"] = np.where(d.label_platinum.notna(), "overlap_with_platinum_status", "added_by_reconstruction")
    d["disagreement"] = d.label_platinum.notna() & (d.label_platinum != d.label_pfiplat6)
    cols = ["group", "label_platinum", "label_pfiplat6", "pfi_from_platinum_d", "event_source", "provenance_class",
            "redacted", "adj_platinum_rows", "adj_platinum_stop_missing", "later_line_before_event", "near_threshold",
            "disagreement", "src_platinum_status_raw"]
    d[cols].to_csv(W / "a15b_provenance.csv")

    # strict combined label
    strict = df.label_platinum.copy()
    ok = d.index[(d.label_platinum.isna()) & d.provenance_class.isin(["clean_resistant", "clean_sensitive"])]
    strict.loc[ok] = d.loc[ok, "label_pfiplat6"]
    df["label_combined_strict"] = strict

    # summaries
    added = d[d.group == "added_by_reconstruction"]
    add_res = added[added.label_pfiplat6 == 1]
    t1 = pd.crosstab([d.group, d.label_pfiplat6], d.provenance_class, margins=True)
    t2 = pd.crosstab(d.loc[d.label_pfiplat6 == 1, "group"], d.loc[d.label_pfiplat6 == 1, "event_source"], margins=True)
    t1.to_csv(W / "a15b_class_by_group.csv")
    t2.to_csv(W / "a15b_resistant_event_source.csv")
    rows = []
    for ref in ["label_hybrid", "label_combined_strict"]:
        for t in ["label_os18_all", "label_os24_all"]:
            s = df[[ref, t]].dropna(); r, a = s[ref].astype(int), s[t].astype(int)
            tp, fn, fp, tn = int(((a == 1) & (r == 1)).sum()), int(((a == 0) & (r == 1)).sum()), int(((a == 1) & (r == 0)).sum()), int(((a == 0) & (r == 0)).sum())
            se = wilson(tp, tp + fn); pp = wilson(tp, tp + fp)
            rows.append(dict(reference=ref, os_label=t, n=len(s), tp=tp, fn=fn, fp=fp, tn=tn, sensitivity=se[0], sens_lo=se[1], sens_hi=se[2],
                             ppv=pp[0], ppv_lo=pp[1], ppv_hi=pp[2]))
    os_t = pd.DataFrame(rows); os_t.to_csv(W / "a15b_os_test_strict.csv", index=False)
    df[["label_combined_strict"]].to_csv(W / "a15b_label_combined_strict.csv")

    rec = add_res.event_source.astype(str).str.startswith("recorded").sum()
    L = ["# A15b — Provenance of the re-derived platinum-free-interval label (correction run: near-threshold intervals flagged, per A15's header)", "",
         f"Re-derived interval determinate: {len(d)}; overlap with platinum status: {int((d.group == 'overlap_with_platinum_status').sum())}; "
         f"added by reconstruction: {len(added)} ({int((added.label_pfiplat6 == 1).sum())} resistant).", "",
         "## Provenance class by group and label", "", "```", t1.to_string(), "```", "",
         "## Event source of resistant calls", "", "```", t2.to_string(), "```", "",
         f"Added resistant calls backed by a recorded new tumour event: {rec}/{len(add_res)}.",
         f"Added patients classed clean: {int(added.provenance_class.isin(['clean_resistant', 'clean_sensitive']).sum())}/{len(added)}.",
         f"Strict combined label: {int(strict.notna().sum())} determinate ({int((strict == 1).sum())} resistant / {int((strict == 0).sum())} sensitive).", "",
         "## The disagreements between platinum status and the re-derived interval", "", "```",
         d.loc[d.disagreement, cols].to_string(), "```", "",
         "## OS thresholds as tests: broad vs strict combined reference", ""]
    for r in os_t.itertuples():
        L.append(f"- {r.os_label} vs {r.reference} (n {r.n}): sensitivity {r.tp}/{r.tp + r.fn} = {r.sensitivity:.2f} "
                 f"[{r.sens_lo:.2f}, {r.sens_hi:.2f}]; PPV {r.tp}/{r.tp + r.fp} = {r.ppv:.2f} [{r.ppv_lo:.2f}, {r.ppv_hi:.2f}]")
    L += ["", "## Note", "", "Correction run; no new predictions. A15's predictions and decision rule are scored in 15_reconstruction_provenance_summary.md.", ""]
    (W / "15b_reconstruction_provenance_specfix_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
