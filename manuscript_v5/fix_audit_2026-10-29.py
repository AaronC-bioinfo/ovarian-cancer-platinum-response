p = "manuscript_v5_src.md"
s = open(p, encoding="utf-8").read()
R = [
    # short title <= 50 chars
    ("Short title: Outcome labels for platinum-response prediction in TCGA-OV", "Short title: Platinum-response labels in TCGA-OV"),
    # abstract
    ("and trained cross-validated expression classifiers on each label.",
     "and trained cross-validated expression classifiers on four of the labels."),
    ("No threshold between 6 and 60 months agreed well with platinum status (highest κ 0.47, at 36 months).",
     "No threshold between 6 and 60 months agreed better than moderately with platinum status (highest κ 0.47, at 36 months)."),
    ("In exploratory analyses, *BRCA1/2*, *CCNE1* and aneuploidy were associated mainly with the platinum-free interval, whereas age and bulky residual disease were associated with survival after progression,",
     "In exploratory analyses added after review, *BRCA1/2*, *CCNE1* and aneuploidy were associated mainly with the platinum-free interval, whereas age and bulky residual disease were associated with survival after progression,"),
    ("OS thresholds thus combine early platinum failure with prognosis unrelated to platinum, and agree poorly with platinum status at any cut-off.",
     "These exploratory results suggest that OS thresholds combine early platinum failure with prognostic factors acting after progression; at no cut-off did they agree better than moderately with platinum status."),
    # intro: Markman, Cocchi novelty
    ("Clinically, platinum response has been judged by the interval from the last platinum dose to recurrence, which predicts response to platinum re-treatment [@markman],",
     "Clinically, platinum response has been judged by the time since the last platinum dose, which predicts response to platinum re-treatment [@markman],"),
    ("Earlier work re-annotated TCGA-OV treatment outcomes and related platinum sensitivity and first-line response to overall survival [@villalobos], and showed that patient selection and interval definitions change the genes reported [@cocchi];",
     "Earlier work re-annotated TCGA-OV treatment outcomes and related platinum sensitivity and first-line response to overall survival [@villalobos]; most closely, Cocchi et al. cross-tabulated re-derived platinum-free-interval categories against TCGA's platinum status and showed that patient selection and interval definitions change the genes reported [@cocchi];"),
    ("To our knowledge, however, no study has quantified agreement among the candidate platinum-response labels in TCGA-OV within the same patients, evaluated OS thresholds as tests for platinum resistance, or compared what classifiers trained on each label learn.",
     "To our knowledge, however, no study has quantified agreement across the families of candidate labels in TCGA-OV — platinum-based, survival-based and response-based — within the same patients, evaluated OS thresholds as tests for platinum resistance, or compared what classifiers trained on each label learn."),
    # methods: sweep etc flagged
    ("OS thresholds from 6 to 60 months were evaluated as tests for platinum resistance, with platinum status as the reference: sensitivity, specificity and positive predictive value (PPV), with Wilson 95% intervals [@wilson27]. Each was compared with the values expected if the OS label carried no information about platinum status (PPV equal to the prevalence of resistance; specificity equal to the proportion of patients the label does not flag) and with the highest sensitivity the label's prevalence allows. Because platinum status is missing for many patients, we also report bounds on sensitivity and PPV obtained by assigning all OS-labelled patients without a status to resistant or to sensitive.",
     "The 18- and 24-month OS thresholds were evaluated as tests for platinum resistance, with platinum status as the reference: sensitivity, specificity, positive predictive value (PPV) and negative predictive value, with Wilson 95% intervals [@wilson27]. After internal review we added, as exploratory analyses, the same evaluation at every threshold from 6 to 60 months; comparison with the values expected if the OS label carried no information about platinum status (PPV equal to the prevalence of resistance; specificity equal to the proportion of patients the label does not flag) and with the highest sensitivity the label's prevalence allows; and bounds on sensitivity and PPV obtained by assigning all OS-labelled patients without a status to resistant or to sensitive."),
    ("differences between labels in the log OR for *BRCA1/2* and residual disease and in r for aneuploidy were estimated with 95% intervals from 2,000 bootstrap resamples, and the smallest difference detectable with 80% power was derived from each interval.",
     "differences between labels in the log OR for *BRCA1/2* (platinum label minus OS label) and for residual disease and in r for aneuploidy (OS label minus platinum status) were estimated with 95% intervals from 2,000 bootstrap resamples. The smallest difference detectable with 80% power was derived from each interval in an exploratory analysis added after review."),
    ("Third, the re-derived interval was recomputed without the 38 patients whose TCGA-CDR record is marked as redacted.",
     "Third, the re-derived interval was recomputed without the 38 patients whose TCGA-CDR record is marked as redacted. The threshold sweep, reference bounds, minimum detectable differences and an alternative coding of residual disease (any versus none) were added at the same time. The clinical-only models used logistic regression only."),
    # results
    ("The re-derived interval was determinate for 389 patients (358 without the redacted TCGA-CDR records, with unchanged agreement, κ 0.96),",
     "The re-derived interval was determinate for 389 patients (358 without the redacted TCGA-CDR records; κ with platinum status 0.964 versus 0.966),"),
    ("### OS thresholds agree poorly with platinum status at every cut-off", "### OS thresholds agree at best moderately with platinum status"),
    ("At 18 months the OS threshold flagged", "At 18 months the OS threshold flagged"),
    ("Across thresholds from 6 to 60 months, sensitivity rose and specificity and PPV fell, and agreement never became good: κ was highest at 36 months (0.47; sensitivity 0.64, specificity 0.83, PPV 0.65).",
     "Across thresholds from 6 to 60 months (exploratory), sensitivity rose and specificity and PPV fell, and agreement was at best moderate: κ was highest at 36 months (0.47; sensitivity 0.64, specificity 0.83, PPV 0.65; S2 Table)."),
    ("so they do not show that the labels behave alike. *CCNE1* amplification", "so they do not show that the labels behave alike (S3 Table). *CCNE1* amplification"),
    ("Older age was associated with both OS thresholds (r = 0.26 and 0.28) but not with platinum status (r = 0.07), as pre-specified for the 24-month threshold.",
     "Older age was associated with both OS thresholds (r = 0.26 and 0.28) but not with platinum status (r = 0.07), as predicted in advance for the 24-month threshold in patients with RNA-seq data (S1 Text). Full results, including raw P values, are in S5 Table."),
    ("When overall survival was divided into its two parts,", "When overall survival was divided into the platinum-free interval and survival after progression (S10 Table),"),
    ("mean cross-validated AUC was 0.63 for platinum status (range over models and repeats 0.56–0.69),",
     "mean cross-validated AUC was 0.63 for platinum status (range over models and repeats 0.56–0.69; S6 Table),"),
    ("a comparison that was not pre-specified (S1 Fig).", "a comparison that was not pre-specified (S1 Fig, S7 Table)."),
    ("and the 5 genes of Gao et al. did not differ from random sets.", "and the 5 genes of Gao et al. did not differ from random sets (S8 Table)."),
    ("by +0.006 with unsupervised selection (S2 Fig).", "by +0.006 with unsupervised selection (S2 Fig, S9 Table)."),
    ("The proportion of TCGA patients labelled resistant ranged from 19% to 44%.",
     "The proportion of TCGA patients labelled resistant ranged from 19% to 44% (S1 Table)."),
    # discussion
    ("The exploratory decomposition suggests why. Overall survival is the sum of the platinum-free interval and survival after progression.",
     "The exploratory decomposition, added after review, suggests a reason. Overall survival comprises the time to the end of first-line platinum, the platinum-free interval and survival after progression."),
    ("An OS-threshold label therefore mixes early platinum failure with prognosis that has little to do with platinum, and a classifier trained on it is asked to learn both.",
     "Any residual disease was associated with both parts. If confirmed, this would mean that an OS-threshold label mixes early platinum failure with prognostic factors that act after progression, and that a classifier trained on it is asked to learn both."),
    ("re-deriving the interval from TCGA-CDR recovers about half of them without loss of agreement.",
     "re-deriving the interval from TCGA-CDR recovers about half of them, and where both labels are available they agree closely."),
    # limitations
    ("The cohort definition excludes 89 patients without a treatment record, whose survival was poorer than the cohort's.",
     "The cohort definition excludes 89 patients without a treatment record, whose survival was poorer than the cohort's (median 27.6 months) and only five of whom had a platinum status; the finding that patients without a platinum status did not have shorter survival holds only within the defined cohort."),
    ("The decomposition of overall survival and the clinical-only models were exploratory and were added after the main results were known.",
     "The decomposition of overall survival, the clinical-only models, the threshold sweep and the reference bounds were exploratory and were added after the main results were known."),
    # conclusion
    ("overall-survival thresholds cover more of it but agree poorly with platinum status at every cut-off, because they combine early platinum failure with prognosis unrelated to platinum; and expression predicts all of them modestly.",
     "overall-survival thresholds cover more of it but agree at best moderately with platinum status, and exploratory analyses suggest that they combine early platinum failure with prognostic factors acting after progression; expression predicts all of them modestly."),
    # discussion para 1 phrase "at no cut-off do they agree well"
    ("The OS thresholds cover more patients, but at no cut-off do they agree well with platinum status.",
     "The OS thresholds cover more patients, but at no cut-off do they agree better than moderately with platinum status."),
    # data availability
    ("and the TCGA-CDR supplementary table [@liu].", "and the TCGA-CDR supplementary table [@liu] (Genomic Data Commons file 1b5f413e-a8d1-4d10-92eb-7c4ae739ed81)."),
    # SI captions
    ("S7 Table. Transfer to GSE63885: methods and AUC with 95% bootstrap intervals", "S7 Table. Transfer to GSE63885: AUC with 95% bootstrap intervals"),
    ("S1 Table. Full literature extraction for Table 1, with verbatim quotations and their locations.",
     "S1 Table. Full literature extraction for Table 1, with verbatim quotations and their page locations."),
    # Table 1 Wang C 2025 row
    ("| Merged GSE114206, GSE51373, GSE63885 | Selection on the merged set; no held-out split | Per-gene AUC 0.66–0.72 |",
     "| Merged GSE114206, GSE51373, GSE63885; GSE30161 (test) | Selection on the merged set; no held-out split | Per-gene AUC 0.66–0.72 (merged), 0.55–0.75 (GSE30161) |"),
]
for a, b in R:
    if a == b:
        continue
    assert s.count(a) == 1, ("NOT FOUND/AMBIGUOUS", a[:70])
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
