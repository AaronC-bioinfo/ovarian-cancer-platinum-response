# Coverage, agreement and provenance of candidate platinum-response labels in TCGA-OV

Aaron Michael Anuroop Chintala¹*

Short title: Platinum-response labels in TCGA-OV

¹ School of Systems Biology, George Mason University, Manassas, VA, USA

\* Corresponding author: aaronmichael1489@gmail.com (AMAC)

ORCID (AMAC): 0009-0009-0062-6453

## Abstract

Studies using The Cancer Genome Atlas ovarian cancer cohort (TCGA-OV) to predict platinum response define their outcomes in different and often incompletely reported ways. We compared five candidate labels in 489 platinum-treated patients: TCGA's published platinum status, a platinum-free interval re-derived from the TCGA Clinical Data Resource, first-course response, and death before 18 or 24 months. The overall-survival (OS) thresholds, from our earlier analyses, were evaluated as candidate surrogates. Platinum status was available for 277 patients (57%) and agreed closely with the re-derived interval where both were available (κ 0.97). Of the 117 patients added by re-derivation, 78 had no specified provenance flag. Adding these patients yielded a candidate combined label covering 355 patients (99 resistant), with only 2 additional resistant patients who had RNA-seq data. The 18- and 24-month OS thresholds flagged 21% and 39% of platinum-resistant patients. Among flagged patients with a known status, 82% and 74% were resistant, compared with 31–32% expected without platinum information; about half of flagged patients had no status. Across thresholds from 6 to 60 months, agreement with platinum status was at best moderate (highest κ 0.47, at 36 months). *BRCA1/2* variants and *CCNE1* amplification showed associations in the same direction under every label and did not distinguish between them. Expression classifiers predicted four training labels with AUCs of 0.61–0.68. In the same 134 patients and folds, platinum-trained and 24-month-OS-trained models showed no detectable difference in predicting platinum status (AUC difference −0.005; 95% conditional interval −0.105 to +0.087). Refitting the whole pipeline left this comparison inconclusive. We release a versioned patient-level table documenting each label and the provenance of every re-derived call. These findings support explicit reporting of label definitions, class sizes and provenance, the use of platinum-specific labels for what they measure, and the interpretation of OS thresholds as survival end-points.

## Introduction

High-grade serous ovarian cancer (HGSOC) is usually diagnosed at an advanced stage and treated with cytoreductive surgery and platinum-based chemotherapy [@tcga2011]. Many patients subsequently relapse with platinum-resistant disease. A pre-treatment genomic test of platinum response has yet to enter routine use, although the TCGA-OV cohort [@tcga2011] has supported numerous studies of expression-based prediction (Table 1). A meta-analysis reported pooled concordance indices of 0.81 in training and 0.83 in validation cohorts for machine-learning models of platinum response [@wangq]. The outcomes behind such models vary. An earlier systematic review of chemoresistance prediction found that studies used overall survival, progression-free survival and chemotherapy response as end-points, with most predicting survival or prognosis rather than treatment response [@lloyd].

The outcome label defines what a classifier learns to predict. In clinical practice, the time since the last platinum dose predicts response to re-treatment [@markman]. A six-month cut-off has conventionally defined platinum resistance, including in TCGA's published status [@tcga2011]. The Gynecologic Cancer InterGroup subsequently adopted the therapy-free interval in place of this dichotomy for trial design [@wilson17], although binary classifiers still require a two-class outcome.

TCGA-OV offers several candidate labels: platinum status from the 2011 release, a platinum-free interval re-derived from the TCGA Clinical Data Resource (TCGA-CDR) [@liu], and response after first-line therapy. Thresholds on overall survival (OS), the cohort's most complete outcome, can also be evaluated as candidate surrogates. Other studies have used composite groups, including short-term survivors defined by OS of 6 months to 2 years, primary platinum resistance and progression within six months of completing platinum [@yangsyc]. A review of 44 expression studies identified 12 definitions of platinum resistance [@talijanovic].

We examine the 18- and 24-month OS thresholds because our earlier classifier used them [@chintala2026]. None of the TCGA-OV studies in our non-systematic review used an OS threshold (Table 1), so these thresholds should not be taken as established practice. Reporting guidelines require an explicit outcome definition, and risk-of-bias tools assess the outcome as a distinct domain [@tripod; @probast]. Only 4 of 39 platinum-response models in the meta-analysis were at low risk of bias in that domain [@wangq]. Whether a label measures the intended construct therefore requires consideration separately from how accurately a model predicts it [@jacobs].

Previous work re-annotated TCGA-OV treatment outcomes and related platinum sensitivity and first-line response to OS [@villalobos]. Cocchi et al. compared platinum-free-interval categories from that re-annotation with the original TCGA annotation. They found that differences in patient selection, platinum-sensitivity definitions, data sources and analytical pipelines limited the reproducibility of reported genes [@cocchi]. The TCGA-CDR generally favours the progression-free interval for pan-cancer analyses, while recommending all four of its end-points, including OS, for TCGA-OV [@liu]. OS also includes non-cancer deaths and has consequently been described as a noisy label [@yousefi]. In cell lines, label choice has been shown to affect drug-response prediction [@bayer].

Within the literature we reviewed, no study compared agreement across platinum-based, survival-based and response-based labels in the same TCGA-OV patients. Nor did we find a study evaluating OS thresholds as tests for platinum resistance, comparing the outcomes predicted by classifiers trained on each label, or releasing a patient-level table that documented the provenance of every call.

We examined how candidate labels differ when used to train a platinum-response classifier in TCGA-OV. Our questions concerned patient coverage, resistance assignments and the records supporting re-derived calls; associations with characteristics linked to platinum response and prognosis; and the outcomes predicted by expression classifiers trained on each label. The study compares labels rather than evaluating individual published studies.

## Materials and methods

### Data and cohort

We obtained clinical, treatment, mutation, copy-number and expression data from cBioPortal [@cerami; @gaoj] and the TCGA-CDR [@liu]. The cBioPortal sources were the PanCancer Atlas 2018 release (`ov_tcga_pan_can_atlas_2018`) and the TCGA 2011 release (`ov_tcga_pub`). Of 585 patients in the PanCancer Atlas clinical file, 496 had a treatment-timeline record. Carboplatin or cisplatin was recorded for 489 patients, who formed the study cohort (S4 Table). We excluded 89 patients whose treatment could not be established because no treatment record was available, and 7 whose records contained neither agent and were therefore classified as not platinum-treated.

RNA-seq data were available for 251 platinum-treated patients. Expression values were RNA-Seq by Expectation-Maximization (RSEM) estimates from the PanCancer Atlas release. This secondary analysis used publicly available, de-identified TCGA data released under its consent and governance procedures; no further ethics approval or consent was required.

