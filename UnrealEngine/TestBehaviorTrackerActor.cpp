// TestBehaviorTrackerActor.cpp
// 행동 추적 시스템 테스트 액터 구현

#include "TestBehaviorTrackerActor.h"
#include "Engine/Engine.h"

ATestBehaviorTrackerActor::ATestBehaviorTrackerActor()
{
    PrimaryActorTick.bCanEverTick = true;

    // 컴포넌트 생성
    TrackerComponent = CreateDefaultSubobject<UBehaviorTrackerComponent>(TEXT("TrackerComponent"));
    
    // 평가기 생성
    Evaluator = NewObject<UBehaviorEvaluator>(this);
}

void ATestBehaviorTrackerActor::BeginPlay()
{
    Super::BeginPlay();
    
    // 추적 시작
    if (TrackerComponent)
    {
        TrackerComponent->StartTracking();
        UE_LOG(LogTemp, Log, TEXT("Behavior Tracker: Tracking started"));
    }
}

void ATestBehaviorTrackerActor::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    if (!TrackerComponent)
    {
        return;
    }

    // 시뮬레이션된 마우스 움직임
    if (bSimulateMouseMovement)
    {
        SimulateMouseMovement(DeltaTime);
    }

    // 주기적으로 프로필 출력
    ProfilePrintTimer += DeltaTime;
    if (ProfilePrintTimer >= ProfilePrintInterval)
    {
        ProfilePrintTimer = 0.0f;

        // 프로필 가져오기
        FBehavioralProfile Profile = TrackerComponent->GetProfile();

        if (bPrintProfileToLog)
        {
            UE_LOG(LogTemp, Warning, TEXT("=== Behavior Profile ==="));
            UE_LOG(LogTemp, Warning, TEXT("Path Efficiency: %.2f"), Profile.PathEfficiency);
            UE_LOG(LogTemp, Warning, TEXT("Avg Decision Latency: %.2f ms"), Profile.AvgDecisionLatency);
            UE_LOG(LogTemp, Warning, TEXT("Revision Rate: %d"), Profile.RevisionRate);
            UE_LOG(LogTemp, Warning, TEXT("Jitter Index: %.4f"), Profile.JitterIndex);
            UE_LOG(LogTemp, Warning, TEXT("Intensity: %.2f"), Profile.Intensity);
        }

        // 평가 수행
        if (Evaluator)
        {
            FBehaviorEvaluationResult Result = Evaluator->EvaluateBehavior(Profile, SessionCount);
            
            if (bPrintProfileToLog)
            {
                UE_LOG(LogTemp, Warning, TEXT("=== Personality Weights ==="));
                UE_LOG(LogTemp, Warning, TEXT("Logic: %.2f"), Result.PersonalityWeights.Logic);
                UE_LOG(LogTemp, Warning, TEXT("Intuition: %.2f"), Result.PersonalityWeights.Intuition);
                UE_LOG(LogTemp, Warning, TEXT("Fluidity: %.2f"), Result.PersonalityWeights.Fluidity);
                UE_LOG(LogTemp, Warning, TEXT("Complexity: %.2f"), Result.PersonalityWeights.Complexity);
                UE_LOG(LogTemp, Warning, TEXT("Confidence: %.2f"), Result.ConfidenceScore);
                UE_LOG(LogTemp, Warning, TEXT("Reasoning: %s"), *Result.Reasoning);
            }
        }
    }
}

void ATestBehaviorTrackerActor::SimulateMouseMovement(float DeltaTime)
{
    // 간단한 원형 움직임 시뮬레이션
    static float Angle = 0.0f;
    Angle += DeltaTime * 2.0f; // 2 rad/s

    SimulatedMouseX = 400.0f + FMath::Cos(Angle) * 200.0f;
    SimulatedMouseY = 300.0f + FMath::Sin(Angle) * 200.0f;

    if (TrackerComponent && TrackerComponent->GetTracker())
    {
        TrackerComponent->GetTracker()->TrackMovement(FVector2D(SimulatedMouseX, SimulatedMouseY));
    }
}
