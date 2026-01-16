// TestBehaviorTrackerActor.h
// 행동 추적 시스템 테스트용 액터

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "BehaviorTrackerComponent.h"
#include "BehaviorEvaluator.h"
#include "TestBehaviorTrackerActor.generated.h"

/**
 * 행동 추적 시스템 테스트용 액터
 * 월드에 배치하여 자동으로 행동 추적 테스트 수행
 */
UCLASS()
class DIGITALHUMANTWIN_API ATestBehaviorTrackerActor : public AActor
{
    GENERATED_BODY()

public:
    ATestBehaviorTrackerActor();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;

protected:
    // 행동 추적 컴포넌트
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Behavior Tracker")
    UBehaviorTrackerComponent* TrackerComponent;

    // 행동 평가기
    UPROPERTY()
    UBehaviorEvaluator* Evaluator;

    // 테스트 설정
    UPROPERTY(EditAnywhere, Category = "Test Settings")
    float ProfilePrintInterval = 5.0f;

    UPROPERTY(EditAnywhere, Category = "Test Settings")
    bool bPrintProfileToLog = true;

    UPROPERTY(EditAnywhere, Category = "Test Settings")
    bool bSimulateMouseMovement = false;

private:
    float ProfilePrintTimer = 0.0f;
    int32 SessionCount = 1;
    float SimulatedMouseX = 0.0f;
    float SimulatedMouseY = 0.0f;

    // 시뮬레이션된 마우스 움직임 생성
    void SimulateMouseMovement(float DeltaTime);
};
