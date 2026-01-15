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
├── public/             # 정적 파일
└── package.json
```

## 🔧 Environment Variables

`.env.production` 파일에서 환경 변수를 설정합니다.

## 📄 License

MIT License
