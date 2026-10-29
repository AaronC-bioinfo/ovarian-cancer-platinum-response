# G5 — How published expression classifiers labelled platinum response in ovarian cancer (Table 1 source data)

> **Main-session verification (2026-10-29).** Spot-checked against publisher HTML in a separate fetch: Gao 2025 "71 classified as sensitive and 333 classified as resistant", the 404 = 287 + 117 pooling, the 8:2 split and AUCs 1 / 0.993 / 0.989 — match. Chen 2022 PFI definition, "212 out of 230 samples (161 sensitivity vs. 51 resistance)", sensitivity/specificity "1 and 0.839", PPV "0.899", validation "41sensitivity vs. 30 resistance" and "34 resistant and 41sensitive" — match; 51/69 = 0.739 ≠ 0.839 confirmed. Li 2022 "287 of which had known platinum sensitivity" and absence of a cutoff — match. Other quotes not yet re-checked; joined quotes (fetch returns ≤125-char pieces) still need a PDF check before printing.
>
> **Cross-reference to our data (label_validity/outputs/gate_g2_platinum_sources.csv, row all_patients):** cBioPortal ov_tcga_pub `PLATINUM_STATUS` is Resistant or Sensitive for exactly **287** patients (90 R / 197 S) — the same TCGA n reported by Li 2022 and Gao 2025. This suggests, but does not prove, that both used this field. With 197 sensitive in TCGA alone, Gao's pooled "71 sensitive / 333 resistant" (n = 404) cannot be correct as printed; the class names appear swapped. Report as an internal inconsistency, not an accusation (rule 5).


Compiled 2026-10-29. Each item was taken from the full text of the article (publisher HTML or the NCBI PMC-OA BioC full-text service). Nothing was filled in from abstracts alone except where an item is explicitly marked "Abstract".

**How the quotes were captured.** Every quote was pulled from the live full text by a fetch tool that returns verbatim passages capped at about 125 characters. Some longer sentences therefore came back in consecutive pieces. Where I joined pieces, the join is marked `[…]` if any words in between may be missing. Before the table goes to press, spot-check the joined quotes against the publisher PDF. I could not record page numbers because every source was HTML or XML. Locations are given as section headings, figure or table numbers, or "Abstract".

Conventions:
- **not stated**: the full text I read does not give this item.
- **not reachable**: the item is in a supplement or file I could not retrieve.
- **[my arithmetic]**: a check I computed myself. It is not a claim made by the paper.

---

## 1. Compact summary table (paper × cohort)

