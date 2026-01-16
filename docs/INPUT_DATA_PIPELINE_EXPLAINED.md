# 입력 데이터 파이프라인 완전 설명
## "게임 플레이 데이터만 넣으면 알아서 파싱해주지 않는다"

---

## ❓ 핵심 질문

**Q: "입력 데이터가 어떻게 되는지 궁금해. 게임 플레이 데이터만 넣으면 알아서 파싱해주진 않을거 아냐?"**

**A: 맞습니다! 게임 플레이 데이터를 그냥 넣으면 파싱되지 않습니다. 3단계 파이프라인이 필요합니다.**

---

## 📊 전체 파이프라인

### 단계별 데이터 변환 과정

```
[게임 플레이]
    ↓
[1단계: 원시 이벤트 수집]
게임 모드에서 이벤트 리스너로 수집
    ↓
원시 이벤트 데이터 (JSON)
{
  "events": [
    {"type": "block_place", "timestamp": 1234, "position": {...}},
    {"type": "player_move", "timestamp": 1235, "from": {...}, "to": {...}}
  ]
}
    ↓
[2단계: 이벤트 파싱 및 메트릭 계산]
GameEventParser.parse_minecraft_events()
    ↓
행동 메트릭 (계산된 값)
{
  "planning_time": 300000,    # 계산됨
  "revision_count": 5,         # 계산됨
  "complexity": 0.9,           # 계산됨
  "path_efficiency": 0.75,     # 계산됨
  "risk_taking": 0.3           # 계산됨
}
    ↓
[3단계: 표준 프로필 변환]
GameBehaviorProcessor.process()
    ↓
표준 행동 프로필
{
  "pathEfficiency": 0.75,
  "avgDecisionLatency": 0,
  "revisionRate": 5,
  "jitterIndex": 0.25,
  "intensity": 1.8
}
    ↓
[4단계: 성격 추론]
ML 모델 (Random Forest)
    ↓
성격 가중치
{
  "Logic": 0.75,
  "Intuition": 0.25,
  "Fluidity": 0.7,
  "Complexity": 0.9
}
```

---

## 🔧 1단계: 원시 이벤트 수집

### 마인크래프트 모드 예시

**게임 모드에서 수집하는 원시 데이터:**

```java
// Forge 모드
@SubscribeEvent
public void onBlockPlace(BlockEvent.PlaceEvent event) {
    // 원시 이벤트 수집
    GameEvent rawEvent = {
        "type": "block_place",
        "timestamp": System.currentTimeMillis(),
        "position": {
            "x": event.getPos().getX(),
            "y": event.getPos().getY(),
            "z": event.getPos().getZ()
        },
        "block_type": event.getState().getBlock().getRegistryName().toString()
    };
    
    eventCollector.addEvent(rawEvent);
}
```

**수집된 원시 이벤트 (JSON):**
```json
{
  "session_id": "mc_session_001",
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
    }
  ]
}
```

**이것을 그대로 API에 보내면 안 됩니다!** 파싱이 필요합니다.

---

## 🔧 2단계: 이벤트 파싱 및 메트릭 계산

### GameEventParser 사용

```python
from game_event_parser import parse_game_events

# 1단계에서 수집한 원시 이벤트
raw_events = [
    {"type": "block_place", "timestamp": 1705123456789, "position": {...}},
    {"type": "block_break", "timestamp": 1705123457000, "position": {...}},
    {"type": "player_move", "timestamp": 1705123457100, "from": {...}, "to": {...}}
]

# 2단계: 원시 이벤트 → 행동 메트릭 변환
metrics = parse_game_events("minecraft", raw_events)

# 결과:
# {
#   "planning_time": 300000,    # 건축 시작 전 계획 시간 계산
#   "revision_count": 5,         # 블록 배치 후 제거 횟수 계산
#   "complexity": 0.9,           # 건축 복잡도 계산
#   "path_efficiency": 0.75,     # 이동 경로 효율성 계산
#   "risk_taking": 0.3,          # 위험 지역 탐험 비율 계산
#   "diversity": 0.6             # 자원 다양성 계산
# }
```

