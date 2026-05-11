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
