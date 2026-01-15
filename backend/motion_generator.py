"""
Emotional 3D Motion Generator for Digital Human Twin
Maps emotional behavioral profiles to 3D kinematic modifiers.
"""
import math
import random
from typing import Dict, List, Tuple


class EmotionalMotionGenerator:
    """
    Generates 3D kinematic modifications based on emotional profiles.
    Used to bridge the gap between emotional data (TESS) and 3D character behavior.
    """
    
    def __init__(self):
        # Default kinematic state
        self.base_posture = {
            "head_pitch": 0.0,
            "shoulder_width": 1.0,
            "spine_curve": 0.0,
            "hand_tremor": 0.0
        }

    def generate_modifiers(self, profile: Dict) -> Dict:
        """
        Maps a behavioral profile (from TESS or interaction) to kinematic modifiers.
        """
        valence = profile.get("emotionalContext", {}).get("valence", 0.0)
        arousal = profile.get("emotionalContext", {}).get("arousal", 0.0)
        intensity = profile.get("intensity", 0.5)
        
        # 1. Posture Modifiers
        # Negative valence (sad/fear) -> head down (pitch > 0), slumped spine
        # Positive valence (happy/surprise) -> head up (pitch < 0)
        head_pitch = -valence * 0.4  # radians
        spine_curve = max(0, -valence * 0.3)
        
        # 2. Dynamics Modifiers
        # High arousal (angry/fear) -> high tremor, high speed
        # Low arousal (sad) -> low speed, high latency
        hand_tremor = max(0, arousal * 0.05 * intensity)
        movement_speed_multiplier = 1.0 + (arousal * 0.5) # Fast or slow
        
        # 3. Synchrony (Kuramoto parameters)
        # Higher valence/lower arousal -> more coherent movement (stable theta)
        # Low valence/high arousal -> chaotic movement (high beta)
        target_coherence = 0.5 + (valence * 0.4) - (abs(arousal) * 0.1)
        
        return {
            "kinematics": {
                "headPitch": head_pitch,
                "spineSlump": spine_curve,
                "handTremor": hand_tremor,
                "speedMultiplier": movement_speed_multiplier
            },
            "neural_targets": {
                "targetCoherence": max(0.1, min(0.9, target_coherence)),
                "estimatedTheta": 0.5 + (valence * 0.3),
                "estimatedBeta": 0.5 + (abs(arousal) * 0.4)
            },
            "interpretation": self._get_interpretation(valence, arousal)
        }

    def _get_interpretation(self, valence: float, arousal: float) -> str:
        if valence > 0.5:
            return "Positive/Energetic" if arousal > 0 else "Positive/Calm"
        elif valence < -0.5:
            return "Negative/Agitated" if arousal > 0 else "Negative/Withdrawn"
        return "Neutral"


if __name__ == "__main__":
    generator = EmotionalMotionGenerator()
    
    # Test with Happy profile
    happy_profile = {
        "intensity": 0.8,
        "emotionalContext": {"valence": 0.9, "arousal": 0.6}
    }
    print("Happy Profile Modifiers:", generator.generate_modifiers(happy_profile))
    
    # Test with Sad profile
    sad_profile = {
        "intensity": 0.4,
        "emotionalContext": {"valence": -0.8, "arousal": -0.3}
    }
    print("\nSad Profile Modifiers:", generator.generate_modifiers(sad_profile))
