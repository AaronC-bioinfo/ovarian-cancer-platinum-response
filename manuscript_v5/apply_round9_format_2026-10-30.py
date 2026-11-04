#!/usr/bin/env python3
"""
manuscript_v5/apply_round9_format_2026-10-30.py  (2026-10-30, ~09:15 ET; Aaron's instructions)
1. Remove the "Use of AI tools" section: the disclosure wording is to be agreed with the co-author first.
2. Author contributions: the co-author's role is left for him to state; only the first author's is given.
"""
from pathlib import Path

P = Path(__file__).resolve().parent / "manuscript_v5_src.md"
E = [
("## Use of AI tools\n\nClaude (Anthropic), an AI assistant, was used to write and run analysis and figure scripts under the first author's direction, to extract and check quotations from the literature, to audit the provenance of reported numbers, and to edit manuscript text. The first author reviewed all AI-assisted work against the analysis outputs and takes responsibility for the content. AI tools are not authors of this work.\n\n", ""),
("AMAC: conceptualization, data curation, formal analysis, methodology, software, visualization, writing – original draft. CL: methodology (guidance on the framing of the label-validity, leakage and validation analyses), writing – review and editing.",
 "AMAC: conceptualization, data curation, formal analysis, methodology, software, visualization, writing – original draft. CL: [to be stated by the co-author]."),
]


def main() -> None:
    s = P.read_text(encoding="utf-8"); assert "\r" not in s
    for i, (a, b) in enumerate(E):
        n = s.count(a); assert n == 1, f"edit {i}: {n} matches"
        s = s.replace(a, b)
    P.write_text(s, encoding="utf-8"); print(f"applied {len(E)} edits")


if __name__ == "__main__":
    main()

# 3. Section order changed to PLOS ONE's: … Acknowledgments, References, Supporting information, Figure legends, Tables.
