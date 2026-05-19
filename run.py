#!/usr/bin/env python3
"""
run.py
──────
Command-line entry point for the ovarian cancer platinum response pipeline.

Usage
─────
    python run.py                         # uses default config
    python run.py --config path/to/config.yaml
    python run.py --data-dir data/raw/my_dataset
    python run.py --thresholds 12 24      # only run 12m and 24m

Examples
────────
    python run.py --config config/config.yaml --data-dir data/raw/ov_tcga_pan_can_atlas_2018
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────


def setup_logging(level: str = "INFO") -> None:
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO),
                        format=fmt, datefmt=datefmt)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ovarian Cancer Platinum Response — ML Pipeline"
    )
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="Path to YAML configuration file (default: config/config.yaml)",
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Override the data directory in config (useful for quick testing)",
    )
    parser.add_argument(
        "--thresholds",
        nargs="+",
        type=int,
        default=None,
        help="Override survival thresholds to test, e.g. --thresholds 12 24",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)",
    )
    return parser.parse_args()


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    # Load config
    config_path = Path(args.config)
    if not config_path.exists():
        logger.error("Config file not found: %s", config_path)
        sys.exit(1)

    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    # CLI overrides
    if args.data_dir:
        cfg["data"]["data_dir"] = args.data_dir
        logger.info("Data directory overridden: %s", args.data_dir)

    if args.thresholds:
        cfg["clinical"]["thresholds"] = args.thresholds
        logger.info("Thresholds overridden: %s", args.thresholds)

    logger.info("Project: %s v%s", cfg["project"]["name"], cfg["project"]["version"])
    logger.info("Random seed: %d", cfg["project"]["seed"])

    # Run
    from src.pipeline import run_pipeline

    try:
        results = run_pipeline(cfg)
        logger.info("Pipeline finished successfully.")
        logger.info("Results table:\n%s", results["results_table"].to_string(index=False))
    except FileNotFoundError as exc:
        logger.error(
            "Data file not found: %s\n"
            "Make sure you have downloaded the TCGA OV dataset and set the "
            "correct path in config/config.yaml or via --data-dir.",
            exc,
        )
        sys.exit(1)
    except Exception as exc:
        logger.exception("Pipeline failed with unexpected error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
