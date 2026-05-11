import { useState, useCallback, useEffect, useRef } from 'react';
import { useAudio } from './AudioManager';

interface WelcomeSequenceProps {
    onComplete: () => void;
}

const WELCOME_MESSAGES = [
    "당신의 영혼을 기다려왔습니다...",
    "We've been waiting for your soul...",
    "디지털 트윈이 깨어납니다",
    "Your Digital Twin Awakens"
];
const TYPING_INTERVAL_MS = 60;
const PHASE_PAUSE_MS = 1500;
const COMPLETION_PAUSE_MS = 2000;
const TOTAL_WELCOME_DURATION_MS = WELCOME_MESSAGES.reduce(
    (total, message) => total + (message.length + 2) * TYPING_INTERVAL_MS + PHASE_PAUSE_MS,
    COMPLETION_PAUSE_MS
);

const WelcomeSequence = ({ onComplete }: WelcomeSequenceProps) => {
    const { playChime } = useAudio();
    const playChimeRef = useRef(playChime);
    const onCompleteRef = useRef(onComplete);
    const completedRef = useRef(false);
    const [phase, setPhase] = useState(0);
    const [displayText, setDisplayText] = useState('');
    const [showParticles, setShowParticles] = useState(false);

    useEffect(() => {
        playChimeRef.current = playChime;
    }, [playChime]);

    useEffect(() => {
        onCompleteRef.current = onComplete;
    }, [onComplete]);

    const completeOnce = useCallback(() => {
        if (completedRef.current) {
            return;
        }
        completedRef.current = true;
        onCompleteRef.current();
    }, []);

    useEffect(() => {
        const fallbackTimeout = window.setTimeout(() => {
            setShowParticles(true);
            completeOnce();
        }, TOTAL_WELCOME_DURATION_MS);

        return () => window.clearTimeout(fallbackTimeout);
    }, [completeOnce]);

    // Typing animation effect
    useEffect(() => {
        if (phase >= WELCOME_MESSAGES.length) {
            setShowParticles(true);
            const completeTimeout = window.setTimeout(completeOnce, COMPLETION_PAUSE_MS);
            return () => window.clearTimeout(completeTimeout);
        }

        const message = WELCOME_MESSAGES[phase];
        let charIndex = 0;
        let phaseTimeout: number | undefined;
        setDisplayText('');

        const interval = window.setInterval(() => {
            if (charIndex <= message.length) {
                setDisplayText(message.slice(0, charIndex));
                if (charIndex > 0 && message[charIndex - 1] !== ' ') {
                    playChimeRef.current(800 + Math.random() * 400, 'sine', 0.03);
                }
                charIndex++;
            } else {
                window.clearInterval(interval);
                phaseTimeout = window.setTimeout(() => setPhase(p => p + 1), PHASE_PAUSE_MS);
            }
        }, TYPING_INTERVAL_MS);

        return () => {
            window.clearInterval(interval);
            if (phaseTimeout) {
                window.clearTimeout(phaseTimeout);
            }
        };
    }, [phase, completeOnce]);

    return (
        <div className="welcome-overlay">
            <div className="welcome-content">
                {/* Animated background particles */}
                <div className="particle-field">
                    {Array.from({ length: 50 }).map((_, i) => (
                        <div
                            key={i}
                            className="particle"
                            style={{
                                left: `${Math.random() * 100}%`,
                                animationDelay: `${Math.random() * 5}s`,
                                animationDuration: `${5 + Math.random() * 10}s`
                            }}
                        />
                    ))}
                </div>

                {/* Central glowing orb */}
                <div className={`soul-orb ${showParticles ? 'awakening' : ''}`}>
                    <div className="orb-core" />
                    <div className="orb-ring ring-1" />
                    <div className="orb-ring ring-2" />
                    <div className="orb-ring ring-3" />
                </div>

                {/* Typed message */}
                <div className="welcome-message">
                    <p className={`message ${phase % 2 === 0 ? 'korean' : 'english'}`}>
                        {displayText}
                        <span className="cursor">|</span>
                    </p>
                </div>

                {/* Progress indicator */}
                <div className="welcome-progress">
                    {WELCOME_MESSAGES.map((_, i) => (
                        <div
                            key={i}
                            className={`progress-dot ${i <= phase ? 'active' : ''}`}
                        />
                    ))}
                </div>

                {showParticles && (
                    <div className="ascension-particles">
                        {Array.from({ length: 30 }).map((_, i) => (
                            <div
                                key={i}
                                className="ascension-particle"
                                style={{
                                    left: `${30 + Math.random() * 40}%`,
                                    animationDelay: `${Math.random() * 0.5}s`
                                }}
                            />
                        ))}
                    </div>
                )}
            </div>

            <style dangerouslySetInnerHTML={{
                __html: `
                .welcome-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background: radial-gradient(ellipse at center, #0a0015 0%, #000 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 9999;
                    overflow: hidden;
                }
                .welcome-content {
                    text-align: center;
                    position: relative;
                }
                .particle-field {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                }
                .particle {
                    position: absolute;
                    width: 3px;
                    height: 3px;
                    background: var(--neon-cyan);
                    border-radius: 50%;
                    bottom: -10px;
                    opacity: 0;
                    animation: floatUp 10s infinite;
                }
                @keyframes floatUp {
                    0% { opacity: 0; transform: translateY(0) scale(0); }
                    10% { opacity: 0.8; }
                    90% { opacity: 0.3; }
                    100% { opacity: 0; transform: translateY(-100vh) scale(1); }
                }
                .soul-orb {
                    width: 200px;
                    height: 200px;
                    position: relative;
                    margin: 0 auto 60px;
                    transition: all 1s ease;
                }
                .soul-orb.awakening {
                    transform: scale(1.5);
                    filter: brightness(2);
                }
                .orb-core {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 60px;
                    height: 60px;
                    background: radial-gradient(circle, #fff 0%, var(--neon-magenta) 50%, transparent 100%);
                    border-radius: 50%;
                    transform: translate(-50%, -50%);
                    box-shadow: 0 0 60px var(--neon-magenta), 0 0 120px var(--neon-cyan);
                    animation: corePulse 2s infinite ease-in-out;
                }
                @keyframes corePulse {
                    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
                    50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
                }
                .orb-ring {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    border: 2px solid var(--neon-cyan);
                    border-radius: 50%;
                    transform: translate(-50%, -50%);
                    opacity: 0.5;
                }
                .ring-1 {
                    width: 100px;
                    height: 100px;
                    animation: ringPulse 3s infinite;
                }
                .ring-2 {
                    width: 140px;
                    height: 140px;
                    animation: ringPulse 3s infinite 0.5s;
                }
                .ring-3 {
                    width: 180px;
                    height: 180px;
                    animation: ringPulse 3s infinite 1s;
                }
                @keyframes ringPulse {
                    0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
                    50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.2; }
                }
                .welcome-message {
                    min-height: 80px;
                }
                .message {
                    font-size: 1.8rem;
                    font-weight: 300;
                    letter-spacing: 2px;
                    color: white;
                    margin: 0;
                    text-shadow: 0 0 20px var(--neon-cyan);
                }
                .message.korean {
                    font-family: 'Noto Sans KR', 'Outfit', sans-serif;
                }
                .cursor {
                    animation: blink 0.8s infinite;
                    color: var(--neon-magenta);
                }
                @keyframes blink {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0; }
                }
                .welcome-progress {
                    display: flex;
                    gap: 12px;
                    justify-content: center;
                    margin-top: 40px;
                }
                .progress-dot {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.2);
                    transition: all 0.5s ease;
                }
                .progress-dot.active {
                    background: var(--neon-magenta);
                    box-shadow: 0 0 10px var(--neon-magenta);
                }
                .ascension-particles {
                    position: absolute;
                    top: 50%;
                    left: 0;
                    width: 100%;
                    pointer-events: none;
                }
                .ascension-particle {
                    position: absolute;
                    width: 10px;
                    height: 10px;
                    background: var(--neon-magenta);
                    border-radius: 50%;
                    animation: ascend 2s forwards;
                }
                @keyframes ascend {
                    0% { opacity: 1; transform: translateY(0) scale(1); }
                    100% { opacity: 0; transform: translateY(-200px) scale(0); }
                }
            `}} />
        </div>
    );
};

export default WelcomeSequence;
