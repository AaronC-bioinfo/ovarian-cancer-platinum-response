# Project Log — Ovarian Cancer Platinum Response

**Last updated:** 2026-10-29
**Status:** Analysis complete across Findings 1–6 and Enhancements 3–5. Consolidating
into a single manuscript. This log supersedes `archive/PROJECT_LOG_2026-06-22.md`
(kept for history).

---

## 2026-10-29 (22:00–23:30 ET) — External review: A15/A15b/A16/A17, manuscript v5 revised

- **External review of v5 (7 points)**, answered per the approved plan. Pre-specified analyses A15 and A16 were deposited before running (d349b2b, 21:56:39 ET).
- **A16** (controlled label comparison; Windows host, pinned environment, 21:57–21:59 ET): 134 patients, the same folds for every label. ΔAUC_24 −0.005 [−0.105, +0.087]. Q1 FAILED, Q2 held, Q3 held, Q4 FAILED (opposite direction). Decision rule: no difference detected; the claim that label choice changes classifier performance is withdrawn; A5 is descriptive only.
  - Deviation: crash at the final `print` (cp1252 console, U+2212) after the summary was written; no number affected.
  - VM environment check (scikit-learn 1.7.2), `label_validity/outputs/a16_env_check_vm/`: LR and SVM identical; RF cells differ by up to 0.136; all conclusions unchanged.
- **A15** (provenance audit; VM, 22:00 ET): P1 held (20/26), P2 FAILED (367 < 370), P3 held, P4 FAILED (1/4). Decision rule triggered: the strict combined label is recommended, the broad label (394) is a sensitivity analysis.
  - Deviation found while scoring: the header lists the 150–215-day interval as a flag, but the code left it out of `any_flag`.
- **A15b** (`15b_reconstruction_provenance_specfix.py`, correction run, 22:25 ET; Aaron chose the header definition): strict label 355 (99 / 256); 78/117 added patients clean; P3 still holds. The `a15_*` outputs are kept unchanged.
- **A17** (`17_label_resource.py`): versioned patient-level label table `label_resource_v1.csv` + dictionary + counts → S11 Table.
- **Scorecards** filled in `15_…_summary.md` and `16_…_summary.md`, including corrections of the script-header times (headers said ~22:10/~22:15 ET; commit d349b2b is 21:56:39 ET).
- **Manuscript** (`manuscript_v5/apply_external_review_2026-10-29.py`, 35 exact replacements; pre-review files in `manuscript_v5/archive_pre_external_review_2026-10-29/`):
  - title: "provenance" replaces "validity";
  - OS thresholds framed as candidate surrogates from our own earlier analyses;
  - A15/A15b results; strict label in Table 2;
  - Fig 4 retitled as associations (exploratory), with the handling of negative intervals and deaths stated;
  - A16 null result; A5 descriptive;
  - "markers do not resolve the comparison"; OR 0.64 reported as "no clear evidence of association";
  - label table (S11) named in the abstract (271 words) and the conclusion.
- **Rebuilt:** `manuscript_v5.md`, the docx, the SI (S11 Table; A15/A15b/A16/A17 in S1 Text), Fig 4 (title only; plotted values unchanged), and S2 Text headings. README points to the strict label and the label table.
- **Independent audit:** fresh agent, read-only. All new A15b/A16/label-table numbers matched except one: the decomposition floors 28 intervals below 1 day (19 negative, 9 zero), not 8 — fixed. The should-fix items were applied in `manuscript_v5/apply_external_review_round2_2026-10-29.py` (20 edits): the precise "clean" definition (3 added patients not clean only because of death-dated events); broad vs strict wording; the GSE63885 comparison marked descriptive; the A16 interval described as conditional on the fitted models, two-sided (+0.09 / −0.11), with fold stratification and the per-repeat mean −0.016 stated; the earlier v1.0.0 release cited (Zenodo 10.5281/zenodo.20802754); leftover decomposition contrasts removed. S11 OS columns renamed `label_os18_all`/`label_os24_all` to match `labels_full.csv`; missing event types written as `type_not_recorded`; README results updated (strict label, A16). Not changed: OS-labelled patients still called "non-responders" in tables; "label-validity" in Author contributions (Aaron to decide).
- **Open:** Zenodo release and DOI; Cocchi 2026 PDF; AI-use paragraph decision; Lockhart email.

---

## 2026-10-30 (early) — SI, reporting checklists, final audit of v5

- **Supporting information** built by `manuscript_v5/build_SI.py` from saved outputs only:
  - S1–S10 Tables (.xlsx with README sheets; S1 includes the G5/G6 verbatim-quotation sheets);
  - S1 Text (every script header verbatim plus full summaries);
  - S2 Text (STROBE + STARD 2015).
