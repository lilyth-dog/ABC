# Nexus Entertainment

> The Future of Digital Human Twins and Virtual Idols

디지털 트윈과 버추얼 아이돌을 위한 차세대 플랫폼. 하이퍼 리얼리스틱 아바타를 생성하고 메타버스에서 활동하세요.

## 🚀 Features

- **Avatar Creator** - Ready Player Me 통합 아바타 생성
- **Identity Configurator** - AI 기반 페르소나 설정
- **3D World** - Three.js 기반 인터랙티브 월드
- **Analytics Dashboard** - 실시간 분석 대시보드
- **Neuro Controller** - 뉴럴 커플링 시스템
- **Game Data Pipeline** - 게임 플레이 데이터를 통한 플레이 스타일 카테고리 분석 (3단계 파이프라인)
- **Behavioral Analysis** - 행동 패턴 기반 디지털 휴먼 트윈 생성 및 진화
- **Continuous Learning** - 세션 간 지속적 학습 및 프로필 업데이트

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | React 19, Vite 7, Three.js |
| 3D | @react-three/fiber, @react-three/drei, @react-three/rapier |
| Backend | Python, FastAPI, Uvicorn |
| Charts | Recharts |
| Icons | Lucide React |

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/lilyth-dog/ABC.git
cd ABC

# Install dependencies
npm install

# Install backend dependencies
pip install -r backend/requirements.txt
```

## 📊 Datasets

프로젝트에 필요한 대용량 데이터셋 파일들은 GitHub에 포함되지 않습니다 (100MB 제한).

### 필요한 데이터셋

1. **TESS (Toronto Emotional Speech Set)** - 427.79 MB
   - 감정 인식 및 오디오 분석용
   - 다운로드: [TESS 공식 사이트](https://tspace.library.utoronto.ca/handle/1807/24487)
   - 압축 해제: `unzip datasets/toronto-emotional-speech-set-tess.zip -d datasets/tess/`

2. **Workout Fitness Video** - 330.12 MB
   - 모션 분석 및 바이오시그널 통합용
   - 팀 내부에서 공유된 링크 사용 또는 별도 제공

자세한 내용은 [`datasets/README.md`](datasets/README.md)를 참고하세요.

### Git LFS 사용 (선택사항)

대용량 파일을 Git에 포함하려면:

```bash
git lfs install
git lfs track "datasets/*.zip"
git add .gitattributes
```

## 🏃 Running

```bash
# Development (Frontend + Backend)
npm run dev

# Frontend only
npm run dev:frontend

# Backend only
npm run dev:backend

# Production build
npm run build
```

The app runs at:
- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`

## 📁 Project Structure

```
ABC/
├── src/
│   ├── components/     # React 컴포넌트
│   ├── hooks/          # Custom hooks
│   ├── simulation/     # 시뮬레이션 로직
│   ├── styles/         # 스타일시트
│   └── utils/          # 유틸리티 함수
├── backend/
│   ├── api_server.py           # FastAPI 서버
│   ├── neuro_controller.py    # 신경 제어 및 행동 분석
│   ├── game_event_parser.py    # 게임 이벤트 파서
│   ├── game_behavior_processor.py  # 게임 행동 처리
│   ├── user_profiles.py        # 사용자 프로필 관리 (GDPR)
│   ├── ml_personality_model.py # ML 기반 성격 모델
│   ├── simulation_db.py        # 시뮬레이션 데이터베이스
│   ├── tests/                  # 백엔드 테스트
│   └── final_verification_test.py  # 최종 검증 테스트
├── docs/
│   ├── ABC해커톤_논문_발표용.md  # 발표 논문
│   ├── DEVELOPER_GUIDE.md      # 개발자 가이드
│   └── FINAL_VERIFICATION_REPORT.md  # 최종 검증 리포트
├── datasets/           # 데이터셋 파일 (GitHub에 제외됨)
│   ├── README.md       # 데이터셋 사용 가이드
│   └── public/         # 공개 게임 데이터
├── public/             # 정적 파일
└── package.json
```

## Environment Variables

환경 변수는 `.env.production` 파일 또는 시스템 환경 변수로 설정합니다.

### 주요 환경 변수

- `CORS_ORIGINS`: CORS 허용 오리진 (기본값: `http://localhost:5173,http://localhost:3000,http://localhost:5180`)
- `LOG_LEVEL`: 로그 레벨 (기본값: `INFO`)
- `PORT`: 백엔드 서버 포트 (기본값: `8000`)
- `VITE_API_URL`: 프론트엔드 API URL (기본값: `http://localhost:8000`)
- `VITE_WS_URL`: WebSocket URL (기본값: `ws://localhost:8000`)

자세한 내용은 `backend/env_validator.py`를 참고하세요.

## 📡 API Documentation

백엔드 서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 API 엔드포인트

- `GET /health` - 서버 상태 확인
- `POST /api/game/events` - 게임 원시 이벤트 처리
- `POST /api/game/session` - 게임 세션 데이터 처리
- `POST /api/behavior` - 행동 프로필 처리 및 플레이 스타일/행동 분석
- `POST /api/user/{id}/consent` - 사용자 동의 저장
- `GET /api/user/{id}/export` - GDPR 데이터 내보내기
- `DELETE /api/user/{id}` - 사용자 데이터 삭제

## 최종 검증 결과

프로젝트는 최종 검증을 통과했습니다:

- **시스템 컴포넌트**: 5/5 통과 (100%)
- **API 엔드포인트**: 4/4 통과 (100%)
- **게임 파이프라인**: 3/3 통과 (100%)
- **성능 벤치마크**: 2/2 통과 (100%)
- **E2E 통합**: 1/1 통과 (100%)

