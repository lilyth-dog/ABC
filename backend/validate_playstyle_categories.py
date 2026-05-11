#!/usr/bin/env python3
"""
Validate playstyle category analysis against labeled session fixtures.

This module treats the system as a category-analysis tool for observable play
styles, not as a tool that claims to infer a user's true personality.
"""
from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from game_event_parser import parse_game_events

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = REPO_ROOT / "datasets" / "validation" / "labeled_playstyle_sessions.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "datasets" / "public" / "playstyle_validation_report.json"


@dataclass(frozen=True)
class CategoryDefinition:
    """Definition for an observable playstyle category."""

    name: str
    description: str
    minimum_signal: str


CATEGORY_DEFINITIONS: Dict[str, CategoryDefinition] = {
    "planner": CategoryDefinition(
        name="planner",
        description="Preparation actions before the first build action.",
        minimum_signal="At least one preparation action and one build action.",
    ),
    "iterative_refiner": CategoryDefinition(
        name="iterative_refiner",
        description="Frequent placement revisions at the same location.",
        minimum_signal="At least one block_place followed by a matching block_break.",
    ),
    "route_optimizer": CategoryDefinition(
        name="route_optimizer",
        description="Efficient movement path across multiple movement events.",
        minimum_signal="At least two player_move events.",
    ),
    "complex_builder": CategoryDefinition(
        name="complex_builder",
        description="High spatial spread and vertical variation in build events.",
        minimum_signal="At least two block_place events with positions.",
    ),
    "resource_diversifier": CategoryDefinition(
        name="resource_diversifier",
        description="Broad variety of inventory and block resources.",
        minimum_signal="Inventory or block type diversity.",
    ),
    "risk_taker": CategoryDefinition(
        name="risk_taker",
        description="Actions in low-height or low-light positions.",
        minimum_signal="Positioned actions with y < 40 or light_level < 7.",
    ),
}


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    """
    Clamp a numeric value to a closed interval.

    Args:
        value: Value to clamp.
        lower: Lower bound.
        upper: Upper bound.

    Returns:
        Clamped value.
    """
    return max(lower, min(upper, value))


