/**
 * BehaviorTracker 단위 테스트
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { BehaviorTracker } from '../utils/BehaviorTracker';

describe('BehaviorTracker', () => {
    let tracker: BehaviorTracker;

    beforeEach(() => {
        tracker = new BehaviorTracker();
    });

    it('should start a session', () => {
        tracker.startSession();
        const profile = tracker.getBehavioralProfile();
        expect(profile).toBeDefined();
    });

    it('should record mouse movement', () => {
        tracker.startSession();
        tracker.recordMouseMove(100, 200);
        tracker.recordMouseMove(150, 250);
        
        const profile = tracker.getBehavioralProfile();
        expect(profile.pathEfficiency).toBeGreaterThan(0);
    });

    it('should record decision latency', () => {
        tracker.startSession();
        const startTime = Date.now();
        
        // 의사결정 시뮬레이션
        setTimeout(() => {
            tracker.recordDecision();
        }, 100);
        
        const profile = tracker.getBehavioralProfile();
        expect(profile.avgDecisionLatency).toBeGreaterThanOrEqual(0);
    });

    it('should record revisions', () => {
        tracker.startSession();
        tracker.recordRevision();
        tracker.recordRevision();
        
        const profile = tracker.getBehavioralProfile();
        expect(profile.revisionRate).toBe(2);
    });

    it('should calculate path efficiency correctly', () => {
        tracker.startSession();
        
        // 직선 경로 (효율적)
        tracker.recordMouseMove(0, 0);
        tracker.recordMouseMove(100, 0);
        tracker.recordMouseMove(200, 0);
        
        const profile1 = tracker.getBehavioralProfile();
        const efficiency1 = profile1.pathEfficiency;
        
        // 복잡한 경로 (비효율적)
        tracker.startSession();
        tracker.recordMouseMove(0, 0);
        tracker.recordMouseMove(50, 50);
        tracker.recordMouseMove(100, -50);
        tracker.recordMouseMove(200, 0);
        
        const profile2 = tracker.getBehavioralProfile();
        const efficiency2 = profile2.pathEfficiency;
        
        // 직선 경로가 더 효율적이어야 함
        expect(efficiency1).toBeGreaterThan(efficiency2);
    });

    it('should generate valid behavioral profile', () => {
        tracker.startSession();
        tracker.recordMouseMove(100, 200);
        tracker.recordDecision();
        tracker.recordRevision();
        
        const profile = tracker.getBehavioralProfile();
        
        expect(profile).toHaveProperty('pathEfficiency');
        expect(profile).toHaveProperty('avgDecisionLatency');
        expect(profile).toHaveProperty('revisionRate');
        expect(profile).toHaveProperty('jitterIndex');
        expect(profile).toHaveProperty('intensity');
        
        // 값 범위 검증
        expect(profile.pathEfficiency).toBeGreaterThanOrEqual(0);
        expect(profile.pathEfficiency).toBeLessThanOrEqual(1);
        expect(profile.avgDecisionLatency).toBeGreaterThanOrEqual(0);
        expect(profile.revisionRate).toBeGreaterThanOrEqual(0);
    });
});
