// BehaviorEvaluator.cpp
// 행동 평가 시스템 구현

#include "BehaviorEvaluator.h"
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Serialization/Json.h"
#include "Serialization/JsonSerializer.h"

UBehaviorEvaluator::UBehaviorEvaluator(const FObjectInitializer& ObjectInitializer)
    : Super(ObjectInitializer)
{
}

FBehaviorEvaluationResult UBehaviorEvaluator::EvaluateBehavior(const FBehavioralProfile& Profile, int32 SessionCount)
{
    // 기본적으로 규칙 기반 평가 사용
    FBehaviorEvaluationResult Result = EvaluateWithRules(Profile);
    Result.SessionCount = SessionCount;
    
    // 신뢰도 계산
    float Stability = 0.7f; // 기본값 (실제로는 히스토리 기반 계산 필요)
    Result.ConfidenceScore = CalculateConfidence(SessionCount, Stability);
    
    return Result;
}

FBehaviorEvaluationResult UBehaviorEvaluator::EvaluateWithRules(const FBehavioralProfile& Profile)
{
    FBehaviorEvaluationResult Result;
    
    // 규칙 기반 성격 가중치 계산
    // 논문의 규칙 기반 공식을 사용 (ML 모델 폴백)
    
    // Logic Weight: 의사결정 지연시간 기반
    // latency < 1000ms → 직관적 (Logic 낮음)
    // latency > 5000ms → 논리적 (Logic 높음)
    float LogicWeight = FMath::Clamp((Profile.AvgDecisionLatency - 1000.0f) / 4000.0f, 0.0f, 1.0f);
    
    // Intuition Weight: Logic의 보완
    float IntuitionWeight = 1.0f - LogicWeight;
    
    // Fluidity Weight: 경로 효율성 직접 매핑
    float FluidityWeight = FMath::Clamp(Profile.PathEfficiency, 0.0f, 1.0f);
    
    // Complexity Weight: 수정 빈도와 지연시간 조합
    float ComplexityWeight = FMath::Clamp(
        (Profile.RevisionRate * 0.2f) + (Profile.AvgDecisionLatency / 10000.0f),
        0.0f, 1.0f
    );
    
    Result.PersonalityWeights.Logic = LogicWeight;
    Result.PersonalityWeights.Intuition = IntuitionWeight;
    Result.PersonalityWeights.Fluidity = FluidityWeight;
    Result.PersonalityWeights.Complexity = ComplexityWeight;
    
    // 평가 근거 생성
    Result.Reasoning = FString::Printf(
        TEXT("의사결정 지연시간: %.0fms, 수정 빈도: %d, 경로 효율성: %.2f"),
        Profile.AvgDecisionLatency,
        Profile.RevisionRate,
        Profile.PathEfficiency
    );
    
    return Result;
}

void UBehaviorEvaluator::EvaluateWithML(const FBehavioralProfile& Profile, const FString& APIEndpoint)
{
    // HTTP 요청으로 백엔드 ML 모델 호출
    TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->OnProcessRequestComplete().BindLambda([this](FHttpRequestPtr Request, FHttpResponsePtr Response, bool bWasSuccessful)
    {
        if (bWasSuccessful && Response.IsValid())
        {
            // JSON 응답 파싱
            TSharedPtr<FJsonObject> JsonObject;
            TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());
            
            if (FJsonSerializer::Deserialize(Reader, JsonObject))
            {
                // 결과 처리 (델리게이트나 이벤트로 전달)
                // 실제 구현은 프로젝트 구조에 따라 다를 수 있음
            }
        }
    });
    
    // JSON 요청 본문 생성
    TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject);
    JsonObject->SetNumberField(TEXT("latency"), Profile.AvgDecisionLatency);
    JsonObject->SetNumberField(TEXT("revisions"), Profile.RevisionRate);
    JsonObject->SetNumberField(TEXT("efficiency"), Profile.PathEfficiency);
    JsonObject->SetNumberField(TEXT("intensity"), Profile.Intensity);
    
    FString OutputString;
    TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&OutputString);
    FJsonSerializer::Serialize(JsonObject.ToSharedRef(), Writer);
    
    Request->SetURL(APIEndpoint);
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request->SetContentAsString(OutputString);
    Request->ProcessRequest();
}

float UBehaviorEvaluator::CalculateConfidence(int32 SessionCount, float Stability) const
{
    // 신뢰도 = 기본값 + 세션 수 기여 + 안정성 기여
    // 최대 0.95로 제한
    float BaseConfidence = 0.2f;
    float SessionContribution = FMath::Min(SessionCount * 0.1f, 0.5f);
    float StabilityContribution = Stability * 0.3f;
    
    return FMath::Min(BaseConfidence + SessionContribution + StabilityContribution, 0.95f);
}

float UBehaviorEvaluator::CalculateStability(const TArray<FPersonalityWeights>& WeightHistory) const
{
    if (WeightHistory.Num() < 2)
    {
        return 0.3f; // 데이터 부족 시 낮은 안정성
    }
    
    // 표준편차 계산 (간단한 버전)
    // 실제로는 더 정교한 통계 계산 필요
    float Mean = 0.0f;
    for (const FPersonalityWeights& Weights : WeightHistory)
    {
        Mean += Weights.Logic;
    }
    Mean /= WeightHistory.Num();
    
    float Variance = 0.0f;
    for (const FPersonalityWeights& Weights : WeightHistory)
    {
        float Diff = Weights.Logic - Mean;
        Variance += Diff * Diff;
    }
    Variance /= WeightHistory.Num();
    
    float StdDev = FMath::Sqrt(Variance);
    
    // 안정성 = 1.0 - (표준편차 / 평균)
    if (Mean > 0.0f)
    {
        return FMath::Clamp(1.0f - (StdDev / Mean), 0.0f, 1.0f);
    }
    
    return 0.5f;
}
