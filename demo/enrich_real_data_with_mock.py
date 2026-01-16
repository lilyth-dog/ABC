"""
실제 데이터에 Mock 행동 프로필 추가
실제 성격 가중치를 기반으로 논리적인 행동 데이터 생성
"""
import json
import numpy as np
from pathlib import Path

def generate_mock_behavioral_profile(personality_weights, session_num):
    """
    성격 가중치를 기반으로 논리적인 행동 프로필 생성
    
    Logic이 높으면 → 높은 의사결정 지연시간
    Intuition이 높으면 → 낮은 의사결정 지연시간
    Fluidity가 높으면 → 높은 경로 효율성
    Complexity가 높으면 → 높은 수정 빈도
    """
    logic = personality_weights.get('Logic', 0.5)
    intuition = personality_weights.get('Intuition', 0.5)
    fluidity = personality_weights.get('Fluidity', 0.5)
    complexity = personality_weights.get('Complexity', 0.5)
    
    # 의사결정 지연시간: Logic이 높을수록 높음 (1000ms ~ 5000ms)
    # Logic=0.0 → 1000ms, Logic=1.0 → 5000ms
    base_latency = 1000 + (logic * 4000)
    # 세션이 진행될수록 약간 증가 (학습 효과)
    latency = base_latency + (session_num * 100) + np.random.normal(0, 200)
    latency = max(500, min(6000, latency))  # 범위 제한
    
    # 경로 효율성: Fluidity가 높을수록 높음 (0.3 ~ 1.0)
    base_efficiency = 0.3 + (fluidity * 0.7)
    # 세션이 진행될수록 개선
    efficiency = base_efficiency + (session_num * 0.02) + np.random.normal(0, 0.05)
    efficiency = max(0.3, min(1.0, efficiency))
    
    # 수정 빈도: Complexity가 높을수록 높음 (0 ~ 8)
    base_revisions = complexity * 8
    # Logic이 높으면 더 신중하게 수정
    if logic > 0.6:
        revisions = int(base_revisions * 1.2) + np.random.randint(0, 2)
    else:
        revisions = int(base_revisions) + np.random.randint(0, 2)
    revisions = max(0, min(10, revisions))
    
    # 지터 지수: Fluidity가 낮을수록 높음 (0.0 ~ 0.3)
    jitter = (1.0 - fluidity) * 0.3 + np.random.normal(0, 0.02)
    jitter = max(0.0, min(0.3, jitter))
    
    # 상호작용 강도: Complexity와 Logic의 조합
    intensity = (complexity * 2.0) + (logic * 1.5) + np.random.normal(0, 0.2)
    intensity = max(0.5, min(5.0, intensity))
    
    return {
        "pathEfficiency": round(efficiency, 2),
        "avgDecisionLatency": int(latency),
        "revisionRate": revisions,
        "jitterIndex": round(jitter, 2),
        "intensity": round(intensity, 2)
    }

