"""
오프라인 시연 - 백엔드 서버 없이 직접 함수 호출
실제 시스템 로직을 실행하여 결과 보여주기
"""
import sys
from pathlib import Path

# 백엔드 모듈 경로 추가
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from neuro_controller import BehavioralPersonalityDecoder, ContinuousLearner
from predictive_model import PredictiveModel
import json

def demo_personality_inference():
    """성격 추론 시연"""
    print("=" * 60)
    print("시연 1: 행동 프로필 → 성격 가중치 추론")
    print("=" * 60)
    
    # 샘플 행동 프로필
    behavioral_profile = {
        "pathEfficiency": 0.75,
        "avgDecisionLatency": 3500,  # 3.5초 - 분석적 사고
        "revisionRate": 4,  # 여러 번 수정 - 신중함
        "jitterIndex": 0.12,
        "intensity": 2.3,
        "maturityLevel": 1
    }
    
    print("\n입력: 행동 프로필")
    print(f"  - 의사결정 지연시간: {behavioral_profile['avgDecisionLatency']}ms")
    print(f"  - 경로 효율성: {behavioral_profile['pathEfficiency']:.2f}")
    print(f"  - 수정 빈도: {behavioral_profile['revisionRate']}회")
    
    # 성격 추론 실행
    decoder = BehavioralPersonalityDecoder(cultural_context="default", use_ml=True)
    result = decoder.decode(behavioral_profile)
    
    print("\n✓ 성격 추론 완료!")
    print("\n출력: 성격 가중치")
    weights = result.get("traits", {}).get("weights", {})
    print(f"  - Logic: {weights.get('Logic', 0):.2f} ({weights.get('Logic', 0)*100:.0f}%)")
    print(f"  - Intuition: {weights.get('Intuition', 0):.2f} ({weights.get('Intuition', 0)*100:.0f}%)")
    print(f"  - Fluidity: {weights.get('Fluidity', 0):.2f} ({weights.get('Fluidity', 0)*100:.0f}%)")
    print(f"  - Complexity: {weights.get('Complexity', 0):.2f} ({weights.get('Complexity', 0)*100:.0f}%)")
    
    evidence = result.get("traits", {}).get("evidence", {})
    print(f"\n추론 근거:")
    print(f"  - {evidence.get('reasoning', 'N/A')}")
    print(f"  - ML 모델 사용: {evidence.get('ml_model_used', False)}")
    print(f"  - 모델 타입: {evidence.get('model_type', 'N/A')}")
    
    return result

def demo_continuous_learning():
    """지속적 학습 시연"""
    print("\n" + "=" * 60)
    print("시연 2: 지속적 학습 (EMA 업데이트)")
    print("=" * 60)
    
    learner = ContinuousLearner(learning_rate=0.3)
    
    # 세션 1
    print("\n세션 1:")
    current_weights = {"Logic": 0.45, "Intuition": 0.55, "Fluidity": 0.68, "Complexity": 0.52}
    new_weights = {"Logic": 0.52, "Intuition": 0.48, "Fluidity": 0.72, "Complexity": 0.58}
    
    print(f"  현재: Logic={current_weights['Logic']:.2f}")
    print(f"  새로운: Logic={new_weights['Logic']:.2f}")
    
    updated = learner.update_weights(current_weights, new_weights)
    print(f"  → 업데이트 후: Logic={updated['Logic']:.2f}")
    
    # 세션 2
    print("\n세션 2:")
    current_weights = updated
    new_weights = {"Logic": 0.58, "Intuition": 0.42, "Fluidity": 0.75, "Complexity": 0.62}
    
    print(f"  현재: Logic={current_weights['Logic']:.2f}")
    print(f"  새로운: Logic={new_weights['Logic']:.2f}")
    
    updated = learner.update_weights(current_weights, new_weights)
    print(f"  → 업데이트 후: Logic={updated['Logic']:.2f}")
    
    # 신뢰도 계산
    confidence = learner.compute_confidence(3, 0.7)
    print(f"\n세션 3개 후 신뢰도: {confidence:.2%}")
    
    # 아키타입 생성
    archetype = learner.generate_archetype(updated)
    print(f"아키타입: {archetype}")
    
    return updated

