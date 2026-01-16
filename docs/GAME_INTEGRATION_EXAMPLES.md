# 게임 통합 예시 코드
## 실제 게임에서 행동 데이터 수집 및 전송

---

## 🎮 마인크래프트 모드 예시

### Forge 모드 (Java)

```java
// BehaviorTrackerMod.java
package com.nexus.behaviortracker;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.world.BlockEvent;

import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

@Mod("behaviortracker")
public class BehaviorTrackerMod {
    private long buildStartTime = 0;
    private int revisionCount = 0;
    private List<BlockPos> buildPath = new ArrayList<>();
    private Map<String, Object> gameMetrics = new HashMap<>();
    
    public BehaviorTrackerMod() {
        MinecraftForge.EVENT_BUS.register(this);
    }
    
    @SubscribeEvent
    public void onBlockPlace(BlockEvent.PlaceEvent event) {
        if (buildStartTime == 0) {
            buildStartTime = System.currentTimeMillis();
        }
        
        buildPath.add(event.getPos());
        
        // 수정 빈도 계산 (블록 제거 후 재배치)
        if (wasRemovedRecently(event.getPos())) {
            revisionCount++;
        }
    }
    
    @SubscribeEvent
    public void onPlayerMove(PlayerEvent event) {
        // 탐험 패턴 기록
        recordExplorationPattern(event.getPlayer().getPosition());
    }
    
    public void sendBehavioralData() {
        long planningTime = System.currentTimeMillis() - buildStartTime;
        double pathEfficiency = calculatePathEfficiency(buildPath);
        double complexity = calculateBuildComplexity(buildPath);
        
        Map<String, Object> data = new HashMap<>();
        data.put("game_id", "minecraft");
        data.put("session_id", generateSessionId());
        data.put("decision_latency", 0); // 마인크래프트는 실시간이므로 0
        data.put("planning_time", planningTime);
        data.put("revision_count", revisionCount);
        data.put("path_efficiency", pathEfficiency);
        data.put("task_efficiency", 0.7); // 기본값
        data.put("complexity", complexity);
        data.put("diversity", calculateResourceDiversity());
        
        // 게임별 특화 메트릭
        Map<String, Object> gameSpecific = new HashMap<>();
        gameSpecific.put("buildComplexity", complexity);
        gameSpecific.put("explorationRange", calculateExplorationRange());
        gameSpecific.put("resourceDiversity", calculateResourceDiversity());
        gameSpecific.put("riskTaking", calculateRiskTaking());
        data.put("game_specific_metrics", gameSpecific);
        
        // API로 전송
        sendToAPI(data);
    }
    
    private void sendToAPI(Map<String, Object> data) {
        // HTTP POST 요청으로 백엔드 API에 전송
        // 실제 구현은 HTTP 클라이언트 라이브러리 사용
    }
}
```

---

## 🌾 스타듀밸리 모드 예시

### SMAPI 모드 (C#)

```csharp
// BehaviorTrackerMod.cs
using StardewModdingAPI;
using StardewModdingAPI.Events;
using System;
using System.Collections.Generic;
using System.Linq;

namespace BehaviorTracker
{
    public class BehaviorTrackerMod : Mod
    {
        private Dictionary<string, long> decisionTimes;
        private List<string> cropSelections;
        private long dayStartTime;
        
        public override void Entry(IModHelper helper)
        {
            decisionTimes = new Dictionary<string, long>();
            cropSelections = new List<string>();
            
            helper.Events.Input.ButtonPressed += OnButtonPressed;
            helper.Events.GameLoop.DayStarted += OnDayStarted;
            helper.Events.GameLoop.DayEnding += OnDayEnding;
        }
        
        private void OnButtonPressed(object sender, ButtonPressedEventArgs e)
        {
            // 작물 선택 시 의사결정 시간 기록
            if (IsCropSelection(e.Button))
            {
                long decisionTime = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
                decisionTimes[e.Button.ToString()] = decisionTime;
            }
        }
        
        private void OnDayStarted(object sender, DayStartedEventArgs e)
        {
            dayStartTime = DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond;
        }
        
        private void OnDayEnding(object sender, DayEndingEventArgs e)
        {
            long planningTime = (DateTime.Now.Ticks / TimeSpan.TicksPerMillisecond) - dayStartTime;
            int cropDiversity = cropSelections.Distinct().Count();
            
            var data = new
            {
                game_id = "stardew_valley",
                session_id = Guid.NewGuid().ToString(),
                decision_latency = CalculateAverageDecisionLatency(),
                planning_time = planningTime,
                revision_count = CountRevisions(),
                path_efficiency = 0.7, // 기본값
                task_efficiency = CalculateTaskEfficiency(),
                complexity = CalculateFarmComplexity(),
                diversity = cropDiversity / 10.0, // 정규화
                game_specific_metrics = new
                {
                    cropDiversity = cropDiversity / 10.0,
                    farmOptimization = CalculateOptimizationScore(),
                    relationshipDepth = CalculateRelationshipDepth()
                }
            };
            
            SendToAPI(data);
        }
        
        private void SendToAPI(object data)
        {
            // HTTP POST 요청으로 백엔드 API에 전송
            // 실제 구현은 HttpClient 사용
        }
    }
}
```

---