### Labels

We constructed five labels for the 489 patients, coding non-response or resistance as 1 and the alternative outcome as 0. We also constructed two combinations of the platinum labels (Table 2).

*Platinum status.* We used TCGA's published status from `ov_tcga_pub` without modification [@tcga2011]. Its definition states: “Platinum status was defined as resistant if the platinum free interval was less than six months and the patient had progressed or recurred” [@tcga2011, Supplementary Methods S1, pp. 2–3]. Sensitive tumours had an interval of six months or more. Patients without progression were excluded if follow-up after the last dose was shorter than six months. We treated “Tooearly”, missing status and absence from the 2011 release as undetermined.

*Platinum-free interval from first-line platinum.* We re-derived the interval by subtracting the latest stop date of platinum regimens with an adjuvant indication from the TCGA-CDR progression-free interval time [@liu]. Both dates were measured in days from diagnosis. Treatment-timeline rows were selected when the agent name contained “platin”, which also includes oxaliplatin. Restricting the anchor to carboplatin and cisplatin changed no resistant or sensitive classification among patients determinate under both rules. It left 2 patients undetermined, including 1 of the 78 unflagged additions.

Progression within less than 183 days after platinum ended was classified as resistant; an interval of 183 days or more was classified as sensitive. Patients censored before 183 days were undetermined. We classified 8 patients whose recorded progression preceded the end of platinum as resistant and left 11 patients censored before the end of platinum undetermined. TCGA-CDR treats death with tumour as a progression event and dates progression using new-tumour-event records [@liu].

Three alternative anchors changed 0 to 5 calls among patients determinate under both anchors (κ with the primary label about 0.97). All 78 unflagged additions remained determinate with unchanged classifications (S1 Text; S11 Table). The broad combined label retained platinum status wherever determinate and used the re-derived interval otherwise.

*Provenance audit and combined labels.* After the main results were known, we audited the records supporting every re-derived call. Each resistant call was traced to a recorded new tumour event (recurrence or progression) or a death counted as progression. We flagged redacted TCGA-CDR records, adjuvant platinum regimens without a stop date, and later-line regimens starting after platinum ended but before the recorded event. For sensitive patients, the later-line flag applied within 183 days of the end of platinum. We also flagged intervals of 150–215 days. This window was specified before the audit to identify classifications that a dating error of about a month could reverse; a flag did not establish that a record was incorrect.

Patients with no applicable flag were classified as unflagged (clean_resistant or clean_sensitive in the label table). Resistant calls dated only by death could not enter this group, and negative intervals formed a separate class. Unflagged status therefore records the absence of specified concerns; it does not verify the call's accuracy.

The provenance-filtered combined label retained determinate platinum status and added re-derived calls only for unflagged patients. It appears as the “strict combined label” in S1 Text and as label_combined_strict in the label table. We used it in the released table and as a combined reference for evaluating OS thresholds. Other analyses used platinum status, the re-derived interval or the broad combined label. Since the filter applies only to additions, the original and added calls are subject to different quality requirements, and the extension's accuracy remains unverified.

A rule fixed before the audit specified that the filtered label would become the preferred combination if more than 20% of additions could not be classified as unflagged. That condition was met, and the broad label became a sensitivity analysis. We also report the combination without the 150–215-day flag (367 patients; label_combined_strict_asrun) as a further sensitivity analysis.

*First-course response.* We compared stable or progressive disease with complete or partial response after primary therapy. Sources were used in the following order: the TCGA-CDR treatment-outcome field, `ov_tcga_pub`, and the PanCancer Atlas timeline. We fixed this order after observing agreement in 365 of 365 and 141 of 142 shared patients across the three sources.

*OS thresholds.* We compared death before 18 or 24 months from diagnosis with survival beyond each threshold, excluding patients censored earlier. Our previous classifier defined platinum response as survival beyond 12, 18 or 24 months [@chintala2026]. The present study replaces that interpretation by evaluating these thresholds as candidate survival surrogates for platinum resistance. No OS threshold appeared in our literature sample (Table 1). Results for the 12-month threshold are included in the Supporting information.

### Coverage and agreement

We compared patients with and without determinate platinum status on overall survival using Kaplan–Meier medians and the log-rank test. Fisher's exact test was used for death before 18 and 24 months, the re-derived interval and first-course response. For each pair of labels, we calculated Cohen's κ among patients with both labels determinate [@cohen], with 95% intervals from 2,000 patient bootstrap resamples. We also calculated the maximum κ attainable given the marginal frequencies.

The 18- and 24-month thresholds were assessed as tests for platinum resistance against published platinum status. We estimated sensitivity, specificity, positive predictive value (PPV) and negative predictive value, with Wilson 95% intervals [@wilson27]. Exploratory analyses added after internal review extended this assessment to every threshold from 6 to 60 months. For comparison, we calculated the values expected when the OS label carried no platinum-status information: PPV equal to resistance prevalence and specificity equal to the proportion not flagged. We also calculated the highest sensitivity allowed by the label's prevalence and bounded the results by assigning all OS-labelled patients without platinum status first to resistant and then to sensitive.

Patients censored before a threshold have no OS label. To examine the effect of this exclusion, we re-estimated the measures with inverse-probability-of-censoring weights (IPCW) [@vock]. We used both Kaplan–Meier weights and a Cox censoring model with age, stage IV and residual disease (S1 Text).

### Associations with characteristics linked to platinum response and prognosis

Among the 272 sequenced platinum-treated patients in the 2011 release, we defined *BRCA1/2* carriers by a germline or somatic truncating or splice-site variant. This identified 55 carriers, including 44 with a germline variant. Germline calls came from the 2011 release because the public PanCancer Atlas mutation file contains somatic calls only. *CCNE1* amplification was defined by a GISTIC call of 2 in the same release.

We tested each label against residual disease after surgery (more than 1 cm versus less, following TCGA [@tcga2011], and alternatively any versus none), stage IV disease, Aneuploidy Score, tumour mutational burden (TMB) and age. Binary characteristics were analysed with Fisher's exact test and conditional odds ratios (OR) for non-response. For continuous characteristics, we used the Mann–Whitney U test and rank-biserial correlation (r). Benjamini–Hochberg adjustment [@bh] was applied within each label to the P values for the five pre-specified clinical and tumour characteristics.

Direct comparisons used patients with determinate platinum status and both OS thresholds. We estimated differences in log OR for *BRCA1/2* and residual disease and in r for aneuploidy, with 95% intervals from 2,000 patient bootstrap resamples. A Haldane correction added 0.5 to every cell to avoid discarding resamples. As an exploratory assessment of sensitivity to differences, we used each interval to approximate the smallest difference detectable with 80% power; this was not an estimate of achieved power.

### Classifiers

