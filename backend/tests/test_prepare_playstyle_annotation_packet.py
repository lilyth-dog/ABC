"""
Tests for playstyle annotation packet preparation.
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prepare_playstyle_annotation_packet import (
    build_annotation_packet,
    build_annotation_form_rows,
    build_unlabeled_dataset,
    collect_candidate_sessions,
    write_annotation_artifacts,
)


class TestPreparePlaystyleAnnotationPacket:
    """Test annotation packet preparation."""

    def test_collect_candidate_sessions_finds_public_samples(self):
        """Committed public artifacts should provide annotation candidates."""
        candidates = collect_candidate_sessions()

        assert len(candidates) >= 1
        assert any(candidate["game_id"] == "minecraft" for candidate in candidates)

    def test_build_annotation_packet_omits_model_predictions(self):
        """Annotation packets should not include predicted category fields."""
        candidates = [
            {
                "user_id": "u1",
                "session_id": "s1",
                "game_id": "minecraft",
                "source_file": "source.json",
                "raw_events": [{"type": "inventory_change", "timestamp": 1000, "items": ["stone"]}],
            }
        ]

        packet = build_annotation_packet(candidates)
        session = packet["sessions"][0]

        assert "predicted_primary_playstyle" not in session
        assert session["annotation_form"]["primary_playstyle"] == ""
        assert session["event_type_counts"] == {"inventory_change": 1}

    def test_write_annotation_artifacts(self, tmp_path):
        """Artifact writer should create packet and validator-ready dataset."""
        packet_path = tmp_path / "packet.json"
        unlabeled_path = tmp_path / "unlabeled.json"
        csv_path = tmp_path / "labels.csv"

        summary = write_annotation_artifacts(packet_path, unlabeled_path, csv_path)

        assert packet_path.exists()
        assert unlabeled_path.exists()
        assert csv_path.exists()
        assert summary["candidate_sessions"] >= 1
        assert summary["validator_ready_sessions"] >= 1
        assert summary["csv_rows"] >= 3

    def test_build_annotation_form_rows_creates_three_rows_per_minecraft_session(self):
        """CSV form rows should target validator-ready Minecraft sessions."""
        candidates = [
            {
                "user_id": "u1",
                "session_id": "s1",
                "game_id": "minecraft",
                "source_file": "source.json",
                "raw_events": [],
            },
            {
                "user_id": "u2",
                "session_id": "s2",
                "game_id": "opendota",
                "source_file": "source.json",
                "raw_events": [],
            },
        ]

        rows = build_annotation_form_rows(candidates, annotators_per_session=3)

        assert len(rows) == 3
        assert {row["session_id"] for row in rows} == {"s1"}
        assert rows[0]["annotator_id"] == "annotator_1"
