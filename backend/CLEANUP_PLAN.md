# 파일 정리 계획

## 📅 정리 일시
2026년 1월 16일

---

## 🗑️ 삭제 대상 파일

### 1. 중복된 논문 생성 스크립트
- ✅ **유지**: `create_paper_perfect.py` (최종 버전)
- ❌ **삭제**: 
  - `create_paper_two_column.py`
  - `create_paper_from_template.py`
  - `create_paper_from_template_complete.py`
  - `create_presentation_paper_docx.py`

### 2. 분석 스크립트 (개발용 임시 파일)
- ❌ **삭제**:
  - `analyze_paper_detailed.py`
  - `analyze_template_exact.py`
  - `analyze_pdf_format.py`

### 3. 추출 스크립트 (개발용 임시 파일)
- ❌ **삭제**:
  - `extract_template_details.py`
  - `extract_table_info.py`
  - `extract_top_elements.py`
  - `extract_pdf_top.py`
  - `extract_pdf_image.py`
  - `extract_pdf_image_fitz.py`
  - `extract_image_from_pdf.py`

### 4. 검증 스크립트 (개발용 임시 파일)
- ❌ **삭제**:
  - `verify_paper_author.py`
  - `verify_docx_output.py`
  - `compare_with_template.py`

### 5. 이미지 추가 스크립트 (기능 통합됨)
- ❌ **삭제**:
  - `add_image_to_paper.py` (기능이 `create_paper_perfect.py`에 통합됨)

### 6. 기타 임시 파일
- ❌ **삭제**:
  - `read_docx_template.py` (개발용)
  - `read_pdf_template.py` (개발용)
  - `convert_to_formal_writing.py` (사용 안 함)

---

## ✅ 유지할 파일

### 핵심 논문 생성
- `create_paper_perfect.py` - 최종 논문 생성 스크립트

### 핵심 기능 모듈
- `api_server.py` - FastAPI 서버
- `neuro_controller.py` - 신경 제어
- `ml_personality_model.py` - ML 모델
- `game_event_parser.py` - 게임 이벤트 파싱
- `game_behavior_processor.py` - 게임 행동 처리
- `user_profiles.py` - 사용자 프로필
- `predictive_model.py` - 예측 모델
- 기타 핵심 기능 모듈들

### 테스트 파일
- `test_*.py` - 테스트 스크립트들
- `comprehensive_test.py` - 종합 테스트
- `final_verification.py` - 최종 검증

---

## 📊 정리 결과 예상

- **삭제 예정**: 약 20개 파일
- **유지**: 핵심 기능 및 테스트 파일
- **효과**: 코드베이스 정리, 유지보수성 향상
