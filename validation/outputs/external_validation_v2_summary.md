# Corrected external validation (GSE63885)

sklearn 1.7.2; common genes 15994; predictions in script header.

| variant   |   threshold_m | model               | label    |   n |   n_nonresponder |    auc |   ci_lo |   ci_hi | ci_excludes_half   |
|:----------|--------------:|:--------------------|:---------|----:|-----------------:|-------:|--------:|--------:|:-------------------|
| P         |            12 | Logistic Regression | clinical |  74 |               10 | 0.5063 |  0.3188 |  0.6953 | False              |
| P         |            12 | Logistic Regression | dfs      |  74 |               34 | 0.536  |  0.4065 |  0.6684 | False              |
| P         |            12 | Random Forest       | clinical |  74 |               10 | 0.5023 |  0.3218 |  0.6696 | False              |
| P         |            12 | Random Forest       | dfs      |  74 |               34 | 0.5324 |  0.4    |  0.6691 | False              |
| P         |            12 | SVM                 | clinical |  74 |               10 | 0.5641 |  0.3671 |  0.7563 | False              |
| P         |            12 | SVM                 | dfs      |  74 |               34 | 0.4985 |  0.3515 |  0.6383 | False              |
| S         |            12 | Logistic Regression | clinical |  74 |               10 | 0.5703 |  0.3843 |  0.7469 | False              |
| S         |            12 | Logistic Regression | dfs      |  74 |               34 | 0.5897 |  0.4537 |  0.7184 | False              |
| S         |            12 | Random Forest       | clinical |  74 |               10 | 0.6312 |  0.4805 |  0.7727 | False              |
| S         |            12 | Random Forest       | dfs      |  74 |               34 | 0.5625 |  0.4301 |  0.689  | False              |
| S         |            12 | SVM                 | clinical |  74 |               10 | 0.5297 |  0.3625 |  0.6985 | False              |
| S         |            12 | SVM                 | dfs      |  74 |               34 | 0.5676 |  0.4331 |  0.6941 | False              |
| P         |            18 | Logistic Regression | clinical |  74 |               10 | 0.5078 |  0.2984 |  0.7203 | False              |
| P         |            18 | Logistic Regression | dfs      |  74 |               34 | 0.5809 |  0.4522 |  0.7155 | False              |
| P         |            18 | Random Forest       | clinical |  74 |               10 | 0.4805 |  0.2914 |  0.6586 | False              |
| P         |            18 | Random Forest       | dfs      |  74 |               34 | 0.5765 |  0.4448 |  0.7092 | False              |
| P         |            18 | SVM                 | clinical |  74 |               10 | 0.55   |  0.3562 |  0.7345 | False              |
| P         |            18 | SVM                 | dfs      |  74 |               34 | 0.5449 |  0.4132 |  0.675  | False              |
| S         |            18 | Logistic Regression | clinical |  74 |               10 | 0.5328 |  0.3109 |  0.7516 | False              |
| S         |            18 | Logistic Regression | dfs      |  74 |               34 | 0.525  |  0.3926 |  0.6581 | False              |
| S         |            18 | Random Forest       | clinical |  74 |               10 | 0.4977 |  0.3093 |  0.7009 | False              |
| S         |            18 | Random Forest       | dfs      |  74 |               34 | 0.4485 |  0.3187 |  0.5751 | False              |
| S         |            18 | SVM                 | clinical |  74 |               10 | 0.5422 |  0.3515 |  0.7266 | False              |
| S         |            18 | SVM                 | dfs      |  74 |               34 | 0.5485 |  0.4169 |  0.6802 | False              |
| P         |            24 | Logistic Regression | clinical |  74 |               10 | 0.5047 |  0.3    |  0.7125 | False              |
| P         |            24 | Logistic Regression | dfs      |  74 |               34 | 0.6221 |  0.4971 |  0.7471 | False              |
| P         |            24 | Random Forest       | clinical |  74 |               10 | 0.5148 |  0.35   |  0.6797 | False              |
| P         |            24 | Random Forest       | dfs      |  74 |               34 | 0.6735 |  0.5478 |  0.7938 | True               |
| P         |            24 | SVM                 | clinical |  74 |               10 | 0.575  |  0.3656 |  0.7579 | False              |
| P         |            24 | SVM                 | dfs      |  74 |               34 | 0.6096 |  0.4787 |  0.7346 | False              |
| S         |            24 | Logistic Regression | clinical |  74 |               10 | 0.6031 |  0.3688 |  0.8172 | False              |
| S         |            24 | Logistic Regression | dfs      |  74 |               34 | 0.5949 |  0.4603 |  0.7294 | False              |
| S         |            24 | Random Forest       | clinical |  74 |               10 | 0.5516 |  0.325  |  0.7672 | False              |
| S         |            24 | Random Forest       | dfs      |  74 |               34 | 0.5463 |  0.4114 |  0.6801 | False              |
| S         |            24 | SVM                 | clinical |  74 |               10 | 0.5469 |  0.3437 |  0.7469 | False              |
| S         |            24 | SVM                 | dfs      |  74 |               34 | 0.6118 |  0.4779 |  0.7419 | False              |
