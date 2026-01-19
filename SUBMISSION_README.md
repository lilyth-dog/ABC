# Nexus Entertainment 해커톤 프로젝트 제출 가이드

## 📦 제출 구성

이 프로젝트는 **논문**과 **코드**로 구성되어 있습니다.

### 1. 논문 제출
- **위치**: `archive/paper_submission/`
- **제출 파일**: `ABC해커톤_논문_제출용.docx`
- **상세 정보**: `archive/paper_submission/README.md` 참조

### 2. 코드 제출 (클라우드 업로드용)

---

## 🚀 프로젝트 개요

**Nexus Entertainment: 행동 기반 디지털 휴먼 트윈 — 게임 플레이 기반 성격 추론 및 개인화 시스템**

Nexus Entertainment는 게임 플레이 데이터를 활용하여 사용자의 성격을 추론하고, 이를 바탕으로 개인화된 게임 경험을 제공하는 시스템입니다.

---

## 📋 프로젝트 구조

리포지토리 폴더명은 `ABC/`입니다.

```
ABC/
├── backend/              # 백엔드 서버 (Python/FastAPI)
│   ├── api_server.py     # FastAPI 서버
│   ├── ml_personality_model.py  # ML 모델
│   ├── game_event_parser.py     # 게임 이벤트 파싱
│   ├── game_behavior_processor.py  # 행동 처리
│   └── ...
├── src/                  # 프론트엔드 (React/TypeScript)
│   ├── components/       # React 컴포넌트
│   ├── hooks/            # React Hooks
│   └── ...
├── docs/                 # 문서
├── archive/              # 논문 아카이브
│   └── paper_submission/ # 제출용 논문
└── README.md            # 프로젝트 README
```

---

## 🛠️ 기술 스택

### Backend
- **언어**: Python 3.10+
- **프레임워크**: FastAPI
- **ML 라이브러리**: scikit-learn, NumPy
- **데이터베이스**: SQLite

### Frontend
- **언어**: TypeScript
- **프레임워크**: React 19
- **3D 렌더링**: Three.js
- **빌드 도구**: Vite

---

## 📦 설치 및 실행

### 필수 요구사항
- Python 3.10 이상
- Node.js 18 이상
- npm 또는 yarn

### Backend 설정

```bash
cd backend
pip install -r requirements.txt
python api_server.py
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

### Frontend 설정

```bash
npm install
npm run dev
```

프론트엔드는 기본적으로 `http://localhost:5173`에서 실행됩니다.

---

## 🔧 환경 변수

`.env.example`를 복사해 `.env.local` 또는 `.env.production`으로 사용하고, 백엔드는 시스템 환경 변수로 설정하세요.

```env
# Frontend (Vite)
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Backend
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5180
LOG_LEVEL=INFO
PORT=8000
# DB_PATH=backend/user_profiles.db
```

---

## 📊 주요 기능

### 1. 게임 데이터 수집
- 마인크래프트, 스타듀밸리, 두근두근타운 지원
- 실제 공개 데이터 통합 (OpenDota API, MineRL)

### 2. 성격 추론
- 랜덤 포레스트 회귀 모델
- 4차원 성격 가중치 (Logic, Intuition, Fluidity, Complexity)
- 온라인 학습 (EMA)

### 3. 개인화 서비스
- 적응형 게임 경험
- 게임 추천 시스템
- 소셜 매칭

---

## 📈 성능 지표

### 시스템 성능
- **파싱 정확도**: 75.00%
- **엣지 케이스 처리율**: 100.00%
- **파이프라인 성능**: 초당 118만+ 이벤트
- **API 응답 시간**: 3.62ms

### 성격 추론 성능
- **통합 프로필 신뢰도**: 75%
- **Logic 정확도**: 78%
- **Intuition 정확도**: 72%

---

## 🧪 테스트

### Backend 테스트
```bash
cd backend
pytest tests/
```

### 전체 시스템 테스트
```bash
cd backend
python final_verification_test.py
```

---

## 📚 문서

- **프로젝트 README**: `README.md`
- **개발자 가이드**: `docs/DEVELOPER_GUIDE.md`
- **API 레퍼런스**: `docs/API_REFERENCE.md`
- **논문**: `archive/paper_submission/`

---

## 🔒 보안 및 프라이버시

- 사용자 데이터는 명시적 동의 후에만 수집
- GDPR 준수
- 환경 변수를 통한 민감 정보 관리
- Rate Limiting 적용

---

## 📝 라이선스

Nexus Entertainment 프로젝트는 ABC 해커톤 제출용으로 개발되었습니다.

---

## 👥 저자

- **유준석** (Jun-seok Yoo)
- 한신대학교 공공인재학부
- 이메일: dbwnstjr1973@hs.ac.kr

---

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이메일로 연락주세요.

---

**제출 일시**: 2026년 1월 16일  
**프로젝트 상태**: ✅ 제출 준비 완료
