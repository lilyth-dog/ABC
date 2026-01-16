#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전체 API 파이프라인 테스트
실제 API 서버 없이도 로직 테스트
"""
import sys
import json
import os
from typing import Dict, List

def test_full_pipeline_with_mock_data():
    """Mock 데이터로 전체 파이프라인 테스트"""
    print("=" * 60)
    print("전체 API 파이프라인 테스트 (Mock 데이터)")
    print("=" * 60)
    
    # Mock 원시 이벤트 생성
    raw_events = [
        {
            "type": "inventory_change",
            "timestamp": 1000,
            "items": ["minecraft:stone", "minecraft:dirt", "minecraft:wood"]
        },
        {
            "type": "inventory_change",
            "timestamp": 2000,
            "items": ["minecraft:stone", "minecraft:dirt"]
        },
        {
            "type": "block_place",
            "timestamp": 5000,
            "position": {"x": 0, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        },
        {
            "type": "block_place",
            "timestamp": 6000,
            "position": {"x": 1, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        },
        {
            "type": "block_place",
            "timestamp": 7000,
            "position": {"x": 2, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        },
        {
            "type": "block_break",
            "timestamp": 8000,
            "position": {"x": 0, "y": 64, "z": 0}
        },
        {
            "type": "player_move",
            "timestamp": 10000,
            "from": {"x": 0, "y": 64, "z": 0},
            "to": {"x": 10, "y": 64, "z": 10}
        },
        {
            "type": "player_move",
            "timestamp": 11000,
            "from": {"x": 10, "y": 64, "z": 10},
            "to": {"x": 20, "y": 64, "z": 20}
        }
    ]
    
    print(f"\n1단계: 원시 이벤트 생성 ({len(raw_events)}개)")
    
    # 2단계: 이벤트 파싱
    print("\n2단계: 이벤트 파싱")
    from game_event_parser import parse_game_events
    
    metrics = parse_game_events("minecraft", raw_events)
    print(f"✓ 파싱 완료:")
    print(f"  - planning_time: {metrics['planning_time']} ms")
    print(f"  - revision_count: {metrics['revision_count']}")
    print(f"  - complexity: {metrics['complexity']:.2f}")
    print(f"  - path_efficiency: {metrics['path_efficiency']:.2f}")
    print(f"  - risk_taking: {metrics['risk_taking']:.2f}")
    print(f"  - diversity: {metrics['diversity']:.2f}")
    
    # 3단계: 표준 프로필 변환
    print("\n3단계: 표준 프로필 변환")
    from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData
    
    processor = GameBehaviorProcessor()
    game_data = GameBehavioralData(
        game_id="minecraft",
        session_id="full_test_session",
        decision_latency=0,
        planning_time=metrics["planning_time"],
        revision_count=metrics["revision_count"],
        path_efficiency=metrics["path_efficiency"],
        task_efficiency=0.8,
        complexity=metrics["complexity"],
        diversity=metrics["diversity"],
        game_specific_metrics={
            "riskTaking": metrics["risk_taking"]
        }
    )
    
    behavioral_profile = processor.process(game_data)
    print(f"✓ 프로필 변환 완료:")
    print(f"  - pathEfficiency: {behavioral_profile['pathEfficiency']:.2f}")
    print(f"  - revisionRate: {behavioral_profile['revisionRate']}")
    print(f"  - jitterIndex: {behavioral_profile['jitterIndex']:.2f}")
    print(f"  - intensity: {behavioral_profile['intensity']:.2f}")
    
    # 4단계: 성격 추론 (간단한 시뮬레이션)
    print("\n4단계: 성격 추론 시뮬레이션")
    
    # 실제로는 neuro_controller를 사용하지만, 여기서는 간단한 시뮬레이션
    logic_score = min(1.0, metrics["planning_time"] / 300000)  # 계획 시간 기반
    intuition_score = 1.0 - logic_score
    fluidity_score = metrics["path_efficiency"]
    complexity_score = metrics["complexity"]
    
    personality_weights = {
        "Logic": logic_score,
        "Intuition": intuition_score,
        "Fluidity": fluidity_score,
        "Complexity": complexity_score
    }
    
    print(f"✓ 성격 가중치 계산:")
    for trait, weight in personality_weights.items():
        print(f"  - {trait}: {weight:.2f}")
    
    # 결과 저장
    output_dir = "datasets/public"
    os.makedirs(output_dir, exist_ok=True)
    
    result = {
        "raw_events": raw_events,
        "parsed_metrics": metrics,
        "behavioral_profile": behavioral_profile,
        "personality_weights": personality_weights
    }
    
    output_path = f"{output_dir}/full_pipeline_result.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ 전체 파이프라인 결과 저장: {output_path}")
    
    return result

def test_api_request_format():
    """API 요청 형식 테스트"""
    print("\n" + "=" * 60)
    print("API 요청 형식 테스트")
    print("=" * 60)
    
    # API 요청 형식 생성
    raw_events = [
        {
            "type": "block_place",
            "timestamp": 1000,
            "position": {"x": 0, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        }
    ]
    
    api_request = {
        "user_id": "test_user_full_pipeline",
        "game_id": "minecraft",
        "session_id": "full_pipeline_session_001",
        "raw_events": raw_events
    }
    
    print(f"\n✓ API 요청 형식 생성:")
    print(f"  - user_id: {api_request['user_id']}")
    print(f"  - game_id: {api_request['game_id']}")
    print(f"  - session_id: {api_request['session_id']}")
    print(f"  - raw_events: {len(api_request['raw_events'])}개")
    
    # 저장
    output_dir = "datasets/public"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = f"{output_dir}/api_request_example.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(api_request, f, indent=2, ensure_ascii=False)
    
    print(f"✓ API 요청 예시 저장: {output_path}")
    
    return api_request

def main():
    """메인 함수"""
    try:
        # 1. 전체 파이프라인 테스트
        result = test_full_pipeline_with_mock_data()
        
        # 2. API 요청 형식 테스트
        api_request = test_api_request_format()
        
        print("\n" + "=" * 60)
        print("✓ 전체 API 파이프라인 테스트 완료!")
        print("=" * 60)
        
        print("\n생성된 파일:")
        print("  - datasets/public/full_pipeline_result.json")
        print("  - datasets/public/api_request_example.json")
        
        print("\n다음 단계:")
        print("  1. API 서버 실행: python backend/api_server.py")
        print("  2. API 호출: curl -X POST http://localhost:8000/api/game/events \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d @datasets/public/api_request_example.json")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