| Ref | Paper | Cohort (role) | Label name (as used) | Label source / field | n per class (as reported) | Design (split / CV / selection) | AUC reported |
|---|---|---|---|---|---|---|---|
| 2 | Chen 2022 J Ovarian Res | TCGA-OV (training) | platinum-sensitive / platinum-resistant | "clinical platinum response status" after barcode matching. Rule stated: PFI > 6 mo sensitive, PFI < 6 mo resistant. TCGA field name: **not stated**. Portal: **not stated** | 69 resistant / 161 sensitive (n = 230) | No held-out split; trained on all 230. DEGs (limma) and RF feature selection (OOB) on the full 230. e1071 SVM, sigmoid kernel, "parameters were selected by 100-fold cross-validation" | 0.971 ("average AUC"), training |
| 2 | Chen 2022 | GSE63885 (external validation; also spelled "GSE638855") | same | "having platinum response status". GEO field: **not stated** | Methods: 34 resistant / 41 sensitive (n = 75). Results: "41sensitivity vs. 30 resistance" correctly classified out of 75 | Independent external validation | 0.926 |
| 2 | Chen 2022 | FUSCC (IHC only; not an expression classifier) | resistant / sensitive | not stated beyond the general PFI rule | 20 resistant / 60 sensitive (Results) | IHC validation of hub genes | not applicable |
| 3 | Li 2022 Front Oncol | TCGA-OV (training) | platinum-sensitive / platinum-resistant; "initial platinum resistant (IPR)" | cBioPortal ("transcriptomic and clinical features … derived from the cbioportal website"). Field name: **not stated**. Definition or cut-off: **not stated** | 287 "had known platinum sensitivity" out of 489. Per-class n: **not stated** in main text (refers to Supp. Table S1, **not reachable**) | DEGs (limma, p < 0.01) "from the training cohort". RF, XGBoost and LASSO selection, then 11 shared genes, then multivariate logistic regression. Held-out split: **not stated**. CV: **not stated** | 0.841, training |
| 3 | Li 2022 | GSE15622 (validation, platinum resistance) | platinum sensitivity / IPR | GEO. Field: **not stated**. Definition: **not stated** | 15 samples "with known platinum sensitivity". Per-class n: **not stated** (Supp. Table S1, **not reachable**) | Independent validation | 0.796 |
| 3 | Li 2022 | GSE102073, GSE19829, GSE26712 (survival validation only) | not used as response labels | not applicable | n = 85, 28, 195 (total) | survival / KM only | GSE102073: AUCs 0.67, 0.67, 0.7 for 1-, 3-, 5-yr PFS (survival, not response). Others: none |
| 4 | Gao 2025 Sci Rep | Pooled TCGA-OV + GSE15622 + GSE51373 (train/test, 8:2 random split) | sensitive / resistant | Rule stated (PFI < 6 mo resistant, > 6 mo sensitive), but only in the scRNA-seq section. Source field for bulk TCGA/GEO labels: **not stated**. Data from "xenabrowser TCGA ovarian cancer cohort" and GEO | Pooled 404 = TCGA 287 + GEO 117. "71 classified as sensitive and 333 classified as resistant". Per-cohort per-class n: **not stated** | Rank-In batch integration, then random 8:2 train/test split. "fivefold cross-validation for identifying optimal hyperparameters". Candidate genes from external scRNA-seq (GSE165897, FindMarkers/MAST). Gene number chosen by adding "5 feature genes at a time" to RF. Whether that choice used the training set only: **not stated** | Training: "mean AUC of 1 (fivefold cross validation)". Test: 0.993 |
| 4 | Gao 2025 | GSE63885 (independent validation; also "GSE63855", "GSE64885") | sensitive / resistant | **not stated** | n = 75. Per-class: **not stated** | held out, processed separately | 0.989 |
| 4 | Gao 2025 | GSE165897 (scRNA-seq discovery) | sensitive / resistant patients | "progression-free survival information". The PFI rule appears in this section | per-class patient n: **not stated** | gene discovery only | not applicable |
| 5 | Sun X 2021 Bioengineered | TCGA-OV | none. No response label; "PFS was commonly used as a surrogate of chemotherapy response" | GDC clinical (PFS, OS, grade, stage) | not applicable (240 stage III–IV patients for PFS) | **No classifier trained.** WGCNA plus stemness index (mRNAsi), then key genes. No split, no CV | none |
| 5 | Sun X 2021 | GSE131978 (validation of key genes) | platinum-based chemotherapy-resistant / -sensitive | GEO. Field and definition: **not stated** | 7 resistant / 4 sensitive (stage III–IV) | per-gene differential expression only | none |
| 5 | Sun X 2021 | GSE51373 (validation of key genes) | platinum-resistant / platinum-sensitive | GEO. Field and definition: **not stated** | 10 resistant / 13 sensitive (stage III–IV) | per-gene differential expression only | none |
| 6 | Sun J 2019 Cell Death Dis | Meta-discovery: Dressman, Patch, TCGA (patients) + GSE47856 (cell lines) | resistant / sensitive samples | Patient label definition: **not stated** in main text (Supp. Table 1, **not reachable**). Cell lines: median GI50 | 754 patients (3 cohorts) + 171 cell-line transcriptomes. Per-class n: **not stated**. TCGA n = 557 | No fitted classifier. Top 1000 DEGs (limma) per dataset, then genes in ≥3 of 4 datasets, then 16 genes (6 sensitive + 10 resistant). Rank-based IndividCRS score with cut-off 0. "Cross-validation was used to prevent over-fitting by performing meta-discovery…" (type and folds **not stated**) | none (t-tests, r², HRs only) |
| 6 | Sun J 2019 | Response validation sets: GDSC (cell lines), GSE3149, GSE51373, GSE23554, GSE15709, GSE15622, GSE71340 (+ GSE51088) | resistant / sensitive; pre/post chemotherapy | Patients: **not stated**. GDSC: median GI50 | **not stated** in main text | independent validation by t-test | none |
| 7 | Wang 2025 Open Med | Merged GSE114206 + GSE51373 + GSE63885 (training, "merged group") | platinum-sensitive / resistant | GEO. Field: **not stated**. Only definition is a general Introduction sentence ("recurrence … within 6 months") | GSE114206 6 S / 6 R. GSE51373 16 S / 12 R. GSE63885 41 S / 34 R | sva/limma merge. 45 DEGs and WGCNA (31 overlap), then LASSO, SVM-RFE and RF, then 4 genes. All selection on the merged set (training only, no held-out split): **not stated explicitly**. CV type and folds: **not stated** (Fig. 2 legend mentions SVM-RFE "cross-validation error") | Per-gene: ROR2 0.704, MFAP4 0.716, EFEMP1 0.657, ZBTB7C 0.659 |
| 7 | Wang 2025 | GSE30161 ("testing cohort" in Abstract; "external validation set" in Results) | not stated | **not stated** (absent from Methods) | **not stated** | external validation | ROR2 0.598, MFAP4 0.629, EFEMP1 0.746, ZBTB7C 0.546 |