We fitted logistic regression with an L2 penalty, a random forest with 300 trees, and a radial-basis-function support vector machine (SVM). Models used balanced class weights and fixed seeds in scikit-learn 1.9.0 [@sklearn]; S1 Text lists analyses run in version 1.7.2. Expression was transformed as log2(RSEM + 1) and restricted to the 15,994 genes also measured on the external platform. Within each training set, we selected the 500 highest-variance genes and estimated the standardisation parameters.

*All-patients analysis.* For each of four training labels (Fig 3A, rows), we trained and evaluated models among the 251 patients with RNA-seq data using five-fold stratified cross-validation repeated five times. Pooled out-of-fold scores were evaluated against every label, giving a matrix of AUCs by training and test label. We report the mean across three models and five repeats, with the range. The matrix describes predicted outcomes; it does not identify the biological information used by the models. Differences in eligible patients and class balance make these comparisons descriptive. S1 Text gives the pre-specified decision rule.

*Controlled comparison.* After the main results were known, we added a comparison in the 134 patients with RNA-seq data and determinate platinum status, OS at 18 months and OS at 24 months. The same pipeline was trained on each label using identical outer folds: five-fold cross-validation stratified on platinum status and repeated 20 times. The primary contrast was the difference in AUC for predicting platinum status between platinum-trained and 24-month-OS-trained models (platinum-trained minus OS-trained). Each model's difference was calculated from its own predicted probabilities and then averaged across the three models. We calculated two secondary contrasts in the same way: platinum-trained minus 18-month-OS-trained models for platinum status, and 24-month-OS-trained minus platinum-trained models for OS at 24 months.

Conditional 95% intervals used 2,000 patient bootstrap resamples stratified by the target label. They were calculated from out-of-fold scores averaged over repeats, without refitting. In a separate sensitivity analysis, we refitted the entire pipeline in 500 bootstrap samples drawn within platinum-status groups and evaluated it on patients not drawn. These single fits use about 63% of the distinct patients and estimate a different quantity from repeated cross-validation. We therefore report their out-of-bag median and percentile range separately.

### Exploratory analyses

We added three exploratory analyses after the main results were known (S1 Text). The first divided overall survival into the platinum-free interval and survival after progression among patients who progressed. Each outcome was modelled with univariable Cox regression on age, stage, residual disease, *BRCA1/2*, *CCNE1* and Aneuploidy Score. The platinum-free interval began at the end of first-line platinum and included the 408 patients still at risk at that point, with intervals above 0 days. A sensitivity analysis set the 28 intervals of 0 days or less to 1 day (S10 Table). Survival after progression was calculated by subtracting the TCGA-CDR progression-free interval from overall survival; patients whose progression event was death were excluded. We did not formally compare the two models. A rank-based proportional-hazards test gave P < 0.05 in 2 of 14 models: age for the platinum-free interval and Aneuploidy Score for survival after progression. These two hazard ratios require cautious interpretation. Adding a quadratic term detected no non-linearity for either continuous covariate (P ≥ 0.28; S1 Text).

The second analysis assessed prediction from clinical characteristics alone. It used logistic regression with age, stage IV and residual disease (> 1 cm), evaluated by five-fold cross-validation repeated five times. The third recomputed the re-derived interval after excluding the 38 patients whose TCGA-CDR records were marked as redacted.

### Supplementary analyses

We transferred the TCGA-trained classifiers to GSE63885 [@lisowska], an independent microarray cohort restricted here to serous and undifferentiated tumours (80 samples). Genes were z-scored within GSE63885, making this an assessment of transfer to a batch of samples; it does not represent a frozen pipeline applied to individual new patients. S7 Table provides verbatim label definitions, sample identifiers and probe mapping. Its platinum-resistance label used disease-free survival < 180 days (34 resistant, 40 sensitive), and its clinical-response label compared stable or progressive disease with complete or partial response (10 of 74). S1 Text reconciles these counts with the original publication and Chen et al. Differences in transfer performance cannot be assigned solely to the training label.

We also used the 10 genes of Chen et al. [@chen] and the 5 genes of Gao et al. [@gao] as fixed inputs to our pipeline. Each set was compared with 1,000 random sets of the same size drawn from the 15,484 common genes with complete data. Both published sets were selected using data that included TCGA-OV patients, giving them an advantage in TCGA. This experiment assesses transfer of the gene sets; the original models were neither replicated nor tested.

Finally, we quantified AUC inflation when genes were selected on the full dataset before splitting, a documented source of bias [@ambroise; @vabalas; @teschendorff; @whalen]. This analysis used OS-threshold labels and the pipeline's simpler preprocessing, with untransformed RSEM values for all 20,531 genes.

### Literature review

An initial search and a targeted search identified studies of expression-based platinum-response prediction using TCGA-OV [@chen; @gao; @gonzalez; @sunj; @choi; @gb2021; @sunx; @guoli; @li; @wangc24; @kilim; @wangc]. From their full texts and supplements, we extracted label definitions and sources, class sizes, validation designs and reported discrimination. Missing information was recorded as “not stated”; definitions were not inferred. The searches were non-systematic, and their databases, dates and search terms were not recorded. The selection is therefore illustrative and cannot be reproduced. Statements that no study used a particular approach refer only to this sample.

### Pre-specification

Predictions and decision rules were recorded in script headers before the corresponding analyses ran, with exceptions documented in S1 Text. Scripts for five analyses were deposited in the public repository before execution: *BRCA1/2* and *CCNE1*, patients without platinum status, full-cohort prognostic characteristics, provenance, and the controlled classifier comparison (commits d5bd844, e98b3d9 and d349b2b). Other headers are archived with the code but have no external timestamp.

The timing of specification varied. Initial label-analysis predictions were written before those analyses but after the author's earlier work on the cohort. Secondary predictions for the five deposited analyses were written after earlier study results were available and may have been informed by them. Post hoc analyses with decision rules included the restricted survival decomposition and the anchor, censoring-weight, event-type and out-of-bag sensitivity analyses. Other exploratory or descriptive analyses had no predictions. No hypothesis preceded all inspection of TCGA-OV data; the commit timestamps establish the order of writing and execution only. The descriptive full-cohort tables and exploratory analyses were added after the main results were known.

Two material deviations occurred. The provenance-audit code omitted the pre-specified 150–215-day flag. The reported label comes from a correction run that added only this flag. The out-of-bag analysis also departed from its pre-specified rule, which designated its range as the main uncertainty measure, because that analysis estimates a different quantity. S1 Text documents analysis identifiers (A1–A23), predictions, outcomes including failed predictions, software environments and development history. Reporting follows STROBE [@strobe] and, for OS thresholds evaluated as tests, STARD 2015 [@stard] (S2 Text).

### Use of AI tools

