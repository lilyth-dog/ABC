"""
Neuro-Twin FastAPI Server with WebSocket Support
Connects React frontend to MagnonicController backend

API Documentation available at: /docs (Swagger UI) or /redoc (ReDoc)
"""
import asyncio
import json
import os
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from neuro_controller import MagnonicController, ContinuousLearner
from user_profiles import UserProfileManager
from tess_loader import TESSDataLoader
from motion_generator import EmotionalMotionGenerator
from logger_config import logger, log_request, log_error, log_websocket_event
from env_validator import validate_environment
from biosignal_integration import get_biosignal_integration
from predictive_model import get_predictive_model
from game_behavior_processor import GameBehaviorProcessor, GameBehavioralData
from game_event_parser import parse_game_events

# 환경 변수 검증 (애플리케이션 시작 시)
validate_environment()

# 생체신호 통합 초기화
biosignal = get_biosignal_integration()

# 예측 모델 초기화
predictive_model = get_predictive_model()

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize core components
controller = MagnonicController()
profile_manager = UserProfileManager()
tess_loader = TESSDataLoader()
motion_generator = EmotionalMotionGenerator()

# Try to load TESS dataset if available
try:
    tess_count = tess_loader.load()
    logger.info(f"TESS Dataset loaded: {tess_count} samples")
except Exception as e:
    logger.warning(f"TESS Dataset not found or error loading: {e}")
    tess_count = 0

# API Metadata for Swagger documentation
tags_metadata = [
    {
        "name": "health",
        "description": "Server health and status endpoints",
    },
    {
        "name": "privacy",
        "description": "GDPR/PIPA compliant privacy management - data consent, export, and deletion",
    },
    {
        "name": "behavior",
        "description": "Behavioral profile processing and personality inference",
    },
    {
        "name": "learning",
        "description": "Continuous learning and session management",
    },
    {
        "name": "websocket",
        "description": "Real-time WebSocket connections for simulation streaming",
    },
]

app = FastAPI(
    title="Neuro-Twin API",
    description="""
# Behavioral Digital Human Twin API

This API powers the Neuro-Twin application, enabling:

- **Real-time behavioral analysis** from user interactions
- **Personality inference** using the BehavioralPersonalityDecoder
- **Continuous learning** that evolves user profiles over time
- **GDPR/PIPA compliance** with data export and deletion

## Key Features

- 🧠 Neural physics simulation with EEG-to-kinematics mapping
- 👤 Behavioral Digital Twin creation and evolution
- 🔒 Privacy-first design with explicit consent management
- 🌍 Cultural bias mitigation with configurable weights

## Authentication

Currently, this API uses user IDs for identification. Future versions will implement OAuth2.
    """,
    version="2.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Rate Limiter 적용
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration from environment variables
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://localhost:5180"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize continuous learning (controller and profile_manager already initialized above)
continuous_learner = ContinuousLearner(learning_rate=0.3)


# ============== REQUEST/RESPONSE MODELS ==============

class SimulationRequest(BaseModel):
    """Request model for simulation parameters."""
    theta: float = Field(0.5, ge=0, le=1, description="Theta wave strength (0-1)")
    beta: float = Field(0.5, ge=0, le=1, description="Beta wave strength (0-1)")
    action: Optional[str] = Field(None, description="Optional action type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "theta": 0.7,
                "beta": 0.3,
                "action": "walk"
            }
        }

class BehavioralProfile(BaseModel):
    """User behavioral profile for personality inference."""
    pathEfficiency: float = Field(..., ge=0, le=1, description="Path efficiency score")
    avgDecisionLatency: float = Field(..., ge=0, description="Average decision latency in ms")
    revisionRate: int = Field(..., ge=0, description="Number of revisions made")
    jitterIndex: float = Field(0.0, description="Mouse movement jitter index")
    intensity: float = Field(0.5, description="Interaction intensity")
    contextualChoices: Optional[dict] = Field(None, description="User's contextual choices (aesthetics, etc)")
    taskCompletion: Optional[float] = Field(0.0, description="Task completion rate")
    culturalContext: Optional[str] = Field(None, description="Cultural context for bias adjustment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pathEfficiency": 0.85,
                "avgDecisionLatency": 2500,
                "revisionRate": 2,
                "jitterIndex": 0.15,
                "intensity": 0.7,
                "contextualChoices": {"aesthetics": "Cyber/Industrial"},
                "taskCompletion": 0.9,
                "culturalContext": "east_asian"
            }
        }

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Server status")
    controller: str = Field(..., description="Controller status")

