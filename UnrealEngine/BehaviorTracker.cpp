// BehaviorTracker.cpp
// 언리얼 엔진용 행동 수집 및 평가 시스템 구현

#include "BehaviorTracker.h"
#include "Engine/Engine.h"
#include "HAL/PlatformTime.h"

UBehaviorTracker::UBehaviorTracker(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer)
    , FastMovementThreshold(5.0f)
    , JitterThreshold(10.0f)
{
    StartSession();
}

void UBehaviorTracker::StartSession()
{
    Metrics = FInteractionMetrics();
    Metrics.SessionStartTime = GetCurrentTime();
    Metrics.StepStartTime = GetCurrentTime();
    Metrics.LastMoveTime = GetCurrentTime();
    LastPosition = FVector2D::ZeroVector;
}

void UBehaviorTracker::TrackMovement(const FVector2D& MousePosition)
{
    const float CurrentTime = GetCurrentTime();
    
    if (LastPosition != FVector2D::ZeroVector)
    {
        // 거리 계산
        const float Distance = CalculateDistance(LastPosition, MousePosition);
        const float DeltaTime = CurrentTime - Metrics.LastMoveTime;
        
        if (DeltaTime > 0.0f)
        {
            // 경로 길이 누적
            Metrics.MousePathLength += Distance;
            
            // 속도 계산 (픽셀/ms)
            const float Velocity = Distance / DeltaTime;
            
            // 빠른 움직임 감지
            if (Velocity > FastMovementThreshold)
            {
                Metrics.VelocityPeaks.Add(Velocity);
            }
            
            // 지터 감지 (작고 빈번한 움직임)
            if (Distance > 0.0f && Distance < JitterThreshold)
            {
                Metrics.JitterSum += 1.0f;
            }
        }
    }
    
    LastPosition = MousePosition;
    Metrics.LastMousePosition = MousePosition;
    Metrics.LastMoveTime = CurrentTime;
}

void UBehaviorTracker::RecordClick()
{
    Metrics.ClickCount++;
}

void UBehaviorTracker::StartDecisionStep()
{
    Metrics.StepStartTime = GetCurrentTime();
}

void UBehaviorTracker::RecordStepCompletion()
{
    const float CurrentTime = GetCurrentTime();
    const float Latency = CurrentTime - Metrics.StepStartTime;
    
    if (Latency > 0.0f)
    {
        Metrics.DecisionLatencies.Add(Latency);
    }
    
    // 다음 단계를 위한 초기화
    Metrics.StepStartTime = CurrentTime;
}

void UBehaviorTracker::RecordRevision()
{
    Metrics.RevisionCount++;
}

void UBehaviorTracker::RecordChoice(const FString& Key, const FString& Value)
{
    Metrics.ContextualChoices.Add(Key, Value);
}

FBehavioralProfile UBehaviorTracker::GetBehavioralProfile() const
{
    FBehavioralProfile Profile;
    
    const float TotalTime = GetCurrentTime() - Metrics.SessionStartTime;
    
    // 경로 효율성 계산
    // 실제 경로 길이를 시간으로 나눈 값 (픽셀/ms)
    if (TotalTime > 0.0f)
    {
        Profile.PathEfficiency = Metrics.MousePathLength / TotalTime;
    }
    
    // 평균 의사결정 지연시간
    if (Metrics.DecisionLatencies.Num() > 0)
    {
        float Sum = 0.0f;
        for (float Latency : Metrics.DecisionLatencies)
        {
            Sum += Latency;
        }
        Profile.AvgDecisionLatency = Sum / Metrics.DecisionLatencies.Num();
    }
    
    // 수정 빈도
    Profile.RevisionRate = Metrics.RevisionCount;
    
    // 지터 지수 (지터 합 / 경로 길이)
    if (Metrics.MousePathLength > 0.0f)
    {
        Profile.JitterIndex = Metrics.JitterSum / Metrics.MousePathLength;
    }
    
    // 상호작용 강도 (최대 속도 피크)
    if (Metrics.VelocityPeaks.Num() > 0)
    {
        float MaxVelocity = 0.0f;
        for (float Velocity : Metrics.VelocityPeaks)
        {
            if (Velocity > MaxVelocity)
            {
                MaxVelocity = Velocity;
            }
        }
        Profile.Intensity = MaxVelocity;
    }
    
    // 컨텍스트 선택 복사
    Profile.ContextualChoices = Metrics.ContextualChoices;
    
    return Profile;
}

float UBehaviorTracker::CalculateDistance(const FVector2D& Pos1, const FVector2D& Pos2) const
{
    const float DX = Pos2.X - Pos1.X;
    const float DY = Pos2.Y - Pos1.Y;
    return FMath::Sqrt(DX * DX + DY * DY);
}

float UBehaviorTracker::GetCurrentTime() const
{
    // 밀리초 단위로 시간 반환
    return static_cast<float>(FPlatformTime::Seconds() * 1000.0);
}
