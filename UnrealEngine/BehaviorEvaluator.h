// BehaviorEvaluator.h
// 수집된 행동 데이터를 평가하고 성격 특성으로 변환
// ML 모델과 연동하여 성격 가중치를 계산

#pragma once

#include "CoreMinimal.h"
#include "UObject/NoExportTypes.h"
#include "DigitalHumanTwin.h"
#include "BehaviorTracker.h"
#include "BehaviorEvaluator.generated.h"

/**
 * 성격 가중치 구조체
 */
USTRUCT(BlueprintType)
struct FPersonalityWeights
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite, Category = "Personality")
    float Logic = 0.5f;

    UPROPERTY(BlueprintReadWrite, Category = "Personality")
    float Intuition = 0.5f;

    UPROPERTY(BlueprintReadWrite, Category = "Personality")
    float Fluidity = 0.5f;

    UPROPERTY(BlueprintReadWrite, Category = "Personality")
    float Complexity = 0.5f;
};

/**
 * 행동 평가 결과
 */
USTRUCT(BlueprintType)
struct FBehaviorEvaluationResult
{
    GENERATED_BODY()

    // 성격 가중치
    UPROPERTY(BlueprintReadWrite, Category = "Evaluation")
    FPersonalityWeights PersonalityWeights;

    // 신뢰도 점수 (0.0 ~ 1.0)
    UPROPERTY(BlueprintReadWrite, Category = "Evaluation")
    float ConfidenceScore = 0.0f;

    // 세션 수
    UPROPERTY(BlueprintReadWrite, Category = "Evaluation")
    int32 SessionCount = 0;

    // 평가 근거
    UPROPERTY(BlueprintReadWrite, Category = "Evaluation")
    FString Reasoning;
};

/**
 * 행동 평가 시스템
 * 수집된 행동 데이터를 분석하여 성격 특성을 추론
 */
UCLASS(BlueprintType, Blueprintable)
class DIGITALHUMANTWIN_API UBehaviorEvaluator : public UObject
{
    GENERATED_BODY()

public:
    UBehaviorEvaluator(const FObjectInitializer& ObjectInitializer);

    /**
     * 행동 프로필을 평가하여 성격 가중치 계산
     * @param Profile 수집된 행동 프로필
     * @param SessionCount 현재 세션 수
     * @return 평가 결과
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Evaluator")
    FBehaviorEvaluationResult EvaluateBehavior(const FBehavioralProfile& Profile, int32 SessionCount = 1);

    /**
     * ML 모델을 사용한 평가 (백엔드 API 호출)
     * @param Profile 행동 프로필
     * @param APIEndpoint 백엔드 API 엔드포인트
     * @return 평가 결과
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Evaluator")
    void EvaluateWithML(const FBehavioralProfile& Profile, const FString& APIEndpoint);

    /**
     * 규칙 기반 평가 (ML 모델이 없을 때 폴백)
     * @param Profile 행동 프로필
     * @return 평가 결과
     */
    UFUNCTION(BlueprintCallable, Category = "Behavior Evaluator")
    FBehaviorEvaluationResult EvaluateWithRules(const FBehavioralProfile& Profile);

protected:
    /**
     * 신뢰도 점수 계산
     * @param SessionCount 세션 수
     * @param Stability 안정성 점수 (0.0 ~ 1.0)
     * @return 신뢰도 점수
     */
    float CalculateConfidence(int32 SessionCount, float Stability) const;

    /**
     * 안정성 점수 계산 (가중치 변동성 기반)
     * @param WeightHistory 과거 가중치 히스토리
     * @return 안정성 점수
     */
    float CalculateStability(const TArray<FPersonalityWeights>& WeightHistory) const;
};
