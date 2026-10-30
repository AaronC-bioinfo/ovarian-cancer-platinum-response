#!/usr/bin/env python3
"""
manuscript_v5/build_SI.py
─────────────────────────
Builds the Supporting-information files for manuscript v5 from saved analysis outputs only
(no analysis is re-run). Each S Table is one .xlsx workbook whose first sheet ("README") gives the
caption, the source files and notes; the other sheets are the source CSVs copied unchanged.
S1 Text is assembled verbatim from the analysis-script headers (pre-specified predictions and
decision rules) and the post-run sections of the analysis summaries.

Run from the repo root:  python manuscript_v5/build_SI.py   (needs pandas + openpyxl; pandoc for S1 Text .docx)
Outputs → manuscript_v5/SI/S1_Table.xlsx … S11_Table.xlsx, S1_Text.md (+ .docx if pandoc is available)
Does not read outputs/results/ablation_split_variance_summary.csv.
"""
import re
import shutil
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LV = ROOT / "label_validity"
O = LV / "outputs"
PIN = ROOT / "outputs" / "results_pinned_2026-10-29"
SI = ROOT / "manuscript_v5" / "SI"
SI.mkdir(parents=True, exist_ok=True)


def md_table(path: Path, heading_prefix: str) -> pd.DataFrame:
    """Read the first markdown pipe table after a heading starting with heading_prefix."""
    lines = path.read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith(heading_prefix))
    rows = []
    for l in lines[i + 1:]:
        if l.startswith("|"):
            rows.append([c.strip() for c in l.strip().strip("|").split("|")])
        elif rows:
            break
    hdr, body = rows[0], [r for r in rows[2:]]
    return pd.DataFrame(body, columns=hdr)


def quotes(path: Path) -> pd.DataFrame:
    """Section 2 (per-paper verbatim quotations with page locations) of an extraction file, one line per row."""
    t = path.read_text(encoding="utf-8")
    i = t.index("\n## 2. "); j = t.find("\n## 3. ", i)
    return pd.DataFrame({"line": [l for l in t[i:j if j > 0 else None].splitlines() if l.strip()]})


def workbook(name: str, caption: str, notes: list[str], sheets: dict):
    readme = pd.DataFrame({"field": ["caption"] + ["source / note"] * len(notes), "text": [caption] + notes})
    with pd.ExcelWriter(SI / f"{name}.xlsx", engine="openpyxl") as w:
        readme.to_excel(w, sheet_name="README", index=False)
        for sh, src in sheets.items():
            df = src if isinstance(src, pd.DataFrame) else pd.read_csv(src)
            df.to_excel(w, sheet_name=sh[:31], index=False)
    print("wrote", name)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


# ── S1 Table: literature extraction ──────────────────────────────────────────
g5 = md_table(LV / "G5_literature_label_table.md", "## 1. Compact summary table")
g6 = md_table(LV / "G6_literature_additions.md", "## 1. Compact summary table")
g5.insert(0, "extraction_file", "G5_literature_label_table.md")
g6.insert(0, "extraction_file", "G6_literature_additions.md")
workbook("S1_Table", "S1 Table. Full literature extraction for Table 1, with verbatim quotations and their page locations. Each row of the study sheets is one study × cohort, as recorded from the full text and "
         "supplements; 'not stated' means the item was not reported. Quotation sheets reproduce section 2 of each extraction file verbatim.",
         [rel(LV / "G5_literature_label_table.md") + " (section 1; quotations in section 2; quote check in sections 6–7)",
          rel(LV / "G6_literature_additions.md") + " (section 1; quotations in section 2; 163 quotations machine-checked against the PDFs)"],
         {"G5_studies": g5, "G6_studies": g6, "G5_quotations": quotes(LV / "G5_literature_label_table.md"),
          "G6_quotations": quotes(LV / "G6_literature_additions.md")})