---

## 2. Per-paper sections (verbatim quotes with locations)

### Ref 2 — Chen S et al. 2022, J Ovarian Res 15:39
Source read: publisher full-text HTML (BMC). PMC returned a CAPTCHA page.

**Label definition** (Methods, *Statistical analyses*):
> "patients were divided into platinum-sensitive and platinum-resistant subgroups according to the platinum-free interval (PFI)."
> "PFI is defined as the time from the end of the first chemotherapy course to disease recurrence, and PFI > 6 months was regarded as platinum-sensitive, whereas PFI < 6 months was the platinum-resistant group."

This matches the known facts in the brief: the label was PFI-based, with PFI < 6 months counted as resistant.

**Source field** (Methods, *OC datasets extraction*):
> "After barcode matching, 230 OC samples possessing clinical platinum response status were obtained, […] comprised of 69 resistant and 161 sensitive samples respectively, which serve as our training dataset."
- Expression and SNP data were "downloaded from TCGA". No portal is named.
- TCGA clinical field name: **not stated**.
- Whether PFI was computed by the authors or read from a TCGA platinum-status field: **not stated**.

**n per class:**
- TCGA: 69 resistant / 161 sensitive / 230 total (Methods, *OC datasets extraction*).
- GSE63885 (Methods, *OC datasets extraction*):
  > "containing a total of 75 samples having platinum response status, […] consisting of 34 resistant and 41sensitive samples, respectively."
- Results, *Construction and validation of the classifier*:
  > "71 samples (41sensitivity vs. 30 resistance) out of 75 samples could be discriminated precisely"
- The 30 is the number of resistant samples correctly classified, set against 34 in Methods. This is the "30" location noted in the brief.

**Gene selection on the full labelled set:**
- Methods, *DEGs identification*:
  > "Significant DEGs were defined as those with adjusted P < 0 .05 and |log FC| ≥1."
- Results:
  > "Via Limma package in R, 1144 DEGs differently expressed (524 downregulated and 620 upregulated)"
- Results:
  > "Integrated with SNP information, we found 48 genes had variant sites" […] "between platinum-resistant and sensitive groups simultaneously."
- Results:
  > "To extract the most representative and feature genes in these 48 genes, the RandomForest algorithm was performed." / "And 10 genes were figured out optimally when the OOB error is minimum (Fig. 3A)."
- Methods (RF):
  > "The model was built on expression levels of genes identified in TCGA samples." / "features of the model with the lowest OOB error rate were selected as the optimal combination."

**Classifier and CV** (Methods, *Development and validation of the SVM classifier*):
> "We used the e1071 R package" […] "using "Sigmoid" as the Kernel and the optimal signature genes as features." / "The parameters were selected by 100-fold cross-validation."

**No held-out split** (Results, *Construction and validation of the classifier*):
> "Based on expression profiles of the above 10 feature genes in the TCGA dataset, we constructed an SVM classifier" / "It was able to accurately distinguish 212 out of 230 samples (161 sensitivity vs. 51 resistance)"

**AUC:**
- Results:
  > "with a precision rate of 92.17% and an average AUC of 0.971"
- Results, validation:
  > "accuracy rate was 94.76% with an AUC of 0.926 (Fig. 3B, dotted line)."
- Abstract:
  > "with an AUC of 0.971 in the training set and of 0.926 in the GEO dataset (GSE638855)."
- Fig. 3 legend:
  > "B The receiver operating characteristic (ROC) curve (area under the curve (AUC) of the TCGA training set (solid line) and GSE63885 validation set (dotted line)"

**Other details:**
- Table 1 ("Clinicopathological characteristics of patients with OC in this study"): only the caption appeared in the HTML I read. The table body was **not reachable**, because the /tables/1 page is robots-disallowed.
- FUSCC IHC cohort (Results):
  > "in the FUSCC cohort, 20 patients were resistant to platinum-based therapy and the other 60 were in the sensitive group."

### Ref 3 — Li Y et al. 2022, Front Oncol 12:847085
Source read: Frontiers full-text HTML, the Frontiers XML and the PDF. PMC returned a CAPTCHA page.

**Label definition: not stated.** I found no cut-off, no PFI and no "6 months" anywhere in the main text (I searched HTML, XML and PDF). The Abstract Background says:
> "nearly 20%–30% of patients with OC are initial platinum resistant (IPR)"

