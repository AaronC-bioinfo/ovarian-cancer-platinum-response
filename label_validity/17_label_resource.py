#!/usr/bin/env python3
"""
label_validity/17_label_resource.py
───────────────────────────────────
Builds the versioned, patient-level label resource released with the paper (S11 Table; Zenodo record).
Written 2026-10-29 ~22:45 ET, after A15/A15b/A16, in response to point 6 of the external review of manuscript
v5 (make the label table the main deliverable). Descriptive assembly only: no new analysis, no predictions.
Every column is copied from an existing output; nothing is recomputed except the counts table (event types missing in TCGA-CDR are written as type_not_recorded).

Inputs (label_validity/outputs/): labels_full.csv, labels_master.csv (pfi_from_platinum_d),
  a15b_provenance.csv (provenance class, event source and flags, header definition of "clean"),
  a15b_label_combined_strict.csv (strict combined label, primary; 355 determinate),
  a15_label_combined_strict.csv (strict label as first run, before the near-threshold correction; 367).
Outputs → label_validity/outputs/label_resource_v1.csv, label_resource_v1_dictionary.csv,
          label_resource_v1_counts.csv
Run (from the repo root): python label_validity/17_label_resource.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

VERSION = "1.0 (2026-10-29)"
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    f = pd.read_csv(OUT / "labels_full.csv", index_col=0)
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    pv = pd.read_csv(OUT / "a15b_provenance.csv", index_col=0)
    strict = pd.read_csv(OUT / "a15b_label_combined_strict.csv", index_col=0)["label_combined_strict"]
    strict_asrun = pd.read_csv(OUT / "a15_label_combined_strict.csv", index_col=0)["label_combined_strict"]
    assert len(f) == 489 and f.index.equals(m.index)
    r = pd.DataFrame(index=f.index)
    r["in_rnaseq"] = f.in_rnaseq
    r["label_combined_strict"] = strict.reindex(f.index)
    r["label_combined_broad"] = f.label_hybrid
    r["label_platinum"] = f.label_platinum
    r["src_platinum_status_raw"] = f.src_platinum_status_raw
    r["label_pfiplat6"] = f.label_pfiplat6
    r["pfi_from_platinum_d"] = m.pfi_from_platinum_d
    for c in ["group", "provenance_class", "event_source", "redacted", "adj_platinum_stop_missing",
              "later_line_before_event", "near_threshold", "disagreement"]:
        r[c] = pv[c].reindex(f.index)
    r["label_response"] = f.label_response
    r["label_os18_all"] = f.label_os18_all
    r["label_os24_all"] = f.label_os24_all
    r["event_source"] = r["event_source"].replace("recorded_new_tumour_event:nan", "recorded_new_tumour_event:type_not_recorded")
    r["label_combined_strict_asrun"] = strict_asrun.reindex(f.index)
    r.insert(0, "resource_version", VERSION)
    r.to_csv(OUT / "label_resource_v1.csv")

    D = [
        ("PATIENT_ID", "TCGA patient barcode; the 489 platinum-treated patients (carboplatin or cisplatin in the PanCancer Atlas treatment timeline)."),
        ("resource_version", "Version of this table."),
        ("in_rnaseq", "Patient has PanCancer Atlas RNA-seq (RSEM) data (251 patients)."),
        ("label_combined_strict", "Provenance-filtered candidate extension of platinum status (preferred of the two combined labels under the pre-specified A15 rule; added calls not verified as accurate). 1 resistant, 0 sensitive, empty undetermined. TCGA 2011 platinum status where determinate; otherwise label_pfiplat6 only when provenance_class is clean_resistant or clean_sensitive, i.e. unflagged (A15 header definition; script 15b)."),
        ("label_combined_broad", "Sensitivity-analysis label: platinum status where determinate, otherwise label_pfiplat6 regardless of provenance."),
        ("label_platinum", "TCGA 2011 published platinum status (ov_tcga_pub), unchanged: 1 Resistant, 0 Sensitive; Tooearly, missing or absent = empty."),
        ("src_platinum_status_raw", "Raw platinum-status value in the 2011 release."),
        ("label_pfiplat6", "Platinum-free interval re-derived from TCGA-CDR PFI.time minus the stop date of the last adjuvant platinum regimen: 1 if progression < 183 days after end of platinum (including negative intervals), 0 if >= 183 days, empty if censored earlier."),
        ("pfi_from_platinum_d", "Re-derived platinum-free interval in days (negative = progression recorded before the end of platinum)."),
        ("group", "For patients with label_pfiplat6 determinate: overlap_with_platinum_status or added_by_reconstruction."),
        ("provenance_class", "clean_resistant (recorded new tumour event, no flag); clean_sensitive (interval >= 183 days, no flag); flagged (any flag, or a resistant call from a death counted as progression); negative_interval."),
        ("event_source", "For resistant calls: recorded_new_tumour_event:<type> (new_tumor_event_dx_days_to equals PFI.time +/- 1 day) or death_counted_as_progression; type_not_recorded = event recorded without a type."),
        ("redacted", "Flag: TCGA-CDR record marked Redacted."),
        ("adj_platinum_stop_missing", "Flag: an adjuvant platinum row lacks a STOP_DATE."),
        ("later_line_before_event", "Flag: a later-line (Progression/Recurrence) regimen started before the recorded event (sensitive: before day 183 after platinum)."),
        ("near_threshold", "Flag: interval within 150-215 days of the end of platinum."),
        ("disagreement", "label_platinum and label_pfiplat6 both determinate and different (4 patients)."),
        ("label_response", "First-course response: 1 stable or progressive disease, 0 complete or partial response (TCGA-CDR, then ov_tcga_pub, then timeline)."),
        ("label_os18_all", "1 death before 18 months from diagnosis, 0 survival beyond; empty if censored earlier. A candidate survival surrogate, not a platinum-response label."),
        ("label_os24_all", "As label_os18_all, at 24 months."),
        ("label_combined_strict_asrun", "Strict label as first run (A15, before the correction that flags near-threshold intervals); kept for transparency, not recommended."),
    ]
    pd.DataFrame(D, columns=["column", "definition"]).to_csv(OUT / "label_resource_v1_dictionary.csv", index=False)

    rows = []
    for c in ["label_combined_strict", "label_combined_broad", "label_platinum", "label_pfiplat6", "label_response",
              "label_os18_all", "label_os24_all", "label_combined_strict_asrun"]:
        for sub, d in [("platinum_cohort", r), ("with_rnaseq", r[r.in_rnaseq])]:
            rows.append(dict(label=c, subset=sub, determinate=int(d[c].notna().sum()), n1=int((d[c] == 1).sum()),
                             n0=int((d[c] == 0).sum())))
    ct = pd.DataFrame(rows); ct.to_csv(OUT / "label_resource_v1_counts.csv", index=False)
    print(ct.to_string(index=False))


if __name__ == "__main__":
    main()
