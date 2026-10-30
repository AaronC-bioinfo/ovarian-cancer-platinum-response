# G6 — Literature additions: eleven further papers on platinum-response labels in TCGA-OV and related questions

Compiled 2026-10-29 from the publisher PDFs in `C:\PROJECTS\OV Data\Project data\Literature\` (text extracted with `pdftotext -layout`; every quote was then re-read in the page text). Companion to `G5_literature_label_table.md`; same conventions.

Conventions:
- **not stated**: the full text I read does not give this item. Supplements were not opened unless they are in the Literature folder.
- **[my arithmetic]**: a check I computed; not a claim made by the paper.
- Page numbers are the printed journal pages. Where the PDF page differs from the printed page, both are given once per paper (see "Pagination" line in each section).
- Each verbatim quote is ≤ 40 words. Where a quote spans a line-break hyphenation in the PDF, the hyphen was removed.

File → paper identification (by content, not file name):
| File | Paper | Confirmed |
|---|---|---|
| `villalobos2018.pdf` | Villalobos VM, Wang YC, Sikic BI. JCO Clin Cancer Inform 2018 | yes (DOI 10.1200/CCI.17.00096 printed p. 9) |
| `Yang SYC et al. 2018.pdf` | Yang SYC et al. Genome Med 2018;10:81 | yes (DOI 10.1186/s13073-018-0590-x, p. 1) |
| `Talijanovic, Lopacinska-Jørgensen & Høgdall 2025.pdf` | Anticancer Res 2025;45:11–26 | yes (DOI 10.21873/anticanres.17389, p. 11) |
| `s12943-016-0548-9.pdf` | Gonzalez Bosquet J et al. Mol Cancer 2016;15:66 | yes |
| `s41598-021-85256-9.pdf` | Gonzalez Bosquet J et al. Sci Rep 2021;11:5957 | yes |
| `s12885-020-06922-1.pdf` | Choi J et al. BMC Cancer 2020;20:413 | yes |
| `s41698-025-00808-w.pdf` | Kilim O et al. npj Precis Oncol 2025;9:27 | yes |
| `IJGM-338044-…pdf` | Guo K, Li L. Int J Gen Med 2021;14:8237–8248 | yes (DOI 10.2147/IJGM.S338044) |
| `89228-PB5-2620-R2.pdf` | Wang C et al. Transl Cancer Res 2024;13(8):4354–4371 | **yes, confirmed**: title "Identification of genes predicting chemoresistance and short survival in ovarian cancer"; "doi: 10.21037/tcr-23-2157" (p. 4354) |
| `markman1991.pdf` | Markman M et al. J Clin Oncol 1991;9:389–393 | yes |
| `1904.01637v1.pdf` | Yousefi S et al. arXiv:1904.01637v1 [q-bio.QM], 2 Apr 2019 | yes |

---

## 1. Compact summary table (same columns as G5 section 1)

| Ref | Paper | Cohort (role) | Label name (as used) | Label source / field | n per class (as reported) | Design (split / CV / selection) | AUC reported |
|---|---|---|---|---|---|---|---|
| G6-1 | Villalobos 2018 JCO CCI | TCGA-OV "2011 clinical annotation set", 587 → 450 high-risk (re-annotation; no classifier) | platinum sensitive / resistant / refractory; also RECIST CR/PR/SD/PD | Authors' own re-annotation of the TCGA chemotherapy data (drug start/end dates, days to recurrence/progression/death). Rule: ≥ 6 mo after last platinum dose = sensitive; 1–6 mo = resistant; during treatment or < 1 mo = refractory (p. 4). TCGA field name: **not stated**; no comparison with TCGA's PLATINUM_STATUS | OS curves (high-risk set): 212 sensitive / 91 resistant / 28 refractory (Fig 1A, p. 5). RECIST: CR 249 / PR 53 / SD 27 / PD 32 (Fig 1B). Unclassified for platinum status: **not stated** ([my arithmetic] 450 − 331 = 119) | **No classifier.** Kaplan–Meier, log-rank, t tests | none |
| G6-2 | Yang SYC 2018 Genome Med | TCGA-OV (independent validation of PM extremes; no classifier) | short-term (ST) / long-term (LT) survivors | TCGA clinical data via Broad GDAC Firebrowse, "accessed on November 1, 2016" (p. 2–3). ST = OS 6 mo–2 y AND primary platinum resistance AND progression within 6 mo of completing platinum (PM definition, p. 2); LT = OS ≥ 10 y. How "primary platinum resistance" was read from TCGA fields: **not stated** | 60 ST / 10 LT identified clinically (p. 3); molecular analyses use 40 ST / 8 LT (Fig 1b, p. 5) and 32 ST / 8 LT (p. 12) | **No classifier.** Group comparisons (Wilcoxon, Fisher) | none |
| G6-3 | Gonzalez Bosquet 2016 Mol Cancer | TCGA-OV serous (training) | complete responders (CR) / incomplete responders (IR) ("platinum-resistant") | TCGA clinical data; labels from their 2014 Cancer Res paper [18]. CR = "progression-free survival 6 months after the first platinum-based treatment"; IR = refractory or "recurred within 6 months of treatment completion" (p. 2). Field name / portal: **not stated** | 292 CR / 158 IR (n = 450) (p. 2, Table 1) | 9 CMA classifiers on 422 genes, then 34 genes selected with all CMA filters on the full TCGA set; internal cross-validation (type/folds **not stated**); corrected for batch, FIGO stage and "optimal treatment". External: 6 GEO/EBI sets recoded to CR/IR; Table 2 gives per-class n | TCGA 422-gene: 0.53–0.73 (Tables 6–7). TCGA 34-gene: 0.64–0.79 (Table 8). Validation 34-gene: 0.45–0.73 (Table 8, p. 12) |
| G6-4 | Gonzalez Bosquet 2021 Sci Rep | TCGA-OV HGSC RNA-seq (**external validation only**; training = Univ. Iowa n = 88) | responders / non-responders | "progression-free survival of at least 6 months after the first platinum-based treatment" (p. 2); non-responders = platinum-resistant or -refractory. TCGA inclusion: ≥ 6 mo follow-up after completing chemo, known status at 6 mo, chemo type known (p. 5). Field: **not stated** (Supplementary Methods) | TCGA: 189 responders / 149 non-responders (n = 338) (p. 6). UI: 50 / 38 | UI: univariate ANOVA → lasso; 1,000 × 10-fold CV; 1–3 data-type models. TCGA used as held-out validation of 107 UI-built models (p. 7). Not an expression-only classifier (clinical + RNA-seq-derived variables, methylation) | UI training "over 95%" (p. 6). TCGA numeric AUCs: **not stated** in main text (Fig 4 heat-maps; "80% (51 out of 64)" CIs overlap, p. 7; "97% (62 out of 64)" after genotype adjustment, p. 8) |
| G6-5 | Choi 2020 BMC Cancer | TCGA-OV HGSOC (discovery; no classifier) | chemo-sensitive / chemo-resistant | GDC via TCGAbiolinks (p. 2). Interval from last primary chemotherapy to recurrence/progression: < 6 mo resistant, > 12 mo sensitive, 6–12 mo **excluded** (p. 3). Field: **not stated** | 110 R / 160 S of 587 (p. 3); with microarray 100 R / 138 S; after QC 99 R / 135 S (p. 3) | **No classifier.** limma DEG + WGCNA; validation = PFS Cox/KM in GSE9891 (n = 225) via KM-plotter and SurvExpress | none |
| G6-6 | Kilim 2025 npj Precis Oncol | TCGA-OV with CPTAC proteomics + H&E WSIs (train or test, alternating with PTRC-HGSOC) | refractory (non-responder) / sensitive (responder) | Definition from Chowdhury et al. [10]: refractory = progressed or stable disease within 6 cycles of initial platinum/taxane; sensitive = responded and no progression within 2 years (p. 8). Patients between these: **not stated** (Supplementary Table 7). TCGA clinical field: **not stated** | TCGA 127 patients / 159 samples (p. 8). Per class: **not stated** in main text | Deep multimodal (WSI + proteomics), **not mRNA**. Train on one cohort, test on the other; 5-fold CV within cohort; weighted sampling for class imbalance (p. 12) | PTRC→TCGA primary: multimodal 0.752, proteomics 0.61, WSI 0.566; TCGA→PTRC: 0.835 (Table 1, p. 2; text p. 4). TCGA 5-fold CV multimodal 0.613 |
| G6-7 | Guo & Li 2021 Int J Gen Med | TCGA-OV via "GDC apps" (clinical validation of 3 cell-line DEGs) | platinum-sensitive / resistant | NCCN-style rule: relapse within 6 mo after completing chemo = resistant; sensitive = clinical remission and recurrence > 6 mo after stopping chemo (p. 8239). Field: **not stated** | 205 S / 49 R (n = 254) (p. 8239, 8240) | **No trained classifier.** Single-gene ROC on expression; χ², KM, binary logistic | IFI27 0.5964, JAG1 0.6011, DNM3 0.5812 (Table 4, p. 8247) |
| G6-8 | Wang C 2024 Transl Cancer Res | TCGA-OV 489 via cBioPortal (DEG discovery; survival) | platinum resistant / sensitive | cBioPortal clinical fields listed as "staging", "grading", "overall survival" and "primary treatment outcome"; "a subgroup of 90 platinum resistant samples and 197 sensitive samples" (p. 4355). Definition for TCGA: **not stated**. Only cut-off given is for ROC-plotter patients (relapse at 6 mo, p. 4356) | 90 R / 197 S (= 287) | **No trained classifier.** t-test DEGs; ROC-plotter single-gene AUC in 1,347 GEO/TCGA patients; KM-plotter survival | per-gene "AUC >0.6" threshold only (p. 4357); exact values in Fig 3 |

---

## 2. Per-paper sections

### G6-1 — Villalobos VM, Wang YC, Sikic BI. Reannotation and Analysis of Clinical and Chemotherapy Outcomes in the Ovarian Data Set From The Cancer Genome Atlas. JCO Clin Cancer Inform 2018. DOI 10.1200/CCI.17.00096
Pagination: PDF page = printed page (1–16). Volume/article number not printed in the PDF; "Published online on ascopubs.org/journal/cci on February 22, 2018" (p. 9). Bibliographic check: authors, title, journal and DOI match the brief.

**Data set and TCGA release** (p. 2, Materials and Methods):
> "The master data set contains all data on 587 patients with ovarian cancer within the 2011 clinical annotation set."
> "We included only 450 patients with grade 3 tumors and stage III ot IV disease (Table 1)." [sic: "ot"]
> "The clinical data cutoff for this analysis was August 9, 2011."
- Sources used for re-annotation (p. 2, *Chemotherapy Annotation*): the original TCGA clinical annotation (age, stage, grade, days to death/last follow-up/progression/recurrence, "primary therapy outcome using Response Evaluation Criteria in Solid Tumors (RECIST) measures", vital status) and the TCGA chemotherapy table ("days to drug start and end, drug name, and regimen indication"). No chart review or external source is mentioned.
- Number of patients re-annotated: 587 (master) and 450 (high-risk); "Data herein contain data from the high-risk data set unless otherwise specified" (p. 2).

**Definitions of platinum sensitivity** (p. 4, *Classification of Platinum Sensitivity*):
> "patients receiving first-line therapy who experienced progression or recurrence ≥ 6 months after their last platinum dose are considered platinum sensitive."
> "Platinum-resistant patients experienced treatment failure from 1 to 6 months after their last platinum dose."
> "Platinum-refractory patients experienced treatment failure during treatment or within 1 month of their last platinum dose."
- Time reference: **last platinum dose of first-line therapy** (p. 4): "Time since last platinum dose before recurrence is calculated as the difference between the last day of first-line platinum and treatment failure". Where dates were incomplete: "we estimated each cycle length to be 21 days" and "If there was no information on number of cycles, we assumed six cycles were given." (p. 4).
- Censored / disease-free patients (p. 4, two statements):
> "Patients who had not yet experienced relapse and were free of disease within 6 months of their last platinum dose were excluded from the resistant and refractory groups in this analysis.22"
> "Patients who had not yet experienced relapse and were free of disease were excluded from the resistant and refractory groups if their follow-up time was < 6 months from their last platinum dose."
- Fig 1 legend (p. 5) restates the rule as "sensitive (treatment failure free ≥ 6 months from last platinum dose), resistant (treatment failure free ≥ 1 to 6 months from last platinum dose), and refractory (treatment failure free < 1 month since last platinum dose)".
- A second, operational wording appears in Results (p. 7): "platinum-sensitive disease, defined as reinitiation of treatment > 6 months after the last platinum dose" and "platinum-resistant or platinum-refractory disease, defined as reinitiation of treatment within 6 months of the last platinum dose". This uses start of second-line treatment, not progression, as the event. The paper does not reconcile the two wordings.
- TTF rationale (p. 2): "Because there is no documentation of progression-free survival (PFS) for each therapeutic regimen, we have inferred that the initiation of a new therapy signifies that the patient had experienced recurrence or progression of disease."

**Comparison with TCGA's published platinum status: none.** The strings "platinum status", "PLATINUM_STATUS", "concordance", "agreement", "kappa", "reclassif", "Tooearly"/"too early" do not occur anywhere in the text. The 2011 Nature paper is cited only as the data source (ref 9). No count of agreement, reclassification or recovered missing values is reported.

**Counts** (high-risk set unless stated):
- OS by platinum category (Fig 1A, p. 5): Sensitive n = 212, median OS 56.6 mo; Resistant n = 91, 27.0 mo; Refractory n = 28, 11.6 mo. P < .0001 (sensitive v resistant) and .001 (refractory v resistant). Text (p. 5–6): "median OS, 56.6 v 27.0 months, respectively; P < .001" and "11.6 v 27.0 months, respectively; P = .001".
- [my arithmetic] 212 + 91 + 28 = 331 of 450 high-risk patients carry a platinum category; 119 (26%) do not. The paper does not state this number or why those patients are absent (presumably disease-free with < 6 months follow-up, or insufficient chemotherapy data).
- OS by RECIST first-line response (Fig 1B, p. 5): CR 249 (54.1 mo), PR 53 (33.7), SD 27 (34.4), PD 32 (20.9). Text p. 6: "patients who achieved partial responses (PR) did not significantly differ in their median OS from those with stable disease (SD; 33.7 v 34.4 months, respectively; P = .95)".
- TTF by RECIST (Fig 1C): CR 246 (18.0 mo), PR 47 (9.1), SD 25 (13.5), PD 29 (6.0).
- Patients lacking usable chemotherapy information: Table 2 (p. 3) first-line "Insufficient data" = 44 (9.8%) high-risk, 77 (13.1%) full set. Fig 2A first-line TTF curve n = 402 of 450. p. 6: "Occasionally, dates were available for treatments but no drug was listed, or there were drugs listed but no treatment dates. This occurred in four patients in first line".
- Second-line by platinum category (Fig 3, p. 8): sensitive–platinum 71, sensitive–other 39, resistant/refractory–platinum 15 (OS: 14), resistant/refractory–other 55. Mean time since last platinum: sensitive–platinum 19.1 mo (15.5–22.7), sensitive–other 13.5 (10.8–16.2), P = .038; resistant/refractory 3.4 and 3.0 mo.
- BRCA1/2 (p. 7, Fig 4): mutated 78, median OS 66.6 mo; wild type 369, 38.1 mo; "hazard ratio [HR], 0.52; 95% CI, 0.4 to 0.71; P < .001" in text, but Fig 4A prints "HR, 0.53 (95% CI, 0.40 to 0.71) P = .0004" — minor internal discrepancy (0.52 v 0.53).

**Comparison of response categories with each other**: Only qualitative. p. 6: "These OS data for platinum sensitivity correlate closely with the documented RECIST responses to treatment." No cross-tabulation of platinum category against RECIST category is given. The RECIST-based comparison PR v SD (OS and TTF) is the only explicit between-category test.

**OS or survival thresholds as response labels**: Not used and not discussed. OS is an outcome stratified by the platinum categories; it is never proposed as a label. Abstract: "The major determinant of OS in this study was platinum sensitivity status."

**Availability**: p. 2: "The final, complete, reannotated master and high-risk data sets are included in the Data Supplement, along with the original patient and chemotherapy data." No URL given beyond the journal Data Supplement.

**Other items relevant to label validity**:
- TTF caveat (p. 7): "One of the primary caveats of using a surrogate, such as TTF, instead of a validated end point, such as PFS … is a potential overestimation of TTF for the final line of chemotherapy".
- Only 65% of sensitive patients were re-treated with platinum in second line; 21% of resistant/refractory patients received platinum (p. 7).
- Fig 2 footnote (p. 6): "discrepancies in values listed here compared with Table 2 are a result of variations in data that were available in the TCGA cohort."

### G6-2 — Yang SYC, Lheureux S, Karakasis K, Burnier JV, Bruce JP, Clouthier DL, et al. Landscape of genomic alterations in high-grade serous ovarian cancer from exceptional long- and short-term survivors. Genome Med 2018;10:81. DOI 10.1186/s13073-018-0590-x
Pagination: PDF page = printed page (1–17).

**Definition of the groups** (p. 2, Methods, *Sample inclusion criteria*; Princess Margaret cohort):
> "Short-term survival patients were defined as patients with (1) overall survival between 6 months and 2 years, (2) primary platinum resistance, and (3) documented disease progression within 6 months from completing platinum-based chemotherapy."
> "Patients with LT survival had durable platinum sensitivity and were identified based on OS greater than 10 years following HGSOC diagnosis (Additional file 1: Figures S1, S2A)."
- So yes: the ST label **combines** OS < 2 years (and > 6 months) with platinum resistance (progression within 6 months of completing platinum). The LT label combines OS ≥ 10 years with "durable platinum sensitivity". Discussion restates it as survival only (p. 13): "patients who experienced prolonged chemosensitivity (OS > 10 years) to patients with primary chemoresistance (OS < 2 years)".
- Inclusion (p. 2): stage III HGSOC, primary debulking, "at least 6 cycles of platinum-based chemotherapy", chemo-naïve tissue.

**TCGA selection** (p. 2–3):
> "TCGA data for HGSOC was downloaded from Broad GDAC Firebrowse (http://firebrowse.org/?cohort=OV/)." (p. 2)
> "From data accessed on November 1, 2016, we found 214 of 603 patients with stage III HGSOC and completed overall survival data." (p. 3)
> "Applying the same selection criteria used to filter the PM cohort, we identified 60 of 288 patients had primary platinum resistance and OS between 6 months and 2 years (28%)," (p. 3)
> "and 10 patients (5%) with extended platinum sensitivity and OS ≥ 10 years (Additional file 1: Figure S2B)." (p. 5)
- Which TCGA field supplied "primary platinum resistance" (platinum status, progression date, or RECIST outcome): **not stated**.

**Numbers in each group**:
- PM: Abstract and Table 1: LT n = 20, ST n = 21 (41 tumours); Results p. 3 text reverses them: "ST (< 2 years, 20 patients) and LT OS (≥ 10 years, 21 patients)". Exome/RNA analysed: 19 ST, 20 LT (p. 5). Table 1 (p. 4): ST OS 6–12 mo 4 (19%), 12–24 mo 17 (81%); LT all > 24 mo.
- TCGA: 60 ST / 10 LT identified (p. 3, 5); mutation-burden analysis "short-term (n = 40) and long-term (n = 8)" (Fig 1 legend, p. 5); immune analysis "8 LT and 32 ST tumors that matched the survival selection criteria" (p. 12). Why 60/10 shrinks to 40/8 and 32/8: **not stated**.
- [my arithmetic] 60/288 = 20.8%, not 28%; 60/214 = 28.0% and 10/214 = 4.7%, so the denominator "288" on p. 3 is inconsistent with the "214" in the preceding sentence and the 28%/5% percentages; 214 appears to be the intended denominator.

**Markers tested against the ST/LT label in TCGA** (relevant to C3): somatic mutation burden (Fig 1b, p = 0.022 in PM; TCGA "only difference between short- and long-term survivors is assessed"); TP53 p.Arg248 occurring in 4 ST TCGA patients (p. 9); BRCA1 expression trend (Fig 3b, p. 7); CCNE1 amplification in TCGA LT "at a 10% (1/10) frequency" (p. 10); immune ssGSEA (Fig S11, p. 12). No AUC and no classifier.

**Relevance to OS-vs-platinum**: This paper is the clearest published example of a compound label (OS window + platinum resistance + progression ≤ 6 months). It does not compare OS-only with platinum-only labels, and it does not report how many TCGA patients satisfied one criterion but not the other.

### G6-3 — Gonzalez Bosquet J, Newtson AM, Chung RK, Thiel KW, Ginader T, Goodheart MJ, et al. Prediction of chemo-response in serous ovarian cancer. Mol Cancer 2016;15:66. DOI 10.1186/s12943-016-0548-9
Pagination: PDF page = printed page (1–15).

**Label definition** (p. 2, Methods, *Patients and data collection*):
> "Patients with serous OVCA in TCGA were utilized to create a prediction model in the testing dataset, and were divided into two categories: complete responders (CR) and incomplete responders (IR)."
> "Clinical complete response (CR) was defined as progression-free survival 6 months after the first platinum-based treatment."
> "In patients with incomplete response (IR), the disease either not did respond or progressed during treatment (refractory), or recurred within 6 months of treatment completion (resistant) [4, 19]."
> "Patients defined as IR in our study are also clinically referred to as 'platinum-resistant' [20]"
- Reference point: the CR sentence says "after the first platinum-based treatment"; the IR sentence says "within 6 months of treatment completion". Refractory and resistant are pooled into IR. Intermediate category: none (binary at 6 months). Censoring rule for disease-free patients with short follow-up: **not stated** in this paper (labels were carried over from ref 18, Gonzalez Bosquet 2014 Cancer Res).
- TCGA field / portal: **not stated**. "In the TCGA dataset, there were 292 patients classified as CR and 158 classified as IR." (p. 2). Table 1 (p. 2) also lists grade 1–2 and stage I–II patients, so this 450 is **not** the 450 high-risk set of Villalobos 2018 (grade 3, stage III/IV only) despite the identical n.
- Table 1 (p. 2): FIGO stage (p < 0.01) and "Optimal Treatment" (surgery + 6 cycles; p < 0.001) are associated with CR/IR. Footnote: "Only FIGO stage and optimal treatment (including optimal surgery AND 6 cycles of platinum-based chemotherapy) were independently associated with chemo-response".

**Design** (p. 2–3):
- Nine CMA classifiers (RF, Lasso, Elastic Net, PAM, DDA, PLS, PLS-RF, penalized logistic, PLS-logistic) on the 422-gene signature from ref 18. "to avoid over-fitting, cross-validation was used (internal validation of the classifier) [29]" (p. 3); CV type and folds: **not stated**. "predictive performance was computed with corrections for TCGA batch-effect and to account for two other variables independently associated with chemo-response in serous OVCA (FIGO stage classification and optimal treatment, Table 1)" (p. 3).
- 34-gene set: "only 34 genes had more than 10 hits with all methods of gene selection" (p. 5), selected on the full TCGA set with all CMA filter methods (p. 3). No held-out TCGA split is described.
- External sets (Table 2, p. 3, CR/IR): GSE23554 90/37; GSE9891 185/55; GSE28739 20/30; GSE17260 93/17; GSE30161 32/23; E-MTAB-386 64/41; GSE3149 listed without counts. "Response to therapy variables were coded to make outcomes comparable with TCGA: CR and IR." (p. 3). How each GEO response field was mapped: **not stated**.

**AUC** (Tables 6–8, p. 11–12):
- TCGA 422-gene training (CV): 0.53 (penalized logistic) to 0.73 (Elastic Net); text p. 5: "in AUCs ranging from 53 to 73 %". Clinical-only models "mean AUC around 58 %" (p. 5).
- TCGA 34-gene (Table 8): 0.64–0.79 (penalized logistic 0.79, 95% CI 0.77–0.81). Abstract: "AUCs approaching 80 %".
- Validation of 34-gene model (Table 8): Australia 0.67–0.73; Ferriss 0.51–0.59; MCC 0.45–0.66. Text p. 6: "AUC values ranging from 56 to 73 %".
- Replication sets with missing genes (Table 6): Trinh AUCs 0.00–0.18 for several methods (degenerate).

**Label-validity notes**:
- OS by label: Fig 1 legend (p. 3): "Complete responders (CR) have a median survival 2 years greater than IR"; Cox p < 10⁻¹⁴ (p. 2). Medians not printed.
- Misclassification (p. 10): "The only independent variable associated with misclassification was 'optimal treatment' (p < 0.001)" and "TCGA was not designed to study chemo-response". Because IR includes patients who progressed during treatment, "optimal treatment (6 cycles)" is partly a consequence of the label; the paper does not discuss this circularity.
- "158 of 450 patients" misclassified "more than 20 % of the time on average" (p. 10).

### G6-4 — Gonzalez Bosquet J, Devor EJ, Newtson AM, Smith BJ, Bender DP, Goodheart MJ, et al. Creation and validation of models to predict response to primary treatment in serous ovarian cancer. Sci Rep 2021;11:5957. DOI 10.1038/s41598-021-85256-9
Pagination: PDF page = printed page (1–14).

**Role of TCGA**: validation only. Training cohort is University of Iowa (UI), n = 88 (50 responders / 38 non-responders, p. 2). "Validation of all models was performed using TCGA HGSC database." (Abstract).

**Label definition** (p. 2, *Outcomes definition*):
> "Responders were those with a progression-free survival of at least 6 months after the first platinum-based treatment. Non-responders were those who did not respond (platinum-resistant) or progressed during treatment (platinum-refractory)."
- Introduction (p. 2) gives the clinical gloss: refractory = "progresses during initial chemotherapy"; resistant = "recurs < 6 months after finishing treatment".
- Reference point: inclusion criteria use completion of chemotherapy: patients "that had less than 6 months of follow-up after completing initial chemotherapy, unknown disease status after 6 months of completion of initial chemotherapy, or incomplete data about the chemotherapy delivered were excluded" (p. 2). Same rule applied to TCGA (p. 5): "We included only patients with follow-up of at least 6 months after completing initial chemotherapy, with known disease status after 6 months of completion of initial chemotherapy, and data about type of chemotherapy delivered25."
- TCGA field: **not stated** ("see Supplementary Methods"). RNA-seq BAMs via dbGaP #16,003 (p. 6); data availability points to portal.gdc.cancer.gov (p. 13).

**TCGA n** (p. 6): "there were a total of 189 patients classified as responders and 149 as non-responders in TCGA for validation of prediction models (Supplementary Table S2)." [my arithmetic] 338 total; 44.1% non-responders, matching "in TCGA HGSC dataset 44% of patients were non-responders" (p. 6).

**OS by label** (p. 6): UI responders median 39.3 mo (95% CI 31, 58.2); TCGA responders 57.7 mo (44.3, 82); UI non-responders 12.5 mo (8, 19.1); TCGA non-responders 22.7 mo (15.9, 26.3).

**Design**: univariate ANOVA with CV → lasso; "AUC was estimated with 1,000 replicates of tenfold cross-validation" (p. 5); models of 1–3 data types; TCGA validation of "107 different models" (p. 7) with a > 90% sensitivity threshold chosen by pROC. Clinical variables are included; this is not an expression-only classifier.

**AUC**: UI training "over 95%" (p. 6); 59 models with AUC > 90% shown in Fig 3. TCGA numeric AUCs: **not stated** in main text; summary is CI overlap: "80% (51 out of 64) of UI-built models had an AUC 95% CI in the TCGA validation set that overlapped with the UI training set interval" (p. 7), rising to "97% (62 out of 64 models)" after genotype adjustment (p. 8). Models with DNA methylation or lncRNA underperformed in TCGA (p. 7, 10).

**BRCA**: in UI, "BRCA2 variants in 24% (12 out of 50) of responders and in 26% (10 out of 38) of non-responders (p = 0.52)" and "BRCA1 variants in 36% (18 out of 50) of responders and 50% (19 out of 38) in non-responders (p = 0.06)" (p. 6); not selected. Not tested in TCGA.

### G6-5 — Choi J, Topouza DG, Tarnouskaya A, Nesdoly S, Koti M, Duan QL. Gene networks and expression quantitative trait loci associated with adjuvant chemotherapy response in high-grade serous ovarian cancer. BMC Cancer 2020;20:413. DOI 10.1186/s12885-020-06922-1
Pagination: PDF page = printed page (1–11).

**Source** (p. 2): "We retrieved 587 high-grade serous ovarian carcinoma (HGSOC) patients with available clinical data from the Cancer Genome Atlas (TCGA) Genomic Data Commons (GDC) portal [21] using the TCGAbiolinks R/Bioconductor package [22]." Expression: "Affymetrix ht_hg_u133a chip" from the GDC portal (p. 3).

**Label definition** (p. 3, *Patient classification*):
> "The interval between a patient's last primary chemotherapy treatment and the onset of a recurrent tumor or progression of an existing tumor was used as a metric for determining chemotherapy sensitivity."
> "Patients who developed a new tumor in less than 6 months following their last primary chemotherapy treatment were defined as resistant (N = 110)."
> "those who did not have a recurrent tumor event for over a year after their last primary chemotherapy treatment were defined as sensitive (N = 160)."
> "Individuals who had a recurrent tumor event between 6 months to 1 year following chemotherapy were excluded from the study. This strategy for dichotomizing resistant and sensitive patients was used to enrich for genetic differences."
- Reference point: last primary chemotherapy treatment (end of first-line chemo). Cut-offs: < 6 mo resistant, > 12 mo sensitive; 6–12 mo excluded. GDC field names: **not stated**. Handling of patients with no recurrence and < 12 mo follow-up: **not stated** (Abstract wording "remained progression-free for 12 months").
- n: 110 R / 160 S (270); with microarray 100 R / 138 S (238); after QC 99 R / 135 S (234) (p. 3). Age differed between groups (p = 0.0041) and was used as covariate.

**Classifier / AUC**: none. limma DEGs (VCP) and WGCNA module eigengenes vs response (GLM). Validation is survival-based, not label-based: GSE9891 serous platinum-treated subset (n = 225), "progression-free survival (PFS) was the primary outcome used in the replication analysis" via KM-plotter and SurvExpress (p. 4).

**Label-validity note**: excluding the 6–12 month band is the explicit "enrich for genetic differences" strategy; it changes class balance (110/270 = 41% resistant) relative to a 6-month-only rule.

### G6-6 — Kilim O, Olar A, Biricz A, Madaras L, Pollner P, Szállási Z, et al. Histopathology and proteomics are synergistic for high-grade serous ovarian cancer platinum response prediction. npj Precis Oncol 2025;9:27. DOI 10.1038/s41698-025-00808-w
Pagination: PDF page = printed page (1–15).

**Data**: PTRC-HGSOC (158 patients, 348 samples; FHCRC, UAB, Mayo) and TCGA-OV with CPTAC proteomics and H&E WSIs ("127 patients 159 samples with all 3 data types", p. 8). WSIs from TCIA "collection/tcga-ov/" (p. 8). Modality is **proteomics + histology**, not mRNA expression.

**Label definition** (p. 8, *Patient cohorts*):
> "Refractory cancers were defined as those that progressed or had stable disease within 6 cycles of initial platinum/taxane therapy after initial debulking surgery10."
> "Sensitive tumors were defined as those that responded to initial platinum/taxane therapy and did not progress within 2 years."
- Reference point: during the 6 cycles of first-line therapy (refractory) and 2 years (sensitive); source of definition is Chowdhury et al. [10]. The Introduction's generic definition differs: "platinum resistance, defined as disease recurrence within 6 months of first-line platinum-based chemotherapy" (p. 1) — this is not the operational label.
- Patients who progressed between end of therapy and 2 years (the usual "resistant" and "partially sensitive" groups): **not stated** how handled (presumably excluded; "Supplementary Table 7").
- TCGA clinical field used: **not stated**. Per-class TCGA n: **not stated** in main text; Table 1 note: "TCGA cohort is comprised of 127 patients." Class imbalance acknowledged: "weighted sampling to make sure models were not biased by class imbalances as there were more sensitive/responder patients than refractory patients" (p. 12).

**Design**: train on one cohort, test on the other, plus 5-fold CV within cohort; primary and metastatic samples modelled separately. Table 1 "Patients" row gives train:test = 158:127 (HGSOC→TCGA) and 127:158 (TCGA→HGSOC); 5-fold CV 126:32 and 102:25.

**AUC** (Table 1, p. 2; text p. 4), primary tumours: PTRC-HGSOC train → TCGA test: histopathology 0.566 ± 0.052, proteomics 0.61 ± 0.05, multimodal 0.752 ± 0.044. TCGA train → HGSOC test: 0.528 / 0.755 / 0.835. TCGA 5-fold CV: 0.586 / 0.552 / 0.613. FHCRC+MC → UAB: multimodal 0.84. Metastatic: PTRC→TCGA multimodal 0.704.

**Markers vs label** (p. 5): "the HRD-score, Signature 3 and HRDetect scores were available for n = 98 TCGA cases. The WSI+proteomics model outperformed the HRD-score, HRDetect, and Signature 3 for the TCGA" (DeLong Z = −3.113, P = 0.002). Fig 3d: survival curves (PFS, PFI, OS; "N = 98 for PFS and OS") vs "bonified BRCA status" and HRDetect.

### G6-7 — Guo K, Li L. Prediction of Key Candidate Genes for Platinum Resistance in Ovarian Cancer. Int J Gen Med 2021;14:8237–8248. DOI 10.2147/IJGM.S338044
Pagination: PDF page n = printed page 8236 + n.

**Discovery**: five GEO **cell-line** datasets (GSE58470, GSE45553, GSE41499, GSE33482, GSE15372) (p. 8238); intersection DEGs → IFI27, JAG1, DNM3. TCGA is used only for clinical validation of these three genes.

**TCGA source and label** (p. 8239, *TCGA Public Database for Clinical Case Analysis*):
> "The gene expression and clinical follow-up information of ovarian cancer clinical samples were downloaded from the official application tool GDC apps provided by TCGA database"
> "A total of 362 clinical samples were included, excluding 108 patients without chemotherapy outcomes, and 254 patients who received standard chemotherapy in combination with platinum-based agents"
> "it is generally considered that the relapse within 6 months after the completion of chemotherapy is regarded as chemoresistance."
> "Chemosensitivity is defined as patients who have received more than 3 courses of regular chemotherapy after the initial cytoreductive surgery and have achieved clinical remission, and have recurred more than 6 months after stopping chemotherapy."
> "Therefore, there were 205 cases in the platinum-sensitive group and 49 cases in the resistant group."
- Reference point: completion of chemotherapy. Cut-off 6 months. Field name: **not stated**. Whether non-recurring patients count as sensitive (the wording requires recurrence > 6 months): **not stated**. Requirement of > 3 courses is an extra inclusion rule.
- [my arithmetic] 49/254 = 19.3% resistant, well below the ~31% in TCGA 2011; the paper does not comment.
- OS and PFS definitions (p. 8239): "Overall survival (OS) is defined as the time from diagnosis to death due to ovarian cancer. Progression-free survival (PFS) is defined as the time from the patient's initial treatment to tumor progression."

**Classifier / AUC**: none trained. Single-gene ROC (p. 8242, Table 4 p. 8247): IFI27 AUC 0.5964 (0.506–0.686), P 0.0361; JAG1 0.6011 (0.510–0.692), P 0.0279; DNM3 0.5812 (0.497–0.666), P 0.0775. Binary logistic regression and χ² against clinicopathological parameters (Table 2, p. 8243); KM for OS/PFS by gene expression within the resistant group (Fig 6).

### G6-8 — Wang C, Chen C, Chen X, Luo J, Su Y, Liu X, et al. Identification of genes predicting chemoresistance and short survival in ovarian cancer. Transl Cancer Res 2024;13(8):4354–4371. DOI 10.21037/tcr-23-2157
Pagination: PDF page n = printed page 4353 + n. Identity of file `89228-PB5-2620-R2.pdf` confirmed from title page and DOI line (p. 4354).

**Source and label** (p. 4355, *Data acquisition and large samples*):
> "TCGA ovarian cohort (10) of 489 OC patients with clinical data and gene expression was retrieved from cBioPortal (http://www.cbioportal.org/) (11,12), including 'staging', 'grading', 'overall survival' and 'primary treatment outcome'"
> "in which a subgroup of 90 platinum resistant samples and 197 sensitive samples was included."
- Definition of resistant/sensitive for TCGA: **not stated**. Field name: not named, but the 90/197 split equals the cBioPortal ov_tcga_pub `PLATINUM_STATUS` counts (G5, cross-reference) and Li 2022's Data Sheet 2; the paper lists "primary treatment outcome" among retrieved fields, which is a different cBioPortal field (RECIST-type). The TCGA 2011 label class is therefore inferred from the counts, not stated.
- Only cut-off in the paper is for ROC plotter (p. 4356): "The relapse status at six months was used as a cutoff for determination of patient's response to therapy. And patients relapsed within six months were considered as non-responders to drugs." (applies to the 1,816-patient GEO+TCGA KM/ROC-plotter collection, not to the 90/197 TCGA split).

**Design / AUC**: no trained classifier. DEGs by t-test between 90 R and 197 S; ROC plotter in 1,347 patients with per-gene AUC and "P<0.01, AUC >0.6" as the criterion (p. 4357; Fig 3 legend p. 4359); KM plotter OS/PFS in 1,816 patients; DFS/OS in 489 TCGA patients.

**OS-vs-platinum relevance**: the paper's premise (Abstract) is "The genes which contribute to chemoresistance are often leading to short survival", and it screens genes for both resistance and short OS/DFS; it does not compare labels.

### G6-9 — Talijanovic M, Lopacinska-Jørgensen J, Høgdall EV. Gene Expression Profiles in Ovarian Cancer Tissues as a Potential Tool to Predict Platinum-based Chemotherapy Resistance. Anticancer Res 2025;45:11–26. DOI 10.21873/anticanres.17389
Pagination: PDF page n = printed page 10 + n (printed 11–26).

**Scope** (p. 11–12): PubMed, 20 Nov 2018 – 20 Nov 2024, 490 hits → 161 after abstract screen → 44 included; mRNA measured in human tissue by microarray, RNA-seq or qRT-PCR; comparison of platinum-sensitive vs -resistant patients. "17 studies used exclusively publicly available datasets, such as TCGA and GEO" (p. 12). Table IV (p. 23): "TGCA-OV" [sic] used by studies (8, 15-17, 19, 30, 36, 38, 41, 43, 45, 48, 50, 52) — 14 studies.

**How many definitions, across how many studies**:
> "Based on the included studies in this review, there were 12 different definitions of platinum-based chemotherapy resistance, and seven studies did not provide any definition." (p. 16)
> "there are 12 different platinum-based chemotherapy resistance definitions that are defined based on either progression free survival (PFS), platinum free interval (PFI), disease free survival (DFS), or time to recurrence (TTR), as shown in Table III." (p. 22)
> "It is also important to notice that 25% (n=11) of the studies lack a definition in their studies." (p. 22)
- Internal inconsistency: "seven studies did not provide any definition" (p. 16) vs "25% (n=11) of the studies lack a definition" (p. 22). Table III row 13 ("Not defined or not clear as two or more datasets have been combined") lists 7 references (14, 19, 36, 51-54); ref 36 also appears in row 1. [my arithmetic] 11/44 = 25%, so the n = 11 count may include studies with unclear definitions beyond row 13; the paper does not reconcile the two numbers.

**Table III (p. 22), verbatim rows** (R = resistant, S = sensitive):
1. "R: Recurrence <six months post-treatment; S: Recurrence >six months post-treatment" — 12 studies (11, 13, 16, 27, 28, 33, 36, 37, 40, 41, 42, 55)
2. "R: PFI <six months; S: PFI >six months" — (12, 30, 31, 43, 44)
3. "R: PFS <eight months; S: PFS >18 months" — (21, 32, 45-47)
4. "R: PFI <six months; Partially S: PFI 6-12 months; S: PFI >12 months" — (18, 38, 39)
5. "R: Relapse <six months; Partially S: Relapse 6-12 months; S: Relapse >12 months" — (8)
6. "R: time to recurrence (TTR) ≤6 months; S: TTR ≥30 months" — (29)
7. "R: TTR <six months; S: TTR >12 months" — (15)
8. "R: Cancer-free ≤6 months; S: Cancer-free ≥12 months" — (48)
9. "R: PFI <six months; S: PFI >12 months" — (22, 49)
10. "R: OSC patients with 'stable disease' and 'progressive disease' S: OSC patients with 'complete response' and 'partial response'" — (50)
11. "R: disease-free survival (DFS) ≤6 months; S: DFS >6 months" — (17)
12. "R: progressive or persistent disease or progression within six months of completing platinum therapy. S: a complete response during adjuvant chemotherapy and clinical remission for at least six months after the completion of chemotherapy." — (25)
13. "Not defined or not clear as two or more datasets have been combined and each dataset has different definition." — (14, 19, 36, 51-54)
- Note Table III footnote expands PFI as "progression-free interval", not platinum-free interval.

**OS-based or survival-threshold labels in the reviewed studies**: **No row of Table III uses overall survival.** Rows 3 (PFS < 8 vs > 18 months), 6 (TTR ≤ 6 vs ≥ 30 months), 7, 8 and 9 are time-to-event thresholds with an excluded middle band, but all are progression/recurrence-based, not OS-based. Row 10 is a first-course RECIST-type label. In Tables I–II, OS appears only as a correlative outcome (e.g., ref 34 "correlation between CHD4 mRNA expression with overall survival and platinum", p. 18; ref 36 risk score "and overall survival (OS)", p. 20), not as a class label. Therefore: none of the 44 studies, as summarised by the reviewers, used an OS threshold as the resistance label.

**Direct comparison of definitions**: none quantitative. The review tabulates definitions but does not cross-tabulate or measure agreement. Statements on consequences:
> "Furthermore, even among studies using PFI as a measure for platinum-based chemotherapy resistance, there are differences. The inconsistence and lack of definition across studies leads to significant challenges in reproducibility of findings." (p. 22)
> "According to the findings in this review there is no overlapping of results between the genes in different studies that used the same publicly available dataset" (p. 22)
> "these two studies have different definitions of chemotherapy resistance and might have different patient and tumor characteristics" (DOCK4 discordance, p. 23)

**Recommendations**:
> "Therefore, including TCGA patient barcodes for each TCGA-based study together with platinum sensitivity or resistance definition applied should be required." (p. 22)
> "this review highlights the importance of consensus across studies regarding chemotherapy resistance definition, tissue handling, patient characteristics, and treatment protocols" (p. 24)
> Table IV note on TCGA: "The number of patients used by different studies may vary, as not studies provide the information about how many patients from TCGA are used for the gene expression analysis." (p. 23) [sic]
- Also recommended: specifying histological type and FIGO stage (p. 23); reporting tumour percentage (p. 22).

### G6-10 — Markman M, Rothman R, Hakes T, Reichman B, Hoskins W, Rubin S, et al. Second-Line Platinum Therapy in Patients With Ovarian Cancer Previously Treated With Cisplatin. J Clin Oncol 1991;9:389–393
Pagination: PDF page n = printed page 388 + n.

**Design and entry criterion** (p. 389):
> "Eighty-two patients were identified who met the entry criteria of having had a cisplatin-free interval (CFI) of more than 4 months between the completion of their first regimen and the institution of a second cisplatin/carboplatin program."
> "This interval, measured from the date of the last cisplatin dose of the previous therapeutic program to the first dose of the second-line cisplatin/carboplatin regimen, was selected to avoid including patients in the analysis who were continuing to respond"
- Retrospective, single centre (MSKCC); 82 patients, 94 second/third-line cisplatin/carboplatin courses; 72 assessable second-regimen patients (Abstract) / "82 assessable courses" (p. 390). "Only three of the 82 patients (4%) … had demonstrated progressive disease on cisplatin when used as initial therapy." (p. 390)

**Intervals and response rates** (Table 2, p. 391; second cisplatin regimen, by CFI):
- 5–12 months: N 26, assessable 22, response 6 (27%), S-CR 1 (5%)
- 13–24 months: N 23, assessable 18, response 6 (33%), S-CR 2 (11%)
- > 24 months: N 33, assessable 32, response 19 (59%), S-CR 7 (22%)
> "This difference was most evident when comparing patients with a CFI of less than or greater than 24 months, 30% (12 of 40) versus 59% (19 of 32) response rate, respectively (P < .025, x2 test with 1 df)." (p. 391) [PDF text renders χ² as "x2"]
- By treatment-free interval (Table 4, p. 391): < 12 months 9/35 (26%), S-CR 2 (6%); 13–24 months 5/15 (33%); > 24 months 17/22 (77%), S-CR 7 (32%). Text: "While 28% of patients receiving second cisplatin regimens with a TFI of less than 24 months responded to therapy (S-CR rate, 6%), 77% with a TFI of more than 24 months responded (S-CR rate, 32%)" (p. 391).
- Discussion (p. 392): "Patients with a CFI (or TFI) of more than 2 years have a greater than 50% chance of responding a second time to either a cisplatin- or carboplatin-based regimen".
- On refractory patients (p. 392): "in the three assessable patients in our study who received second-line cisplatin under these clinical circumstances, all demonstrated disease progression." and "the high objective response rate … pertains only to patients who have previously responded to cisplatin … and not to individuals with clinically defined cisplatin-resistant disease."

**Verdict on citing Markman 1991 for "less than six months defines platinum resistance"**: **Not appropriate as a direct citation.** The study excluded every patient with a cisplatin-free interval ≤ 4 months, its shortest bin is 5–12 months, and it never uses a 6-month boundary or the term "platinum resistant" as a category. What it supports is (a) the time reference (interval measured from the last platinum dose to re-treatment) and (b) a monotone rise in secondary response rate with longer interval (27% → 33% → 59%; TFI 26% → 33% → 77%), plus the anecdote that 3/3 patients progressing on first-line cisplatin progressed again. The 6-month convention derives from later consensus (e.g., GCIG / Davis, Tinker & Friedlander 2014, cited by Villalobos as ref 22), not from this paper. If cited, phrase it as support for the platinum-free-interval gradient, not for the 6-month cut-off.

### G6-11 — Yousefi S, Shaban A, Amgad M, Chandradevan R, Cooper LAD. Learning Clinical Outcomes from Heterogeneous Genomic Data Sources. arXiv:1904.01637v1 [q-bio.QM], 2 Apr 2019
Pagination: PDF page = printed page.

**Does it state that OS is noisy because of non-cancer deaths? Yes, explicitly.**
> "OS is the period from the date of diagnosis until the date of death from any cause." (p. 5)
> "Since patients generally suffer from disease progression or recurrence before dying, PFI requires shorter follow-up times and has higher event rate." (p. 5–6)
> "Additionally, OS is a noisy signal due to deaths from non-cancer causes. Therefore, wherever possible, PFI is used as the outcome variable." (p. 6)
> "Overall survival (OS) labels are noisier, but simpler to obtain since the patients are either deceased or alive at the end of the study." (p. 12, §5.5)
- PFI definition used (p. 5): "the period from the date of diagnosis until the date of the first occurrence of a new tumor-related event, which includes progression of the disease, locoregional recurrence, distant metastasis, new primary tumor, or death with tumor" (citing Liu et al. 2018).
- Context: pan-TCGA survival modelling (ACC, CESC, KIRC, KIRP, LGG, MESO, PAAD, BRCA, METABRIC; Table 1, p. 6). **TCGA-OV is not among the cohorts analysed.** The statement is general, not ovarian-specific, and is not supported by a quantified estimate of non-cancer deaths. Appropriate to cite for the qualitative claim only.

---

## 3. Label-class assignment (TCGA-OV studies)

| Paper | Label class | Basis |
|---|---|---|
| Villalobos 2018 | **platinum-free interval from end of platinum** (3-level: sensitive / resistant / refractory), re-derived by the authors; plus RECIST first-course response as a separate stratifier | p. 4 definitions; last platinum dose as reference |
| Yang SYC 2018 | **other** — compound: OS 6 mo–2 y AND primary platinum resistance AND progression ≤ 6 mo from completing platinum (ST); OS ≥ 10 y AND durable sensitivity (LT) | p. 2; how TCGA fields were used: not stated |
| Gonzalez Bosquet 2016 | **platinum-free interval from end of platinum** (binary at 6 mo; refractory pooled with resistant), as inherited from their 2014 paper; wording mixes "after the first platinum-based treatment" and "treatment completion" | p. 2 |
| Gonzalez Bosquet 2021 | **platinum-free interval from end of platinum** (binary at 6 mo after completing chemo; refractory pooled) | p. 2, p. 5 |
| Choi 2020 | **platinum-free interval from end of platinum** with excluded 6–12 mo band (< 6 R, > 12 S) | p. 3 |
| Kilim 2025 | **other** — first-course refractory (progression/SD within 6 cycles) vs 2-year progression-free; follows Chowdhury 2023 | p. 8 |
| Guo & Li 2021 | **platinum-free interval from end of platinum** (relapse ≤ 6 mo after completion = R; remission and relapse > 6 mo = S) | p. 8239 |
| Wang C 2024 | **not stated** for TCGA (counts 90/197 match the TCGA platinum-status field, so probably **TCGA platinum status field**, inferred) | p. 4355 |

Comparison with G5: Li 2022 and Gao 2025 (287 = 90 + 197) and now Wang C 2024 all appear to use the TCGA 2011 platinum-status field; Chen 2022 (69/161 of 230) and Choi 2020 (110/160 of 270, then 99/135) recomputed intervals from clinical dates; Gonzalez Bosquet 2016 (158/292 of 450), Gonzalez Bosquet 2021 (149/189 of 338) and Guo & Li 2021 (49/205 of 254) report class counts that match none of the above, implying their own derivations with different inclusion rules. Resistant fraction ranges from 19% (Guo & Li) to 44% (GB 2021) in the same source cohort.

---

## 4. Overlap with the manuscript's planned analyses (C1–C4)

### Villalobos 2018
- **C1 — coverage of candidate labels in the same TCGA-OV patients: No.** The paper reports only its own categories (212 / 91 / 28 in the high-risk set; RECIST 249 / 53 / 27 / 32) and "Insufficient data" counts for chemotherapy lines (Table 2). It does not report how many patients carry TCGA's platinum-status value, how many have a computable PFI, or how many have both. The 119 high-risk patients without a platinum category are not enumerated or explained.
- **C2 — agreement between labels, or OS thresholds as tests for platinum resistance: No.** No κ, no cross-tabulation, no mention of the TCGA PLATINUM_STATUS field. The only between-label statement is qualitative: "These OS data for platinum sensitivity correlate closely with the documented RECIST responses to treatment." (p. 6). OS is treated only as an outcome.
- **C3 — BRCA/CCNE1 or other markers against each label: No.** BRCA1/2 mutation is tested against OS and TTF (HR 0.52/0.53 for OS; HR 0.65, 0.64, 0.76 for TTF by line; p. 7, Fig 4, A4, A5), not against platinum category or RECIST category. CCNE1 is not mentioned.
- **C4 — classifiers trained on alternative labels: No.** No model of any kind is fitted; the paper is descriptive (KM, log-rank, t test).
- What it does provide that the manuscript can use: (i) a third re-derived PFI-type label for TCGA-OV with a published Data Supplement; (ii) OS medians by category (56.6 / 27.0 / 11.6 mo) as an external check on the manuscript's OS-by-label figures; (iii) a documented gap between definitions (progression-based on p. 4 vs treatment-reinitiation-based on p. 7); (iv) explicit statement that PFS per regimen is not documented in TCGA and had to be inferred from therapy start dates (p. 2).

### Yang SYC 2018
- **C1: No.** Reports 214/603 stage III with complete OS, then 60 ST and 10 LT; does not report how many had platinum-status or PFI information independently of the compound criterion.
- **C2: No.** Does not compare OS-only with platinum-only labels and does not report patients meeting one criterion but not the other; no κ.
- **C3: Partly, but against a compound label, not against separate labels.** CCNE1 gain (PM: 4/19 ST vs 2/20 LT, p. 9–10; TCGA LT 1/10), BRCA1/2 inactivation, HRD-LOH, mutation burden (TCGA Fig 1b) and immune scores (TCGA Fig S11) are compared between ST and LT. Because ST requires both OS < 2 y and platinum resistance, these results cannot separate the OS and platinum components.
- **C4: No.** No classifier.
- Relevance: it is the published precedent for a label that fuses OS with platinum resistance; the manuscript can cite it as such while noting that it does not evaluate the fusion.

### Other papers (brief)
- Gonzalez Bosquet 2016/2021, Choi 2020, Guo & Li 2021, Wang C 2024, Kilim 2025: none reports label coverage across alternative definitions, none measures agreement between labels, none evaluates OS thresholds as resistance tests, and none trains a classifier on more than one label definition. GB 2016 tests FIGO stage and "optimal treatment" (p < 0.001) against its CR/IR label and finds "optimal treatment" the only predictor of misclassification (p. 10), which is a partial C3-type observation on a clinical covariate. GB 2021 tests BRCA1/2 variants against responder status in the UI cohort only (p = 0.06 and 0.52; p. 6). Kilim 2025 tests HRD-score, HRDetect, Signature 3 and BRCA status against its refractory/sensitive label in 98 TCGA cases (p. 5), the closest C3 analogue, but with a non-PFI label.
- Talijanovic 2025 catalogues 12 definitions but performs no agreement analysis; its recommendation that TCGA barcodes and the applied definition be published (p. 22) is directly aligned with the manuscript's aim and can be cited as motivation.

---

## 5. Points that may contradict or qualify statements in the manuscript

1. **"Villalobos re-annotated 587 TCGA patients and compared with TCGA's platinum status"** — the second half is not supported. They re-annotated 587/450 but never compare with PLATINUM_STATUS or report agreement.
2. **Markman 1991 as the source of the 6-month rule** — not supported; the paper excluded intervals ≤ 4 months and its bins start at 5–12 months. It supports the interval-from-last-platinum reference and the response gradient only.
3. **Talijanovic's count of undefined studies** — the paper itself gives both "seven" (p. 16) and "25% (n=11)" (p. 22). Quote one with the page and note the discrepancy rather than choosing silently.
4. **Yang SYC's TCGA denominator** — "60 of 288" (p. 3) is inconsistent with "214 of 603" and with 28%; downstream analyses use 40/8 and 32/8, not 60/10.
5. **"PFI" in Talijanovic Table III** is expanded as progression-free interval; if the manuscript equates it with platinum-free interval, say so explicitly.
6. **Gonzalez Bosquet 2016's n = 450** is not Villalobos's 450 high-risk set (GB includes stage I–II and grade 1–2 patients, Table 1 p. 2).
7. **Yousefi 2019** supports "OS is noisy because of non-cancer deaths" verbatim, but it is a pan-cancer arXiv preprint that does not analyse TCGA-OV; cite accordingly.
8. **Kilim 2025** is not an mRNA-expression classifier (proteomics + histology) and does not use a 6-month PFI label; if listed among expression classifiers it needs a footnote.
