"""Convert [@key; @key] citations in manuscript_v4_src.md to numbered citations (order of first
appearance) and append the reference list. Usage: python number_refs.py <src.md> <out.md>"""
import re
import sys

REFS = {
    "strobe": "von Elm E, Altman DG, Egger M, Pocock SJ, Gøtzsche PC, Vandenbroucke JP. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. Lancet. 2007;370:1453–1457. doi:10.1016/S0140-6736(07)61602-X",
    "stard": "Bossuyt PM, Reitsma JB, Bruns DE, Gatsonis CA, Glasziou PP, Irwig L, et al. STARD 2015: an updated list of essential items for reporting diagnostic accuracy studies. BMJ. 2015;351:h5527. doi:10.1136/bmj.h5527",
    "yangsyc": "Yang SYC, Lheureux S, Karakasis K, Burnier JV, Bruce JP, Clouthier DL, et al. Landscape of genomic alterations in high-grade serous ovarian cancer from exceptional long- and short-term survivors. Genome Med. 2018;10:81. doi:10.1186/s13073-018-0590-x",
    "gb2021": "Gonzalez Bosquet J, Devor EJ, Newtson AM, Smith BJ, Bender DP, Goodheart MJ, et al. Creation and validation of models to predict response to primary treatment in serous ovarian cancer. Sci Rep. 2021;11:5957. doi:10.1038/s41598-021-85256-9",
    "choi": "Choi J, Topouza DG, Tarnouskaya A, Nesdoly S, Koti M, Duan QL. Gene networks and expression quantitative trait loci associated with adjuvant chemotherapy response in high-grade serous ovarian cancer. BMC Cancer. 2020;20:413. doi:10.1186/s12885-020-06922-1",
    "kilim": "Kilim O, Olar A, Biricz A, Madaras L, Pollner P, Szállási Z, et al. Histopathology and proteomics are synergistic for high-grade serous ovarian cancer platinum response prediction. NPJ Precis Oncol. 2025;9:27. doi:10.1038/s41698-025-00808-w",
    "guoli": "Guo K, Li L. Prediction of key candidate genes for platinum resistance in ovarian cancer. Int J Gen Med. 2021;14:8237–8248. doi:10.2147/IJGM.S338044",
    "wangc24": "Wang C, Chen C, Chen X, Luo J, Su Y, Liu X, et al. Identification of genes predicting chemoresistance and short survival in ovarian cancer. Transl Cancer Res. 2024;13:4354–4371. doi:10.21037/tcr-23-2157",
    "markman": "Markman M, Rothman R, Hakes T, Reichman B, Hoskins W, Rubin S, et al. Second-line platinum therapy in patients with ovarian cancer previously treated with cisplatin. J Clin Oncol. 1991;9:389–393. doi:10.1200/JCO.1991.9.3.389",
    "villalobos": "Villalobos VM, Wang YC, Sikic BI. Reannotation and analysis of clinical and chemotherapy outcomes in the ovarian data set from The Cancer Genome Atlas. JCO Clin Cancer Inform. 2018;2:1–16. doi:10.1200/CCI.17.00096",
    "talijanovic": "Talijanovic M, Lopacinska-Jørgensen J, Høgdall EV. Gene expression profiles in ovarian cancer tissues as a potential tool to predict platinum-based chemotherapy resistance. Anticancer Res. 2025;45:11–26. doi:10.21873/anticanres.17389",
    "tcga2011": "The Cancer Genome Atlas Research Network. Integrated genomic analyses of ovarian carcinoma. Nature. 2011;474:609–615. doi:10.1038/nature10166",
    "chen": "Chen S, Wu Y, Wang S, Wu J, Wu X, Zheng Z. A risk model of gene signatures for predicting platinum response and survival in ovarian cancer. J Ovarian Res. 2022;15:39. doi:10.1186/s13048-022-00969-3",
    "li": "Li Y, Nie Y, Guo H, Guo H, Ha C, Li Y. Establish of an initial platinum-resistance predictor in high-grade serous ovarian cancer patients regardless of homologous recombination deficiency status. Front Oncol. 2022;12:847085. doi:10.3389/fonc.2022.847085",
    "gao": "Gao T, Zhao P, Han S. Integrating bulk RNA-seq and scRNA-seq analyses with machine learning to predict platinum response and prognosis in ovarian cancer. Sci Rep. 2025;15:19123. doi:10.1038/s41598-025-99930-9",
    "sunx": "Sun X, Liu Q, Huang J, Diao G, Liang Z. Transcriptome-based stemness indices analysis reveals platinum-based chemo-theraputic response indicators in advanced-stage serous ovarian cancer. Bioengineered. 2021;12:3753–3771. doi:10.1080/21655979.2021.1939514",
    "sunj": "Sun J, Bao S, Xu D, Zhang Y, Su J, Liu J, et al. Large-scale integrated analysis of ovarian cancer tumors and cell lines identifies an individualized gene expression signature for predicting response to platinum-based chemotherapy. Cell Death Dis. 2019;10:661. doi:10.1038/s41419-019-1874-9",
    "gonzalez": "Gonzalez Bosquet J, Newtson AM, Chung RK, Thiel KW, Ginader T, Goodheart MJ, et al. Prediction of chemo-response in serous ovarian cancer. Mol Cancer. 2016;15:66. doi:10.1186/s12943-016-0548-9",
    "wangc": "Wang C, Peng C, Xie C. Unveiling novel biomarkers for platinum chemoresistance in ovarian cancer. Open Med (Wars). 2025;20:20241084. doi:10.1515/med-2024-1084",
    "wangq": "Wang Q, Chang Z, Liu X, Wang Y, Feng C, Ping Y, et al. Predictive value of machine learning for platinum chemotherapy responses in ovarian cancer: systematic review and meta-analysis. J Med Internet Res. 2024;26:e48527. doi:10.2196/48527",
    "chintala2026": "Chintala AMA. Ovarian Cancer Platinum Response: ML Pipeline with Feature-Selection Leakage Analysis (v1.0.0) [software]. Zenodo; 2026. doi:10.5281/zenodo.20802754",
    "lloyd": "Lloyd KL, Cree IA, Savage RS. Prediction of resistance to chemotherapy in ovarian cancer: a systematic review. BMC Cancer. 2015;15:117. doi:10.1186/s12885-015-1101-8",
    "wilson17": "Wilson MK, Pujade-Lauraine E, Aoki D, Mirza MR, Lorusso D, Oza AM, et al. Fifth Ovarian Cancer Consensus Conference of the Gynecologic Cancer InterGroup: recurrent disease. Ann Oncol. 2017;28:727–732. doi:10.1093/annonc/mdw663",
    "liu": "Liu J, Lichtenberg T, Hoadley KA, Poisson LM, Lazar AJ, Cherniack AD, et al. An integrated TCGA pan-cancer clinical data resource to drive high-quality survival outcome analytics. Cell. 2018;173:400–416.e11. doi:10.1016/j.cell.2018.02.052",
    "tripod": "Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. doi:10.1136/bmj-2023-078378",
    "probast": "Wolff RF, Moons KGM, Riley RD, Whiting PF, Westwood M, Collins GS, et al. PROBAST: a tool to assess the risk of bias and applicability of prediction model studies. Ann Intern Med. 2019;170:51–58. doi:10.7326/M18-1376",
    "jacobs": "Jacobs AZ, Wallach H. Measurement and fairness. In: Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency. 2021. p. 375–385. doi:10.1145/3442188.3445901",
    "yousefi": "Yousefi S, Shaban A, Amgad M, Chandradevan R, Cooper LAD. Learning clinical outcomes from heterogeneous genomic data sources. arXiv:1904.01637 [Preprint]. 2019.",
    "bayer": "Bayer I, Groth P, Schneckener S. Prediction errors in learning drug response from gene expression data – influence of labeling, sample size, and machine learning algorithm. PLoS ONE. 2013;8:e70294. doi:10.1371/journal.pone.0070294",
    "cocchi": "Cocchi S, Talijanovic M, Høgdall EV, Lopacinska-Jørgensen J. Assessing the impact of patient selection and analytical methods on mRNA biomarker identification in ovarian cancer using TCGA data. Cancer Control. 2026;33:10732748261468094. doi:10.1177/10732748261468094",
    "cerami": "Cerami E, Gao J, Dogrusoz U, Gross BE, Sumer SO, Aksoy BA, et al. The cBio Cancer Genomics Portal: an open platform for exploring multidimensional cancer genomics data. Cancer Discov. 2012;2:401–404. doi:10.1158/2159-8290.CD-12-0095",
    "gaoj": "Gao J, Aksoy BA, Dogrusoz U, Dresdner G, Gross B, Sumer SO, et al. Integrative analysis of complex cancer genomics and clinical profiles using the cBioPortal. Sci Signal. 2013;6:pl1. doi:10.1126/scisignal.2004088",
    "cohen": "Cohen J. A coefficient of agreement for nominal scales. Educ Psychol Meas. 1960;20:37–46. doi:10.1177/001316446002000104",
    "wilson27": "Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc. 1927;22:209–212. doi:10.1080/01621459.1927.10502953",
    "pennington": "Pennington KP, Walsh T, Harrell MI, Lee MK, Pennil CC, Rendi MH, et al. Germline and somatic mutations in homologous recombination genes predict platinum response and survival in ovarian, fallopian tube, and peritoneal carcinomas. Clin Cancer Res. 2014;20:764–775. doi:10.1158/1078-0432.CCR-13-2287",
    "yang": "Yang D, Khan S, Sun Y, Hess K, Shmulevich I, Sood AK, et al. Association of BRCA1 and BRCA2 mutations with survival, chemotherapy sensitivity, and gene mutator phenotype in patients with ovarian cancer. JAMA. 2011;306:1557–1565. doi:10.1001/jama.2011.1456",
    "etemad": "Etemadmoghadam D, deFazio A, Beroukhim R, Mermel C, George J, Getz G, et al. Integrated genome-wide DNA copy number and expression analysis identifies distinct mechanisms of primary chemoresistance in ovarian carcinomas. Clin Cancer Res. 2009;15:1417–1427. doi:10.1158/1078-0432.CCR-08-1564",
    "bh": "Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Series B Stat Methodol. 1995;57:289–300. doi:10.1111/j.2517-6161.1995.tb02031.x",
    "sklearn": "Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, et al. Scikit-learn: machine learning in Python. J Mach Learn Res. 2011;12:2825–2830.",
    "hanley": "Hanley JA, McNeil BJ. The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology. 1982;143:29–36. doi:10.1148/radiology.143.1.7063747",
    "lisowska": "Lisowska KM, Olbryt M, Dudaladava V, Pamuła-Piłat J, Kujawa K, Grzybowska E, et al. Gene expression analysis in ovarian cancer – faults and hints from DNA microarray study. Front Oncol. 2014;4:6. doi:10.3389/fonc.2014.00006",
    "ambroise": "Ambroise C, McLachlan GJ. Selection bias in gene extraction on the basis of microarray gene-expression data. Proc Natl Acad Sci U S A. 2002;99:6562–6566. doi:10.1073/pnas.102102699",
    "vabalas": "Vabalas A, Gowen E, Poliakoff E, Casson AJ. Machine learning algorithm validation with a limited sample size. PLoS ONE. 2019;14:e0224365. doi:10.1371/journal.pone.0224365",
    "teschendorff": "Teschendorff AE. Avoiding common pitfalls in machine learning omic data science. Nat Mater. 2019;18:422–427. doi:10.1038/s41563-018-0241-z",
    "whalen": "Whalen S, Schreiber J, Noble WS, Pollard KS. Navigating the pitfalls of applying machine learning in genomics. Nat Rev Genet. 2022;23:169–181. doi:10.1038/s41576-021-00434-9",
    "vock": "Vock DM, Wolfson J, Bandyopadhyay S, Adomavicius G, Johnson PE, Vazquez-Benitez G, et al. Adapting machine learning techniques to censored time-to-event health record data: a general-purpose approach using inverse probability of censoring weighting. J Biomed Inform. 2016;61:119–131. doi:10.1016/j.jbi.2016.03.009",
}

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
order: list[str] = []
pat = re.compile(r"\[(@[^\]]+)\]")


def fmt(nums):
    nums = sorted(set(nums)); parts = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        parts.append(str(nums[i]) if i == j else (f"{nums[i]},{nums[j]}" if j == i + 1 else f"{nums[i]}–{nums[j]}"))
        i = j + 1
    return ",".join(parts)


def repl(m):
    items = [x.strip() for x in m.group(1).split(";")]
    nums, suffix = [], ""
    for it in items:
        k = it.lstrip("@")
        if "," in k:  # locator, e.g. "@tcga2011, Supplementary Methods S1"
            k, suffix = k.split(",", 1)
            suffix = "," + suffix
        k = k.strip()
        assert k in REFS, k
        if k not in order:
            order.append(k)
        nums.append(order.index(k) + 1)
    return f"[{fmt(nums)}{suffix}]"


s = pat.sub(repl, s)
unused = [k for k in REFS if k not in order]
if unused:
    print("unused references (dropped):", unused)
reflist = "\n".join(f"{i}. {REFS[k]}" for i, k in enumerate(order, 1))
assert s.count("## References\n") == 1
s = s.replace("## References\n", "## References\n\n" + reflist + "\n", 1)
open(out, "w", encoding="utf-8").write(s)
print(len(order), "references")