- **A14** (`14_cohort_characteristics.py`, descriptive): cohort characteristics for S4 Table. The A13 environment is recorded in `label_validity/outputs/a13_ENVIRONMENT.txt`.
- **Final independent audit** (`review_v5/FINAL_AUDIT.md`, `number_ledger.csv`): 160 numbers checked; 125 match, 33 differ only by rounding, 0 mismatch. Blockers B1–B2 and majors M1–M6 were fixed in the text (`manuscript_v5/fix_audit_2026-10-29.py`):
  - exploratory claims hedged;
  - "agree at best moderately" replaces "agree poorly";
  - the post hoc analyses are flagged in Methods;
  - Cocchi named as the closest prior work;
  - the sign conventions of the differences are stated;
  - the limitation on the 89 excluded patients is added;
  - every S item is cited;
  - the short title has 37 characters.
- **Open:**
  - B3 (Aaron): commit/push all v4–v5 material, then make a Zenodo release; the DOI goes into Data availability.
  - Cocchi 2026 PDF to confirm the citation.
  - Lockhart's ORCID.
  - TIFF/EPS figures at submission.
  - The AI-use paragraph is kept until Aaron says otherwise.

---

## 2026-10-29 (night) — Red team on v4; A13; G6 literature; manuscript v5

- **Red team** (`review_v4/`: CODE_ATTACK, METHODS_ATTACK, REVIEW_ROUND2, NOVELTY_ATTACK; consolidated in CONSOLIDATED_FINDINGS.md; scratch scripts preserved):
  - Code and numbers reproduce byte-for-byte.
  - The interpretive claims failed or were weakened: "not a different construct"; "specific but insensitive" forced by prevalence; PPV conditional on having a status; similarity claimed from underpowered tests.
  - The A5 verdict was unreported, and the reframe was undisclosed.
  - Villalobos 2018, Yang SYC 2018 and Talijanovic 2025 were not cited.
- **A13** (`label_validity/13_exploratory_label_structure.py`; exploratory, post hoc, no predictions; VM, scikit-learn 1.7.2, lifelines 0.30.0):
  - Cohort flow: 585 → 496 → 489. The 89 without a treatment record have median OS 27.6 months.
  - Threshold sweep 6–60 months: best κ 0.47 at 36 months.
  - PPV bounds: 0.38–0.91 at 18 months.
  - Cox decomposition: BRCA, CCNE1 and aneuploidy act on PFI; age and residual > 1 cm act on survival after progression.
  - Clinical-only AUC: OS labels 0.62–0.64, platinum status 0.48.
  - Any-residual coding: platinum status OR 3.22.
  - Minimum detectable differences; redaction sensitivity (PFI 358, κ 0.964).
- **G6 literature** (`label_validity/G6_literature_additions.md`; 11 PDFs; 163 quotes machine-checked):
  - Villalobos did not compare with PLATINUM_STATUS (C1–C4 all no).
  - Markman 1991 does not source the 6-month cut-off.
  - Yousefi p. 6 supports "OS noisy".
- **Manuscript v5** (`manuscript_v5/`, figures `figures/v5/`):
  - Analysis-history disclosure; A5 verdict reported; threshold-specific claims.
  - Table 1 expanded to 12 studies; 42 references.
  - All 169 decimals found in outputs (heuristic check).
  - The AI-use paragraph is kept until Aaron says otherwise; the Zenodo DOI is a placeholder.

---

## 2026-10-29 (late) — Reviews, A8–A12, reframed manuscript v4

- **Independent reviews** (`review_v3/EDITOR_REVIEW.md`, `PEER_REVIEW.md`) found these problems:
  - the question was not evident;
  - the OS labels were set up as a straw man;
  - BRCA was a weak anchor, and germline calls were already on disk;
  - the claims about prediction were overstated;
  - leakage, GEO transfer and the gene sets were off-question;
  - desk-check failures.
- **A8 (germline + somatic BRCA; CCNE1), A9 (who lacks platinum status), A10 (prognostic covariates, full cohort):** predictions were pushed to GitHub before each run (d5bd844, e98b3d9). Scorecards are in `label_validity/outputs/08–10_*_summary.md`. Key results:
  - BRCA OR: platinum 0.41 [0.14, 1.04]; OS18 0.15 [0.00, 0.97]; OS24 0.22 [0.04, 0.75]. Same-patient differences include 0.
  - Undetermined status: OS no different (p 0.37), but more early deaths and more PD/SD.
  - OS thresholds: specificity 0.94–0.98, PPV 0.74–0.82, sensitivity 0.21–0.39.
  - Residual disease and aneuploidy: same-patient differences include 0.
