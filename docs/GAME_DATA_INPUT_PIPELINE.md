# 게임 데이터 입력 파이프라인 상세 설명
## 원시 게임 이벤트 → 행동 메트릭 → 성격 추론

---

## 🔍 핵심 질문: "입력 데이터가 어떻게 되는가?"

**답변**: 게임 플레이 데이터를 그냥 넣으면 알아서 파싱되지 않습니다. 
**3단계 파이프라인**이 필요합니다:

1. **게임 이벤트 수집** (게임 모드/플러그인)
2. **원시 데이터 → 행동 메트릭 변환** (파싱 및 계산)
3. **행동 메트릭 → 표준 프로필 변환** (GameBehaviorProcessor)

---

## 📊 전체 데이터 흐름

```
게임 플레이
    ↓
[1단계: 이벤트 수집]
게임 모드/플러그인에서 원시 이벤트 수집
    ↓
원시 이벤트 데이터 (JSON/로그)
    ↓
[2단계: 메트릭 계산]
원시 이벤트 → 행동 메트릭 변환
    ↓
행동 메트릭 (planning_time, revision_count, etc.)
    ↓
[3단계: 프로필 변환]
GameBehaviorProcessor로 표준 프로필 변환
    ↓
표준 행동 프로필 (pathEfficiency, avgDecisionLatency, etc.)
    ↓
[4단계: 성격 추론]
ML 모델로 성격 가중치 예측
```

---

## 🎮 1단계: 게임 이벤트 수집

### 마인크래프트 예시

**원시 이벤트 데이터 (JSON):**
```json
{
  "events": [
    {
      "type": "block_place",
      "timestamp": 1705123456789,
      "position": {"x": 100, "y": 64, "z": 200},
      "block_type": "minecraft:stone"
    },
    {
      "type": "block_break",
      "timestamp": 1705123457000,
      "position": {"x": 100, "y": 64, "z": 200}
    },
    {
      "type": "player_move",
      "timestamp": 1705123457100,
      "from": {"x": 50, "y": 64, "z": 150},
      "to": {"x": 100, "y": 64, "z": 200}
    },
    {
      "type": "inventory_change",
      "timestamp": 1705123457200,
      "items": ["minecraft:stone", "minecraft:dirt"]
    }
  ],
  "session_start": 1705123400000,
  "session_end": 1705123600000
}
```

**이것을 그대로 넣으면 안 됩니다!** 파싱이 필요합니다.

---

## 🔧 2단계: 원시 이벤트 → 행동 메트릭 변환

### 파싱 알고리즘 구현

