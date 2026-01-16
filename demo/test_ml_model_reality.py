"""ML 모델 실제 작동 확인"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from ml_personality_model import MLPersonalityModel

print("=" * 60)
print("ML 모델 실제 작동 확인")
print("=" * 60)

model = MLPersonalityModel(model_type="random_forest", use_pretrained=True)
print(f"\n모델 정보:")
print(f"  - 타입: {model.model_type}")
print(f"  - 학습 상태: {model.is_trained}")
print(f"  - 모델 수: {len(model.models)}")

# 테스트 예측
test_features = {
    'latency': 3500,
    'revisions': 4,
    'efficiency': 0.75,
    'intensity': 2.3
}

print(f"\n테스트 입력:")
print(f"  - Latency: {test_features['latency']}ms")
print(f"  - Revisions: {test_features['revisions']}")
print(f"  - Efficiency: {test_features['efficiency']:.2f}")
print(f"  - Intensity: {test_features['intensity']:.2f}")

prediction = model.predict(test_features)

print(f"\n✓ ML 모델 예측 결과:")
print(f"  - Logic: {prediction['Logic']:.2f} ({prediction['Logic']*100:.0f}%)")
print(f"  - Intuition: {prediction['Intuition']:.2f} ({prediction['Intuition']*100:.0f}%)")
print(f"  - Fluidity: {prediction['Fluidity']:.2f} ({prediction['Fluidity']*100:.0f}%)")
print(f"  - Complexity: {prediction['Complexity']:.2f} ({prediction['Complexity']*100:.0f}%)")

# 특징 중요도
importance = model.get_feature_importance()
if importance:
    print(f"\n특징 중요도 (Logic):")
    for feature, imp in importance.get('Logic', {}).items():
        print(f"  - {feature}: {imp:.3f}")

print("\n" + "=" * 60)
print("✓ ML 모델이 실제로 작동하고 있습니다!")
print("=" * 60)
