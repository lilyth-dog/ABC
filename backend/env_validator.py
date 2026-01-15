"""
환경 변수 검증 모듈
애플리케이션 시작 시 필수 환경 변수 확인
"""
import os
import sys
from typing import List, Tuple


class EnvValidator:
    """환경 변수 검증 클래스"""
    
    REQUIRED_VARS = []  # 현재는 선택사항만 있음
    
    OPTIONAL_VARS = {
        "CORS_ORIGINS": "http://localhost:5173,http://localhost:3000,http://localhost:5180",
        "LOG_LEVEL": "INFO",
        "PORT": "8000",
        "VITE_API_URL": "http://localhost:8000",
        "VITE_WS_URL": "ws://localhost:8000"
    }
    
    @classmethod
    def validate(cls, strict: bool = False) -> Tuple[bool, List[str]]:
        """
        환경 변수 검증
        
        Args:
            strict: True면 필수 변수가 없으면 에러
        
        Returns:
            (is_valid, missing_vars)
        """
        missing = []
        warnings = []
        
        # 필수 변수 검증
        for var in cls.REQUIRED_VARS:
            if not os.getenv(var):
                missing.append(var)
        
        # 선택사항 변수 경고 (개발 모드)
        if not strict:
            for var, default in cls.OPTIONAL_VARS.items():
                if not os.getenv(var):
                    warnings.append(f"{var} not set, using default: {default}")
        
        if missing and strict:
            return False, missing
        
        return True, warnings
    
    @classmethod
    def print_summary(cls):
        """환경 변수 설정 요약 출력"""
        print("\n" + "="*50)
        print("환경 변수 설정 요약")
        print("="*50)
        
        for var, default in cls.OPTIONAL_VARS.items():
            value = os.getenv(var, default)
            status = "✅" if os.getenv(var) else "⚠️ (기본값)"
            print(f"{status} {var}: {value}")
        
        print("="*50 + "\n")


def validate_environment():
    """애플리케이션 시작 시 환경 변수 검증"""
    is_valid, warnings = EnvValidator.validate(strict=False)
    
    if warnings:
        print("\n⚠️ 환경 변수 경고:")
        for warning in warnings:
            print(f"  - {warning}")
        print("  프로덕션 배포 시 환경 변수를 명시적으로 설정하세요.\n")
    
    EnvValidator.print_summary()
    
    return is_valid


if __name__ == "__main__":
    validate_environment()