Generative AI tools were used for three tasks only: debugging and testing code, rephrasing manuscript text and the literature search. Claude (Anthropic) was used to debug and test code; ChatGPT (OpenAI) was used to rephrase manuscript text; and Perplexity was used to search for candidate studies for the literature review. AI tools were not used to generate or alter data. Code changes were checked by rerunning the affected scripts and the test suite, rephrased text was checked against its intended meaning, and every label definition, class size and reported result taken from a study was verified against its full text and supplements. The author takes full responsibility for the content of this article.

## Results

### Studies label patients in different ways

The twelve studies of expression (mRNA or protein) and platinum response using TCGA-OV or a cohort analysed alongside it used at least five label constructions. None used an overall-survival threshold (Table 1). Five defined resistance by progression or recurrence within six months of platinum or chemotherapy completion, with different reference points and exclusions for intermediate patients [@chen; @gonzalez; @choi; @gb2021; @guoli]. One compared platinum-refractory disease with no progression within two years [@kilim], and another used progression-free survival as a surrogate [@sunx]. Two reported class sizes matching TCGA's published platinum status (90 resistant, 197 sensitive) without supplying a definition [@li; @wangc24]. Four studies incompletely described their TCGA labelling [@gao; @sunj; @li; @wangc24]. Across this illustrative sample, 19% to 44% of TCGA patients were labelled resistant (S1 Table).

### Platinum status covers just over half of treated patients

Published platinum status was determinate for 277 of 489 platinum-treated patients (57%; 87 resistant, 190 sensitive), including 145 of the 251 patients with RNA-seq data (Fig 1A, Table 2). The other 212 patients had missing status (87), were too early to classify (57), or were absent from the 2011 release (68).

Within the 2011 release, median overall survival was 47.5 months for patients without determinate status and 47.7 months for those with status (log-rank p = 0.37). The former group was heterogeneous: patients with missing status had a median survival of 39.0 months, whereas only 10 of 57 patients classified as too early had died. Patients without status were more often dead before 18 months (16 of 96 versus 22 of 268; OR 2.23, 95% CI 1.04–4.70). The corresponding difference at 24 months was less clear (24 of 95 versus 43 of 259; OR 1.70, 95% CI 0.92–3.09). Stable or progressive disease after first-line therapy was also more common without status (28 of 114 versus 28 of 255; OR 2.63, 95% CI 1.41–4.91), while resistance by the re-derived interval was less common (13 of 68 versus 89 of 272; OR 0.49, 95% CI 0.23–0.96; S4 Table).

The re-derived interval was determinate for 389 patients. Excluding redacted TCGA-CDR records reduced this to 358, with almost no change in κ with platinum status (S10 Table). Table 2 reports coverage for all labels.

Of the 389 patients with a re-derived interval, 272 also had published platinum status. Re-derivation added 117 patients, including 26 classified as resistant. Among these 26 resistant calls, 20 were dated by a recorded new tumour event and 6 by death counted as progression (S11 Table).

The audit classified 78 additions as unflagged (12 resistant, 66 sensitive) and 39 otherwise. Counting each patient once, the latter group comprised 1 negative interval, 6 resistant calls dated only by death, 20 other record problems, and 12 intervals flagged solely for falling within 150–215 days (Fig 1D, S11 Table). Other record problems included redacted TCGA-CDR records, adjuvant platinum without a stop date, and a later-line regimen before the event. Omitting the near-threshold flag adds exactly those 12 patients.

All four disagreements between the platinum labels involved a patient classified as sensitive by TCGA and resistant by re-derivation. One interval was near the cut-off (154 days). The other three (18, 101 and 148 days) had recorded recurrence and no flag. The 101-day case became sensitive under two of three alternative anchors, although those anchors introduced other disagreements. Available records did not explain the remaining two cases (S11 Table). In addition, 2 of the 12 unflagged resistant additions were supported by a new tumour event of unrecorded type.

Excluding the 10 resistant calls dated solely by death (6) or by an event of unrecorded type (4, including the 2 above) changed OS-threshold sensitivity and PPV against the broad combined label by at most 0.04. *BRCA1/2* and *CCNE1* odds ratios changed by at most 0.05, with no change in whether their intervals included 1 (S11 Table).

The provenance-filtered combination covered 355 patients (99 resistant, 256 sensitive; Fig 1A), compared with 367 (104 resistant) when the 150–215-day flag was omitted. Its gain for expression classifiers was limited: it added 22 patients with RNA-seq data, only 2 resistant, increasing coverage from 145 to 167 and the resistant count from 41 to 43. S11 Table reports its OS-threshold test characteristics.

### OS thresholds agree at best moderately with platinum status

The published and re-derived platinum labels agreed in 268 of 272 patients with both available (κ 0.97, 95% CI 0.93–0.99; Fig 1B). Agreement with platinum status was much lower for the OS thresholds: κ was 0.24 (0.14–0.35) at 18 months and 0.37 (0.25–0.49) at 24 months. The maximum attainable values were 0.33 and 0.59, respectively.

At 18 months, the OS threshold flagged 18 of 84 resistant patients (sensitivity 0.21, 0.14–0.31) and 4 of 184 sensitive patients (specificity 0.98). At 24 months, it flagged 32 of 83 resistant patients (0.39, 0.29–0.49) and 11 of 176 sensitive patients (specificity 0.94; Fig 1C). The small number of early deaths constrains these measures. Even without platinum-status information, these labels would have specificities of 0.92 and 0.83; their prevalence limits sensitivity to at most 0.26 and 0.52.

Among flagged patients with known status, 18 of 22 at 18 months (PPV 0.82, 0.61–0.93) and 32 of 43 at 24 months (0.74, 0.60–0.85) were resistant. These proportions exceeded the values of 0.31 and 0.32 expected without platinum information. However, status was unavailable for 25 of the 47 patients flagged at 18 months and 35 of the 78 flagged at 24 months. Assigning all of these patients to sensitive or resistant bounded PPV at 0.38–0.91 and 0.41–0.86, respectively. The estimates also excluded patients censored before each threshold (8 and 17 with platinum status) and 1 platinum-sensitive patient who died without a recorded survival time (S2 Table).

Censoring weights changed sensitivity, specificity and PPV by at most 0.04 (S1 Text). Kaplan–Meier weights assume censoring is unrelated to outcome; Cox weights make that assumption conditional on age, stage and residual disease. Estimating censoring only among patients with status, or separately within each status group, changed results by at most 0.01. Missing platinum status remains unresolved by this weighting.

In the exploratory sweep from 6 to 60 months, sensitivity increased as specificity and PPV decreased. Agreement peaked at 36 months (κ 0.47; sensitivity 0.64, specificity 0.83, PPV 0.65; S2 Table). The two OS thresholds agreed with one another at κ 0.71. First-course response showed weak agreement with every other label (κ 0.21–0.26).

