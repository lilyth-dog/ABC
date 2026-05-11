"""
Tests for playstyle category validation.
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validate_playstyle_categories import (
    DEFAULT_DATASET_PATH,
    extract_event_features,
    resolve_expected_label,
    score_playstyle_categories,
    validate_playstyle_categories,
)


class TestPlaystyleCategoryValidation:
    """Test playstyle category scoring and validation."""

    def test_score_playstyle_categories_prefers_planner(self):
        """Planner score should dominate for long preparation before build."""
        metrics = {
            "planning_time": 6000,
            "revision_count": 0,
            "path_efficiency": 1.0,
            "complexity": 0.0,
            "diversity": 0.1,
            "risk_taking": 0.0,
        }
        features = {
            "preparation_count": 2,
            "build_count": 1,
            "move_count": 0,
            "resource_type_count": 2,
            "risky_event_count": 0,
        }

        scores = score_playstyle_categories(metrics, features)

        assert scores["planner"] == 1.0
        assert scores["planner"] > scores["resource_diversifier"]

    def test_extract_event_features_counts_signals(self):
        """Raw event features should count resources, movement, and risk."""
        raw_events = [
            {"type": "inventory_change", "items": ["stone", "glass"]},
            {"type": "player_move", "from": {"x": 0}, "to": {"x": 1}},
            {"type": "block_place", "position": {"x": 0, "y": 20, "z": 0}, "block_type": "minecraft:stone"},
        ]

        features = extract_event_features(raw_events)

        assert features["preparation_count"] == 2
        assert features["move_count"] == 1
        assert features["build_count"] == 1
        assert features["resource_type_count"] == 3
        assert features["risky_event_count"] == 1

    def test_default_fixture_validates_all_primary_categories(self, tmp_path):
        """Synthetic calibration fixture should classify all labeled sessions."""
        output_path = tmp_path / "playstyle_validation_report.json"

        report = validate_playstyle_categories(DEFAULT_DATASET_PATH, output_path)

        assert output_path.exists()
        assert report["summary"]["labeled_sessions"] == 6
        assert report["summary"]["correct_predictions"] == 6
        assert report["summary"]["accuracy"] == 1.0
        assert report["summary"]["failures"] == []

    def test_resolve_expected_label_uses_annotation_majority(self):
        """Annotation majority should become the expected label without explicit labels."""
        session = {
            "session_id": "annotated_session_001",
            "annotations": [
                {"annotator_id": "a1", "primary_playstyle": "planner"},
                {"annotator_id": "a2", "primary_playstyle": "planner"},
                {"annotator_id": "a3", "primary_playstyle": "route_optimizer"},
            ],
        }

        expected = resolve_expected_label(session)

        assert expected["expected"] == "planner"
        assert expected["source"] == "annotation_majority"
        assert expected["annotation_vote_counts"] == {"planner": 2, "route_optimizer": 1}
        assert expected["annotation_pairwise_agreement"] == 0.3333

    def test_real_style_dataset_with_annotations_reports_agreement(self, tmp_path):
        """Validation should report majority labels and pairwise annotator agreement."""
        dataset_path = tmp_path / "annotated_playstyle_sessions.json"
        output_path = tmp_path / "annotated_playstyle_report.json"
        dataset_path.write_text(
            """
{
  "metadata": {"dataset_type": "real_collection_template_test"},
  "sessions": [
    {
      "user_id": "annotated_planner_001",
      "session_id": "annotated_planner_session_001",
      "game_id": "minecraft",
      "annotations": [
        {"annotator_id": "a1", "primary_playstyle": "planner"},
        {"annotator_id": "a2", "primary_playstyle": "planner"},
        {"annotator_id": "a3", "primary_playstyle": "route_optimizer"}
      ],
      "raw_events": [
        {"type": "inventory_change", "timestamp": 1000, "items": ["stone"]},
        {"type": "item_craft", "timestamp": 3000, "item": "minecraft:planks"},
        {"type": "block_place", "timestamp": 7000, "position": {"x": 0, "y": 64, "z": 0}, "block_type": "minecraft:stone"}
      ]
    }
  ]
}
""",
            encoding="utf-8",
        )

        report = validate_playstyle_categories(dataset_path, output_path)

        assert output_path.exists()
        assert report["summary"]["labeled_sessions"] == 1
        assert report["summary"]["correct_predictions"] == 1
        assert report["summary"]["annotated_sessions"] == 1
        assert report["summary"]["mean_pairwise_annotation_agreement"] == 0.3333
        assert report["sessions"][0]["expected_label_source"] == "annotation_majority"
