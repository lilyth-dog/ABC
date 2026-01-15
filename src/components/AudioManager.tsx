import { useEffect, useRef, useState, createContext, useContext, ReactNode } from 'react';

interface AudioContextValue {
    playChime: (freq?: number, type?: OscillatorType, duration?: number) => void;
    playSuccess: () => void;
    setAesthetic: (type: string) => void;
    updateHeartbeat: (intensity: number) => void;
    isMuted: boolean;
    setIsMuted: (muted: boolean) => void;
}

const AudioContext = createContext<AudioContextValue | null>(null);

export const useAudio = (): AudioContextValue => {
    const context = useContext(AudioContext);
    if (!context) {
        return {
            playChime: () => { },
            playSuccess: () => { },
            setAesthetic: () => { },
            updateHeartbeat: () => { },
            isMuted: false,
            setIsMuted: () => { },
        };
    }
    return context;
};

interface AudioManagerProps {
    children: ReactNode;
}

const AudioManager = ({ children }: AudioManagerProps) => {
    const [isMuted, setIsMuted] = useState(false);
    const audioCtx = useRef<AudioContext | null>(null);
    const mainGain = useRef<GainNode | null>(null);
    const atmosphereOsc = useRef<OscillatorNode | null>(null);
    const heartbeatOsc = useRef<OscillatorNode | null>(null);
    const heartbeatGain = useRef<GainNode | null>(null);

    const initAudio = () => {
        if (audioCtx.current) return;

        audioCtx.current = new (window.AudioContext || (window as any).webkitAudioContext)();
        mainGain.current = audioCtx.current.createGain();
        mainGain.current.connect(audioCtx.current.destination);
        mainGain.current.gain.value = 0.3;

        atmosphereOsc.current = audioCtx.current.createOscillator();
        const atmosGain = audioCtx.current.createGain();
        const lfo = audioCtx.current.createOscillator();
        const lfoGain = audioCtx.current.createGain();

        atmosphereOsc.current.type = 'sine';
        atmosphereOsc.current.frequency.value = 55;

        lfo.frequency.value = 0.5;
        lfoGain.gain.value = 5;
        lfo.connect(lfoGain);
        lfoGain.connect(atmosphereOsc.current.frequency);

        atmosGain.gain.value = 0.1;
        atmosphereOsc.current.connect(atmosGain);
        atmosGain.connect(mainGain.current);

        atmosphereOsc.current.start();
        lfo.start();

        // Heartbeat setup
        heartbeatOsc.current = audioCtx.current.createOscillator();
        heartbeatGain.current = audioCtx.current.createGain();
        heartbeatOsc.current.type = 'sine';
        heartbeatOsc.current.frequency.value = 40; // Low frequency thump
        heartbeatGain.current.gain.value = 0;
        heartbeatOsc.current.connect(heartbeatGain.current);
        heartbeatGain.current.connect(mainGain.current);
        heartbeatOsc.current.start();
    };

    const playChime = (freq = 880, type: OscillatorType = 'sine', duration = 0.1) => {
        if (!audioCtx.current || !mainGain.current || isMuted) return;
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

    const setAesthetic = (type: string) => {
        if (!atmosphereOsc.current) return;
        const freq = type === 'Zen/Minimal' ? 44 : type === 'Neon/Vibrant' ? 66 : 55;
        atmosphereOsc.current.frequency.exponentialRampToValueAtTime(freq, audioCtx.current!.currentTime + 2);
    };

    const updateHeartbeat = (intensity: number) => {
        if (!heartbeatGain.current || isMuted) return;
        // Pulse gain based on intensity (coupling)
        const volume = Math.min(intensity / 20, 0.4);
        heartbeatGain.current.gain.setTargetAtTime(volume, audioCtx.current!.currentTime, 0.1);
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
        <AudioContext.Provider value={{ playChime, playSuccess, setAesthetic, updateHeartbeat, isMuted, setIsMuted }}>
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