# ── S2 Table: agreement and OS-as-test ────────────────────────────────────────
workbook("S2_Table", "S2 Table. Pairwise agreement and OS-threshold test characteristics: full cohort (A11), patients with RNA-seq data and the "
         "12-month threshold (A2), against platinum status and the broad combined label, and at every threshold from 6 to 60 months (A13, exploratory).",
         ["A11: " + rel(O / "a11_kappa_full.csv") + ", " + rel(O / "a11_os_test_full.csv") + ", " + rel(O / "a11_coverage.csv"),
          "A2: " + rel(O / "a2_pairwise_agreement.csv") + ", " + rel(O / "a2_os_sens_spec.csv") + " (OS labels in the RNA-seq subset; column 'supplement' marks 12-month rows)",
          "A13: " + rel(O / "a13_threshold_sweep.csv") + " (null_ppv / null_specificity = values with no platinum information; max_sensitivity = bound set by prevalence)",
          "A19: " + rel(O / "a19_ipcw.csv") + " (inverse-probability-of-censoring-weighted sensitivity, specificity and PPV at 18 and 24 months)",
          "A9 Part B/C: " + rel(O / "a9_os_label_metrics.csv") + " (κmax, PABAK)"],
         {"A11_kappa_full": O / "a11_kappa_full.csv", "A11_os_test_full": O / "a11_os_test_full.csv",
          "A11_coverage": O / "a11_coverage.csv", "A2_pairwise_rnaseq": O / "a2_pairwise_agreement.csv",
          "A2_os_sens_spec_rnaseq": O / "a2_os_sens_spec.csv", "A9_os_label_metrics": O / "a9_os_label_metrics.csv",
          "A13_threshold_sweep": O / "a13_threshold_sweep.csv", "A19_ipcw": O / "a19_ipcw.csv"})

# ── S3 Table: BRCA / CCNE1 ───────────────────────────────────────────────────
md = pd.read_csv(O / "a13_min_detectable.csv")
workbook("S3_Table", "S3 Table. BRCA1/2 and CCNE1 associations for every carrier definition (A8): primary (germline or somatic truncating/splice), "
         "any non-silent variant, germline only, somatic only (A3 definition), BRCA1 and BRCA2 separately; CCNE1 amplification; same-patient "
         "differences between labels; minimum detectable differences (A13, exploratory).",
         ["A8: " + rel(O / "a8_brca_tests.csv") + " (set T1_all, T2_common, T4_CCNE1_amp), " + rel(O / "a8_brca_diff.csv") + ", " + rel(O / "a8_carriers.csv"),
          "A13 E7: " + rel(O / "a13_min_detectable.csv")],
         {"A8_tests": O / "a8_brca_tests.csv", "A8_same_patient_diff": O / "a8_brca_diff.csv",
          "A8_carriers": O / "a8_carriers.csv", "A13_min_detectable": md})

# ── S4 Table: cohort flow and missing platinum status ─────────────────────────
workbook("S4_Table", "S4 Table. Cohort characteristics (A14, descriptive), cohort flow (A13, exploratory) and comparison of patients with and without a determinate platinum status (A9), "
         "with bounds on sensitivity and PPV of the OS thresholds under the missing reference standard (A13).",
         ["A14: " + rel(O / "a14_cohort_characteristics.csv"), "A13 E1: " + rel(O / "a13_cohort_flow.csv"), "A9: " + rel(O / "a9_group_tests.csv") + ", " + rel(O / "a9_km.csv"),
          "A13 E3: " + rel(O / "a13_reference_missingness.csv"), "Patient-level labels: " + rel(O / "labels_full.csv")],
         {"A14_characteristics": O / "a14_cohort_characteristics.csv", "A13_cohort_flow": O / "a13_cohort_flow.csv", "A9_group_tests": O / "a9_group_tests.csv",
          "A9_km": O / "a9_km.csv", "A13_reference_missingness": O / "a13_reference_missingness.csv"})