def enrich_real_data():
    """실제 데이터에 Mock 행동 프로필 추가"""
    # 실제 데이터 로드
    real_data_path = Path(__file__).parent / "real_user_profile.json"
    
    if not real_data_path.exists():
        print("❌ real_user_profile.json을 찾을 수 없습니다.")
        print("   먼저 demo/extract_real_data.py를 실행하세요.")
        return None
    
    with open(real_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("실제 데이터에 Mock 행동 프로필 추가")
    print("=" * 60)
    print(f"사용자: {data['user_id']}")
    print(f"세션 수: {len(data['sessions'])}")
    
    # 각 세션에 Mock 행동 프로필 추가
    for i, session in enumerate(data['sessions'], 1):
        if 'personality_weights' in session:
            # 기존 행동 프로필이 0이면 Mock 데이터로 교체
            bp = session['behavioral_profile']
            if bp.get('avgDecisionLatency', 0) == 0 and bp.get('pathEfficiency', 0) == 0:
                mock_profile = generate_mock_behavioral_profile(
                    session['personality_weights'],
                    i
                )
                session['behavioral_profile'] = mock_profile
                print(f"  ✓ 세션 {i}: Mock 행동 프로필 생성")
                print(f"    - Latency: {mock_profile['avgDecisionLatency']}ms")
                print(f"    - Efficiency: {mock_profile['pathEfficiency']:.2f}")
                print(f"    - Revisions: {mock_profile['revisionRate']}")
            else:
                print(f"  - 세션 {i}: 기존 데이터 유지")
        else:
            print(f"  ⚠️ 세션 {i}: 성격 가중치 없음, 기본값 사용")
            # 기본 성격 가중치로 Mock 생성
            default_weights = {
                "Logic": 0.5,
                "Intuition": 0.5,
                "Fluidity": 0.5,
                "Complexity": 0.5
            }
            mock_profile = generate_mock_behavioral_profile(default_weights, i)
            session['behavioral_profile'] = mock_profile
            session['personality_weights'] = default_weights
    
    # 예측 데이터 추가 (선형 추세 기반)
    if len(data['sessions']) >= 2:
        latest = data['sessions'][-1]
        prev = data['sessions'][-2]
        
        pw_latest = latest['personality_weights']
        pw_prev = prev['personality_weights']
        
        # 선형 추세 계산
        trends = {}
        for key in ['Logic', 'Intuition', 'Fluidity', 'Complexity']:
            current = pw_latest.get(key, 0.5)
            previous = pw_prev.get(key, 0.5)
            slope = (current - previous) / (latest['session'] - prev['session'])
            
            # 30일 후 예측 (세션당 0.1 증가 가정)
            predicted = current + (slope * 30)
            predicted = max(0.0, min(1.0, predicted))
            
            trends[key] = {
                "current": round(current, 2),
                "predicted": round(predicted, 2),
                "trend": "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable",
                "slope": round(slope, 4)
            }
        
        data['predictions'] = {
            "30days": {k: v["predicted"] for k, v in trends.items()},
            "trend": {k: v["trend"] for k, v in trends.items()},
            "slope": {k: v["slope"] for k, v in trends.items()}
        }
        print("\n✓ 예측 데이터 생성 완료")
    
    # 스트레스 분석 추가
    latest_bp = data['sessions'][-1]['behavioral_profile']
    latency = latest_bp.get('avgDecisionLatency', 0)
    efficiency = latest_bp.get('pathEfficiency', 0)
    
    # 스트레스 레벨 계산 (지연시간이 높고 효율성이 낮으면 스트레스 높음)
    stress_level = (latency / 6000) * 0.5 + (1.0 - efficiency) * 0.5
    stress_level = max(0.0, min(1.0, stress_level))
    
    if stress_level < 0.3:
        category = "low"
    elif stress_level < 0.6:
        category = "medium"
    else:
        category = "high"
    
    data['stress_analysis'] = {
        "level": round(stress_level, 2),
        "category": category,
        "indicators": [
            "경로 효율성 안정적" if efficiency > 0.7 else "경로 효율성 개선 필요",
            "의사결정 패턴 일관성 유지" if latency < 4000 else "의사결정 지연시간 증가"
        ],
        "recommendation": "현재 상태 양호. 지속적인 모니터링 권장." if category == "low" else "스트레스 관리 권장."
    }
    print("✓ 스트레스 분석 추가 완료")
    
    # 저장
    output_path = Path(__file__).parent / "real_user_profile_enriched.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 보강된 데이터 저장: {output_path}")
    return data

if __name__ == '__main__':
    np.random.seed(42)  # 재현 가능한 결과
    data = enrich_real_data()
    
    if data:
        print("\n" + "=" * 60)
        print("보강된 데이터로 차트 생성 가능합니다!")
        print("=" * 60)
        print("\n다음 명령어로 차트 생성:")
        print("  python test_real_data.py")
        print("\n또는:")
        print("  python generate_demo_charts.py  # real_user_profile_enriched.json 사용")
