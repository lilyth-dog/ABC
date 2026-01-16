# 게임에서 행동 데이터 수집 가이드
## 마인크래프트, 두근두근타운, 스타듀밸리 등에서 성격 특성 추출

---

## 🎮 게임별 수집 가능한 행동 데이터

### 1. 마인크래프트 (Minecraft)

#### 수집 가능한 행동 신호

**빌드 패턴:**
- **건축 스타일**: 대칭적/비대칭적, 복잡도, 높이 선호도
- **빌드 시간**: 계획 시간, 실행 시간, 수정 빈도
- **재료 선택**: 보수적(나무) vs 공격적(다이아몬드), 다양성 선호

**탐험 패턴:**
- **위험 선호도**: 안전한 지역 탐험 vs 위험한 지역 탐험
- **탐험 범위**: 좁은 지역 집중 vs 넓은 지역 탐험
- **탐험 속도**: 신중한 탐험 vs 빠른 탐험

**자원 관리:**
- **수집 패턴**: 보수적 수집 vs 공격적 수집
- **인벤토리 관리**: 체계적 정리 vs 무질서
- **자원 사용**: 절약 vs 낭비

**사회적 상호작용:**
- **멀티플레이어 참여**: 협력 vs 경쟁
- **거래 패턴**: 공정한 거래 vs 이기적 거래
- **도움 제공**: 적극적 vs 소극적

#### 성격 특성 매핑

```typescript
interface MinecraftBehavioralProfile {
  // Logic vs Intuition
  buildPlanningTime: number;        // 계획 시간 (높으면 Logic)
  buildRevisionCount: number;        // 수정 횟수 (높으면 Logic)
  explorationRiskTaking: number;      // 위험 선호도 (높으면 Intuition)
  
  // Fluidity
  buildEfficiency: number;            // 건축 효율성
  movementSmoothness: number;        // 움직임 부드러움
  
  // Complexity
  buildComplexity: number;           // 건축 복잡도
  resourceDiversity: number;         // 자원 다양성
  inventoryOrganization: number;     // 인벤토리 정리도
}
```

---

### 2. 두근두근타운 (Animal Crossing)

#### 수집 가능한 행동 신호

**섬 관리 패턴:**
- **섬 디자인**: 계획적 vs 즉흥적
- **꾸미기 시간**: 세심함 vs 빠른 완성
- **수정 빈도**: 완벽주의 vs 실용주의

**NPC 상호작용:**
- **대화 빈도**: 적극적 vs 소극적
- **선물 선택**: 개인화된 선물 vs 일반적 선물
- **이벤트 참여**: 적극적 vs 소극적

**자원 수집:**
- **수집 패턴**: 체계적 vs 무작위
- **거래 패턴**: 보수적 vs 공격적
- **시간 관리**: 계획적 vs 즉흥적

#### 성격 특성 매핑

```typescript
interface AnimalCrossingBehavioralProfile {
  // Logic vs Intuition
  islandPlanningTime: number;       // 섬 계획 시간
  decisionLatency: number;           // 의사결정 지연시간
  npcInteractionDepth: number;      // NPC 상호작용 깊이
  
  // Fluidity
  designEfficiency: number;          // 디자인 효율성
  taskCompletionSpeed: number;       // 작업 완료 속도
  
  // Complexity
  designComplexity: number;          // 디자인 복잡도
  collectionDiversity: number;        // 수집 다양성
  customizationDepth: number;         // 커스터마이징 깊이
}
```

---

### 3. 스타듀밸리 (Stardew Valley)

#### 수집 가능한 행동 신호

**농장 관리:**
- **작물 선택**: 단일 작물 vs 다양성
- **계획성**: 계절별 계획 vs 즉흥적
- **최적화**: 효율 최적화 vs 다양성 선호

**탐험 및 전투:**
- **광산 탐험**: 신중한 탐험 vs 공격적 탐험
- **전투 스타일**: 방어적 vs 공격적
- **위험 관리**: 안전 우선 vs 보상 우선

**사회적 상호작용:**
- **NPC 관계**: 깊은 관계 vs 표면적 관계
- **선물 선택**: 개인화 vs 효율성
- **이벤트 참여**: 적극적 vs 소극적

**자원 관리:**
- **수익 최적화**: 최대 수익 vs 다양성
- **인벤토리 관리**: 체계적 vs 무질서
- **장비 선택**: 보수적 vs 실험적

#### 성격 특성 매핑

```typescript
interface StardewValleyBehavioralProfile {
  // Logic vs Intuition
  farmPlanningTime: number;          // 농장 계획 시간
  cropSelectionStrategy: number;     // 작물 선택 전략 (계획적 vs 직관적)
  mineExplorationStyle: number;      // 광산 탐험 스타일 (신중 vs 공격적)
  
  // Fluidity
  taskEfficiency: number;            // 작업 효율성
  dailyRoutineConsistency: number;   // 일일 루틴 일관성
  
  // Complexity
  farmComplexity: number;            // 농장 복잡도
  cropDiversity: number;             // 작물 다양성
  relationshipDepth: number;         // 관계 깊이
}
```

