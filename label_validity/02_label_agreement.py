#!/usr/bin/env python3
"""
label_validity/02_label_agreement.py
────────────────────────────────────
Q2 analysis A2 — how the response labels relate to each other
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A2).

Reads only label_validity/outputs/labels_master.csv (A1).

Analyses (fixed before running)
  1. Every pair of labels among: label_platinum (primary), label_pfiplat6,
     label_response, label_os18, label_os24. label_os12 pairs go to the
     supplement table only. Population: platinum-treated patients with both
     labels determinate (OS labels exist only inside their OS cohorts, so any
     pair with an OS label is automatically within platinum ∩ RNA-seq).
     Output per pair: 2×2 table, n, raw agreement, Cohen's κ with 95% CI
     (2,000-resample percentile bootstrap, seed 42, resampling patients).
  2. OS-threshold labels as "tests" against each platinum/response label as
     reference: sensitivity = P(OS label = 1 | reference = 1),
     specificity = P(OS label = 0 | reference = 0), Wilson 95% CIs.
  Repeated restricted to platinum ∩ RNA-seq as a sensitivity check (only pairs
  without an OS label change).
  Descriptive estimates with CIs only; no hypothesis tests, so no multiplicity
  correction applies to A2.

Outputs → label_validity/outputs/
  a2_pairwise_agreement.csv, a2_os_sens_spec.csv, 02_agreement_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already seen (disclosed, so partly not predictions): gate G3 gave OS18 and OS24
sensitivity of 11/49 and 17/49 against the COMBINED platinum label (pub status,
else PFI-from-platinum); gate G2 gave pub status vs PFI-from-platinum raw
agreement 268/272; post hoc 00b gave P(Resistant | PD) 15/18 and
P(Sensitive | CR) 156/191. No κ has been computed; the pure label_platinum
sensitivities have not been computed.

  P1  κ(OS18, platinum) < 0.40 and κ(OS24, platinum) < 0.40.
  P2  κ(OS18, pfiplat6) < 0.40 and κ(OS24, pfiplat6) < 0.40.
  P3  Sensitivity of OS18 and of OS24 for label_platinum = 1 is < 0.50.
  P4  Specificity of OS18 and OS24 for label_platinum = 0 is > 0.85.
  P5  κ(platinum, pfiplat6) ≥ 0.80 (check; agreement already seen).
  P6  κ(platinum, response) between 0.30 and 0.60.

DECISION RULE (for the paper's claim "OS-threshold labels do not measure
platinum response in TCGA-OV"):
  Supported if κ(OS18, platinum) and κ(OS24, platinum) both have point
  estimate < 0.40 AND upper 95% bound < 0.60.
  Not supported if either point estimate ≥ 0.60.
  Otherwise: "partial agreement", reported as such.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent / "outputs"
SEED, B = 42, 2000
MAIN = ["label_platinum", "label_pfiplat6", "label_response", "label_os18", "label_os24"]
SUPP = ["label_os12"]
REFS = ["label_platinum", "label_pfiplat6", "label_response"]
OS = ["label_os12", "label_os18", "label_os24"]


def kappa(a: np.ndarray, b: np.ndarray) -> float:
    n = len(a)
    po = np.mean(a == b)
    pa1, pb1 = a.mean(), b.mean()
    pe = pa1 * pb1 + (1 - pa1) * (1 - pb1)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def boot_kappa(a, b, rng) -> tuple[float, float]:
    n = len(a)
    ks = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        k = kappa(a[i], b[i])
        if not math.isnan(k):
            ks.append(k)
    return float(np.percentile(ks, 2.5)), float(np.percentile(ks, 97.5))


def wilson(k: int, n: int) -> tuple[float, float, float]:
    if n == 0:
        return (float("nan"),) * 3
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def pair_rows(m: pd.DataFrame, labels: list[str], pop: str, rng) -> list[dict]:
    rows = []
    for x, y in itertools.combinations(labels, 2):
        s = m[[x, y]].dropna()
        a, b = s[x].to_numpy(int), s[y].to_numpy(int)
        if len(s) == 0:
            continue
        lo, hi = boot_kappa(a, b, rng)
        rows.append({"population": pop, "label_a": x, "label_b": y, "n": len(s),
                     "a1b1": int(((a == 1) & (b == 1)).sum()), "a1b0": int(((a == 1) & (b == 0)).sum()),
                     "a0b1": int(((a == 0) & (b == 1)).sum()), "a0b0": int(((a == 0) & (b == 0)).sum()),
                     "agreement": float(np.mean(a == b)), "kappa": kappa(a, b),
                     "kappa_lo": lo, "kappa_hi": hi})
    return rows


def main() -> None:
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    rng = np.random.default_rng(SEED)

    rows = pair_rows(m, MAIN, "platinum_489", rng)
    rows += [r | {"supplement": True} for r in pair_rows(m, MAIN + SUPP, "platinum_489", rng)
             if "label_os12" in (r["label_a"], r["label_b"])]
    rows += pair_rows(m[m["in_rnaseq"]], ["label_platinum", "label_pfiplat6", "label_response"],
                      "platinum_rnaseq", rng)
    pw = pd.DataFrame(rows)
    pw["supplement"] = pw["supplement"].fillna(False).astype(bool) if "supplement" in pw else False
    pw.to_csv(OUT / "a2_pairwise_agreement.csv", index=False)

    ss = []
    for ref in REFS:
        for os_ in OS:
            s = m[[ref, os_]].dropna()
            r, t = s[ref].astype(int), s[os_].astype(int)
            se = wilson(int(((r == 1) & (t == 1)).sum()), int((r == 1).sum()))
            sp = wilson(int(((r == 0) & (t == 0)).sum()), int((r == 0).sum()))
            ss.append({"reference": ref, "os_label": os_, "n": len(s),
                       "ref_pos": int((r == 1).sum()), "ref_neg": int((r == 0).sum()),
                       "tp": int(((r == 1) & (t == 1)).sum()), "tn": int(((r == 0) & (t == 0)).sum()),
                       "sensitivity": se[0], "sens_lo": se[1], "sens_hi": se[2],
                       "specificity": sp[0], "spec_lo": sp[1], "spec_hi": sp[2],
                       "supplement": os_ == "label_os12"})
    ss = pd.DataFrame(ss)
    ss.to_csv(OUT / "a2_os_sens_spec.csv", index=False)

    def k(x, y, pop="platinum_489"):
        r = pw[(pw.population == pop) & (((pw.label_a == x) & (pw.label_b == y)) | ((pw.label_a == y) & (pw.label_b == x)))].iloc[0]
        return r

    def fk(r):
        return f"κ = {r.kappa:.3f} [{r.kappa_lo:.3f}, {r.kappa_hi:.3f}], n = {r.n}, agreement {r.agreement:.3f}"

    def fs(ref, os_, which):
        r = ss[(ss.reference == ref) & (ss.os_label == os_)].iloc[0]
        if which == "se":
            return f"{r.tp}/{r.ref_pos} = {r.sensitivity:.3f} [{r.sens_lo:.3f}, {r.sens_hi:.3f}]"
        return f"{r.tn}/{r.ref_neg} = {r.specificity:.3f} [{r.spec_lo:.3f}, {r.spec_hi:.3f}]"

    k18, k24 = k("label_os18", "label_platinum"), k("label_os24", "label_platinum")
    if k18.kappa < 0.40 and k24.kappa < 0.40 and k18.kappa_hi < 0.60 and k24.kappa_hi < 0.60:
        verdict = "SUPPORTED"
    elif k18.kappa >= 0.60 or k24.kappa >= 0.60:
        verdict = "NOT SUPPORTED"
    else:
        verdict = "PARTIAL AGREEMENT"

    show = pw[(pw.population == "platinum_489") & (~pw.supplement)]
    L = ["# A2 — label agreement", "",
         "Population: platinum-treated patients with both labels determinate. κ 95% CI: 2,000-resample bootstrap (seed 42).",
         "Coding: 1 = non-responder / resistant. Cells a1b1 … a0b0 are label_a × label_b.", "",
         "```", show[["label_a", "label_b", "n", "a1b1", "a1b0", "a0b1", "a0b0", "agreement", "kappa", "kappa_lo", "kappa_hi"]]
         .round(3).to_string(index=False), "```", "",
         "## Predictions vs observed", "",
         f"- P1 κ(OS18, platinum) {fk(k18)}; κ(OS24, platinum) {fk(k24)} — predicted both < 0.40",
         f"- P2 κ(OS18, pfiplat6) {fk(k('label_os18','label_pfiplat6'))}; κ(OS24, pfiplat6) {fk(k('label_os24','label_pfiplat6'))} — predicted both < 0.40",
         f"- P3 sensitivity for platinum-resistant: OS18 {fs('label_platinum','label_os18','se')}; OS24 {fs('label_platinum','label_os24','se')} — predicted < 0.50",
         f"- P4 specificity for platinum-sensitive: OS18 {fs('label_platinum','label_os18','sp')}; OS24 {fs('label_platinum','label_os24','sp')} — predicted > 0.85",
         f"- P5 κ(platinum, pfiplat6) {fk(k('label_platinum','label_pfiplat6'))} — predicted ≥ 0.80",
         f"- P6 κ(platinum, response) {fk(k('label_platinum','label_response'))} — predicted 0.30–0.60",
         "", f"**Decision rule: {verdict}** (OS-threshold labels vs the primary platinum label).", "",
         "## OS labels as tests against each reference (sensitivity / specificity, Wilson 95% CI)", "",
         "```", ss[["reference", "os_label", "n", "ref_pos", "tp", "sensitivity", "sens_lo", "sens_hi",
                    "ref_neg", "tn", "specificity", "spec_lo", "spec_hi"]].round(3).to_string(index=False), "```", "",
         "## Sensitivity check: platinum ∩ RNA-seq (pairs without OS labels)", "",
         "```", pw[pw.population == "platinum_rnaseq"][["label_a", "label_b", "n", "agreement", "kappa", "kappa_lo", "kappa_hi"]]
         .round(3).to_string(index=False), "```", "",
         "Supplement (12m): see rows with supplement = True in a2_pairwise_agreement.csv and a2_os_sens_spec.csv."]
    (OUT / "02_agreement_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
