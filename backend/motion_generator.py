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
        행동 프로필(TESS 또는 상호작용)을 운동학적 수정자로 매핑합니다.
        
        Args:
            profile (Dict): 행동 프로필 딕셔너리
                - emotionalContext (Dict): 감정 컨텍스트
                    - valence (float): 감정 가치 (-1.0 ~ 1.0)
                    - arousal (float): 각성도 (-1.0 ~ 1.0)
                - intensity (float): 상호작용 강도 (0.0 ~ 1.0)
        
        Returns:
            Dict: 운동학적 수정자 및 신경 타겟
                - kinematics (Dict): 3D 운동학 파라미터
                - neural_targets (Dict): 신경 신호 타겟 값
                - interpretation (str): 감정 해석
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
        """
        감정 가치와 각성도로부터 감정 해석 문자열을 생성합니다.
        
        Args:
            valence (float): 감정 가치 (-1.0 ~ 1.0)
            arousal (float): 각성도 (-1.0 ~ 1.0)
        
        Returns:
            str: 감정 해석 문자열
                - "Positive/Energetic": 높은 가치, 높은 각성
                - "Positive/Calm": 높은 가치, 낮은 각성
                - "Negative/Agitated": 낮은 가치, 높은 각성
                - "Negative/Withdrawn": 낮은 가치, 낮은 각성
                - "Neutral": 중간 범위
        """
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