### 파싱 알고리즘 상세

**계획 시간 계산:**
```python
def _calculate_planning_time(raw_events, build_start_time):
    # 건축 시작 전 5분간의 이벤트 분석
    pre_build_events = [
        e for e in raw_events 
        if e['timestamp'] < build_start_time 
        and build_start_time - e['timestamp'] < 300000
    ]
    
    # 인벤토리 준비, 이동 등 계획 행동 시간
    planning_actions = [
        e for e in pre_build_events 
        if e['type'] in ['inventory_change', 'player_move']
    ]
    
    return last_action_time - first_action_time
```

**수정 빈도 계산:**
```python
def _calculate_revision_count(raw_events, build_events):
    revision_count = 0
    
    for place_event in build_events:
        # 같은 위치에 블록을 배치했다가 제거한 경우
        break_events = [
            e for e in raw_events 
            if e['type'] == 'block_break'
            and e['position'] == place_event['position']
            and e['timestamp'] > place_event['timestamp']
        ]
        if break_events:
            revision_count += 1
    
    return revision_count
```

**경로 효율성 계산:**
```python
def _calculate_path_efficiency(move_events):
    # 실제 이동 거리
    actual_distance = sum(
        euclidean_distance(e['from'], e['to']) 
        for e in move_events[1:]
    )
    
    # 직선 거리
    straight_distance = euclidean_distance(
        move_events[0]['from'],
        move_events[-1]['to']
    )
    
    # 효율성 = 직선 거리 / 실제 거리
    return straight_distance / actual_distance
```

---

## 🔧 3단계: 표준 프로필 변환

### GameBehaviorProcessor 사용

```python
from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData

# 2단계에서 계산된 메트릭
metrics = {
    "planning_time": 300000,
    "revision_count": 5,
    "complexity": 0.9,
    "path_efficiency": 0.75,
    "risk_taking": 0.3,
    "diversity": 0.6
}

# 표준 프로필로 변환
processor = GameBehaviorProcessor()
game_data = GameBehavioralData(
    game_id="minecraft",
    session_id="mc_session_001",
    decision_latency=0,  # 마인크래프트는 실시간
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
# → {"pathEfficiency": 0.75, "avgDecisionLatency": 0, "revisionRate": 5, ...}
```

---

## 🔧 4단계: 성격 추론

### ML 모델 사용

```python
from neuro_controller import MagnonicController

controller = MagnonicController()

# 3단계에서 변환된 표준 프로필
result = controller.process_behavioral_profile(behavioral_profile)

# 결과:
# {
#   "behavioral_traits": {
#     "weights": {
#       "Logic": 0.75,
#       "Intuition": 0.25,
#       "Fluidity": 0.7,
#       "Complexity": 0.9
#     }
#   }
# }
```

---

## 📋 완전한 구현 예시

### 마인크래프트 모드 (전체 파이프라인)

