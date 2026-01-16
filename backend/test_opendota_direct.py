#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenDota API 직접 호출 테스트 (패키지 없이)
"""
import requests
import json
import time
from typing import List, Dict, Optional

def get_opendota_public_matches(limit: int = 5) -> List[Dict]:
    """
    OpenDota 공개 매치 조회 (패키지 없이 직접 API 호출)
    
    Args:
        limit: 조회할 매치 수
    
    Returns:
        공개 매치 리스트
    """
    try:
        url = "https://api.opendota.com/api/publicMatches"
        params = {
            "limit": limit,
            "min_mmr": 0  # 최소 MMR (필터링)
        }
        
        print(f"OpenDota API 호출 중: {url}")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            matches = response.json()
            print(f"✓ {len(matches)}개 매치 조회 성공")
            return matches
        else:
            print(f"⚠ API 호출 실패: {response.status_code}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"⚠ 네트워크 오류: {e}")
        return []
    except Exception as e:
        print(f"⚠ 오류 발생: {e}")
        return []

def get_match_details(match_id: int) -> Optional[Dict]:
    """
    매치 상세 정보 조회
    
    Args:
        match_id: 매치 ID
    
    Returns:
        매치 상세 정보
    """
    try:
        url = f"https://api.opendota.com/api/matches/{match_id}"
        
        print(f"  매치 {match_id} 상세 정보 조회 중...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            match = response.json()
            print(f"  ✓ 매치 {match_id} 조회 성공")
            return match
        else:
            print(f"  ⚠ 매치 {match_id} 조회 실패: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ⚠ 오류: {e}")
        return None

def convert_dota2_to_our_format(match_detail: Dict) -> List[Dict]:
    """Dota 2 매치 데이터를 우리 이벤트 형식으로 변환"""
    events = []
    
    if not match_detail:
        return events
    
    match_id = match_detail.get("match_id", 0)
    start_time = match_detail.get("start_time", 0) * 1000  # 초를 밀리초로 변환
    duration = match_detail.get("duration", 0) * 1000
    
    # 매치 시작 이벤트
    events.append({
        "type": "match_start",
        "timestamp": start_time,
        "match_id": match_id,
        "game_mode": match_detail.get("game_mode", 0),
        "lobby_type": match_detail.get("lobby_type", 0)
    })
    
    # 플레이어 이벤트
    players = match_detail.get("players", [])
    for player in players:
        player_id = player.get("account_id") or player.get("player_slot", 0)
        
        events.append({
            "type": "player_action",
            "timestamp": start_time,
            "player_id": player_id,
            "hero": player.get("hero_id", 0),
            "kills": player.get("kills", 0),
            "deaths": player.get("deaths", 0),
            "assists": player.get("assists", 0),
            "gold_per_min": player.get("gold_per_min", 0),
            "xp_per_min": player.get("xp_per_min", 0),
            "last_hits": player.get("last_hits", 0),
            "denies": player.get("denies", 0)
        })
    
    # 매치 종료 이벤트
    events.append({
        "type": "match_end",
        "timestamp": start_time + duration,
        "match_id": match_id,
        "radiant_win": match_detail.get("radiant_win", False),
        "duration": duration
    })
    
    return events

def test_opendota_integration():
    """OpenDota API 통합 테스트"""
    print("=" * 60)
    print("OpenDota API 직접 호출 테스트")
    print("=" * 60)
    
    # 1. 공개 매치 조회
    print("\n1단계: 공개 매치 조회")
    matches = get_opendota_public_matches(limit=3)
    
    if not matches:
        print("⚠ 공개 매치를 찾을 수 없습니다. Mock 데이터로 테스트합니다.")
        return test_with_mock_data()
    
    # 2. 첫 번째 매치 상세 정보 조회
    print("\n2단계: 매치 상세 정보 조회")
    if matches:
        first_match = matches[0]
        match_id = first_match.get("match_id")
        
        if match_id:
            match_detail = get_match_details(match_id)
            
            if match_detail:
                # 3. 우리 형식으로 변환
                print("\n3단계: 우리 이벤트 형식으로 변환")
                events = convert_dota2_to_our_format(match_detail)
                print(f"✓ {len(events)}개 이벤트 변환 완료")
                
                # 저장
                output_dir = "datasets/public"
                import os
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = f"{output_dir}/opendota_real_match_{match_id}.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "match_id": match_id,
                        "match_detail": match_detail,
                        "converted_events": events
                    }, f, indent=2, ensure_ascii=False)
                
                print(f"✓ 데이터 저장: {output_path}")
                
                # 이벤트 요약
                print("\n이벤트 요약:")
                event_types = {}
                for event in events:
                    event_type = event.get("type", "unknown")
                    event_types[event_type] = event_types.get(event_type, 0) + 1
                
                for event_type, count in event_types.items():
                    print(f"  - {event_type}: {count}개")
                
                return events
    
    return []

def test_with_mock_data():
    """Mock 데이터로 테스트"""
    print("\nMock 데이터로 테스트 진행...")
    
    # Mock Dota 2 매치 데이터
    mock_match = {
        "match_id": 12345,
        "start_time": int(time.time()) - 3600,
        "duration": 1800,
        "game_mode": 2,
        "lobby_type": 0,
        "radiant_win": True,
        "players": [
            {
                "account_id": 1,
                "hero_id": 1,
                "kills": 5,
                "deaths": 2,
                "assists": 10,
                "gold_per_min": 400,
                "xp_per_min": 500,
                "last_hits": 100,
                "denies": 5
            },
            {
                "account_id": 2,
                "hero_id": 2,
                "kills": 3,
                "deaths": 4,
                "assists": 8,
                "gold_per_min": 350,
                "xp_per_min": 450,
                "last_hits": 80,
                "denies": 3
            }
        ]
    }
    
    events = convert_dota2_to_our_format(mock_match)
    print(f"✓ Mock 데이터 변환 완료: {len(events)}개 이벤트")
    
    return events

if __name__ == "__main__":
    try:
        events = test_opendota_integration()
        
        print("\n" + "=" * 60)
        print("✓ OpenDota API 테스트 완료!")
        print("=" * 60)
        
        if events:
            print(f"\n총 {len(events)}개 이벤트 처리 완료")
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