## 🏝️ 두근두근타운 (Animal Crossing) 데이터 수집

### 게임 로그 분석 방식

```python
# animal_crossing_tracker.py
import json
import time
from typing import Dict, List

class AnimalCrossingTracker:
    """두근두근타운 게임 로그를 분석하여 행동 데이터 추출"""
    
    def __init__(self):
        self.island_changes = []
        self.npc_interactions = []
        self.design_times = {}
    
    def analyze_game_log(self, log_file: str) -> Dict:
        """게임 로그 파일 분석"""
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        # 섬 디자인 변경 추적
        design_changes = [log for log in logs if log['type'] == 'island_design']
        planning_time = self._calculate_planning_time(design_changes)
        revision_count = self._count_revisions(design_changes)
        
        # NPC 상호작용 분석
        npc_logs = [log for log in logs if log['type'] == 'npc_interaction']
        interaction_depth = self._calculate_interaction_depth(npc_logs)
        
        return {
            "game_id": "animal_crossing",
            "session_id": f"ac_{int(time.time())}",
            "decision_latency": self._calculate_decision_latency(logs),
            "planning_time": planning_time,
            "revision_count": revision_count,
            "path_efficiency": 0.7,  # 기본값
            "task_efficiency": self._calculate_task_efficiency(logs),
            "complexity": self._calculate_island_complexity(design_changes),
            "diversity": self._calculate_collection_diversity(logs),
            "game_specific_metrics": {
                "islandComplexity": self._calculate_island_complexity(design_changes),
                "npcInteractionDepth": interaction_depth,
                "designConsistency": self._calculate_design_consistency(design_changes)
            }
        }
    
    def send_to_api(self, data: Dict):
        """백엔드 API로 전송"""
        import requests
        
        response = requests.post(
            'http://localhost:8000/api/game/session',
            json={
                "user_id": "user_123",
                **data
            }
        )
        
        return response.json()
```

---

## 📡 클라이언트 → 백엔드 통신

### JavaScript/TypeScript 예시

```typescript
// gameClient.ts
interface GameBehavioralData {
  game_id: string;
  session_id: string;
  decision_latency: number;
  planning_time: number;
  revision_count: number;
  path_efficiency: number;
  task_efficiency: number;
  complexity: number;
  diversity: number;
  game_specific_metrics: Record<string, any>;
}

class GameBehaviorClient {
  private apiUrl = 'http://localhost:8000/api/game/session';
  
  async sendGameData(
    userId: string,
    gameData: GameBehavioralData
  ): Promise<any> {
    const response = await fetch(this.apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        ...gameData
      }),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }
    
    const result = await response.json();
    
    // 성격 가중치 반환
    return {
      personalityWeights: result.updated_weights,
      archetype: result.archetype,
      confidence: result.confidence
    };
  }
}

// 사용 예시
const client = new GameBehaviorClient();

// 마인크래프트 데이터 전송
await client.sendGameData('user_123', {
  game_id: 'minecraft',
  session_id: 'mc_session_001',
  decision_latency: 0,
  planning_time: 300000,  // 5분
  revision_count: 5,
  path_efficiency: 0.75,
  task_efficiency: 0.8,
  complexity: 0.9,
  diversity: 0.6,
  game_specific_metrics: {
    buildComplexity: 0.9,
    explorationRange: 0.7,
    resourceDiversity: 0.6,
    riskTaking: 0.3
  }
});
```

---

## 🎯 게임별 데이터 수집 전략

### 1. 마인크래프트
- **모드 개발**: Forge/Fabric 모드로 이벤트 리스너 구현
- **수집 데이터**: 블록 배치, 이동 경로, 인벤토리 변경
- **특화 메트릭**: 건축 복잡도, 탐험 범위, 위험 선호도

### 2. 스타듀밸리
- **모드 개발**: SMAPI 모드로 게임 이벤트 후킹
- **수집 데이터**: 작물 선택, NPC 대화, 농장 관리
- **특화 메트릭**: 작물 다양성, 농장 최적화, 관계 깊이

### 3. 두근두근타운
- **로그 분석**: 게임 로그 파일 분석
- **수집 데이터**: 섬 디자인, NPC 상호작용, 이벤트 참여
- **특화 메트릭**: 섬 복잡도, NPC 상호작용 깊이, 디자인 일관성

---

## 🔄 통합 워크플로우

```
게임 플레이
    ↓
행동 데이터 수집 (게임 모드/로그)
    ↓
로컬 처리 및 정규화
    ↓
백엔드 API 전송 (/api/game/session)
    ↓
게임 데이터 → 표준 행동 프로필 변환
    ↓
ML 모델로 성격 가중치 추론
    ↓
지속적 학습 (EMA 업데이트)
    ↓
결과 반환 (성격 가중치, 아키타입, 신뢰도)
```

---

## 💡 활용 사례

### 1. 크로스 게임 프로필
여러 게임에서 수집한 데이터를 통합하여 종합 성격 프로필 생성

### 2. 게임 추천
성격에 맞는 게임 추천 (Logic 높으면 전략 게임, Intuition 높으면 액션 게임)

### 3. 적응형 게임플레이
성격에 맞춰 게임 난이도나 콘텐츠 조정

---

**© 2026 Nexus Entertainment**