# ── S5 Table: clinical and tumour characteristics ────────────────────────────
workbook("S5_Table", "S5 Table. Associations of each label with clinical and tumour characteristics: full cohort (A10, raw P and BH q within label), "
         "same-patient differences (A10), any-vs-no residual coding (A13, exploratory), and the earlier analysis with somatic BRCA1/2 and OS labels "
         "in the RNA-seq subset (A3).",
         ["A10: " + rel(O / "a10_tests.csv") + ", " + rel(O / "a10_diff.csv"), "A13 E6: " + rel(O / "a13_residual_any.csv"),
          "A3: " + rel(O / "a3_known_groups.csv") + ", covariates " + rel(O / "a3_covariates.csv")],
         {"A10_tests": O / "a10_tests.csv", "A10_same_patient_diff": O / "a10_diff.csv",
          "A13_residual_any": O / "a13_residual_any.csv", "A3_known_groups": O / "a3_known_groups.csv"})

# ── S6 Table: within-TCGA AUC ────────────────────────────────────────────────
r5 = pd.read_csv(O / "a5_cross_label_repeats.csv")
summ = r5.groupby(["train_label", "test_label"]).auc.agg(["mean", "min", "max", "count"]).reset_index()
rule = (O / "05_cross_label_summary.md").read_text(encoding="utf-8")
rule_lines = [l for l in rule.splitlines() if l.strip()]
workbook("S6_Table", "S6 Table. Within-TCGA cross-label AUC (A5): pooled out-of-fold AUC for each training label, test label, model and repeat; "
         "means and ranges; and the pre-specified decision rule with its outcome (verbatim from the analysis summary). In a later revision this "
         "all-patients analysis is reported as descriptive only; the controlled same-patient comparison (A16) is in S1 Text.",
         ["A5: " + rel(O / "a5_cross_label_repeats.csv") + "; summary and rule: " + rel(O / "05_cross_label_summary.md"),
          "Hanley–McNeil intervals (A12, " + rel(O / "a12_auc_intervals.csv") + ") are included for completeness but treat the mean AUC as one AUC and are anti-conservative for the OS labels (review_v4/CODE_ATTACK.md M1); the manuscript reports ranges instead."],
         {"A20_A16_fold_counts": O / "a20_a16_fold_counts.csv", "A5_by_model_repeat": r5, "A5_mean_range": summ, "A5_summary_verbatim": pd.DataFrame({"line": rule_lines}),
          "A12_hanley_mcneil": O / "a12_auc_intervals.csv"})

# ── S7 Table: GSE63885 transfer ──────────────────────────────────────────────
gl = (ROOT / "validation" / "GSE63885_label_definitions.md").read_text(encoding="utf-8").splitlines()
workbook("S7_Table", "S7 Table. Transfer to GSE63885 (A4): AUC with 95% bootstrap intervals for every training label, model and GEO label, in the "
         "primary (variant P) and untransformed-expression analyses; GEO label definitions (verbatim).",
         ["A4: " + rel(O / "a4_transfer_results.csv") + "; summary " + rel(O / "04_transfer_summary.md"),
          "GEO label definitions: " + rel(ROOT / "validation" / "GSE63885_label_definitions.md")],
         {"A4_transfer": O / "a4_transfer_results.csv", "GSE63885_label_definitions": pd.DataFrame({"line": [l for l in gl if l.strip()]})})

# ── S8 Table: published gene sets ────────────────────────────────────────────
workbook("S8_Table", "S8 Table. Gene-set transfer experiment (A6): published gene sets as fixed inputs, not replications of the published models; both sets were selected in data that included TCGA-OV patients. The 10 genes of Chen et al. and the 5 genes of Gao et al., compared with "
         "1,000 random same-size gene sets drawn from the 15,484 shared genes with complete data.",
         ["A6: " + rel(O / "a6_tests.csv") + ", " + rel(O / "a6_published_sets.csv") + ", " + rel(O / "a6_null.csv")],
         {"A6_tests": O / "a6_tests.csv", "A6_published_sets": O / "a6_published_sets.csv", "A6_null": O / "a6_null.csv"})

