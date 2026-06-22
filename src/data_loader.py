"""
data_loader.py
──────────────
Handles all I/O for the TCGA OV pan-cancer atlas dataset.
Reads raw text files and returns clean DataFrames.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_clinical(data_dir: str | Path, filename: str) -> pd.DataFrame:
    """
    Load the clinical patient file.

    Args:
        data_dir: Directory containing the raw data files.
        filename: Name of the clinical patient file.

    Returns:
        DataFrame with one row per patient.
    """
    path = Path(data_dir) / filename
    logger.info("Loading clinical data from %s", path)

    df = pd.read_csv(path, sep="\t", comment="#", low_memory=False)
    logger.info("Clinical data shape: %s", df.shape)
    return df


def load_treatment(data_dir: str | Path, filename: str) -> pd.DataFrame:
    """
    Load the treatment timeline file.

    Args:
        data_dir: Directory containing the raw data files.
        filename: Name of the treatment timeline file.

    Returns:
        DataFrame with one row per treatment event.
    """
    path = Path(data_dir) / filename
    logger.info("Loading treatment data from %s", path)

    df = pd.read_csv(path, sep="\t", comment="#", low_memory=False)
    logger.info("Treatment data shape: %s", df.shape)
    return df


def load_expression(data_dir: str | Path, filename: str) -> pd.DataFrame:
    """
    Load the mRNA-seq (RSEM) expression matrix.

    The raw file has genes as rows and patients (sample IDs) as columns.
    This function does **not** perform any transformation — that is
    handled downstream in ``preprocessing.py``.

    Args:
        data_dir: Directory containing the raw data files.
        filename: Name of the mRNA expression file.

    Returns:
        Raw expression DataFrame (genes × samples).
    """
    path = Path(data_dir) / filename
    logger.info("Loading expression data from %s", path)

    df = pd.read_csv(path, sep="\t", comment="#", low_memory=False)
    logger.info("Expression data shape: %s", df.shape)
    return df


def load_clinical_sample(data_dir: str | Path, filename: str = "data_clinical_sample.txt") -> pd.DataFrame:
    """
    Load the sample-level clinical file (one row per tumor sample).

    Unlike data_clinical_patient.txt (one row per patient, mostly survival
    and demographics), this file typically carries sample-level genomic
    summary fields — tumor grade, MSI score, tumor mutation burden,
    aneuploidy score — which are candidate covariates for a more rigorous
    outcome model.

    Args:
        data_dir: Directory containing the raw data files.
        filename: Name of the clinical sample file.

    Returns:
        DataFrame with one row per sample.
    """
    path = Path(data_dir) / filename
    logger.info("Loading clinical sample data from %s", path)

    df = pd.read_csv(path, sep="\t", comment="#", low_memory=False)
    logger.info("Clinical sample data shape: %s", df.shape)
    return df


def load_timeline_status(data_dir: str | Path, filename: str = "data_timeline_status.txt") -> pd.DataFrame:
    """
    Load the disease-status timeline file (one row per status-check event,
    multiple rows per patient possible).

    This file is the most promising source for a true platinum-response
    label: it typically carries PRIMARY_THERAPY_OUTCOME_SUCCESS (direct
    response to first-line therapy), TUMOR_STATUS (disease/no evidence of
    disease at the timepoint), and CLINICAL_STAGE.

    Args:
        data_dir: Directory containing the raw data files.
        filename: Name of the timeline status file.

    Returns:
        DataFrame with one row per timeline event.
    """
    path = Path(data_dir) / filename
    logger.info("Loading timeline status data from %s", path)

    df = pd.read_csv(path, sep="\t", comment="#", low_memory=False)
    logger.info("Timeline status data shape: %s", df.shape)
    return df
