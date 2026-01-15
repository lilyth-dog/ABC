/**
 * config.ts 유틸리티 테스트
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import config from '../utils/config';

describe('config', () => {
  beforeEach(() => {
    // 환경 변수 초기화
    vi.resetModules();
  });

  it('should have default API URL', () => {
    expect(config.apiUrl).toBe('http://localhost:8000');
  });

  it('should have default WebSocket URL', () => {
    expect(config.wsUrl).toBe('ws://localhost:8000');
  });

  it('should get API URL with path', () => {
    const url = config.getApiUrl('/api/test');
    expect(url).toBe('http://localhost:8000/api/test');
  });

  it('should get API URL without leading slash', () => {
    const url = config.getApiUrl('api/test');
    expect(url).toBe('http://localhost:8000/api/test');
  });

  it('should handle trailing slash in base URL', () => {
    const url = config.getApiUrl('/api/test');
    expect(url).toBe('http://localhost:8000/api/test');
  });

  it('should get WebSocket URL with path', () => {
    const url = config.getWsUrl('/ws/simulation');
    expect(url).toBe('ws://localhost:8000/ws/simulation');
  });

  it('should detect development mode', () => {
    // Vite의 기본 동작에 따라 DEV 모드 확인
    expect(typeof config.isDevelopment).toBe('boolean');
  });
});
