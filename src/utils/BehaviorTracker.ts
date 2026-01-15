/**
 * BehaviorTracker.ts
 * Captures user interaction patterns to infer personality traits.
 */

export interface InteractionMetrics {
    lastMoveTime: number;
    mousePathLength: number;
    clickCount: number;
    startTime: number;
    stepStartTime: number;
    decisionLatencies: number[];
    velocityPeaks: number[];
    revisionCount: number;
    jitterSum: number;
    contextualChoices: {
        aesthetics?: string;
        primaryTrait?: string;
        traitWeights?: Record<string, number>;
    };
}

class BehaviorTracker {
    private metrics: InteractionMetrics = {
        lastMoveTime: Date.now(),
        mousePathLength: 0,
        clickCount: 0,
        startTime: Date.now(),
        stepStartTime: Date.now(),
        decisionLatencies: [],
        velocityPeaks: [],
        revisionCount: 0,
        jitterSum: 0,
        contextualChoices: {}
    };

    private lastPos: { x: number; y: number } | null = null;

    /**
     * Start/Reset tracking for a specific session
     */
    public startSession() {
        this.metrics = {
            lastMoveTime: Date.now(),
            mousePathLength: 0,
            clickCount: 0,
            startTime: Date.now(),
            stepStartTime: Date.now(),
            decisionLatencies: [],
            velocityPeaks: [],
            revisionCount: 0,
            jitterSum: 0
        };
        this.lastPos = null;
    }

    /**
     * Call this when a significant decision step is completed
     */
    public recordStepCompletion() {
        const now = Date.now();
        const latency = now - this.metrics.stepStartTime;
        this.metrics.decisionLatencies.push(latency);
        this.metrics.stepStartTime = now;
    }

    /**
     * Call this whenever a user changes a previously made choice
     */
    public recordRevision() {
        this.metrics.revisionCount++;
    }

    /**
     * Record a specific contextual choice
     */
    public recordChoice(key: keyof InteractionMetrics['contextualChoices'], value: any) {
        this.metrics.contextualChoices[key] = value;
    }

    /**
     * Hook into mouse movement
     */
    public trackMovement(x: number, y: number) {
        const now = Date.now();
        if (this.lastPos) {
            const dx = x - this.lastPos.x;
            const dy = y - this.lastPos.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const dt = now - this.metrics.lastMoveTime || 1;

            this.metrics.mousePathLength += dist;

            // Velocity peak tracking
            const velocity = dist / dt;
            if (velocity > 5) { // Threshold for "fast" movement
                this.metrics.velocityPeaks.push(velocity);
            }

            // Jitter/Directness tracking (Sudden direction changes)
            // Simplified: adding up movements that are very small but frequent
            if (dist > 0 && dist < 10) {
                this.metrics.jitterSum += 1;
            }
        }
        this.lastPos = { x, y };
        this.metrics.lastMoveTime = now;
    }

    public recordClick() {
        this.metrics.clickCount++;
    }

    /**
     * Summarize data for backend consumption
     */
    public getBehavioralProfile() {
        const totalTime = Date.now() - this.metrics.startTime;
        const avgLatency = this.metrics.decisionLatencies.length > 0
            ? this.metrics.decisionLatencies.reduce((a, b) => a + b, 0) / this.metrics.decisionLatencies.length
            : 0;

        return {
            pathEfficiency: this.metrics.mousePathLength / (totalTime || 1),
            avgDecisionLatency: avgLatency,
            revisionRate: this.metrics.revisionCount,
            jitterIndex: this.metrics.jitterSum / (this.metrics.mousePathLength || 1),
            intensity: this.metrics.velocityPeaks.length > 0
                ? Math.max(...this.metrics.velocityPeaks)
                : 0,
            contextualChoices: this.metrics.contextualChoices
        };
    }
}

export const tracker = new BehaviorTracker();
