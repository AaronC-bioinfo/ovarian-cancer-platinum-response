#!/usr/bin/env python3
"""
validation/00_gse63885_labels.py
────────────────────────────────
Q2 reorganisation, decision gate G4
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §3).

Parses data/external/GSE63885_series_matrix.txt directly (not the R-derived
CSVs), records the two response definitions VERBATIM from the GEO
characteristic keys, rebuilds both labels per sample (GEO writes missing values as the string "NA"), checks them against
data/external/harmonised_metadata.csv (what validation/06_external_validation_v2.py
uses), cross-tabs the two labels, and looks for the source of Chen et al.'s
34 resistant / 41 sensitive versus our 34 / 40.

Outputs
  validation/GSE63885_label_definitions.md      (verbatim definitions + results)
  validation/outputs/gse63885_label_table.csv   (one row per GSM)

Usage:  python validation/00_gse63885_labels.py

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already seen while locating fields (not predictions): the verbatim key text of
both characteristics; validation/02_parse_metadata.R keeps serous +
undifferentiated samples (series design: 73 serous, 7 undifferentiated) and
codes clinical CR/PR = 0, P/SD = 1, platinum 'resistant' = 1,
'moderately sensitive'/'highly sensitive' = 0; v2 reports 10 vs 64 (clinical)
and 34 vs 40 (DFS).

  P4.1  Exactly 75 of the 101 samples have a non-missing clinical status and a
        non-missing platinum-sensitivity category (series design: "For 75
        samples we provide extensive pathological and clinical data").
  P4.2  Rebuilding from the series matrix with the 02 filter reproduces the
        harmonised_metadata labels sample-for-sample: clinical 10 / 64,
        DFS 34 / 40, zero mismatches.
  P4.3  The platinum category agrees with the numeric DFS field
        (resistant ⇔ DFS < 180 d) for 100 % of samples with both.
  P4.4  ≥ 9 of the 10 clinical non-responders (SD/P) are DFS-resistant.
  P4.5  Chen's 34/41 (n = 75) equals the 75 annotated samples with no
        histology filter; our 74 differs by one sensitive sample that the
        serous/undifferentiated filter removes, OR by one sample absent from
        the expression matrix. (Two candidate explanations; the script
        reports which, if either, holds.)
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EXT = ROOT / "data" / "external"
SM = EXT / "GSE63885_series_matrix.txt"


def read_characteristics(path: Path) -> tuple[pd.DataFrame, dict[str, str]]:
    gsm, chars, hist_src = None, [], None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("!Sample_geo_accession"):
            gsm = [x.strip('"') for x in line.split("\t")[1:]]
        elif line.startswith("!Sample_characteristics_ch1"):
            chars.append([x.strip('"') for x in line.split("\t")[1:]])
    rows, keys = {}, {}
    for vals in chars:
        for g, v in zip(gsm, vals):
            if not v or ":" not in v:
                continue
            # key = text up to the LAST ': ' (keys themselves contain colons)
            k, val = v.rsplit(": ", 1) if ": " in v else (v, "")
            short = re.sub(r"\s*\(.*", "", k).strip().lower()
            keys.setdefault(short, k)
            rows.setdefault(g, {})[short] = val.strip()
    df = pd.DataFrame.from_dict(rows, orient="index")
    df.index.name = "sample_id"
    return df, keys


def main() -> None:
    df, keys = read_characteristics(SM)
    k_hist = next(k for k in df.columns if k.startswith("histophatological"))
    k_cs = next(k for k in df.columns if k.startswith("clinical status post"))
    k_ps = next(k for k in df.columns if k.startswith("platinium sensitivity"))
    k_dfs = next(k for k in df.columns if k.startswith("dfs"))

    t = pd.DataFrame(index=df.index)
    t["histology"] = df[k_hist]
    t["clinical_status"] = df[k_cs].replace({"": pd.NA, "NA": pd.NA})
    t["platinum_category"] = df[k_ps].replace({"": pd.NA, "NA": pd.NA})
    t["dfs_days"] = pd.to_numeric(df[k_dfs], errors="coerce")
    t["serous_or_undiff"] = t["histology"].str.contains("serous|undifferentiated", case=False, na=False)
    t["label_clinical"] = t["clinical_status"].map({"CR": 0, "PR": 0, "SD": 1, "P": 1})
    t["label_dfs"] = t["platinum_category"].map(
        {"resistant": 1, "moderately sensitive": 0, "highly sensitive": 0})

    geo = pd.read_csv(EXT / "GSE63885_expr_gene.csv", index_col=0, nrows=1)
    t["in_expr_matrix"] = t.index.isin(geo.columns)
    h = pd.read_csv(EXT / "harmonised_metadata.csv").set_index("sample_id")
    h = h[h["dataset"] == "GSE63885"] if "dataset" in h else h
    t["harm_present"] = t.index.isin(h.index)
    t["harm_clinical"] = pd.to_numeric(h["platinum_label_clinical"], errors="coerce").reindex(t.index)
    t["harm_dfs"] = pd.to_numeric(h["platinum_label_dfs.y"], errors="coerce").reindex(t.index)
    out_dir = ROOT / "validation" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    t.to_csv(out_dir / "gse63885_label_table.csv")

    # ── Checks ────────────────────────────────────────────────────────────
    annotated = t["clinical_status"].notna() & t["platinum_category"].notna()
    f = t[t["serous_or_undiff"]]
    used = t[t["harm_present"] & t["in_expr_matrix"]]  # what 06 actually scores

    def vc(s):
        return s.value_counts(dropna=False).to_dict()

    mism_c = used[(used["label_clinical"].fillna(-9) != used["harm_clinical"].fillna(-9))]
    mism_d = used[(used["label_dfs"].fillna(-9) != used["harm_dfs"].fillna(-9))]
    both = t["platinum_category"].notna() & t["dfs_days"].notna()
    cat_vs_num = pd.crosstab(t.loc[both, "platinum_category"], t.loc[both, "dfs_days"] < 180,
                             colnames=["dfs_days<180"])
    agree_num = int(((t.loc[both, "label_dfs"] == 1) == (t.loc[both, "dfs_days"] < 180)).sum())
    nr = used["label_clinical"] == 1
    ct = pd.crosstab(used["label_clinical"], used["label_dfs"], dropna=False)

    ann_all = t[annotated]
    ann_f = f[f["clinical_status"].notna() & f["platinum_category"].notna()]
    dropped_by_filter = ann_all[~ann_all["serous_or_undiff"]]
    used_dfs = used[used["label_dfs"].notna()]
    ann_not_used = ann_f[~ann_f.index.isin(used_dfs.index)]

    L = ["# GSE63885 label definitions (gate G4)", "",
         "Generated by `validation/00_gse63885_labels.py` from `data/external/GSE63885_series_matrix.txt`.", "",
         "## Verbatim definitions (GEO `!Sample_characteristics_ch1` keys)", "",
         f"- Clinical response key: `{keys[k_cs]}`",
         f"- Platinum sensitivity key: `{keys[k_ps]}`",
         f"- DFS key: `{keys[k_dfs]}`",
         f"- Histology key: `{keys[k_hist]}`", "",
         "Note: the moderately-sensitive interval is printed in GEO as `180>DFS>732` (sic).", "",
         "## Coding used in v2 (validation/02_parse_metadata.R; 06 reads harmonised_metadata.csv)", "",
         "- `label_clinical`: CR, PR → 0; SD, P → 1.",
         "- `label_dfs`: resistant → 1; moderately sensitive, highly sensitive → 0.",
         "- Histology filter: serous or undifferentiated.", "",
         "## Results", "",
         f"- Samples in series matrix: {len(t)}; histology: {vc(t['histology'])}",
         f"- P4.1 annotated (clinical status AND platinum category): {int(annotated.sum())} (predicted 75)",
         f"- Clinical status values (all): {vc(t['clinical_status'])}",
         f"- Platinum category values (all): {vc(t['platinum_category'])}",
         f"- After serous/undifferentiated filter: {len(f)}; in expression matrix and harmonised metadata: {len(used)}",
         f"- Labels as scored by 06: clinical {vc(used['label_clinical'])}; DFS {vc(used['label_dfs'])}",
         f"- P4.2 mismatches vs harmonised_metadata: clinical {len(mism_c)}, DFS {len(mism_d)} (predicted 0, 0)",
         f"- P4.3 category vs numeric DFS<180: {agree_num}/{int(both.sum())} agree (predicted all)",
         "", "```", cat_vs_num.to_string(), "```", "",
         f"- P4.4 clinical non-responders that are DFS-resistant: "
         f"{int((nr & (used['label_dfs'] == 1)).sum())}/{int(nr.sum())} (predicted ≥9/10)",
         "", "Cross-tab, clinical (rows) × DFS (cols), samples scored by 06 (NaN = missing):",
         "```", ct.to_string(), "```", "",
         "## Chen et al. 2022: 34 resistant / 41 sensitive vs ours", "",
         f"- All annotated samples, no histology filter: DFS {vc(ann_all['label_dfs'])} (n={len(ann_all)})",
         f"- Annotated after serous/undiff filter: DFS {vc(ann_f['label_dfs'])} (n={len(ann_f)})",
         f"- DFS-labelled samples scored by 06: {vc(used_dfs['label_dfs'])} (n={len(used_dfs)})",
         f"- Annotated samples removed by the histology filter: "
         + (", ".join(f"{i} ({r.histology}; {r.platinum_category})" for i, r in dropped_by_filter.iterrows()) or "none"),
         f"- Annotated serous/undiff samples not scored by 06: "
         + (", ".join(f"{i} (in_expr={r.in_expr_matrix}, harm={r.harm_present}; {r.platinum_category})"
                      for i, r in ann_not_used.iterrows()) or "none"),
         "", "P4.5 verdict is read from the three lines above; Chen's own selection rule is not stated in their paper "
         "beyond the counts, so any match is a reconstruction, not a confirmation."]
    out = ROOT / "validation" / "GSE63885_label_definitions.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
