"""
게임 행동 데이터 처리 모듈
마인크래프트, 스타듀밸리, 두근두근타운 등에서 수집한 데이터를 처리
"""
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class GameBehavioralData(BaseModel):
    """게임에서 수집한 행동 데이터"""
    game_id: str = Field(..., description="게임 ID (minecraft, stardew_valley, animal_crossing)")
    session_id: str = Field(..., description="세션 ID")
    
    # 공통 메트릭
    decision_latency: float = Field(0, ge=0, description="의사결정 지연시간 (ms)")
    planning_time: float = Field(0, ge=0, description="계획 시간 (ms)")
    revision_count: int = Field(0, ge=0, description="수정 빈도")
    
    # Fluidity 메트릭
    path_efficiency: float = Field(0.5, ge=0, le=1, description="경로 효율성 [0, 1]")
    task_efficiency: float = Field(0.5, ge=0, le=1, description="작업 효율성 [0, 1]")
    
    # Complexity 메트릭
    complexity: float = Field(0.5, ge=0, le=1, description="복잡도 [0, 1]")
    diversity: float = Field(0.5, ge=0, le=1, description="다양성 [0, 1]")
    
    # 게임별 특화 메트릭
    game_specific_metrics: Dict = Field(default_factory=dict, description="게임별 특화 메트릭")


class GameBehaviorProcessor:
    """게임 행동 데이터를 표준 행동 프로필로 변환"""
    
    # 게임별 가중치 (게임 특성에 따라 조정)
    GAME_WEIGHTS = {
        "minecraft": {
            "planning_time_weight": 0.4,
            "revision_weight": 0.3,
            "complexity_weight": 0.3,
        },
        "stardew_valley": {
            "planning_time_weight": 0.35,
            "revision_weight": 0.25,
            "complexity_weight": 0.4,
        },
        "animal_crossing": {
            "planning_time_weight": 0.3,
            "revision_weight": 0.4,
            "complexity_weight": 0.3,
        }
    }
    
    def __init__(self):
        self.default_weights = {
            "planning_time_weight": 0.35,
            "revision_weight": 0.3,
            "complexity_weight": 0.35,
        }
    
    def process(self, game_data: GameBehavioralData) -> Dict:
        """
        게임 행동 데이터를 표준 행동 프로필로 변환
        
        Args:
            game_data: 게임에서 수집한 행동 데이터
            
        Returns:
            표준 행동 프로필 딕셔너리
        """
        weights = self.GAME_WEIGHTS.get(
            game_data.game_id, 
            self.default_weights
        )
        
        # Logic vs Intuition 계산
        logic_score = self._calculate_logic_score(game_data, weights)
        intuition_score = 1.0 - logic_score
        
        # Fluidity 계산
        fluidity_score = self._calculate_fluidity_score(game_data)
        
        # Complexity 계산
        complexity_score = self._calculate_complexity_score(game_data, weights)
        
        # 게임별 특화 메트릭 처리
        game_specific = self._process_game_specific_metrics(
            game_data.game_id,
            game_data.game_specific_metrics
        )
        
        return {
            "pathEfficiency": fluidity_score,
            "avgDecisionLatency": game_data.decision_latency,
            "revisionRate": game_data.revision_count,
            "jitterIndex": 1.0 - fluidity_score,  # Fluidity의 역
            "intensity": complexity_score * 2.0,  # Complexity 기반
            "gameId": game_data.game_id,
            "gameSpecific": game_specific
        }
    
    def _calculate_logic_score(
        self, 
        game_data: GameBehavioralData, 
        weights: Dict
    ) -> float:
        """Logic 점수 계산"""
        # 계획 시간 (정규화: 0-5분 = 0-1)
        planning_normalized = min(1.0, game_data.planning_time / 300000)
        
        # 수정 빈도 (정규화: 0-10회 = 0-1)
        revision_normalized = min(1.0, game_data.revision_count / 10)
        
        # 위험 회피 (게임별 메트릭에서 추출)
        risk_aversion = 1.0 - game_data.game_specific_metrics.get(
            "riskTaking", 0.5
        )
        
        logic_score = (
            planning_normalized * weights["planning_time_weight"] +
            revision_normalized * weights["revision_weight"] +
            risk_aversion * (1 - weights["planning_time_weight"] - weights["revision_weight"])
        )
        
        return min(1.0, max(0.0, logic_score))
    
    def _calculate_fluidity_score(self, game_data: GameBehavioralData) -> float:
        """Fluidity 점수 계산"""
        return (
            game_data.path_efficiency * 0.4 +
            game_data.task_efficiency * 0.3 +
            game_data.game_specific_metrics.get("movementSmoothness", 0.5) * 0.3
        )
    
    def _calculate_complexity_score(
        self,
        game_data: GameBehavioralData,
        weights: Dict
    ) -> float:
        """Complexity 점수 계산"""
        complexity_base = game_data.complexity
        diversity = game_data.diversity
        revision_normalized = min(1.0, game_data.revision_count / 10)
        
        complexity_score = (
            complexity_base * weights["complexity_weight"] +
            diversity * (1 - weights["complexity_weight"]) * 0.5 +
            revision_normalized * (1 - weights["complexity_weight"]) * 0.5
        )
        
        return min(1.0, max(0.0, complexity_score))
    
    def _process_game_specific_metrics(
        self,
        game_id: str,
        metrics: Dict
    ) -> Dict:
        """게임별 특화 메트릭 처리"""
        if game_id == "minecraft":
            return {
                "buildComplexity": metrics.get("buildComplexity", 0.5),
                "explorationRange": metrics.get("explorationRange", 0.5),
                "resourceDiversity": metrics.get("resourceDiversity", 0.5),
            }
        elif game_id == "stardew_valley":
            return {
                "cropDiversity": metrics.get("cropDiversity", 0.5),
                "farmOptimization": metrics.get("farmOptimization", 0.5),
                "relationshipDepth": metrics.get("relationshipDepth", 0.5),
            }
        elif game_id == "animal_crossing":
            return {
                "islandComplexity": metrics.get("islandComplexity", 0.5),
                "npcInteractionDepth": metrics.get("npcInteractionDepth", 0.5),
                "designConsistency": metrics.get("designConsistency", 0.5),
            }
        else:
            return {}


def convert_game_to_behavioral_profile(game_data: Dict) -> Dict:
    """
    게임 데이터를 표준 행동 프로필로 변환 (편의 함수)
    
    Args:
        game_data: 게임에서 수집한 원시 데이터
        
    Returns:
        표준 행동 프로필
    """
    processor = GameBehaviorProcessor()
    
    try:
        game_behavior = GameBehavioralData(**game_data)
        return processor.process(game_behavior)
    except Exception as e:
        logger.error(f"게임 데이터 변환 실패: {e}")
        raise