**Source** (Methods, *Data Source*):
> "The transcriptomic and clinical features of 489 patients with ovarian serous cystadenocarcinoma from the TCGA cohort were derived from the cbioportal website (http://www.cbioportal.org/), setting as the training cohort, and 287 of which had known platinum sensitivity."
- cBioPortal field name: **not stated**.

**GSE15622** (Methods, *Data Source*):
> "The GSE15622 dataset, which included 15 ovarian cancer samples with known platinum sensitivity, was downloaded from GEO (https://www.ncbi.nlm.nih.gov/geo/) as the validation cohort of platinum-resistance prediction of IPR signature."

**n per class: not stated** in the main text. The paper says:
> "More details of involved samples in each dataset are provided in Supplementary Table S1." (Methods, *Data Source*)
- DataSheet_1.pdf and DataSheet_2.pdf are listed in the XML, but I could not find a retrievable file URL. **Not reachable.**
- Whether all 287 or a subset trained the model: **not stated**.

**Selection and model:**
- Abstract, Methods:
  > "Differentially expressed genes (DEGs) were selected between platinum-sensitive and platinum-resistant patients from the training cohort, and multiple machine-learning algorithms [including random forest, XGboost, and least absolute shrinkage and selection operator (LASSO) regression] were utilized to determine the candidate genes from DEGs."
- Methods, *DEG screening*:
  > "The DEGs between platinum-sensitive and platinum-resistant samples (median value serves as the cutoff) were identified through the "Limma" package from Bioconductor in R language, and p-value <0.01 was set as the threshold for screening the expression difference of DEGs."
- Results:
  > "Then, 27, 141, and 73 candidate DEGs were further selected by RF, XGBoost, and LASSO, respectively, 11 of which were shared by these three machine learning algorithms"
- Methods:
  > "we applied logistic regression to establish the IPR signature based on the expression"
- Held-out split within TCGA: **not stated**. CV type and folds (including for LASSO, RF or XGBoost): **not stated**.

**AUC:**
- Results, *Establishment*:
  > "This IPR prediction model reached an AUC value of 0.841 to predict IPR in the training cohort"
- Results, *Validation*:
  > "The AUC value for predicting the IPR was 0.796, which indicated the satisfactory performance of the IPR prediction score model." (GSE15622; see Fig. 2 legend)
- Also reported:
  - IPR vs HRD: "AUC, 0.83 vs. 0.65, p=0.035"
  - IPR vs mutation count: "AUC, 0.84 vs. 0.63, p < 0.001" (Results)

### Ref 4 — Gao T, Zhao P, Han S. 2025, Sci Rep 15:19123
Source read: nature.com full-text HTML.

**Label definition.** The section is Results/Methods, *Different gene analysis of cancer cells between platinum-sensitive and platinum-resistant patients*. That is the scRNA-seq section.
> "The Platinum-Free Interval (PFI) is a measure used in clinical practice to assess the duration of response to platinum-based chemotherapy in cancer patients."
> "It is defined as the time elapsed between the last dose of first-line platinum-based chemotherapy […] and the date of tumor progression."
> "Ovarian cancer patients who have a PFI less than 6 months are typically categorized as resistance" […] "patients with a PFI greater than 6 months are categorized as sensitive."

How labels were derived for the bulk TCGA and GEO cohorts: **not stated**. No Xena field is named.
- Data availability: datasets are "available in the GEO" (GSE165897, GSE51373, GSE63885, GSE15622) "and xenabrowser TCGA ovarian cancer cohort."
- GSE165897 is described as one "which includes single-cell transcriptomic data from ovarian cancer patients with progression-free survival information". Per-class patient numbers: **not stated**.

**n.** Section: *Identification of optimal gene combination: high performance of the GPPS model in predicting platinum response*.
> "we conducted a comprehensive data collection, consisting of" … "a total of 404 samples (TCGA ovarian cancer: 287, GEO: 117)" … "there were 71 classified as sensitive and 333 classified as resistant to platinum treatment."
- Methods (*Integration of transcriptome data from different platforms*) lists GSE51373 n = 28, GSE63885 n = 75 and GSE15622 n = 14.
- [my arithmetic] 28 + 75 + 14 = 117. So the pooled 71/333 count appears to include the validation set GSE63885.
- Per-cohort per-class n: **not stated**.

**Design:**
- Split: "were randomly divided into training and testing sets at an 8:2 ratio" (GSE15622, GSE51373 and TCGA OV after Rank-In). GSE63885 was held out.
- CV: "we use fivefold cross-validation for identifying optimal hyperparameters" (same section). The model was then retrained on the full training set.
- Gene selection:
  - Candidates came from scRNA-seq FindMarkers (MAST).
  - "To determine the optimal combination of genes, we sequentially added genes to the Random Forest (RF) model." Genes were added 5 at a time, up to 50.
  - The rank order of the added genes: **not stated**.
  - Whether the choice of gene number used training data only or also the test set: **not stated**.