- **A11 (full-cohort label table, κ, OS-as-test; descriptive) and A12 (Hanley–McNeil AUC intervals; descriptive).**
- **Reframe (Aaron approved 19:29 ET):** `manuscript_v4/` with the question "Which outcome label should a platinum-response classifier use?" Answer: OS thresholds are specific but insensitive subsets of platinum resistance; the choice trades coverage against sensitivity. Withdrawn from v3: "OS labels measure survival, not platinum response" and "Only the platinum labels show known-groups validity".
  - Figures: `figures/v4/` (F1–F3; S1 GEO transfer; S2 leakage).
  - Author summary removed.
  - The AI-use paragraph is kept until Aaron says otherwise.
  - The Zenodo DOI is pending release.
- v3 files are kept unchanged as superseded.

---

## 2026-10-29 (evening) — v3 draft, independent audit, leakage ablation rerun in the pinned environment

- **v3 manuscript:** `manuscript_v3/manuscript_v3.md` (canonical) → `PLOS_Draft_Chintala_v3_LabelValidity.docx`
  via `manuscript_v3/build_docx.py` (pandoc 3.1.3). Not yet sent to Lockhart.
- **Independent audit** (Fable agent, prompt `manuscript_v3/AUDIT_PROMPT_v3_Fable.md`; output `audit_v3/`):
  150 numbers traced, none wrong from an analysis output.
  - Blockers: leakage provenance; Data availability (Zenodo/GitHub lack the v3 work); four text slips.
  - Text fixes applied, plus majors M1/M4 and minors 1–4, 6–8, 10–11, 13.
- **A7 leakage ablation rerun** (`label_validity/07_ablation_rerun_PRERUN.md`, predictions written first):
  - Host run: Python 3.14.5 / scikit-learn 1.9.0 (`outputs/results_pinned_2026-10-29/ENVIRONMENT.txt`).
  - Patch (Aaron approved 18:19 ET): `src/ablation.py` l.62, l.233–234 pass `.to_numpy()` to
    `f_classif` / `StandardScaler`, because scikit-learn 1.9.0 rejects duplicate gene symbols. Output
    identical under 1.7.2.
  - P1–P4 all held. 18/24-mo mean inflation: supervised +0.208 (June +0.207), unsupervised +0.006
    (June +0.003). Only RF rows and two unsupervised SVM rows changed.
  - F4 now reads `outputs/results_pinned_2026-10-29/`. The June `outputs/results/ablation_*` files are
    superseded but kept, and the old figures are kept in `figures/v3/superseded_june-ablation_2026-10-29/`.
- **R environment recorded:** R 4.6.0, survival 3.8.6 (`label_validity/outputs/R_ENVIRONMENT.txt`).
- **Open (Aaron):**
  - commit, push and tag the v3 work, then make a new Zenodo version and cite its version DOI;
  - S1–S7 Tables and S1 Text are not yet built;
  - `_to_delete/` holds stray build files.

---

## 2026-10-29 — Paper reorganised around Q2 (label construct validity); decision gate run

- **Decision (Aaron, 2026-10-29):** the v2 draft is reorganised around one question — *Does TCGA-OV
  support a valid platinum-response label, and what do classifiers trained on the common proxy labels
  actually predict?* Plan: `claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md` (claude.ai project).
- **Primary response label:** `PLATINUM_STATUS` (Resistant vs Sensitive) from cBioPortal `ov_tcga_pub`
  (TCGA, Nature 2011). Sensitivity label: PFI from end of first-line platinum = CDR `PFI.time` − last
  `Adjuvant` platinum `STOP_DATE`, 183-day cutoff. The `PLATINUM_STATUS` definition is still to be
  verified verbatim from the TCGA 2011 paper.
- **Gate G1–G4** (`label_validity/00_gate_pfi_coverage.py`, `validation/00_gse63885_labels.py`,
  predictions in headers):
  - G1 PASS — CDR PFI for 214/214, 206/206, 199/199 classification patients and 432/432 Cox patients.
  - G2 PASS — `PLATINUM_STATUS` determinate for 134 patients in the 24m cohort (39 R / 95 S);
    agrees with PFI-from-platinum in 268/272 = 0.985.
  - G3 FAIL as pre-registered (power: 5 PD patients with a platinum label in the pan-can response field).
    Post hoc (`00b_gate_posthoc_response_sources.py`): with the ov_tcga_pub/CDR copies of the same
    field, P(Resistant | PD) = 15/18 = 0.833; P(short PFI-from-platinum | PD) = 18/30 = 0.600.
    OS18 flags 11/49 and OS24 17/49 Resistant patients as non-responders.
  - G4 — all predictions held; definitions in `validation/GSE63885_label_definitions.md`.
    Chen et al.'s 34/41 = all 75 annotated GSE63885 samples with no histology filter.
