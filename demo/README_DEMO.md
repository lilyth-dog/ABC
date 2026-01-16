# 시연용 결과물 가이드

## 📁 파일 구조

```
demo/
├── sample_user_profile.json          # 샘플 사용자 프로필 데이터
├── api_response_example.json         # API 응답 예시
├── generate_demo_charts.py          # 차트 생성 스크립트
├── README_DEMO.md                   # 이 파일
└── (생성된 차트 파일들)
    ├── demo_confidence_growth.png
    ├── demo_personality_evolution.png
    ├── demo_radar_prediction.png
    ├── demo_behavioral_trends.png
    └── demo_summary_report.md
```

## 🚀 빠른 시작

### 1. 차트 생성

```bash
cd demo
python generate_demo_charts.py
```

**필수 패키지:**
```bash
pip install matplotlib numpy
```

**Windows 한글 폰트 설정:**
- 기본적으로 'Malgun Gothic' 사용
- 다른 폰트 사용 시 `generate_demo_charts.py`의 `plt.rcParams['font.family']` 수정

### 2. 생성되는 파일

- `demo_confidence_growth.png`: 세션별 신뢰도 증가 그래프
- `demo_personality_evolution.png`: 성격 가중치 진화 그래프
- `demo_radar_prediction.png`: 현재 vs 30일 후 예측 레이더 차트
- `demo_behavioral_trends.png`: 행동 트렌드 영역 차트
- `demo_summary_report.md`: 시연용 요약 리포트

## 📊 시연 시나리오

### 시나리오 1: 신뢰도 성장 (30초)

**발표 스크립트:**
> "시스템은 사용자가 여러 세션을 진행할수록 더 정확한 성격 프로필을 학습합니다. 
> 세션 1에서는 30%의 신뢰도로 시작했지만, 세션 7에서는 82%까지 증가했습니다.
> 이는 지속적 학습 알고리즘(EMA)이 점진적으로 모델을 개선하기 때문입니다."

**사용 파일:** `demo_confidence_growth.png`

### 시나리오 2: 성격 진화 (30초)

**발표 스크립트:**
> "성격 가중치는 시간에 따라 변화합니다. 이 사용자의 경우, Logic 가중치가 
> 0.45에서 0.65로 증가한 반면, Intuition은 0.55에서 0.35로 감소했습니다.
> 이는 사용자가 더 분석적이고 신중한 의사결정 패턴을 보이기 시작했다는 것을 의미합니다."

**사용 파일:** `demo_personality_evolution.png`

### 시나리오 3: 미래 예측 (30초)

**발표 스크립트:**
> "머신러닝 모델을 사용하여 30일 후의 성격 진화를 예측합니다. 레이더 차트에서 
> 보시는 바와 같이, Logic은 계속 증가하고, Intuition은 감소하는 추세입니다.
> 이러한 예측은 시계열 분석과 선형 회귀를 통해 계산됩니다."

**사용 파일:** `demo_radar_prediction.png`

### 시나리오 4: 행동 분석 (30초)

**발표 스크립트:**
> "행동 트렌드를 분석하면, 의사결정 지연시간이 증가하고, 경로 효율성도 
> 개선되었습니다. 수정 빈도도 증가했는데, 이는 사용자가 더 신중하게 
> 선택을 검토한다는 의미입니다."

**사용 파일:** `demo_behavioral_trends.png`

## 📝 API 응답 예시

### 세션 저장 응답

```json
{
  "session_id": "sess_20260114_140000",
  "updated_weights": {
    "Logic": 0.58,
    "Intuition": 0.42,
    "Fluidity": 0.75,
    "Complexity": 0.62
  },
  "confidence": 0.70,
  "ml_model_used": true
}
```

### 예측 인사이트 응답

```json
{
  "stress_analysis": {
    "stress_level": 0.3,
    "category": "low"
  },
  "behavior_trend": {
    "Logic": {
      "current": 0.65,
      "predicted": 0.72,
      "trend": "increasing"
    }
  }
}
```

## 🎯 발표 시 활용 방법

### Option 1: 실제 시스템 데모
1. 백엔드 실행: `python backend/api_server.py`
2. 프론트엔드 실행: `npm run dev`
3. `sample_user_profile.json` 데이터를 사용하여 시연

### Option 2: 스크린샷/차트 사용
1. 생성된 차트 이미지를 PowerPoint에 삽입
2. 각 차트에 대한 설명 추가
3. 시연 시나리오에 따라 순서대로 설명

### Option 3: API 응답 예시
1. `api_response_example.json`을 사용하여 API 구조 설명
2. 실제 API 호출 대신 예시 데이터로 설명

## 🔧 커스터마이징

### 샘플 데이터 수정

`sample_user_profile.json`을 수정하여 다른 시나리오를 만들 수 있습니다:

```json
{
  "sessions": [
    {
      "session": 1,
      "personality_weights": {
        "Logic": 0.30,  // 직관적 사용자
        "Intuition": 0.70
      }
    }
  ]
}
```

### 차트 스타일 변경

`generate_demo_charts.py`에서 색상, 크기, 폰트 등을 수정할 수 있습니다:

```python
plt.plot(sessions, confidence, color='#your_color')
plt.figure(figsize=(12, 8))  # 크기 조정
```

## 📌 체크리스트

시연 전 확인:
- [ ] 차트 생성 완료
- [ ] 샘플 데이터 확인
- [ ] API 응답 예시 확인
- [ ] 발표 스크립트 숙지
- [ ] 백업 스크린샷 준비

## 💡 팁

1. **차트는 고해상도로 저장**: `dpi=300`으로 저장하여 발표 시 선명하게 보이도록
2. **색상 일관성**: 모든 차트에서 동일한 색상 팔레트 사용
3. **간결한 설명**: 각 차트마다 핵심 포인트만 1-2문장으로 설명
4. **시간 관리**: 각 시나리오는 30초 이내로 제한

---

**© 2026 Nexus Entertainment**
