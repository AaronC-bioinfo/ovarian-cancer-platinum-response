#!/usr/bin/env python3
"""
manuscript_v5/apply_review4_round5c_2026-10-30.py
Round 5c (2026-10-30, ~00:35 ET): after the Cocchi 2026 PDF was obtained (OV Data/Project data/Literature/
10.1177_10732748261468094.pdf). Its Abstract and Conclusions support the two existing Cocchi sentences; its Methods state
that cohort barcode lists and platinum status (cohorts of 230, 201 and 142 patients) and workflows were released, which the
comparison now says. Also review point 14: GSE63885 processing (validation/04_probe_mapping.R: GPL570, hgu133plus2.db,
highest-mean probe; 06_external_validation_v2.py: log2 RMA, z-scored within GEO; validation/GSE63885_label_definitions.md:
serous/undifferentiated 80; DFS 34/40; clinical 10/64; sample identifiers in validation/outputs/gse63885_label_table.csv).
Run from manuscript_v5/: python apply_review4_round5c_2026-10-30.py
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
("Our label table differs from both in its sources (the TCGA-CDR progression-free interval and the PanCancer Atlas treatment timeline), in recording the provenance and flags of each re-derived call, and in placing platinum, survival and response labels side by side in the same patients; it does not supersede their annotations.",
 "Cocchi et al. also released the patient barcodes and platinum status of their three cohorts (230, 201 and 142 patients) with their workflows. Our label table differs from both in its sources (the TCGA-CDR progression-free interval and the PanCancer Atlas treatment timeline), in covering all 489 platinum-treated patients, in recording the provenance and flags of each re-derived call, and in placing platinum, survival and response labels side by side in the same patients; it does not supersede their annotations."),
("the pipeline's own simpler preprocessing (untransformed RSEM values for all 20,531 genes).",
 "the pipeline's own simpler preprocessing (untransformed RSEM values for all 20,531 genes). GSE63885 (Affymetrix GPL570; series-matrix log2 RMA values; probes mapped with hgu133plus2.db, keeping the probe with the highest mean expression per gene; genes z-scored within the cohort) was restricted to serous and undifferentiated tumours (80 samples). Its platinum-resistance label (disease-free survival < 180 days; 34 resistant, 40 sensitive) and clinical-response label (stable or progressive disease versus complete or partial response; 10 of 74) are defined verbatim, with sample identifiers, in S7 Table; differences in transfer performance cannot be attributed to the training label alone."),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:70]!r}"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