### Characteristics linked to platinum response point the same way under every label

*BRCA1/2* carriers were less often classified as non-responders under every label (Fig 2A, Table 3). For platinum status, the counts were 7 of 37 carriers and 54 of 149 non-carriers (OR 0.41, 95% CI 0.14–1.04). Corresponding results were 8 of 47 versus 64 of 179 for the re-derived interval (0.37, 0.14–0.87), 1 of 51 versus 23 of 195 for OS at 18 months (0.15, 0.004–0.97), and 3 of 50 versus 43 of 192 for OS at 24 months (0.22, 0.04–0.75). The first-course-response estimate was imprecise (0.64, 0.18–1.80).

In the 180 patients with all three relevant labels determinate, the difference in log OR between platinum status and the OS threshold was +1.12 (95% CI −0.16 to +2.00) at 18 months and +0.95 (−0.52 to +2.71) at 24 months. The approximate minimum detectable ratios of odds ratios were 4.7 and 10. These comparisons could therefore detect only large differences and do not establish similar behaviour across labels (S3 Table). *CCNE1* amplification was associated with non-response in the same direction under all labels (OR 1.11–2.01; Fig 2B).

Residual disease > 1 cm was associated with non-response under both OS thresholds (OR 2.86, 1.30–6.29, and 2.41, 1.28–4.50) and first-course response (2.55, 1.31–4.91). The estimate for platinum status was 1.12 (0.59–2.09). Using any residual disease versus none gave associations with platinum status (3.22, 1.40–8.35), the re-derived interval (3.04, 1.44–7.03) and OS at 24 months (2.78, 1.12–8.29; Fig 2C, Table 3).

Aneuploidy Score was higher in non-responders under both OS thresholds (r = 0.20 and 0.25) and the re-derived interval (r = 0.21), with a weak association under platinum status (r = 0.13, q = 0.26; Fig 2D). In comparisons restricted to the same patients, no contrast between platinum status and the OS thresholds for these characteristics could be distinguished from zero. Only large differences were detectable (S5 Table, including raw P values).

Older age was associated with both OS thresholds (r = 0.26 and 0.28) but not with platinum status (r = 0.07). The association at 24 months had been predicted in advance for patients with RNA-seq data (S1 Text). First-course response had no clear association with aneuploidy (r = −0.03). Taken together, these characteristics did not distinguish the candidate labels in this cohort.

### Exploratory: associations with the platinum-free interval and with survival after progression

In the exploratory survival decomposition, 408 patients were at risk at the end of platinum (S10 Table). *BRCA1/2* carriers had a longer platinum-free interval (hazard ratio 0.55, 95% CI 0.38–0.79). *CCNE1* amplification (1.58, 1.19–2.09) and higher Aneuploidy Score (1.23 per SD, 1.10–1.38) were associated with a shorter interval. These characteristics showed weaker or no associations with survival after progression (Fig 4).

Age and residual disease > 1 cm were associated with shorter survival after progression (1.26 per 10 years, 1.12–1.42; and 1.41, 1.03–1.93), with less clear associations for the platinum-free interval (1.09, 0.98–1.20; and 1.08, 0.82–1.41). Setting excluded intervals to 1 day changed no hazard ratio by more than about 0.03 and did not change the conclusions. Any residual disease was associated with both outcomes. These differences in the clarity of associations remain descriptive because the two models were not formally compared.

A separate logistic regression using age, stage and residual disease predicted death before 18 and 24 months with cross-validated AUCs of 0.64 and 0.62. Discrimination was near chance for platinum status (0.48), the re-derived interval (0.52) and the broad combined label (0.49).

### Classifiers trained on each label predict modestly

Within TCGA, mean cross-validated AUC was 0.63 for platinum status (range across models and repeats 0.56–0.69; S6 Table), 0.61 for the re-derived interval, 0.63 for OS at 18 months and 0.68 for OS at 24 months (Fig 3A). Models trained on the OS thresholds predicted platinum status with AUCs of 0.55 and 0.60. Platinum-trained models predicted OS at 24 months with an AUC of 0.63. Because the eligible patients and class balance differed across labels, this matrix provides a descriptive comparison.

The controlled comparison included 134 patients, 39 platinum-resistant, with identical folds for every training label (Fig 3B). The AUC difference between platinum-trained and 24-month-OS-trained models for predicting platinum status was −0.005 (conditional 95% interval −0.105 to +0.087). For the comparison with 18-month-OS-trained models, the difference was +0.080 (−0.045 to +0.201); only 7 positives contributed to that OS label, making the comparison particularly unstable (S6 Table). On the 24-month OS outcome, 24-month-OS-trained models showed no demonstrated improvement over platinum-trained models (difference −0.069, −0.236 to +0.081). These intervals account for patient resampling with the fitted predictions held fixed.

Refitting the entire pipeline in the separate out-of-bag analysis gave median differences of +0.01 (2.5th–97.5th percentiles −0.18 to +0.16), +0.06 (−0.15 to +0.24) and −0.004 (−0.23 to +0.22) for the three contrasts (Fig 3B). Each replicate evaluated a single fit on an average of 49 patients, sometimes with only one positive for the 24-month OS label. These ranges measure variability across single refits and are not confidence intervals for the cross-validated estimates. Neither analysis demonstrated a clear difference between training labels (S1 Text).

Transfer to GSE63885 yielded weak discrimination of its platinum-resistance label across all training labels (mean AUC 0.56–0.63). For clinical response, with 10 non-responders, the AUCs were 0.67 and 0.71 for models trained on platinum labels and 0.49 and 0.52 for OS-trained models. This comparison was not pre-specified and has no uncertainty interval, so it is descriptive (S1 Fig, S7 Table).

In the gene-set transfer experiment, Chen et al.'s 10 genes separated platinum-resistant and sensitive TCGA patients better than random sets (AUC 0.735), but did not do so in GSE63885 (0.499). Gao et al.'s 5 genes did not differ from random sets (S8 Table). Selecting genes before splitting the full dataset increased mean AUC at the 18- and 24-month thresholds by +0.21 for supervised selection and +0.006 for unsupervised selection (S2 Fig, S9 Table).

## Discussion

The choice of label changes both the patients available for analysis and the outcome a TCGA-OV classifier is trained to predict. Published platinum status covered 277 treated patients, compared with 389 for the re-derived interval. The broad and provenance-filtered combinations covered about four-fifths and nearly three-quarters of the cohort, respectively. Where the two platinum labels overlapped, their agreement was almost perfect.

