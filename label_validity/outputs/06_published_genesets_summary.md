# A6 — published gene sets as fixed inputs (supplementary)

sklearn 1.9.0; 251 platinum-treated patients with RNA-seq; null = 1000 random same-size sets from 15484 common genes. Evaluates the gene LISTS in this pipeline; not a reproduction of either paper's pipeline.

## LR vs random gene sets (BH across 12 tests)

```
   gene_set          label        endpoint  auc_lr  null_median  null_p95  n_null  p_emp  q_bh  better_than_random
Chen2022_10 label_platinum      E1_tcga_cv   0.735        0.500     0.599    1000  0.001 0.006                True
Chen2022_10 label_platinum      E2_geo_dfs   0.499        0.525     0.628    1000  0.645 0.705               False
Chen2022_10 label_platinum E3_geo_clinical   0.530        0.526     0.684    1000  0.493 0.705               False
Chen2022_10 label_pfiplat6      E1_tcga_cv   0.687        0.521     0.608    1000  0.001 0.006                True
Chen2022_10 label_pfiplat6      E2_geo_dfs   0.485        0.529     0.640    1000  0.754 0.754               False
Chen2022_10 label_pfiplat6 E3_geo_clinical   0.514        0.541     0.706    1000  0.603 0.705               False
  Gao2025_5 label_platinum      E1_tcga_cv   0.537        0.498     0.604    1000  0.271 0.705               False
  Gao2025_5 label_platinum      E2_geo_dfs   0.501        0.513     0.624    1000  0.567 0.705               False
  Gao2025_5 label_platinum E3_geo_clinical   0.492        0.520     0.694    1000  0.590 0.705               False
  Gao2025_5 label_pfiplat6      E1_tcga_cv   0.517        0.511     0.608    1000  0.461 0.705               False
  Gao2025_5 label_pfiplat6      E2_geo_dfs   0.521        0.524     0.628    1000  0.520 0.705               False
  Gao2025_5 label_pfiplat6 E3_geo_clinical   0.486        0.536     0.703    1000  0.646 0.705               False
```

## All models, published sets only (descriptive)

```
endpoint                                        E1_tcga_cv  E2_geo_dfs  E3_geo_clinical
gene_set    label          model                                                       
Chen2022_10 label_pfiplat6 Logistic Regression       0.687       0.485            0.514
                           Random Forest             0.646       0.541            0.470
                           SVM                       0.645       0.482            0.536
            label_platinum Logistic Regression       0.735       0.499            0.530
                           Random Forest             0.716       0.575            0.541
                           SVM                       0.676       0.503            0.536
Gao2025_5   label_pfiplat6 Logistic Regression       0.517       0.521            0.486
                           Random Forest             0.492       0.435            0.451
                           SVM                       0.486       0.586            0.516
            label_platinum Logistic Regression       0.537       0.501            0.492
                           Random Forest             0.508       0.463            0.504
                           SVM                       0.451       0.422            0.430
```

## Predictions vs observed

- P1 Chen, E1, platinum: AUC 0.735 vs random median 0.500 (95th pct 0.599), p = 0.001, q = 0.006 (predicted p < 0.05)
- P2 Chen, E2, platinum: AUC 0.499 vs random median 0.525 (95th pct 0.628), p = 0.645, q = 0.705 (predicted p ≥ 0.05)
- P3 Gao, E1, platinum: AUC 0.537 vs random median 0.498 (95th pct 0.604), p = 0.271, q = 0.705 (predicted p ≥ 0.05)
- P4 Gao, E2, platinum: AUC 0.501 vs random median 0.513 (95th pct 0.624), p = 0.567, q = 0.705 (predicted p ≥ 0.05)
- P5 random-set median E1 AUC, platinum: size 5 0.498, size 10 0.500 (predicted 0.50–0.58)
- P6 max published-set LR AUC on any endpoint: 0.735 (predicted ≤ 0.75)

## Decision rule (BH q < 0.05)

- Chen2022_10 / label_platinum / E1_tcga_cv: **better than random gene sets of the same size**
- Chen2022_10 / label_platinum / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Chen2022_10 / label_platinum / E3_geo_clinical: not distinguishable from random gene sets of the same size
- Chen2022_10 / label_pfiplat6 / E1_tcga_cv: **better than random gene sets of the same size**
- Chen2022_10 / label_pfiplat6 / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Chen2022_10 / label_pfiplat6 / E3_geo_clinical: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_platinum / E1_tcga_cv: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_platinum / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_platinum / E3_geo_clinical: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_pfiplat6 / E1_tcga_cv: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_pfiplat6 / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_pfiplat6 / E3_geo_clinical: not distinguishable from random gene sets of the same size
## Post-run notes (added after the run; header predictions unchanged)

Run by Aaron on the host (sklearn 1.9.0), 2026-10-29 ~17:05 ET. One pre-run design fix: null pool restricted to genes with complete data (15,484 of 15,994), after a 20-draw VM smoke test hit NaN values; smoke-test results were not inspected.

### Scorecard
- P1 held: Chen set within TCGA, platinum label, LR AUC 0.735 vs random median 0.500 (95th pct 0.599); p = 0.001 (no random set reached it), q = 0.006. Same for PFI-from-platinum: 0.687, q = 0.006.
- P2 held: Chen set on GSE63885 dfs 0.499 (random median 0.525), q = 0.705; clinical label 0.530, q = 0.705.
- P3, P4 held: Gao set not distinguishable from random on any endpoint (LR AUC 0.49–0.54; all q = 0.705).
- P5 held for size 10 (0.500), missed narrowly for size 5 (0.498 vs predicted 0.50–0.58).
- P6 held: max published-set LR AUC 0.735 (≤ 0.75).

### Reading (wording for the supplement)
- Chen's 10 genes separate platinum-resistant from sensitive TCGA patients far better than random 10-gene sets (0.735, above A5's 500-gene ceiling of 0.634), yet are at chance on GSE63885 (0.499; random sets 0.525). This within-cohort-only pattern is what gene selection on overlapping patients produces; Chen et al. selected the genes on TCGA-OV patients with a PFI-based label using the full labelled set. Patient overlap cannot be verified (IDs not published), so state the pattern and the design fact, not a cause.
- Gao's 5 genes carry no signal distinguishable from random sets in TCGA or GSE63885 in this pipeline.
- Scope sentence (required): these results describe the gene lists as fixed inputs to this pipeline; they are not a reproduction of either study and do not address the performance those studies report.