class ConsentRecord(BaseModel):
    """Individual consent settings."""
    behavioralTracking: bool = Field(False, description="Allow behavioral data collection")
    profileStorage: bool = Field(False, description="Allow profile storage")
    continuousLearning: bool = Field(False, description="Allow cross-session learning")

class ConsentRequest(BaseModel):
    """Request model for saving consent."""
    consent_record: ConsentRecord
    timestamp: str = Field(..., description="ISO timestamp of consent")
    
    class Config:
        json_schema_extra = {
            "example": {
                "consent_record": {
                    "behavioralTracking": True,
                    "profileStorage": True,
                    "continuousLearning": False
                },
                "timestamp": "2026-01-14T15:00:00Z"
            }
        }


@app.get("/health", response_model=HealthResponse, tags=["health"])
@limiter.limit("100/minute")
async def health_check(request: Request):
    """
    Check server health status.
    
    Returns the current status of the API server and the neural controller.
    """
    logger.debug("Health check requested")
    return {"status": "ok", "controller": "ready"}


@app.post("/api/simulate")
@limiter.limit("60/minute")
async def simulate(request: Request, sim_request: SimulationRequest):
    """Single simulation request"""
    try:
        log_request("POST", "/api/simulate", user_id=None, action=sim_request.action)
        if sim_request.action:
            result = controller.simulate_action_pattern(sim_request.action)
        else:
            result = controller.process_eeg_stream(sim_request.theta, sim_request.beta)
        return result
    except Exception as e:
        log_error(e, "simulate")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")


@app.post("/api/behavior")
@limiter.limit("30/minute")
async def process_behavior(request: Request, profile: BehavioralProfile):
    """Process behavioral interaction metrics"""
    try:
        user_id = profile.contextualChoices.get("user_id") if profile.contextualChoices else None
        log_request("POST", "/api/behavior", user_id=user_id)
        result = controller.process_behavioral_profile(profile.dict())
        return result
    except Exception as e:
        log_error(e, "process_behavior")
        raise HTTPException(status_code=500, detail=f"Behavior processing failed: {str(e)}")


