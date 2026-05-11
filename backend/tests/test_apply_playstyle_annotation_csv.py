"""
Tests for applying playstyle annotations from CSV.
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apply_playstyle_annotation_csv import apply_annotations
from validate_playstyle_categories import validate_playstyle_categories


class TestApplyPlaystyleAnnotationCsv:
    """Test CSV annotation merge workflow."""

    def test_apply_annotations_creates_labeled_dataset(self, tmp_path):
        """Completed CSV rows should populate annotations[]."""
        dataset_path = tmp_path / "unlabeled.json"
        csv_path = tmp_path / "labels.csv"
        output_path = tmp_path / "labeled.json"
        report_path = tmp_path / "report.json"

        dataset_path.write_text(
            """
{
  "metadata": {"dataset_name": "test_unlabeled", "label_status": "unlabeled"},
  "sessions": [
    {
      "user_id": "u1",
      "session_id": "s1",
      "game_id": "minecraft",
      "annotations": [],
      "raw_events": [
        {"type": "inventory_change", "timestamp": 1000, "items": ["stone"]},
        {"type": "block_place", "timestamp": 7000, "position": {"x": 0, "y": 64, "z": 0}, "block_type": "minecraft:stone"}
      ]
    }
  ]
}
""",
            encoding="utf-8",
        )
        csv_path.write_text(
            "\n".join(
                [
                    "session_id,user_id,game_id,annotator_id,primary_playstyle,secondary_playstyles,confidence,evidence",
                    "s1,u1,minecraft,a1,planner,resource_diversifier,0.8,long prep",
                    "s1,u1,minecraft,a2,planner,,0.7,prep before build",
                    "s1,u1,minecraft,a3,route_optimizer,planner,0.6,direct path",
                ]
            ),
            encoding="utf-8",
        )

        summary = apply_annotations(dataset_path, csv_path, output_path)
        report = validate_playstyle_categories(output_path, report_path)

        assert output_path.exists()
        assert summary["annotated_sessions"] == 1
        assert summary["annotations"] == 3
        assert report["summary"]["labeled_sessions"] == 1
        assert report["summary"]["correct_predictions"] == 1
        assert report["summary"]["mean_pairwise_annotation_agreement"] == 0.3333