- Threshold: "Based on the optimal threshold of 0.5, determined through ROC curve analysis on the training set."

**AUC:**
- "a mean AUC of 1 (fivefold cross validation) in the training set"
- 0.993 in the test set
- 0.989 in the validation set (GSE63885)
- Abstract: "an AUC value of 0.993"

### Ref 5 — Sun X et al. 2021, Bioengineered 12:3753–3771
Source read: NCBI PMC-OA BioC full text (PMC8806806). PMC HTML returned a CAPTCHA, Taylor & Francis returned a client error, and Europe PMC was rate-limited.

**This paper does not train an expression classifier and reports no AUC.** It uses WGCNA and the stemness index to find key genes, then checks those genes one by one in two GEO sets.

**TCGA:**
- Results:
  > "PFS was commonly used as a surrogate of chemotherapy response in OC."
- Methods:
  > "Removed the samples with incomplete information of survival time, PFS analyses were conducted on 240 SOC patients of stage III–IV."
- No platinum-response label is applied to TCGA.

**GEO labels** (Methods, *Prognostic and chemotherapeutic response predict the value of key genes*):
> "In addition, GSE131978 [16] and GSE51373 [17] datasets were selected to validate whether the key genes were associated with platinum sensitivity in advanced SOC patients."
> "In GSE131978, a total of 7 platinum-based chemotherapy-resistant SOC samples of stage III–IV and 4 platinum-based chemotherapy-sensitive samples were selected for analysis."
> "In GSE51373, 10 platinum-resistant and 13 platinum-sensitive samples of stage III–IV were also utilized in the validation."

- Label definition and where the response information came from: **not stated**.
- The only threshold in the paper is in the Discussion:
  > "(a platinum-treatment free interval of 6–12 months)"

  This describes "limited platinum sensitivity". It is not stated as the labelling rule.
- Statistical test for GSE131978 and GSE51373: **not stated**. The Fig. 9 legend gives only "'*' indicates p <0.05".

### Ref 6 — Sun J et al. 2019, Cell Death Dis 10:661
Source read: nature.com full-text HTML.

**This paper does not fit a classifier and reports no AUC.** It builds IndividCRS, a within-sample score that contrasts 6 sensitive genes with 10 resistant genes, with a cut-off at 0.

**Datasets** (Methods):
> "A total of 29 public OvCa datasets were analyzed in this study, including three cell line datasets and 26 patient datasets"
> "Of these, 11 OvCa datasets included chemotherapeutic response information and 21 datasets included overall survival (OS) information."
> "the following four large datasets: Dressman, Patch and TCGA (all patient datasets) and the GSE47856 cell line dataset, were selected as a meta-discovery dataset"
> "The remaining 25 individual datasets were used as testing datasets for independent validation."

**Label definition for patients: not stated** in the main text.
- Methods:
  > "Differentially expressed genes between resistant samples and sensitive samples were determined using R package" ("limma")
- Results (cell lines only):
  > "OvCa cell lines treated with cisplatin were divided into resistant and sensitive cell line groups using the median GI50 values."
- Fig. 1 abbreviations: "CR: Complete response; PR: partial response; PD: progression disease; SD: stable disease" *(not re-verified: absent from the fetched publisher text, likely a figure legend; supports no Table 1 cell)*
- Details are in Supplementary Table 1 ("Detailed information about the 29 OvCa datasets"). **Not reachable**: the page gives only #MOESM anchors.

**n:**
- "performing meta-discovery using 754 patients from three cohort studies and 171 transcriptomes from OvCa cell lines" (Results)
- "the TCGA dataset (n = 557), that included patients treated with platinum-based chemotherapy" (Results)
- Per-class n: **not stated**.

**Selection and "CV":**
- Results:
  > "the top 1000 differentially expressed genes were selected as candidate chemotherapy-responsive genes" … "chemotherapy-responsive genes that appeared in at least three of the four datasets in the meta-discovery dataset were selected as candidate robust chemotherapy-responsive genes."
- Results:
  > "Cross-validation was used to prevent over-fitting by performing meta-discovery using 754 patients from three cohort studies and 171 transcriptomes from OvCa cell lines"
- CV type and folds: **not stated**.

**Validation statistics (no AUC):**
- "unpaired t-test; P = 0.001 for GSE3149; P = 0.08 for GSE51373; P = 0.011 for GSE23554"
- GDSC: P = 0.041
- GSE15622 carboplatin: "paired t-test, P = 0.049"
- GSE71340: P = 0.014
- CR probability vs IndividCRS: "Pearson correlation coefficient [r2] = 0.88, P < 0.001"