- **Correction:** "~89% missing PRIMARY_THERAPY_OUTCOME_SUCCESS" is true only of the pan-can
  `data_timeline_status.txt`. The field is present for 366/489 (ov_tcga_pub) and 424/489 (CDR)
  platinum patients. The v2 label-validity statement must be restated.
- **Dropped:** AACR 2027 abstract (Nov 10). Preprint target moves from Nov 5 to about Nov 13–14.

---

## 2026-09-07 — Audit, headline AUC correction, F1000 archived

- Full project audit run; report at `AUDIT_INVENTORY_2026-09-07*.md`.
- Headline AUC table corrected; prior values traced to a stale intermediate file (see note below).
- `cox_quick.R` retired after `phase2_02_cox_model.R` re-run reproduced C-index 0.5698, log-rank
  p 0.02342, Schoenfeld global p 0.1785.
- KM figure rendering bug fixed (`ggsave`/`print` → `png`/`print`/`dev.off()`);
  `km_risk_groups.png` now renders at 65 KB.
- F1000 track archived to `archive/F1000Research_Draft_ARCHIVED_2026-09-07.docx`; two superseded
  drafts deleted, backups in `archive/f1000_superseded_2026-09-07/`.

---

## Publication strategy

- **Sole target: PLOS Computational Biology.** One comprehensive submission.
- **The F1000Research methods-critique track is DROPPED.** No longer a publication
  target. All findings fold into the single PLOS submission. Pre-correction F1000 base
  draft moved to `archive/`.
- Nature Communications only as a stretch goal, contingent on co-authorship and data access.
- ~~To confirm with Dr. Lockhart before final submission: that Findings 1–3 (leakage
  ablation, label construct validity, external-validation failure) fold into the PLOS
  paper rather than being dropped or retargeted.~~ *Superseded 2026-10-29: the paper is
  reorganised around label construct validity (Q2); see the 2026-10-29 entry.*

---

## Headline results (current, verified)

### Classification performance — clean, leakage-free (30 repeated stratified splits)

Generated by `fixes/phase1_rerun_clean_auc.py` → `outputs/results/clean_auc_table.csv` — authoritative leak-free AUC values (2026-08-20 re-run). NOTE: `ablation_split_variance_summary.csv` is a STALE ORPHAN and must not be used; it disagrees with its own raw file by up to 0.09 AUC. See `fixes/phase1_provenance.md`.

| Model | 12m AUC | 18m AUC | 24m AUC | Status |
|---|---|---|---|---|
| Logistic Regression | **0.457** | **0.669** | **0.678** | LOCKED (deterministic, triple-verified) |
| Random Forest | **0.400** | **0.628** | **0.716** | VERIFIED (clean_auc_table.csv, 2026-08-20 re-run) |
| SVM (RBF) | **0.405** | **0.619** | **0.733** | VERIFIED (clean_auc_table.csv, 2026-08-20 re-run) |

**Important correction (2026-07-20).** The prior AUC table (LR 0.542/0.658/0.712,
RF 0.411/0.609/0.709, SVM 0.363/0.515/0.771) was traced to a **stale orphan output**,
`ablation_split_variance_summary.csv` — the oldest of the eight ablation files, left over
from a superseded run and inconsistent with its own raw data. See `fixes/phase1_provenance.md`.
Logistic Regression is deterministic and reproduces exactly across three independent runs;
its corrected row is final. RF and SVM are scikit-learn-version-sensitive and must be
regenerated in the authors' pinned environment before publication.

### Leakage ablation
- Supervised F-score selection inflates AUC by mean **+0.223** (up to **+0.552** for SVM@12m);
  significant at p<0.05 in 7/9 model×threshold combinations.
- Unsupervised variance selection: negligible inflation (**+0.011**).
- Replicates cross-cancer: LUAD +0.320, COADREAD +0.330 (unsupervised +0.004 / +0.018).
- Source: `outputs/results/ablation_*`, `multi_cancer/outputs/comparison/`.

### Label construct validity (Finding 2)
- OS-threshold proxy label has **0/5 recall** on clinically confirmed Progressive Disease
  (95% CI [0.000, 0.522], Clopper-Pearson) — `outputs/results/label_investigation_recall_on_confirmed.csv`.
