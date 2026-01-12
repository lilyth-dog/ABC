import React, { useEffect, useRef, useState, createContext, useContext } from 'react';

const AudioContext = createContext(null);

export const useAudio = () => useContext(AudioContext);

const AudioManager = ({ children }) => {
  const [isMuted, setIsMuted] = useState(false);
  const audioCtx = useRef(null);
  const mainGain = useRef(null);
  const atmosphereOsc = useRef(null);

  const initAudio = () => {
    if (audioCtx.current) return;
    
    audioCtx.current = new (window.AudioContext || window.webkitAudioContext)();
    mainGain.current = audioCtx.current.createGain();
    mainGain.current.connect(audioCtx.current.destination);
    mainGain.current.gain.value = 0.3;

    // Background Atmosphere: Low frequency drone
    atmosphereOsc.current = audioCtx.current.createOscillator();
    const atmosGain = audioCtx.current.createGain();
    const lfo = audioCtx.current.createOscillator();
    const lfoGain = audioCtx.current.createGain();

    atmosphereOsc.current.type = 'sine';
    atmosphereOsc.current.frequency.value = 55; // A1
    
    lfo.frequency.value = 0.5;
    lfoGain.gain.value = 5;
    lfo.connect(lfoGain);
    lfoGain.connect(atmosphereOsc.current.frequency);
    
    atmosGain.gain.value = 0.1;
    atmosphereOsc.current.connect(atmosGain);
    atmosGain.connect(mainGain.current);

    atmosphereOsc.current.start();
    lfo.start();
  };

  const playChime = (freq = 880, type = 'sine', duration = 0.1) => {
    if (!audioCtx.current || isMuted) return;
    if (audioCtx.current.state === 'suspended') audioCtx.current.resume();

    const osc = audioCtx.current.createOscillator();
    const g = audioCtx.current.createGain();
    
    osc.type = type;
    osc.frequency.setValueAtTime(freq, audioCtx.current.currentTime);
    osc.frequency.exponentialRampToValueAtTime(freq / 2, audioCtx.current.currentTime + duration);

    g.gain.setValueAtTime(0.2, audioCtx.current.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, audioCtx.current.currentTime + duration);

    osc.connect(g);
    g.connect(mainGain.current);
    
    osc.start();
    osc.stop(audioCtx.current.currentTime + duration);
  };

  const playSuccess = () => {
    playChime(440, 'triangle', 0.2);
    setTimeout(() => playChime(880, 'triangle', 0.4), 100);
  };

  useEffect(() => {
    const handleInteraction = () => {
        initAudio();
        document.removeEventListener('click', handleInteraction);
    };
    document.addEventListener('click', handleInteraction);
    return () => document.removeEventListener('click', handleInteraction);
  }, []);

  return (
    <AudioContext.Provider value={{ playChime, playSuccess, isMuted, setIsMuted }}>
        <div style={{ position: 'fixed', bottom: '20px', left: '20px', zIndex: 9999 }}>
            <button 
                onClick={() => setIsMuted(!isMuted)} 
                className="btn-xs" 
                style={{ background: 'rgba(0,0,0,0.5)', border: '1px solid var(--neon-cyan)', padding: '5px 10px', borderRadius: '4px', fontSize: '10px' }}
            >
                {isMuted ? 'UNMUTE AUDIO' : 'MUTE AUDIO'}
            </button>
        </div>
        {children}
    </AudioContext.Provider>
  );
};

export default AudioManager;
