"""
구조화된 로깅 시스템 설정
프로덕션 환경에서 안전하고 유용한 로깅을 제공
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime

# 로그 레벨 환경 변수에서 가져오기
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# 로그 디렉토리 생성
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 로그 포맷 정의
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# JSON 포맷 (구조화된 로깅용, 선택사항)
JSON_LOG_FORMAT = {
    "timestamp": "%(asctime)s",
    "logger": "%(name)s",
    "level": "%(levelname)s",
    "message": "%(message)s",
    "module": "%(module)s",
    "function": "%(funcName)s",
    "line": "%(lineno)d"
}


def setup_logger(name: str = "neuro_twin", log_to_file: bool = True) -> logging.Logger:
    """
    구조화된 로거 설정
    
    Args:
        name: 로거 이름
        log_to_file: 파일 로깅 활성화 여부
    
    Returns:
        설정된 Logger 인스턴스
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    
    # 기존 핸들러 제거 (중복 방지)
    logger.handlers.clear()
    
    # 콘솔 핸들러 (항상 활성화)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 파일 핸들러 (선택사항)
    if log_to_file:
        log_file = os.path.join(LOG_DIR, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # 파일에는 더 상세한 로그
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # 프로파게이션 방지 (루트 로거에 중복 전달 방지)
    logger.propagate = False
    
    return logger


# 기본 로거 인스턴스 생성
logger = setup_logger("neuro_twin")

# 보안: 민감한 정보 마스킹 헬퍼
def mask_sensitive_data(data: dict) -> dict:
    """
    로그에 기록하기 전 민감한 정보 마스킹
    
    Args:
        data: 마스킹할 데이터 딕셔너리
    
    Returns:
        마스킹된 데이터 딕셔너리
    """
    sensitive_keys = ['password', 'token', 'secret', 'api_key', 'authorization']
    masked = data.copy()
    
    for key in masked.keys():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            masked[key] = "***MASKED***"
    
    return masked


# 로깅 헬퍼 함수
def log_request(method: str, path: str, user_id: str = None, **kwargs):
    """API 요청 로깅"""
    extra_info = f" | user_id: {user_id}" if user_id else ""
    logger.info(f"API Request: {method} {path}{extra_info}", extra=kwargs)


def log_error(error: Exception, context: str = "", user_id: str = None):
    """에러 로깅"""
    extra_info = f" | user_id: {user_id}" if user_id else ""
    logger.error(
        f"Error in {context}: {str(error)}{extra_info}",
        exc_info=True
    )


def log_websocket_event(event: str, client_id: str = None, **kwargs):
    """WebSocket 이벤트 로깅"""
    extra_info = f" | client: {client_id}" if client_id else ""
    logger.info(f"WebSocket {event}{extra_info}", extra=kwargs)
