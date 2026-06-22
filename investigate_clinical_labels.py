#!/usr/bin/env python3
"""
investigate_clinical_labels.py
────────────────────────────────
Phase 2 diagnostic: is PRIMARY_THERAPY_OUTCOME_SUCCESS (or another flagged
column) usable as a direct platinum-response label, replacing the
OS-threshold proxy?

This script is READ-ONLY with respect to the main pipeline — it does not
modify config.yaml, preprocessing.py, or any existing labels. It produces
a diagnostic report so we can decide how (or whether) to proceed with
relabeling before writing that code into the real pipeline.

Usage:
    python investigate_clinical_labels.py
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)

    with open("config/config.yaml") as f:
        cfg = yaml.safe_load(f)

    from src.data_loader import load_clinical, load_clinical_sample, load_timeline_status, load_treatment
    from src.label_investigation import (
        check_within_patient_consistency,
        cross_tabulate_against_os_labels,
        map_therapy_outcome_to_binary,
        report_column_coverage,
        report_recall_on_confirmed_nonresponders,
        report_value_distribution,
    )
    from src.preprocessing import build_labelled_survival, extract_survival, identify_platinum_patients

    results_dir = Path(cfg["output"]["results_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 70)
    logger.info("PHASE 2 DIAGNOSTIC: Clinical Label Investigation")
    logger.info("=" * 70)

    # ── Load data ──────────────────────────────────────────────────────
    data_dir = cfg["data"]["data_dir"]
    clinical = load_clinical(data_dir, cfg["data"]["clinical_file"])
    treatment = load_treatment(data_dir, cfg["data"]["treatment_file"])

    try:
        timeline_status = load_timeline_status(data_dir)
    except FileNotFoundError:
        logger.error(
            "data_timeline_status.txt not found in %s — cannot run this investigation.", data_dir
        )
        sys.exit(1)

    try:
        clinical_sample = load_clinical_sample(data_dir)
    except FileNotFoundError:
        logger.warning("data_clinical_sample.txt not found — skipping that portion.")
        clinical_sample = None

    # ── Existing pipeline labels (for comparison) ─────────────────────
    surv = extract_survival(clinical, cfg["clinical"]["time_col"], cfg["clinical"]["status_col"])
    platinum_ids = identify_platinum_patients(treatment, cfg["clinical"]["platinum_drugs"])
    os_labelled_dict = build_labelled_survival(
        surv, platinum_ids, cfg["clinical"]["time_col"], cfg["clinical"]["thresholds"]
    )

    # ── 1. Full column inventory (so nothing is missed) ───────────────
    logger.info("\n" + "-" * 70)
    logger.info("data_timeline_status.txt columns (%d total): %s", len(timeline_status.columns), list(timeline_status.columns))
    if clinical_sample is not None:
        logger.info("data_clinical_sample.txt columns (%d total): %s", len(clinical_sample.columns), list(clinical_sample.columns))

    # ── 2. Coverage report ──────────────────────────────────────────────
    logger.info("\n" + "-" * 70)
    logger.info("COVERAGE: data_timeline_status.txt (restricted to platinum cohort)")
    timeline_candidates = ["PRIMARY_THERAPY_OUTCOME_SUCCESS", "CLINICAL_STAGE", "TUMOR_STATUS"]
    timeline_candidates = [c for c in timeline_candidates if c in timeline_status.columns]
    coverage_timeline = report_column_coverage(
        timeline_status, timeline_candidates, platinum_ids=platinum_ids
    )
    coverage_timeline.to_csv(results_dir / "label_investigation_coverage_timeline.csv", index=False)

    if clinical_sample is not None:
        logger.info("\n" + "-" * 70)
        logger.info("COVERAGE: data_clinical_sample.txt (restricted to platinum cohort)")
        sample_candidates = ["GRADE", "MSI_SCORE_MANTIS", "MSI_SENSOR_SCORE", "TMB_NONSYNONYMOUS", "ANEUPLOIDY_SCORE"]
        sample_candidates = [c for c in sample_candidates if c in clinical_sample.columns]
        coverage_sample = report_column_coverage(
            clinical_sample, sample_candidates, patient_id_col="PATIENT_ID", platinum_ids=platinum_ids
        )
        coverage_sample.to_csv(results_dir / "label_investigation_coverage_sample.csv", index=False)

    # ── 3. Value distribution for the key candidate label ──────────────
    if "PRIMARY_THERAPY_OUTCOME_SUCCESS" in timeline_status.columns:
        logger.info("\n" + "-" * 70)
        logger.info("VALUE DISTRIBUTION: PRIMARY_THERAPY_OUTCOME_SUCCESS")
        report_value_distribution(timeline_status, "PRIMARY_THERAPY_OUTCOME_SUCCESS")

        # ── 4. Within-patient consistency (multiple timeline rows) ─────
        logger.info("\n" + "-" * 70)
        logger.info("WITHIN-PATIENT CONSISTENCY: PRIMARY_THERAPY_OUTCOME_SUCCESS")
        consistency = check_within_patient_consistency(timeline_status, "PRIMARY_THERAPY_OUTCOME_SUCCESS")
        logger.info(consistency)

        # ── 5. Build candidate binary label + cross-tab vs OS proxy ────
        logger.info("\n" + "-" * 70)
        logger.info("CANDIDATE LABEL: mapping PRIMARY_THERAPY_OUTCOME_SUCCESS to binary response")
        candidate_labels = map_therapy_outcome_to_binary(timeline_status)
        candidate_labels.to_csv(results_dir / "label_investigation_candidate_labels.csv", header=["candidate_response"])

        logger.info("\n" + "-" * 70)
        logger.info("CROSS-TABULATION vs. existing OS-threshold proxy labels")
        crosstab = cross_tabulate_against_os_labels(candidate_labels, os_labelled_dict)
        crosstab.to_csv(results_dir / "label_investigation_crosstab_vs_os.csv", index=False)

        # Cohen's kappa collapses toward zero under extreme class imbalance
        # even with high raw agreement — recall on the small set of
        # documented non-responders is the more decision-relevant check.
        logger.info("\n" + "-" * 70)
        logger.info("RECALL: does the OS-threshold proxy correctly flag documented non-responders?")
        recall_report = report_recall_on_confirmed_nonresponders(candidate_labels, os_labelled_dict)
        recall_report.to_csv(results_dir / "label_investigation_recall_on_confirmed.csv", index=False)

    if "TUMOR_STATUS" in timeline_status.columns:
        logger.info("\n" + "-" * 70)
        logger.info("VALUE DISTRIBUTION: TUMOR_STATUS")
        report_value_distribution(timeline_status, "TUMOR_STATUS")

    if clinical_sample is not None and "GRADE" in clinical_sample.columns:
        logger.info("\n" + "-" * 70)
        logger.info("VALUE DISTRIBUTION: GRADE")
        report_value_distribution(clinical_sample, "GRADE")

    logger.info("\n" + "=" * 70)
    logger.info("Investigation complete. CSV outputs in: %s", results_dir)
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
