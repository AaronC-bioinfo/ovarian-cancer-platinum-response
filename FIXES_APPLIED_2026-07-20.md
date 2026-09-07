# Fixes applied — audit 2026-07-20 close-out

**Branch:** `fixes-2026-07-20` · **Applied:** 2026-08-20 · **Pushed:** no
**Numbers source:** the author's own Windows re-run (Python 3.14 / scikit-learn 1.9.0, R 4.6.0),
independently verified against the on-disk CSVs before any manuscript edit was made.

Status legend — **Done** (applied and verified) · **Author-decision** (flagged, deliberately
not resolved) · **Human-only** (cannot be done from here).

---

## 1. Table 2 — RF and SVM AUCs

**Status: Done.**

| Model | 12 m | 18 m | 24 m |
|---|---|---|---|
| Logistic Regression *(already locked, unchanged)* | 0.457 | 0.669 | 0.678 |
| Random Forest | **0.400** | **0.628** | **0.716** |
| SVM (RBF) | **0.405** | **0.619** | **0.733** |

Source `outputs/results/clean_auc_table.csv` (0.4004 / 0.6277 / 0.7157 and 0.4045 / 0.6191 /
0.7333, 30 splits each). Direction of travel worth noting in review: RF and SVM both **fell**
at 12 m and 18 m and **rose** at 24 m relative to the pre-audit draft.

Files touched: `PLOS_CompBio_Draft_Chintala_v1_redline.docx`, `fixes/manuscript_changelist.md`.

## 2. Cox baseline, BRCA, ComBat, elastic-net α

**Status: Done.**

| Item | Manuscript | Computed | Action |
|---|---|---|---|
| Cox C-index | 0.570 | 0.569801 | confirmed, pending flag rejected |
| KM log-rank p | 0.023 | 0.023423 | confirmed, pending flag rejected |
| BRCA matched n | 335 | 335 | confirmed, pending flag rejected |
| BRCA HR / p | 0.455 / 0.024 | 0.455287 / 0.023824 | confirmed, no edit needed |
| BRCA C-index | 0.573 → 0.588 | 0.573149 → 0.588457 | confirmed, no edit needed |
| post-ComBat Pearson r | −0.005 | −0.0071670 | **changed to −0.007** (2 places) |
| Cohort A final α | — | 0.9 | recorded |
| Cohort B final α | 0 ("pure ridge") | 0 | **rewritten** — see below |

The "pure ridge" sentence now states that α=0 is a property of the **final** Cohort B model
fit on the full n=163 cohort, and that α=0 was selected in only **8 of 25** outer CV folds
(`enhancement5/outputs/alpha_selection_summary.csv`), so it is not a stable fold-level
preference. This resolves the earlier "pure ridge" flag.

Files touched: the redline, `fixes/manuscript_changelist.md`.

## 3. Variance ratio — 3.70 vs ~1.00

**Status: Author-decision. Not resolved.**

`validation/outputs/combat_diagnostics.csv` gives
`geo_variance_ratio_tcga_top500_vs_all = 3.7039` (mean variance of the 500 selected genes in
GEO 1.0657, against 0.2877 for all 15,994 common genes). The manuscript asserts ~1.00 and uses
that to rule out feature selection as the cause of external-validation failure. **3.70x does
not support that inference.**

Three sentences carry a `[COWORK: AUTHOR DECISION]` tracked flag; the value 1.00 was left in
place and the surrounding argument was not rewritten:

1. **Results** — "…indistinguishable from the variance of all genes in that dataset (ratio 1.00)" — the sentence that cites the number.
2. **Methods** — "…we additionally compared the variance of TCGA's selected genes to the variance of all genes within the GEO dataset itself…" — describes the computation that yields 3.70x.
3. **Abstract** — "…a failure attributable to platform-level distributional incompatibility rather than model or feature choice." — the inference that rests on the ~1.00 claim.

## 4. Ribosome framing

**Status: Author-decision. Untouched by design.**

The existing `[COWORK: confirm framing]` flag on the ribosomal/translation sentence is
preserved verbatim. The underlying tension is unchanged: the theme is not significant at the
top 50 or top 100 under the 12-month-inclusive SHAP ranking, but *is* significant at the top
100 (adj p=0.020) under the privileged without-12m condition. Which condition the paper
presents is a framing decision.

## 5. Corrupted R scripts

**Status: Done.**

`phase2/phase2_02_cox_model.R` and `validation/05_batch_correction.R` were genuinely
un-runnable. An earlier non-ASCII strip had left ASCII residue — em-dashes reduced to `"'`
inside `cat()` string literals, which silently terminated the string and swallowed following
code. `rerun_log_R2.txt` / `rerun_log_R3.txt` show both attempts halting at
`Error: unexpected string constant`.

Both files rewritten to clean ASCII comments and printed strings, UTF-8 **without BOM**, LF
endings.

| File | Changed lines | All comment / `cat()` only | Lexical check before | after |
|---|---|---|---|---|
| `phase2_02_cox_model.R` | 44 | yes | FAIL (unterminated string L201, 2 unclosed parens) | **PASS** |
| `05_batch_correction.R` | 4 | yes | FAIL (unterminated string L273, 1 unclosed paren) | **PASS** |

Call-site counts identical across both files before and after: `coxph` 1, `survfit` 1,
`survdiff` 1, `cox.zph` 1, `ggsave` 1, `write.csv` 8, `quantile` 1, `ComBat` 16, `log1p` 3,
`predict(` 1. **No computational logic changed.**

