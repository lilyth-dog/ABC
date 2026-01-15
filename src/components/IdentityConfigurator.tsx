import { useState, useEffect, Suspense, ChangeEvent } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import DNAHelix from './DNAHelix';
import BrainWaveVisualizer from './BrainWaveVisualizer';
import NeuroKinematicDashboard from './NeuroKinematicDashboard';
import { useAudio } from './AudioManager';
import useNeuroStream from '../hooks/useNeuroStream';
import useBiosignal from '../hooks/useBiosignal';
import { tracker } from '../utils/BehaviorTracker';
import config from '../utils/config';

interface TraitData {
    subject: string;
    A: number;
    fullMark: number;
}

interface IdentityConfiguratorProps {
    onComplete: (traits: TraitData[], maturityData?: { level: number; syncScore: number }) => void;
    onCancel: () => void;
    coupling: number;
    setCoupling: (value: number) => void;
}

type StepType = 'genomics' | 'personality' | 'aesthetics' | 'neural' | 'kinematics' | 'sync';

const IdentityConfigurator = ({ onComplete, onCancel, coupling, setCoupling }: IdentityConfiguratorProps) => {
    const { playChime, playSuccess } = useAudio();
    const { sendEEG, isConnected } = useNeuroStream('/ws/simulation');
    
    // 생체신호 수집 (오디오 분석)
    const { data: biosignalData, isRecording, startRecording, stopRecording } = useBiosignal(true);

    const [step, setStep] = useState<StepType>('genomics');
    const [progress, setProgress] = useState(0);
    const [sessionCount, setSessionCount] = useState(0);
    const [learnedArchetype, setLearnedArchetype] = useState<string | null>(null);
    const [maturityLevel, setMaturityLevel] = useState(1);
    const [syncScore, setSyncScore] = useState(0);

    // Generate or retrieve persistent user ID
    const getUserId = (): string => {
        let userId = localStorage.getItem('anima_user_id');
        if (!userId) {
            userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            localStorage.setItem('anima_user_id', userId);
        }
        return userId;
    };

    useEffect(() => {
        tracker.startSession();
        // Fetch existing profile if available
        const userId = getUserId();
        fetch(config.getApiUrl(`/api/profile/${userId}`))
            .then(res => {
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                return res.json();
            })
            .then(data => {
                if (data.profile) {
                    setSessionCount(data.recent_sessions || 0);
                    setLearnedArchetype(data.archetype);
                    setMaturityLevel(data.maturity_level || 1);
                    setSyncScore(data.sync_score || 0);
                }
            })
            .catch((error) => {
                // New user or error - silently handle
                if (config.isDevelopment) {
                    console.debug('[IdentityConfigurator] New user or fetch error:', error);
                }
            });
    }, []);

    const [traits, setTraits] = useState<TraitData[]>([
        { subject: 'Openness', A: 80, fullMark: 100 },
        { subject: 'Conscientiousness', A: 65, fullMark: 100 },
        { subject: 'Extroversion', A: 90, fullMark: 100 },
        { subject: 'Agreeableness', A: 70, fullMark: 100 },
        { subject: 'Neuroticism', A: 40, fullMark: 100 },
    ]);

    const [showBloom, setShowBloom] = useState(false);
    const [showSummary, setShowSummary] = useState(false);
    const [behavioralTraits, setBehavioralTraits] = useState<{ analytical: boolean; stable: boolean } | null>(null);
    const [selectedAesthetic, setSelectedAesthetic] = useState<string>('Cyber/Industrial');

    // 오디오 분석 시작/중지
    useEffect(() => {
        if (step === 'neural' || step === 'sync') {
            startRecording();
        } else {
            stopRecording();
        }
        return () => stopRecording();
    }, [step, startRecording, stopRecording]);
    
    useEffect(() => {
        if (step === 'neural' && isConnected) {
            const theta = Math.min(coupling / 10, 1.0);
            const beta = Math.min((10 - coupling) / 10, 1.0);
            sendEEG(theta, beta);
        }
    }, [coupling, step, isConnected, sendEEG]);

    useEffect(() => {
        if (step === 'sync') {
            const interval = setInterval(() => {
                setProgress((prev) => {
                    if (prev >= 100) {
                        clearInterval(interval);

                        // Continuous Learning: Save session and get updated profile
                        const profile = tracker.getBehavioralProfile();
                        
                        // 생체신호 데이터 추가
                        if (biosignalData?.audio) {
                            profile.audioAnalysis = {
                                valence: biosignalData.audio.valence,
                                arousal: biosignalData.audio.arousal,
                                emotion: biosignalData.audio.emotion,
                                energy: biosignalData.audio.energy
                            };
                        }
                        
                        const userId = getUserId();

                        fetch(config.getApiUrl('/api/session'), {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ user_id: userId, behavioral_profile: profile })
                        })
                            .then(res => {
                                if (!res.ok) {
                                    throw new Error(`HTTP error! status: ${res.status}`);
                                }
                                return res.json();
                            })
                            .then(data => {
                                // Use learned weights from continuous learning
                                const traits = {
                                    weights: data.weights,
                                    evidence: { reasoning: `Session ${data.session_count}: ${data.archetype}` },
                                    analytical: data.weights?.Logic > 0.5,
                                    stable: data.weights?.Fluidity > 0.5
                                };
                                setBehavioralTraits(traits);
                                setSessionCount(data.session_count);
                                setLearnedArchetype(data.archetype);
                                setMaturityLevel(data.maturity_level);
                                setSyncScore(data.sync_score);
                                playSuccess();
                                setShowBloom(true);
                                setTimeout(() => setShowSummary(true), 500);
                            })
                            .catch(err => {
                                console.error('[SyncError]', err);
                                // Fallback to one-shot behavior API
                                fetch(config.getApiUrl('/api/behavior'), {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify(profile)
                                })
                                .then(res => {
                                    if (!res.ok) {
                                        throw new Error(`HTTP error! status: ${res.status}`);
                                    }
                                    return res.json();
                                })
                                .then(data => {
                                    setBehavioralTraits(data.behavioral_traits);
                                    setShowSummary(true);
                                })
                                .catch(fallbackErr => {
                                    console.error('[FallbackError]', fallbackErr);
                                    // 최종 fallback: 기본 트레이트 설정
                                    setBehavioralTraits({
                                        analytical: false,
                                        stable: true,
                                        weights: { Logic: 0.5, Intuition: 0.5, Fluidity: 0.5, Complexity: 0.5 }
                                    });
                                    setShowSummary(true);
                                });
                            });

                        return 100;
                    }
                    if (prev % 10 === 0) playChime(440 + prev * 2, 'sine', 0.05);
                    return prev + 2;
                });
            }, 50);
            return () => clearInterval(interval);
        }
    }, [step, traits, playChime, playSuccess]);

    const handleNextStep = (next: StepType) => {
        tracker.recordStepCompletion();
        playChime(660);
        setStep(next);
    };

    if (showSummary) {
        const topTraits = [...traits].sort((a, b) => b.A - a.A);
        const dominant = topTraits[0].subject;
        const subDominant = topTraits[1].subject;

        return (
            <div className="identity-configurator-overlay glass-panel soul-card fade-in" style={{ borderColor: 'var(--neon-cyan)', padding: '2rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🧠</div>
                <h2 className="neon-cyan">SELF-EXPLORATION COMPLETE</h2>
                <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>AI has mapped your behavioral essence.</p>

                <div className="discovery-insights glass-panel" style={{ width: '100%', maxWidth: '450px', padding: '20px', marginBottom: '25px', textAlign: 'left', border: '1px solid rgba(0, 212, 255, 0.3)' }}>
                    <h4 className="neon-magenta" style={{ fontSize: '0.8rem', marginBottom: '15px', textTransform: 'uppercase', letterSpacing: '2px' }}>AI Inference Weights</h4>

                    {behavioralTraits?.weights && Object.entries(behavioralTraits.weights).map(([trait, weight]) => (
                        <div key={trait} style={{ marginBottom: '12px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginBottom: '4px' }}>
                                <span style={{ color: 'white' }}>{trait.toUpperCase()}</span>
                                <span className="neon-cyan">{(Number(weight) * 100).toFixed(0)}%</span>
                            </div>
                            <div style={{ height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                                <div style={{ height: '100%', background: 'linear-gradient(90deg, var(--neon-cyan), var(--neon-magenta))', width: `${Number(weight) * 100}%`, transition: 'width 1.5s ease-out' }}></div>
                            </div>
                        </div>
                    ))}

                    <div style={{ marginTop: '20px', padding: '12px', background: 'rgba(0,0,0,0.4)', borderRadius: '4px', fontSize: '0.8rem', borderLeft: '3px solid var(--neon-magenta)' }}>
                        <span style={{ color: 'var(--neon-magenta)', fontWeight: 800, marginRight: '8px' }}>EVIDENCE:</span>
                        <span style={{ color: 'rgba(255,255,255,0.9)' }}>{behavioralTraits?.evidence?.reasoning || "Balanced interaction pattern detected."}</span>
                    </div>
                </div>

                <div className="soul-trait-highlight" style={{ fontSize: '1.4rem', marginBottom: '25px', fontWeight: 800 }}>
                    Archetype: <span className="neon-magenta">{dominant} & {subDominant}</span>
                </div>

                <button className="btn btn-primary glow-effect" style={{ padding: '15px 40px', width: '100%', maxWidth: '450px' }} onClick={() => {
                    onComplete(traits, { level: maturityLevel, syncScore: syncScore });
                    
                    // 레벨업 알림
                    if (data.level_up && (window as any).addNotification) {
                        (window as any).addNotification({
                            type: 'level_up',
                            title: '레벨 업!',
                            message: `디지털 트윈이 Tier ${maturityLevel}로 진화했습니다!`,
                            severity: 'low'
                        });
                    }
                    
                    // 스트레스 알림
                    if (data.predictive_insights?.stress_analysis?.stress_level > 0.6 && (window as any).addNotification) {
                        (window as any).addNotification({
                            type: 'stress',
                            title: '높은 스트레스 감지',
                            message: data.predictive_insights.stress_analysis.recommendation || '충분한 휴식이 필요합니다.',
                            severity: 'high'
                        });
                    }
                }}>
                    ENTER WORLD WITH SELF-KNOWLEDGE
                </button>
            </div>
        )
    }

    const randomizeTraits = () => {
        tracker.recordRevision();
        const newTraits = traits.map(t => ({ ...t, A: Math.floor(Math.random() * 60) + 40 }));
        setTraits(newTraits);
        playChime(800, 'square', 0.1);
    };

    return (
        <div
            className="identity-configurator-overlay glass-panel"
            onMouseMove={(e) => tracker.trackMovement(e.clientX, e.clientY)}
            onClick={() => tracker.recordClick()}
        >
            {showBloom && <div className="neural-bloom"></div>}
            <div className="config-header">
                <h2 className="neon-magenta">ANIMA WEAVING</h2>
                <button onClick={onCancel} className="btn-close">×</button>
            </div>

            <div className="config-content">
                <div style={{ display: 'flex', gap: '5px', marginBottom: '10px', justifyContent: 'center' }}>
                    <button className={`btn-xs ${step === 'genomics' ? 'active' : ''}`} onClick={() => { playChime(440); setStep('genomics'); }}>ORIGIN</button>
                    <button className={`btn-xs ${step === 'personality' ? 'active' : ''}`} onClick={() => { playChime(550); setStep('personality'); }}>ESSENCE</button>
                    <button className={`btn-xs ${step === 'aesthetics' ? 'active' : ''}`} onClick={() => { playChime(600); setStep('aesthetics'); }}>AURA</button>
                    <button className={`btn-xs ${step === 'neural' ? 'active' : ''}`} onClick={() => { playChime(660); setStep('neural'); }}>HARMONY</button>
                    <button className={`btn-xs ${step === 'kinematics' ? 'active' : ''}`} onClick={() => { playChime(770); setStep('kinematics'); }}>PULSE</button>
                </div>

                {step === 'genomics' && (
                    <div className="step-genomics fade-in" style={{ width: '100%', textAlign: 'center' }}>
                        <div className="dna-viz-container" style={{ width: '100%', height: '300px' }}>
                            <Canvas camera={{ position: [0, 0, 15], fov: 45 }}>
                                <ambientLight intensity={0.5} />
                                <pointLight position={[10, 10, 10]} intensity={1} />
                                <Suspense fallback={null}>
                                    <DNAHelix />
                                </Suspense>
                                <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={2} />
                            </Canvas>
                        </div>
                        <p className="status-text blink" style={{ marginTop: '1rem' }}>ANALYZING GENOMIC SEQUENCES...</p>
                        <div className="trait-list" style={{ maxWidth: '400px', margin: '20px auto' }}>
                            <div className="trait-item"><span>ORIGIN:</span> <span className="neon-cyan">EARTH-PRIME</span></div>
                            <div className="trait-item"><span>BLOODLINE:</span> <span className="neon-magenta">AUGMENTED</span></div>
                            <div className="trait-item"><span>POTENTIAL:</span> <span className="neon-green">UNLIMITED</span></div>
                        </div>
                        <button className="btn btn-primary glow-effect mt-4" onClick={() => handleNextStep('personality')}>
                            DECODE PERSONALITY MATRIX
                        </button>
                    </div>
                )}

                {step === 'personality' && (
                    <div className="step-personality fade-in">
                        <h3 style={{ textAlign: 'center', marginBottom: '1rem', color: 'var(--text-muted)' }}>PSYCHE MATRIX CONFIGURATION</h3>
                        <div className="chart-container" style={{ width: '100%', height: '300px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={traits}>
                                    <PolarGrid stroke="#ffffff33" />
                                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#00d4ff', fontSize: 12 }} />
                                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                                    <Radar
                                        name="Identity"
                                        dataKey="A"
                                        stroke="#ff00ff"
                                        strokeWidth={3}
                                        fill="#ff00ff"
                                        fillOpacity={0.4}
                                    />
                                </RadarChart>
                            </ResponsiveContainer>
                        </div>
                        <div className="controls" style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '1rem' }}>
                            <button className="btn btn-secondary glass-effect" onClick={randomizeTraits}>RANDOMIZE TRAITS</button>
                            <button className="btn btn-primary glow-effect" onClick={() => {
                                const weights: Record<string, number> = {};
                                traits.forEach(t => weights[t.subject] = t.A);
                                tracker.recordChoice('traitWeights', weights);
                                handleNextStep('aesthetics');
                            }}>
                                DEFINE VISUAL RESONANCE
                            </button>
                        </div>
                    </div>
                )}

                {step === 'aesthetics' && (
                    <div className="step-aesthetics fade-in" style={{ width: '100%', textAlign: 'center' }}>
                        <h3 style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>Aura Aesthetic Calibration</h3>
                        <div className="aesthetics-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
                            {['Zen/Minimal', 'Cyber/Industrial', 'Neon/Vibrant'].map(type => (
                                <div
                                    key={type}
                                    className={`glass-panel ${selectedAesthetic === type ? 'active' : ''}`}
                                    style={{
                                        padding: '1.5rem',
                                        cursor: 'pointer',
                                        border: selectedAesthetic === type ? '2px solid var(--neon-cyan)' : '1px solid var(--glass-border)',
                                        background: selectedAesthetic === type ? 'rgba(0, 212, 255, 0.1)' : 'var(--glass)'
                                    }}
                                    onClick={() => {
                                        playChime(440);
                                        setSelectedAesthetic(type);
                                        tracker.recordChoice('aesthetics', type);
                                    }}
                                >
                                    <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>
                                        {type === 'Zen/Minimal' ? '⚪' : type === 'Cyber/Industrial' ? '🤖' : '🌈'}
                                    </div>
                                    <div style={{ fontWeight: 800, fontSize: '0.8rem' }}>{type.toUpperCase()}</div>
                                </div>
                            ))}
                        </div>
                        <button className="btn btn-primary glow-effect" onClick={() => handleNextStep('neural')}>
                            INITIALIZE NEURAL ENGINE
                        </button>
                    </div>
                )}

                {step === 'neural' && (
                    <div className="step-neural fade-in" style={{ width: '100%', textAlign: 'center' }}>
                        <h3 style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>NEURAL PHYSICS SIMULATION</h3>
                        <div className="neural-viz-container" style={{ width: '100%', height: '300px', background: '#000' }}>
                            <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
                                <ambientLight intensity={0.2} />
                                <Suspense fallback={null}>
                                    <BrainWaveVisualizer couplingStrength={coupling} />
                                </Suspense>
                                <OrbitControls />
                            </Canvas>
                        </div>

                        <div className="controls" style={{ marginTop: '20px', width: '80%', margin: '20px auto' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                                <label>SYNCHRONIZATION COUPLING (K)</label>
                                <span className="neon-green" style={{ fontFamily: 'monospace', fontSize: '1.2rem' }}>{coupling}</span>
                            </div>

                            <input
                                type="range"
                                min="0"
                                max="10"
                                step="0.1"
                                value={coupling}
                                onChange={(e: ChangeEvent<HTMLInputElement>) => {
                                    tracker.recordRevision();
                                    setCoupling(parseFloat(e.target.value));
                                }}
                                style={{ width: '100%', accentColor: 'var(--neon-blue)' }}
                            />

                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#666', marginTop: '5px' }}>
                                <span>CHAOS (Beta)</span>
                                <span>SYNC (Theta)</span>
                            </div>

                            <p style={{ fontSize: '0.8rem', color: isConnected ? 'var(--neon-blue)' : '#ff5555', marginTop: '10px', fontFamily: 'monospace' }}>
                                {isConnected ? `[LINK ACTIVE] TRANSMITTING NEURAL PARAMS...` : `[OFFLINE] SIMULATION RUNNING LOCALLY`}
                            </p>

                            <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '20px' }}>
                                <button className="btn btn-secondary glass-effect" onClick={() => setStep('kinematics')}>
                                    VIEW MATHEMATICS
                                </button>
                                <button className="btn btn-primary glow-effect" onClick={() => handleNextStep('sync')}>
                                    COMMENCE BIO-SYNC
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {step === 'kinematics' && (
                    <div className="step-kinematics fade-in" style={{ width: '100%', height: '500px' }}>
                        <h3 style={{ textAlign: 'center', color: 'var(--text-muted)' }}>NEURO-KINEMATIC SKELETON</h3>
                        <NeuroKinematicDashboard />
                        <div className="controls" style={{ marginTop: '20px', textAlign: 'center' }}>
                            <button className="btn btn-primary glow-effect" onClick={() => setStep('sync')}>
                                COMMENCE BIO-SYNC
                            </button>
                        </div>
                    </div>
                )}

                {step === 'sync' && (
                    <div className="step-sync fade-in" style={{ textAlign: 'center' }}>
                        <div className="sync-loader">
                            <div className="sync-circle" style={{ width: `${progress}%`, height: `${progress}%`, background: 'var(--neon-magenta)', boxShadow: '0 0 30px var(--neon-magenta)' }}></div>
                            <span className="sync-percentage" style={{ color: 'white' }}>{progress}%</span>
                        </div>
                        <p className="status-text blink" style={{ color: 'var(--neon-magenta)' }}>WHISPERING TO YOUR ANIMA...</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default IdentityConfigurator;