OS thresholds covered more patients but achieved at most moderate agreement with platinum status across cut-offs from 6 to 60 months. At 18 and 24 months, they selected an early-failure group enriched for platinum resistance among patients with known status. Most resistant patients nevertheless survived beyond the thresholds, and about half of flagged patients lacked a status against which to check their classification. Extending the threshold captured more resistant patients while also flagging more sensitive patients.

The exploratory survival decomposition is consistent with one explanation for this pattern. Associations with *BRCA1/2*, *CCNE1* and aneuploidy were clearer for the platinum-free interval, whereas those with age and bulky residual disease were clearer for survival after progression. Clinical characteristics alone also predicted the OS labels but not platinum status. An OS threshold may therefore combine information about early platinum failure with other aspects of prognosis. This remains a hypothesis: the decomposition did not formally compare the models, and confirmation would require another cohort.

The marker analyses offered little basis for choosing among labels. *BRCA1/2* and *CCNE1* are associated with survival as well as platinum response [@pennington; @yang; @etemad], and their associations pointed in the same direction under every label. The comparisons in the same patients could detect only large differences. First-course response showed weak agreement with the other labels and no clear *BRCA1/2* association, consistent with an outcome reflecting surgery and chemotherapy together.

Expression classifiers achieved cross-validated AUCs near 0.6–0.7 for their training labels. Restricting the comparison to the same patients and folds did not demonstrate an advantage for platinum-trained over 24-month-OS-trained models. The conditional interval (−0.105 to +0.087) and the wider variation across whole-pipeline refits leave moderate differences in either direction possible. The study therefore provides no clear evidence that training-label choice changed classifier performance under this design.

These estimates came from a standard, untuned pipeline, with only 41 resistant patients in the all-patients analysis. They are imprecise and do not establish the best performance achievable from these data. Several published studies reported higher figures [@wangq; @chen; @gao; @li], but used different cohorts, data types and designs. In our pipeline, selecting genes before data splitting inflated AUC by about 0.2, consistent with known selection bias [@ambroise; @vabalas; @teschendorff; @whalen]. This experiment demonstrates one route to inflated performance without identifying the cause of any particular published result.

Earlier re-annotations provide useful context. Villalobos et al. classified 212 patients as platinum-sensitive, 91 as resistant and 28 as refractory. Median OS was 27.0 months for treatment failure 1 to 6 months after the last platinum dose and 11.6 months for refractory disease [@villalobos]. Our resistant category includes both groups. The longer median in the former group is consistent with many resistant patients surviving beyond the OS thresholds examined here. Cocchi et al. released patient barcodes, platinum status and workflows for three cohorts of 230, 201 and 142 patients [@cocchi]. Our table complements these annotations by using different sources, covering all 489 platinum-treated patients, and recording multiple labels alongside the provenance and flags of each re-derived call.

Missing platinum status is unlikely to be random. Some patients died early or never responded, while others had insufficient follow-up. Re-derivation recovered 117 of the 212 patients without status. Its close agreement with published status in overlapping patients supports consistency with that reference, but cannot establish accuracy in the added patients. The provenance-filtered combination retains the 78 additions with unflagged records, about two-thirds of those recovered.

For TCGA-OV studies of platinum response, we recommend reporting the label definition, source field and number of patients in each class, and choosing a platinum-specific outcome. When extending published status with a TCGA-CDR-derived interval, document the records supporting each addition and report results with and without those patients. The provenance-filtered extension in S11 Table provides one candidate approach. Its accuracy has not been established, and the near-threshold filter may exclude patients whose records are correct.

OS thresholds should be described as survival end-points. Short thresholds have low sensitivity for platinum resistance; longer thresholds sacrifice specificity. First-course response should not be relabelled as platinum resistance. Feature selection and preprocessing must be estimated from training data within cross-validation, with separate reporting of any normalisation that uses an external cohort's predictor distribution.

### Limitations

The label comparisons rely on TCGA-OV; GSE63885 was used only to assess external transfer. Only 145 patients with RNA-seq data had platinum status, including 41 resistant patients, limiting classifier precision. The comparisons in the same patients were underpowered and do not establish equivalence. Conditional intervals for the controlled classifier comparison also leave moderate differences in either direction unresolved.

The available records constrain the labels themselves. Published platinum status depends on complete treatment and follow-up information, while the re-derived interval shares TCGA's progression dates and includes death with tumour as progression. Their agreement is therefore not independent validation. The provenance audit examined supporting records without verifying clinical events, and at least two disagreements involving unflagged records remain unexplained. Excluding intervals of 150–215 days may also reduce the representativeness of the filtered population. Both platinum labels use the six-month dichotomy that consensus has replaced for trial design [@wilson17], and neither distinguishes refractory from resistant disease.

OS-threshold sensitivity and PPV are conditional on having platinum status; the missing-status bounds are wide. Excluding patients censored before a threshold can bias the labels [@vock]. Weighting changed the estimates little, but depends on assumptions about censoring that cannot be checked. Cohort selection adds another restriction: 89 patients without treatment records were excluded, and their median survival was 27.6 months, compared with 47.7 months in the cohort. Only five had platinum status. The finding of no shorter survival among patients without status therefore applies only within the defined cohort.

*BRCA1/2* carriers were limited to truncating and splice-site variants in the 2011 release. The sequenced patients form a non-random subset of the cohort; missense variants of uncertain significance and homologous-recombination-deficiency scores were not assessed. The survival decomposition, clinical-only models, threshold sweep and reference bounds were exploratory additions after the main results were known. The decomposition applies to patients event-free and under observation at the end of first-line platinum. Several pre-specified predictions failed, including the prediction that platinum-trained classifiers would outperform OS-trained classifiers for platinum status (S1 Text). Finally, TCGA expression data were centrally processed before our splits, leaving upstream batch effects outside our pipeline's control.

### Conclusion

Published and re-derived platinum labels are consistent in TCGA-OV, although both leave part of the cohort unclassified. Re-derivation extends coverage and allows the supporting records to be examined patient by patient. OS thresholds cover more patients but agree at best moderately with platinum status. Expression classifiers predicted each of four training labels modestly, and the controlled comparison found no detectable performance difference between training labels in the same patients.

