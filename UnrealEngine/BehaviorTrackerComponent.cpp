// BehaviorTrackerComponent.cpp
// 행동 추적 컴포넌트 구현

#include "BehaviorTrackerComponent.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "Engine/World.h"

// Slate 애플리케이션은 에디터에서만 사용 가능
#if WITH_EDITOR
#include "Framework/Application/SlateApplication.h"
#endif

UBehaviorTrackerComponent::UBehaviorTrackerComponent(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer)
    , bIsTracking(false)
    , bAutoStart(true)
    , bAutoTrackMouse(true)
    , bAutoTrackClicks(true)
{
    PrimaryComponentTick.bCanEverTick = true;
    PrimaryComponentTick.TickGroup = TG_PrePhysics;
    
    Tracker = NewObject<UBehaviorTracker>(this);
}

void UBehaviorTrackerComponent::BeginPlay()
{
    Super::BeginPlay();
    
    if (bAutoStart)
    {
        StartTracking();
    }
}

void UBehaviorTrackerComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
    Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
    
    if (!bIsTracking || !Tracker)
    {
        return;
    }
    
    // 자동 마우스 추적
    if (bAutoTrackMouse)
    {
#if WITH_EDITOR
        // 에디터에서만 Slate 사용
        if (FSlateApplication::IsInitialized())
        {
            FVector2D MousePosition = FSlateApplication::Get().GetCursorPos();
            Tracker->TrackMovement(MousePosition);
        }
#else
        // 런타임에서는 플레이어 컨트롤러에서 마우스 위치 가져오기
        if (APlayerController* PC = GetWorld()->GetFirstPlayerController())
        {
            float MouseX, MouseY;
            if (PC->GetMousePosition(MouseX, MouseY))
            {
                Tracker->TrackMovement(FVector2D(MouseX, MouseY));
            }
        }
#endif
    }
}

void UBehaviorTrackerComponent::StartTracking()
{
    if (Tracker)
    {
        Tracker->StartSession();
        bIsTracking = true;
        
        if (bAutoTrackMouse || bAutoTrackClicks)
        {
            SetupInputBindings();
        }
    }
}

void UBehaviorTrackerComponent::StopTracking()
{
    bIsTracking = false;
}

FBehavioralProfile UBehaviorTrackerComponent::GetProfile() const
{
    if (Tracker)
    {
        return Tracker->GetBehavioralProfile();
    }
    return FBehavioralProfile();
}

void UBehaviorTrackerComponent::SetupInputBindings()
{
    // 플레이어 컨트롤러에서 입력 바인딩 설정
    // 실제 구현은 프로젝트의 입력 시스템에 따라 다를 수 있음
    // 여기서는 기본 구조만 제공
}

void UBehaviorTrackerComponent::OnMouseMove()
{
    if (bIsTracking && Tracker && bAutoTrackMouse)
    {
#if WITH_EDITOR
        if (FSlateApplication::IsInitialized())
        {
            FVector2D MousePosition = FSlateApplication::Get().GetCursorPos();
            Tracker->TrackMovement(MousePosition);
        }
#else
        if (APlayerController* PC = GetWorld()->GetFirstPlayerController())
        {
            float MouseX, MouseY;
            if (PC->GetMousePosition(MouseX, MouseY))
            {
                Tracker->TrackMovement(FVector2D(MouseX, MouseY));
            }
        }
#endif
    }
}

void UBehaviorTrackerComponent::OnMouseClick()
{
    if (bIsTracking && Tracker && bAutoTrackClicks)
    {
        Tracker->RecordClick();
    }
}