---

## 🔧 게임 데이터 수집 구현 방법

### 1. 게임 모드/플러그인 개발

#### 마인크래프트 (Forge/Fabric 모드)

```java
// Minecraft Mod 예시
public class BehaviorTrackerMod {
    private long buildStartTime;
    private int revisionCount;
    private List<BlockPos> buildPath;
    
    @SubscribeEvent
    public void onBlockPlace(BlockEvent.PlaceEvent event) {
        // 건축 시작 시간 기록
        if (buildStartTime == 0) {
            buildStartTime = System.currentTimeMillis();
        }
        
        // 건축 경로 기록
        buildPath.add(event.getPos());
        
        // 수정 빈도 계산 (이전 블록 제거 후 재배치)
        if (wasRemovedRecently(event.getPos())) {
            revisionCount++;
        }
    }
    
    @SubscribeEvent
    public void onPlayerMove(TickEvent.PlayerTickEvent event) {
        // 탐험 패턴 기록
        recordExplorationPattern(event.player.getPosition());
    }
    
    public BehavioralProfile generateProfile() {
        return new BehavioralProfile(
            calculateDecisionLatency(),  // 계획 시간
            calculatePathEfficiency(),  // 건축 효율성
            revisionCount,               // 수정 빈도
            calculateComplexity()        // 복잡도
        );
    }
}
```

#### 스타듀밸리 (SMAPI 모드)

```csharp
// Stardew Valley Mod 예시
public class BehaviorTrackerMod : Mod {
    private Dictionary<string, long> decisionTimes;
    private List<Crop> cropSelections;
    
    public override void Entry(IModHelper helper) {
        // 작물 선택 이벤트
        helper.Events.Input.ButtonPressed += OnButtonPressed;
        helper.Events.GameLoop.DayStarted += OnDayStarted;
    }
    
    private void OnButtonPressed(object sender, ButtonPressedEventArgs e) {
        // 의사결정 시간 기록
        if (IsDecisionPoint(e.Button)) {
            RecordDecisionLatency(e.Button);
        }
    }
    
    private void OnDayStarted(object sender, DayStartedEventArgs e) {
        // 농장 계획 시간 계산
        long planningTime = CalculatePlanningTime();
        int cropDiversity = CountCropTypes();
        
        // 행동 프로필 업데이트
        UpdateBehavioralProfile(planningTime, cropDiversity);
    }
}
```

---

### 2. 게임 로그 분석

#### 게임 로그에서 추출 가능한 데이터

**공통 메트릭:**
- **플레이 시간**: 세션 길이, 일일 플레이 시간
- **의사결정 시간**: 메뉴 체류 시간, 선택 지연시간
- **행동 빈도**: 특정 행동 반복 횟수
- **경로 효율성**: 목표까지의 경로 최적화

**게임별 특화 메트릭:**

**마인크래프트:**
```json
{
  "buildMetrics": {
    "planningTime": 120000,      // 밀리초
    "executionTime": 300000,
    "revisionCount": 5,
    "complexity": 0.75,
    "symmetry": 0.8
  },
  "explorationMetrics": {
    "distanceTraveled": 5000,
    "riskLevel": 0.6,
    "explorationEfficiency": 0.7
  }
}
```

**스타듀밸리:**
```json
{
  "farmMetrics": {
    "planningTime": 90000,
    "cropDiversity": 0.8,
    "optimizationScore": 0.65
  },
  "socialMetrics": {
    "npcInteractionDepth": 0.7,
    "giftPersonalization": 0.6
  }
}
```

---

### 3. API 통합

#### 게임 → 백엔드 API 전송

```typescript
// 게임 클라이언트에서 백엔드로 전송
interface GameBehavioralData {
  gameId: string;              // "minecraft", "stardew_valley", etc.
  sessionId: string;
  behavioralProfile: {
    // Logic vs Intuition
    decisionLatency: number;   // 의사결정 지연시간 (ms)
    planningTime: number;      // 계획 시간 (ms)
    riskTaking: number;        // 위험 선호도 [0, 1]
    
    // Fluidity
    pathEfficiency: number;    // 경로 효율성 [0, 1]
    taskEfficiency: number;    // 작업 효율성 [0, 1]
    
    // Complexity
    revisionRate: number;      // 수정 빈도
    complexity: number;        // 복잡도 [0, 1]
    diversity: number;        // 다양성 [0, 1]
  };
  gameSpecificMetrics: {
    // 게임별 특화 메트릭
    [key: string]: any;
  };
}

// API 호출
async function sendGameBehavioralData(data: GameBehavioralData) {
  const response = await fetch('http://api.example.com/api/game/behavior', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  const result = await response.json();
  return result.personalityWeights; // Logic, Intuition, Fluidity, Complexity
}
```

---

## 🎯 게임별 성격 특성 추론 예시

### 마인크래프트 예시

