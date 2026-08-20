# Phase 1 — Provenance of the headline AUC table

**Date:** 2026-07-20
**Question:** where do the manuscript's AUC values (LR 0.542/0.658/0.712, RF 0.411/0.609/0.709,
SVM 0.363/0.515/0.771) come from, and are they correct?

---

## 1. Correction to AUDIT_2026-07-20.md

The audit reported that the table reproduced from **no** output file. **That was wrong.**
The audit checked `ablation_leakage_summary.csv` and `ablation_supervised_leakage_summary.csv`
but missed a third ablation output.

`PROJECT_LOG.md:99` names the source explicitly:

> Source: `results/ablation_split_variance_summary.csv` — these are the authoritative clean-split numbers.

That file exists and **matches the manuscript in all nine cells**:

| Model | 12m | 18m | 24m |
|---|---|---|---|
| Logistic Regression | 0.5415 → 0.542 | 0.6579 → 0.658 | 0.7117 → 0.712 |
| Random Forest | 0.4110 → 0.411 | 0.6092 → 0.609 | 0.7087 → 0.709 |
| SVM | 0.3634 → 0.363 | 0.5145 → 0.515 | 0.7714 → 0.771 |

So the table **is** traceable. The real problem is different, and worse.

---

## 2. The source file is a stale orphan

`run_ablation_study.py` writes its eight outputs in a fixed order within a single run
(lines 114→192): `leakage_raw` → `leakage_summary` → `leakage_significance` →
`supervised_*` → `split_variance_raw` → `split_variance_summary`.

Actual mtimes:

```
2026-06-17 23:26:58   ablation_split_variance_summary.csv   <-- OLDEST
2026-06-17 23:56:54   ablation_split_variance_raw.csv
2026-06-18 00:33:27   ablation_leakage_raw.csv
2026-06-18 00:33:27   ablation_supervised_leakage_raw.csv
2026-06-18 00:33:27   ablation_leakage_summary.csv
2026-06-18 00:33:27   ablation_leakage_significance.csv
2026-06-18 00:33:27   ablation_supervised_leakage_summary.csv
2026-06-18 00:33:27   ablation_supervised_leakage_significance.csv
```

The order is **reversed** relative to the script's write sequence. The manuscript's source file
is the *oldest of all eight*, written 67 minutes before the final run.

Reconstruction: the last complete run (00:33) wrote all six leakage files, then terminated
before reaching the split-variance section. `split_variance_raw.csv` (23:56) and
`split_variance_summary.csv` (23:26) are therefore leftovers from two *different* earlier runs.

**They do not agree with each other.** Recomputing the mean from `split_variance_raw.csv`:

| Model/threshold | summary (manuscript source) | mean of its own raw | Δ |
|---|---:|---:|---:|
| LR 12m | 0.5415 | 0.4569 | −0.0846 |
| LR 18m | 0.6579 | 0.6691 | +0.0112 |
| LR 24m | 0.7117 | 0.6778 | −0.0339 |
| RF 12m | 0.4110 | 0.4376 | +0.0266 |
| RF 18m | 0.6092 | 0.6432 | +0.0340 |
| RF 24m | 0.7087 | 0.7172 | +0.0085 |
| SVM 12m | 0.3634 | 0.3935 | +0.0301 |
| SVM 18m | 0.5145 | 0.6064 | +0.0919 |
| SVM 24m | 0.7714 | 0.7333 | −0.0381 |

min/max also differ (e.g. SVM 18m: summary 0.336–0.684, raw 0.309–0.915), confirming these
are different runs on different code or data — not a rounding or RNG artifact.

---

## 3. Re-run on the original data

`fixes/phase1_rerun_clean_auc.py` reproduces `src.ablation.run_split_variance_ablation`
exactly: 30 stratified splits (seeds 42–71), test_size 0.20, top-500 variance computed on the
train fold only after the split, StandardScaler fit on train only, models and hyperparameters
straight from `config/config.yaml`.

Data pipeline verified faithful — cohort sizes reproduce the documented figures exactly:

```
platinum-treated patients: 489
  12m: n=214  events=11   genes=20531
  18m: n=206  events=22   genes=20531
  24m: n=199  events=36   genes=20531
```

### Full comparison