**전체 결과: 15/15 통과 (100%)**

자세한 내용은 [`docs/FINAL_VERIFICATION_REPORT.md`](docs/FINAL_VERIFICATION_REPORT.md)를 참고하세요.

## Testing

```bash
# 백엔드 테스트 실행
cd backend
python -m pytest tests/

# 최종 검증 테스트 실행
python final_verification_test.py

# 프론트엔드 테스트 실행
npm run test
```

## 🏷️ 플레이 스타일 라벨링 방법

이 프로젝트의 검증 목표는 “사람의 성격을 정확히 추론한다”가 아니라, 게임 이벤트에서 관찰 가능한 **플레이 스타일 카테고리**를 일관되게 분석하는 것입니다.

### 1. 라벨링 패킷 생성

라벨러에게 전달할 패킷을 생성합니다. 이 파일에는 모델 예측값이 들어가지 않아 라벨링 편향을 줄입니다.

```bash
PYTHONPATH=backend python3 backend/prepare_playstyle_annotation_packet.py
```

생성 파일:

- `datasets/validation/playstyle_annotation_packet.json` - 라벨러가 읽을 이벤트 요약
- `datasets/validation/real_playstyle_sessions_unlabeled.json` - 라벨을 채워 넣을 검증 데이터셋

### 2. 라벨 카테고리 선택

각 세션마다 아래 중 하나를 `primary_playstyle`로 선택합니다.

| Category | 라벨링 기준 |
|----------|-------------|
| `planner` | 첫 건축/행동 전 준비 행동이 뚜렷함 |
| `iterative_refiner` | 배치 후 제거/수정/반복 개선이 많음 |
| `route_optimizer` | 이동 경로가 직접적이고 효율적임 |
| `complex_builder` | 건축 위치·높이·공간 구성이 복잡함 |
| `resource_diversifier` | 다양한 아이템/블록/자원을 사용함 |
| `risk_taker` | 낮은 높이, 낮은 조도 등 위험 신호가 많음 |

### 3. `annotations[]`에 라벨 입력

`datasets/validation/real_playstyle_sessions_unlabeled.json`에서 각 세션의 `annotations` 배열을 채웁니다. 최소 3명의 독립 라벨러를 권장합니다.

```json
"annotations": [
  {
    "annotator_id": "annotator_a",
    "primary_playstyle": "planner",
    "secondary_playstyles": ["resource_diversifier"],
    "confidence": 0.8,
    "evidence": "첫 block_place 전에 inventory_change와 item_craft가 선행됨"
  },
  {
    "annotator_id": "annotator_b",
    "primary_playstyle": "planner",
    "secondary_playstyles": [],
    "confidence": 0.7,
    "evidence": "건축 시작 전 준비 구간이 뚜렷함"
  },
  {
    "annotator_id": "annotator_c",
    "primary_playstyle": "route_optimizer",
    "secondary_playstyles": ["planner"],
    "confidence": 0.6,
    "evidence": "이동 경로가 직선적이고 효율적으로 보임"
  }
]
```

`labels.primary_playstyle`가 없으면 검증 스크립트는 `annotations[].primary_playstyle`의 majority vote를 기준 라벨로 사용하고, 라벨러 간 pairwise agreement도 계산합니다.

### 4. 라벨 기준 검증 실행

```bash
PYTHONPATH=backend python3 backend/validate_playstyle_categories.py \
  --dataset datasets/validation/real_playstyle_sessions_unlabeled.json \
  --output datasets/public/real_playstyle_validation_report.json
```

결과에는 다음이 포함됩니다.

- 라벨 기준 정확도
- confusion table
- 실패 사례
- 카테고리별 점수
- annotator vote count
- pairwise annotator agreement

자세한 수집 프로토콜은 [`docs/PLAYSTYLE_DATA_COLLECTION_PROTOCOL.md`](docs/PLAYSTYLE_DATA_COLLECTION_PROTOCOL.md)를 참고하세요.

## 🐳 Docker 실행

Python/Node.js 환경 없이 Docker만으로 백엔드를 실행할 수 있습니다.

### 사전 요구사항
- Docker 설치 ([Docker Desktop](https://www.docker.com/products/docker-desktop/) 권장)

### 빌드 및 실행

```bash
# 1. Docker 이미지 빌드
docker build -t abc-backend .

# 2. 컨테이너 실행
docker run -p 8080:8080 abc-backend

# 3. 헬스체크 (다른 터미널에서)
curl http://localhost:8080/health
# 또는 브라우저에서 http://localhost:8080/docs 접속
```

### 환경 변수 설정

```bash
# 환경 변수와 함께 실행
docker run -p 8080:8080 \
  -e LOG_LEVEL=DEBUG \
  -e CORS_ORIGINS="http://localhost:5173" \
  abc-backend
```

### 개발 모드 (볼륨 마운트)

```bash
# 코드 변경 시 컨테이너 재시작 없이 반영 (개발용)
docker run -p 8080:8080 \
  -v $(pwd)/backend:/app \
  abc-backend
```

### 트러블슈팅

| 문제 | 해결 방법 |
|------|----------|
| 포트 충돌 | `-p 8081:8080`으로 다른 포트 사용 |
| 빌드 실패 | `docker build --no-cache -t abc-backend .` |
| 권한 오류 | `sudo docker ...` 또는 Docker 그룹에 사용자 추가 |

## ☁️ Cloud Run 배포

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

## License

MIT License