### Ref 7 — Wang C, Peng C, Xie C. 2025, Open Med (Wars) 20:20241084
Source read: De Gruyter Brill full-text HTML.

**Definition.** This is the only definition in the paper, and it appears in Section 1, *Introduction*, not as a labelling rule:
> "Platinum resistance refers to the recurrence of patients within 6 months of treatment with platinum drugs"

- Cohort-specific definition or source field: **not stated**.

**Data** (Section 2.1, *GEO data download and preprocessing*):
> "The gene expression profiles of GSE114206, GSE51373, and GSE63885 were downloaded from the GEO database."
> "The three GEO series were merged and normalized using the R packages sva and limma"

**n** (Section 3.1, *Identification of platinum-based chemoresistance related geneset*):
> "we extracted RNA level profiles from three datasets: GSE114206 (6 samples of platinum-sensitive and 6 samples of resistant), GSE51373 (16 samples of platinum-sensitive and 12 samples of resistant), and GSE63885 (41 samples of platinum-sensitive and 34 samples of resistant)."
> "These datasets were merged and normalized for subsequent analyses"

**Selection** (all reported on the merged training data; no internal held-out split is described):
- "We screened 45 DEGs between the sensitive and resistant groups (|logFC| > 1.5, p < 0.05)."
- WGCNA blue module: 554 genes. The overlap of DEGs and WGCNA genes is 31.
- "LASSO regression analysis identified 16 variables"
- SVM-RFE: "the error was minimized when the number of features was 16"
- RF: nine genes with importance > 2
- Consensus: "four common signature genes, ROR2, MFAP4, EFEMP1, and ZBTB7C, were identified."
- That DEG analysis ran on the merged dataset is **not stated explicitly**. "For subsequent analyses" is the closest wording.
- Lambda, CV type, CV folds and ntree are absent from Methods. They appear only in the Fig. 2 legend: "Variation curve of gene cross-validation error in SVM-RFE algorithm."

**AUC:**
- Results (merged group): "ROR2, MFAP4, EFEMP1, and ZBTB7C were 0.704, 0.716, 0.657, and 0.659, respectively."
- Section 3.2: "In the external validation set GSE30161, the AUCs for these markers were 0.598, 0.629, 0.746, and 0.546, respectively"
- GSE30161 n and per-class counts: **not stated**.
- Methods: "genes with an area under the curve exceeding 0.60 could potentially offer diagnostic advantages."

---

## 3. "Not stated" cells and internal inconsistencies

### 3a. Every "not stated" / "not reachable" cell

**Ref 2, Chen:**
- TCGA clinical field name and portal
- Whether PFI was computed by the authors or taken from a TCGA field
- GSE63885 label field and definition
- How PFI = exactly 6 months is classified (the rule covers only > 6 and < 6)
- Table 1 body (not reachable)
- RF ntree

**Ref 3, Li:**
- Label definition and cut-off (TCGA and GSE15622)
- cBioPortal field name
- Per-class n for TCGA and GSE15622 (Supp. Table S1 not reachable)
- Whether all 287 trained the model
- Held-out split
- CV type and folds

**Ref 4, Gao:**
- Bulk TCGA and GEO label source and derivation
- Per-cohort per-class n
- Per-class n for scRNA-seq patients
- Rank order for adding genes
- Whether the choice of gene number used training data only

**Ref 5, Sun X:**
- GEO label definitions and source
- Statistical test for the GEO comparisons
- Classifier, CV and AUC: none exist in the paper

**Ref 6, Sun J:**
- Patient label definitions (Supp. Table 1 not reachable)
- Per-class n for every cohort
- n for Dressman, Patch and each GSE set
- CV type and folds
- AUC: none

**Ref 7, Wang:**
- Cohort-specific label definition and source field
- DEG analysis on the merged set (not explicit)
- LASSO, SVM-RFE and RF CV and folds (Methods)
- GSE30161 n, per-class counts and labels (GSE30161 is absent from Methods)

### 3b. Internal inconsistencies

