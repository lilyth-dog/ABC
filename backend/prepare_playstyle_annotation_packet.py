#!/usr/bin/env python3
"""
Prepare annotation packets for real playstyle validation.

The packet intentionally omits model predictions so annotators can label
observable playstyle categories without being biased by the scoring tool.
"""
from __future__ import annotations

import argparse
import json
import logging
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from validate_playstyle_categories import CATEGORY_DEFINITIONS, REPO_ROOT

logger = logging.getLogger(__name__)

DEFAULT_PACKET_PATH = REPO_ROOT / "datasets" / "validation" / "playstyle_annotation_packet.json"
DEFAULT_UNLABELED_PATH = REPO_ROOT / "datasets" / "validation" / "real_playstyle_sessions_unlabeled.json"


def _load_json(path: Path) -> Optional[Dict[str, Any]]:
    """
    Load a JSON object if it exists.

    Args:
        path: JSON file path.

    Returns:
        Parsed object or None.
    """
    if not path.exists():
        logger.warning("Source file not found: %s", path)
        return None
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload if isinstance(payload, dict) else None


def _event_type_counts(raw_events: List[Mapping[str, Any]]) -> Dict[str, int]:
    """
    Count event types.

    Args:
        raw_events: Raw event objects.

    Returns:
        Event type counts.
    """
    return dict(Counter(str(event.get("type", "unknown")) for event in raw_events))


