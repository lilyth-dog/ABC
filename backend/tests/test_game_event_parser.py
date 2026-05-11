"""
Unit tests for game_event_parser.py.
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_event_parser import parse_game_events


class TestGameEventParser:
    """Test game event parser metric semantics."""

    def test_minecraft_planning_time_first_preparation_to_first_build(self):
        """Planning time spans from first preparation action to first build."""
        events = [
            {"type": "inventory_change", "timestamp": 1000, "items": ["stone"]},
            {"type": "inventory_change", "timestamp": 2000, "items": ["dirt"]},
            {"type": "block_place", "timestamp": 5000, "position": {"x": 0, "y": 64, "z": 0}},
        ]

        metrics = parse_game_events("minecraft", events)

        assert metrics["planning_time"] == 4000

    def test_minecraft_planning_time_uses_earliest_build_when_events_unsorted(self):
        """Planning time remains stable when raw events arrive out of order."""
        events = [
            {"type": "block_place", "timestamp": 7000, "position": {"x": 1, "y": 64, "z": 0}},
            {"type": "inventory_change", "timestamp": 1000, "items": ["stone"]},
            {"type": "block_place", "timestamp": 5000, "position": {"x": 0, "y": 64, "z": 0}},
            {"type": "item_craft", "timestamp": 3000, "item": "minecraft:planks"},
        ]

        metrics = parse_game_events("minecraft", events)

        assert metrics["planning_time"] == 4000
