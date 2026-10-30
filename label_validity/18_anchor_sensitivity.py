#!/usr/bin/env python3
"""
label_validity/18_anchor_sensitivity.py
───────────────────────────────────────
A18 — sensitivity of the re-derived platinum-free-interval label (label_pfiplat6) to the treatment anchor.
Post hoc. Written 2026-10-29 23:55–23:57 ET, BEFORE this script was run, in response to a fourth review
(point 3: the anchor "stop date of the last platinum regimen marked adjuvant" does not by itself establish the
end of first-line platinum). Known before writing: the primary anchor is the maximum STOP_DATE of platinum rows
with REGIMEN_INDICATION == "Adjuvant"; among the 389 patients with label_pfiplat6 determinate, 329 have 1 such
row, 55 have 2 and 5 have 3; platinum-row indications are Adjuvant 544, Recurrence 150, Progression 116,
"Other, Specify In Notes" 14, missing 11 (no Neoadjuvant category). Not seen: any label under another anchor.

Platinum rows: AGENT contains "PLATIN" (carboplatin, cisplatin; as in the cohort definition). Days from diagnosis.
Anchors:
  A0  primary: max STOP_DATE of Adjuvant platinum rows (must reproduce labels_master pfi_from_platinum_d exactly).
  A1  earliest end of adjuvant platinum: min STOP_DATE of Adjuvant platinum rows.
  A2  end of the first platinum regimen regardless of indication: among platinum rows with the earliest
      START_DATE, the max STOP_DATE.
  A3  end of adjuvant platinum before any later-line treatment: max STOP_DATE of Adjuvant platinum rows that
      START before the first row of any agent with REGIMEN_INDICATION Recurrence or Progression (A0 if none).
Label under each anchor (same rule as label_pfiplat6): interval = CDR PFI.time − anchor; 1 if PFI event and
interval < 183 days (negative included); 0 if interval ≥ 183; otherwise undetermined.
Also reported (descriptive): patients with > 1 Adjuvant platinum row; overlapping Adjuvant platinum rows;
Adjuvant platinum rows with a missing STOP_DATE; ties at the max STOP_DATE; Adjuvant platinum rows starting
after the first Recurrence/Progression row; platinum rows with indication Other or missing.

DECISION RULE (for the manuscript)
  * For each alternative anchor, report determinate n, calls changed relative to A0 (among patients determinate
    under both), and Cohen's κ with A0 and with TCGA platinum status (patients determinate under both).
  * If any alternative changes more than 5% of the calls determinate under both, the manuscript states in
    Results that the anchor is a material source of uncertainty and reports that alternative; otherwise the
    results are reported in Methods in one sentence with details in S1 Text / S11 Table.
  No predictions are made.

Run (from the repo root): python label_validity/18_anchor_sensitivity.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a18_anchor_labels.csv, a18_anchor_summary.csv, a18_anchor_counts.csv,
          18_anchor_sensitivity_summary.md
"""
from __future__ import annotations

import argparse
import platform
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"


