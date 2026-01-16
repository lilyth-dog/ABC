# API Reference

## Neuro-Twin API v2.0.0

Behavioral Digital Human Twin API 문서

---

## Base URL

```
http://localhost:8000
```

프로덕션 환경에서는 환경 변수 `VITE_API_URL`로 설정된 URL을 사용합니다.

---

## 인증

현재 버전에서는 사용자 ID를 통한 식별을 사용합니다. 향후 OAuth2 인증이 추가될 예정입니다.

---

## Rate Limiting

모든 엔드포인트는 Rate Limiting이 적용됩니다:

- Health Check: 100 requests/minute
- 일반 API: 30 requests/minute
- 시뮬레이션: 60 requests/minute

Rate limit 초과 시 `429 Too Many Requests` 응답이 반환됩니다.

---

## 엔드포인트 목록

### Health Check

#### `GET /health`

서버 상태 확인

**Response:**
```json
{
  "status": "ok",
  "controller": "ready"
}
```

---

### Privacy & GDPR

#### `POST /api/user/{user_id}/consent`

사용자 동의 저장

**Request Body:**
```json
{
  "consent_record": {
    "behavioralTracking": true,
    "profileStorage": true,
    "continuousLearning": true
  },
  "timestamp": "2026-01-16T14:00:00Z"
}
```

**Response:**
```json
{
  "status": "saved",
  "user_id": "user123",
  "consent_id": "consent_001"
}
```

#### `GET /api/user/{user_id}/consent`

사용자 동의 조회

**Response:**
```json
{
  "status": "found",
  "user_id": "user123",
  "consent": {
    "behavioralTracking": true,
    "profileStorage": true,
    "continuousLearning": true
  }
}
```

#### `GET /api/user/{user_id}/export`

GDPR 데이터 내보내기

**Response:**
```json
{
  "user_id": "user123",
  "profile": {...},
  "sessions": [...],
  "consents": [...],
  "exported_at": "2026-01-16T14:00:00Z"
}
```

#### `DELETE /api/user/{user_id}`

사용자 데이터 삭제 (GDPR)

**Response:**
```json
{
  "status": "deleted",
  "user_id": "user123",
  "deleted_at": "2026-01-16T14:00:00Z"
}
```

---

### Behavioral Processing

#### `POST /api/behavior`

행동 프로필 처리 및 성격 추론

**Request Body:**
```json
{
  "pathEfficiency": 0.85,
  "avgDecisionLatency": 2500,
  "revisionRate": 2,
  "jitterIndex": 0.15,
  "intensity": 0.7,
  "contextualChoices": {
    "aesthetics": "Cyber/Industrial",
    "user_id": "user123"
  },
  "taskCompletion": 0.9,
  "culturalContext": "east_asian"
}
```

**Response:**
```json
{
  "synthetic_theta": 0.5,
  "synthetic_beta": 0.3,
  "behavioral_traits": {
    "weights": {
      "Logic": 0.6,
      "Intuition": 0.4,
      "Fluidity": 0.7,
      "Complexity": 0.5
    },
    "archetype": "Analytical Explorer"
  },
  "sync_score": 0.85
}
```

---

### Game Data Pipeline

#### `POST /api/game/events`

게임 원시 이벤트 처리 (3단계 파이프라인)

**Request Body:**
```json
{
  "user_id": "user123",
  "game_id": "minecraft",
  "session_id": "session001",
  "raw_events": [
    {
      "type": "inventory_change",
      "timestamp": 1000,
      "items": ["stone", "dirt"]
    },
    {
      "type": "player_move",
      "timestamp": 2000,
      "from": {"x": 0, "y": 64, "z": 0},
      "to": {"x": 10, "y": 64, "z": 10}
    },
    {
      "type": "block_place",
      "timestamp": 3000,
      "position": {"x": 10, "y": 64, "z": 10}
    }
  ]
}
```

**처리 과정:**
1. 원시 이벤트 파싱 및 메트릭 계산
2. 표준 프로필로 변환
3. 성격 추론 및 가중치 업데이트

**Response:**
```json
{
  "session_id": "session001",
  "game_id": "minecraft",
  "parsed_metrics": {
    "planning_time": 2000,
    "revision_count": 1,
    "path_efficiency": 0.85,
    "complexity": 0.7,
    "diversity": 0.6
  },
  "updated_weights": {
    "Logic": 0.6,
    "Intuition": 0.4,
    "Fluidity": 0.7,
    "Complexity": 0.5
  },
  "archetype": "Analytical Explorer",
  "confidence": 0.65,
  "sync_score": 0.85
}
```