```python
class GameEventParser:
    """게임 원시 이벤트를 행동 메트릭으로 변환"""
    
    def parse_minecraft_events(self, raw_events: List[Dict]) -> Dict:
        """
        마인크래프트 원시 이벤트를 행동 메트릭으로 변환
        
        입력: 원시 이벤트 리스트
        출력: 행동 메트릭 딕셔너리
        """
        # 1. 건축 패턴 분석
        build_events = [e for e in raw_events if e['type'] == 'block_place']
        build_start_time = build_events[0]['timestamp'] if build_events else None
        build_end_time = build_events[-1]['timestamp'] if build_events else None
        
        # 계획 시간 계산 (건축 시작 전 대기 시간)
        planning_time = 0
        if build_start_time:
            # 건축 시작 전 5분간의 이벤트 분석
            pre_build_events = [
                e for e in raw_events 
                if e['timestamp'] < build_start_time 
                and build_start_time - e['timestamp'] < 300000  # 5분
            ]
            # 인벤토리 준비, 이동 등 계획 행동 시간 계산
            planning_time = self._calculate_planning_time(pre_build_events)
        
        # 수정 빈도 계산 (블록 배치 후 제거)
        revision_count = 0
        for i, place_event in enumerate(build_events):
            # 같은 위치에 블록을 배치했다가 제거한 경우
            break_events = [
                e for e in raw_events 
                if e['type'] == 'block_break' 
                and e['position'] == place_event['position']
                and e['timestamp'] > place_event['timestamp']
            ]
            if break_events:
                revision_count += 1
        
        # 건축 복잡도 계산
        build_positions = [e['position'] for e in build_events]
        complexity = self._calculate_build_complexity(build_positions)
        
        # 경로 효율성 계산 (이동 경로 분석)
        move_events = [e for e in raw_events if e['type'] == 'player_move']
        path_efficiency = self._calculate_path_efficiency(move_events)
        
        # 위험 선호도 계산 (위험한 지역 탐험)
        risk_taking = self._calculate_risk_taking(raw_events)
        
        return {
            "planning_time": planning_time,      # ms
            "revision_count": revision_count,
            "complexity": complexity,            # [0, 1]
            "path_efficiency": path_efficiency, # [0, 1]
            "risk_taking": risk_taking,          # [0, 1]
            "diversity": self._calculate_resource_diversity(raw_events)
        }
    
    def _calculate_planning_time(self, pre_build_events: List[Dict]) -> float:
        """계획 시간 계산"""
        if not pre_build_events:
            return 0
        
        # 인벤토리 준비, 이동 등 계획 행동 시간
        planning_actions = [
            e for e in pre_build_events 
            if e['type'] in ['inventory_change', 'player_move']
        ]
        
        if not planning_actions:
            return 0
        
        first_action = planning_actions[0]['timestamp']
        last_action = planning_actions[-1]['timestamp']
        
        return last_action - first_action
    
    def _calculate_build_complexity(self, positions: List[Dict]) -> float:
        """건축 복잡도 계산"""
        if len(positions) < 2:
            return 0.0
        
        # 높이 차이, 면적, 3D 구조 복잡도 계산
        heights = [p['y'] for p in positions]
        height_variance = np.var(heights) if len(heights) > 1 else 0
        
        # 면적 계산
        x_coords = [p['x'] for p in positions]
        z_coords = [p['z'] for p in positions]
        area = (max(x_coords) - min(x_coords)) * (max(z_coords) - min(z_coords))
        
        # 복잡도 = 높이 분산 + 면적 정규화
        complexity = min(1.0, (height_variance / 100) + (area / 10000))
        
        return complexity
    
    def _calculate_path_efficiency(self, move_events: List[Dict]) -> float:
        """경로 효율성 계산"""
        if len(move_events) < 2:
            return 1.0
        
        # 실제 이동 거리
        actual_distance = 0
        for i in range(1, len(move_events)):
            from_pos = move_events[i-1]['from']
            to_pos = move_events[i]['to']
            dist = self._euclidean_distance(from_pos, to_pos)
            actual_distance += dist
        
        # 직선 거리 (시작점 → 끝점)
        start_pos = move_events[0]['from']
        end_pos = move_events[-1]['to']
        straight_distance = self._euclidean_distance(start_pos, end_pos)
        
        # 효율성 = 직선 거리 / 실제 거리
        if actual_distance == 0:
            return 1.0
        
        efficiency = straight_distance / actual_distance
        return min(1.0, max(0.0, efficiency))
    
    def _calculate_risk_taking(self, events: List[Dict]) -> float:
        """위험 선호도 계산"""
        # 위험한 지역 탐험 (낮은 Y 좌표, 어두운 지역 등)
        dangerous_events = [
            e for e in events 
            if e.get('position', {}).get('y', 64) < 40  # 낮은 높이
            or e.get('light_level', 15) < 7  # 어두운 지역
        ]
        
        total_events = len(events)
        if total_events == 0:
            return 0.5
        
        risk_ratio = len(dangerous_events) / total_events
        return min(1.0, max(0.0, risk_ratio))
    
    def _euclidean_distance(self, pos1: Dict, pos2: Dict) -> float:
        """유클리드 거리 계산"""
        dx = pos1['x'] - pos2['x']
        dy = pos1['y'] - pos2['y']
        dz = pos1['z'] - pos2['z']
        return math.sqrt(dx*dx + dy*dy + dz*dz)
```

---

## 🔄 3단계: 행동 메트릭 → 표준 프로필 변환

### GameBehaviorProcessor 사용

```python
from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData

# 2단계에서 계산된 메트릭
metrics = {
    "planning_time": 300000,      # 5분
    "revision_count": 5,
    "complexity": 0.9,
    "path_efficiency": 0.75,
    "risk_taking": 0.3
}

# 표준 프로필로 변환
processor = GameBehaviorProcessor()
game_data = GameBehavioralData(
    game_id="minecraft",
    session_id="mc_session_001",
    decision_latency=0,  # 마인크래프트는 실시간이므로 0
    planning_time=metrics["planning_time"],
    revision_count=metrics["revision_count"],
    path_efficiency=metrics["path_efficiency"],
    task_efficiency=0.8,  # 기본값 또는 계산
    complexity=metrics["complexity"],
    diversity=0.6,  # 계산된 값
    game_specific_metrics={
        "riskTaking": metrics["risk_taking"],
        "buildComplexity": metrics["complexity"]
    }
)

# 표준 행동 프로필로 변환
behavioral_profile = processor.process(game_data)
# → {"pathEfficiency": 0.75, "avgDecisionLatency": 0, ...}
```

