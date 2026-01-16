// BehaviorTrackerComponent.h
// 언리얼 엔진 컴포넌트로 행동 추적을 자동화
// UI 위젯이나 플레이어 컨트롤러에 추가하여 자동으로 행동 수집

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "DigitalHumanTwin.h"
#include "BehaviorTracker.h"
#include "BehaviorTrackerComponent.generated.h"

/**
 * 행동 추적 컴포넌트
 * 액터나 위젯에 추가하여 자동으로 사용자 행동을 수집
 */
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class DIGITALHUMANTWIN_API UBehaviorTrackerComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UBehaviorTrackerComponent(const FObjectInitializer& ObjectInitializer);

    virtual void BeginPlay() override;
    virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

    /**
     * 행동 추적 시작
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void StartTracking();

    /**
     * 행동 추적 중지
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void StopTracking();

    /**
     * 행동 프로필 가져오기
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    FBehavioralProfile GetProfile() const;

    /**
     * 행동 추적기 인스턴스 가져오기
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    UBehaviorTracker* GetTracker() const { return Tracker; }

protected:
    // 행동 추적기 인스턴스
    UPROPERTY()
    UBehaviorTracker* Tracker;

    // 추적 활성화 여부
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Behavior Tracker")
    bool bIsTracking = false;

    // 자동 시작 여부
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Behavior Tracker")
    bool bAutoStart = true;

    // 마우스 입력 자동 추적 여부
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Behavior Tracker")
    bool bAutoTrackMouse = true;

    // 클릭 자동 추적 여부
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Behavior Tracker")
    bool bAutoTrackClicks = true;

private:
    // 이전 프레임 마우스 위치
    FVector2D PreviousMousePosition;

    // 마우스 입력 바인딩
    void SetupInputBindings();
    void OnMouseMove();
    void OnMouseClick();
};