**Ref 2, Chen:**
1. **Accession spelling.** The dataset is "GSE638855" in three places: two in the Abstract (AUC 0.926; "validated in GSE638855 (p = 0.04862)") and one in Results ("TCGA and GSE638855 datasets were displayed in Supplementary Table 5"). It is "GSE63885" everywhere else.
2. **GSE63885 resistant count.** Methods give 34 resistant / 41 sensitive. Results say "71 samples (41sensitivity vs. 30 resistance) out of 75 samples could be discriminated precisely", which is 30 resistant correctly classified.
3. **Validation accuracy.** [my arithmetic] The paper reports "94.76%", but 71/75 = 94.67%.
4. **TCGA specificity.** [my arithmetic] The paper reports "sensitivity and specificity were 1 and 0.839". But 51 of 69 resistant samples correct is 0.739.
5. **Validation PPV.** [my arithmetic] The paper reports PPV "0.899", the same value as in TCGA. But 41/(41 + 4) = 0.911.
6. **"Precision rate" and "average AUC".** "precision rate of 92.17%" equals 212/230 [my arithmetic], which is accuracy, not precision. "average AUC of 0.971" is the training AUC, and the averaging procedure is not stated.

**Ref 3, Li:**
- "11 of which were shared by these three machine learning algorithms" (Results) matches the Abstract.
- No numeric inconsistency was found. Without Supp. Table S1, the class counts cannot be cross-checked.

**Ref 4, Gao:**
1. The accession is spelled "GSE63855" in Methods ("Subsequently, the dataset GSE63855 was independently uploaded…") and "GSE64885" in the Fig. 5 legend. It is "GSE63885" elsewhere.
2. The Fig. 4 legend covers "training set, and independent validation set" and omits the test set, but the text reports a test AUC of 0.993.
3. [my arithmetic] The pooled class counts (71 / 333 of 404) appear to include the held-out validation set GSE63885 (28 + 75 + 14 = 117 GEO).

**Ref 5, Sun X:** none found.

**Ref 6, Sun J:**
- GSE51373 P = 0.08 is reported alongside significant datasets. This is not a contradiction in itself.

**Ref 7, Wang:**
1. The Abstract calls GSE30161 the "testing cohort". Results call it the "external validation set".
2. GSE30161 is used in Results and Fig. 3 but is absent from the Methods dataset list.
3. The Abstract highlights 2 genes (MFAP4, EFEMP1); Results carry 4 signature genes.
4. The single-cell set is written "GES151214" in Results and "GSE151214" elsewhere.

### 3c. Cross-paper discrepancies (same dataset, different counts)

These are not inconsistencies within any one paper.

- **GSE63885:**
  - Chen: 34 R / 41 S
  - Wang: 41 S / 34 R
  - Gao: n = 75, per-class not stated
- **GSE51373:**
  - Sun X: 10 R / 13 S, "stage III–IV" (n = 23)
  - Wang: 16 S / 12 R (n = 28)
  - Gao: n = 28
- **GSE15622:**
  - Li: 15 samples "with known platinum sensitivity"
  - Gao: n = 14

---

## 4. Appendix — TCGA Research Network 2011 (Nature 474:609–615) PLATINUM STATUS definitions

**Result: the defining text for the categories "Resistant", "Sensitive", "Tooearly" and "Missing" was not reachable from a primary source in this session.**

**What the main text says.** Source: NCBI PMC-OA BioC full text, PMC3163504. This copy ended partway through Table 1 and does not include the Supplementary Information.
- Introduction:
  > "After therapy, platinum resistant cancer recurs in approximately 25% of patients within 6 months and overall 5-year survival is 31%."
- *Samples and clinical data*:
  > "HGS-OvCa specimens were surgically resected before systemic treatment but all patients received a platinum agent and 94% received a taxane."
- *Samples and clinical data*:
  > "Twenty five percent of the patients remained free of disease and 45% were alive at the time of last follow-up, while 31% progressed within 6 months after completing platinum-based therapy."
- *Samples and clinical data*:
  > "Clinical data were current as of August 25, 2010."
- The main text does **not** define the platinum-status categories. It sends readers to Methods S1 and Table S1.1 in the Supplementary Information for clinical details.
- The strings "too early", "Tooearly", "refractory", "platinum-free" and "missing" do not occur in the main text.

**Supplementary Information (Methods S1, clinical data section): not reachable.** URLs tried:
- https://www.nature.com/articles/nature10166 (client error)
- http://www.nature.com/nature/journal/v474/n7353/full/nature10166 (client error)
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3163504/supplementaryFiles (rate-limited twice, with requests about 2 minutes apart)
- https://api.gdc.cancer.gov/data/945fd4d0-b015-4203-adac-04d39f89fa9e: this is the GDC-hosted clinical Table S1.2 as HTML. It came back as binary and was unreadable, and direct download of the .xlsx version (…/e0d199f4-64ee-4795-977c-9e9b233f6338) was blocked by the egress proxy.
- https://gdc.cancer.gov/about-data/publications/ov_2011: the publication page. It lists the files but does not define platinum status.
- pmc.ncbi.nlm.nih.gov returned a reCAPTCHA page for every PMC article URL in this session.

