#!/usr/bin/env python3
"""
Merge human playstyle labels from CSV into a validator-ready dataset.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from validate_playstyle_categories import CATEGORY_DEFINITIONS, REPO_ROOT

logger = logging.getLogger(__name__)

DEFAULT_DATASET_PATH = REPO_ROOT / "datasets" / "validation" / "real_playstyle_sessions_unlabeled.json"
DEFAULT_CSV_PATH = REPO_ROOT / "datasets" / "validation" / "playstyle_annotation_form.csv"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "datasets" / "validation" / "real_playstyle_sessions.json"


def _parse_secondary_playstyles(value: str) -> List[str]:
    """
    Parse secondary playstyles from a semicolon- or comma-separated string.

    Args:
        value: Raw secondary-playstyle cell.

    Returns:
        Validated secondary playstyle list.

    Raises:
        ValueError: If a category is unknown.
    """
    if not value.strip():
        return []
    parts = [part.strip() for chunk in value.split(";") for part in chunk.split(",")]
    labels = [part for part in parts if part]
    unknown = [label for label in labels if label not in CATEGORY_DEFINITIONS]
    if unknown:
        raise ValueError(f"Unknown secondary_playstyles: {unknown}")
    return labels


def _parse_confidence(value: str) -> Optional[float]:
    """
    Parse confidence in [0, 1].

    Args:
        value: Raw confidence cell.

    Returns:
        Confidence float or None.

    Raises:
        ValueError: If confidence is not numeric or out of range.
    """
    if not value.strip():
        return None
    confidence = float(value)
    if confidence < 0 or confidence > 1:
        raise ValueError("confidence must be between 0 and 1")
    return confidence


def load_dataset(dataset_path: Path) -> Dict[str, Any]:
    """
    Load validator-ready dataset JSON.

    Args:
        dataset_path: Dataset path.

    Returns:
        Dataset payload.
    """
    with dataset_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict) or not isinstance(payload.get("sessions"), list):
        raise ValueError("Dataset must contain a sessions list")
    return payload


def load_annotation_rows(csv_path: Path) -> List[Dict[str, str]]:
    """
    Load annotation CSV rows.

    Args:
        csv_path: CSV path.

    Returns:
        Row dictionaries.
    """
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def rows_to_annotations(rows: List[Dict[str, str]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Convert CSV rows to session annotations.

    Args:
        rows: CSV row dictionaries.

    Returns:
        Mapping of session_id to annotations.
    """
    annotations_by_session: Dict[str, List[Dict[str, Any]]] = {}
    for row_number, row in enumerate(rows, start=2):
        session_id = row.get("session_id", "").strip()
        primary = row.get("primary_playstyle", "").strip()
        if not session_id or not primary:
            continue
        if primary not in CATEGORY_DEFINITIONS:
            raise ValueError(f"Unknown primary_playstyle '{primary}' at row {row_number}")

        annotator_id = row.get("annotator_id", "").strip()
        if not annotator_id:
            raise ValueError(f"annotator_id is required at row {row_number}")

        annotation = {
            "annotator_id": annotator_id,
            "primary_playstyle": primary,
            "secondary_playstyles": _parse_secondary_playstyles(row.get("secondary_playstyles", "")),
            "confidence": _parse_confidence(row.get("confidence", "")),
            "evidence": row.get("evidence", "").strip(),
        }
        annotations_by_session.setdefault(session_id, []).append(annotation)
    return annotations_by_session


def apply_annotations(
    dataset_path: Path = DEFAULT_DATASET_PATH,
    csv_path: Path = DEFAULT_CSV_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> Dict[str, Any]:
    """
    Merge CSV annotations into a dataset.

    Args:
        dataset_path: Input unlabeled dataset.
        csv_path: Completed annotation CSV.
        output_path: Output labeled dataset.

    Returns:
        Summary of applied annotations.
    """
    dataset = load_dataset(dataset_path)
    annotations_by_session = rows_to_annotations(load_annotation_rows(csv_path))
    known_sessions = {session["session_id"] for session in dataset["sessions"] if "session_id" in session}
    unknown_sessions = sorted(set(annotations_by_session) - known_sessions)
    if unknown_sessions:
        raise ValueError(f"CSV contains unknown session_id values: {unknown_sessions}")

    annotated_sessions = 0
    for session in dataset["sessions"]:
        session_id = session.get("session_id")
        annotations = annotations_by_session.get(session_id, [])
        if annotations:
            session["annotations"] = annotations
            annotated_sessions += 1

    metadata = dataset.setdefault("metadata", {})
    metadata["label_status"] = "annotated_from_csv" if annotated_sessions else "unlabeled"
    metadata["annotation_csv_path"] = str(csv_path.relative_to(REPO_ROOT) if csv_path.is_relative_to(REPO_ROOT) else csv_path)
    metadata["annotations_applied_at"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(dataset, handle, ensure_ascii=False, indent=2)

    return {
        "sessions": len(dataset["sessions"]),
        "annotated_sessions": annotated_sessions,
        "annotations": sum(len(value) for value in annotations_by_session.values()),
        "output_path": str(output_path),
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Apply playstyle labels from CSV.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser.parse_args()


def main() -> None:
    """Run the command-line CSV merge entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    args = parse_args()
    try:
        summary = apply_annotations(args.dataset, args.csv, args.output)
    except (OSError, ValueError) as exc:
        logger.error("Failed to apply playstyle annotations: %s", exc)
        raise SystemExit(1) from exc

    print("Playstyle annotations applied")
    print(f"- sessions: {summary['sessions']}")
    print(f"- annotated sessions: {summary['annotated_sessions']}")
    print(f"- annotations: {summary['annotations']}")
    print(f"- output: {summary['output_path']}")


if __name__ == "__main__":
    main()
