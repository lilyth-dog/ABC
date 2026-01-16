"""
머신러닝 기반 성격 추론 모델
규칙 기반 시스템을 실제 머신러닝 모델로 교체
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
import json
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class MLPersonalityModel:
    """
    머신러닝 기반 성격 추론 모델
    행동 특징으로부터 4차원 성격 가중치를 예측
    """
    
    def __init__(self, model_type: str = "random_forest", use_pretrained: bool = True):
        """
        Args:
            model_type: 'random_forest' 또는 'ridge'
            use_pretrained: 사전 학습된 모델 사용 여부
        """
        self.model_type = model_type
        self.models = {}  # 각 성격 특성별 모델
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = os.path.join(os.path.dirname(__file__), "ml_models")
        os.makedirs(self.model_path, exist_ok=True)
        
        if use_pretrained and self._load_pretrained_models():
            self.is_trained = True
            logger.info("사전 학습된 모델을 로드했습니다.")
        else:
            # 초기 모델 생성 (규칙 기반으로 생성된 데이터로 학습)
            self._initialize_models()
    
    def _initialize_models(self):
        """초기 모델 생성 및 규칙 기반 데이터로 사전 학습"""
        if self.model_type == "random_forest":
            for trait in ["Logic", "Intuition", "Fluidity", "Complexity"]:
                self.models[trait] = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    n_jobs=-1
                )
        else:  # ridge
            for trait in ["Logic", "Intuition", "Fluidity", "Complexity"]:
                self.models[trait] = Ridge(alpha=1.0)
        
        # 규칙 기반으로 생성된 합성 데이터로 초기 학습
        self._pretrain_with_synthetic_data()
    
    def _pretrain_with_synthetic_data(self):
        """규칙 기반 공식을 사용하여 합성 학습 데이터 생성 및 학습"""
        # 다양한 시나리오 생성
        n_samples = 1000
        X = []
        y_logic = []
        y_intuition = []
        y_fluidity = []
        y_complexity = []
        
        for _ in range(n_samples):
            # 랜덤 특징 생성
            latency = np.random.uniform(500, 6000)  # ms
            revisions = np.random.randint(0, 10)
            efficiency = np.random.uniform(0.3, 1.0)
            intensity = np.random.uniform(0.5, 5.0)
            
            # 규칙 기반으로 타겟 생성 (ground truth로 사용)
            logic = min(max((latency - 1000) / 4000, 0.0), 1.0)
            intuition = 1.0 - logic
            fluidity = efficiency
            complexity = min((revisions * 0.2) + (latency / 10000), 1.0)
            
            X.append([latency, revisions, efficiency, intensity])
            y_logic.append(logic)
            y_intuition.append(intuition)
            y_fluidity.append(fluidity)
            y_complexity.append(complexity)
        
        X = np.array(X)
        X_scaled = self.scaler.fit_transform(X)
        
        # 각 특성별 모델 학습
        self.models["Logic"].fit(X_scaled, y_logic)
        self.models["Intuition"].fit(X_scaled, y_intuition)
        self.models["Fluidity"].fit(X_scaled, y_fluidity)
        self.models["Complexity"].fit(X_scaled, y_complexity)
        
        self.is_trained = True
        logger.info("합성 데이터로 모델을 사전 학습했습니다.")
    
    def predict(self, behavioral_features: Dict) -> Dict[str, float]:
        """
        행동 특징으로부터 성격 가중치 예측
        
        Args:
            behavioral_features: {
                'latency': float,      # 의사결정 지연시간 (ms)
                'revisions': int,      # 수정 횟수
                'efficiency': float,   # 경로 효율성 [0, 1]
                'intensity': float     # 상호작용 강도
            }
        
        Returns:
            {
                'Logic': float,
                'Intuition': float,
                'Fluidity': float,
                'Complexity': float
            }
        """
        if not self.is_trained:
            logger.warning("모델이 학습되지 않았습니다. 규칙 기반으로 대체합니다.")
            return self._rule_based_fallback(behavioral_features)
        
        # 특징 벡터 생성
        X = np.array([[
            behavioral_features.get('latency', 1000),
            behavioral_features.get('revisions', 0),
            behavioral_features.get('efficiency', 1.0),
            behavioral_features.get('intensity', 1.0)
        ]])
        
        X_scaled = self.scaler.transform(X)
        
        # 각 특성별 예측
        predictions = {}
        for trait in ["Logic", "Intuition", "Fluidity", "Complexity"]:
            pred = self.models[trait].predict(X_scaled)[0]
            # [0, 1] 범위로 클리핑
            predictions[trait] = max(0.0, min(1.0, pred))
        
        # Logic + Intuition = 1.0 제약 조건 적용
        total = predictions["Logic"] + predictions["Intuition"]
        if total > 0:
            predictions["Logic"] = predictions["Logic"] / total
            predictions["Intuition"] = predictions["Intuition"] / total
        
        return predictions
    
    def _rule_based_fallback(self, behavioral_features: Dict) -> Dict[str, float]:
        """규칙 기반 폴백 (모델이 학습되지 않은 경우)"""
        latency = behavioral_features.get('latency', 1000)
        revisions = behavioral_features.get('revisions', 0)
        efficiency = behavioral_features.get('efficiency', 1.0)
        
        logic = min(max((latency - 1000) / 4000, 0.0), 1.0)
        intuition = 1.0 - logic
        fluidity = efficiency
        complexity = min((revisions * 0.2) + (latency / 10000), 1.0)
        
        return {
            "Logic": logic,
            "Intuition": intuition,
            "Fluidity": fluidity,
            "Complexity": complexity
        }
    
    def update_with_real_data(self, X: np.ndarray, y: Dict[str, np.ndarray]):
        """
        실제 사용자 데이터로 모델 업데이트 (온라인 학습)
        
        Args:
            X: 특징 행렬 (n_samples, 4)
            y: 타겟 딕셔너리 {'Logic': array, 'Intuition': array, ...}
        """
        if X.shape[0] < 10:
            logger.warning("학습 데이터가 부족합니다 (최소 10개 필요).")
            return
        
        X_scaled = self.scaler.fit_transform(X)
        
        # 각 특성별 모델 재학습
        for trait in ["Logic", "Intuition", "Fluidity", "Complexity"]:
            if trait in y:
                self.models[trait].fit(X_scaled, y[trait])
        
        self.is_trained = True
        logger.info("실제 데이터로 모델을 업데이트했습니다.")
    
    def save_models(self, filepath: Optional[str] = None):
        """모델 저장"""
        if filepath is None:
            filepath = self.model_path
        
        os.makedirs(filepath, exist_ok=True)
        
        # 각 모델 저장
        for trait, model in self.models.items():
            model_file = os.path.join(filepath, f"{trait.lower()}_model.pkl")
            joblib.dump(model, model_file)
        
        # Scaler 저장
        scaler_file = os.path.join(filepath, "scaler.pkl")
        joblib.dump(self.scaler, scaler_file)
        
        logger.info(f"모델을 {filepath}에 저장했습니다.")
    
    def _load_pretrained_models(self) -> bool:
        """사전 학습된 모델 로드"""
        try:
            for trait in ["Logic", "Intuition", "Fluidity", "Complexity"]:
                model_file = os.path.join(self.model_path, f"{trait.lower()}_model.pkl")
                if not os.path.exists(model_file):
                    return False
                self.models[trait] = joblib.load(model_file)
            
            scaler_file = os.path.join(self.model_path, "scaler.pkl")
            if os.path.exists(scaler_file):
                self.scaler = joblib.load(scaler_file)
            
            return True
        except Exception as e:
            logger.error(f"모델 로드 실패: {e}")
            return False
    
    def get_feature_importance(self) -> Dict[str, Dict[str, float]]:
        """특징 중요도 반환 (Random Forest인 경우만)"""
        if self.model_type != "random_forest":
            return {}
        
        importance = {}
        feature_names = ['latency', 'revisions', 'efficiency', 'intensity']
        
        for trait, model in self.models.items():
            if hasattr(model, 'feature_importances_'):
                importance[trait] = {
                    feature_names[i]: float(imp)
                    for i, imp in enumerate(model.feature_importances_)
                }
        
        return importance
