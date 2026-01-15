# Nexus Entertainment

> The Future of Digital Human Twins and Virtual Idols

디지털 트윈과 버추얼 아이돌을 위한 차세대 플랫폼. 하이퍼 리얼리스틱 아바타를 생성하고 메타버스에서 활동하세요.

## 🚀 Features

- **Avatar Creator** - Ready Player Me 통합 아바타 생성
- **Identity Configurator** - AI 기반 페르소나 설정
- **3D World** - Three.js 기반 인터랙티브 월드
- **Analytics Dashboard** - 실시간 분석 대시보드
- **Neuro Controller** - 뉴럴 커플링 시스템

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
│   ├── api_server.py   # FastAPI 서버
│   ├── neuro_controller.py
│   └── simulation_db.py
├── datasets/           # 데이터셋 파일 (GitHub에 제외됨)
│   ├── README.md       # 데이터셋 사용 가이드
│   └── .gitkeep        # 폴더 구조 유지
├── public/             # 정적 파일
└── package.json
```

## 🔧 Environment Variables

`.env.production` 파일에서 환경 변수를 설정합니다.

## 📄 License

MIT License