# ── S9 Table: leakage ────────────────────────────────────────────────────────
workbook("S9_Table", "S9 Table. Feature-selection leakage at the 12-, 18- and 24-month OS thresholds (A7; pinned environment): mean AUC with "
         "selection on the training split vs on the full dataset, supervised (F-score) and unsupervised (variance), with paired tests.",
         ["A7: " + ", ".join(rel(PIN / f) for f in ["ablation_supervised_leakage_summary.csv", "ablation_leakage_summary.csv",
                                                     "ablation_supervised_leakage_significance.csv", "ablation_leakage_significance.csv", "ENVIRONMENT.txt"]),
          "Pre-run note with predictions and post-run scorecard: " + rel(LV / "07_ablation_rerun_PRERUN.md"),
          "Preprocessing differs from the main classifier pipeline: untransformed RSEM, all 20,531 genes."],
         {"supervised_summary": PIN / "ablation_supervised_leakage_summary.csv", "unsupervised_summary": PIN / "ablation_leakage_summary.csv",
          "supervised_significance": PIN / "ablation_supervised_leakage_significance.csv",
          "unsupervised_significance": PIN / "ablation_leakage_significance.csv"})

# ── S10 Table: exploratory + Cox ─────────────────────────────────────────────
workbook("S10_Table", "S10 Table. Exploratory analyses (A13, A13b; added after the main results were known): decomposition of overall survival into the "
         "platinum-free interval (A13b: patients at risk at the end of platinum; the earlier A13 model, which set intervals below 1 day to 1 day, as a sensitivity analysis) and survival after progression; clinical-only models; exclusion of TCGA-CDR redacted records. Also the "
         "pre-specified Cox models of the TCGA-CDR progression-free interval (A3, R survival).",
         ["A13b (reported decomposition: platinum-free interval in the 408 patients at risk at the end of platinum; column analysis = at_risk / clipped_as_A13 sensitivity / unchanged): " + rel(O / "a13b_decomposition_cox.csv"),
          "A13: " + ", ".join(rel(O / f) for f in ["a13_os_decomposition_cox.csv", "a13_clinical_only_auc.csv", "a13_redaction.csv"]) + " (A13 decomposition set intervals below 1 day to 1 day; superseded by A13b)",
          "A3 Cox: " + ", ".join(rel(O / f) for f in ["a3_pfi_cox_hr.csv", "a3_pfi_cox_summary.csv", "a3_pfi_cox_ph.csv"])
          + " (cohort of 432 patients with any 'platin' agent; includes one oxaliplatin-only patient not in the 489)"],
         {"A13_os_decomposition": O / "a13_os_decomposition_cox.csv", "A13_clinical_only_auc": O / "a13_clinical_only_auc.csv",
          "A13_redaction": O / "a13_redaction.csv", "A13b_decomposition": O / "a13b_decomposition_cox.csv", "A20_cox_checks": O / "a20_cox_checks.csv", "A3_cox_hr": O / "a3_pfi_cox_hr.csv",
          "A3_cox_summary": O / "a3_pfi_cox_summary.csv", "A3_cox_ph": O / "a3_pfi_cox_ph.csv"})

# ── S11 Table: patient-level label resource ──────────────────────────────────
workbook("S11_Table", "S11 Table. Patient-level label table, version 1.0 (A17): for each of the 489 platinum-treated patients, every candidate label, "
         "the provenance-filtered combined label (column label_combined_strict; a candidate extension, preferred under the pre-specified A15 rule; 355 determinate) and the broad combined label (sensitivity analysis; 394), the re-derived "
         "platinum-free interval, and the provenance class, event source and flags of each re-derived call (A15, corrected run A15b); with a "
         "data dictionary, class counts, and the OS-threshold test characteristics against the broad and strict combined labels.",
         ["A17: " + ", ".join(rel(O / f) for f in ["label_resource_v1.csv", "label_resource_v1_dictionary.csv", "label_resource_v1_counts.csv"]),
          "A15b (provenance-filtered label as recommended): " + ", ".join(rel(O / f) for f in ["a15b_provenance.csv", "a15b_class_by_group.csv", "a15b_resistant_event_source.csv", "a15b_os_test_strict.csv"]),
          "A15 (as first run, before the near-threshold flag was added): " + rel(O / "a15_os_test_strict.csv") + "; scorecard in S1 Text"],
         {"label_table_v1": O / "label_resource_v1.csv", "data_dictionary": O / "label_resource_v1_dictionary.csv",
          "class_counts": O / "label_resource_v1_counts.csv", "A15b_class_by_group": O / "a15b_class_by_group.csv",
          "A15b_event_source": O / "a15b_resistant_event_source.csv", "A15b_os_test_strict": O / "a15b_os_test_strict.csv",
          "A15_os_test_strict_asrun": O / "a15_os_test_strict.csv", "A20_discordant_patients": O / "a20_discordant.csv",
          "A18_anchor_summary": O / "a18_anchor_summary.csv", "A18_anchor_counts": O / "a18_anchor_counts.csv"})

