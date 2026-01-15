"""
생체신호 통합 모듈
실제 EEG, HRV 등 생체신호 센서와의 연동을 위한 인터페이스

지원 센서:
- OpenBCI (EEG)
- NeuroSky MindWave
- Polar H10 (HRV)
- Web Audio API (오디오 분석)
"""
import os
import numpy as np
from typing import Dict, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class BiosignalIntegration:
    """
    생체신호 통합 클래스
    다양한 센서로부터 실시간 생체신호를 수집하고 처리
    """
    
    def __init__(self):
        self.eeg_enabled = False
        self.hrv_enabled = False
        self.audio_enabled = False
        self.callbacks: Dict[str, Callable] = {}
    
    def enable_eeg(self, device_type: str = "openbci", port: Optional[str] = None):
        """
        EEG 센서 활성화
        
        Args:
            device_type: "openbci" 또는 "neurosky"
            port: 시리얼 포트 또는 WebSocket URL
        """
        try:
            if device_type == "openbci":
                # OpenBCI 통합 (향후 구현)
                logger.info("OpenBCI EEG integration (placeholder)")
                self.eeg_enabled = True
            elif device_type == "neurosky":
                # NeuroSky 통합 (향후 구현)
                logger.info("NeuroSky EEG integration (placeholder)")
                self.eeg_enabled = True
            else:
                logger.warning(f"Unknown EEG device type: {device_type}")
        except Exception as e:
            logger.error(f"Failed to enable EEG: {e}")
            self.eeg_enabled = False
    
    def enable_hrv(self, device_type: str = "polar", port: Optional[str] = None):
        """
        HRV (Heart Rate Variability) 센서 활성화
        
        Args:
            device_type: "polar" 또는 "fitbit"
            port: 블루투스 주소 또는 API 키
        """
        try:
            if device_type == "polar":
                # Polar H10 통합 (향후 구현)
                logger.info("Polar H10 HRV integration (placeholder)")
                self.hrv_enabled = True
            else:
                logger.warning(f"Unknown HRV device type: {device_type}")
        except Exception as e:
            logger.error(f"Failed to enable HRV: {e}")
            self.hrv_enabled = False
    
    def enable_audio_analysis(self):
        """
        Web Audio API를 통한 오디오 분석 활성화
        프론트엔드에서 오디오 스트림을 분석
        """
        self.audio_enabled = True
        logger.info("Audio analysis enabled (Web Audio API)")
    
    def get_eeg_features(self) -> Optional[Dict]:
        """
        현재 EEG 특징 추출
        
        Returns:
            {"theta": float, "beta": float, "alpha": float, "gamma": float} 또는 None
        """
        if not self.eeg_enabled:
            return None
        
        # 실제 구현에서는 센서로부터 데이터 읽기
        # 현재는 플레이스홀더
        return {
            "theta": 0.5,
            "beta": 0.5,
            "alpha": 0.3,
            "gamma": 0.2,
            "source": "synthetic"
        }
    
    def get_hrv_features(self) -> Optional[Dict]:
        """
        HRV 특징 추출
        
        Returns:
            {"rmssd": float, "sdnn": float, "hr": float} 또는 None
        """
        if not self.hrv_enabled:
            return None
        
        # 실제 구현에서는 센서로부터 데이터 읽기
        return {
            "rmssd": 50.0,  # ms
            "sdnn": 45.0,   # ms
            "hr": 70.0,     # bpm
            "source": "synthetic"
        }
    
    def process_audio_stream(self, audio_data: np.ndarray, sample_rate: int = 44100) -> Dict:
        """
        오디오 스트림 분석
        
        Args:
            audio_data: 오디오 샘플 배열
            sample_rate: 샘플링 레이트
        
        Returns:
            {"valence": float, "arousal": float, "emotion": str}
        """
        if not self.audio_enabled:
            return {"valence": 0.5, "arousal": 0.5, "emotion": "neutral"}
        
        # 간단한 오디오 특징 추출
        # 실제로는 더 정교한 분석 필요 (MFCC, Spectral features 등)
        energy = np.mean(np.abs(audio_data))
        spectral_centroid = self._calculate_spectral_centroid(audio_data, sample_rate)
        
        # 에너지와 스펙트럼 중심으로 감정 추정
        valence = min(1.0, energy * 2)
        arousal = min(1.0, spectral_centroid / 2000)
        
        emotion = self._classify_emotion(valence, arousal)
        
        return {
            "valence": valence,
            "arousal": arousal,
            "emotion": emotion,
            "energy": energy,
            "spectral_centroid": spectral_centroid
        }
    
    def _calculate_spectral_centroid(self, audio_data: np.ndarray, sample_rate: int) -> float:
        """스펙트럼 중심 계산 (간단한 버전)"""
        # FFT 계산
        fft = np.fft.fft(audio_data)
        magnitude = np.abs(fft)
        frequencies = np.fft.fftfreq(len(audio_data), 1/sample_rate)
        
        # 양의 주파수만 사용
        positive_freq_idx = frequencies > 0
        frequencies = frequencies[positive_freq_idx]
        magnitude = magnitude[positive_freq_idx]
        
        # 스펙트럼 중심
        if np.sum(magnitude) > 0:
            centroid = np.sum(frequencies * magnitude) / np.sum(magnitude)
        else:
            centroid = 0
        
        return centroid
    
    def _classify_emotion(self, valence: float, arousal: float) -> str:
        """감정 분류 (Valence-Arousal 모델)"""
        if valence > 0.6 and arousal > 0.6:
            return "happy"
        elif valence < 0.4 and arousal > 0.6:
            return "angry"
        elif valence < 0.4 and arousal < 0.4:
            return "sad"
        elif valence > 0.6 and arousal < 0.4:
            return "calm"
        else:
            return "neutral"
    
    def register_callback(self, signal_type: str, callback: Callable):
        """
        생체신호 콜백 등록
        
        Args:
            signal_type: "eeg", "hrv", "audio"
            callback: 신호 수신 시 호출될 함수
        """
        self.callbacks[signal_type] = callback
        logger.info(f"Registered callback for {signal_type}")


# 전역 인스턴스
_biosignal_integration: Optional[BiosignalIntegration] = None


def get_biosignal_integration() -> BiosignalIntegration:
    """생체신호 통합 인스턴스 가져오기"""
    global _biosignal_integration
    
    if _biosignal_integration is None:
        _biosignal_integration = BiosignalIntegration()
        
        # 환경 변수로 센서 활성화
        if os.getenv("ENABLE_EEG", "false").lower() == "true":
            device_type = os.getenv("EEG_DEVICE", "openbci")
            _biosignal_integration.enable_eeg(device_type)
        
        if os.getenv("ENABLE_HRV", "false").lower() == "true":
            device_type = os.getenv("HRV_DEVICE", "polar")
            _biosignal_integration.enable_hrv(device_type)
        
        # 오디오는 항상 활성화 가능
        if os.getenv("ENABLE_AUDIO_ANALYSIS", "false").lower() == "true":
            _biosignal_integration.enable_audio_analysis()
    
    return _biosignal_integration


if __name__ == "__main__":
    # 테스트
    integration = get_biosignal_integration()
    print(f"EEG enabled: {integration.eeg_enabled}")
    print(f"HRV enabled: {integration.hrv_enabled}")
    print(f"Audio enabled: {integration.audio_enabled}")
