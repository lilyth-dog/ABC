/**
 * Neural Physics Engine
 * Implementation of the Kuramoto Model for Coupled Oscillators.
 */

interface UpdateResult {
    phases: Float32Array;
    coherence: number;
    meanPhase: number;
}

class NeuralEngine {
    private N: number;
    private phases: Float32Array;
    private frequencies: Float32Array;
    private K: number;
    private dt: number;

    constructor(numNeurons = 100) {
        this.N = numNeurons;
        this.phases = new Float32Array(this.N);
        this.frequencies = new Float32Array(this.N);
        this.K = 0;
        this.dt = 0.05;

        this.initialize();
    }

    private initialize(): void {
        for (let i = 0; i < this.N; i++) {
            this.phases[i] = Math.random() * Math.PI * 2;

            const u1 = Math.random();
            const u2 = Math.random();
            const z = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
            this.frequencies[i] = 1.0 + z * 0.2;
        }
    }

    setCoupling(k: number): void {
        this.K = k;
    }

    update(): UpdateResult {
        const newPhases = new Float32Array(this.N);
        let coherenceReal = 0;
        let coherenceImag = 0;

        for (let i = 0; i < this.N; i++) {
            coherenceReal += Math.cos(this.phases[i]);
            coherenceImag += Math.sin(this.phases[i]);
        }

        const meanReal = coherenceReal / this.N;
        const meanImag = coherenceImag / this.N;
        const r = Math.sqrt(meanReal * meanReal + meanImag * meanImag);
        const psi = Math.atan2(meanImag, meanReal);

        for (let i = 0; i < this.N; i++) {
            const dTheta = this.frequencies[i] + this.K * r * Math.sin(psi - this.phases[i]);
            newPhases[i] = this.phases[i] + dTheta * this.dt;
        }

        this.phases = newPhases;

        return {
            phases: this.phases,
            coherence: r,
            meanPhase: psi
        };
    }
}

export default NeuralEngine;
