"""
예측 모델 단위 테스트
"""
import pytest
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from predictive_model import PredictiveModel


class TestPredictiveModel:
    """PredictiveModel 클래스 테스트"""
    
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.model = PredictiveModel(lookback_window=10)
    
    def test_predict_behavioral_trend_insufficient_data(self):
        """데이터가 부족한 경우 테스트"""
        history = [
            {"logic_weight": 0.5, "intuition_weight": 0.5}
        ]
        result = self.model.predict_behavioral_trend(history)
        assert result["status"] == "insufficient_data"
        assert "sessions_needed" in result
    
    def test_predict_behavioral_trend_sufficient_data(self):
        """충분한 데이터가 있는 경우 테스트"""
        history = [
            {"logic_weight": 0.5, "intuition_weight": 0.5, "fluidity_weight": 0.5, "complexity_weight": 0.5},
            {"logic_weight": 0.52, "intuition_weight": 0.48, "fluidity_weight": 0.51, "complexity_weight": 0.49},
            {"logic_weight": 0.54, "intuition_weight": 0.46, "fluidity_weight": 0.52, "complexity_weight": 0.50},
        ]
        result = self.model.predict_behavioral_trend(history)
        assert result["status"] == "predicted"
        assert "trends" in result
        assert "logic" in result["trends"]
        assert result["trends"]["logic"]["trend"] in ["increasing", "decreasing", "stable"]
    
    def test_detect_stress_pattern_low_stress(self):
        """낮은 스트레스 감지 테스트"""
        history = [
            {"avg_decision_latency": 1000, "revision_rate": 1, "path_efficiency": 0.9}
        ]
        current = {
            "avg_decision_latency": 1100,
            "revision_rate": 1,
            "path_efficiency": 0.9
        }
        result = self.model.detect_stress_pattern(history, current)
        assert result["status"] == "analyzed"
        assert result["stress_level"] < 0.3
    
    def test_detect_stress_pattern_high_stress(self):
        """높은 스트레스 감지 테스트"""
        history = [
            {"avg_decision_latency": 1000, "revision_rate": 1, "path_efficiency": 0.9}
        ]
        current = {
            "avg_decision_latency": 2000,  # 2배 증가
            "revision_rate": 5,  # 5배 증가
            "path_efficiency": 0.5  # 50% 감소
        }
        result = self.model.detect_stress_pattern(history, current)
        assert result["status"] == "analyzed"
        assert result["stress_level"] > 0.6
        assert len(result["indicators"]) > 0
    
    def test_detect_anomaly_normal(self):
        """정상 패턴 테스트"""
        history = [
            {"avg_decision_latency": 1000, "revision_rate": 2, "path_efficiency": 0.9},
            {"avg_decision_latency": 1100, "revision_rate": 2, "path_efficiency": 0.88},
            {"avg_decision_latency": 1050, "revision_rate": 3, "path_efficiency": 0.91},
        ]
        current = {
            "avg_decision_latency": 1080,
            "revision_rate": 2,
            "path_efficiency": 0.89
        }
        result = self.model.detect_anomaly(history, current)
        assert result["status"] == "analyzed"
        assert result["has_anomaly"] == False
    
    def test_detect_anomaly_abnormal(self):
        """이상 패턴 테스트"""
        history = [
            {"avg_decision_latency": 1000, "revision_rate": 2, "path_efficiency": 0.9},
            {"avg_decision_latency": 1100, "revision_rate": 2, "path_efficiency": 0.88},
            {"avg_decision_latency": 1050, "revision_rate": 3, "path_efficiency": 0.91},
        ]
        current = {
            "avg_decision_latency": 5000,  # 5배 이상 증가
            "revision_rate": 20,  # 10배 증가
            "path_efficiency": 0.3  # 70% 감소
        }
        result = self.model.detect_anomaly(history, current)
        assert result["status"] == "analyzed"
        assert result["has_anomaly"] == True
        assert len(result["anomalies"]) > 0
    
    def test_predict_personality_evolution_insufficient_data(self):
        """데이터 부족 시 진화 예측 테스트"""
        history = [
            {"logic_weight": 0.5, "intuition_weight": 0.5, "fluidity_weight": 0.5, "complexity_weight": 0.5, "timestamp": "2026-01-01T00:00:00Z"}
        ]
        result = self.model.predict_personality_evolution(history, forecast_days=30)
        assert result["status"] == "insufficient_data"
    
    def test_predict_personality_evolution_sufficient_data(self):
        """충분한 데이터로 진화 예측 테스트"""
        from datetime import datetime, timedelta
        base_time = datetime.now()
        history = []
        for i in range(10):
            history.append({
                "logic_weight": 0.5 + i * 0.01,
                "intuition_weight": 0.5 - i * 0.01,
                "fluidity_weight": 0.5 + i * 0.005,
                "complexity_weight": 0.5 + i * 0.002,
                "timestamp": (base_time + timedelta(days=i)).isoformat()
            })
        
        result = self.model.predict_personality_evolution(history, forecast_days=30)
        assert result["status"] == "predicted"
        assert "predictions" in result
        assert "logic" in result["predictions"]
        assert "predicted_30days" in result["predictions"]["logic"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
