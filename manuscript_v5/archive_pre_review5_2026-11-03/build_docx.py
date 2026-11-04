"""
manuscript_v5/build_docx.py
───────────────────────────
Builds the Word draft from manuscript_v5.md (canonical text).
Pre-processing only (no text changes):
  * the first-line "# Title" becomes the YAML title;
  * headings are shifted up one level (## → #, ### → ##);
  * each figure image is inserted immediately before its legend ("**Fig N.");
  * pipe-table separator rows are rewritten with dash counts that set relative column widths.
Usage (needs pandoc on PATH):
  python build_docx.py <manuscript_v5.md> <figures_dir> <out.docx>
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

md, figdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
lines = md.read_text(encoding="utf-8").splitlines()

FIGS = {1: ("F1_coverage_agreement.png", "5.83in"), 2: ("F2_known_groups.png", "5.83in"),
        3: ("F3_cross_label_auc.png", "5.83in"), 4: ("F4_os_decomposition.png", "4.3in")}
# relative column widths (from the reviewed v3 layout), one list per table in order
WIDTHS = [[8, 14, 8, 9, 13, 10], [7, 15, 7, 6, 6], [4, 3, 3, 3, 3, 3]]

assert lines[0].startswith("# "), "first line must be the title"
title = lines[0][2:].strip().replace('"', '\\"')
body, table_i = [], 0
for ln in lines[1:]:
    m = re.match(r"\*\*Fig (\d)\.", ln)
    if m:
        f, w = FIGS[int(m.group(1))]
        body += [f"![]({(figdir / f).as_posix()}){{width={w}}}", ""]
    if re.fullmatch(r"\|(-+\|)+", ln.strip()):
        ws = WIDTHS[table_i]
        assert ln.count("|") - 1 == len(ws), f"table {table_i + 1}: column count mismatch"
        ln = "|" + "|".join("-" * (w * 3) for w in ws) + "|"
        table_i += 1
    if ln.startswith("### "):
        ln = ln[1:]
    elif ln.startswith("## "):
        ln = ln[1:]
    body.append(ln)
assert table_i == len(WIDTHS), f"found {table_i} tables, expected {len(WIDTHS)}"

tmp = Path(tempfile.gettempdir()) / "v5_build.md"  # outside the repo
tmp.write_text(f'---\ntitle: "{title}"\n---\n\n' + "\n".join(body) + "\n", encoding="utf-8")
ref = Path(__file__).resolve().parent / "reference_plos.docx"  # Times New Roman 12 pt, double-spaced, 1-inch margins, line numbers
subprocess.run(["pandoc", str(tmp), "-o", str(out)] + (["--reference-doc", str(ref)] if ref.exists() else []), check=True)
tmp.unlink()
# journal format: continuous line numbers and black headings (pandoc's sectPr/styles override the reference doc)
import re as _re, shutil as _sh, zipfile as _zf
_tmpz = out.with_suffix(".tmp.docx")
with _zf.ZipFile(out) as zin, _zf.ZipFile(_tmpz, "w", _zf.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/document.xml":
            t = data.decode("utf-8")
            if "<w:lnNumType" not in t:
                t = _re.sub(r"<w:sectPr([^>]*)>", r'<w:sectPr\1><w:lnNumType w:countBy="1" w:restart="continuous"/>', t, count=1)
            data = t.encode("utf-8")
        if item.filename == "word/styles.xml":
            t = data.decode("utf-8")
            t = _re.sub(r'<w:color w:val="[0-9A-Fa-f]{6}"[^/]*/>', '<w:color w:val="000000"/>', t)
            data = t.encode("utf-8")
        zout.writestr(item, data)
_sh.move(_tmpz, out)
print("wrote", out)
