"""
게임 원시 이벤트 파싱 모듈
게임에서 수집한 원시 이벤트를 행동 메트릭으로 변환
"""
from typing import Dict, List, Optional
import math
import numpy as np
import logging

logger = logging.getLogger(__name__)


class GameEventParser:
    """게임 원시 이벤트를 행동 메트릭으로 변환"""
    
    def parse_minecraft_events(self, raw_events: List[Dict]) -> Dict:
        """
        마인크래프트 원시 이벤트를 행동 메트릭으로 변환
        
        Args:
            raw_events: 원시 이벤트 리스트
                [
                    {
                        "type": "block_place",
                        "timestamp": 1705123456789,
                        "position": {"x": 100, "y": 64, "z": 200},
                        "block_type": "minecraft:stone"
                    },
                    ...
                ]
        
        Returns:
            행동 메트릭 딕셔너리
            {
                "planning_time": float,      # ms
                "revision_count": int,
                "complexity": float,         # [0, 1]
                "path_efficiency": float,    # [0, 1]
                "risk_taking": float,        # [0, 1]
                "diversity": float           # [0, 1]
            }
        """
        if not raw_events:
            return self._default_metrics()
        
        # 타임스탬프 누락 처리: 기본값 설정
        import time
        current_time = int(time.time() * 1000)
        for event in raw_events:
            if 'timestamp' not in event:
                event['timestamp'] = current_time
                current_time += 100  # 다음 이벤트를 위해 시간 증가
        
        # 건축 패턴 분석
        build_events = [e for e in raw_events if e.get('type') == 'block_place']
        build_start_time = build_events[0]['timestamp'] if build_events else None
        
        # 계획 시간 계산
        planning_time = self._calculate_planning_time(raw_events, build_start_time)
        
        # 수정 빈도 계산
        revision_count = self._calculate_revision_count(raw_events, build_events)
        
        # 건축 복잡도 계산
        complexity = self._calculate_build_complexity(build_events)
        
        # 경로 효율성 계산
        move_events = [e for e in raw_events if e.get('type') == 'player_move']
        path_efficiency = self._calculate_path_efficiency(move_events)
        
        # 위험 선호도 계산
        risk_taking = self._calculate_risk_taking(raw_events)
        
        # 자원 다양성 계산
        diversity = self._calculate_resource_diversity(raw_events)
        
        return {
            "planning_time": planning_time,
            "revision_count": revision_count,
            "complexity": complexity,
            "path_efficiency": path_efficiency,
            "risk_taking": risk_taking,
            "diversity": diversity
        }
    
    def parse_stardew_valley_events(self, raw_events: List[Dict]) -> Dict:
        """스타듀밸리 원시 이벤트 파싱"""
        if not raw_events:
            return self._default_metrics()
        
        # 작물 선택 이벤트
        crop_selection_events = [
            e for e in raw_events 
            if e.get('type') == 'crop_selection'
        ]
        
        # 계획 시간 (작물 선택 전 대기 시간)
        planning_time = self._calculate_planning_time_stardew(raw_events, crop_selection_events)
        
        # 작물 다양성
        crop_types = set(
            e.get('crop_type') for e in crop_selection_events 
            if e.get('crop_type')
        )
        diversity = len(crop_types) / 10.0  # 정규화 (최대 10종류)
        
        # 농장 복잡도
        complexity = self._calculate_farm_complexity(raw_events)
        
        # 경로 효율성
        move_events = [e for e in raw_events if e.get('type') == 'player_move']
        path_efficiency = self._calculate_path_efficiency(move_events)
        
        # 수정 빈도 (작물 재배치)
        revision_count = self._calculate_crop_revisions(raw_events)
        
        return {
            "planning_time": planning_time,
            "revision_count": revision_count,
            "complexity": complexity,
            "path_efficiency": path_efficiency,
            "risk_taking": 0.5,  # 스타듀밸리는 위험 요소 적음
            "diversity": min(1.0, diversity)
        }
    
    def parse_animal_crossing_events(self, raw_events: List[Dict]) -> Dict:
        """두근두근타운 원시 이벤트 파싱"""
        if not raw_events:
            return self._default_metrics()
        
        # 섬 디자인 변경 이벤트
        design_events = [
            e for e in raw_events 
            if e.get('type') in ['item_place', 'item_remove', 'island_edit']
        ]
        
        # 계획 시간
        planning_time = self._calculate_planning_time_ac(raw_events, design_events)
        
        # 수정 빈도
        revision_count = len([
            e for e in design_events 
            if e.get('type') == 'item_remove'  # 배치 후 제거
        ])
        
        # 섬 복잡도
        complexity = self._calculate_island_complexity(design_events)
        
        # 다양성 (아이템 종류)
        item_types = set(
            e.get('item_type') for e in design_events 
            if e.get('item_type')
        )
        diversity = len(item_types) / 20.0  # 정규화
        
        return {
            "planning_time": planning_time,
            "revision_count": revision_count,
            "complexity": complexity,
            "path_efficiency": 0.7,  # 기본값
            "risk_taking": 0.3,  # 두근두근타운은 위험 요소 없음
            "diversity": min(1.0, diversity)
        }
    
    def _calculate_planning_time(
        self, 
        raw_events: List[Dict], 
        build_start_time: Optional[int]
    ) -> float:
        """계획 시간 계산 (마인크래프트) - 개선된 버전"""
        if not raw_events:
            return 0
        
        # 건축 시작 시간이 없으면 첫 건축 이벤트 시간 사용
        if not build_start_time:
            build_events = [e for e in raw_events if e.get('type') == 'block_place']
            if build_events:
                build_start_time = build_events[0].get('timestamp', 0)
            else:
                # 건축 이벤트가 없으면 첫 이벤트 시간 사용
                build_start_time = raw_events[0].get('timestamp', 0)
        
        # 건축 시작 전 5분간의 이벤트
        pre_build_events = [
            e for e in raw_events 
            if e.get('timestamp', 0) < build_start_time 
            and build_start_time - e.get('timestamp', 0) < 300000  # 5분
        ]
        
        if not pre_build_events:
            return 0
        
        # 계획 행동 (인벤토리 준비, 이동 등)
        planning_actions = [
            e for e in pre_build_events 
            if e.get('type') in ['inventory_change', 'player_move', 'item_craft']
        ]
        
        if not planning_actions:
            # 계획 행동이 없어도 첫 이벤트부터 건축 시작까지의 시간 계산
            first_event_time = pre_build_events[0].get('timestamp', 0)
            return max(0, build_start_time - first_event_time)
        
        first_action = planning_actions[0].get('timestamp', 0)
        last_action = planning_actions[-1].get('timestamp', 0)
        
        return max(0, last_action - first_action)
    
    def _calculate_revision_count(
        self, 
        raw_events: List[Dict], 
        build_events: List[Dict]
    ) -> int:
        """수정 빈도 계산 (블록 배치 후 제거) - 개선된 버전"""
        revision_count = 0
        
        try:
            for place_event in build_events:
                place_pos = place_event.get('position', {})
                place_time = place_event.get('timestamp', 0)
                
                # 위치 정보가 없으면 건너뛰기
                if not place_pos or not isinstance(place_pos, dict):
                    continue
                
                # 같은 위치에 블록을 제거한 이벤트 찾기
                break_events = [
                    e for e in raw_events 
                    if e.get('type') == 'block_break'
                    and e.get('position') == place_pos
                    and e.get('timestamp', 0) > place_time
                ]
                
                if break_events:
                    revision_count += 1
        except Exception as e:
            logger.warning(f"수정 빈도 계산 중 오류: {e}")
        
        return revision_count
    
    def _calculate_build_complexity(self, build_events: List[Dict]) -> float:
        """건축 복잡도 계산"""
        if len(build_events) < 2:
            return 0.0
        
        positions = [e.get('position', {}) for e in build_events]
        
        # 높이 분산
        heights = [p.get('y', 64) for p in positions if isinstance(p, dict)]
        if len(heights) < 2:
            return 0.5
        
        height_variance = np.var(heights) if len(heights) > 1 else 0
        
        # 면적 계산
        x_coords = [p.get('x', 0) for p in positions if isinstance(p, dict)]
        z_coords = [p.get('z', 0) for p in positions if isinstance(p, dict)]
        
        if not x_coords or not z_coords:
            return 0.5
        
        area = (max(x_coords) - min(x_coords)) * (max(z_coords) - min(z_coords))
        
        # 복잡도 = 높이 분산 + 면적 정규화
        complexity = min(1.0, (height_variance / 100) + (area / 10000))
        
        return complexity
    
    def _calculate_path_efficiency(self, move_events: List[Dict]) -> float:
        """경로 효율성 계산 - 개선된 버전 (에러 핸들링 강화)"""
        if len(move_events) < 2:
            return 1.0
        
        try:
            # 실제 이동 거리
            actual_distance = 0
            valid_moves = 0
            
            for i in range(1, len(move_events)):
                from_pos = move_events[i-1].get('from', {})
                to_pos = move_events[i].get('to', {})
                
                # 위치 정보가 없으면 기본값 사용
                if not from_pos:
                    from_pos = {'x': 0, 'y': 64, 'z': 0}
                if not to_pos:
                    to_pos = {'x': 0, 'y': 64, 'z': 0}
                
                try:
                    dist = self._euclidean_distance(from_pos, to_pos)
                    actual_distance += dist
                    valid_moves += 1
                except (KeyError, TypeError):
                    # 위치 정보가 불완전하면 건너뛰기
                    continue
            
            if valid_moves == 0:
                return 0.5  # 기본값
            
            # 직선 거리
            start_pos = move_events[0].get('from', {})
            end_pos = move_events[-1].get('to', {})
            
            if not start_pos:
                start_pos = {'x': 0, 'y': 64, 'z': 0}
            if not end_pos:
                end_pos = {'x': 0, 'y': 64, 'z': 0}
            
            try:
                straight_distance = self._euclidean_distance(start_pos, end_pos)
            except (KeyError, TypeError):
                return 0.5  # 기본값
            
            if actual_distance == 0:
                return 1.0
            
            efficiency = straight_distance / actual_distance
            return min(1.0, max(0.0, efficiency))
            
        except Exception as e:
            logger.warning(f"경로 효율성 계산 중 오류: {e}, 기본값 반환")
            return 0.5  # 기본값
    
    def _calculate_risk_taking(self, events: List[Dict]) -> float:
        """위험 선호도 계산"""
        dangerous_events = []
        
        for e in events:
            pos = e.get('position', {})
            if isinstance(pos, dict):
                # 낮은 높이 (위험)
                if pos.get('y', 64) < 40:
                    dangerous_events.append(e)
                # 어두운 지역
                elif e.get('light_level', 15) < 7:
                    dangerous_events.append(e)
        
        total_events = len(events)
        if total_events == 0:
            return 0.5
        
        risk_ratio = len(dangerous_events) / total_events
        return min(1.0, max(0.0, risk_ratio))
    
    def _calculate_resource_diversity(self, events: List[Dict]) -> float:
        """자원 다양성 계산"""
        resource_types = set()
        
        for e in events:
            if e.get('type') == 'inventory_change':
                items = e.get('items', [])
                if isinstance(items, list):
                    resource_types.update(items)
            elif e.get('type') == 'block_place':
                block_type = e.get('block_type')
                if block_type:
                    resource_types.add(block_type)
        
        # 정규화 (최대 20종류)
        diversity = len(resource_types) / 20.0
        return min(1.0, max(0.0, diversity))
    
    def _euclidean_distance(self, pos1: Dict, pos2: Dict) -> float:
        """유클리드 거리 계산"""
        x1, y1, z1 = pos1.get('x', 0), pos1.get('y', 0), pos1.get('z', 0)
        x2, y2, z2 = pos2.get('x', 0), pos2.get('y', 0), pos2.get('z', 0)
        
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def _calculate_planning_time_stardew(
        self, 
        raw_events: List[Dict], 
        crop_events: List[Dict]
    ) -> float:
        """스타듀밸리 계획 시간 계산"""
        if not crop_events:
            return 0
        
        first_crop_time = crop_events[0].get('timestamp', 0)
        
        # 작물 선택 전 이벤트
        pre_crop_events = [
            e for e in raw_events 
            if e.get('timestamp', 0) < first_crop_time
        ]
        
        if not pre_crop_events:
            return 0
        
        first_event = pre_crop_events[0].get('timestamp', 0)
        return max(0, first_crop_time - first_event)
    
    def _calculate_farm_complexity(self, events: List[Dict]) -> float:
        """농장 복잡도 계산"""
        crop_events = [e for e in events if e.get('type') == 'crop_selection']
        
        if not crop_events:
            return 0.5
        
        # 작물 종류 다양성
        crop_types = set(e.get('crop_type') for e in crop_events if e.get('crop_type'))
        
        # 배치 패턴 복잡도
        positions = [e.get('position', {}) for e in crop_events]
        if positions:
            x_coords = [p.get('x', 0) for p in positions if isinstance(p, dict)]
            z_coords = [p.get('z', 0) for p in positions if isinstance(p, dict)]
            
            if x_coords and z_coords:
                area = (max(x_coords) - min(x_coords)) * (max(z_coords) - min(z_coords))
                complexity = min(1.0, (len(crop_types) / 10) + (area / 1000))
                return complexity
        
        return len(crop_types) / 10.0
    
    def _calculate_crop_revisions(self, events: List[Dict]) -> int:
        """작물 재배치 횟수 계산"""
        revisions = 0
        
        for i, event in enumerate(events):
            if event.get('type') == 'crop_remove':
                # 같은 위치에 작물을 다시 심은 경우
                pos = event.get('position', {})
                later_plant_events = [
                    e for e in events[i+1:]
                    if e.get('type') == 'crop_selection'
                    and e.get('position') == pos
                ]
                if later_plant_events:
                    revisions += 1
        
        return revisions
    
    def _calculate_planning_time_ac(
        self, 
        raw_events: List[Dict], 
        design_events: List[Dict]
    ) -> float:
        """두근두근타운 계획 시간 계산"""
        if not design_events:
            return 0
        
        first_design_time = design_events[0].get('timestamp', 0)
        
        # 디자인 시작 전 이벤트
        pre_design_events = [
            e for e in raw_events 
            if e.get('timestamp', 0) < first_design_time
        ]
        
        if not pre_design_events:
            return 0
        
        first_event = pre_design_events[0].get('timestamp', 0)
        return max(0, first_design_time - first_event)
    
    def _calculate_island_complexity(self, design_events: List[Dict]) -> float:
        """섬 복잡도 계산"""
        if not design_events:
            return 0.5
        
        # 아이템 종류 다양성
        item_types = set(
            e.get('item_type') for e in design_events 
            if e.get('item_type')
        )
        
        # 배치 위치 다양성
        positions = [e.get('position', {}) for e in design_events]
        position_count = len(set(str(p) for p in positions if p))
        
        complexity = min(1.0, (len(item_types) / 20) + (position_count / 100))
        return complexity
    
    def _default_metrics(self) -> Dict[str, float]:
        """기본 메트릭 반환"""
        return {
            "planning_time": 0,
            "revision_count": 0,
            "complexity": 0.5,
            "path_efficiency": 0.5,
            "risk_taking": 0.5,
            "diversity": 0.5
        }


