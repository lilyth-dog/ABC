/**
 * 생체신호 수집 Hook
 * Web Audio API를 통한 오디오 분석 및 향후 센서 연동
 */
import { useState, useEffect, useRef, useCallback } from 'react';

interface BiosignalData {
    eeg?: {
        theta: number;
        beta: number;
        alpha: number;
        gamma: number;
    };
    audio?: {
        valence: number;
        arousal: number;
        emotion: string;
        energy: number;
    };
    hrv?: {
        rmssd: number;
        sdnn: number;
        hr: number;
    };
}

interface UseBiosignalReturn {
    data: BiosignalData | null;
    isRecording: boolean;
    startRecording: () => void;
    stopRecording: () => void;
    error: string | null;
}

export const useBiosignal = (enableAudio: boolean = true): UseBiosignalReturn => {
    const [data, setData] = useState<BiosignalData | null>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const audioContextRef = useRef<AudioContext | null>(null);
    const analyserRef = useRef<AnalyserNode | null>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const animationFrameRef = useRef<number | null>(null);

    const startRecording = useCallback(async () => {
        if (!enableAudio) {
            setError('Audio analysis is disabled');
            return;
        }

        try {
            // 마이크 접근
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            streamRef.current = stream;

            // AudioContext 생성
            const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
            audioContextRef.current = audioContext;

            // AnalyserNode 생성
            const analyser = audioContext.createAnalyser();
            analyser.fftSize = 2048;
            analyserRef.current = analyser;

            // 마이크 입력을 analyser에 연결
            const source = audioContext.createMediaStreamSource(stream);
            source.connect(analyser);

            setIsRecording(true);
            setError(null);

            // 오디오 분석 루프
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);

            const analyze = () => {
                if (!analyserRef.current || !isRecording) return;

                analyserRef.current.getByteTimeDomainData(dataArray);

                // 간단한 특징 추출
                let sum = 0;
                for (let i = 0; i < bufferLength; i++) {
                    const normalized = (dataArray[i] - 128) / 128;
                    sum += Math.abs(normalized);
                }
                const energy = sum / bufferLength;

                // FFT로 주파수 분석
                const fftArray = new Uint8Array(bufferLength);
                analyserRef.current.getByteFrequencyData(fftArray);

                // 스펙트럼 중심 계산
                let weightedSum = 0;
                let magnitudeSum = 0;
                const sampleRate = audioContext.sampleRate;
                
                for (let i = 0; i < bufferLength; i++) {
                    const magnitude = fftArray[i];
                    const frequency = (i * sampleRate) / (2 * bufferLength);
                    weightedSum += frequency * magnitude;
                    magnitudeSum += magnitude;
                }
                
                const spectralCentroid = magnitudeSum > 0 ? weightedSum / magnitudeSum : 0;

                // 감정 추정
                const valence = Math.min(1.0, energy * 2);
                const arousal = Math.min(1.0, spectralCentroid / 2000);
                
                let emotion = 'neutral';
                if (valence > 0.6 && arousal > 0.6) emotion = 'happy';
                else if (valence < 0.4 && arousal > 0.6) emotion = 'angry';
                else if (valence < 0.4 && arousal < 0.4) emotion = 'sad';
                else if (valence > 0.6 && arousal < 0.4) emotion = 'calm';

                setData({
                    audio: {
                        valence,
                        arousal,
                        emotion,
                        energy,
                        spectralCentroid
                    }
                });

                animationFrameRef.current = requestAnimationFrame(analyze);
            };

            analyze();

        } catch (err) {
            setError((err as Error).message);
            setIsRecording(false);
        }
    }, [enableAudio, isRecording]);

    const stopRecording = useCallback(() => {
        if (animationFrameRef.current) {
            cancelAnimationFrame(animationFrameRef.current);
            animationFrameRef.current = null;
        }

        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }

        if (audioContextRef.current) {
            audioContextRef.current.close();
            audioContextRef.current = null;
        }

        analyserRef.current = null;
        setIsRecording(false);
    }, []);

    useEffect(() => {
        return () => {
            stopRecording();
        };
    }, [stopRecording]);

    return {
        data,
        isRecording,
        startRecording,
        stopRecording,
        error
    };
};

export default useBiosignal;
