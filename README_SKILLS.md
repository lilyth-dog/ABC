# Claude Skills & MCP Integration

이 프로젝트는 Claude Code의 Skills 시스템과 MCP(Model Context Protocol) 통합을 지원합니다.

**Cursor IDE 사용자**: Cursor에서도 이 Skills를 활용할 수 있습니다. `.cursorrules` 파일과 `.cursor/skills-reference.md`를 참조하세요.

## 설치된 Skills

### 1. Behavioral Analysis Skill
- **위치**: `.claude/skills/behavioral-analysis/`
- **용도**: 사용자 행동 패턴 분석 및 성격 추론
- **활성화**: 자동 활성화

### 2. Neural Simulation Skill
- **위치**: `.claude/skills/neural-simulation/`
- **용도**: EEG 신호를 운동학으로 변환하는 신경 물리 시뮬레이션
- **활성화**: 자동 활성화

## MCP 설정

MCP 서버 설정은 `.claude/mcp-config.json`에 정의되어 있습니다.

### 활성화된 MCP 서버
- `anthropics/mcp-integration`: Smithery를 통한 MCP 통합 패턴
- `local-behavioral-analysis`: 로컬 행동 분석 API

## 프롬프트 엔지니어링 패턴

프로젝트는 다음 프롬프트 패턴을 사용합니다:

### 1. Few-Shot Learning
- 의미적 유사도 기반 예제 선택
- 동적 예제 검색 지원

### 2. Chain-of-Thought
- 단계별 추론 프로세스
- 자체 검증 메커니즘 포함

### 3. Progressive Disclosure
- 3단계 레벨 구조 (Echo → Reflection → Synthesis)
- 점진적 정보 공개

프롬프트 템플릿은 `.claude/prompt-templates/` 디렉토리에 있습니다.

## 사용 방법

### Claude Code에서 Skills 사용

1. **Skills 자동 로드**: 프로젝트 디렉토리에서 Claude Code를 실행하면 자동으로 Skills가 로드됩니다.

2. **특정 Skill 참조**: 
   ```
   @behavioral-analysis를 사용하여 사용자 행동을 분석해줘
   ```

3. **프롬프트 템플릿 사용**:
   ```
   behavioral-analysis 템플릿을 사용하여 새로운 분석 로직을 작성해줘
   ```

### MCP 서버 연결

MCP 서버는 Claude Code 설정에서 자동으로 연결됩니다. 수동 설정이 필요한 경우:

1. Claude Code 설정 열기
2. MCP 섹션으로 이동
3. `.claude/mcp-config.json` 경로 지정

## 참고 자료

- [Anthropic Skills 공식 문서](https://github.com/anthropics/skills)
- [MCP 통합 가이드](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [프롬프트 엔지니어링 패턴](https://smithery.ai/skills/wshobson/prompt-engineering-patterns)

## 적용된 스킬들

이 프로젝트에 적용된 외부 스킬들:

1. **mcp-integration** (anthropics): MCP 통합 패턴
2. **prompt-engineering-patterns** (wshobson): 고급 프롬프트 엔지니어링 기법
3. **skill-development** (anthropics): Skills 개발 가이드라인
4. **docstring** (pytorch): 표준 docstring 작성 규칙 (Python 코드에 적용됨)
