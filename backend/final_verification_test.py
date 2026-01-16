#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
최종 검증 및 테스트 스크립트
전체 시스템 통합 테스트, API 검증, E2E 테스트, 성능 벤치마크
"""
import sys
import os
import json
import time
import requests
from typing import Dict, List, Tuple, Any
from datetime import datetime

# 백엔드 디렉토리를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from api_server import app

# 테스트 결과 저장
test_results = {
    "timestamp": datetime.now().isoformat(),
    "tests": {},
    "summary": {}
}

def print_section(title: str):
    """섹션 제목 출력"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_test(name: str, status: str, details: str = ""):
    """테스트 결과 출력"""
    status_symbol = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
    print(f"{status_symbol} [{status}] {name}")
    if details:
        print(f"    {details}")

def test_1_system_components():
    """1. 시스템 컴포넌트 초기화 테스트"""
    print_section("1. 시스템 컴포넌트 초기화 테스트")
    
    results = []
    
    try:
        from neuro_controller import MagnonicController, ContinuousLearner
        controller = MagnonicController()
        results.append(("MagnonicController 초기화", "PASS", ""))
    except Exception as e:
        results.append(("MagnonicController 초기화", "FAIL", str(e)))
    
    try:
        from user_profiles import UserProfileManager
        profile_manager = UserProfileManager()
        results.append(("UserProfileManager 초기화", "PASS", ""))
    except Exception as e:
        results.append(("UserProfileManager 초기화", "FAIL", str(e)))
    
    try:
        from game_event_parser import parse_game_events
        results.append(("game_event_parser 임포트", "PASS", ""))
    except Exception as e:
        results.append(("game_event_parser 임포트", "FAIL", str(e)))
    
    try:
        from game_behavior_processor import GameBehaviorProcessor
        processor = GameBehaviorProcessor()
        results.append(("GameBehaviorProcessor 초기화", "PASS", ""))
    except Exception as e:
        results.append(("GameBehaviorProcessor 초기화", "FAIL", str(e)))
    
    try:
        from neuro_controller import BehavioralPersonalityDecoder
        decoder = BehavioralPersonalityDecoder()
        results.append(("BehavioralPersonalityDecoder 초기화", "PASS", ""))
    except Exception as e:
        results.append(("BehavioralPersonalityDecoder 초기화", "FAIL", str(e)))
    
    # 결과 출력 및 저장
    passed = sum(1 for r in results if r[1] == "PASS")
    total = len(results)
    
    for name, status, details in results:
        print_test(name, status, details)
    
    test_results["tests"]["system_components"] = {
        "passed": passed,
        "total": total,
        "results": [{"name": r[0], "status": r[1], "details": r[2]} for r in results]
    }
    
    print(f"\n결과: {passed}/{total} 통과")
    return passed == total

