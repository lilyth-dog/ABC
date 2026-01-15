import React, { Suspense, useEffect, useState } from 'react';
import GlassCard from './GlassCard';
import { useAudio } from './AudioManager';
const AvatarViewer = React.lazy(() => import('./AvatarViewer'));
const HologramSphere = React.lazy(() => import('./HologramSphere'));
import { MaturityGauge } from './MaturityGauge';
import PredictiveInsights from './PredictiveInsights';

interface IdentityDataItem {
    subject: string;
    A: number;
    fullMark: number;
}

interface HeroProps {
    onInitialize: () => void;
    avatarUrl: string | null;
    onEnterWorld: () => void;
    onConfigureIdentity: () => void;
    identityData: IdentityDataItem[] | null;
    onShowManifesto: () => void;
    onShowArchive?: () => void;
    maturityLevel?: number;
    syncScore?: number;
    userId?: string;
}

const Hero = ({ onInitialize, avatarUrl, onEnterWorld, onConfigureIdentity, identityData, onShowManifesto, onShowArchive, maturityLevel = 1, syncScore = 0, userId }: HeroProps) => {
    const { playChime } = useAudio();
    const [displayText, setDisplayText] = useState('');
    const fullText = "WAKE YOUR ANIMA COMPANION";

    useEffect(() => {
        let i = 0;
        const interval = setInterval(() => {
            setDisplayText(fullText.slice(0, i));
            if (i > 0 && fullText[i - 1] !== ' ') {
                playChime(1200, 'sine', 0.05);
            }
            i++;
            if (i > fullText.length) clearInterval(interval);
        }, 80);
        return () => clearInterval(interval);
    }, []);

    return (
        <section id="home" className="hero-section">
            <div className="hero-content">
                <h1 className="glitch-text" data-text={fullText}>
                    {displayText.split(' ').map((word, idx) => (
                        <span key={idx}>
                            {word === 'METAVERSE' ? <span className="highlight-neon">METAVERSE</span> : word}
                            {' '}
                        </span>
                    ))}
                    <span className="blink">_</span>
                </h1>
                <p className="hero-subtitle">
                    Your soul has a digital twin. We don't just build avatars; we weave a companion that feels your heart and walks beside you.
                </p>
                <div className="hero-buttons">
                    <button
                        className="btn btn-primary glow-effect"
                        onClick={() => { playChime(880); onInitialize(); }}
                        onMouseEnter={() => playChime(440, 'sine', 0.05)}
                    >
                        {avatarUrl ? 'Re-Initialize Twin' : 'Initialize Twin'}
                    </button>

                    {!identityData && (
                        <button
                            className="btn btn-primary glow-effect"
                            style={{ marginLeft: '1rem', borderColor: '#ff00ff', color: '#ff00ff' }}
                            onClick={() => { playChime(1000); onConfigureIdentity(); }}
                            onMouseEnter={() => playChime(660, 'sine', 0.05)}
                        >
                            Bio-Link Identity
                        </button>
                    )}

                    {avatarUrl && identityData && (
                        <button
                            className="btn btn-primary glow-effect"
                            style={{ marginLeft: '1rem', background: 'var(--neon-magenta)', color: 'white', border: 'none' }}
                            onClick={() => { playChime(1200); onEnterWorld(); }}
                            onMouseEnter={() => playChime(880, 'sine', 0.05)}
                        >
                            Enter Our World
                        </button>
                    )}

                    {!avatarUrl && (
                        <>
                            <button className="btn btn-secondary glass-effect" onClick={onShowManifesto} onMouseEnter={() => playChime(440, 'sine', 0.05)}>Our Manifesto</button>
                            <button className="btn btn-outline" style={{ marginLeft: '1rem', borderColor: 'var(--neon-magenta)', color: 'var(--neon-magenta)' }} onClick={onShowArchive} onMouseEnter={() => playChime(550, 'sine', 0.05)}>Our Memories</button>
                        </>
                    )}
                </div>
            </div>

            <div className="hero-visual">
                <div className="hologram-circle"></div>

                <div style={{ width: '100%', height: '100%', position: 'relative', zIndex: 2 }}>
                    <Suspense fallback={<div>Loading Visuals...</div>}>
                        {avatarUrl ? (
                            <>
                                <AvatarViewer avatarUrl={avatarUrl} maturityLevel={maturityLevel} />
                                {identityData && (
                                    <div className="stats-overlay glass-panel slide-up">
                                        <MaturityGauge level={maturityLevel} syncScore={syncScore} />

                                        <div className="stat-row mt-4 pt-4 border-t border-white/5">
                                            <span>Dominant Trait:</span>
                                            <span className="bold neon-magenta">
                                                {identityData.reduce((prev, current) => (prev.A > current.A) ? prev : current).subject.toUpperCase()}
                                            </span>
                                        </div>
                                    </div>
                                )}
                            </>
                        ) : (
                            <HologramSphere />
                        )}
                    </Suspense>
                </div>
            </div>
            
            {/* 예측 인사이트 섹션 */}
            {identityData && userId && (
                <div style={{ marginTop: '4rem', padding: '0 10%' }}>
                    <PredictiveInsights userId={userId} />
                </div>
            )}
        </section>
    );
};

export default Hero;
