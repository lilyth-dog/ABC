# ABC 해커톤 프로젝트 제출 가이드

## 제출 구성

이 프로젝트는 **논문**과 **코드**로 구성되어 있습니다.

### 1. 논문 제출
- **위치**: `archive/paper_submission/`
- **제출 파일**: `ABC해커톤_논문_제출용.docx`
- **상세 정보**: `archive/paper_submission/README.md` 참조

### 2. 코드 제출 (클라우드 업로드용)

---

## Quick Start (압축 파일 받은 경우)

```bash
# 1. 압축 해제 후 폴더로 이동
cd ABC

# 2. 프론트엔드 의존성 설치
npm install

# 3. 백엔드 의존성 설치
pip install -r backend/requirements.txt

# 4. 실행 (프론트엔드 + 백엔드 동시)
npm run dev
```

**또는 Docker로 백엔드만 실행 (Python/Node.js 설치 불필요):**

```bash
docker build -t abc-backend .
docker run -p 8080:8080 abc-backend
# API 문서: http://localhost:8080/docs
```

---

## 프로젝트 개요

**행동 기반 디지털 휴먼 트윈: 게임 플레이 기반 성격 추론 및 개인화 시스템**

게임 플레이 데이터를 활용하여 사용자의 성격을 추론하고, 이를 바탕으로 개인화된 게임 경험을 제공하는 시스템입니다.

---

## 프로젝트 구조

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

## 기술 스택

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

## 설치 및 실행

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

## 환경 변수

`.env` 파일을 생성하고 다음 변수를 설정하세요:

```env
# API 설정
API_HOST=localhost
API_PORT=8000

# 데이터베이스
DATABASE_PATH=backend/user_profiles.db

# 로깅
LOG_LEVEL=INFO
```

---

## 주요 기능

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

## 성능 지표

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

## 테스트

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

## Docker 실행

Python 환경 없이 Docker만으로 백엔드를 실행할 수 있습니다.

### 빌드 및 실행

```bash
# Docker 이미지 빌드
docker build -t abc-backend .

# 컨테이너 실행
docker run -p 8080:8080 abc-backend

# 헬스체크
curl http://localhost:8080/health
```

### API 문서 확인
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

---

## 문서

- **프로젝트 README**: `README.md`
- **개발자 가이드**: `docs/DEVELOPER_GUIDE.md`
- **API 레퍼런스**: `docs/API_REFERENCE.md`
- **논문**: `archive/paper_submission/`

---

## 보안 및 프라이버시

- 사용자 데이터는 명시적 동의 후에만 수집
- GDPR 준수
- 환경 변수를 통한 민감 정보 관리
- Rate Limiting 적용

---

## Cloud Run 배포

### 사전 요구사항
- Google Cloud SDK (`gcloud`) 설치 및 인증
- GCP 프로젝트 생성 및 Cloud Run API 활성화

### 배포 방법

```bash
# 1. GCP 인증
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. 배포 스크립트 실행
cd cloudrun
chmod +x deploy_backend.sh
./deploy_backend.sh
```

자세한 내용은 [`cloudrun/README.md`](cloudrun/README.md)를 참고하세요.

---

## 라이선스

이 프로젝트는 ABC 해커톤 제출용으로 개발되었습니다.

---

## 저자

- **유준석** (Jun-seok Yoo)
- 한신대학교 공공인재학부
- 이메일: dbwnstjr1973@hs.ac.kr

---

## 문의

프로젝트 관련 문의사항이 있으시면 이메일로 연락주세요.

---

**제출 일시**: 2026년 1월 16일  
**프로젝트 상태**: 제출 준비 완료