---

## 📋 실제 구현 예시

### 마인크래프트 모드 (완전한 파이프라인)

```java
// 1단계: 이벤트 수집
@SubscribeEvent
public void onBlockPlace(BlockEvent.PlaceEvent event) {
    GameEvent eventData = new GameEvent(
        "block_place",
        System.currentTimeMillis(),
        event.getPos(),
        event.getState().getBlock().getRegistryName().toString()
    );
    eventCollector.addEvent(eventData);
}

// 세션 종료 시
public void onSessionEnd() {
    // 2단계: 원시 이벤트 → 메트릭 변환
    List<GameEvent> rawEvents = eventCollector.getEvents();
    BehavioralMetrics metrics = eventParser.parse(rawEvents);
    
    // 3단계: API로 전송
    sendToAPI(metrics);
}

// API 전송
private void sendToAPI(BehavioralMetrics metrics) {
    JSONObject data = new JSONObject();
    data.put("user_id", getUserId());
    data.put("game_id", "minecraft");
    data.put("session_id", getSessionId());
    data.put("planning_time", metrics.getPlanningTime());
    data.put("revision_count", metrics.getRevisionCount());
    data.put("complexity", metrics.getComplexity());
    data.put("path_efficiency", metrics.getPathEfficiency());
    data.put("game_specific_metrics", metrics.getGameSpecific());
    
    // POST /api/game/session
    httpClient.post("http://api.example.com/api/game/session", data);
}
```

---

## 🎯 핵심 포인트

### 입력 데이터 형식

**❌ 잘못된 방법:**
```json
{
  "game_play_data": "마인크래프트 플레이 로그 전체..."
}
```
→ 이것은 파싱되지 않습니다!

**✅ 올바른 방법:**

**1단계 입력 (원시 이벤트):**
```json
{
  "events": [
    {"type": "block_place", "timestamp": 1234567890, "position": {...}},
    {"type": "player_move", "timestamp": 1234567900, "from": {...}, "to": {...}}
  ]
}
```

**2단계 입력 (행동 메트릭):**
```json
{
  "game_id": "minecraft",
  "planning_time": 300000,
  "revision_count": 5,
  "complexity": 0.9,
  "path_efficiency": 0.75
}
```

**3단계 입력 (표준 프로필):**
```json
{
  "pathEfficiency": 0.75,
  "avgDecisionLatency": 0,
  "revisionRate": 5,
  "jitterIndex": 0.25,
  "intensity": 1.8
}
```

---

## 🔧 구현 필요 사항

### 각 게임별로 필요한 것

1. **이벤트 수집 모듈**
   - 게임 이벤트 리스너
   - 원시 데이터 저장

2. **파싱 모듈**
   - 원시 이벤트 → 메트릭 변환
   - 게임별 특화 계산

3. **API 통합**
   - 메트릭을 백엔드로 전송
   - 표준 프로필 변환

---

## 💡 Skills 활용

Behavioral Analysis Skill은 **2-3단계 이후**에 사용됩니다:

```python
# Skills는 이미 파싱된 행동 프로필을 받아서 성격 추론
from neuro_controller import MagnonicController

controller = MagnonicController()
# 이미 변환된 표준 프로필
profile = {
    "pathEfficiency": 0.75,
    "avgDecisionLatency": 0,
    "revisionRate": 5
}
result = controller.process_behavioral_profile(profile)
```

**Skills는 파싱을 하지 않습니다.** 파싱은 게임별 모듈에서 해야 합니다.

---

## 📝 요약

**입력 데이터 파이프라인:**

1. **원시 게임 이벤트** (게임 모드에서 수집)
   - 블록 배치, 이동, 인벤토리 변경 등

2. **행동 메트릭** (파싱 모듈에서 계산)
   - 계획 시간, 수정 빈도, 복잡도 등

3. **표준 프로필** (GameBehaviorProcessor에서 변환)
   - pathEfficiency, avgDecisionLatency 등

4. **성격 가중치** (ML 모델에서 예측)
   - Logic, Intuition, Fluidity, Complexity

**게임 플레이 데이터를 그냥 넣으면 안 되고, 파싱이 필요합니다!**

---

**© 2026 Nexus Entertainment**
