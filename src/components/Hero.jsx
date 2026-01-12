import React, { Suspense, useEffect, useState } from 'react';
import GlassCard from './GlassCard';
import { useAudio } from './AudioManager';
const AvatarViewer = React.lazy(() => import('./AvatarViewer'));
const HologramSphere = React.lazy(() => import('./HologramSphere'));

const Hero = ({ onInitialize, avatarUrl, onEnterWorld, onConfigureIdentity, identityData }) => {
  const { playChime } = useAudio();
  const [displayText, setDisplayText] = useState('');
  const fullText = "ASCEND TO THE METAVERSE";

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setDisplayText(fullText.slice(0, i));
      if (i > 0 && fullText[i-1] !== ' ') {
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
          Forge your Digital Human Twin. Experience the next generation of virtual interaction and hyper-realistic idols.
        </p>
        <div className="hero-buttons">
          <button 
            className="btn btn-primary glow-effect" 
            onClick={() => { playChime(880); onInitialize(); }}
            onMouseEnter={() => playChime(440, 'sine', 0.05)}
          >
            {avatarUrl ? 'Re-Initialize Twin' : 'Initialize Twin'}
          </button>
          
          {avatarUrl && !identityData && (
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
                style={{ marginLeft: '1rem', background: '#00f3ff', color: 'black' }} 
                onClick={() => { playChime(1200); onEnterWorld(); }}
                onMouseEnter={() => playChime(880, 'sine', 0.05)}
            >
               Enter World
             </button>
          )}

          {!avatarUrl && <button className="btn btn-secondary glass-effect" onMouseEnter={() => playChime(440, 'sine', 0.05)}>Explore Idols</button>}
        </div>
      </div>
      
      {/* Central Visual Stage */}
      <div className="hero-visual">
         <div className="hologram-circle"></div>
         
         <div style={{ width: '100%', height: '100%', position: 'relative', zIndex: 2 }}>
            <Suspense fallback={<div>Loading Visuals...</div>}>
                {avatarUrl ? (
                    <>
                        <AvatarViewer avatarUrl={avatarUrl} />
                        {identityData && (
                          <div className="stats-overlay glass-panel slide-up">
                            <h3 className="neon-cyan">BIO-SYNC ACTIVE</h3>
                            <div className="stat-row">
                              <span>Dominant Trait:</span>
                              <span className="bold neon-magenta">
                                {identityData.reduce((prev, current) => (prev.A > current.A) ? prev : current).subject.toUpperCase()}
                              </span>
                            </div>
                            <div className="stat-row">
                              <span>Neuro-Link:</span>
                              <span className="bold neon-green">100% STABLE</span>
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
    </section>
  );
};

export default Hero;
