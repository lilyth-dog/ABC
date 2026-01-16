"""
실제 시스템 시연 테스트
백엔드 API를 호출하여 실제 동작 확인
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_api_health():
    """API 서버 상태 확인"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✓ API 서버 실행 중")
            return True
        else:
            print(f"⚠️ API 서버 응답: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API 서버에 연결할 수 없습니다.")
        print("   백엔드를 먼저 실행하세요: python backend/api_server.py")
        return False
    except Exception as e:
        print(f"❌ 오류: {e}")
        return False

def demo_session_save():
    """세션 저장 시연"""
    print("\n" + "=" * 60)
    print("시연 1: 세션 저장 및 성격 추론")
    print("=" * 60)
    
    # 샘플 행동 프로필 데이터
    session_data = {
        "user_id": "demo_live_user",
        "behavioral_profile": {
            "pathEfficiency": 0.75,
            "avgDecisionLatency": 3500,
            "revisionRate": 4,
            "jitterIndex": 0.12,
            "intensity": 2.3
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/session",
            json=session_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ 세션 저장 성공!")
            print(f"\n응답 데이터:")
            print(f"  - 세션 ID: {result.get('session_id', 'N/A')}")
            
            if 'updated_weights' in result:
                weights = result['updated_weights']
                print(f"\n성격 가중치:")
                print(f"  - Logic: {weights.get('Logic', 0):.2f}")
                print(f"  - Intuition: {weights.get('Intuition', 0):.2f}")
                print(f"  - Fluidity: {weights.get('Fluidity', 0):.2f}")
                print(f"  - Complexity: {weights.get('Complexity', 0):.2f}")
            
            print(f"  - 신뢰도: {result.get('confidence', 0):.2%}")
            print(f"  - 아키타입: {result.get('archetype', 'N/A')}")
            print(f"  - ML 모델 사용: {result.get('evidence', {}).get('ml_model_used', False)}")
            
            return result
        else:
            print(f"❌ 오류: {response.status_code}")
            print(f"   응답: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None

def demo_predictive_insights():
    """예측 인사이트 시연"""
    print("\n" + "=" * 60)
    print("시연 2: 예측 인사이트 조회")
    print("=" * 60)
    
    user_id = "demo_live_user"
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/insights/{user_id}",
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ 예측 인사이트 조회 성공!")
            
            # 스트레스 분석
            if 'stress_analysis' in result:
                stress = result['stress_analysis']
                print(f"\n스트레스 분석:")
                print(f"  - 레벨: {stress.get('stress_level', 0):.2f}")
                print(f"  - 카테고리: {stress.get('stress_category', 'N/A')}")
                if 'recommendation' in stress:
                    print(f"  - 권장사항: {stress['recommendation']}")
            
            # 행동 트렌드
            if 'behavior_trend' in result and 'trends' in result['behavior_trend']:
                trends = result['behavior_trend']['trends']
                print(f"\n행동 트렌드:")
                for trait, data in trends.items():
                    print(f"  - {trait}: {data.get('trend', 'N/A')} "
                          f"(현재: {data.get('current', 0):.2f}, "
                          f"예측: {data.get('predicted', 0):.2f})")
            
            # 이상 감지
            if 'anomaly_detection' in result:
                anomaly = result['anomaly_detection']
                print(f"\n이상 감지:")
                print(f"  - 이상 발견: {anomaly.get('has_anomaly', False)}")
                print(f"  - 이상 점수: {anomaly.get('anomaly_score', 0):.2f}")
            
            return result
        else:
            print(f"❌ 오류: {response.status_code}")
            print(f"   응답: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None

def demo_evolution():
    """진화 데이터 시연"""
    print("\n" + "=" * 60)
    print("시연 3: 프로필 진화 조회")
    print("=" * 60)
    
    user_id = "demo_live_user"
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/evolution/{user_id}",
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ 진화 데이터 조회 성공!")
            
            if 'sessions' in result:
                print(f"\n세션 수: {len(result['sessions'])}")
                for i, session in enumerate(result['sessions'][-3:], 1):  # 최근 3개만
                    print(f"\n세션 {session.get('session', i)}:")
                    if 'weights' in session:
                        w = session['weights']
                        print(f"  - Logic: {w.get('Logic', 0):.2f}, "
                              f"Intuition: {w.get('Intuition', 0):.2f}")
                    print(f"  - 신뢰도: {session.get('confidence', 0):.2%}")
            
            if 'summary' in result:
                summary = result['summary']
                print(f"\n요약:")
                print(f"  - 총 세션: {summary.get('total_sessions', 0)}")
                print(f"  - 신뢰도 성장: {summary.get('confidence_growth', 'N/A')}")
                print(f"  - 주요 특성: {summary.get('primary_trait', 'N/A')}")
            
            return result
        else:
            print(f"❌ 오류: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        return None

def run_full_demo():
    """전체 시연 실행"""
    print("=" * 60)
    print("행동 기반 디지털 휴먼 트윈 - 라이브 시연")
    print("=" * 60)
    
    # 1. API 서버 확인
    if not test_api_health():
        print("\n⚠️ API 서버가 실행되지 않았습니다.")
        print("\n백엔드를 실행하려면:")
        print("  1. 새 터미널 열기")
        print("  2. cd backend")
        print("  3. python api_server.py")
        print("\n그 다음 이 스크립트를 다시 실행하세요.")
        return
    
    # 2. 세션 저장 시연
    session_result = demo_session_save()
    if not session_result:
        print("\n⚠️ 세션 저장 실패. 시연을 계속할 수 없습니다.")
        return
    
    time.sleep(1)
    
    # 3. 예측 인사이트 시연
    insights_result = demo_predictive_insights()
    
    time.sleep(1)
    
    # 4. 진화 데이터 시연
    evolution_result = demo_evolution()
    
    # 5. 시연 요약
    print("\n" + "=" * 60)
    print("시연 완료!")
    print("=" * 60)
    print("\n시연된 기능:")
    print("  ✓ 세션 저장 및 성격 추론")
    if insights_result:
        print("  ✓ 예측 인사이트 (스트레스, 트렌드, 이상 감지)")
    if evolution_result:
        print("  ✓ 프로필 진화 추적")
    
    print("\n실제 시스템이 정상적으로 작동하고 있습니다!")

if __name__ == '__main__':
    try:
        run_full_demo()
    except KeyboardInterrupt:
        print("\n\n시연이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