**Caveat — verification is partial.** There is no R in this environment, so
`Rscript -e 'parse(...)'` could not be run. Verification was a quote/comment/bracket-aware
lexical scan that correctly fails both originals and passes both cleaned files. A real
`parse()` on your machine is still worth doing.

## 6. Version pin and tidy

**Status: Done, with one deliberate deviation.**

- `requirements.txt`: the conflicting `scikit-learn>=1.5.0` line is removed and
  `scikit-learn==1.9.0` is now the sole, authoritative pin, with a comment explaining that
  Table 2 depends on it.
- All five output CSVs exist and are current (2026-08-19 23:51 → 2026-08-20 00:04).
- **`cox_quick.R` was NOT deleted.** See below.

## 7. Commits

**Status: Done. Nothing pushed.**

```
601b11e  Hygiene: docs, config, project log consolidation, directory map      13 files
13bdb28  Add Enhancement 3/4/5 and SHAP/CV evidence files                    134 files
5b78069  Persist manuscript-cited numbers to CSV; add regenerated outputs     15 files
34f0818  Correct Table 2 AUCs, add run provenance, pin scikit-learn==1.9.0    12 files
```

`_tmp_LUAD_data` and `_tmp_COADREAD_data` remain untracked and ignored. `Rplots.pdf` is left
untracked as an incidental R device artefact. Working tree is otherwise clean.

---

## Findings that contradict the brief

Three things did not match the assumptions in the task, and were not papered over.

### A. `cox_quick.R` is load-bearing, not a throwaway — so it was kept

`phase2/phase2_02_cox_model.R` **never completed**. It halted on the encoding fault before
reaching its own write of `cox_summary_stats.csv` at line 195. The file on disk has header
`"c_index","logrank_p"` and 1 data row — the shape `cox_quick.R` writes, not the 6-row
`metric,value,manuscript_value` shape `phase2_02` writes. Its mtime (00:04:59) matches
`cox_quick.R`'s.

So `cox_quick.R` is currently the **only provenance** for the manuscript's C-index 0.570 and
log-rank p 0.023. Deleting it would have destroyed that with nothing to replace it. It is
retained with an explanatory header. The encoding fault is now fixed, so:

```powershell
& "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" phase2\phase2_02_cox_model.R
```

should now run end to end and regenerate `cox_summary_stats.csv` properly. Delete
`cox_quick.R` after that, not before.

Worth a look while you are there: `cox_quick.R` fits the model from the pre-existing
`cox_patients_with_risk.csv` handoff file rather than rebuilding the cohort from source.
Same covariates and the numbers are plausible, but it is not a byte-identical path to
`phase2_02`, so the 0.570 / 0.023 pair should be treated as provisional until `phase2_02`
regenerates them.

### B. `km_risk_groups.png` was never regenerated

Still **1,337 bytes, dated 2026-06-25** — the broken file. `phase2_02_cox_model.R` halted long
before its `ggsave` at line 171. Re-running the now-repaired script is what fixes this; it
could not be confirmed from here.

### C. Commit 3 is 134 files, not 77

94 newly added plus 40 modified. The extra files are the regenerated `multi_cancer` ablation
outputs for LUAD and COADREAD and the modified `phase2/outputs` importance and gene-list
files, which were uncommitted and belong with the same evidence base. Nothing outside the
project tree was staged.

---

## Still open — author-level

1. **Variance-ratio re-argument (3.70 vs ~1.00)** — with Lockhart. The largest open item: an
   Abstract-level claim currently rests on a figure the code contradicts.
2. **Ribosome framing decision** — which 12-month condition the paper presents.
3. **Accept or adjust the tracked changes** in `PLOS_CompBio_Draft_Chintala_v1_redline.docx`.
   Nothing has been accepted.
4. **Re-run `phase2_02_cox_model.R`**, then delete `cox_quick.R` and confirm
   `km_risk_groups.png` renders at full size.
5. **filter-repo + force-push** — coordinate with JOSS first (below).
6. **Out-of-scope authorial items** carried forward from the audit:
   - add Ambroise & McLachlan 2002 and Whalen 2022 to the leakage discussion
   - rescale the purity HR interpretation
   - add a multiplicity note
   - confirm the Findings 1–3 fold-in and the venue decision with Lockhart

---

## filter-repo + force-push — NOT RUN

> **Coordinate with JOSS before running this.** Force-pushing rewrites commit hashes, and the
> JOSS review references a specific hash. Rewriting it without telling the editor breaks the
> review's link to the code under review. Agree the change with the editor first, then run.

```bash
# 0. Full backup first. This is irreversible.
cd C:\PROJECTS
git clone --mirror ovarian-cancer-platinum-response ovarian-backup-$(date +%Y%m%d).git

cd ovarian-cancer-platinum-response
git checkout fixes-2026-07-20

# 1. Confirm what you are stripping and how big it is.
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3>10000000 {print $3, $4}' | sort -rn | head -20

# 2. Strip the raw TCGA staging directories from all history.
pip install git-filter-repo
git filter-repo --force \
  --path multi_cancer/outputs/_tmp_LUAD_data \
  --path multi_cancer/outputs/_tmp_COADREAD_data \
  --invert-paths

# 3. filter-repo drops the remote. Re-add it.
git remote add origin <ORIGIN_URL>

# 4. Verify BEFORE pushing: history, size, and that the paths are gone.
git log --oneline -12
git count-objects -vH
git log --all --oneline -- multi_cancer/outputs/_tmp_LUAD_data   # expect empty

# 5. Force-push only after the JOSS editor has agreed.
git push --force-with-lease origin fixes-2026-07-20

# 6. Tell every collaborator to re-clone. Old clones cannot merge cleanly
#    across a rewritten history.
```
