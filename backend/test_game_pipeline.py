#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
게임 데이터 파이프라인 테스트 스크립트
"""
import sys
from game_event_parser import GameEventParser, parse_game_events
from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData

def test_event_parser():
    """이벤트 파서 테스트"""
    print("=" * 50)
    print("1단계: 이벤트 파서 테스트")
    print("=" * 50)
    
    parser = GameEventParser()
    
    # 마인크래프트 테스트 이벤트
    test_events = [
        {
            "type": "block_place",
            "timestamp": 1000,
            "position": {"x": 0, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        },
        {
            "type": "block_break",
            "timestamp": 2000,
            "position": {"x": 0, "y": 64, "z": 0}
        },
        {
            "type": "player_move",
            "timestamp": 3000,
            "from": {"x": 0, "y": 64, "z": 0},
            "to": {"x": 10, "y": 64, "z": 10}
        },
        {
            "type": "inventory_change",
            "timestamp": 500,
            "items": ["minecraft:stone", "minecraft:dirt", "minecraft:wood"]
        }
    ]
    
    result = parser.parse_minecraft_events(test_events)
    
    print("✓ 파싱 성공!")
    print(f"  - planning_time: {result['planning_time']} ms")
    print(f"  - revision_count: {result['revision_count']}")
    print(f"  - complexity: {result['complexity']:.2f}")
    print(f"  - path_efficiency: {result['path_efficiency']:.2f}")
    print(f"  - risk_taking: {result['risk_taking']:.2f}")
    print(f"  - diversity: {result['diversity']:.2f}")
    
    return result

def test_parse_game_events_function():
    """parse_game_events 함수 테스트"""
    print("\n" + "=" * 50)
    print("2단계: parse_game_events 함수 테스트")
    print("=" * 50)
    
    test_events = [
        {
            "type": "block_place",
            "timestamp": 1000,
            "position": {"x": 0, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        },
        {
            "type": "player_move",
            "timestamp": 2000,
            "from": {"x": 0, "y": 64, "z": 0},
            "to": {"x": 10, "y": 64, "z": 10}
        }
    ]
    
    metrics = parse_game_events("minecraft", test_events)
    
    print("✓ 함수 호출 성공!")
    print(f"  파싱된 메트릭:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"    - {key}: {value:.2f}")
        else:
            print(f"    - {key}: {value}")
    
    return metrics

def test_behavior_processor():
    """행동 프로세서 테스트"""
    print("\n" + "=" * 50)
    print("3단계: 행동 프로세서 테스트")
    print("=" * 50)
    
    processor = GameBehaviorProcessor()
    
    game_data = GameBehavioralData(
        game_id="minecraft",
        session_id="test_session",
        decision_latency=0,
        planning_time=300000,  # 5분
        revision_count=5,
        path_efficiency=0.75,
        task_efficiency=0.8,
        complexity=0.9,
        diversity=0.6,
        game_specific_metrics={
            "riskTaking": 0.3,
            "buildComplexity": 0.9
        }
    )
    
    profile = processor.process(game_data)
    
    print("✓ 프로필 변환 성공!")
    print(f"  - pathEfficiency: {profile['pathEfficiency']:.2f}")
    print(f"  - avgDecisionLatency: {profile['avgDecisionLatency']} ms")
    print(f"  - revisionRate: {profile['revisionRate']}")
    print(f"  - jitterIndex: {profile['jitterIndex']:.2f}")
    print(f"  - intensity: {profile['intensity']:.2f}")
    print(f"  - gameId: {profile['gameId']}")
    
    return profile

def test_full_pipeline():
    """전체 파이프라인 테스트"""
    print("\n" + "=" * 50)
    print("4단계: 전체 파이프라인 테스트")
    print("=" * 50)
    
    # 1단계: 원시 이벤트
    raw_events = [
        {
            "type": "block_place",
            "timestamp": 1000,
            "position": {"x": 0, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        },
        {
            "type": "block_place",
            "timestamp": 2000,
            "position": {"x": 1, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        },
        {
            "type": "block_break",
            "timestamp": 3000,
            "position": {"x": 0, "y": 64, "z": 0}
        },
        {
            "type": "player_move",
            "timestamp": 4000,
            "from": {"x": 0, "y": 64, "z": 0},
            "to": {"x": 10, "y": 64, "z": 10}
        }
    ]
    
    # 2단계: 이벤트 파싱
    metrics = parse_game_events("minecraft", raw_events)
    print("✓ 2단계: 이벤트 파싱 완료")
    print(f"  - planning_time: {metrics['planning_time']} ms")
    print(f"  - revision_count: {metrics['revision_count']}")
    print(f"  - complexity: {metrics['complexity']:.2f}")
    
    # 3단계: 표준 프로필 변환
    processor = GameBehaviorProcessor()
    game_data = GameBehavioralData(
        game_id="minecraft",
        session_id="full_test",
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
    
    profile = processor.process(game_data)
    print("✓ 3단계: 표준 프로필 변환 완료")
    print(f"  - pathEfficiency: {profile['pathEfficiency']:.2f}")
    print(f"  - revisionRate: {profile['revisionRate']}")
    
    print("\n✓ 전체 파이프라인 테스트 성공!")
    return profile

if __name__ == "__main__":
    try:
        # 각 단계별 테스트
        test_event_parser()
        test_parse_game_events_function()
        test_behavior_processor()
        test_full_pipeline()
        
        print("\n" + "=" * 50)
        print("모든 테스트 통과! ✓")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