**시나리오 1: 계획적 건축가**
```json
{
  "buildPlanningTime": 300000,    // 5분 계획
  "buildRevisionCount": 8,         // 여러 번 수정
  "buildComplexity": 0.9,          // 복잡한 구조
  "explorationRiskTaking": 0.2     // 안전한 탐험
}
```
→ **예상 성격**: Logic 높음, Complexity 높음, Intuition 낮음

**시나리오 2: 즉흥적 탐험가**
```json
{
  "buildPlanningTime": 10000,     // 10초 계획
  "buildRevisionCount": 1,         // 거의 수정 안 함
  "explorationRiskTaking": 0.9,   // 위험한 탐험
  "explorationRange": 0.8          // 넓은 탐험
}
```
→ **예상 성격**: Intuition 높음, Fluidity 높음, Logic 낮음

---

### 스타듀밸리 예시

**시나리오 1: 최적화 농부**
```json
{
  "farmPlanningTime": 180000,     // 3분 계획
  "cropDiversity": 0.3,            // 단일 작물 집중
  "optimizationScore": 0.95,       // 높은 최적화
  "dailyRoutineConsistency": 0.9   // 일관된 루틴
}
```
→ **예상 성격**: Logic 높음, Fluidity 높음, Complexity 낮음

**시나리오 2: 다양성 선호자**
```json
{
  "farmPlanningTime": 30000,      // 30초 계획
  "cropDiversity": 0.9,            // 다양한 작물
  "relationshipDepth": 0.8,        // 깊은 관계
  "explorationStyle": 0.7          // 적극적 탐험
}
```
→ **예상 성격**: Complexity 높음, Intuition 높음, Logic 낮음

---

## 🔄 게임 데이터 → 성격 특성 변환

### 변환 알고리즘

```python
def game_behavior_to_personality(game_data: dict) -> dict:
    """
    게임 행동 데이터를 성격 가중치로 변환
    """
    # Logic vs Intuition
    logic_score = (
        (game_data.get('planningTime', 0) / 300000) * 0.4 +  # 계획 시간
        (game_data.get('revisionCount', 0) / 10) * 0.3 +      # 수정 빈도
        (1 - game_data.get('riskTaking', 0.5)) * 0.3          # 위험 회피
    )
    logic_score = min(1.0, max(0.0, logic_score))
    intuition_score = 1.0 - logic_score
    
    # Fluidity
    fluidity_score = (
        game_data.get('pathEfficiency', 0.5) * 0.4 +
        game_data.get('taskEfficiency', 0.5) * 0.3 +
        game_data.get('movementSmoothness', 0.5) * 0.3
    )
    
    # Complexity
    complexity_score = (
        game_data.get('complexity', 0.5) * 0.4 +
        game_data.get('diversity', 0.5) * 0.3 +
        (game_data.get('revisionCount', 0) / 10) * 0.3
    )
    complexity_score = min(1.0, max(0.0, complexity_score))
    
    return {
        'Logic': logic_score,
        'Intuition': intuition_score,
        'Fluidity': fluidity_score,
        'Complexity': complexity_score
    }
```

---

## 📊 게임 데이터 수집 예시

### 실제 수집 가능한 이벤트

**마인크래프트:**
- 블록 배치/제거
- 아이템 선택
- 이동 경로
- 인벤토리 변경
- 전투 행동

**스타듀밸리:**
- 작물 선택/심기
- NPC 대화
- 선물 선택
- 광산 탐험
- 상점 거래

**두근두근타운:**
- 섬 디자인 변경
- NPC 대화
- 선물 선택
- 이벤트 참여
- 자원 수집

---

## 🚀 구현 로드맵

### Phase 1: 데이터 수집 인터페이스 (1주)
- 게임별 이벤트 리스너 구현
- 행동 메트릭 계산
- 로컬 저장

### Phase 2: API 통합 (1주)
- 백엔드 API 엔드포인트 추가
- 게임 데이터 → 행동 프로필 변환
- 성격 가중치 계산

### Phase 3: 게임별 모드 개발 (2-4주)
- 마인크래프트 모드
- 스타듀밸리 모드
- 두근두근타운 모드

### Phase 4: 통합 및 테스트 (1주)
- 게임 데이터 검증
- 성격 추론 정확도 테스트
- 사용자 피드백 수집

---

## 💡 활용 사례

### 1. 게임 내 개인화
- **맞춤형 추천**: 성격에 맞는 게임 요소 추천
- **적응형 난이도**: Logic 높으면 복잡한 퍼즐, Intuition 높으면 빠른 반응 요구
- **개인화된 NPC**: 성격에 맞는 대화 스타일

### 2. 크로스 게임 프로필
- **통합 프로필**: 여러 게임에서 수집한 데이터로 종합 성격 분석
- **게임 추천**: 성격에 맞는 게임 추천
- **진화 추적**: 시간에 따른 성격 변화 추적

### 3. 소셜 기능
- **성격 기반 매칭**: 비슷한 성격의 플레이어 매칭
- **팀 구성**: Logic + Intuition 조합으로 균형잡힌 팀
- **경쟁 분석**: 성격별 플레이 스타일 비교

---

**© 2026 Nexus Entertainment**