- ~89% of the platinum cohort is missing `PRIMARY_THERAPY_OUTCOME_SUCCESS`.
- Cohen's kappa ≈ 0 despite high raw agreement (extreme class imbalance).

### External validation failure (Finding 3)
- Near-chance AUC on GSE63885 / GSE9891.
- Post-ComBat inter-platform Pearson r and TCGA-top500 variance ratio: **now computed in code**
  (`validation/05_batch_correction.R` → `validation/outputs/combat_diagnostics.csv`);
  manuscript values were r = −0.005 and ratio ~1.00, pending confirmation on re-run.

### Cox model (Finding / Enhancement baseline, n=432, 242 events)
- Aneuploidy Score HR 1.021 (95% CI 1.004–1.039) p=0.017; TMB HR 0.894 p=0.238.
- C-index and KM log-rank p **now persisted** (`phase2/outputs/cox_summary_stats.csv`);
  manuscript values C-index 0.570, log-rank p 0.023, pending confirmation on re-run.
- Schoenfeld global p 0.178. Median OS by risk tertile: 52.0 / 51.9 / 39.4 months.

### Enhancement 3 — tumour cellularity (ESTIMATE) — COMPLETE
- Purity a non-significant Cox covariate (HR 4.36, p=0.526); C-index 0.603 → 0.604.
- Gene overlap 491/500 after purity correction. EMT adj p 1.35e-30 (corrected) vs 1.6e-17.
- Purity does NOT explain the ribosomal signal — cellularity-confound hypothesis not supported.

### Enhancement 4 — HRD / BRCA — COMPLETE
- BRCA1/2 somatic mutation 33/409 (8.1%); HR 0.455 p=0.024; C-index 0.573 → 0.588.
- Matched-subset size **now persisted** (`hrd/brca_cox_summary.csv`); manuscript n=335 pending
  confirmation on re-run.
- HRR-panel overlap with importance/variance lists = 0.
- scarHRD scoped out (seg file has total CN only, not allele-specific).

### Enhancement 5 — expression-augmented Cox — COMPLETE
- Cohort A (n=235): 0.585 / 0.587 / 0.585 — expression adds nothing.
- Cohort B (n=163): 0.557 / 0.606 / 0.558 — fragile gain, collapses under conservative
  regularization; paired t p=0.036, Wilcoxon p=0.063.
- "Pure ridge (α=0)" applies to the **final refit only**; per-fold CV selected α=0 in just
  8/25 Cohort B folds (`enhancement5/outputs/alpha_selection_summary.csv`). Final-model α
  **now persisted** (`enhancement5/outputs/final_model_alpha.csv`).

### Finding 5 — feature-importance robustness
- SHAP–MDI Spearman ρ = 0.98; permutation agreement 0.37–0.42 (correlated features).
- 12m excluded from gene-importance averaging (near-chance: mean AUC 0.475, SD 0.198,
  range 0.075–0.976).
- **Theme 2 (EMT/ECM)** robust across all list sizes, all methods, with/without 12m.
- **Theme 1 (ribosome/translation)** an open question: NOT significant under SHAP at top-50/100
  **with 12m** (p=0.371, 0.305), but IS significant at top-100 **without 12m** (p=0.020) — must
  state the condition.
- COL1A1 is 12m-dependent (drops from top-200 without 12m). FLNA never ranks highly:
  **rank 299–508** across all methods/thresholds (corrected from the earlier "460–505").
- SHAP is primary; MDI a concordance check; permutation a weaker supplementary note.
- Gene-list cutoff standardized at top-200.

---

## Reproducibility notes / open items

- **Pin scikit-learn** in `requirements.txt` to the authors' environment version — unpinned
  deps (`scikit-learn>=1.5.0`) are why RF/SVM AUCs were not reproducible.
- Git history still carries ~4.7 GiB of `_tmp_LUAD_data` / `_tmp_COADREAD_data` blobs from
  commit `1d3b542`. Removal via `git filter-repo` is a HUMAN-ONLY action — see
  `AUDIT_2026-07-20.md` §6.4 and coordinate with the JOSS submission first (force-push changes
  referenced commit hashes).
- Manuscript numeric corrections applied as tracked changes in
  `PLOS_CompBio_Draft_Chintala_v1_redline.docx`; RF/SVM cells and R-derived numbers left as
  `[COWORK: pending Windows re-run]` placeholders until the authors' environment run supplies them.

---

## Directory map

See `DIRECTORY_MAP.md`. In brief: `cellularity/` = Enhancement 3, `hrd/` = Enhancement 4,
`enhancement5/` = Enhancement 5.