def kappa(a, b):
    a, b = np.asarray(a, int), np.asarray(b, int)
    po = (a == b).mean(); pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    dr = Path(ap.parse_args().data_root)
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    ids = m.index
    tr = pd.read_csv(dr / "ov_tcga_pan_can_atlas_2018" / "data_timeline_treatment.txt", sep="\t")
    tr = tr[tr.PATIENT_ID.isin(ids)].copy()
    tr["START_DATE"] = pd.to_numeric(tr.START_DATE, errors="coerce"); tr["STOP_DATE"] = pd.to_numeric(tr.STOP_DATE, errors="coerce")
    pl = tr[tr.AGENT.astype(str).str.upper().str.contains("PLATIN")]
    adj = pl[pl.REGIMEN_INDICATION == "Adjuvant"]
    later = tr[tr.REGIMEN_INDICATION.isin(["Recurrence", "Progression"])]
    first_later = later.groupby("PATIENT_ID").START_DATE.min()

    A = pd.DataFrame(index=ids)
    A["A0"] = adj.groupby("PATIENT_ID").STOP_DATE.max()
    A["A1"] = adj.groupby("PATIENT_ID").STOP_DATE.min()
    fs = pl.groupby("PATIENT_ID").START_DATE.transform("min")
    A["A2"] = pl[pl.START_DATE == fs].groupby("PATIENT_ID").STOP_DATE.max()
    adj2 = adj.join(first_later.rename("fl"), on="PATIENT_ID")
    pre = adj2[adj2.fl.isna() | (adj2.START_DATE < adj2.fl)]
    A["A3"] = pre.groupby("PATIENT_ID").STOP_DATE.max()
    A["A3"] = A["A3"].fillna(A["A0"].where(~A.index.isin(first_later.index)))

    pfi_t, pfi_e = m.pfi_time_d, m.pfi_event
    lab = pd.DataFrame(index=ids)
    for k in ["A0", "A1", "A2", "A3"]:
        iv = pfi_t - A[k]
        lab[f"interval_{k}"] = iv
        lab[f"label_{k}"] = np.where((pfi_e == 1) & (iv < 183), 1.0, np.where(iv >= 183, 0.0, np.nan))
    lab["label_platinum"] = m.label_platinum
    # reproduction check
    rep_iv = np.allclose(lab.interval_A0.dropna(), m.pfi_from_platinum_d.reindex(lab.interval_A0.dropna().index), equal_nan=False) and lab.interval_A0.notna().sum() == m.pfi_from_platinum_d.notna().sum()
    rep_lab = lab.label_A0.fillna(-1).equals(m.label_pfiplat6.fillna(-1))
    lab.to_csv(OUT / "a18_anchor_labels.csv")

    rows = []
    for k in ["A0", "A1", "A2", "A3"]:
        x = lab[f"label_{k}"]
        both = lab[["label_A0", f"label_{k}"]].dropna()
        bp = lab[["label_platinum", f"label_{k}"]].dropna()
        rows.append(dict(anchor=k, determinate=int(x.notna().sum()), resistant=int((x == 1).sum()),
                         anchor_differs_from_A0=int(((A[k] != A["A0"]) & A[k].notna() & A["A0"].notna()).sum()),
                         n_both_A0=len(both), changed_vs_A0=int((both.iloc[:, 0] != both.iloc[:, 1]).sum()),
                         pct_changed=100 * float((both.iloc[:, 0] != both.iloc[:, 1]).mean()),
                         kappa_A0=kappa(both.iloc[:, 0], both.iloc[:, 1]), n_both_platinum=len(bp),
                         agree_platinum=int((bp.iloc[:, 0] == bp.iloc[:, 1]).sum()), kappa_platinum=kappa(bp.iloc[:, 0], bp.iloc[:, 1])))
    sm = pd.DataFrame(rows); sm.to_csv(OUT / "a18_anchor_summary.csv", index=False)

    det = m.index[m.label_pfiplat6.notna()]
    a_det = adj[adj.PATIENT_ID.isin(det)]
    def overl(g):
        g = g.sort_values("START_DATE"); s, e = g.START_DATE.to_numpy(), g.STOP_DATE.to_numpy()
        return any(s[i + 1] <= e[i] for i in range(len(g) - 1) if not np.isnan(e[i]))
    nrows = a_det.groupby("PATIENT_ID").size()
    ties = a_det.groupby("PATIENT_ID").STOP_DATE.apply(lambda s: int((s == s.max()).sum()) > 1 and s.notna().sum() > 1)
    a_late = adj2[adj2.fl.notna() & (adj2.START_DATE >= adj2.fl)]
    C = [("patients with label_pfiplat6 determinate", len(det)),
         ("  with >1 Adjuvant platinum row", int((nrows > 1).sum())),
         ("  with overlapping Adjuvant platinum rows", int(a_det.groupby("PATIENT_ID").apply(overl).sum())),
         ("  with >1 Adjuvant platinum row sharing the max STOP_DATE", int(ties.sum())),
         ("  with an Adjuvant platinum row missing STOP_DATE", int(a_det.STOP_DATE.isna().groupby(a_det.PATIENT_ID).any().sum())),
         ("  with an Adjuvant platinum row starting on/after the first Recurrence/Progression row", int(a_late[a_late.PATIENT_ID.isin(det)].PATIENT_ID.nunique())),
         ("  with any platinum row of indication Other or missing", int(pl[pl.PATIENT_ID.isin(det) & ~pl.REGIMEN_INDICATION.isin(["Adjuvant", "Recurrence", "Progression"])].PATIENT_ID.nunique())),
         ("cohort patients without any Adjuvant platinum row", int((~ids.isin(adj.PATIENT_ID)).sum()))]
    ct = pd.DataFrame(C, columns=["item", "n"]); ct.to_csv(OUT / "a18_anchor_counts.csv", index=False)

    flag = [r.anchor for r in sm.itertuples() if r.anchor != "A0" and r.pct_changed > 5]
    L = ["# A18 — Sensitivity of the re-derived interval label to the treatment anchor", "",
         f"Python {platform.python_version()}; pandas {pd.__version__}; numpy {np.__version__}", "",
         f"Reproduction of labels_master (A0): intervals identical {rep_iv}; labels identical {rep_lab}.", "",
         "```", sm.round(3).to_string(index=False), "```", "", "```", ct.to_string(index=False), "```", "",
         "Decision rule — alternatives changing > 5% of calls: " + (", ".join(flag) if flag else "none"), ""]
    (OUT / "18_anchor_sensitivity_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
