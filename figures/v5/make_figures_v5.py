"""
figures/v5/make_figures_v5.py
─────────────────────────────
Figures for manuscript v5. Reads only saved analysis outputs; computes nothing new
except means/ranges of already-computed AUCs. Does NOT read outputs/results/ablation_split_variance_summary.csv.

Main figures
  F1  Coverage, agreement and OS thresholds as tests for platinum resistance across thresholds
        label_validity/outputs/a11_coverage.csv, label_resource_v1_counts.csv, a11_kappa_full.csv, a13_threshold_sweep.csv, a15b_provenance.csv (D)
  F2  Associations with characteristics linked to platinum response and prognosis, under each label (full platinum-treated cohort)
        label_validity/outputs/a8_brca_tests.csv (T1 primary BRCA; T4 CCNE1), a10_tests.csv (T1)
  F3  What classifiers trained on each label predict within TCGA
        label_validity/outputs/a5_cross_label_repeats.csv (A); a16_paired_differences.csv, a22_fullpipeline_replicates.csv (B)
  F4  (exploratory) Associations with the platinum-free interval and with survival after progression
        label_validity/outputs/a13b_decomposition_cox.csv (analysis at_risk / unchanged)
Supporting figures
  S1_Fig  Transfer to GSE63885            label_validity/outputs/a4_transfer_results.csv
  S2_Fig  Feature-selection leakage       outputs/results_pinned_2026-10-29/ablation_*_summary.csv
Outputs: figures/v5/*.png|pdf, figures/v5/figure_values.md
Run (any Python with pandas + matplotlib), from the project root:
  python figures/v5/make_figures_v5.py

Colour: label family (platinum labels blue #2a78d6, OS-threshold labels orange #eb6834,
first-course response aqua #1baf7a), as in v3. Heatmaps: single-hue blue ramp, values printed.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
LV = ROOT / "label_validity" / "outputs"
RES_PINNED = ROOT / "outputs" / "results_pinned_2026-10-29"
OUT = ROOT / "figures" / "v5"
OUT.mkdir(parents=True, exist_ok=True)

INK, INK2, MUTED, GRID, BASE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
FAM = {"platinum": "#2a78d6", "os": "#eb6834", "response": "#1baf7a"}
BLUES = LinearSegmentedColormap.from_list(
    "blues", ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"])
ORDER = ["label_platinum", "label_pfiplat6", "label_response", "label_os18_all", "label_os24_all"]
LAB1 = {"label_platinum": "Platinum status (TCGA 2011)", "label_pfiplat6": "PFI from first-line platinum < 6 mo",
        "label_response": "First-course response (PD/SD)", "label_os18_all": "OS < 18 mo", "label_os24_all": "OS < 24 mo",
        "label_hybrid": "Platinum status or PFI (broad combined)",
        "label_combined_strict": "Platinum status or PFI (provenance-filtered)"}
LAB2 = {"label_platinum": "Platinum status\n(TCGA 2011)", "label_pfiplat6": "PFI from first-line\nplatinum < 6 mo",
        "label_response": "First-course\nresponse (PD/SD)", "label_os18_all": "OS < 18 mo", "label_os24_all": "OS < 24 mo"}
SHORT = {"label_platinum": "Platinum\nstatus", "label_pfiplat6": "PFI from\nplatinum", "label_response": "Response\n(PD/SD)",
         "label_os18_all": "OS\n< 18 mo", "label_os24_all": "OS\n< 24 mo"}
FAMOF = {"label_platinum": "platinum", "label_pfiplat6": "platinum", "label_hybrid": "platinum", "label_combined_strict": "platinum",
         "label_response": "response", "label_os18_all": "os", "label_os24_all": "os",
         "label_os18": "os", "label_os24": "os"}

plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 8.5, "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 9.5, "axes.titleweight": "bold",
    "axes.titlecolor": INK, "axes.titlelocation": "left", "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": False, "legend.frameon": False, "savefig.dpi": 300,
    "savefig.bbox": "tight", "figure.facecolor": "white"})
VALUES = []


def note(fig, key, text):
    VALUES.append(f"- {fig} {key}: {text}")


def key(marker, filled, label):
    return Line2D([], [], linestyle="none", marker=marker, markersize=6.5, color=INK2,
                  markerfacecolor=INK2 if filled else "white", markeredgewidth=1.4, label=label)


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}")
    plt.close(fig)


def heat(ax, mat, rows, cols, vmin, vmax, fmt="{:.2f}"):
    im = ax.imshow(np.ma.masked_invalid(mat), cmap=BLUES, vmin=vmin, vmax=vmax, aspect="auto")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            if np.isnan(v):
                continue
            ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=8,
                    color="white" if (v - vmin) / (vmax - vmin) > 0.55 else INK)
    ax.set_xticks(range(len(cols)), cols); ax.set_yticks(range(len(rows)), rows)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-.5, len(cols)), minor=True); ax.set_yticks(np.arange(-.5, len(rows)), minor=True)
    ax.grid(which="minor", color="white", linewidth=2); ax.tick_params(which="minor", length=0)
    return im


def ref_line(ax, x=None):
    ax.axvline(x, color=BASE, linewidth=1, zorder=0)


# ── F1 ───────────────────────────────────────────────────────────────────────
def f1():
    cov = pd.read_csv(LV / "a11_coverage.csv").set_index("label")
    kp = pd.read_csv(LV / "a11_kappa_full.csv")
    ts = pd.read_csv(LV / "a11_os_test_full.csv")
    ts = ts[ts.reference == "label_platinum"]

    fig = plt.figure(figsize=(8.6, 5.9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.05], width_ratios=[1, 1.05], hspace=0.62, wspace=0.55)
    a, b = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
    gb = gs[1, :].subgridspec(1, 2, width_ratios=[2.2, 1], wspace=0.75)
    c, d = fig.add_subplot(gb[0]), fig.add_subplot(gb[1])
    rc = pd.read_csv(LV / "label_resource_v1_counts.csv")
    rc = rc[(rc.label == "label_combined_strict") & (rc.subset == "platinum_cohort")].iloc[0]
    cov.loc["label_combined_strict", ["determinate", "pos", "neg"]] = [int(rc.determinate), int(rc.n1), int(rc.n0)]

    rows = ORDER + ["label_hybrid", "label_combined_strict"]
    y = np.arange(len(rows))[::-1]
    for yi, lab in zip(y, rows):
        r = cov.loc[lab]
        col = FAM[FAMOF[lab]]
        a.barh(yi, r.pos, color=col, height=0.62)
        a.barh(yi, r.neg, left=r.pos, color=col, alpha=0.32, height=0.62)
        a.text(r.determinate + 8, yi, f"{int(r.determinate)} ({int(r.pos)})", va="center", fontsize=7.2, color=INK)
        note("F1A", lab, f"{int(r.determinate)}/489 determinate ({int(r.pos)} non-responder / {int(r.neg)} responder)")
    a.axvline(489, color=BASE, linewidth=1, linestyle=(0, (3, 2)))
    a.set_yticks(y, [LAB1[l] for l in rows]); a.tick_params(axis="y", labelsize=7)
    a.set_xlim(0, 620); a.set_xlabel("Platinum-treated patients with the label (of 489)")
    a.set_title("A  Coverage")
    a.legend(handles=[Patch(color=INK2, label="Non-responder / resistant"), Patch(color=INK2, alpha=0.32, label="Responder")],
             loc="upper center", bbox_to_anchor=(0.35, -0.24), ncol=2, fontsize=7, handlelength=1.2, columnspacing=1)

    k = np.full((5, 5), np.nan)
    for r in kp.itertuples():
        i, j = ORDER.index(r.label_a), ORDER.index(r.label_b)
        k[i, j] = k[j, i] = r.kappa
        note("F1B", f"κ {r.label_a}–{r.label_b}", f"{r.kappa:.3f} [{r.kappa_lo:.3f}, {r.kappa_hi:.3f}], n={r.n}")
    im = heat(b, k, [LAB2[l] for l in ORDER], [SHORT[l] for l in ORDER], 0, 1)
    b.tick_params(axis="x", labelsize=6.6); b.tick_params(axis="y", labelsize=6.8)
    b.set_title("B  Agreement (Cohen's κ)")
    cb = fig.colorbar(im, ax=b, fraction=0.045, pad=0.02)
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7, length=0)

    sw = pd.read_csv(LV / "a13_threshold_sweep.csv")
    sw = sw[sw.reference == "label_platinum"]
    t = sw.threshold_months.to_numpy()
    for col, lo, hi, nm, mk, filled in [("sensitivity", "sens_lo", "sens_hi", "Sensitivity", "o", True),
                                        ("specificity", "spec_lo", "spec_hi", "Specificity", "s", False),
                                        ("ppv", "ppv_lo", "ppv_hi", "PPV", "D", True)]:
        c.fill_between(t, sw[lo], sw[hi], color=FAM["os"], alpha=0.10, linewidth=0)
        c.plot(t, sw[col], color=FAM["os"], linewidth=1.4, marker=mk, markersize=4.5 if mk != "D" else 4,
               markerfacecolor=FAM["os"] if filled else "white", markeredgecolor=FAM["os"], label=nm)
    c.plot(t, sw.null_ppv, color=MUTED, linewidth=1, linestyle=(0, (4, 2)), label="PPV with no platinum information")
    for r in sw.itertuples():
        note("F1C", f"OS < {r.threshold_months} mo vs platinum (n {r.n})",
             f"sens {r.tp}/{r.tp + r.fn}={r.sensitivity:.3f} [{r.sens_lo:.3f},{r.sens_hi:.3f}]; spec {r.tn}/{r.tn + r.fp}={r.specificity:.3f}; "
             f"PPV {r.tp}/{r.tp + r.fp}={r.ppv:.3f} [{r.ppv_lo:.3f},{r.ppv_hi:.3f}]; null PPV {r.null_ppv:.3f}; kappa {r.kappa:.3f} (kmax {r.kappa_max:.3f})")
    for x in (18, 24):
        c.axvline(x, color=BASE, linewidth=1, zorder=0)
    c.set_xticks([6, 12, 18, 24, 30, 36, 42, 48, 60]); c.set_xlim(4, 62); c.set_ylim(0, 1.03)
    c.set_xlabel("OS threshold (months from diagnosis)"); c.set_ylabel("Proportion (95% CI)")
    c.set_title("C  OS < threshold as a test for platinum resistance")
    c.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2, fontsize=7, handletextpad=0.4, columnspacing=1.2)

    pv = pd.read_csv(LV / "a15b_provenance.csv")
    ad = pv[pv.group == "added_by_reconstruction"]
    recflag = ad.redacted | ad.adj_platinum_stop_missing | ad.later_line_before_event | ad.near_threshold
    # each patient counted once, in priority order: negative interval > death-dated call > other record flag > near-threshold only
    neg_ = ad.provenance_class == "negative_interval"
    death_ = ad.event_source.astype(str).eq("death_counted_as_progression") & ~neg_
    other_ = (ad.redacted | ad.adj_platinum_stop_missing | ad.later_line_before_event) & ~neg_ & ~death_
    near_ = ad.near_threshold & ~neg_ & ~death_ & ~other_
    cats = [("Unflagged, resistant", (ad.provenance_class == "clean_resistant").sum(), FAM["platinum"], 1.0),
            ("Unflagged, sensitive", (ad.provenance_class == "clean_sensitive").sum(), FAM["platinum"], 0.32),
            ("Flagged: 150–215 days only", near_.sum(), MUTED, 0.8),
            ("Flagged: other record\nproblem", other_.sum(), MUTED, 1.0),
            ("Resistant, dated\nby death only", death_.sum(), MUTED, 0.55),
            ("Negative interval", neg_.sum(), MUTED, 0.3)]
    assert sum(int(x[1]) for x in cats) == len(ad)
    yd = np.arange(len(cats))[::-1]
    for yi, (nm_, n_, col_, al_) in zip(yd, cats):
        d.barh(yi, n_, color=col_, alpha=al_, height=0.62)
        d.text(n_ + 1.5, yi, f"{int(n_)}", va="center", fontsize=7.2, color=INK)
        note("F1D", nm_.replace("\n", " "), f"{int(n_)} of {len(ad)} added patients")
    d.set_yticks(yd, [x[0] for x in cats]); d.tick_params(axis="y", labelsize=7)
    d.set_xlim(0, 80); d.set_xlabel("Patients added by the\nre-derived interval")
    d.set_title(f"D  Provenance of {len(ad)} added patients")
    save(fig, "F1_coverage_agreement")


# ── F2 ───────────────────────────────────────────────────────────────────────
def f2():
    a8 = pd.read_csv(LV / "a8_brca_tests.csv")
    a10 = pd.read_csv(LV / "a10_tests.csv")
    a10 = a10[a10.set == "T1_all"]
    fig, axes = plt.subplots(1, 4, figsize=(9.2, 2.9), sharey=True, gridspec_kw={"wspace": 0.14})
    y = np.arange(len(ORDER))[::-1]
    panels = [("A  BRCA1/2 carrier", "or", lambda lab: a8[(a8.set == "T1_all") & (a8.carrier_def == "primary_trunc_germ_som") & (a8.label == lab)].iloc[0]),
              ("B  CCNE1 amplified", "or", lambda lab: a8[(a8.set == "T4_CCNE1_amp") & (a8.label == lab)].iloc[0]),
              ("C  Residual > 1 cm", "or", lambda lab: a10[(a10.label == lab) & (a10.covariate == "residual_subopt")].iloc[0]),
              ("D  Aneuploidy score", "r", lambda lab: a10[(a10.label == lab) & (a10.covariate == "aneuploidy")].iloc[0])]
    for ax, (title, kind, get) in zip(axes, panels):
        for yi, lab in zip(y, ORDER):
            r = get(lab); col = FAM[FAMOF[lab]]
            if kind == "or":
                est = r.OR if "OR" in r.index else r.value
                lo, hi = r.lo, r.hi
                lo_plot = max(lo, 0.03)
                ax.plot([lo_plot, hi], [yi, yi], color=col, linewidth=1.5, solid_capstyle="round")
                ax.plot(max(est, 0.03), yi, "o", color=col, markersize=6.3, markeredgecolor="white", markeredgewidth=1, zorder=3)
                star = " *" if (hi < 1 or lo > 1) else ""
                ax.text(hi * 1.15, yi, f"{est:.2f}{star}", va="center", fontsize=7.2, color=INK)
                extra = (f"{int(r.exp_pos)}/{int(r.exp_n)} vs {int(r.unexp_pos)}/{int(r.unexp_n)}; " if "exp_pos" in r.index else f"n {int(r.n)}; ")
                note("F2" + title[0], lab, extra + f"OR {est:.3f} [{lo:.3f}, {hi:.3f}], p {r.p:.3g}")
            else:
                ax.plot([0, r.value], [yi, yi], color=GRID, linewidth=2, zorder=1)
                ax.plot(r.value, yi, "o", color=col, markersize=6.3, markeredgecolor="white", markeredgewidth=1, zorder=3)
                ax.text(max(r.value, 0) + 0.03, yi, f"{r.value:+.2f}" + (" *" if r.q_bh < 0.05 else ""), va="center", fontsize=7.2, color=INK)
                note("F2D", lab, f"aneuploidy r {r.value:+.3f}, q {r.q_bh:.3g}, n {int(r.n)}")
        if kind == "or":
            ax.set_xscale("log"); ref_line(ax, 1)
            ax.set_xlim(0.025, 30); ax.set_xticks([0.05, 0.25, 1, 4, 16], ["0.05", "0.25", "1", "4", "16"])
            ax.set_xlabel("Odds ratio, 95% CI (log)")
        else:
            ref_line(ax, 0); ax.set_xlim(-0.15, 0.45); ax.set_xlabel("Rank-biserial r")
        ax.set_title(title, fontsize=8.6)
    axes[0].set_yticks(y, [LAB1[l] for l in ORDER]); axes[0].tick_params(axis="y", labelsize=7)
    fig.tight_layout()
    save(fig, "F2_known_groups")


# ── F3 ───────────────────────────────────────────────────────────────────────
def f3():
    r5 = pd.read_csv(LV / "a5_cross_label_repeats.csv")
    o4 = ["label_platinum", "label_pfiplat6", "label_os18", "label_os24"]
    nm = {"label_platinum": "Platinum status\n(TCGA 2011)", "label_pfiplat6": "PFI from first-line\nplatinum < 6 mo",
          "label_os18": "OS < 18 mo", "label_os24": "OS < 24 mo"}
    sh = {"label_platinum": "Platinum\nstatus", "label_pfiplat6": "PFI from\nplatinum", "label_os18": "OS\n< 18 mo", "label_os24": "OS\n< 24 mo"}
    g = r5.groupby(["train_label", "test_label"]).auc
    m = g.mean().unstack().reindex(index=o4, columns=o4).values
    for i, tr in enumerate(o4):
        for j, te in enumerate(o4):
            s = r5[(r5.train_label == tr) & (r5.test_label == te)]
            note("F3", f"{tr}→{te}", f"mean {m[i, j]:.3f}; range over 3 models × 5 repeats {s.auc.min():.3f}–{s.auc.max():.3f}; "
                 f"n {int(s.n.iloc[0])} ({int(s.n_pos.iloc[0])} positive)")
    fig, (a, bx) = plt.subplots(1, 2, figsize=(8.6, 3.4), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=1.05))
    im = heat(a, m, [nm[l] for l in o4], [sh[l] for l in o4], 0.5, 0.75)
    a.tick_params(axis="both", labelsize=7)
    a.set_xlabel("Label predicted (held-out patients)"); a.set_ylabel("Label trained on")
    a.set_title("A  Cross-validated AUC (descriptive)")
    cb = fig.colorbar(im, ax=a, fraction=0.045, pad=0.03)
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7, length=0)
    pdf = pd.read_csv(LV / "a16_paired_differences.csv").set_index("contrast")
    fpb = pd.read_csv(LV / "a22_fullpipeline_replicates.csv")  # A22: whole pipeline refitted in 500 bootstrap samples
    cons = [("primary_dAUC24", "Platinum − OS < 24 mo trained\n(predicting platinum status)"),
            ("dAUC18", "Platinum − OS < 18 mo trained\n(predicting platinum status)"),
            ("reverse_OS24_target", "OS < 24 mo − platinum trained\n(predicting OS < 24 mo)")]
    yb = np.arange(len(cons))[::-1]
    for yi, (k_, lab_) in zip(yb, cons):
        r = pdf.loc[k_]
        flo, fhi = np.percentile(fpb[k_].dropna(), [2.5, 97.5])
        bx.plot([flo, fhi], [yi, yi], color=BASE, linewidth=5, solid_capstyle="butt", zorder=1,
                label="Whole pipeline refitted (500 bootstrap samples)" if yi == yb[0] else None)
        note("F3B", k_ + " full-pipeline", f"[{flo:+.3f}, {fhi:+.3f}]")
        bx.plot([r.boot_lo, r.boot_hi], [yi, yi], color=INK2, linewidth=1.5, solid_capstyle="round",
                label="Patients resampled, models not refitted" if yi == yb[0] else None)
        bx.plot(r.delta_repeat_averaged_scores, yi, "o", color=INK2, markersize=5.5, markeredgecolor="white", zorder=3)
        note("F3B", k_, f"{r.delta_repeat_averaged_scores:+.3f} [{r.boot_lo:+.3f}, {r.boot_hi:+.3f}], n {int(r.n)} ({int(r.n_pos)} positive)")
    ref_line(bx, 0)
    bx.set_yticks(yb, [c_[1] for c_ in cons]); bx.tick_params(axis="y", labelsize=6.8)
    bx.set_ylim(-0.6, len(cons) - 0.4); bx.set_xlim(-0.3, 0.3)
    bx.set_xlabel("Difference in AUC (95% intervals)")
    bx.legend(loc="upper center", bbox_to_anchor=(0.3, -0.2), ncol=1, fontsize=6.6, handlelength=1.6)
    bx.set_title("B  Same 134 patients")
    save(fig, "F3_cross_label_auc")



# ── F4 (exploratory) ─────────────────────────────────────────────────────────
def f4():
    cx = pd.read_csv(LV / "a13b_decomposition_cox.csv")  # A13b: PFI at risk at end of platinum; survival after progression unchanged
    cx = cx[cx.analysis.isin(["at_risk", "unchanged"])]
    rows = [("age10", "Age (per 10 years)"), ("residual_subopt", "Residual > 1 cm"), ("resid_any", "Any residual disease"),
            ("stage_iv", "Stage IV"), ("brca_carrier", "BRCA1/2 carrier"), ("ccne1_amp", "CCNE1 amplified"),
            ("aneuploidy_sd", "Aneuploidy Score (per SD)")]
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    y = np.arange(len(rows))[::-1]
    for yi, (v, nm) in zip(y, rows):
        for dy, o, col, lab in [(0.15, "PFI_from_platinum", FAM["platinum"], "Platinum-free interval"),
                                (-0.15, "survival_after_progression", FAM["os"], "Survival after progression")]:
            r = cx[(cx.covariate == v) & (cx.outcome == o)].iloc[0]
            ax.plot([r.lo, r.hi], [yi + dy] * 2, color=col, linewidth=1.5, solid_capstyle="round")
            ax.plot(r.HR, yi + dy, "o", color=col, markersize=5.5, markeredgecolor="white", markeredgewidth=0.8, zorder=3,
                    label=lab if yi == y[0] else None)
            note("F4", f"{v} / {o}", f"HR {r.HR:.3f} [{r.lo:.3f}, {r.hi:.3f}], p {r.p:.3g}, n {int(r.n)}/{int(r.events)}")
    ref_line(ax, 1); ax.set_xscale("log")
    ax.set_xticks([0.25, 0.5, 1, 2, 4], ["0.25", "0.5", "1", "2", "4"]); ax.set_xlim(0.25, 4)
    ax.set_yticks(y, [r[1] for r in rows]); ax.tick_params(axis="y", labelsize=7.5)
    ax.set_xlabel("Hazard ratio, 95% CI (log)")
    ax.set_title("Platinum-free interval and survival after progression (exploratory)", fontsize=8.6)
    ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.18), ncol=2, fontsize=7, handletextpad=0.3)
    fig.tight_layout()
    save(fig, "F4_os_decomposition")

# ── S1 Fig: GEO transfer ─────────────────────────────────────────────────────
def s1():
    t4 = pd.read_csv(LV / "a4_transfer_results.csv")
    t4 = t4[(t4.variant == "P") & (~t4.supplement.astype(bool))]
    o5 = ["label_platinum", "label_pfiplat6", "label_response", "label_os18", "label_os24"]
    nm = {"label_platinum": "Platinum status (TCGA 2011)", "label_pfiplat6": "PFI from first-line platinum < 6 mo",
          "label_response": "First-course response (PD/SD)", "label_os18": "OS < 18 mo", "label_os24": "OS < 24 mo"}
    fig, b = plt.subplots(figsize=(4.8, 3.0))
    y = np.arange(len(o5))[::-1]
    for yi, lab in zip(y, o5):
        col = FAM[FAMOF[lab]]
        for gl, dy, filled in [("dfs", 0.13, True), ("clinical", -0.13, False)]:
            s = t4[(t4.train_label == lab) & (t4.label == gl)].auc
            b.plot([s.min(), s.max()], [yi + dy] * 2, color=col, linewidth=1.5, solid_capstyle="round")
            b.plot(s.mean(), yi + dy, "o", color=col, markersize=6.3, markerfacecolor=col if filled else "white",
                   markeredgecolor=col if not filled else "white", markeredgewidth=1.5 if not filled else 1)
            note("S1_Fig", f"{lab} → {gl}", f"mean {s.mean():.3f}, range {s.min():.3f}–{s.max():.3f}")
    ref_line(b, 0.5)
    b.set_yticks(y, [nm[l] for l in o5]); b.tick_params(axis="y", labelsize=7)
    b.set_xlim(0.38, 0.8); b.set_ylim(-0.6, len(o5) - 0.4)
    b.set_xlabel("AUC on GSE63885 (mean; bar = range over 3 models)")
    b.set_title("Transfer to GSE63885")
    b.legend(handles=[key("o", True, "DFS < 180 d (34/74)"), key("o", False, "SD/PD (10/74)")],
             loc="upper center", bbox_to_anchor=(0.3, -0.22), ncol=2, fontsize=7, handletextpad=0.3, columnspacing=1)
    save(fig, "S1_Fig_transfer_GSE63885")


# ── S2 Fig: leakage ─────────────────────────────────────────────────────────
def s2():
    sup = pd.read_csv(RES_PINNED / "ablation_supervised_leakage_summary.csv")
    uns = pd.read_csv(RES_PINNED / "ablation_leakage_summary.csv")
    sup, uns = sup[sup.threshold_m.isin([18, 24])], uns[uns.threshold_m.isin([18, 24])]
    rows = [(f"{r.model.replace('Logistic Regression', 'LR').replace('Random Forest', 'RF')}, {r.threshold_m} mo", r.model, r.threshold_m)
            for r in sup.itertuples()]
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    y = np.arange(len(rows))[::-1]
    for yi, (lab, mdl, thr) in zip(y, rows):
        s = sup[(sup.model == mdl) & (sup.threshold_m == thr)].iloc[0].auc_inflation
        u = uns[(uns.model == mdl) & (uns.threshold_m == thr)].iloc[0].auc_inflation
        ax.plot([u, s], [yi, yi], color=GRID, linewidth=2, zorder=1)
        ax.plot(u, yi, "o", color=INK2, markerfacecolor="white", markersize=6, markeredgewidth=1.3, zorder=3,
                label="Variance filter, before split" if yi == y[0] else None)
        ax.plot(s, yi, "o", color=INK, markersize=6.5, markeredgecolor="white", markeredgewidth=1, zorder=4,
                label="Supervised F-score, before split" if yi == y[0] else None)
        ax.text(max(s, u) + 0.02, yi, f"+{s:.2f}" if s >= 0 else f"{s:.2f}", va="center", fontsize=7.5, color=INK)
        note("S2_Fig", lab, f"supervised inflation {s:+.4f}; unsupervised {u:+.4f}")
    note("S2_Fig", "means (18/24 mo)", f"supervised {sup.auc_inflation.mean():+.4f}; unsupervised {uns.auc_inflation.mean():+.4f}")
    ref_line(ax, 0)
    ax.set_yticks(y, [r[0] for r in rows]); ax.set_xlim(-0.05, 0.45)
    ax.set_xlabel("AUC inflation (leaky − leakage-free)")
    ax.set_title("Feature-selection leakage")
    ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.22), ncol=1, fontsize=7, handletextpad=0.2)
    fig.tight_layout()
    save(fig, "S2_Fig_leakage")


if __name__ == "__main__":
    f1(); f2(); f3(); f4(); s1(); s2()
    (OUT / "figure_values.md").write_text("# Values plotted in figures/v5 (for the number audit)\n\n" + "\n".join(VALUES) + "\n",
                                          encoding="utf-8")
    print("\n".join(VALUES))
