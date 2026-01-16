#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공개 데이터를 우리 파이프라인에 연결하는 테스트
"""
import sys
import os
import json
from typing import List, Dict

# Mock 데이터 생성 (실제 API 호출 없이 테스트)
def create_mock_opendota_events() -> List[Dict]:
    """OpenDota 스타일의 Mock 이벤트 생성"""
    return [
        {
            "type": "match_start",
            "timestamp": 1000,
            "match_id": 12345,
            "game_mode": 2
        },
        {
            "type": "player_action",
            "timestamp": 2000,
            "player_id": 1,
            "hero": 1,
            "kills": 5,
            "deaths": 2,
            "assists": 10,
            "position": {"x": 100, "y": 200}
        },
        {
            "type": "player_action",
            "timestamp": 3000,
            "player_id": 1,
            "hero": 1,
            "kills": 6,
            "deaths": 2,
            "assists": 12,
            "position": {"x": 150, "y": 250}
        },
        {
            "type": "match_end",
            "timestamp": 40000,
            "match_id": 12345,
            "radiant_win": True
        }
    ]

def create_mock_minerl_events() -> List[Dict]:
    """MineRL 스타일의 Mock 이벤트 생성"""
    events = []
    base_time = 1000
    
    # 건축 시작 전 계획 시간
    for i in range(5):
        events.append({
            "type": "inventory_change",
            "timestamp": base_time + i * 1000,
            "items": ["minecraft:stone", "minecraft:dirt"]
        })
    
    # 건축 이벤트
    for i in range(10):
        events.append({
            "type": "block_place",
            "timestamp": base_time + 5000 + i * 500,
            "position": {"x": i, "y": 64, "z": 0},
            "block_type": "minecraft:stone"
        })
    
    # 수정 (블록 제거)
    events.append({
        "type": "block_break",
        "timestamp": base_time + 10000,
        "position": {"x": 0, "y": 64, "z": 0}
    })
    
    # 이동 이벤트
    for i in range(5):
        events.append({
            "type": "player_move",
            "timestamp": base_time + 12000 + i * 1000,
            "from": {"x": i * 10, "y": 64, "z": i * 10},
            "to": {"x": (i + 1) * 10, "y": 64, "z": (i + 1) * 10}
        })
    
    return events

def test_minecraft_pipeline():
    """마인크래프트 데이터 파이프라인 테스트"""
    print("=" * 60)
    print("마인크래프트 (Mock) 데이터 파이프라인 테스트")
    print("=" * 60)
    
    # Mock 이벤트 생성
    raw_events = create_mock_minerl_events()
    print(f"✓ Mock 이벤트 생성: {len(raw_events)}개")
    
    # 1단계: 이벤트 파싱
    from game_event_parser import parse_game_events
    metrics = parse_game_events("minecraft", raw_events)
    print(f"\n✓ 1단계: 이벤트 파싱 완료")
    print(f"  - planning_time: {metrics['planning_time']} ms")
    print(f"  - revision_count: {metrics['revision_count']}")
    print(f"  - complexity: {metrics['complexity']:.2f}")
    print(f"  - path_efficiency: {metrics['path_efficiency']:.2f}")
    print(f"  - risk_taking: {metrics['risk_taking']:.2f}")
    print(f"  - diversity: {metrics['diversity']:.2f}")
    
    # 2단계: 표준 프로필 변환
    from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData
    processor = GameBehaviorProcessor()
    game_data = GameBehavioralData(
        game_id="minecraft",
        session_id="mock_test_session",
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
    print(f"\n✓ 2단계: 표준 프로필 변환 완료")
    print(f"  - pathEfficiency: {profile['pathEfficiency']:.2f}")
    print(f"  - revisionRate: {profile['revisionRate']}")
    print(f"  - jitterIndex: {profile['jitterIndex']:.2f}")
    print(f"  - intensity: {profile['intensity']:.2f}")
    
    # 3단계: 성격 추론 (간단한 테스트)
    print(f"\n✓ 3단계: 프로필 생성 완료")
    print(f"  - gameId: {profile['gameId']}")
    
    return profile

def test_dota2_pipeline():
    """Dota 2 데이터 파이프라인 테스트"""
    print("\n" + "=" * 60)
    print("Dota 2 (Mock) 데이터 파이프라인 테스트")
    print("=" * 60)
    
    # Mock 이벤트 생성
    raw_events = create_mock_opendota_events()
    print(f"✓ Mock 이벤트 생성: {len(raw_events)}개")
    
    # Dota 2는 현재 파서가 없으므로 간단한 변환만 수행
    print(f"\n⚠ Dota 2 파서는 아직 구현되지 않았습니다.")
    print(f"  (현재는 Minecraft, Stardew Valley, Animal Crossing만 지원)")
    
    # 하지만 이벤트 구조는 확인 가능
    print(f"\n✓ 이벤트 구조 확인:")
    for event in raw_events:
        print(f"  - {event['type']}: timestamp={event['timestamp']}")
    
    return raw_events

def test_api_integration():
    """API 통합 테스트 (Mock 데이터)"""
    print("\n" + "=" * 60)
    print("API 통합 테스트 (Mock 데이터)")
    print("=" * 60)
    
    # Mock 이벤트 생성
    raw_events = create_mock_minerl_events()
    
    # API 요청 형식으로 변환
    api_request = {
        "user_id": "test_user_public_data",
        "game_id": "minecraft",
        "session_id": "public_data_session_001",
        "raw_events": raw_events
    }
    
    print(f"✓ API 요청 형식 생성 완료")
    print(f"  - user_id: {api_request['user_id']}")
    print(f"  - game_id: {api_request['game_id']}")
    print(f"  - session_id: {api_request['session_id']}")
    print(f"  - raw_events: {len(api_request['raw_events'])}개")
    
    # 실제 API 호출은 서버가 실행 중일 때만 가능
    print(f"\n⚠ 실제 API 호출은 서버 실행 필요:")
    print(f"  POST /api/game/events")
    print(f"  Body: {json.dumps(api_request, indent=2, ensure_ascii=False)[:200]}...")
    
    return api_request

def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("공개 데이터 파이프라인 테스트")
    print("=" * 60)
    
    try:
        # 1. 마인크래프트 파이프라인 테스트
        minecraft_profile = test_minecraft_pipeline()
        
        # 2. Dota 2 파이프라인 테스트
        dota2_events = test_dota2_pipeline()
        
        # 3. API 통합 테스트
        api_request = test_api_integration()
        
        # 결과 저장
        output_dir = "datasets/public"
        os.makedirs(output_dir, exist_ok=True)
        
        # 마인크래프트 결과 저장
        with open(f"{output_dir}/test_minecraft_profile.json", 'w', encoding='utf-8') as f:
            json.dump(minecraft_profile, f, indent=2, ensure_ascii=False)
        
        # API 요청 예시 저장
        with open(f"{output_dir}/test_api_request.json", 'w', encoding='utf-8') as f:
            json.dump(api_request, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("✓ 모든 테스트 완료!")
        print("=" * 60)
        print(f"\n생성된 파일:")
        print(f"  - {output_dir}/test_minecraft_profile.json")
        print(f"  - {output_dir}/test_api_request.json")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