def demo_predictive_analysis():
    """예측 분석 시연"""
    print("\n" + "=" * 60)
    print("시연 3: 예측 분석 (스트레스, 이상 감지, 트렌드)")
    print("=" * 60)
    
    predictive_model = PredictiveModel()
    
    # 샘플 세션 히스토리
    sessions = [
        {"avg_decision_latency": 2500, "revision_rate": 2, "path_efficiency": 0.68},
        {"avg_decision_latency": 3200, "revision_rate": 3, "path_efficiency": 0.72},
        {"avg_decision_latency": 3800, "revision_rate": 4, "path_efficiency": 0.75},
        {"avg_decision_latency": 4200, "revision_rate": 5, "path_efficiency": 0.78},
    ]
    
    current_session = {
        "avg_decision_latency": 4500,
        "revision_rate": 6,
        "path_efficiency": 0.80
    }
    
    print("\n세션 히스토리:")
    for i, s in enumerate(sessions, 1):
        print(f"  세션 {i}: Latency={s['avg_decision_latency']}ms, "
              f"Efficiency={s['path_efficiency']:.2f}")
    
    # 스트레스 패턴 감지
    print("\n1. 스트레스 패턴 감지:")
    stress = predictive_model.detect_stress_pattern(sessions, current_session)
    print(f"  - 스트레스 레벨: {stress.get('stress_level', 0):.2f}")
    print(f"  - 카테고리: {stress.get('stress_category', 'N/A')}")
    if 'indicators' in stress:
        for indicator in stress['indicators']:
            print(f"  - {indicator}")
    
    # 이상 감지
    print("\n2. 이상 감지:")
    anomaly = predictive_model.detect_anomaly(sessions, current_session)
    print(f"  - 이상 발견: {anomaly.get('has_anomaly', False)}")
    print(f"  - 이상 점수: {anomaly.get('anomaly_score', 0):.2f}")
    if anomaly.get('anomalies'):
        for a in anomaly['anomalies']:
            print(f"  - {a.get('type', 'N/A')}: {a.get('description', 'N/A')}")
    
    # 행동 트렌드 예측
    print("\n3. 행동 트렌드 예측:")
    trend = predictive_model.predict_behavioral_trend(sessions + [current_session])
    if 'trends' in trend:
        for trait, data in trend['trends'].items():
            print(f"  - {trait}: {data.get('trend', 'N/A')} "
                  f"(현재: {data.get('current', 0):.2f}, "
                  f"예측: {data.get('predicted', 0):.2f})")
    
    return {"stress": stress, "anomaly": anomaly, "trend": trend}

def demo_ml_model():
    """ML 모델 시연"""
    print("\n" + "=" * 60)
    print("시연 4: 머신러닝 모델 (랜덤 포레스트)")
    print("=" * 60)
    
    try:
        from ml_personality_model import MLPersonalityModel
        
        model = MLPersonalityModel(model_type="random_forest", use_pretrained=True)
        
        print("\n✓ ML 모델 로드 완료")
        print(f"  - 모델 타입: Random Forest")
        print(f"  - 학습 상태: {'학습됨' if model.is_trained else '미학습'}")
        
        # 테스트 예측
        test_features = {
            'latency': 3500,
            'revisions': 4,
            'efficiency': 0.75,
            'intensity': 2.3
        }
        
        print(f"\n테스트 입력:")
        print(f"  - Latency: {test_features['latency']}ms")
        print(f"  - Revisions: {test_features['revisions']}")
        print(f"  - Efficiency: {test_features['efficiency']:.2f}")
        
        prediction = model.predict(test_features)
        
        print(f"\n✓ ML 모델 예측 결과:")
        print(f"  - Logic: {prediction['Logic']:.2f}")
        print(f"  - Intuition: {prediction['Intuition']:.2f}")
        print(f"  - Fluidity: {prediction['Fluidity']:.2f}")
        print(f"  - Complexity: {prediction['Complexity']:.2f}")
        
        # 특징 중요도
        importance = model.get_feature_importance()
        if importance:
            print(f"\n특징 중요도 (Logic):")
            for feature, imp in importance.get('Logic', {}).items():
                print(f"  - {feature}: {imp:.3f}")
        
        return prediction
        
    except ImportError as e:
        print(f"⚠️ ML 모델을 로드할 수 없습니다: {e}")
        print("   규칙 기반 시스템으로 대체됩니다.")
        return None

def run_full_demo():
    """전체 시연 실행"""
    print("=" * 60)
    print("행동 기반 디지털 휴먼 트윈 - 오프라인 시연")
    print("=" * 60)
    print("\n백엔드 서버 없이 직접 함수를 호출하여 시연합니다.\n")
    
    try:
        # 1. 성격 추론
        personality_result = demo_personality_inference()
        
        # 2. 지속적 학습
        learning_result = demo_continuous_learning()
        
        # 3. 예측 분석
        predictive_result = demo_predictive_analysis()
        
        # 4. ML 모델
        ml_result = demo_ml_model()
        
        # 시연 요약
        print("\n" + "=" * 60)
        print("시연 완료!")
        print("=" * 60)
        print("\n시연된 기능:")
        print("  ✓ 행동 프로필 → 성격 가중치 추론 (ML 모델 사용)")
        print("  ✓ 지속적 학습 (EMA 업데이트)")
        print("  ✓ 예측 분석 (스트레스, 이상 감지, 트렌드)")
        if ml_result:
            print("  ✓ 머신러닝 모델 (랜덤 포레스트)")
        
        print("\n실제 시스템 로직이 정상적으로 작동하고 있습니다!")
        print("\n다음 단계:")
        print("  1. 백엔드 서버 실행: python backend/api_server.py")
        print("  2. 프론트엔드 실행: npm run dev")
        print("  3. 브라우저에서 http://localhost:5173 접속")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_full_demo()