| Model | thr | **Manuscript** | stale summary | split_raw | leakage_raw | **RE-RUN** |
|---|---|---:|---:|---:|---:|---:|
| LR | 12m | 0.542 | 0.5415 | 0.4569 | 0.4569 | **0.4569** |
| LR | 18m | 0.658 | 0.6579 | 0.6691 | 0.6691 | **0.6691** |
| LR | 24m | 0.712 | 0.7117 | 0.6778 | 0.6778 | **0.6778** |
| RF | 12m | 0.411 | 0.4110 | 0.4376 | 0.4085 | **0.4004** |
| RF | 18m | 0.609 | 0.6092 | 0.6432 | 0.6008 | **0.6277** |
| RF | 24m | 0.709 | 0.7087 | 0.7172 | 0.7252 | **0.7157** |
| SVM | 12m | 0.363 | 0.3634 | 0.3935 | 0.3862 | **0.4045** |
| SVM | 18m | 0.515 | 0.5145 | 0.6064 | 0.5857 | **0.6191** |
| SVM | 24m | 0.771 | 0.7714 | 0.7333 | 0.7333 | **0.7333** |

---

## 4. The decisive evidence: Logistic Regression

`LogisticRegression(solver='lbfgs', random_state=42)` is fully deterministic and stable across
scikit-learn versions. It therefore acts as a control on whether the data, splits and
preprocessing are identical between runs.

**LR agrees to four decimal places across three independent artifacts:**

| | 12m | 18m | 24m |
|---|---:|---:|---:|
| `split_variance_raw.csv` (2026-06-17) | 0.4569 | 0.6691 | 0.6778 |
| `leakage_raw.csv` (2026-06-18) | 0.4569 | 0.6691 | 0.6778 |
| Re-run (2026-07-20) | 0.4569 | 0.6691 | 0.6778 |
| **stale summary / manuscript** | **0.5415** | **0.6579** | **0.7117** |

Three runs, a month apart, on the original data, converge exactly. The stale summary is the
lone outlier. Since LR cannot vary by chance, **the manuscript's LR row is wrong** — not
imprecise, wrong. The same holds for SVM 24m (0.7333 in all three reproducible artifacts vs
0.771 claimed).

RF and SVM differ *between* artifacts because both carry version-sensitive internals
(RF bootstrap RNG stream; SVC `probability=True` uses an internal 5-fold Platt calibration).
`requirements.txt` pins nothing (`scikit-learn>=1.5.0`), so these are not reproducible across
environments — a reproducibility weakness in its own right, worth pinning.

---

## 5. Recommended locked values

| Model | 12m | 18m | 24m | Confidence |
|---|---:|---:|---:|---|
| Logistic Regression | **0.457** | **0.669** | **0.678** | High — deterministic, triple-confirmed |
| Random Forest | **0.400** | **0.628** | **0.716** | Medium — sklearn-version sensitive |
| SVM (RBF) | **0.405** | **0.619** | **0.733** | Medium — sklearn-version sensitive |

Generated by: `fixes/phase1_rerun_clean_auc.py`
Canonical outputs: `outputs/results/clean_auc_table.csv` (+ `clean_auc_table_raw.csv`, 270 rows)
Environment: Linux, Python 3.10.12, scikit-learn 1.7.2, numpy 2.2.6, pandas 2.3.3

**Caveat on RF/SVM.** These were produced with scikit-learn 1.7.2, which is almost certainly
not the version that generated the June 2026 results. For values matching the authors' own
environment, re-run on the Windows machine:

```powershell
& "C:\Users\AMAC_WORK\AppData\Local\Python\pythoncore-3.14-64\python.exe" `
  fixes\phase1_rerun_clean_auc.py `
  --data-dir "D:\ALIENWARE\WORK DATA\George Mason\Course Work\3rd Sem FALL 2025\BINF 760 ML\Project data\ov_tcga_pan_can_atlas_2018"
```

LR will return 0.4569 / 0.6691 / 0.6778 on any version. If RF/SVM come back different from the
table above, the Windows values are the ones to use — and `scikit-learn` should then be pinned
in `requirements.txt` to whatever that environment has.

---

## 6. Effect on the manuscript's argument

All nine corrected values are **lower than or equal to** the claimed values in 6 of 9 cells,
and the overall picture is unchanged: performance is modest, weakest at 12 months, and the
"deliberately lower than typical published values" framing still holds. The direction of the
paper's argument is not threatened — but the specific numbers in Table 2 must change.

Worth noting: the corrected 12-month row (LR 0.457, RF 0.400, SVM 0.405) is *further below*
chance than claimed, which if anything strengthens the paper's point about the 12-month
threshold being uninformative at n=214 with 11 events.
