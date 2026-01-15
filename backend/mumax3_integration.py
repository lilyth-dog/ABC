"""
MuMax3 물리 시뮬레이션 통합 모듈
실제 MuMax3 엔진과의 연동을 위한 인터페이스 제공

참고: 실제 MuMax3 연동을 위해서는:
1. MuMax3 설치 필요 (https://mumax.github.io/)
2. Python 바인딩 또는 gRPC 서버 필요
3. 또는 Docker 컨테이너로 MuMax3 실행
"""
import os
import subprocess
import json
import numpy as np
from typing import Dict, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class MuMax3Integration:
    """
    MuMax3 물리 시뮬레이션 통합 클래스
    
    현재는 시뮬레이션 준비 및 인터페이스만 제공.
    실제 MuMax3 연동은 환경 설정에 따라 활성화 가능.
    """
    
    def __init__(self, mumax3_path: Optional[str] = None, enable_realtime: bool = False):
        """
        MuMax3 통합 초기화
        
        Args:
            mumax3_path: MuMax3 실행 파일 경로 (None이면 자동 감지)
            enable_realtime: 실시간 계산 활성화 여부 (기본: False, Pre-computed 사용)
        """
        self.mumax3_path = mumax3_path or self._find_mumax3()
        self.enable_realtime = enable_realtime
        self.temp_dir = Path(__file__).parent / "mumax3_temp"
        self.temp_dir.mkdir(exist_ok=True)
        
        if self.mumax3_path and os.path.exists(self.mumax3_path):
            logger.info(f"MuMax3 found at: {self.mumax3_path}")
            self.available = True
        else:
            logger.warning("MuMax3 not found. Using pre-computed patterns.")
            self.available = False
    
    def _find_mumax3(self) -> Optional[str]:
        """시스템에서 MuMax3 실행 파일 찾기"""
        common_paths = [
            "/usr/local/bin/mumax3",
            "/opt/mumax3/mumax3",
            "C:\\Program Files\\MuMax3\\mumax3.exe",
            os.path.expanduser("~/mumax3/mumax3"),
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        # 환경 변수에서 확인
        env_path = os.getenv("MUMAX3_PATH")
        if env_path and os.path.exists(env_path):
            return env_path
        
        return None
    
    def generate_mumax3_script(
        self, 
        theta: float, 
        beta: float, 
        output_file: str
    ) -> str:
        """
        MuMax3 스크립트 생성
        
        Args:
            theta: Theta 파워 (0-1)
            beta: Beta 파워 (0-1)
            output_file: 출력 파일 경로
        
        Returns:
            생성된 MuMax3 스크립트 내용
        """
        # 물리 파라미터 계산
        alpha = 0.01 + 0.05 * theta  # Gilbert damping
        b_ext_magnitude = 0.05 * beta  # External field magnitude
        freq = 5 + 15 * beta  # Excitation frequency (GHz)
        
        script = f"""
// MuMax3 Script for Neuro-Twin Simulation
// Generated for theta={theta:.3f}, beta={beta:.3f}

SetGridSize(128, 128, 1)
SetCellSize(10e-9, 10e-9, 10e-9)

// Material parameters
Msat = 800e3  // Saturation magnetization (A/m)
Aex = 13e-12  // Exchange constant (J/m)
alpha = {alpha:.4f}  // Gilbert damping

// External field (Beta -> Excitation)
B_ext = vector(0, 0, {b_ext_magnitude:.4f})  // Tesla

// Initial magnetization
m = uniform(1, 0, 0)

// Time evolution
t = 0
dt = 1e-12  // 1 ps
steps = 1000

// Run simulation
for i = 0; i < steps; i++ {{
    relax()
    t += dt
}}

// Save output
save(m, "{output_file}")
"""
        return script
    
    def run_simulation(self, theta: float, beta: float) -> Optional[np.ndarray]:
        """
        MuMax3 시뮬레이션 실행
        
        Args:
            theta: Theta 파워
            beta: Beta 파워
        
        Returns:
            자기 상태 배열 (128x128) 또는 None (실패 시)
        """
        if not self.available:
            logger.warning("MuMax3 not available, skipping real-time simulation")
            return None
        
        if not self.enable_realtime:
            logger.debug("Real-time simulation disabled, using pre-computed")
            return None
        
        try:
            # 임시 스크립트 파일 생성
            script_file = self.temp_dir / f"sim_{theta:.3f}_{beta:.3f}.mx3"
            output_file = self.temp_dir / f"output_{theta:.3f}_{beta:.3f}.ovf"
            
            script = self.generate_mumax3_script(theta, beta, str(output_file))
            
            with open(script_file, 'w') as f:
                f.write(script)
            
            # MuMax3 실행
            result = subprocess.run(
                [self.mumax3_path, str(script_file)],
                capture_output=True,
                text=True,
                timeout=30  # 30초 타임아웃
            )
            
            if result.returncode != 0:
                logger.error(f"MuMax3 simulation failed: {result.stderr}")
                return None
            
            # 결과 파일 읽기 (OVF 형식)
            logger.info(f"MuMax3 simulation completed: {output_file}")
            
            # OVF 파일 파싱
            try:
                from ovf_parser import get_ovf_parser
                parser = get_ovf_parser()
                ovf_data = parser.parse_ovf(str(output_file))
                
                if ovf_data is not None:
                    # z-성분 추출 (2D 시각화용)
                    magnetic_state = parser.extract_z_component(ovf_data)
                    if magnetic_state is not None:
                        logger.info(f"OVF file parsed successfully: shape {magnetic_state.shape}")
                        return magnetic_state
                    else:
                        # 크기 추출
                        magnetic_state = parser.extract_magnetization_magnitude(ovf_data)
                        if magnetic_state is not None and len(magnetic_state.shape) == 2:
                            logger.info(f"OVF file parsed successfully: shape {magnetic_state.shape}")
                            return magnetic_state
                
                logger.warning("OVF parsing returned None, falling back to pre-computed")
                return None
            except ImportError:
                logger.warning("OVF parser not available, falling back to pre-computed")
                return None
            except Exception as e:
                logger.error(f"OVF parsing error: {e}, falling back to pre-computed")
                return None
            
        except subprocess.TimeoutExpired:
            logger.error("MuMax3 simulation timeout")
            return None
        except Exception as e:
            logger.error(f"MuMax3 simulation error: {e}")
            return None
    
    def get_physics_metadata(self, theta: float, beta: float) -> Dict:
        """
        물리 메타데이터 반환
        
        Args:
            theta: Theta 파워
            beta: Beta 파워
        
        Returns:
            물리 파라미터 딕셔너리
        """
        alpha = 0.01 + 0.05 * theta
        b_ext = 0.05 * beta
        freq = 5 + 15 * beta
        
        return {
            "source": "mumax3" if self.available and self.enable_realtime else "precomputed",
            "alpha": alpha,
            "b_ext": b_ext,
            "frequency_ghz": freq,
            "theta": theta,
            "beta": beta,
            "realtime_enabled": self.enable_realtime and self.available
        }


# 전역 인스턴스 (선택적)
_mumax3_integration: Optional[MuMax3Integration] = None


def get_mumax3_integration() -> MuMax3Integration:
    """MuMax3 통합 인스턴스 가져오기 (싱글톤)"""
    global _mumax3_integration
    
    if _mumax3_integration is None:
        enable_realtime = os.getenv("MUMAX3_REALTIME", "false").lower() == "true"
        _mumax3_integration = MuMax3Integration(enable_realtime=enable_realtime)
    
    return _mumax3_integration


if __name__ == "__main__":
    # 테스트
    integration = MuMax3Integration(enable_realtime=False)
    print(f"MuMax3 available: {integration.available}")
    print(f"Real-time enabled: {integration.enable_realtime}")
    
    # 메타데이터 테스트
    metadata = integration.get_physics_metadata(0.5, 0.5)
    print(f"Physics metadata: {metadata}")
