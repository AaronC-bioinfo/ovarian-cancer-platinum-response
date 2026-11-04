#!/usr/bin/env python3
"""
manuscript_v5/apply_review5_preprint_2026-11-03.py  (2026-11-03; Aaron's instructions)
Corrections from claude/REVIEW5_PLOS_preprint_2026-11-03.md before the bioRxiv preprint.
Sole-author paper (Dr. Lockhart declined co-authorship on 2026-11-02).
Each edit must match exactly once. Not applied here (Aaron to decide or check): #13 symbol
convention (needs a figure redraw), #17/#18 citation checks, #19 AI-use statement, affiliation.
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
ZEN = "https://doi.org/10.5281/zenodo.20802753"  # concept DOI (all versions), as in CITATION.cff
E = [
# 1  authorship
("Aaron Michael Anuroop Chintala¹*, Christopher Lockhart¹", "Aaron Michael Anuroop Chintala¹*"),
("AMAC: conceptualization, data curation, formal analysis, methodology, software, visualization, writing – original draft. CL: [to be stated by the co-author].",
 "AMAC: conceptualization, data curation, formal analysis, investigation, methodology, project administration, software, validation, visualization, writing – original draft, writing – review & editing."),
("The authors received no specific funding for this work.", "The author received no specific funding for this work."),
("The authors have declared that no competing interests exist.", "The author has declared that no competing interests exist."),
("after the authors' earlier work on the same cohort", "after the author's earlier work on the same cohort"),
# 2  Zenodo DOI
("(S11 Table; Zenodo, [[ZENODO_DOI]])", f"(S11 Table; Zenodo, {ZEN})"),
("are archived at Zenodo ([[ZENODO_DOI]])", f"are archived at Zenodo ({ZEN})"),
# 4  restricted population + CIs (a9_group_tests.csv, primary_in_2011_release)
(" Patients without a status were more often dead before 18 months", " Within the 2011 release, patients without a status were more often dead before 18 months"),
("(24 of 95 versus 43 of 259; OR 1.70)", "(24 of 95 versus 43 of 259; OR 1.70, 95% CI 0.92–3.09)"),
("(28 of 114 versus 28 of 255; OR 2.63)", "(28 of 114 versus 28 of 255; OR 2.63, 95% CI 1.41–4.91)"),
("(13 of 68 versus 89 of 272; OR 0.49; S4 Table)", "(13 of 68 versus 89 of 272; OR 0.49, 95% CI 0.23–0.96; S4 Table)"),
# 6  sign convention (16_controlled_label_comparison.py header)
("between platinum-trained and 24-month-OS-trained models, averaged over the three models, each model's difference computed from its own predicted probabilities.",
 "between platinum-trained and 24-month-OS-trained models (platinum-trained minus OS-trained), averaged over the three models, each model's difference computed from its own predicted probabilities. Two secondary differences were computed the same way: platinum-trained minus 18-month-OS-trained models for platinum status, and 24-month-OS-trained minus platinum-trained models for OS at 24 months."),
# 7  scikit-learn exceptions (S1 Text)
("fixed seeds in scikit-learn 1.9.0 [@sklearn].", "fixed seeds in scikit-learn 1.9.0 [@sklearn] (analyses run in version 1.7.2 are listed in S1 Text)."),
# 8  gene-set null pool (06_published_genesets_summary.md)
("compared with 1,000 random gene sets of the same size;", "compared with 1,000 random gene sets of the same size drawn from the 15,484 common genes with complete data;"),
# 11  6 + 4 (a15b_resistant_event_source.csv)
("Setting aside the 10 resistant calls dated only by a death or by an event of unrecorded type",
 "Setting aside the 10 resistant calls dated only by a death (6) or by an event of unrecorded type (4, including the 2 above)"),
# 12  Kilim (protein) in the count
("Twelve studies of expression and platinum response that used TCGA-OV", "Twelve studies of expression (mRNA or protein) and platinum response that used TCGA-OV"),
# 14  the 7 non-carboplatin/cisplatin patients (a13_cohort_flow.csv)
("The 89 patients without any treatment record were excluded because their treatment could not be established.",
 "The 89 patients without any treatment record were excluded because their treatment could not be established, and the 7 whose treatment record did not include carboplatin or cisplatin were excluded as not platinum-treated."),
# 15  germline source; non-random sequenced subset
("(55 carriers, 44 with a germline variant);",
 "(55 carriers, 44 with a germline variant; germline calls are from the 2011 release, because the public PanCancer Atlas mutation file is somatic-only);"),
("*BRCA1/2* carriers were limited to truncating and splice-site variants called in the 2011 release;",
 "*BRCA1/2* carriers were limited to truncating and splice-site variants called in the 2011 release, whose sequenced patients are a subset of the cohort, not a random sample of it;"),
# 16  abstract: preference rests on construct grounds
("prefer platinum-specific labels, document provenance", "prefer platinum-specific labels for what they measure, document provenance"),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches for {a[:60]!r}"
        s = s.replace(a, b)
    assert "[[" not in s and "Lockhart" not in s and "authors'" not in s
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()