**Secondary sources:** none verified. No definition from a secondary paper is given here.

**Next step:** open the Nature SI PDF (Methods S1) or the Table S1.2 header notes in a normal browser and quote the definitions directly.

---

## 5. URLs used

**Ref 2 (Chen):**
- https://ovarianresearch.biomedcentral.com/articles/10.1186/s13048-022-00969-3 (full text, read)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8973612 (CAPTCHA)
- …/tables/1 (robots-disallowed)

**Ref 3 (Li):**
- https://www.frontiersin.org/articles/10.3389/fonc.2022.847085/full (read)
- https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2022.847085/pdf (read)
- https://public-pages-files-2025.frontiersin.org/journals/oncology/articles/10.3389/fonc.2022.847085/xml (read)

**Ref 4 (Gao):**
- https://www.nature.com/articles/s41598-025-99930-9 (read)

**Ref 5 (Sun X):**
- https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC8806806/unicode (full text, read)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8806806 (CAPTCHA)
- https://www.tandfonline.com/doi/full/10.1080/21655979.2021.1939514 (client error)
- https://www.tandfonline.com/doi/pdf/10.1080/21655979.2021.1939514 (client error)
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8806806/fullTextXML (rate-limited)
- https://europepmc.org/article/PMC/PMC8806806 (client error)
- https://researchexchange.ocrahope.org/papers/21655979-2021-1939514 (abstract only, not used)

**Ref 6 (Sun J):**
- https://www.nature.com/articles/s41419-019-1874-9 (read)

**Ref 7 (Wang):**
- https://www.degruyterbrill.com/document/doi/10.1515/med-2024-1084/html (read)

**TCGA 2011:**
- https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC3163504/unicode (main text, read)
- The SI URLs tried are listed in Section 4.

---

## 6. Update from local supplements (main session, 2026-10-29, ~16:20 ET)

Files in `C:\PROJECTS\OV Data\Project data\Literature\`, read locally.

- **Li 2022, Data Sheet 2** (TCGA column): "Platinum_status Sensitive 197 / Resistant 90"; GSE15622: "Sensitive 9 / Resistant 6"; footnote "*Samples treated with paclitaxel monotherapy were not included in this analysis". Data Sheet 1 (flow chart): "TCGA-OV dataset (samples with both known platinum-sensitivity status and RNA-seq data, n=287)". → Fills Li's per-class cells. The 197/90 split equals TCGA 2011 `PlatinumStatus` exactly (see `label_validity/PLATINUM_STATUS_definition.md`): Li's TCGA label is the TCGA 2011 platinum status.
- **Sun J 2019, Supplementary Table 1** (`41419_2019_1874_MOESM1_ESM.xlsx`): TCGA listed as "Patient / Discovery / HG-U133A / 557 / chemo-response information YES"; Patch 80, Dressman 117 (discovery); GSE51373 28, GSE15622 35, GSE23554 28, GSE3149 108, GSE71340 35 (testing, chemo-response YES); GSE63885 101 listed with chemo-response "NO". Label definitions and per-class counts: still **not stated** (the table has no definition columns).
- **Chen 2022, Table 1** (PDF): training set "Resistance (N = 69) Sensitive (N = 161)"; validation set "Resistance (N = 34) Sensitive (N = 41)". Confirms the Methods counts.
- **TCGA 2011 platinum status**: Section 4 is now resolved — verbatim definition in `label_validity/PLATINUM_STATUS_definition.md` (SI Methods S1, pp. 2–3).
- Joined-quote check against PDFs: still to do before printing.


## 7. Quote check against local PDFs (main session, 2026-10-29, ~17:20 ET)

Script: every quoted passage (≥ 15 characters) split at `[…]`, normalised (case, punctuation, line-break hyphenation, ligatures) and searched in `pdftotext` output of the publisher PDF.
- 76 quotes checkable against a local PDF: 71 matched exactly.
- 2 corrected above to the PDF wording: Chen 2022 PFI definition (missing "and"); Sun X 2021 GSE131978/GSE51373 sentence (citation markers "[16]", "[17]" restored).
- 3 matched on manual inspection; the miss was a PDF page break inside the sentence (Li 2022 GSE15622 sentence; Sun X 2021 "Removed the samples…"; Wang 2025 "LASSO regression analysis identified 16 variables").
- Sun J 2019 (16 quotes): article PDF not in the Literature folder; checked against the publisher HTML instead (see below).
- Sun J 2019: 15 of 16 quotes found verbatim in the nature.com article text (WebFetch, 2026-10-29). The Fig. 1 abbreviation line was not found and is now marked unverified. The article PDF was not downloaded; a PDF check is optional because no Table 1 cell depends on unverified Sun J wording.
