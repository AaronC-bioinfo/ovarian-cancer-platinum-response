#!/usr/bin/env python3
"""
label_validity/21_event_type_sensitivity.py
───────────────────────────────────────────
A21 — sensitivity of the re-derived interval label to the type of event that dates each resistant call.
Post hoc. Written 2026-10-30 00:29–00:30 ET, BEFORE this script was run, in response to a fourth review (point 4:
the TCGA-CDR progression-free interval counts deaths with tumour and new tumour events of any type; distinguish
documented recurrence/progression from other events in the analyses supporting interpretation). Known before
writing: of the 115 resistant re-derived calls, 90 are dated by a recorded recurrence, 15 by a recorded progression,
4 by a new tumour event of unrecorded type and 6 by a death counted as progression (a15b_resistant_event_source.csv).
Not seen: any result with the restricted label.

Restricted label (label_pfiplat6_rec): label_pfiplat6, but resistant calls not dated by a recorded recurrence or
progression (death-dated or unrecorded type; 10 patients) are set to undetermined. Sensitive calls are unchanged.
Recomputed with the restricted label, and compared with the same quantity for label_pfiplat6:
  Q1  coverage and number resistant;
  Q2  Cohen's κ with TCGA platinum status (patients with both);
  Q3  sensitivity and PPV of OS < 18 / 24 months against the broad combined reference built with the label
      (platinum status where determinate, otherwise the re-derived label) — as A15 P3 (broad: 0.27/0.78, 0.44/0.73);
  Q4  conditional odds ratios (scipy odds_ratio, kind="conditional", exact 95% CI) for BRCA1/2 carriers (A8 primary
      definition, sequenced patients) and CCNE1 amplification (GISTIC 2), as in A8 (Table 3: 0.37 (0.14–0.87);
      1.76 (0.98–3.15) for label_pfiplat6; reproduced here as a check).
DECISION RULE (for the manuscript)
  * If any of κ, sensitivity or PPV changes by more than 0.05, or any odds-ratio 95% CI moves to the other side of 1,
    the manuscript reports the restricted-label results in Results; otherwise in one sentence, with the table in S11.
  No predictions are made.
Run (from the repo root): python label_validity/21_event_type_sensitivity.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a21_event_type.csv, 21_event_type_sensitivity_summary.md
"""
from __future__ import annotations

import argparse
import math
import platform
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats.contingency import odds_ratio

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"


def kappa(a, b):
    a, b = np.asarray(a, int), np.asarray(b, int)
    po = (a == b).mean(); pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return (po - pe) / (1 - pe)


def wilson(k, n):
    z = 1.959963984540054; p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, c - h, c + h


def cor(x, y):
    d = pd.concat([x, y], axis=1).dropna(); a, l = d.iloc[:, 0], d.iloc[:, 1]
    t = [[int(((a == 1) & (l == 1)).sum()), int(((a == 1) & (l == 0)).sum())], [int(((a == 0) & (l == 1)).sum()), int(((a == 0) & (l == 0)).sum())]]
    r = odds_ratio(t, kind="conditional"); ci = r.confidence_interval(0.95)
    return float(r.statistic), float(ci.low), float(ci.high), len(d)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
    dr = Path(ap.parse_args().data_root); pub = dr / "ov_tcga_pub" / "ov_tcga_pub"
    f = pd.read_csv(OUT / "labels_full.csv", index_col=0)
    pv = pd.read_csv(OUT / "a15b_provenance.csv", index_col=0).reindex(f.index)
    rec = pv.event_source.astype(str).isin(["recorded_new_tumour_event:Recurrence", "recorded_new_tumour_event:Progression of Disease"])
    L0 = f.label_pfiplat6
    L1 = L0.where(~((L0 == 1) & ~rec))
    car = pd.read_csv(OUT / "a8_carriers.csv"); car = car[car.trunc.astype(bool) & car.Mutation_Status.isin(["Germline", "Somatic"])]
    seq = {x[:12] for x in (pub / "case_lists" / "cases_sequenced.txt").read_text(encoding="utf-8").split("case_list_ids:")[1].split()}
    brca = pd.Series(np.where(f.index.isin(seq), f.index.isin(set(car.pid)).astype(float), np.nan), index=f.index)
    cna = pd.read_csv(pub / "data_cna.txt", sep="\t")
    cc = cna[cna.Hugo_Symbol == "CCNE1"].iloc[0].drop(["Hugo_Symbol", "Entrez_Gene_Id"])
    cc.index = cc.index.str[:12]; cc = pd.to_numeric(cc[~cc.index.duplicated()], errors="coerce")
    ccne = (cc.reindex(f.index) == 2).astype(float).where(cc.reindex(f.index).notna())

    rows = []
    for nm, L in [("label_pfiplat6", L0), ("label_pfiplat6_rec", L1)]:
        r = dict(label=nm, determinate=int(L.notna().sum()), resistant=int((L == 1).sum()))
        b = pd.concat([f.label_platinum, L], axis=1).dropna(); r["n_with_platinum"] = len(b); r["kappa_platinum"] = kappa(b.iloc[:, 0], b.iloc[:, 1])
        ref = f.label_platinum.where(f.label_platinum.notna(), L)
        for t in (18, 24):
            s = pd.concat([ref, f[f"label_os{t}_all"]], axis=1).dropna(); rr, aa = s.iloc[:, 0], s.iloc[:, 1]
            tp = int(((aa == 1) & (rr == 1)).sum()); fn = int(((aa == 0) & (rr == 1)).sum()); fp = int(((aa == 1) & (rr == 0)).sum())
            se = wilson(tp, tp + fn); pp = wilson(tp, tp + fp)
            r.update({f"os{t}_n": len(s), f"os{t}_sens": se[0], f"os{t}_sens_lo": se[1], f"os{t}_sens_hi": se[2], f"os{t}_ppv": pp[0], f"os{t}_ppv_lo": pp[1], f"os{t}_ppv_hi": pp[2]})
        for g, x in [("brca", brca), ("ccne1", ccne)]:
            o, lo, hi, n = cor(x, L); r.update({f"{g}_or": o, f"{g}_lo": lo, f"{g}_hi": hi, f"{g}_n": n})
        rows.append(r)
    res = pd.DataFrame(rows).set_index("label").T
    res.to_csv(OUT / "a21_event_type.csv")
    a, b = res["label_pfiplat6"], res["label_pfiplat6_rec"]
    big = [k for k in ["kappa_platinum", "os18_sens", "os18_ppv", "os24_sens", "os24_ppv"] if abs(float(a[k]) - float(b[k])) > 0.05]
    side = lambda lo, hi: "above" if lo > 1 else ("below" if hi < 1 else "spans")
    flips = [g for g in ["brca", "ccne1"] if side(float(a[f"{g}_lo"]), float(a[f"{g}_hi"])) != side(float(b[f"{g}_lo"]), float(b[f"{g}_hi"]))]
    L = ["# A21 — Event-type sensitivity of the re-derived interval label", "", f"Python {platform.python_version()}; pandas {pd.__version__}", "",
         f"Patients whose resistant call is set aside: {int(((L0 == 1) & ~rec).sum())}", "", "```", res.to_string(), "```", "",
         f"Decision rule — changes > 0.05: {big or 'none'}; odds-ratio CIs changing side of 1: {flips or 'none'}", ""]
    (OUT / "21_event_type_sensitivity_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
