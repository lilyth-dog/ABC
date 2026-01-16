# 언리얼 엔진 행동 추적 시스템 테스트 가이드

## ⚠️ 중요: 실제 테스트를 위한 설정 필요

현재 코드는 **기본 구조만 제공**합니다. 실제 언리얼 엔진 프로젝트에서 테스트하려면 다음 설정이 필요합니다:

## 1. 프로젝트 구조 설정

### 필수 파일 구조:
```
YourProject/
├── Source/
│   └── DigitalHumanTwin/
│       ├── DigitalHumanTwin.Build.cs
│       ├── DigitalHumanTwin.h
│       ├── DigitalHumanTwin.cpp
│       ├── BehaviorTracker.h
│       ├── BehaviorTracker.cpp
│       ├── BehaviorTrackerComponent.h
│       ├── BehaviorTrackerComponent.cpp
│       ├── BehaviorEvaluator.h
│       └── BehaviorEvaluator.cpp
```

### .uproject 파일에 모듈 추가:
```json
{
    "FileVersion": 3,
    "EngineAssociation": "5.3",
    "Category": "",
    "Description": "",
    "Modules": [
        {
            "Name": "DigitalHumanTwin",
            "Type": "Runtime",
            "LoadingPhase": "Default"
        }
    ]
}
```

## 2. 컴파일 가능 여부 확인

### 현재 코드의 제한사항:

1. **API 매크로**: `DIGITALHUMANTWIN_API`는 모듈이 제대로 설정되면 자동으로 정의됩니다.
   - ✅ 해결: `DigitalHumanTwin.h`에 매크로 정의 추가

2. **HTTP 모듈 의존성**: 
   - ✅ 해결: `DigitalHumanTwin.Build.cs`에 HTTP 모듈 추가

3. **Slate 애플리케이션**: 
   - ⚠️ 문제: 런타임에서는 사용 불가
   - ✅ 해결: 플레이어 컨트롤러의 `GetMousePosition()` 사용하도록 수정

4. **입력 바인딩**:
   - ⚠️ 미완성: `SetupInputBindings()` 함수가 비어있음
   - 실제 프로젝트의 입력 시스템에 맞게 구현 필요

## 3. 실제 테스트 방법

### 방법 1: 간단한 테스트 액터 생성

```cpp
// TestBehaviorTrackerActor.h
UCLASS()
class DIGITALHUMANTWIN_API ATestBehaviorTrackerActor : public AActor
{
    GENERATED_BODY()

public:
    ATestBehaviorTrackerActor();

    UPROPERTY(VisibleAnywhere)
    UBehaviorTrackerComponent* TrackerComponent;

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;
};

// TestBehaviorTrackerActor.cpp
ATestBehaviorTrackerActor::ATestBehaviorTrackerActor()
{
    PrimaryActorTick.bCanEverTick = true;
    
    TrackerComponent = CreateDefaultSubobject<UBehaviorTrackerComponent>(TEXT("TrackerComponent"));
}

void ATestBehaviorTrackerActor::BeginPlay()
{
    Super::BeginPlay();
    TrackerComponent->StartTracking();
}

void ATestBehaviorTrackerActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);
    
    // 테스트: 주기적으로 프로필 출력
    static float Timer = 0.0f;
    Timer += DeltaTime;
    if (Timer > 5.0f)
    {
        FBehavioralProfile Profile = TrackerComponent->GetProfile();
        UE_LOG(LogTemp, Warning, TEXT("Path Efficiency: %f"), Profile.PathEfficiency);
        Timer = 0.0f;
    }
}
```

### 방법 2: 블루프린트 테스트

1. C++ 클래스 생성: `ATestBehaviorTrackerActor`
2. 블루프린트로 변환
3. 월드에 배치
4. 게임 실행 후 로그 확인

## 4. 현재 코드의 실제 동작 가능 여부

### ✅ 동작 가능한 부분:
- `BehaviorTracker` 기본 기능 (C++ 코드 자체는 정상)
- 데이터 수집 로직
- 프로필 계산

### ⚠️ 추가 작업 필요한 부분:
- **입력 바인딩**: 실제 입력 시스템과 연동 필요
- **마우스 추적**: 런타임에서 플레이어 컨트롤러 사용하도록 수정됨
- **HTTP 요청**: 백엔드 API 엔드포인트 확인 필요

### ❌ 테스트 불가능한 부분:
- **Slate 기반 마우스 추적**: 에디터에서만 동작
- **자동 클릭 감지**: 입력 바인딩 구현 필요

## 5. 빠른 테스트를 위한 최소 구현

### 최소 테스트 코드:

```cpp
// 간단한 수동 테스트
void TestBehaviorTracker()
{
    UBehaviorTracker* Tracker = NewObject<UBehaviorTracker>();
    Tracker->StartSession();
    
    // 수동으로 데이터 입력
    Tracker->TrackMovement(FVector2D(100, 200));
    Tracker->TrackMovement(FVector2D(150, 250));
    Tracker->RecordClick();
    Tracker->StartDecisionStep();
    // ... 시간 경과 ...
    Tracker->RecordStepCompletion();
    
    // 결과 확인
    FBehavioralProfile Profile = Tracker->GetBehavioralProfile();
    UE_LOG(LogTemp, Warning, TEXT("Profile - Latency: %f, Revisions: %d"), 
        Profile.AvgDecisionLatency, Profile.RevisionRate);
}
```

## 결론

**현재 상태**: 코드 구조는 완성되었으나, **실제 언리얼 엔진 프로젝트에 통합하고 컴파일해야 테스트 가능**합니다.

**즉시 테스트 가능한 부분**:
- ✅ `BehaviorTracker`의 수동 데이터 입력/계산
- ✅ `BehaviorEvaluator`의 규칙 기반 평가

**추가 작업 후 테스트 가능**:
- ⚠️ 자동 마우스 추적 (입력 바인딩 구현 필요)
- ⚠️ 백엔드 API 연동 (엔드포인트 확인 필요)

**권장 사항**: 
1. 먼저 간단한 테스트 액터로 수동 데이터 입력 테스트
2. 입력 시스템 연동 후 자동 추적 테스트
3. 백엔드 API 연동 테스트