@app.get("/api/behavior/sample/{emotion}")
async def get_sample_behavior(emotion: str):
    """
    Get a sample behavioral profile derived from real emotional audio (TESS).
    Useful for testing the digital twin with specific emotional states.
    """
    if tess_count == 0:
        raise HTTPException(status_code=404, detail="TESS dataset not loaded")
    
    try:
        samples = tess_loader.get_random_samples(n=1, emotion=emotion)
        if not samples:
            raise HTTPException(status_code=404, detail=f"No samples found for emotion: {emotion}")
        
        sample = samples[0]
        profile = tess_loader.to_behavioral_profile(sample)
        audio_features = tess_loader.get_audio_features(sample["path"])
        
        # Generate 3D motion modifiers based on the emotional profile
        motion_data = motion_generator.generate_modifiers(profile)
        
        return {
            "profile": profile,
            "motion_modifiers": motion_data,
            "sample_info": {
                "actor": sample["actor"],
                "emotion": sample["emotion"],
                "word": sample["word"]
            },
            "audio_metrics": audio_features
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== CONTINUOUS LEARNING ENDPOINTS ==============

class SessionData(BaseModel):
    user_id: str
    behavioral_profile: dict

class GameRawEventsData(BaseModel):
    """게임 원시 이벤트 데이터 (1단계 입력)"""
    user_id: str
    game_id: str = Field(..., description="게임 ID (minecraft, stardew_valley, animal_crossing)")
    session_id: str
    raw_events: List[Dict] = Field(..., description="원시 게임 이벤트 리스트")

class GameSessionData(BaseModel):
    """게임에서 수집한 세션 데이터 (2-3단계 입력)"""
    user_id: str
    game_id: str = Field(..., description="게임 ID (minecraft, stardew_valley, animal_crossing)")
    session_id: str
    decision_latency: float = Field(0, ge=0)
    planning_time: float = Field(0, ge=0)
    revision_count: int = Field(0, ge=0)
    path_efficiency: float = Field(0.5, ge=0, le=1)
    task_efficiency: float = Field(0.5, ge=0, le=1)
    complexity: float = Field(0.5, ge=0, le=1)
    diversity: float = Field(0.5, ge=0, le=1)
    game_specific_metrics: dict = Field(default_factory=dict)

@app.post("/api/game/events")
@limiter.limit("30/minute")
async def process_game_raw_events(request: Request, data: GameRawEventsData):
    """
    게임 원시 이벤트를 받아서 파싱하고 성격 특성을 추론합니다.
    
    입력: 원시 게임 이벤트 리스트
    처리: 1) 이벤트 파싱 → 2) 메트릭 계산 → 3) 프로필 변환 → 4) 성격 추론
    """
    log_request("POST", "/api/game/events", user_id=data.user_id)
    try:
        # 1단계: 원시 이벤트 파싱 및 메트릭 계산
        metrics = parse_game_events(data.game_id, data.raw_events)
        
        # 2단계: 메트릭을 표준 프로필로 변환
        game_processor = GameBehaviorProcessor()
        game_behavior = GameBehavioralData(
            game_id=data.game_id,
            session_id=data.session_id,
            decision_latency=0,  # 게임은 실시간이므로 0
            planning_time=metrics.get("planning_time", 0),
            revision_count=metrics.get("revision_count", 0),
            path_efficiency=metrics.get("path_efficiency", 0.5),
            task_efficiency=0.8,  # 기본값 또는 계산
            complexity=metrics.get("complexity", 0.5),
            diversity=metrics.get("diversity", 0.5),
            game_specific_metrics={
                "riskTaking": metrics.get("risk_taking", 0.5),
                **metrics  # 기타 메트릭 포함
            }
        )
        
        behavioral_profile = game_processor.process(game_behavior)
        
        # 3단계: 표준 세션 저장 프로세스 사용
        session_id = profile_manager.save_session(data.user_id, behavioral_profile)
        previous = profile_manager.get_latest_profile(data.user_id)
        user_data = profile_manager.get_or_create_user(data.user_id)
        maturity_level = user_data.get("maturity_level", 1)
        
        behavioral_profile["maturityLevel"] = maturity_level
        result = controller.process_behavioral_profile(behavioral_profile)
        new_weights = result.get("behavioral_traits", {}).get("weights", {})
        sync_score = result.get("sync_score", 0.0)
        
        if previous:
            current_weights = {
                "Logic": previous.get("logic_weight", 0.5),
                "Intuition": previous.get("intuition_weight", 0.5),
                "Fluidity": previous.get("fluidity_weight", 0.5),
                "Complexity": previous.get("complexity_weight", 0.5)
            }
            updated_weights = continuous_learner.update_weights(current_weights, new_weights)
        else:
            updated_weights = new_weights
        
        archetype = continuous_learner.generate_archetype(updated_weights)
        history = profile_manager.get_session_history(data.user_id)
        confidence = continuous_learner.compute_confidence(len(history), 0.7)
        
        profile_manager.save_profile_evolution(
            data.user_id, updated_weights, archetype, confidence
        )
        
        return {
            "session_id": session_id,
            "game_id": data.game_id,
            "parsed_metrics": metrics,  # 파싱된 메트릭 반환
            "updated_weights": updated_weights,
            "archetype": archetype,
            "confidence": confidence,
            "sync_score": sync_score
        }
    except Exception as e:
        log_error(e, "process_game_raw_events", user_id=data.user_id)
        raise HTTPException(status_code=500, detail=f"Game events processing failed: {str(e)}")


@app.post("/api/game/session")
@limiter.limit("30/minute")
async def save_game_session(request: Request, data: GameSessionData):
    """
    게임에서 수집한 행동 데이터를 처리하고 성격 특성을 추론합니다.
    
    지원 게임:
    - minecraft: 마인크래프트
    - stardew_valley: 스타듀밸리
    - animal_crossing: 두근두근타운
    """
    log_request("POST", "/api/game/session", user_id=data.user_id)
    try:
        # 게임 데이터를 표준 행동 프로필로 변환
        game_processor = GameBehaviorProcessor()
        game_behavior = GameBehavioralData(
            game_id=data.game_id,
            session_id=data.session_id,
            decision_latency=data.decision_latency,
            planning_time=data.planning_time,
            revision_count=data.revision_count,
            path_efficiency=data.path_efficiency,
            task_efficiency=data.task_efficiency,
            complexity=data.complexity,
            diversity=data.diversity,
            game_specific_metrics=data.game_specific_metrics
        )
        
        behavioral_profile = game_processor.process(game_behavior)
        
        # 표준 세션 저장 프로세스 사용
        session_data = SessionData(
            user_id=data.user_id,
            behavioral_profile=behavioral_profile
        )
        
        # 기존 save_session 로직 재사용
        session_id = profile_manager.save_session(data.user_id, behavioral_profile)
        previous = profile_manager.get_latest_profile(data.user_id)
        user_data = profile_manager.get_or_create_user(data.user_id)
        maturity_level = user_data.get("maturity_level", 1)
        
        behavioral_profile["maturityLevel"] = maturity_level
        result = controller.process_behavioral_profile(behavioral_profile)
        new_weights = result.get("behavioral_traits", {}).get("weights", {})
        sync_score = result.get("sync_score", 0.0)
        
        if previous:
            current_weights = {
                "Logic": previous.get("logic_weight", 0.5),
                "Intuition": previous.get("intuition_weight", 0.5),
                "Fluidity": previous.get("fluidity_weight", 0.5),
                "Complexity": previous.get("complexity_weight", 0.5)
            }
            updated_weights = continuous_learner.update_weights(current_weights, new_weights)
        else:
            updated_weights = new_weights
        
        archetype = continuous_learner.generate_archetype(updated_weights)
        history = profile_manager.get_session_history(data.user_id)
        confidence = continuous_learner.compute_confidence(len(history), 0.7)
        
        profile_manager.save_profile_evolution(
            data.user_id, updated_weights, archetype, confidence
        )
        
        return {
            "session_id": session_id,
            "game_id": data.game_id,
            "updated_weights": updated_weights,
            "archetype": archetype,
            "confidence": confidence,
            "sync_score": sync_score,
            "game_specific": behavioral_profile.get("gameSpecific", {})
        }
    except Exception as e:
        log_error(e, "save_game_session", user_id=data.user_id)
        raise HTTPException(status_code=500, detail=f"Game session processing failed: {str(e)}")


@app.post("/api/session")
@limiter.limit("20/minute")
async def save_session(request: Request, data: SessionData):
    """
    Save a behavioral session for continuous learning.
    Returns updated profile weights after EMA update.
    """
    log_request("POST", "/api/session", user_id=data.user_id)
    try:
        # Save raw session
        session_id = profile_manager.save_session(data.user_id, data.behavioral_profile)
        
        # Get previous profile
        previous = profile_manager.get_latest_profile(data.user_id)
        
        # Get current user status (maturity level)
        user_data = profile_manager.get_or_create_user(data.user_id)
        maturity_level = user_data.get("maturity_level", 1)
        
        # Process behavioral traits with maturity context
        behavior_data = data.behavioral_profile.dict()
        behavior_data["maturityLevel"] = maturity_level
        
        result = controller.process_behavioral_profile(behavior_data)
        new_weights = result.get("behavioral_traits", {}).get("weights", {})
        sync_score = result.get("sync_score", 0.0)
        
        # Apply continuous learning update
        if previous:
            current_weights = {
                "Logic": previous.get("logic_weight", 0.5),
                "Intuition": previous.get("intuition_weight", 0.5),
                "Fluidity": previous.get("fluidity_weight", 0.5),
                "Complexity": previous.get("complexity_weight", 0.5)
            }
            updated_weights = continuous_learner.update_weights(current_weights, new_weights)
        else:
            updated_weights = new_weights
        
        # Generate archetype
        archetype = continuous_learner.generate_archetype(updated_weights)
        
        # Get session count for confidence
        history = profile_manager.get_session_history(data.user_id)
        confidence = continuous_learner.compute_confidence(len(history), 0.7)
        
        # Save evolved profile
        profile_manager.save_profile_evolution(
            data.user_id, updated_weights, archetype, confidence
        )
        
        # Maturity Advancement Logic
        new_level = maturity_level
        if maturity_level == 1 and len(history) >= 3 and sync_score >= 0.6:
            new_level = 2
        elif maturity_level == 2 and len(history) >= 7 and sync_score >= 0.8:
            new_level = 3
        
        if new_level != maturity_level:
            profile_manager.update_user_maturity(data.user_id, new_level, sync_score)
        else:
            # Just update sync score
            profile_manager.update_user_maturity(data.user_id, maturity_level, sync_score)
        
        # 생체신호 데이터 처리 (오디오 분석)
        audio_analysis = behavior_data.get("audioAnalysis")
        if audio_analysis:
            # 오디오 분석 결과를 행동 프로필에 반영
            biosignal.process_audio_stream(
                np.array([]),  # 실제 오디오 데이터는 프론트엔드에서 이미 분석됨
                sample_rate=44100
            )
        
        # 예측 모델링 및 이상 감지
        sessions = profile_manager.get_session_history(data.user_id, limit=10)
        current_session_data = {
            "avg_decision_latency": behavior_data.get("avgDecisionLatency", 0),
            "revision_rate": behavior_data.get("revisionRate", 0),
            "path_efficiency": behavior_data.get("pathEfficiency", 1.0),
            "raw_metrics": json.dumps(behavior_data),
            "audio_analysis": audio_analysis  # 오디오 분석 데이터 포함
        }
        
        stress_analysis = predictive_model.detect_stress_pattern(sessions, current_session_data)
        anomaly_detection = predictive_model.detect_anomaly(sessions, current_session_data)
        behavior_trend = predictive_model.predict_behavioral_trend(sessions + [current_session_data])
        
        # 알림 트리거 (스트레스, 이상 감지, 레벨업)
        notifications = []
        if stress_analysis.get("stress_level", 0) > 0.6:
            notifications.append({
                "type": "stress",
                "severity": "high",
                "title": "높은 스트레스 감지",
                "message": stress_analysis.get("recommendation", "충분한 휴식이 필요합니다.")
            })
        if anomaly_detection.get("has_anomaly", False):
            notifications.append({
                "type": "anomaly",
                "severity": "high",
                "title": "이상 행동 감지",
                "message": anomaly_detection.get("recommendation", "이상 행동 패턴이 감지되었습니다.")
            })
        if new_level > maturity_level:
            notifications.append({
                "type": "level_up",
                "severity": "low",
                "title": "레벨 업!",
                "message": f"디지털 트윈이 Tier {new_level} ({['Echo', 'Reflection', 'Synthesis'][new_level - 1]})로 진화했습니다!"
            })
        
        return {
            "session_id": session_id,
            "weights": updated_weights,
            "archetype": archetype,
            "confidence": confidence,
            "session_count": len(history),
            "maturity_level": new_level,
            "sync_score": sync_score,
            "level_up": new_level > maturity_level,
            "is_new_user": previous is None,
            "predictive_insights": {
                "stress_analysis": stress_analysis,
                "anomaly_detection": anomaly_detection,
                "behavior_trend": behavior_trend
            },
            "notifications": notifications
        }
    except Exception as e:
        log_error(e, "save_session", user_id=data.user_id)
        raise HTTPException(status_code=500, detail=f"Session save failed: {str(e)}")


@app.get("/api/profile/{user_id}")
async def get_profile(user_id: str):
    """Get latest cumulative profile for a user."""
    profile = profile_manager.get_latest_profile(user_id)
    sessions = profile_manager.get_session_history(user_id, limit=5)
    
    if not profile:
        return {"status": "no_profile", "user_id": user_id}
    
    return {
        "user_id": user_id,
        "profile": profile,
        "recent_sessions": len(sessions),
        "maturity_level": profile.get("maturity_level", 1) if profile else 1,
        "sync_score": profile.get("sync_score", 0.0) if profile else 0.0,
        "archetype": profile.get("archetype", "Unknown") if profile else "Unknown"
    }


@app.get("/api/insights/{user_id}")
@limiter.limit("30/minute")
async def get_predictive_insights(request: Request, user_id: str):
    """Get predictive insights for a user (stress, trends, anomalies)"""
    log_request("GET", f"/api/insights/{user_id}", user_id=user_id)
    try:
        sessions = profile_manager.get_session_history(user_id, limit=10)
        
        if len(sessions) < 1:
            return {
                "status": "insufficient_data",
                "message": "최소 1개 세션이 필요합니다",
                "sessions_needed": 1
            }
        
        # 최근 세션 데이터
        latest_session = sessions[-1] if sessions else {}
        
        # 현재 세션 데이터 준비
        current_session_data = {
            "avg_decision_latency": latest_session.get("avg_decision_latency", 0),
            "revision_rate": latest_session.get("revision_rate", 0),
            "path_efficiency": latest_session.get("path_efficiency", 1.0),
            "raw_metrics": latest_session.get("raw_metrics", "{}")
        }
        
        # 예측 모델링 실행
        stress_analysis = predictive_model.detect_stress_pattern(sessions[:-1] if len(sessions) > 1 else [], current_session_data)
        anomaly_detection = predictive_model.detect_anomaly(sessions[:-1] if len(sessions) > 1 else [], current_session_data)
        behavior_trend = predictive_model.predict_behavioral_trend(sessions)
        
        return {
            "status": "success",
            "stress_analysis": stress_analysis,
            "anomaly_detection": anomaly_detection,
            "behavior_trend": behavior_trend
        }
    except Exception as e:
        log_error(e, "get_predictive_insights", user_id=user_id)
        raise HTTPException(status_code=500, detail=f"Insights retrieval failed: {str(e)}")


@app.get("/api/evolution/{user_id}")
@limiter.limit("30/minute")
async def get_evolution(request: Request, user_id: str):
    """Get personality weight evolution over time for visualization."""
    log_request("GET", f"/api/evolution/{user_id}", user_id=user_id)
    try:
        evolution = profile_manager.get_profile_evolution(user_id)
        
        if not evolution:
            return {"status": "no_history", "user_id": user_id}
        
        # Calculate drift
        drift = continuous_learner.calculate_drift(evolution)
        
        # 예측 모델링 추가
        prediction = predictive_model.predict_personality_evolution(evolution, forecast_days=30)
        
        return {
            "user_id": user_id,
            "evolution": evolution,
            "drift_analysis": drift,
            "data_points": len(evolution),
            "prediction": prediction
        }
    except Exception as e:
        log_error(e, "get_evolution", user_id=user_id)
        raise HTTPException(status_code=500, detail=f"Evolution analysis failed: {str(e)}")


# ============== GDPR PRIVACY MANAGEMENT ENDPOINTS ==============

class ConsentData(BaseModel):
    consent_record: dict
    timestamp: str

@app.post("/api/user/{user_id}/consent")
async def save_consent(user_id: str, data: ConsentData):
    """
    Save user consent record (GDPR compliance).
    """
    consent_id = profile_manager.save_consent(
        user_id, 
        data.consent_record
    )
    return {
        "status": "saved",
        "consent_id": consent_id,
        "user_id": user_id
    }


@app.get("/api/user/{user_id}/export")
async def export_user_data(user_id: str):
    """
    GDPR Article 20 - Right to Data Portability.
    Export all user data in machine-readable format.
    """
    data = profile_manager.export_user_data(user_id)
    return data


@app.delete("/api/user/{user_id}")
async def delete_user_data(user_id: str):
    """
    GDPR Article 17 - Right to be Forgotten.
    Permanently delete all user data.
    """
    result = profile_manager.delete_user_data(user_id)
    return result


@app.get("/api/user/{user_id}/consent")
async def get_consent(user_id: str):
    """Get latest consent status for a user."""
    consent = profile_manager.get_latest_consent(user_id)
    if not consent:
        return {"status": "no_consent", "user_id": user_id}
    return {
        "status": "found",
        "user_id": user_id,
        "consent": consent
    }


@app.websocket("/ws/simulation")
async def websocket_simulation(websocket: WebSocket):
    """
    WebSocket endpoint for real-time EEG -> Kinematics streaming.
    
    Client sends: {"theta": 0.5, "beta": 0.5} or {"action": "WALK"}
    Server responds: {"joint_angles": [...], "fluidity_index": 0.8, ...}
    """
    await websocket.accept()
    client_id = f"{websocket.client.host}:{websocket.client.port}" if websocket.client else "unknown"
    log_websocket_event("connected", client_id=client_id)
    
    try:
        while True:
            # Receive EEG parameters from client
            data = await websocket.receive_text()
            try:
                params = json.loads(data)
            except json.JSONDecodeError as e:
                log_error(e, "websocket_json_parse", user_id=client_id)
                await websocket.send_json({"error": "Invalid JSON format", "detail": str(e)})
                continue
            
            try:
                # Process through MagnonicController
                if "action" in params:
                    result = controller.simulate_action_pattern(params["action"])
                elif "behavior_profile" in params:
                    result = controller.process_behavioral_profile(params["behavior_profile"])
                else:
                    theta = params.get("theta", 0.5)
                    beta = params.get("beta", 0.5)
                    result = controller.process_eeg_stream(theta, beta)
                
                # Send kinematics back to client
                await websocket.send_json(result)
            except Exception as e:
                log_error(e, "websocket_processing", user_id=client_id)
                await websocket.send_json({"error": "Processing failed", "detail": str(e)})
            
            # Rate limit to ~30 FPS
            await asyncio.sleep(0.033)
            
    except WebSocketDisconnect:
        log_websocket_event("disconnected", client_id=client_id)
    except Exception as e:
        log_error(e, "websocket_connection", user_id=client_id)
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass


@app.websocket("/ws/stream")
async def websocket_auto_stream(websocket: WebSocket):
    """
    Auto-streaming mode: Server pushes simulation data continuously.
    Useful for demo/visualization without user input.
    """
    await websocket.accept()
    client_id = f"{websocket.client.host}:{websocket.client.port}" if websocket.client else "unknown"
    log_websocket_event("auto_stream_connected", client_id=client_id)
    
    actions = ["STAND", "WALK", "RUN", "WALK", "STAND"]
    action_idx = 0
    frame_count = 0
    
    try:
        while True:
            # Cycle through actions every 50 frames (~1.5s each)
            if frame_count % 50 == 0:
                action_idx = (action_idx + 1) % len(actions)
            
            action = actions[action_idx]
            result = controller.simulate_action_pattern(action)
            result["current_action"] = action
            
            await websocket.send_json(result)
            frame_count += 1
            
            # ~30 FPS
            await asyncio.sleep(0.033)
            
    except WebSocketDisconnect:
        log_websocket_event("auto_stream_disconnected", client_id=client_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