# ── S1 Text: pre-specified predictions and outcomes ─────────────────────────
def header(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        m = re.search(r'"""(.*?)"""', t, flags=re.S)
        return m.group(1).strip() if m else ""
    out = []
    for l in t.splitlines():
        if l.startswith("#"):
            out.append(l.lstrip("#").rstrip())
        elif out:
            break
    return "\n".join(out).strip()


def postrun(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()  # whole summary: results tables and post-run scorecards


def _postrun_old(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    m = re.search(r"^#+ .*(Predictions vs observed|Prediction scorecard|Post-run|Scorecard|Decision rule).*$", t, flags=re.M)
    return t[m.start():].strip() if m else t.strip()


ANALYSES = [
    ("Gate G1–G4: label coverage and sources", "00_gate_pfi_coverage.py", "00_gate_summary.md", "pre-specified"),
    ("Gate, post hoc: response-field sources", "00b_gate_posthoc_response_sources.py", "00b_posthoc_summary.md", "post hoc"),
    ("A1: label construction", "01_labels_master.py", "01_labels_summary.md", "pre-specified"),
    ("A2: agreement (RNA-seq OS labels)", "02_label_agreement.py", "02_agreement_summary.md", "pre-specified"),
    ("A3: associations with BRCA1/2 and clinical characteristics (somatic BRCA1/2; RNA-seq OS labels)", "03_known_groups.py", "03_known_groups_summary.md", "pre-specified"),
    ("A3b: Cox models of the progression-free interval", "03b_pfi_cox.R", None, "pre-specified"),
    ("A4: transfer to GSE63885", "04_transfer_matrix.py", "04_transfer_summary.md", "pre-specified"),
    ("A5: within-TCGA cross-label CV", "05_cross_label_cv.py", "05_cross_label_summary.md", "pre-specified; in a later revision reported as descriptive only, and its decision rule is superseded by the controlled comparison (A16)"),
    ("A6: published gene sets", "06_published_genesets.py", "06_published_genesets_summary.md", "pre-specified (supplementary)"),
    ("A8: BRCA1/2 germline + somatic; CCNE1", "08_brca_germline.py", "08_brca_germline_summary.md", "pre-specified; deposited before running (d5bd844)"),
    ("A9: patients without a platinum status", "09_platinum_missingness.py", "09_platinum_missingness_summary.md", "pre-specified; deposited before running (d5bd844)"),
    ("A10: prognostic characteristics, full cohort", "10_prognostic_covariates.py", "10_prognostic_covariates_summary.md", "pre-specified; deposited before running (e98b3d9)"),
    ("A11: full-cohort label table, agreement, OS-as-test", "11_full_cohort_labels.py", "11_full_cohort_labels_summary.md", "descriptive; no predictions"),
    ("A12: approximate AUC intervals", "12_auc_intervals.py", None, "descriptive; no predictions"),
    ("A13: exploratory label structure", "13_exploratory_label_structure.py", "13_exploratory_label_structure_summary.md", "exploratory, post hoc; no predictions; its decomposition (E4) is superseded by A13b"),
    ("A13b: Cox decomposition restricted to patients at risk", "13b_decomposition_at_risk.py", "13b_decomposition_at_risk_summary.md", "post hoc correction of A13 E4; decision rule written before running"),
    ("A14: cohort characteristics", "14_cohort_characteristics.py", None, "descriptive; no predictions"),
    ("A15: provenance audit of the re-derived interval", "15_reconstruction_provenance.py", "15_reconstruction_provenance_summary.md", "pre-specified in a later revision; deposited before running (d349b2b)"),
    ("A15b: correction run of A15 (near-threshold flag)", "15b_reconstruction_provenance_specfix.py", "15b_reconstruction_provenance_specfix_summary.md", "post hoc correction of an implementation error in A15; no new predictions"),
    ("A16: controlled comparison of training labels", "16_controlled_label_comparison.py", "16_controlled_label_comparison_summary.md", "pre-specified in a later revision; deposited before running (d349b2b)"),
    ("A17: patient-level label table (S11 Table)", "17_label_resource.py", None, "descriptive assembly; no predictions"),
    ("A18: sensitivity of the re-derived interval to the treatment anchor", "18_anchor_sensitivity.py", "18_anchor_sensitivity_summary.md", "post hoc; decision rule written before running"),
    ("A19: IPCW analysis of the OS thresholds as tests", "19_ipcw_os_thresholds.py", "19_ipcw_os_thresholds_summary.md", "post hoc; decision rule written before running"),
    ("A20: descriptive checks (A16 folds, discordant patients, Cox assumptions)", "20_documentation_checks.py", "20_documentation_checks_summary.md", "descriptive; no predictions"),
]
L = ["---", 'title: "S1 Text. Pre-specified predictions and decision rules for each analysis, with observed outcomes"', "---", "",
     "This file reproduces, verbatim, the header of each analysis script (written before the analysis was run, unless marked post hoc, "
     "descriptive or exploratory) and its full summary (results, and post-run notes and scorecards). Text added after a run is marked as such "
     "in the summaries; headers were not edited after running, except the time string in the A18 header (disclosed in the A18 summary, which also notes an inaccurate description of platinum agents in that header). Scripts A8–A10 were deposited in the public repository before they were run "
     "(commits d5bd844 and e98b3d9), and A15 and A16, added in a later revision, in commit d349b2b. The leakage rerun (A7) has its own pre-run note, reproduced in full. "
     "Headers are reproduced unchanged; those of A13b and A15–A17 refer to the critiques of earlier drafts that prompted those analyses as an 'external review' or a 'second review'.", "",
     "Analysis history (moved from the manuscript's Methods). The study's interpretation changed during the work. An earlier draft concluded, from somatic BRCA1/2 variants and from OS labels analysed only in patients with RNA-seq data, that OS thresholds measure survival rather than platinum response; the publicly deposited analyses with germline variants and the full cohort did not support that conclusion, and the paper was revised. In later revisions, the OS thresholds were reframed as candidate surrogates, the survival decomposition was reported as associations only and restricted to patients at risk at the end of platinum (A13b), the provenance audit was added (A15), and the claim that the training label changes classifier performance was withdrawn when the controlled comparison detected no difference (A16). In the provenance audit, the code omitted one pre-specified flag (an interval within 150–215 days); this was found when the results were scored, and a correction run that adds only that flag (A15b) gives the provenance-filtered label reported in the manuscript (355 patients, against 367 as first run). The descriptive full-cohort tables (agreement, coverage, threshold sweep, cohort characteristics) and the exploratory analyses were added after the main results were known.", ""]
for title, script, summ, status in ANALYSES:
    L += [f"# {title}", "", f"*Status:* {status}. *Script:* `label_validity/{script}`" + (f". *Summary:* `label_validity/outputs/{summ}`" if summ else "") + ".", "",
          "## Header (verbatim)", "", "```text", header(LV / script), "```", ""]
    if summ:
        L += ["## Summary: results and scorecard (verbatim)", "", postrun(O / summ), ""]
L += ["# A7: feature-selection leakage rerun in the pinned environment", "", "*Status:* pre-specified (pre-run note written before the run).", "",
      (LV / "07_ablation_rerun_PRERUN.md").read_text(encoding="utf-8").strip(), ""]
md_path = SI / "S1_Text.md"
md_path.write_text("\n".join(L) + "\n", encoding="utf-8")
if shutil.which("pandoc"):
    subprocess.run(["pandoc", str(md_path), "-o", str(SI / "S1_Text.docx")], check=True)
print("wrote S1_Text")
