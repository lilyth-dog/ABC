"""
예측 모델링 모듈
사용자의 행동 패턴을 기반으로 미래 행동 및 상태를 예측

기능:
- 행동 패턴 예측
- 스트레스/피로 감지
- 성격 변화 예측
- 이상 행동 감지
"""
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from logger_config import logger


class PredictiveModel:
    """
    행동 패턴 예측 모델
    과거 세션 데이터를 기반으로 미래 행동을 예측
    """
    
    def __init__(self, lookback_window: int = 10):
        """
        Args:
            lookback_window: 예측에 사용할 과거 세션 수
        """
        self.lookback_window = lookback_window
    
    def predict_behavioral_trend(
        self, 
        history: List[Dict]
    ) -> Dict:
        """
        행동 트렌드 예측
        
        Args:
            history: 과거 세션 데이터 리스트
        
        Returns:
            예측 결과 딕셔너리
        """
        if len(history) < 3:
            return {
                "status": "insufficient_data",
                "message": "최소 3개 세션이 필요합니다",
                "sessions_needed": 3 - len(history)
            }
        
        # 최근 세션만 사용
        recent = history[-self.lookback_window:]
        
        # 가중치 추출
        weights_history = []
        for session in recent:
            if 'logic_weight' in session:
                weights_history.append({
                    'logic': session.get('logic_weight', 0.5),
                    'intuition': session.get('intuition_weight', 0.5),
                    'fluidity': session.get('fluidity_weight', 0.5),
                    'complexity': session.get('complexity_weight', 0.5)
                })
        
        if len(weights_history) < 2:
            return {"status": "insufficient_data"}
        
        # 선형 회귀로 트렌드 예측
        trends = {}
        for trait in ['logic', 'intuition', 'fluidity', 'complexity']:
            values = [w[trait] for w in weights_history]
            x = np.arange(len(values))
            
            # 선형 피팅
            coeffs = np.polyfit(x, values, 1)
            trend_slope = coeffs[0]
            
            # 다음 세션 예측값
            next_value = np.polyval(coeffs, len(values))
            next_value = np.clip(next_value, 0.0, 1.0)
            
            trends[trait] = {
                "current": values[-1],
                "predicted": float(next_value),
                "trend": "increasing" if trend_slope > 0.01 else "decreasing" if trend_slope < -0.01 else "stable",
                "slope": float(trend_slope),
                "confidence": min(len(weights_history) / 10, 1.0)
            }
        
        return {
            "status": "predicted",
            "trends": trends,
            "next_session_prediction": {
                trait: trends[trait]["predicted"] for trait in trends
            }
        }
    
    def detect_stress_pattern(
        self,
        history: List[Dict[str, Any]],
        current_session: Dict[str, Any]
    ) -> Dict:
        """
        스트레스/피로 패턴 감지
        
        Args:
            history: 과거 세션 데이터
            current_session: 현재 세션 데이터
        
        Returns:
            스트레스 감지 결과
        """
        if len(history) < 1:
            return {"status": "insufficient_data"}
        
        # 최근 3개 세션과 비교
        recent = history[-3:] if len(history) >= 3 else history
        
        # 평균 의사결정 지연시간 계산
        avg_latencies = []
        revision_history = []
        efficiency_history = []
        for session in recent:
            metrics = self._extract_session_metrics(session)
            latency = metrics.get("avg_decision_latency")
            if latency is not None and latency > 0:
                avg_latencies.append(latency)
            if "revision_rate" in metrics:
                revision_history.append(metrics["revision_rate"])
            if "path_efficiency" in metrics:
                efficiency_history.append(metrics["path_efficiency"])
        
        if len(avg_latencies) < 1 and not revision_history and not efficiency_history:
            return {"status": "insufficient_data"}
        
        # 현재 세션의 지연시간
        current_metrics = self._extract_session_metrics(current_session)
        current_latency = current_metrics.get("avg_decision_latency", 0)
        
        # 평균과 비교
        baseline_latency = np.mean(avg_latencies)
        if baseline_latency > 0 and current_latency > 0:
            latency_increase = (current_latency - baseline_latency) / baseline_latency
        else:
            latency_increase = 0
        
        # 스트레스 지표
        stress_level = 0.0
        stress_indicators = []
        
        if latency_increase > 0.3:  # 30% 이상 증가
            stress_level += 0.4
            stress_indicators.append("의사결정 지연시간 증가")
        
        # 수정 빈도 증가도 스트레스 지표
        if "revision_rate" in current_metrics and revision_history:
            avg_revisions = np.mean(revision_history)
            if current_metrics["revision_rate"] > avg_revisions * 1.5:
                stress_level += 0.3
                stress_indicators.append("수정 빈도 증가")
        
        # 경로 효율성 감소
        if "path_efficiency" in current_metrics and efficiency_history:
            avg_efficiency = np.mean(efficiency_history)
            if current_metrics["path_efficiency"] < avg_efficiency * 0.8:
                stress_level += 0.3
                stress_indicators.append("경로 효율성 감소")
        
        stress_level = min(stress_level, 1.0)
        
        return {
            "status": "analyzed",
            "stress_level": round(stress_level, 2),
            "stress_category": self._categorize_stress(stress_level),
            "indicators": stress_indicators,
            "latency_change": round(latency_increase * 100, 1),  # 퍼센트
            "recommendation": self._get_stress_recommendation(stress_level)
        }

    def _extract_session_metrics(self, session: Dict[str, Any]) -> Dict[str, float]:
        """
        세션 데이터에서 스트레스 분석용 메트릭을 추출합니다.

        Args:
            session: raw_metrics 또는 평탄 키를 포함할 수 있는 세션 데이터

        Returns:
            avg_decision_latency, revision_rate, path_efficiency 키를 포함한 딕셔너리
        """
        metrics: Dict[str, float] = {}

        raw_metrics = session.get("raw_metrics")
        if raw_metrics:
            try:
                parsed = json.loads(raw_metrics) if isinstance(raw_metrics, str) else raw_metrics
                summary = parsed.get("summary", {})
                if "avgDecisionLatency" in summary:
                    metrics["avg_decision_latency"] = float(summary.get("avgDecisionLatency", 0) or 0)
                if "revisionRate" in summary:
                    metrics["revision_rate"] = float(summary.get("revisionRate", 0) or 0)
                if "pathEfficiency" in summary:
                    metrics["path_efficiency"] = float(summary.get("pathEfficiency", 0) or 0)
            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                logger.warning("Failed to parse raw_metrics for stress detection: %s", exc)

        fallback_keys = {
            "avg_decision_latency": ["avg_decision_latency", "avgDecisionLatency"],
            "revision_rate": ["revision_rate", "revisionRate"],
            "path_efficiency": ["path_efficiency", "pathEfficiency"],
        }

        for target_key, candidates in fallback_keys.items():
            if target_key in metrics:
                continue
            for candidate in candidates:
                if candidate in session:
                    try:
                        metrics[target_key] = float(session.get(candidate, 0) or 0)
                    except (TypeError, ValueError) as exc:
                        logger.warning("Invalid %s for stress detection: %s", candidate, exc)
                    break

        return metrics
    
    def _categorize_stress(self, level: float) -> str:
        """
        스트레스 레벨을 카테고리로 분류합니다.
        
        Args:
            level (float): 스트레스 레벨 (0.0 ~ 1.0)
        
        Returns:
            str: "low", "moderate", 또는 "high"
        """
        if level < 0.3:
            return "low"
        elif level < 0.6:
            return "moderate"
        else:
            return "high"
    
    def _get_stress_recommendation(self, level: float) -> str:
        """
        스트레스 레벨에 따른 사용자 권장사항을 반환합니다.
        
        Args:
            level (float): 스트레스 레벨 (0.0 ~ 1.0)
        
        Returns:
            str: 권장사항 메시지
        """
        if level < 0.3:
            return "정상적인 패턴입니다. 계속 진행하세요."
        elif level < 0.6:
            return "약간의 변화가 감지되었습니다. 휴식을 고려해보세요."
        else:
            return "스트레스 지표가 높습니다. 충분한 휴식이 필요합니다."
    
    def predict_personality_evolution(
        self,
        history: List[Dict],
        forecast_days: int = 30
    ) -> Dict:
        """
        성격 진화 예측
        
        Args:
            history: 과거 프로필 진화 데이터
            forecast_days: 예측할 일수
        
        Returns:
            미래 성격 가중치 예측
        """
        if len(history) < 5:
            return {
                "status": "insufficient_data",
                "sessions_needed": 5 - len(history)
            }
        
        # 시간 시계열 생성
        timestamps = []
        weights_series = {trait: [] for trait in ['logic', 'intuition', 'fluidity', 'complexity']}
        
        for session in history:
            if 'timestamp' in session:
                timestamps.append(session['timestamp'])
                for trait in weights_series:
                    key = f"{trait}_weight"
                    weights_series[trait].append(session.get(key, 0.5))
        
        if len(timestamps) < 5:
            return {"status": "insufficient_data"}
        
        # 선형 외삽으로 미래 예측
        predictions = {}
        days_from_start = [(datetime.fromisoformat(ts.replace('Z', '+00:00')) - datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))).days for ts in timestamps]
        
        for trait in weights_series:
            values = weights_series[trait]
            x = np.array(days_from_start)
            y = np.array(values)
            
            # 선형 피팅
            coeffs = np.polyfit(x, y, 1)
            
            # 미래 예측
            future_day = days_from_start[-1] + forecast_days
            predicted_value = np.polyval(coeffs, future_day)
            predicted_value = np.clip(predicted_value, 0.0, 1.0)
            
            predictions[trait] = {
                "current": float(values[-1]),
                "predicted_30days": float(predicted_value),
                "change": float(predicted_value - values[-1]),
                "trend": "increasing" if coeffs[0] > 0 else "decreasing" if coeffs[0] < 0 else "stable"
            }
        
        return {
            "status": "predicted",
            "forecast_days": forecast_days,
            "predictions": predictions,
            "confidence": min(len(history) / 20, 1.0)
        }
    
    def detect_anomaly(
        self,
        history: List[Dict],
        current_session: Dict
    ) -> Dict:
        """
        이상 행동 감지
        
        Args:
            history: 과거 세션 데이터
            current_session: 현재 세션 데이터
        
        Returns:
            이상 감지 결과
        """
        if len(history) < 3:
            return {"status": "insufficient_data"}
        
        # 통계적 이상치 감지 (Z-score 기반)
        recent = history[-10:] if len(history) >= 10 else history
        
        anomalies = []
        anomaly_score = 0.0
        
        # 의사결정 지연시간 이상치
        latencies = []
        for s in recent:
            if 'avg_decision_latency' in s and s['avg_decision_latency']:
                latencies.append(s['avg_decision_latency'])
        
        if latencies and 'avg_decision_latency' in current_session:
            mean_latency = np.mean(latencies)
            std_latency = np.std(latencies) if len(latencies) > 1 else mean_latency * 0.2
            
            if std_latency > 0:
                z_score = abs(current_session['avg_decision_latency'] - mean_latency) / std_latency
                if z_score > 2.5:  # 2.5 표준편차 이상
                    anomalies.append({
                        "type": "decision_latency",
                        "severity": "high" if z_score > 3.5 else "medium",
                        "z_score": round(z_score, 2),
                        "description": f"의사결정 지연시간이 평균보다 {z_score:.1f} 표준편차 이상 벗어남"
                    })
                    anomaly_score += 0.3
        
        # 수정 빈도 이상치
        revisions = [s.get('revision_rate', 0) for s in recent]
        if revisions and 'revision_rate' in current_session:
            mean_rev = np.mean(revisions)
            std_rev = np.std(revisions) if len(revisions) > 1 else mean_rev * 0.3
            
            if std_rev > 0:
                z_score = abs(current_session['revision_rate'] - mean_rev) / std_rev
                if z_score > 2.5:
                    anomalies.append({
                        "type": "revision_rate",
                        "severity": "high" if z_score > 3.5 else "medium",
                        "z_score": round(z_score, 2),
                        "description": f"수정 빈도가 평균보다 {z_score:.1f} 표준편차 이상 벗어남"
                    })
                    anomaly_score += 0.3
        
        # 경로 효율성 이상치
        efficiencies = [s.get('path_efficiency', 1.0) for s in recent]
        if efficiencies and 'path_efficiency' in current_session:
            mean_eff = np.mean(efficiencies)
            std_eff = np.std(efficiencies) if len(efficiencies) > 1 else mean_eff * 0.2
            
            if std_eff > 0:
                z_score = abs(current_session['path_efficiency'] - mean_eff) / std_eff
                if z_score > 2.5:
                    anomalies.append({
                        "type": "path_efficiency",
                        "severity": "high" if z_score > 3.5 else "medium",
                        "z_score": round(z_score, 2),
                        "description": f"경로 효율성이 평균보다 {z_score:.1f} 표준편차 이상 벗어남"
                    })
                    anomaly_score += 0.4
        
        anomaly_score = min(anomaly_score, 1.0)
        
        return {
            "status": "analyzed",
            "has_anomaly": len(anomalies) > 0,
            "anomaly_score": round(anomaly_score, 2),
            "anomalies": anomalies,
            "recommendation": "정상적인 패턴입니다." if len(anomalies) == 0 else "이상 행동 패턴이 감지되었습니다. 확인이 필요합니다."
        }


# 전역 인스턴스
_predictive_model: Optional[PredictiveModel] = None


def get_predictive_model() -> PredictiveModel:
    """예측 모델 인스턴스 가져오기"""
    global _predictive_model
    if _predictive_model is None:
        _predictive_model = PredictiveModel()
    return _predictive_model
