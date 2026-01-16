---
name: behavioral-analysis
description: Analyze user behavioral patterns and generate personality insights for Digital Human Twin
version: 1.0.0
author: ABC Project
tags: [behavior, personality, ml, digital-twin]
---

# Behavioral Analysis Skill

## When to Use

Use this skill when:
- Analyzing user interaction patterns from browser metrics
- Generating personality trait weights (Logic, Intuition, Fluidity, Complexity)
- Processing behavioral profiles for continuous learning
- Detecting stress patterns and anomalies in user behavior
- Predicting personality evolution over time

## Core Capabilities

### 1. Behavioral Profile Processing
- Extracts behavioral metrics: decision latency, revision rate, path efficiency
- Maps metrics to personality dimensions using ML models or rule-based systems
- Applies cultural context adjustments for bias mitigation

### 2. Personality Inference
- **Logic vs Intuition**: Derived from decision latency patterns
- **Fluidity**: Based on path efficiency and movement stability
- **Complexity**: Calculated from revision rate and engagement depth

### 3. Continuous Learning
- Exponential Moving Average (EMA) for weight updates
- Session-based evolution tracking
- Confidence scoring based on data volume and stability

### 4. Predictive Analytics
- Behavioral trend prediction using linear regression
- Stress pattern detection from latency and revision metrics
- Anomaly detection using Z-score statistical analysis
- Personality evolution forecasting

## Implementation Patterns

### Progressive Disclosure
1. **Level 1 (Echo)**: Basic signal processing, collapse weak signals
2. **Level 2 (Reflection)**: Moderate sensitivity, cultural adjustments
3. **Level 3 (Synthesis)**: Full sensitivity, advanced ML models

### Cultural Bias Mitigation
- Load cultural weight modifiers from `cultural_weights.json`
- Apply context-specific adjustments to personality weights
- Generate culturally-appropriate archetype names

### ML Model Integration
- Use `MLPersonalityModel` for personality prediction
- Fallback to rule-based system if ML unavailable
- Support online learning with real user data

## Best Practices

1. **Data Quality**: Ensure minimum 3 sessions for trend analysis
2. **Cultural Context**: Always specify cultural context for accurate bias adjustment
3. **Maturity Levels**: Respect DTMM maturity progression (Echo → Reflection → Synthesis)
4. **Privacy**: Follow GDPR/PIPA compliance for data storage and export

## Example Usage

```python
from neuro_controller import MagnonicController

controller = MagnonicController()
profile = {
    "pathEfficiency": 0.85,
    "avgDecisionLatency": 2500,
    "revisionRate": 2,
    "culturalContext": "east_asian"
}
result = controller.process_behavioral_profile(profile)
```

## Related Components

- `neuro_controller.py`: Main orchestration
- `ml_personality_model.py`: ML-based personality inference
- `predictive_model.py`: Trend and anomaly detection
- `user_profiles.py`: Data persistence layer