def parse_game_events(game_id: str, raw_events: List[Dict]) -> Dict:
    """
    게임 원시 이벤트를 행동 메트릭으로 변환 (편의 함수) - 개선된 버전
    
    Args:
        game_id: 게임 ID (minecraft, stardew_valley, animal_crossing)
        raw_events: 원시 이벤트 리스트
    
    Returns:
        행동 메트릭 딕셔너리
    """
    parser = GameEventParser()
    
    try:
        # 입력 검증
        if not isinstance(raw_events, list):
            logger.warning(f"raw_events가 리스트가 아닙니다: {type(raw_events)}, 기본 메트릭 반환")
            return parser._default_metrics()
        
        # 타임스탬프 누락 사전 처리
        import time
        current_time = int(time.time() * 1000)
        for event in raw_events:
            if not isinstance(event, dict):
                continue
            if 'timestamp' not in event:
                event['timestamp'] = current_time
                current_time += 100
        
        if game_id == "minecraft":
            return parser.parse_minecraft_events(raw_events)
        elif game_id == "stardew_valley":
            return parser.parse_stardew_valley_events(raw_events)
        elif game_id == "animal_crossing":
            return parser.parse_animal_crossing_events(raw_events)
        else:
            logger.warning(f"알 수 없는 게임 ID: {game_id}, 기본 메트릭 반환")
            return parser._default_metrics()
            
    except Exception as e:
        logger.error(f"게임 이벤트 파싱 중 오류 발생: {e}, 기본 메트릭 반환")
        import traceback
        traceback.print_exc()
        return parser._default_metrics()
