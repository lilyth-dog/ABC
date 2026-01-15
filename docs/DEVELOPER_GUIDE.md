# 🛠️ Developer Guide

## Nexus Entertainment - Behavioral Digital Human Twin

---

## 📖 Table of Contents

1. [Project Structure](#project-structure)
2. [Development Setup](#development-setup)
3. [Architecture Overview](#architecture-overview)
4. [API Reference](#api-reference)
5. [Component Guide](#component-guide)
6. [Testing](#testing)
7. [Performance Optimization](#performance-optimization)
8. [Contributing](#contributing)

---

## Project Structure

```
ABC/
├── backend/                    # Python FastAPI backend
│   ├── api_server.py          # Main API server
│   ├── neuro_controller.py    # Neural physics & personality decoder
│   ├── user_profiles.py       # User data management (GDPR)
│   ├── cultural_weights.json  # Cultural bias configuration
│   └── tests/                 # Backend tests
├── src/                       # React frontend
│   ├── components/            # React components
│   ├── hooks/                 # Custom React hooks
│   ├── utils/                 # Utility functions
│   ├── tests/                 # Frontend tests
│   ├── App.tsx               # Main application
│   └── index.css             # Global styles
├── docs/                      # Documentation
├── public/                    # Static assets
└── package.json              # Node.js dependencies
```

---

## Development Setup

### Prerequisites

- Node.js 18+
- Python 3.10+
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/lilyth-dog/ABC.git
cd ABC

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install test dependencies
pip install -r backend/tests/requirements-test.txt
```

### Running Development Server

```bash
# Run both frontend and backend
npm run dev

# Or run separately
npm run dev:frontend  # Vite on port 5173
npm run dev:backend   # FastAPI on port 8000
```

### API Documentation

Once the backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Architecture Overview

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ BehaviorTracker│ │ UI Components │ │ Three.js 3D  │      │
│  └──────┬───────┘  └──────────────┘  └──────────────┘      │
│         │                                                   │
└─────────┼───────────────────────────────────────────────────┘
          │ WebSocket / REST API
┌─────────▼───────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ PersonalityDecoder│ │ ContinuousLearner│ │ UserProfileManager│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────┐
│                     DATABASE (SQLite)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    users     │  │  sessions    │  │   consents   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Description |
|-----------|-------------|
| `BehaviorTracker` | Collects user interaction data |
| `BehavioralPersonalityDecoder` | Infers personality from behavior |
| `ContinuousLearner` | Updates weights using EMA |
| `UserProfileManager` | GDPR-compliant data management |

---

## API Reference

### Health Check
```
GET /health
Response: { "status": "ok", "controller": "ready" }
```

### Privacy Endpoints

```
POST /api/user/{user_id}/consent
Body: { "consent_record": {...}, "timestamp": "..." }

GET /api/user/{user_id}/consent
Response: { "status": "found", "consent": {...} }

GET /api/user/{user_id}/export
Response: Full user data export (JSON)

DELETE /api/user/{user_id}
Response: { "status": "deleted", ... }
```

### Behavioral Processing

```
POST /api/behavior
Body: { "pathEfficiency": 0.8, "avgDecisionLatency": 2000, ... }
Response: { "synthetic_theta": 0.5, "behavioral_traits": {...} }

POST /api/session
Body: { "user_id": "...", "behavioral_profile": {...} }
Response: { "weights": {...}, "archetype": "..." }
```

### WebSocket

```
WS /ws/simulation
Messages: { "theta": 0.5, "beta": 0.5 }
Response: Continuous kinematic data stream
```

---

## Component Guide

### Core Components

| Component | Location | Description |
|-----------|----------|-------------|
| `App.tsx` | `src/` | Main application router |
| `PrivacyConsent.tsx` | `src/components/` | GDPR consent UI |
| `WelcomeSequence.tsx` | `src/components/` | First-visit animation |
| `IdentityConfigurator.tsx` | `src/components/` | Anima Weaving flow |
| `CultureSelector.tsx` | `src/components/` | Cultural context picker |
| `WorldScene.tsx` | `src/components/` | 3D world environment |

### Custom Hooks

| Hook | Description |
|------|-------------|
| `useNeuroStream` | WebSocket connection to backend |
| `useAudio` | Audio playback with AudioContext |

### Utilities

| Utility | Description |
|---------|-------------|
| `BehaviorTracker` | User interaction tracking |
| `NeuralEngine` | Kuramoto model simulation |

---

## Testing

### Frontend Tests

```bash
# Run all tests
npm run test

# Watch mode
npm run test:watch

# With coverage
npm run test:coverage

# UI mode
npm run test:ui
```

### Backend Tests

```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Run tests
npm run test:backend
# or
cd backend && python -m pytest tests/ -v
```

### Test Files

| File | Coverage |
|------|----------|
| `PrivacyConsent.test.tsx` | Consent UI & API |
| `WelcomeSequence.test.tsx` | Animation & callbacks |
| `CultureSelector.test.tsx` | Dropdown & selection |
| `test_user_profiles.py` | GDPR functions |
| `test_api.py` | API endpoints |

---

## Performance Optimization

### Bundle Splitting

The project uses manual chunks for optimal loading:

```javascript
manualChunks: {
  'react-vendor': ['react', 'react-dom'],
  'three-vendor': ['three', '@react-three/fiber', '@react-three/drei'],
  'charts': ['recharts'],
  'icons': ['lucide-react'],
}
```

### Build Analysis

```bash
npm run build:analyze
```

### Best Practices

1. **Lazy Loading**: Use `React.lazy()` for route-based splitting
2. **Memoization**: Use `React.memo()`, `useMemo()`, `useCallback()`
3. **Image Optimization**: Use WebP format
4. **Console Removal**: Production builds strip `console.log`

---

## Contributing

### Code Style

- TypeScript for frontend
- Python 3.10+ for backend
- ESLint for JS/TS linting

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for new features
4. Ensure all tests pass
5. Submit PR with clear description

### Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Test changes
- `perf:` Performance improvement

---

## License

This project is proprietary software. All rights reserved.

---

## Contact

For questions or support, please contact the development team.