```java
// ===== 1단계: 원시 이벤트 수집 =====
public class BehaviorTrackerMod {
    private List<GameEvent> rawEvents = new ArrayList<>();
    
    @SubscribeEvent
    public void onBlockPlace(BlockEvent.PlaceEvent event) {
        GameEvent rawEvent = new GameEvent(
            "block_place",
            System.currentTimeMillis(),
            event.getPos(),
            event.getState().getBlock().getRegistryName().toString()
        );
        rawEvents.add(rawEvent);
    }
    
    @SubscribeEvent
    public void onPlayerMove(TickEvent.PlayerTickEvent event) {
        GameEvent rawEvent = new GameEvent(
            "player_move",
            System.currentTimeMillis(),
            event.player.getPreviousPosition(),
            event.player.getPosition()
        );
        rawEvents.add(rawEvent);
    }
    
    // ===== 2단계: 이벤트 파싱 =====
    public void onSessionEnd() {
        // 원시 이벤트를 JSON으로 변환
        JSONObject rawEventsJson = convertToJSON(rawEvents);
        
        // 파이썬 파서로 전송 (또는 Java로 직접 구현)
        BehavioralMetrics metrics = parseEvents(rawEventsJson);
        
        // ===== 3단계: 표준 프로필 변환 =====
        // GameBehaviorProcessor로 변환 (API 호출)
        sendToAPI(metrics);
    }
    
    private void sendToAPI(BehavioralMetrics metrics) {
        JSONObject data = new JSONObject();
        data.put("user_id", getUserId());
        data.put("game_id", "minecraft");
        data.put("session_id", getSessionId());
        data.put("planning_time", metrics.getPlanningTime());
        data.put("revision_count", metrics.getRevisionCount());
        data.put("complexity", metrics.getComplexity());
        data.put("path_efficiency", metrics.getPathEfficiency());
        data.put("task_efficiency", metrics.getTaskEfficiency());
        data.put("diversity", metrics.getDiversity());
        data.put("game_specific_metrics", metrics.getGameSpecific());
        
        // POST /api/game/session
        httpClient.post("http://api.example.com/api/game/session", data);
    }
}
```

---

## 🎯 Skills의 역할

**Behavioral Analysis Skill은 3단계 이후에 사용됩니다:**

```python
# Skills는 이미 파싱된 표준 프로필을 받아서 성격 추론
from neuro_controller import MagnonicController

controller = MagnonicController()

# 이미 변환된 표준 프로필 (3단계 결과)
profile = {
    "pathEfficiency": 0.75,
    "avgDecisionLatency": 0,
    "revisionRate": 5,
    "jitterIndex": 0.25,
    "intensity": 1.8
}

# 4단계: 성격 추론
result = controller.process_behavioral_profile(profile)
```

**Skills는 파싱을 하지 않습니다!** 
- Skills는 **표준 행동 프로필**을 입력으로 받습니다
- 파싱은 **게임별 모듈**에서 해야 합니다

---

## 💡 요약

### 입력 데이터 형식

**❌ 잘못된 방법:**
```json
{
  "game_play_log": "마인크래프트 플레이 로그 전체 텍스트..."
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

**2단계 출력 (행동 메트릭):**
```json
{
  "planning_time": 300000,
  "revision_count": 5,
  "complexity": 0.9,
  "path_efficiency": 0.75
}
```

**3단계 출력 (표준 프로필):**
```json
{
  "pathEfficiency": 0.75,
  "avgDecisionLatency": 0,
  "revisionRate": 5
}
```

**4단계 출력 (성격 가중치):**
```json
{
  "Logic": 0.75,
  "Intuition": 0.25,
  "Fluidity": 0.7,
  "Complexity": 0.9
}
```

---

## 🔧 구현 필요 사항

### 각 게임별로 필요한 것

1. **이벤트 수집 모듈** (게임 모드)
   - 게임 이벤트 리스너
   - 원시 데이터 저장

2. **파싱 모듈** (`game_event_parser.py`)
   - 원시 이벤트 → 메트릭 변환
   - 게임별 특화 계산

3. **프로필 변환 모듈** (`game_behavior_processor.py`)
   - 메트릭 → 표준 프로필 변환

4. **API 통합**
   - 표준 프로필을 백엔드로 전송

---

## 📝 결론

**"게임 플레이 데이터만 넣으면 알아서 파싱해주지 않습니다."**

**필요한 것:**
1. 게임 모드에서 원시 이벤트 수집
2. `GameEventParser`로 메트릭 계산
3. `GameBehaviorProcessor`로 표준 프로필 변환
4. ML 모델로 성격 추론

**Skills는 3-4단계에서만 사용됩니다.** 파싱은 별도 모듈이 필요합니다!

---

**© 2026 Nexus Entertainment**