#### `POST /api/game/session`

게임 세션 데이터 처리

**Request Body:**
```json
{
  "user_id": "user123",
  "game_id": "minecraft",
  "session_id": "session001",
  "decision_latency": 1500,
  "planning_time": 3000,
  "revision_count": 2,
  "path_efficiency": 0.85,
  "task_efficiency": 0.9,
  "complexity": 0.7,
  "diversity": 0.6,
  "game_specific_metrics": {
    "riskTaking": 0.5,
    "movementSmoothness": 0.8
  }
}
```

**Response:**
```json
{
  "session_id": "session001",
  "updated_weights": {...},
  "archetype": "...",
  "confidence": 0.65,
  "sync_score": 0.85
}
```

**지원 게임:**
- `minecraft`: 마인크래프트
- `stardew_valley`: 스타듀밸리
- `animal_crossing`: 두근두근타운

---

### Session Management

#### `POST /api/session`

세션 저장 및 학습

**Request Body:**
```json
{
  "user_id": "user123",
  "behavioral_profile": {
    "pathEfficiency": 0.85,
    "avgDecisionLatency": 2500,
    ...
  }
}
```

**Response:**
```json
{
  "session_id": "session001",
  "weights": {...},
  "archetype": "...",
  "confidence": 0.65
}
```

---

### Profile & Insights

#### `GET /api/profile/{user_id}`

사용자 프로필 조회

**Response:**
```json
{
  "user_id": "user123",
  "weights": {...},
  "archetype": "...",
  "confidence": 0.65,
  "maturity_level": 1
}
```

#### `GET /api/insights/{user_id}`

예측 인사이트 조회

**Response:**
```json
{
  "behavioral_trends": {...},
  "stress_detection": {...},
  "anomaly_detection": {...},
  "personality_evolution": {...}
}
```

#### `GET /api/evolution/{user_id}`

성격 진화 히스토리

**Response:**
```json
{
  "history": [
    {
      "timestamp": "2026-01-16T14:00:00Z",
      "weights": {...},
      "archetype": "...",
      "confidence": 0.65
    },
    ...
  ]
}
```

---

### Simulation

#### `POST /api/simulate`

단일 시뮬레이션 요청

**Request Body:**
```json
{
  "theta": 0.7,
  "beta": 0.3,
  "action": "walk"
}
```

**Response:**
```json
{
  "kinematics": {
    "positions": [...],
    "velocities": [...],
    "accelerations": [...]
  }
}
```

#### `GET /api/behavior/sample/{emotion}`

감정별 샘플 행동 프로필

**Path Parameters:**
- `emotion`: `happy`, `sad`, `angry`, `fear`, `surprise`, `neutral`

**Response:**
```json
{
  "profile": {...},
  "motion_modifiers": {...},
  "sample_info": {
    "actor": "...",
    "emotion": "happy",
    "word": "..."
  },
  "audio_metrics": {...}
}
```

---

### WebSocket

#### `WS /ws/simulation`

실시간 시뮬레이션 스트리밍

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/simulation');
```

**Send:**
```json
{
  "theta": 0.7,
  "beta": 0.3
}
```

**Receive:**
```json
{
  "kinematics": {
    "positions": [...],
    "velocities": [...],
    "accelerations": [...]
  },
  "timestamp": 1234567890
}
```

#### `WS /ws/stream`

자동 스트리밍 (30 FPS)

연결 시 자동으로 30 FPS로 시뮬레이션 데이터를 스트리밍합니다.

---

## 에러 응답

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## API 문서

실시간 API 문서는 다음 URL에서 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 예제 코드

### Python

```python
import requests

# 게임 이벤트 처리
response = requests.post(
    "http://localhost:8000/api/game/events",
    json={
        "user_id": "user123",
        "game_id": "minecraft",
        "session_id": "session001",
        "raw_events": [...]
    }
)
result = response.json()
print(result["updated_weights"])
```

### JavaScript

```javascript
// 게임 이벤트 처리
const response = await fetch('http://localhost:8000/api/game/events', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'user123',
    game_id: 'minecraft',
    session_id: 'session001',
    raw_events: [...]
  })
});
const result = await response.json();
console.log(result.updated_weights);
```

---

## 버전 정보

- **API Version**: 2.0.0
- **Last Updated**: 2026-01-16
- **Status**: Production Ready (95%)

---

## 참고 자료

- [개발자 가이드](DEVELOPER_GUIDE.md)
- [최종 검증 리포트](FINAL_VERIFICATION_REPORT.md)
- [프로젝트 구조](../README.md)
