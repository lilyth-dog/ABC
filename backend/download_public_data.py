#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공개 게임 데이터 다운로드 및 파싱 스크립트
MineRL, OpenDota 등 공개 데이터셋을 우리 파이프라인에 연결
"""
import os
import json
import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PublicDataDownloader:
    """공개 게임 데이터 다운로더"""
    
    def __init__(self, output_dir: str = "datasets/public"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def download_minerl_sample(self, dataset_name: str = "MineRLObtainDiamond-v0") -> List[Dict]:
        """
        MineRL 샘플 데이터 다운로드 (테스트용)
        
        Args:
            dataset_name: MineRL 데이터셋 이름
        
        Returns:
            파싱된 이벤트 리스트
        """
        try:
            import minerl
            logger.info(f"MineRL 데이터셋 로드 중: {dataset_name}")
            
            # 데이터셋 로드
            data = minerl.data.make(dataset_name)
            
            # 샘플 데이터 추출 (처음 10개만)
            events = []
            count = 0
            max_samples = 10
            
            for obs, act, rew, next_obs, done in data.batch_iter(1, 1, 1):
                if count >= max_samples:
                    break
                
                # MineRL 데이터를 우리 형식으로 변환
                event = self._convert_minerl_to_our_format(obs, act, count)
                events.append(event)
                count += 1
            
            # 저장
            output_path = os.path.join(self.output_dir, "minerl_sample.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✓ MineRL 샘플 데이터 저장: {output_path} ({len(events)}개 이벤트)")
            return events
            
        except ImportError:
            logger.warning("MineRL 패키지가 설치되지 않았습니다. 'pip install minerl' 실행 필요")
            return []
        except Exception as e:
            logger.error(f"MineRL 데이터 다운로드 실패: {e}")
            return []
    
    def _convert_minerl_to_our_format(self, obs: Dict, act: Dict, index: int) -> Dict:
        """MineRL 데이터를 우리 이벤트 형식으로 변환"""
        # 간단한 변환 예시
        # 실제로는 obs와 act의 모든 필드를 분석해야 함
        return {
            "type": "game_state",
            "timestamp": index * 1000,  # 가상 타임스탬프
            "position": {
                "x": float(obs.get("location_stats", {}).get("xpos", 0)),
                "y": float(obs.get("location_stats", {}).get("ypos", 64)),
                "z": float(obs.get("location_stats", {}).get("zpos", 0))
            },
            "action": {
                "forward": int(act.get("forward", 0)),
                "jump": int(act.get("jump", 0)),
                "attack": int(act.get("attack", 0))
            }
        }
    
    def download_opendota_sample(self, limit: int = 5) -> List[Dict]:
        """
        OpenDota 공개 매치 샘플 다운로드
        
        Args:
            limit: 다운로드할 매치 수
        
        Returns:
            파싱된 이벤트 리스트
        """
        try:
            from pyopendota import OpenDota
            
            logger.info(f"OpenDota 공개 매치 조회 중 (최대 {limit}개)...")
            
            client = OpenDota()
            
            # 공개 매치 조회
            public_matches = client.get_public_matches(limit=limit)
            
            events = []
            for match in public_matches:
                match_id = match.get('match_id')
                if not match_id:
                    continue
                
                try:
                    # 매치 상세 정보 조회
                    match_detail = client.get_match(match_id)
                    
                    # Dota 2 이벤트를 우리 형식으로 변환
                    converted_events = self._convert_dota2_to_our_format(match_detail)
                    events.extend(converted_events)
                    
                    logger.info(f"✓ 매치 {match_id} 처리 완료 ({len(converted_events)}개 이벤트)")
                    
                except Exception as e:
                    logger.warning(f"매치 {match_id} 처리 실패: {e}")
                    continue
            
            # 저장
            output_path = os.path.join(self.output_dir, "opendota_sample.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✓ OpenDota 샘플 데이터 저장: {output_path} ({len(events)}개 이벤트)")
            return events
            
        except ImportError:
            logger.warning("pyopendota 패키지가 설치되지 않았습니다. 'pip install pyopendota' 실행 필요")
            return []
        except Exception as e:
            logger.error(f"OpenDota 데이터 다운로드 실패: {e}")
            return []
    
    def _convert_dota2_to_our_format(self, match_detail: Dict) -> List[Dict]:
        """Dota 2 매치 데이터를 우리 이벤트 형식으로 변환"""
        events = []
        
        # 매치 시작 이벤트
        events.append({
            "type": "match_start",
            "timestamp": match_detail.get("start_time", 0) * 1000,
            "match_id": match_detail.get("match_id"),
            "game_mode": match_detail.get("game_mode")
        })
        
        # 플레이어 이벤트
        players = match_detail.get("players", [])
        for player in players:
            events.append({
                "type": "player_action",
                "timestamp": match_detail.get("start_time", 0) * 1000,
                "player_id": player.get("account_id"),
                "hero": player.get("hero_id"),
                "kills": player.get("kills", 0),
                "deaths": player.get("deaths", 0),
                "assists": player.get("assists", 0)
            })
        
        # 매치 종료 이벤트
        events.append({
            "type": "match_end",
            "timestamp": (match_detail.get("start_time", 0) + match_detail.get("duration", 0)) * 1000,
            "match_id": match_detail.get("match_id"),
            "radiant_win": match_detail.get("radiant_win", False)
        })
        
        return events
    
    def download_pubg_sample(self, api_key: Optional[str] = None) -> List[Dict]:
        """
        PUBG 텔레메트리 샘플 다운로드 (API 키 필요)
        
        Args:
            api_key: PUBG API 키
        
        Returns:
            파싱된 이벤트 리스트
        """
        if not api_key:
            logger.warning("PUBG API 키가 필요합니다. 환경 변수 PUBG_API_KEY 설정 필요")
            return []
        
        try:
            # PUBG API 호출 예시
            # 실제 구현은 PUBG API 문서 참고
            logger.info("PUBG API 연동은 구현 필요 (API 키 및 엔드포인트 설정)")
            return []
            
        except Exception as e:
            logger.error(f"PUBG 데이터 다운로드 실패: {e}")
            return []


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description="공개 게임 데이터 다운로드")
    parser.add_argument("--source", choices=["minerl", "opendota", "all"], default="all",
                       help="다운로드할 데이터 소스")
    parser.add_argument("--output", default="datasets/public",
                       help="출력 디렉토리")
    
    args = parser.parse_args()
    
    downloader = PublicDataDownloader(output_dir=args.output)
    
    if args.source in ["minerl", "all"]:
        print("=" * 50)
        print("MineRL 데이터 다운로드")
        print("=" * 50)
        downloader.download_minerl_sample()
    
    if args.source in ["opendota", "all"]:
        print("\n" + "=" * 50)
        print("OpenDota 데이터 다운로드")
        print("=" * 50)
        downloader.download_opendota_sample(limit=5)
    
    print("\n✓ 모든 데이터 다운로드 완료!")


if __name__ == "__main__":
    main()