def _timeline_preview(raw_events: List[Mapping[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
    """
    Create an annotator-friendly event preview.

    Args:
        raw_events: Raw event objects.
        limit: Maximum preview length.

    Returns:
        Simplified event preview.
    """
    preview: List[Dict[str, Any]] = []
    for event in raw_events[:limit]:
        compact: Dict[str, Any] = {
            "type": event.get("type"),
            "timestamp": event.get("timestamp"),
        }
        for key in ["items", "item", "position", "from", "to", "block_type", "light_level"]:
            if key in event:
                compact[key] = event[key]
        preview.append(compact)
    return preview


def collect_candidate_sessions() -> List[Dict[str, Any]]:
    """
    Collect annotation candidates from committed public artifacts.

    Returns:
        Candidate sessions containing raw events.
    """
    candidates: List[Dict[str, Any]] = []

    full_pipeline = _load_json(REPO_ROOT / "datasets" / "public" / "full_pipeline_result.json")
    if full_pipeline and isinstance(full_pipeline.get("raw_events"), list):
        candidates.append(
            {
                "user_id": "public_sample_minecraft_user",
                "session_id": "public_full_pipeline_minecraft",
                "game_id": "minecraft",
                "source_file": "datasets/public/full_pipeline_result.json",
                "raw_events": full_pipeline["raw_events"],
            }
        )

    opendota = _load_json(REPO_ROOT / "datasets" / "public" / "opendota_real_match_8650963582.json")
    if opendota and isinstance(opendota.get("converted_events"), list):
        candidates.append(
            {
                "user_id": "public_sample_opendota_match",
                "session_id": "public_opendota_8650963582",
                "game_id": "opendota",
                "source_file": "datasets/public/opendota_real_match_8650963582.json",
                "raw_events": opendota["converted_events"],
                "notes": (
                    "Included for annotator review only. Current playstyle validator "
                    "categories are calibrated for Minecraft-like event metrics."
                ),
            }
        )

    return candidates


def build_annotation_packet(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build a model-output-free annotation packet.

    Args:
        candidates: Candidate raw-event sessions.

    Returns:
        Annotation packet.
    """
    return {
        "metadata": {
            "packet_name": "playstyle_annotation_packet",
            "packet_type": "annotation_packet",
            "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "claim_boundary": "Human annotators label observable playstyle categories, not personality traits.",
            "instructions": [
                "Review event summaries without model predictions.",
                "Choose one primary_playstyle from the fixed category set.",
                "Optionally add secondary_playstyles, confidence, and evidence.",
                "Use at least three independent annotators per session for real validation.",
            ],
            "categories": {
                key: {
                    "description": definition.description,
                    "minimum_signal": definition.minimum_signal,
                }
                for key, definition in CATEGORY_DEFINITIONS.items()
            },
        },
        "sessions": [
            {
                "session_id": candidate["session_id"],
                "user_id": candidate["user_id"],
                "game_id": candidate["game_id"],
                "source_file": candidate["source_file"],
                "event_count": len(candidate["raw_events"]),
                "event_type_counts": _event_type_counts(candidate["raw_events"]),
                "timeline_preview": _timeline_preview(candidate["raw_events"]),
                "notes": candidate.get("notes", ""),
                "annotation_form": {
                    "primary_playstyle": "",
                    "secondary_playstyles": [],
                    "confidence": "",
                    "evidence": "",
                },
            }
            for candidate in candidates
        ],
    }


def build_unlabeled_dataset(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build validator-compatible unlabeled session dataset.

    Args:
        candidates: Candidate raw-event sessions.

    Returns:
        Dataset with raw events and empty annotations.
    """
    minecraft_candidates = [candidate for candidate in candidates if candidate["game_id"] == "minecraft"]
    return {
        "metadata": {
            "dataset_name": "real_playstyle_sessions_unlabeled",
            "dataset_type": "annotation_ready_unlabeled",
            "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "purpose": "Holds raw sessions awaiting human playstyle annotations.",
            "label_status": "unlabeled",
            "notes": [
                "This file is safe to run through the validator before labels arrive.",
                "Accuracy will be n/a until labels.primary_playstyle or annotations[] are added.",
            ],
        },
        "sessions": [
            {
                "user_id": candidate["user_id"],
                "session_id": candidate["session_id"],
                "game_id": candidate["game_id"],
                "collection_context": {
                    "data_source": candidate["source_file"],
                    "scenario": "public_committed_sample",
                },
                "annotations": [],
                "raw_events": candidate["raw_events"],
            }
            for candidate in minecraft_candidates
        ],
    }


def write_annotation_artifacts(
    packet_path: Path = DEFAULT_PACKET_PATH,
    unlabeled_path: Path = DEFAULT_UNLABELED_PATH,
) -> Dict[str, Any]:
    """
    Write annotation packet and unlabeled validator dataset.

    Args:
        packet_path: Annotation packet output path.
        unlabeled_path: Unlabeled validation dataset path.

    Returns:
        Summary of written artifacts.
    """
    candidates = collect_candidate_sessions()
    packet = build_annotation_packet(candidates)
    unlabeled = build_unlabeled_dataset(candidates)

    packet_path.parent.mkdir(parents=True, exist_ok=True)
    unlabeled_path.parent.mkdir(parents=True, exist_ok=True)
    with packet_path.open("w", encoding="utf-8") as handle:
        json.dump(packet, handle, ensure_ascii=False, indent=2)
    with unlabeled_path.open("w", encoding="utf-8") as handle:
        json.dump(unlabeled, handle, ensure_ascii=False, indent=2)

    return {
        "candidate_sessions": len(candidates),
        "validator_ready_sessions": len(unlabeled["sessions"]),
        "packet_path": str(packet_path),
        "unlabeled_path": str(unlabeled_path),
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Prepare playstyle annotation packet.")
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET_PATH)
    parser.add_argument("--unlabeled", type=Path, default=DEFAULT_UNLABELED_PATH)
    return parser.parse_args()


def main() -> None:
    """Run the command-line annotation packet builder."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    args = parse_args()
    summary = write_annotation_artifacts(args.packet, args.unlabeled)
    print("Playstyle annotation artifacts prepared")
    print(f"- candidate sessions: {summary['candidate_sessions']}")
    print(f"- validator-ready sessions: {summary['validator_ready_sessions']}")
    print(f"- packet: {summary['packet_path']}")
    print(f"- unlabeled dataset: {summary['unlabeled_path']}")


if __name__ == "__main__":
    main()
