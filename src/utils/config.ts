/**
 * 환경 변수 설정 유틸리티
 * 모든 API URL과 설정을 중앙에서 관리
 */

export const config = {
  // API Base URL
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  
  // WebSocket URL
  wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:8000',
  
  // 환경 모드
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  
  // API 엔드포인트 헬퍼 함수
  getApiUrl: (path: string) => {
    const baseUrl = config.apiUrl.replace(/\/$/, ''); // trailing slash 제거
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    return `${baseUrl}${cleanPath}`;
  },
  
  // WebSocket 엔드포인트 헬퍼 함수
  getWsUrl: (path: string) => {
    const baseUrl = config.wsUrl.replace(/\/$/, '');
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    return `${baseUrl}${cleanPath}`;
  }
};

// 환경 변수 검증 (개발 모드에서만)
if (config.isDevelopment) {
  if (!import.meta.env.VITE_API_URL) {
    console.warn('[Config] VITE_API_URL이 설정되지 않았습니다. 기본값(localhost:8000)을 사용합니다.');
  }
}

export default config;
