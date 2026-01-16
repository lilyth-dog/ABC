# Skills Reference for Cursor AI

이 파일은 Cursor AI가 프로젝트 작업 시 참조할 Skills 정보를 담고 있습니다.

## Behavioral Analysis Skill

### 사용 시점
- 사용자 행동 패턴 분석
- 성격 특성 가중치 생성 (Logic, Intuition, Fluidity, Complexity)
- 연속 학습을 위한 행동 프로필 처리
- 스트레스 패턴 및 이상 행동 감지
- 성격 진화 예측

### 핵심 기능

#### 1. 행동 프로필 처리
```python
# 예제: 행동 프로필 처리
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

#### 2. 성격 추론
- **Logic vs Intuition**: 의사결정 지연시간 패턴에서 유도
- **Fluidity**: 경로 효율성 및 움직임 안정성 기반
- **Complexity**: 수정 빈도 및 참여 깊이로 계산

#### 3. 연속 학습
- Exponential Moving Average (EMA)로 가중치 업데이트
- 세션 기반 진화 추적
- 데이터 양과 안정성 기반 신뢰도 점수

#### 4. 예측 분석
- 선형 회귀를 사용한 행동 트렌드 예측
- 지연시간 및 수정 메트릭에서 스트레스 패턴 감지
- Z-score 통계 분석을 사용한 이상 감지
- 성격 진화 예측

### 구현 패턴

#### Progressive Disclosure
1. **Level 1 (Echo)**: 기본 신호 처리, 약한 신호 축소
2. **Level 2 (Reflection)**: 중간 민감도, 문화적 조정
3. **Level 3 (Synthesis)**: 전체 민감도, 고급 ML 모델

#### 문화적 편향 완화
- `cultural_weights.json`에서 문화적 가중치 수정자 로드
- 성격 가중치에 컨텍스트별 조정 적용
- 문화적으로 적절한 원형 이름 생성

## Neural Simulation Skill

### 사용 시점
- EEG 신호(theta/beta 파)를 운동학으로 처리
- Magnonic reservoir computing 시뮬레이션 실행
- 신경 상태를 3D 아바타 움직임으로 매핑
- MuMax3 물리 시뮬레이션 통합

### 핵심 기능

#### EEG-to-Kinematics 파이프라인
- **입력**: Theta power (4-8Hz), Beta power (13-30Hz)
- **처리**: Neuro-Magnetic Modulation → Magnonic Reservoir → Readout Layer
- **출력**: 관절 각도, 유동성 지수, 물리 메타데이터

#### 인과 체인
1. **Neuro-Magnetic Modulation**
   - Theta → 감쇠 계수 (alpha)
   - Beta → 외부 자기장 (B_ext)

2. **Magnonic Reservoir Dynamics**
   - MuMax3에서 사전 계산된 패턴
   - 실시간 시뮬레이션 (선택적)
   - Mock 파형 패턴으로 폴백

3. **Spatial Readout**
   - 128x128 → 16384 벡터로 평탄화
   - 20D 운동학으로 선형 투영
   - 유동성 계산 (저크의 역수)

```python
# 예제: EEG 스트림 처리
result = controller.process_eeg_stream(theta_power=0.7, beta_power=0.3)
# 반환: joint_angles, fluidity_index, sim_params, physics
```

## Prompt Engineering Patterns

### Few-Shot Learning
- 의미적 유사도 기반 예제 선택
- 동적 예제 검색 지원
- 컨텍스트 창 트레이드오프 고려

### Chain-of-Thought
- 단계별 추론 프로세스
- 자체 일관성 검증
- 출력 검증 체크리스트

### Progressive Disclosure
- 3단계 레벨 구조
- 점진적 정보 공개
- 복잡도에 따른 구현 조정

## 관련 파일

- Skills 정의: `.claude/skills/behavioral-analysis/SKILL.md`
- Skills 정의: `.claude/skills/neural-simulation/SKILL.md`
- 프롬프트 템플릿: `.claude/prompt-templates/behavioral-analysis.md`
- MCP 설정: `.claude/mcp-config.json`
