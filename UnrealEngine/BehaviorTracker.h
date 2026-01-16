// BehaviorTracker.h
// 언리얼 엔진용 행동 수집 및 평가 시스템
// 사용자 상호작용 패턴을 수집하여 성격 특성을 추론하기 위한 데이터 수집

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "Engine/Engine.h"
#include "DigitalHumanTwin.h"
#include "BehaviorTracker.generated.h"

/**
 * 상호작용 메트릭 구조체
 */
USTRUCT(BlueprintType)
struct FInteractionMetrics
{
    GENERATED_BODY()

    // 마우스 경로 관련
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    float MousePathLength = 0.0f;

    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    FVector2D LastMousePosition = FVector2D::ZeroVector;

    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    float LastMoveTime = 0.0f;

    // 클릭 및 상호작용
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    int32 ClickCount = 0;

    // 의사결정 지연시간
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    TArray<float> DecisionLatencies;

    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    float StepStartTime = 0.0f;

    // 수정 빈도
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    int32 RevisionCount = 0;

    // 속도 피크 (빠른 움직임 감지)
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    TArray<float> VelocityPeaks;

    // 지터 지수 (작은 움직임 빈도)
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    float JitterSum = 0.0f;

    // 세션 시작 시간
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    float SessionStartTime = 0.0f;

    // 컨텍스트 선택 (UI 선택 등)
    UPROPERTY(BlueprintReadWrite, Category = "Behavior")
    TMap<FString, FString> ContextualChoices;
};

/**
 * 행동 프로필 결과 구조체
 */
USTRUCT(BlueprintType)
struct FBehavioralProfile
{
    GENERATED_BODY()

    // 경로 효율성 (최적 경로 대 실제 경로 비율)
    UPROPERTY(BlueprintReadWrite, Category = "Profile")
    float PathEfficiency = 0.0f;

    // 평균 의사결정 지연시간 (ms)
    UPROPERTY(BlueprintReadWrite, Category = "Profile")
    float AvgDecisionLatency = 0.0f;

    // 수정 빈도
    UPROPERTY(BlueprintReadWrite, Category = "Profile")
    int32 RevisionRate = 0;

    // 지터 지수
    UPROPERTY(BlueprintReadWrite, Category = "Profile")
    float JitterIndex = 0.0f;

    // 상호작용 강도 (초당 액션 수)
    UPROPERTY(BlueprintReadWrite, Category = "Profile")
    float Intensity = 0.0f;

    // 컨텍스트 선택
    UPROPERTY(BlueprintReadWrite, Category = "Profile")
    TMap<FString, FString> ContextualChoices;
};

/**
 * 행동 추적 및 평가 시스템
 * 사용자의 마우스 움직임, 클릭, 의사결정 시간 등을 수집하여 성격 추론에 사용
 */
UCLASS(BlueprintType, Blueprintable)
class DIGITALHUMANTWIN_API UBehaviorTracker : public UObject
{
    GENERATED_BODY()

public:
    UBehaviorTracker(const FObjectInitializer& ObjectInitializer);

    /**
     * 세션 시작/리셋
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void StartSession();

    /**
     * 마우스 움직임 추적
     * @param MousePosition 현재 마우스 위치 (화면 좌표)
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void TrackMovement(const FVector2D& MousePosition);

    /**
     * 클릭 이벤트 기록
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void RecordClick();

    /**
     * 의사결정 단계 시작 (옵션이 표시될 때 호출)
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void StartDecisionStep();

    /**
     * 의사결정 단계 완료 (선택이 완료될 때 호출)
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void RecordStepCompletion();

    /**
     * 값 수정 기록 (사용자가 값을 변경할 때 호출)
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void RecordRevision();

    /**
     * 컨텍스트 선택 기록 (UI 선택 등)
     * @param Key 선택 항목 키 (예: "aesthetics", "traitWeights")
     * @param Value 선택된 값
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    void RecordChoice(const FString& Key, const FString& Value);

    /**
     * 행동 프로필 계산 및 반환
     * @return 계산된 행동 프로필
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    FBehavioralProfile GetBehavioralProfile() const;

    /**
     * 현재 메트릭 가져오기 (디버깅용)
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Tracker")
    FInteractionMetrics GetCurrentMetrics() const { return Metrics; }

protected:
    // 현재 수집 중인 메트릭
    UPROPERTY()
    FInteractionMetrics Metrics;

    // 이전 마우스 위치 (경로 계산용)
    UPROPERTY()
    FVector2D LastPosition;

    // 빠른 움직임 임계값 (픽셀/ms)
    UPROPERTY(EditAnywhere, Category = "Behavior Tracker")
    float FastMovementThreshold = 5.0f;

    // 지터 감지 임계값 (픽셀)
    UPROPERTY(EditAnywhere, Category = "Behavior Tracker")
    float JitterThreshold = 10.0f;

private:
    /**
     * 두 점 사이의 거리 계산
     */
    float CalculateDistance(const FVector2D& Pos1, const FVector2D& Pos2) const;

    /**
     * 현재 시간 가져오기 (ms)
     */
    float GetCurrentTime() const;
};