def extract_event_features(raw_events: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Extract lightweight event-count features for category gating.

    Args:
        raw_events: Raw event dictionaries.

    Returns:
        Dictionary of event-count features.
    """
    preparation_types = {"inventory_change", "player_move", "item_craft"}
    resource_types = set()
    risky_events = 0

    for event in raw_events:
        if event.get("type") == "inventory_change":
            items = event.get("items", [])
            if isinstance(items, list):
                resource_types.update(str(item) for item in items)
        if event.get("type") == "block_place" and event.get("block_type"):
            resource_types.add(str(event["block_type"]))

        position = event.get("position", {})
        if isinstance(position, dict) and (
            position.get("y", 64) < 40 or event.get("light_level", 15) < 7
        ):
            risky_events += 1

    return {
        "event_count": len(raw_events),
        "preparation_count": sum(1 for event in raw_events if event.get("type") in preparation_types),
        "build_count": sum(1 for event in raw_events if event.get("type") == "block_place"),
        "move_count": sum(1 for event in raw_events if event.get("type") == "player_move"),
        "resource_type_count": len(resource_types),
        "risky_event_count": risky_events,
    }


def score_playstyle_categories(
    metrics: Mapping[str, Any],
    event_features: Mapping[str, int],
) -> Dict[str, float]:
    """
    Score observable playstyle categories from parser metrics.

    Args:
        metrics: Parsed behavior metrics from game_event_parser.
        event_features: Lightweight counts derived from raw events.

    Returns:
        Category score dictionary in [0, 1].
    """
    has_build = event_features.get("build_count", 0) > 0
    has_preparation = event_features.get("preparation_count", 0) > 0
    has_movement_path = event_features.get("move_count", 0) >= 2
    has_complex_build_signal = event_features.get("build_count", 0) >= 2
    has_resource_signal = event_features.get("resource_type_count", 0) > 0
    has_risk_signal = event_features.get("risky_event_count", 0) > 0

    scores = {
        "planner": _clamp(float(metrics.get("planning_time", 0)) / 5000.0)
        if has_build and has_preparation
        else 0.0,
        "iterative_refiner": _clamp(float(metrics.get("revision_count", 0)) / 3.0),
        "route_optimizer": _clamp(float(metrics.get("path_efficiency", 0)))
        if has_movement_path
        else 0.0,
        "complex_builder": _clamp(float(metrics.get("complexity", 0)))
        if has_complex_build_signal
        else 0.0,
        "resource_diversifier": _clamp(float(metrics.get("diversity", 0)))
        if has_resource_signal
        else 0.0,
        "risk_taker": _clamp(float(metrics.get("risk_taking", 0)))
        if has_risk_signal
        else 0.0,
    }
    return {key: round(value, 4) for key, value in scores.items()}


def predict_primary_category(scores: Mapping[str, float]) -> str:
    """
    Select the highest-scoring playstyle category.

    Args:
        scores: Category score dictionary.

    Returns:
        Predicted primary category, or "uncategorized" if all scores are zero.
    """
    if not scores:
        return "uncategorized"
    category, score = max(scores.items(), key=lambda item: (item[1], item[0]))
    return category if score > 0 else "uncategorized"


def _count_labels(labels: List[str]) -> Dict[str, int]:
    """
    Count category labels.

    Args:
        labels: Category labels.

    Returns:
        Count per category.
    """
    counts: Dict[str, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts


def _pairwise_agreement(labels: List[str]) -> Optional[float]:
    """
    Compute pairwise percent agreement for annotation labels.

    Args:
        labels: Annotator category labels.

    Returns:
        Pairwise agreement in [0, 1], or None when fewer than two labels exist.
    """
    if len(labels) < 2:
        return None

    total_pairs = len(labels) * (len(labels) - 1) / 2
    counts = _count_labels(labels)
    agreeing_pairs = sum(count * (count - 1) / 2 for count in counts.values())
    return round(agreeing_pairs / total_pairs, 4)


def _annotation_labels(session: Mapping[str, Any]) -> List[str]:
    """
    Extract valid annotation labels from a session.

    Args:
        session: Session payload.

    Returns:
        Annotator primary playstyle labels.
    """
    annotations = session.get("annotations", [])
    if not isinstance(annotations, list):
        return []

    labels: List[str] = []
    for annotation in annotations:
        if isinstance(annotation, dict):
            label = annotation.get("primary_playstyle")
            if isinstance(label, str) and label in CATEGORY_DEFINITIONS:
                labels.append(label)
    return labels


def resolve_expected_label(session: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Resolve a session's expected primary category from labels or annotations.

    Args:
        session: Session payload.

    Returns:
        Expected-label metadata.
    """
    labels = session.get("labels", {})
    explicit = labels.get("primary_playstyle") if isinstance(labels, dict) else None
    annotator_labels = _annotation_labels(session)
    vote_counts = _count_labels(annotator_labels)
    agreement = _pairwise_agreement(annotator_labels)

    if explicit:
        return {
            "expected": explicit,
            "source": "labels.primary_playstyle",
            "annotation_vote_counts": vote_counts,
            "annotation_pairwise_agreement": agreement,
        }

    if not vote_counts:
        return {
            "expected": None,
            "source": "unlabeled",
            "annotation_vote_counts": vote_counts,
            "annotation_pairwise_agreement": agreement,
        }

    sorted_votes = sorted(vote_counts.items(), key=lambda item: (-item[1], item[0]))
    top_label, top_count = sorted_votes[0]
    tied_labels = [label for label, count in sorted_votes if count == top_count]
    if len(tied_labels) > 1:
        return {
            "expected": None,
            "source": "annotation_tie",
            "annotation_vote_counts": vote_counts,
            "annotation_pairwise_agreement": agreement,
            "tied_labels": tied_labels,
        }

    return {
        "expected": top_label,
        "source": "annotation_majority",
        "annotation_vote_counts": vote_counts,
        "annotation_pairwise_agreement": agreement,
    }


def _validate_dataset_payload(payload: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """
    Validate and return sessions from a dataset payload.

    Args:
        payload: Parsed dataset JSON.

    Returns:
        Session list.

    Raises:
        ValueError: If the dataset structure is invalid.
    """
    sessions = payload.get("sessions")
    if not isinstance(sessions, list) or not sessions:
        raise ValueError("Dataset must contain a non-empty 'sessions' list")

    for index, session in enumerate(sessions):
        if not isinstance(session, dict):
            raise ValueError(f"Session {index} must be an object")
        if not session.get("session_id"):
            raise ValueError(f"Session {index} is missing session_id")
        if not isinstance(session.get("raw_events"), list):
            raise ValueError(f"Session {session.get('session_id')} is missing raw_events list")
        labels = session.get("labels", {})
        primary = labels.get("primary_playstyle") if isinstance(labels, dict) else None
        if primary and primary not in CATEGORY_DEFINITIONS:
            raise ValueError(f"Unknown primary_playstyle '{primary}' in {session.get('session_id')}")
        annotations = session.get("annotations", [])
        if annotations and not isinstance(annotations, list):
            raise ValueError(f"annotations must be a list in {session.get('session_id')}")
        for annotation in annotations if isinstance(annotations, list) else []:
            if not isinstance(annotation, dict):
                raise ValueError(f"Each annotation must be an object in {session.get('session_id')}")
            annotation_label = annotation.get("primary_playstyle")
            if annotation_label and annotation_label not in CATEGORY_DEFINITIONS:
                raise ValueError(
                    f"Unknown annotation primary_playstyle '{annotation_label}' in {session.get('session_id')}"
                )
    return sessions


def load_labeled_sessions(dataset_path: Path) -> Dict[str, Any]:
    """
    Load a labeled playstyle dataset.

    Args:
        dataset_path: JSON dataset path.

    Returns:
        Parsed dataset payload.

    Raises:
        FileNotFoundError: If the path does not exist.
        ValueError: If JSON or schema validation fails.
    """
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    try:
        with dataset_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON dataset: {exc}") from exc

    _validate_dataset_payload(payload)
    return payload


def analyze_session(session: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Analyze one labeled playstyle session.

    Args:
        session: Session payload with raw_events and optional labels.

    Returns:
        Per-session analysis result.
    """
    raw_events = session["raw_events"]
    game_id = str(session.get("game_id", "minecraft"))
    metrics = parse_game_events(game_id, raw_events)
    event_features = extract_event_features(raw_events)
    scores = score_playstyle_categories(metrics, event_features)
    predicted = predict_primary_category(scores)

    expected_info = resolve_expected_label(session)
    expected = expected_info["expected"]
    return {
        "user_id": session.get("user_id"),
        "session_id": session.get("session_id"),
        "game_id": game_id,
        "expected_primary_playstyle": expected,
        "expected_label_source": expected_info["source"],
        "annotation_vote_counts": expected_info["annotation_vote_counts"],
        "annotation_pairwise_agreement": expected_info["annotation_pairwise_agreement"],
        "predicted_primary_playstyle": predicted,
        "is_correct": predicted == expected if expected else None,
        "category_scores": scores,
        "parsed_metrics": metrics,
        "event_features": event_features,
    }


def summarize_results(session_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize labeled playstyle validation results.

    Args:
        session_results: Per-session analysis results.

    Returns:
        Aggregate metrics and confusion table.
    """
    labeled = [result for result in session_results if result["expected_primary_playstyle"]]
    correct = [result for result in labeled if result["is_correct"]]
    agreement_values = [
        float(result["annotation_pairwise_agreement"])
        for result in session_results
        if result.get("annotation_pairwise_agreement") is not None
    ]

    confusion: Dict[str, Dict[str, int]] = {}
    failures: List[Dict[str, Any]] = []
    for result in labeled:
        expected = str(result["expected_primary_playstyle"])
        predicted = str(result["predicted_primary_playstyle"])
        confusion.setdefault(expected, {})
        confusion[expected][predicted] = confusion[expected].get(predicted, 0) + 1
        if expected != predicted:
            failures.append(
                {
                    "session_id": result["session_id"],
                    "expected": expected,
                    "predicted": predicted,
                    "scores": result["category_scores"],
                }
            )

    return {
        "labeled_sessions": len(labeled),
        "correct_predictions": len(correct),
        "accuracy": round(len(correct) / len(labeled), 4) if labeled else None,
        "annotated_sessions": sum(1 for result in session_results if result["annotation_vote_counts"]),
        "mean_pairwise_annotation_agreement": (
            round(sum(agreement_values) / len(agreement_values), 4) if agreement_values else None
        ),
        "confusion": confusion,
        "failures": failures,
    }


def validate_playstyle_categories(
    dataset_path: Path = DEFAULT_DATASET_PATH,
    output_path: Optional[Path] = DEFAULT_OUTPUT_PATH,
) -> Dict[str, Any]:
    """
    Validate playstyle category analysis against a labeled dataset.

    Args:
        dataset_path: Input dataset path.
        output_path: Optional output report path.

    Returns:
        Validation report.
    """
    dataset = load_labeled_sessions(dataset_path)
    sessions = _validate_dataset_payload(dataset)
    session_results = [analyze_session(session) for session in sessions]
    summary = summarize_results(session_results)

    report = {
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "dataset_path": str(dataset_path.relative_to(REPO_ROOT) if dataset_path.is_relative_to(REPO_ROOT) else dataset_path),
        "dataset_metadata": dataset.get("metadata", {}),
        "claim_boundary": (
            "This validates observable playstyle category scoring. It does not validate "
            "claims about inferring a user's true personality."
        ),
        "category_definitions": {
            key: {
                "description": definition.description,
                "minimum_signal": definition.minimum_signal,
            }
            for key, definition in CATEGORY_DEFINITIONS.items()
        },
        "summary": summary,
        "sessions": session_results,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
    return report


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validate labeled playstyle categories.")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET_PATH,
        help="Path to labeled playstyle sessions JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Path for validation report JSON.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the playstyle validation command-line entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    args = parse_args()
    try:
        report = validate_playstyle_categories(args.dataset, args.output)
    except (FileNotFoundError, ValueError) as exc:
        logger.error("Playstyle validation failed: %s", exc)
        raise SystemExit(1) from exc

    summary = report["summary"]
    print("Playstyle category validation complete")
    print(
        f"- labeled accuracy: {summary['correct_predictions']}/"
        f"{summary['labeled_sessions']} ({summary['accuracy']:.2%})"
    )
    print(f"- failures: {len(summary['failures'])}")
    print(f"- report: {args.output}")


if __name__ == "__main__":
    main()