Comparisons of platinum-response models require an explicit account of the outcome being predicted and the patients contributing to each class. The versioned label table accompanying this study (S11 Table; Zenodo, https://doi.org/10.5281/zenodo.20802753) supplies these patient-level labels and documents the provenance of every re-derived call.

## Data and code availability

TCGA data were obtained from cBioPortal (`ov_tcga_pan_can_atlas_2018`, `ov_tcga_pub`) and the TCGA-CDR supplementary table [@liu] (Genomic Data Commons file 1b5f413e-a8d1-4d10-92eb-7c4ae739ed81). GSE63885 is available from the Gene Expression Omnibus. All code, analysis outputs, pre-specified predictions and figures are available at https://github.com/AaronC-bioinfo/ovarian-cancer-platinum-response and are archived at Zenodo (https://doi.org/10.5281/zenodo.20802753). The patient-level label table (version 1.0, with a data dictionary) is provided as S11 Table and in the Zenodo record.

## Author contributions

AMAC: conceptualization, data curation, formal analysis, investigation, methodology, project administration, software, validation, visualization, writing – original draft, writing – review & editing.

## Funding

The author received no specific funding for this work.

## Competing interests

The author has declared that no competing interests exist.

## Acknowledgments

The results shown here are in whole or in part based upon data generated by the TCGA Research Network: https://www.cancer.gov/tcga.

## References

## Supporting information

S1 Fig. Transfer of TCGA-trained classifiers to GSE63885, by training label.

S2 Fig. Feature-selection leakage: AUC inflation from supervised and unsupervised gene selection before data splitting.

S1 Table. Full literature extraction for Table 1, with verbatim quotations and their page locations.

S2 Table. Pairwise agreement and OS-threshold test characteristics: full cohort, patients with RNA-seq data, against the combined label, at every threshold from 6 to 60 months, and with inverse-probability-of-censoring weights.

S3 Table. *BRCA1/2* and *CCNE1* associations for every carrier definition (primary, any non-silent variant, germline only, somatic only, *BRCA1* and *BRCA2* separately), with same-patient differences between labels and minimum detectable differences.

S4 Table. Cohort characteristics, cohort flow, and patients with and without a determinate platinum status, with bounds under the missing reference standard.

S5 Table. Associations with clinical and tumour characteristics, with raw P values and q values, in all determinate patients and in the same patients.

S6 Table. Within-TCGA cross-label AUC for each model and repeat.

S7 Table. Transfer to GSE63885: AUC with 95% bootstrap intervals for every training label, model and GEO label.

S8 Table. Gene-set transfer experiment: published gene sets as fixed inputs, with the random-gene-set null distribution.

S9 Table. Feature-selection leakage at the 12-, 18- and 24-month thresholds.

S10 Table. Exploratory analyses: decomposition of overall survival (platinum-free interval in patients at risk at the end of platinum, with the earlier model that set short intervals to 1 day as a sensitivity analysis), clinical-only models and the redaction sensitivity analysis; Cox models of the progression-free interval.

S11 Table. Patient-level label table (version 1.0): every label, the provenance-filtered and broad combined labels, provenance class, event source and flags for the 489 platinum-treated patients, with a data dictionary, class counts, the four discordant patients and the treatment-anchor sensitivity analysis.

S1 Text. Pre-specified predictions and decision rules for each analysis, with observed outcomes, and the analysis history and deviations.

S2 Text. Reporting checklists (STROBE; STARD 2015 for the OS-threshold analysis).

## Figure legends

**Fig 1. Coverage and agreement of candidate labels in 489 platinum-treated TCGA-OV patients.** (A) Number of patients in whom each label is determinate; dark segment, non-responders or resistant; light segment, responders; dashed line, all 489 patients; colour denotes label family. Numbers give patients labelled (non-responders or resistant). The broad combined label uses platinum status where available and the re-derived platinum-free interval otherwise; the provenance-filtered combined label (preferred under the pre-specified rule) adds re-derived calls only for unflagged patients. (B) Cohen's κ for each pair of labels, in patients with both labels determinate. (C) Sensitivity, specificity and positive predictive value (PPV) of death before each threshold as a test for platinum resistance, with TCGA platinum status as the reference; shaded bands, Wilson 95% confidence intervals; dashed line, PPV expected if the OS label carried no information about platinum status; vertical lines, 18 and 24 months. (D) Provenance of the 117 patients added by the re-derived interval, each counted once (in the order negative interval, resistant call dated only by a death, other record problem, interval within 150–215 days only): unflagged resistant or sensitive; flagged only for an interval within 150–215 days; flagged for another record problem (redacted TCGA-CDR record, adjuvant platinum without a stop date, or a later-line regimen before the event, with or without a near-threshold interval); resistant call dated only by a death counted as progression; or negative interval.

**Fig 2. Characteristics associated with platinum response and prognosis under each label.** Odds ratio (95% CI, log scale) for being labelled a non-responder in (A) carriers of a germline or somatic truncating or splice-site *BRCA1/2* variant (272 sequenced patients), (B) tumours with *CCNE1* amplification and (C) patients with residual disease > 1 cm. (D) Rank-biserial correlation between Aneuploidy Score and non-response (positive, higher in non-responders). Each label uses all platinum-treated patients in whom it is determinate. A–C: \* 95% CI excludes 1; lower bounds below 0.03 are drawn at 0.03. D: \* Benjamini–Hochberg q < 0.05 within label (five characteristics). Colour denotes label family: platinum labels (blue), first-course response (teal), OS thresholds (orange).

**Fig 3. What classifiers trained on each label predict within TCGA.** (A) Mean cross-validated AUC (three models, five repeats of five-fold cross-validation, 251 patients with RNA-seq data) for each training label (rows) against each label in held-out patients (columns); descriptive, because each label has its own patients and class balance. (B) Controlled comparison in the same 134 patients: difference in AUC between training labels (mean of three models). For each contrast, the upper row (circles, solid lines) gives the cross-validated estimate (same folds for every label) with its conditional 95% interval from resampling patients without refitting the models; the lower row (squares, dashed lines) gives the median and 2.5th–97.5th percentile range of out-of-bag differences from 500 bootstrap refits of the whole pipeline, a sensitivity analysis of a different quantity.

**Fig 4. Associations with the platinum-free interval and with survival after progression (exploratory).** Hazard ratios (95% CI, log scale) from univariable Cox models of the platinum-free interval from the end of first-line platinum (blue; 408 patients at risk at the end of platinum, with an interval above 0 days) and of survival after progression among patients who progressed (orange; patients whose progression event was their death excluded). Times from TCGA-CDR. The two models were not compared formally.

## Tables

**Table 1. Labels used by studies of expression and platinum response in TCGA-OV and related cohorts.**

| Study | TCGA-OV label and stated definition | TCGA n (resistant / sensitive) | External or other cohorts | Design | Reported discrimination |
|---|---|---|---|---|---|
| Gonzalez Bosquet 2016 [@gonzalez] | Complete response, progression-free 6 months after first platinum-based treatment, vs refractory or recurrence within 6 months of completion | 158 / 292 | Six GEO/EBI cohorts recoded to the same classes | 34 genes selected on the full TCGA set; internal cross-validation type not stated | AUC 0.64–0.79 (TCGA), 0.45–0.73 (external) |
| Sun J 2019 [@sunj] | "Chemo-response information"; definition not stated | Not stated (TCGA n = 557, microarray) | Several GEO cohorts | Rank-based score, cut-off 0 | No AUC |
| Choi 2020 [@choi] | Recurrence < 6 months vs > 12 months after last primary chemotherapy; 6–12 months excluded | 110 / 160 | GSE9891 (survival only) | No classifier | Not applicable |
| Gonzalez Bosquet 2021 [@gb2021] | Progression-free ≥ 6 months after first platinum-based treatment; ≥ 6 months of follow-up required | 149 / 189 (validation set) | Trained on 88 patients from one institution | Clinical and multi-omic lasso models; TCGA used for validation | TCGA AUCs not reported numerically in the main text or Fig 4 |
| Sun X 2021 [@sunx] | No response label (progression-free survival used as surrogate) | — | GSE131978, 7 / 4; GSE51373, 10 / 13 | No classifier | Not applicable |
| Guo & Li 2021 [@guoli] | Relapse within 6 months after completing chemotherapy | 49 / 205 | — | Single-gene ROC analysis | Per-gene AUC 0.58–0.60 |
| Chen 2022 [@chen] | Platinum-free interval < 6 months from end of first chemotherapy course; TCGA field not stated | 69 / 161 | GSE63885, 34 / 41 | Genes selected on the full labelled set; no held-out TCGA split; SVM with 100-fold CV | AUC 0.971 (TCGA), 0.926 (GSE63885) |
| Li 2022 [@li] | "Known platinum sensitivity" from cBioPortal; definition not stated | 90 / 197 (supplement; equal to TCGA 2011 platinum status) | GSE15622, 6 / 9 | Held-out split and CV not stated | AUC 0.841 (TCGA), 0.796 (GSE15622) |
| Wang C 2024 [@wangc24] | TCGA label definition not stated (counts equal to TCGA 2011 platinum status); relapse within six months stated for the external ROC-plotter analysis | 90 / 197 | Public cohorts via ROC-plotter | Single-gene ROC analysis | Per-gene AUC > 0.6 |
| Gao 2025 [@gao] | Source of bulk TCGA labels not stated (interval < 6 months stated for single-cell cohort) | 287 TCGA in a pooled 404 from four datasets, including the GSE63885 validation set (pooled counts as printed: 71 sensitive / 333 resistant) | GSE63885, n = 75 | Random 8:2 split of TCGA, GSE15622 and GSE51373 (GSE63885 held out); five-fold CV for hyperparameters | AUC 0.993 (test), 0.989 (GSE63885) |
| Kilim 2025 [@kilim] | Refractory (progression or stable disease within six cycles) vs no progression within 2 years; proteomics and histology, not mRNA | 127 patients; classes not stated | PTRC-HGSOC | Train on one cohort, test on the other; five-fold CV | AUC 0.752 (PTRC → TCGA), 0.835 (TCGA → PTRC), 0.613 (TCGA five-fold CV); multimodal, primary tumours |
| Wang C 2025 [@wangc] | No TCGA response-classifier cohort; GEO labels, definition not stated | — | Merged GSE114206, GSE51373, GSE63885; GSE30161 (test) | Selection on the merged set; no held-out split | Per-gene AUC 0.66–0.72 (merged), 0.55–0.75 (GSE30161) |

**Table 2. Candidate labels in platinum-treated TCGA-OV patients.**

| Label | Definition (1 = non-responder) | Source | Platinum cohort, n (1 / 0) | With RNA-seq, n (1 / 0) |
|---|---|---|---|---|
| Platinum status | Platinum-free interval < 6 months from last primary platinum dose, with progression | TCGA 2011 [@tcga2011] | 277 (87 / 190) | 145 (41 / 104) |
| Platinum-free interval | Progression < 183 days after end of first-line platinum | TCGA-CDR + treatment timeline | 389 (115 / 274) | 188 (53 / 135) |
| Provenance-filtered combined label (candidate extension) | Platinum status where determinate, otherwise platinum-free interval in patients with an unflagged record | As above, with provenance audit | 355 (99 / 256) | 167 (43 / 124) |
| Broad combined label (sensitivity analysis) | Platinum status where determinate, otherwise platinum-free interval | As above | 394 (113 / 281) | 189 (51 / 138) |
| First-course response | Stable or progressive vs complete or partial response | TCGA-CDR, then TCGA 2011 | 425 (65 / 360) | 219 (35 / 184) |
| OS < 18 months | Death before 18 months vs survival beyond | PanCancer Atlas clinical | 419 (47 / 372) | 206 (22 / 184) |
| OS < 24 months | Death before 24 months vs survival beyond | PanCancer Atlas clinical | 401 (78 / 323) | 199 (36 / 163) |

**Table 3. Association of each label with characteristics linked to platinum response and prognosis.**

| Characteristic | Platinum status | Platinum-free interval | First-course response | OS < 18 months | OS < 24 months |
|---|---|---|---|---|---|
| *BRCA1/2* carrier, OR | 0.41 (0.14–1.04) | 0.37 (0.14–0.87)\* | 0.64 (0.18–1.80) | 0.15 (0.004–0.97)\* | 0.22 (0.04–0.75)\* |
| *CCNE1* amplified, OR | 1.55 (0.80–2.97) | 1.76 (0.98–3.15) | 1.11 (0.52–2.26) | 1.78 (0.78–3.89) | 2.01 (1.06–3.75)\* |
| Residual > 1 cm, OR | 1.12 (0.59–2.09) | 1.25 (0.71–2.18) | 2.55 (1.31–4.91)\* | 2.86 (1.30–6.29)\* | 2.41 (1.28–4.50)\* |
| Any residual, OR | 3.22 (1.40–8.35)\* | 3.04 (1.44–7.03)\* | 1.54 (0.67–3.99) | 2.93 (0.87–15.43) | 2.78 (1.12–8.29)\* |
| Stage IV, OR | 1.02 (0.46–2.17) | 1.09 (0.57–2.03) | 1.25 (0.57–2.57) | 1.75 (0.76–3.79) | 1.55 (0.78–2.97) |
| Aneuploidy Score, r | 0.13 | 0.21\* | −0.03 | 0.20\* | 0.25\* |
| TMB, r | −0.16 | −0.06 | −0.03 | −0.08 | −0.08 |
| Age, r | 0.07 | 0.15 | 0.06 | 0.26\* | 0.28\* |

OR, conditional odds ratio for non-response (95% CI); r, rank-biserial correlation (positive = higher in non-responders). Each label uses all platinum-treated patients in whom it is determinate; *BRCA1/2* and *CCNE1* in sequenced and copy-number-profiled patients. Any residual versus none was an alternative coding added after the main results were known. \* OR rows: 95% CI excludes 1; r rows: Benjamini–Hochberg q < 0.05 within label across the five pre-specified clinical and tumour characteristics (as in Fig 2).