def test_2_api_endpoints():
    """2. API 엔드포인트 검증"""
    print_section("2. API 엔드포인트 검증")
    
    client = TestClient(app)
    results = []
    
    # Health Check
    try:
        response = client.get("/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                results.append(("GET /health", "PASS", ""))
            else:
                results.append(("GET /health", "FAIL", f"Unexpected response: {data}"))
        else:
            results.append(("GET /health", "FAIL", f"Status code: {response.status_code}"))
    except Exception as e:
        results.append(("GET /health", "FAIL", str(e)))
    
    # Consent Endpoint
    try:
        user_id = "final_test_user_001"
        consent_data = {
            "consent_record": {
                "behavioralTracking": True,
                "profileStorage": True,
                "continuousLearning": True
            },
            "timestamp": datetime.now().isoformat()
        }
        response = client.post(f"/api/user/{user_id}/consent", json=consent_data)
        if response.status_code == 200:
            results.append(("POST /api/user/{id}/consent", "PASS", ""))
        else:
            results.append(("POST /api/user/{id}/consent", "FAIL", f"Status: {response.status_code}"))
    except Exception as e:
        results.append(("POST /api/user/{id}/consent", "FAIL", str(e)))
    
    # Game Events Endpoint
    try:
        game_data = {
            "user_id": "final_test_user_002",
            "game_id": "minecraft",
            "session_id": "test_session_001",
            "raw_events": [
                {"type": "player_move", "timestamp": 1000, "from": {"x": 0, "y": 64, "z": 0}, "to": {"x": 10, "y": 64, "z": 10}},
                {"type": "block_place", "timestamp": 2000, "position": {"x": 10, "y": 64, "z": 10}}
            ]
        }
        response = client.post("/api/game/events", json=game_data)
        if response.status_code == 200:
            data = response.json()
            if "session_id" in data and "updated_weights" in data:
                results.append(("POST /api/game/events", "PASS", ""))
            else:
                results.append(("POST /api/game/events", "FAIL", "Missing expected fields"))
        else:
            results.append(("POST /api/game/events", "FAIL", f"Status: {response.status_code}, {response.text[:100]}"))
    except Exception as e:
        results.append(("POST /api/game/events", "FAIL", str(e)))
    
    # Behavioral Profile Endpoint
    try:
        profile_data = {
            "pathEfficiency": 0.85,
            "avgDecisionLatency": 1500,
            "revisionRate": 2,
            "jitterIndex": 0.15,
            "intensity": 0.7,
            "contextualChoices": {"user_id": "final_test_user_003"},
            "taskCompletion": 0.9,
            "culturalContext": "east_asian"
        }
        response = client.post("/api/behavior", json=profile_data)
        if response.status_code == 200:
            data = response.json()
            if "behavioral_traits" in data:
                results.append(("POST /api/behavior", "PASS", ""))
            else:
                results.append(("POST /api/behavior", "FAIL", "Missing behavioral_traits"))
        else:
            results.append(("POST /api/behavior", "FAIL", f"Status: {response.status_code}, {response.text[:200]}"))
    except Exception as e:
        results.append(("POST /api/behavior", "FAIL", str(e)))
    
    # 결과 출력 및 저장
    passed = sum(1 for r in results if r[1] == "PASS")
    total = len(results)
    
    for name, status, details in results:
        print_test(name, status, details)
    
    test_results["tests"]["api_endpoints"] = {
        "passed": passed,
        "total": total,
        "results": [{"name": r[0], "status": r[1], "details": r[2]} for r in results]
    }
    
    print(f"\n결과: {passed}/{total} 통과")
    return passed == total

def test_3_game_pipeline():
    """3. 게임 데이터 파이프라인 테스트"""
    print_section("3. 게임 데이터 파이프라인 테스트")
    
    from game_event_parser import parse_game_events
    from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData
    
    results = []
    
    # Minecraft 이벤트 파싱 테스트
    try:
        minecraft_events = [
            {"type": "inventory_change", "timestamp": 1000, "items": ["stone", "dirt"]},
            {"type": "player_move", "timestamp": 2000, "from": {"x": 0, "y": 64, "z": 0}, "to": {"x": 10, "y": 64, "z": 10}},
            {"type": "block_place", "timestamp": 3000, "position": {"x": 10, "y": 64, "z": 10}},
            {"type": "block_break", "timestamp": 4000, "position": {"x": 10, "y": 64, "z": 10}}
        ]
        
        metrics = parse_game_events("minecraft", minecraft_events)
        
        if isinstance(metrics, dict) and len(metrics) > 0:
            results.append(("Minecraft 이벤트 파싱", "PASS", f"메트릭 수: {len(metrics)}"))
        else:
            results.append(("Minecraft 이벤트 파싱", "FAIL", "메트릭이 비어있음"))
    except Exception as e:
        results.append(("Minecraft 이벤트 파싱", "FAIL", str(e)))
    
    # 프로필 변환 테스트
    try:
        processor = GameBehaviorProcessor()
        game_behavior = GameBehavioralData(
            game_id="minecraft",
            session_id="test_session",
            decision_latency=0,
            planning_time=2000,
            revision_count=1,
            path_efficiency=0.85,
            task_efficiency=0.9,
            complexity=0.7,
            diversity=0.6
        )
        
        profile = processor.process(game_behavior)
        
        if isinstance(profile, dict) and "pathEfficiency" in profile:
            results.append(("게임 프로필 변환", "PASS", f"프로필 키 수: {len(profile)}"))
        else:
            results.append(("게임 프로필 변환", "FAIL", f"프로필 형식 오류: {list(profile.keys()) if isinstance(profile, dict) else type(profile)}"))
    except Exception as e:
        results.append(("게임 프로필 변환", "FAIL", str(e)))
    
    # 엣지 케이스 테스트
    try:
        empty_metrics = parse_game_events("minecraft", [])
        if isinstance(empty_metrics, dict):
            results.append(("빈 이벤트 리스트 처리", "PASS", ""))
        else:
            results.append(("빈 이벤트 리스트 처리", "FAIL", ""))
    except Exception as e:
        results.append(("빈 이벤트 리스트 처리", "FAIL", str(e)))
    
    # 결과 출력 및 저장
    passed = sum(1 for r in results if r[1] == "PASS")
    total = len(results)
    
    for name, status, details in results:
        print_test(name, status, details)
    
    test_results["tests"]["game_pipeline"] = {
        "passed": passed,
        "total": total,
        "results": [{"name": r[0], "status": r[1], "details": r[2]} for r in results]
    }
    
    print(f"\n결과: {passed}/{total} 통과")
    return passed == total

def test_4_performance_benchmark():
    """4. 성능 벤치마크"""
    print_section("4. 성능 벤치마크")
    
    from game_event_parser import parse_game_events
    
    results = []
    
    # 대량 이벤트 처리 성능 테스트
    try:
        large_event_list = []
        for i in range(1000):
            large_event_list.append({
                "type": "player_move",
                "timestamp": i * 100,
                "from": {"x": i, "y": 64, "z": i},
                "to": {"x": i + 1, "y": 64, "z": i + 1}
            })
        
        start_time = time.time()
        metrics = parse_game_events("minecraft", large_event_list)
        end_time = time.time()
        
        processing_time = (end_time - start_time) * 1000  # ms
        events_per_sec = len(large_event_list) / (end_time - start_time)
        
        if processing_time < 100:  # 100ms 이하
            results.append(("대량 이벤트 처리 (1000개)", "PASS", f"{processing_time:.2f}ms, {events_per_sec:.0f} events/sec"))
        else:
            results.append(("대량 이벤트 처리 (1000개)", "WARN", f"{processing_time:.2f}ms (목표: <100ms)"))
    except Exception as e:
        results.append(("대량 이벤트 처리", "FAIL", str(e)))
    
    # API 응답 시간 테스트
    try:
        client = TestClient(app)
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # ms
        
        if response_time < 50:  # 50ms 이하
            results.append(("API 응답 시간 (/health)", "PASS", f"{response_time:.2f}ms"))
        else:
            results.append(("API 응답 시간 (/health)", "WARN", f"{response_time:.2f}ms (목표: <50ms)"))
    except Exception as e:
        results.append(("API 응답 시간", "FAIL", str(e)))
    
    # 결과 출력 및 저장
    passed = sum(1 for r in results if r[1] == "PASS")
    total = len(results)
    
    for name, status, details in results:
        print_test(name, status, details)
    
    test_results["tests"]["performance"] = {
        "passed": passed,
        "total": total,
        "results": [{"name": r[0], "status": r[1], "details": r[2]} for r in results]
    }
    
    print(f"\n결과: {passed}/{total} 통과")
    return passed == total

def test_5_e2e_integration():
    """5. E2E 통합 테스트"""
    print_section("5. E2E 통합 테스트 (원시 이벤트 → 성격 추론)")
    
    client = TestClient(app)
    results = []
    
    try:
        # 전체 파이프라인 테스트: 원시 이벤트 → 파싱 → 프로필 변환 → 성격 추론
        user_id = "e2e_test_user_001"
        
        # 1. 동의 저장
        consent_data = {
            "consent_record": {
                "behavioralTracking": True,
                "profileStorage": True,
                "continuousLearning": True
            },
            "timestamp": datetime.now().isoformat()
        }
        client.post(f"/api/user/{user_id}/consent", json=consent_data)
        
        # 2. 게임 이벤트 처리
        game_data = {
            "user_id": user_id,
            "game_id": "minecraft",
            "session_id": "e2e_session_001",
            "raw_events": [
                {"type": "inventory_change", "timestamp": 1000, "items": ["stone"]},
                {"type": "player_move", "timestamp": 2000, "from": {"x": 0, "y": 64, "z": 0}, "to": {"x": 10, "y": 64, "z": 10}},
                {"type": "block_place", "timestamp": 3000, "position": {"x": 10, "y": 64, "z": 10}},
                {"type": "block_break", "timestamp": 4000, "position": {"x": 10, "y": 64, "z": 10}},
                {"type": "block_place", "timestamp": 5000, "position": {"x": 10, "y": 65, "z": 10}}
            ]
        }
        
        response = client.post("/api/game/events", json=game_data)
        
        if response.status_code == 200:
            data = response.json()
            
            # 필수 필드 확인
            required_fields = ["session_id", "game_id", "updated_weights", "archetype", "confidence"]
            missing_fields = [f for f in required_fields if f not in data]
            
            if not missing_fields:
                # 가중치 유효성 확인
                weights = data.get("updated_weights", {})
                if isinstance(weights, dict) and len(weights) > 0:
                    results.append(("E2E 파이프라인 (게임 이벤트 → 성격 추론)", "PASS", 
                                  f"신뢰도: {data.get('confidence', 0):.2f}"))
                else:
                    results.append(("E2E 파이프라인", "FAIL", "가중치가 비어있음"))
            else:
                results.append(("E2E 파이프라인", "FAIL", f"누락된 필드: {missing_fields}"))
        else:
            results.append(("E2E 파이프라인", "FAIL", f"Status: {response.status_code}, {response.text[:200]}"))
            
    except Exception as e:
        results.append(("E2E 파이프라인", "FAIL", str(e)))
        import traceback
        traceback.print_exc()
    
    # 결과 출력 및 저장
    passed = sum(1 for r in results if r[1] == "PASS")
    total = len(results)
    
    for name, status, details in results:
        print_test(name, status, details)
    
    test_results["tests"]["e2e_integration"] = {
        "passed": passed,
        "total": total,
        "results": [{"name": r[0], "status": r[1], "details": r[2]} for r in results]
    }
    
    print(f"\n결과: {passed}/{total} 통과")
    return passed == total

def generate_summary():
    """테스트 결과 요약 생성"""
    print_section("최종 검증 결과 요약")
    
    total_tests = 0
    total_passed = 0
    
    for test_name, test_data in test_results["tests"].items():
        passed = test_data["passed"]
        total = test_data["total"]
        total_tests += total
        total_passed += passed
        
        percentage = (passed / total * 100) if total > 0 else 0
        status = "✓" if passed == total else "⚠" if passed > 0 else "✗"
        
        print(f"{status} {test_name}: {passed}/{total} ({percentage:.1f}%)")
    
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    test_results["summary"] = {
        "total_tests": total_tests,
        "total_passed": total_passed,
        "overall_percentage": overall_percentage,
        "status": "PASS" if total_passed == total_tests else "PARTIAL" if total_passed > 0 else "FAIL"
    }
    
    print(f"\n{'=' * 70}")
    print(f"전체 결과: {total_passed}/{total_tests} 통과 ({overall_percentage:.1f}%)")
    print(f"상태: {test_results['summary']['status']}")
    print(f"{'=' * 70}")

def main():
    """메인 함수"""
    print("\n" + "=" * 70)
    print("  최종 검증 및 테스트 시작")
    print("=" * 70)
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 각 테스트 실행
        test_1_system_components()
        test_2_api_endpoints()
        test_3_game_pipeline()
        test_4_performance_benchmark()
        test_5_e2e_integration()
        
        # 결과 요약
        generate_summary()
        
        # 결과 저장
        output_file = "test_results_final.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n테스트 결과가 저장되었습니다: {output_file}")
        
        # 종료 코드 결정
        if test_results["summary"]["status"] == "PASS":
            print("\n✓ 모든 테스트 통과!")
            return 0
        elif test_results["summary"]["status"] == "PARTIAL":
            print("\n⚠ 일부 테스트 실패. 결과를 확인하세요.")
            return 1
        else:
            print("\n✗ 대부분의 테스트 실패. 시스템을 점검하세요.")
            return 1
            
    except Exception as e:
        print(f"\n✗ 테스트 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
