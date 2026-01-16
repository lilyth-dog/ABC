# 언리얼 엔진 행동 수집 및 평가 시스템

## 개요

이 시스템은 사용자의 상호작용 패턴(마우스 움직임, 클릭, 의사결정 시간 등)을 수집하여 성격 특성을 추론하기 위한 데이터를 제공합니다.

## 파일 구조

- `BehaviorTracker.h/cpp`: 핵심 행동 추적 클래스
- `BehaviorTrackerComponent.h/cpp`: 액터 컴포넌트로 자동 추적
- `BehaviorEvaluator.h/cpp`: 수집된 데이터를 평가하여 성격 가중치 계산

## 사용 방법

### 1. 기본 사용 (C++)

```cpp
// BehaviorTracker 생성
UBehaviorTracker* Tracker = NewObject<UBehaviorTracker>(this);

// 세션 시작
Tracker->StartSession();

// 마우스 움직임 추적
FVector2D MousePos(100.0f, 200.0f);
Tracker->TrackMovement(MousePos);

// 클릭 기록
Tracker->RecordClick();

// 의사결정 단계 시작
Tracker->StartDecisionStep();
// ... 사용자가 선택하는 시간 ...
// 의사결정 완료
Tracker->RecordStepCompletion();

// 프로필 가져오기
FBehavioralProfile Profile = Tracker->GetBehavioralProfile();
```

### 2. 컴포넌트로 사용

```cpp
// 액터에 컴포넌트 추가
UBehaviorTrackerComponent* TrackerComponent = 
    NewObject<UBehaviorTrackerComponent>(this);
TrackerComponent->RegisterComponent();

// 자동 추적 시작
TrackerComponent->StartTracking();

// 프로필 가져오기
FBehavioralProfile Profile = TrackerComponent->GetProfile();
```

### 3. 블루프린트 사용

1. 액터나 위젯에 `BehaviorTrackerComponent` 추가
2. "Start Tracking" 노드 호출
3. "Get Profile" 노드로 프로필 가져오기

### 4. 평가 시스템 사용

```cpp
// BehaviorEvaluator 생성
UBehaviorEvaluator* Evaluator = NewObject<UBehaviorEvaluator>(this);

// 행동 프로필 평가
FBehaviorEvaluationResult Result = 
    Evaluator->EvaluateBehavior(Profile, SessionCount);

// 성격 가중치 접근
float LogicWeight = Result.PersonalityWeights.Logic;
float Confidence = Result.ConfidenceScore;
```

## 수집되는 데이터

### FInteractionMetrics
- `MousePathLength`: 마우스 이동 경로 총 길이
- `ClickCount`: 클릭 횟수
- `DecisionLatencies`: 의사결정 지연시간 배열
- `RevisionCount`: 값 수정 횟수
- `VelocityPeaks`: 빠른 움직임 속도 피크
- `JitterSum`: 지터(작은 움직임) 합계

### FBehavioralProfile (계산된 결과)
- `PathEfficiency`: 경로 효율성 (픽셀/ms)
- `AvgDecisionLatency`: 평균 의사결정 지연시간 (ms)
- `RevisionRate`: 수정 빈도
- `JitterIndex`: 지터 지수
- `Intensity`: 상호작용 강도

## 백엔드 연동

### ML 모델 호출

```cpp
// BehaviorEvaluator를 사용하여 백엔드 API 호출
FString APIEndpoint = TEXT("http://localhost:8000/api/predict");
Evaluator->EvaluateWithML(Profile, APIEndpoint);
```

백엔드 API는 다음 형식의 JSON을 받습니다:
```json
{
    "latency": 2500.0,
    "revisions": 3,
    "efficiency": 0.85,
    "intensity": 2.5
}
```

## 설정 가능한 파라미터

- `FastMovementThreshold`: 빠른 움직임 임계값 (기본: 5.0 픽셀/ms)
- `JitterThreshold`: 지터 감지 임계값 (기본: 10.0 픽셀)
- `bAutoStart`: 컴포넌트 시작 시 자동 추적 (기본: true)
- `bAutoTrackMouse`: 마우스 자동 추적 (기본: true)
- `bAutoTrackClicks`: 클릭 자동 추적 (기본: true)

## 주의사항

1. **성능**: Tick에서 마우스 위치를 추적하므로 성능에 영향을 줄 수 있습니다. 필요시 추적 빈도를 조절하세요.

2. **입력 시스템**: 실제 프로젝트의 입력 시스템에 맞게 `BehaviorTrackerComponent`의 입력 바인딩을 수정해야 할 수 있습니다.

3. **좌표계**: 마우스 위치는 화면 좌표계를 사용합니다. 필요시 월드 좌표로 변환하세요.

4. **네트워크**: ML 모델 호출은 비동기로 처리되므로 결과를 받기 위해 델리게이트나 이벤트를 사용하세요.

## 논문과의 연관성

이 코드는 논문의 다음 섹션과 직접적으로 연관됩니다:

- **3.3 특징 추출 및 엔지니어링**: 행동 신호 수집
- **3.4 성격 추론 모델**: ML 모델 호출 및 규칙 기반 폴백
- **4.2 데이터 수집 및 전처리**: 실제 데이터 수집 파이프라인
