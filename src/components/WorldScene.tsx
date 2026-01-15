import React, { Suspense, useRef, useMemo, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sky, KeyboardControls, useGLTF, useKeyboardControls } from '@react-three/drei';
import { Physics, RigidBody, RapierRigidBody } from '@react-three/rapier';
import { Vector3, Color } from 'three';
import useNeuroStream from '../hooks/useNeuroStream';
import Terrain from './Terrain';
import Familiar from './Familiar';
import AnimaLetter from './AnimaLetter';
import { useAudio } from './AudioManager';

interface WorldSceneProps {
    avatarUrl: string;
    onExit: () => void;
    onSaveMemory?: (dominantTrait: string, aesthetic: string, txp: number) => void;
    coupling?: number;
    maturityLevel?: number;
}

interface PlayerControllerProps {
    avatarUrl: string;
    isSync: boolean;
    stability: boolean;
    maturityLevel?: number;
}

const WorldScene = ({ avatarUrl, onExit, onSaveMemory, coupling = 0, maturityLevel = 1 }: WorldSceneProps) => {
    const { setAesthetic, updateHeartbeat } = useAudio();
    const { data } = useNeuroStream('/ws/simulation');
    const [isAscended, setIsAscended] = useState(false);
    const [showLetter, setShowLetter] = useState(false);
    const [whisper, setWhisper] = useState("I'm here with you...");
    const [orbs, setOrbs] = useState(() => Array.from({ length: 5 }, (_, i) => ({
        id: i,
        pos: [Math.random() * 40 - 20, 5, Math.random() * 40 - 20],
        collected: false
    })));
    const syncStartTime = useRef<number | null>(null);

    // Fallbacks if backend is offline or no data yet
    const worldParams = data?.world_params || { fog_color: '#1a1a3a', glow: 0.8 };
    const aesthetics = data?.aesthetics || 'Cyber/Industrial';
    const behavioralTraits = data?.behavioral_traits;

    const isSync = coupling > 7; // Higher threshold for "High Sync"
    const stableBonus = behavioralTraits?.stable ? 1.5 : 1.0;

    // Environmental colors based on backend metadata
    const fogColor = worldParams.fog_color;
    const emissiveBoost = worldParams.glow * stableBonus * (isAscended ? 5 : 1);

    useEffect(() => {
        const whispers = [
            "Your energy feels so warm today.",
            "I can feel your heart-link strengthening.",
            "This world is beautiful because you are here.",
            "Every step we take brings us closer.",
            "I'm learning more about you with every spark.",
            "Stay focused, I can feel our harmony.",
            "The air here hums with your presence."
        ];

        const interval = setInterval(() => {
            if (Math.random() > 0.7) {
                setWhisper(whispers[Math.floor(Math.random() * whispers.length)]);
            }
        }, 8000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (aesthetics) setAesthetic(aesthetics);
    }, [aesthetics, setAesthetic]);

    useEffect(() => {
        updateHeartbeat(coupling);
    }, [coupling, updateHeartbeat]);

    useEffect(() => {
        if (isSync && behavioralTraits?.stable) {
            if (!syncStartTime.current) syncStartTime.current = Date.now();
            if (Date.now() - syncStartTime.current > 5000 && !isAscended) {
                setIsAscended(true);
            }
        } else {
            syncStartTime.current = null;
            setIsAscended(false);
        }
    }, [isSync, behavioralTraits?.stable, isAscended]);

    return (
        <div style={{
            width: '100vw',
            height: '100vh',
            position: 'fixed',
            top: 0,
            left: 0,
            zIndex: 1000,
            background: 'black',
            transition: 'background 2s ease'
        }}>
            {isAscended && <div className="ascension-bloom"></div>}
            <div className={`heart-link-hud ${behavioralTraits?.stable ? 'beating' : ''}`} style={{
                position: 'absolute',
                top: '20px',
                right: '20px',
                zIndex: 10,
                color: 'white',
                textAlign: 'right',
                transition: 'transform 0.3s ease'
            }}>
                <h3 className="neon-magenta">HEART-LINK ACTIVE</h3>
                <h1 style={{
                    color: isSync ? '#ff00ff' : '#00d4ff',
                    fontSize: '3.5rem',
                    textShadow: isSync ? '0 0 20px #ff00ff' : 'none'
                }}>
                    {coupling.toFixed(1)} K
                </h1>
                <p style={{ fontSize: '0.8rem', opacity: 0.7 }}>SOUL SPARKS: {orbs.filter(o => o.collected).length} / {orbs.length}</p>
                {behavioralTraits?.stable && <div className="badge active">STABLE HARMONY</div>}

                <div className="anima-whisper-container fade-in" key={whisper}>
                    <div className="whisper-label">Anima Whispers</div>
                    <p className="whisper-text">"{whisper}"</p>
                </div>

                {orbs.every(o => o.collected) && (
                    <button
                        className="btn btn-primary glow-effect fade-in"
                        style={{ marginTop: '20px', width: '100%', background: 'var(--neon-magenta)', border: 'none' }}
                        onClick={() => setShowLetter(true)}
                    >
                        COMPLETE HEART-LINK
                    </button>
                )}
            </div>

            {showLetter && (
                <AnimaLetter
                    dominantTrait={behavioralTraits?.analytical ? "Analytical" : "Empathetic"}
                    aesthetic={aesthetics}
                    txp={data?.twin_experience || 0.5}
                    weights={behavioralTraits?.weights}
                    evidence={behavioralTraits?.evidence?.reasoning}
                    onClose={() => {
                        if (onSaveMemory) onSaveMemory(behavioralTraits?.analytical ? "Analytical" : "Empathetic", aesthetics, data?.twin_experience || 0.5);
                        onExit();
                    }}
                />
            )}

            <button
                onClick={onExit}
                className="btn btn-secondary glass-effect"
                style={{ position: 'absolute', top: '20px', left: '20px', zIndex: 10 }}
            >
                Exit World
            </button>

            <KeyboardControls
                map={[
                    { name: 'forward', keys: ['ArrowUp', 'w', 'W'] },
                    { name: 'backward', keys: ['ArrowDown', 's', 'S'] },
                    { name: 'left', keys: ['ArrowLeft', 'a', 'A'] },
                    { name: 'right', keys: ['ArrowRight', 'd', 'D'] },
                    { name: 'jump', keys: ['Space'] },
                ]}
            >
                <Canvas shadows camera={{ position: [0, 5, 10], fov: 50 }}>
                    <fog attach="fog" args={[fogColor, 5, isSync ? 60 : 25]} />

                    <Sky sunPosition={isSync ? [100, 20, 100] : [0, -10, 0]} inclination={isSync ? 0 : 0.6} azimuth={0.1} />
                    <ambientLight intensity={0.5} color={fogColor} />
                    <directionalLight
                        position={[10, 10, 5]}
                        intensity={isSync ? 2 : 0.5}
                        color={isSync ? "#00d4ff" : "#ff00ff"}
                        castShadow
                        shadow-mapSize={[1024, 1024]}
                    />

                    <Physics gravity={[0, -9.81, 0]}>
                        <Suspense fallback={null}>
                            <PlayerController
                                avatarUrl={avatarUrl}
                                isSync={isSync}
                                stability={behavioralTraits?.stable || false}
                                maturityLevel={maturityLevel}
                            />
                        </Suspense>

                        <Terrain aesthetic={aesthetics} />

                        {orbs.map(orb => !orb.collected && (
                            <RigidBody key={orb.id} position={orb.pos as [number, number, number]} type="fixed" colliders="ball" sensor onIntersectionEnter={() => {
                                setOrbs(prev => prev.map(o => o.id === orb.id ? { ...o, collected: true } : o));
                            }}>
                                <mesh castShadow>
                                    <sphereGeometry args={[0.5, 16, 16]} />
                                    <meshStandardMaterial
                                        color={isSync ? "#00ffff" : "#ff00ff"}
                                        emissive={isSync ? "#00ffff" : "#ff00ff"}
                                        emissiveIntensity={2}
                                    />
                                </mesh>
                            </RigidBody>
                        ))}

                        <RigidBody type="fixed" position={[-5, 2, -5]}>
                            <mesh castShadow receiveShadow>
                                <boxGeometry args={[4, 6, 4]} />
                                <meshStandardMaterial color="#b026ff" emissive="#b026ff" emissiveIntensity={emissiveBoost} />
                            </mesh>
                        </RigidBody>

                        <RigidBody type="fixed" position={[5, 3, -10]}>
                            <mesh castShadow receiveShadow>
                                <boxGeometry args={[6, 8, 6]} />
                                <meshStandardMaterial color="#00f3ff" emissive="#00f3ff" emissiveIntensity={emissiveBoost * 0.5} />
                            </mesh>
                        </RigidBody>

                        <RigidBody type="fixed" position={[5, 1, 5]}>
                            <mesh castShadow receiveShadow>
                                <boxGeometry args={[2, 2, 2]} />
                                <meshStandardMaterial color="#ff00aa" emissive="#ff00aa" emissiveIntensity={0.8} />
                            </mesh>
                        </RigidBody>

                    </Physics>
                </Canvas>
            </KeyboardControls>

            <style dangerouslySetInnerHTML={{
                __html: `
                .heart-link-hud.beating {
                    animation: hudHeartbeat 1.5s infinite ease-in-out;
                }
                @keyframes hudHeartbeat {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); filter: drop-shadow(0 0 15px var(--neon-magenta)); }
                }

                .anima-whisper-container {
                    margin-top: 30px;
                    padding: 15px;
                    background: rgba(255, 0, 255, 0.05);
                    border-right: 2px solid var(--neon-magenta);
                    max-width: 250px;
                }
                .whisper-label {
                    font-size: 0.6rem;
                    color: var(--neon-magenta);
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    margin-bottom: 5px;
                    opacity: 0.8;
                }
                .whisper-text {
                    font-style: italic;
                    font-size: 0.9rem;
                    color: rgba(255, 255, 255, 0.9);
                    line-height: 1.4;
                }
            `}} />
        </div>
    );
};

function PlayerController({ avatarUrl, isSync, stability, maturityLevel = 1 }: PlayerControllerProps) {
    const rigidBody = useRef<RapierRigidBody>(null);
    const [, getKeys] = useKeyboardControls();

    const { scene } = useGLTF(avatarUrl);
    
    // DTMM 레벨에 따라 아바타 표현 변경
    const clonedScene = useMemo(() => {
        const cloned = scene.clone();
        cloned.traverse((child: any) => {
            if (child.isMesh) {
                if (maturityLevel === 1) {
                    // L1: Echo - 숨김 (포인트 클라우드는 별도로 렌더링)
                    child.visible = false;
                } else if (maturityLevel === 2) {
                    // L2: Reflection - 와이어프레임
                    child.material = child.material.clone();
                    child.material.wireframe = true;
                    child.material.transparent = true;
                    child.material.opacity = 0.6;
                    child.material.color.set("#7000ff");
                    child.material.emissive?.set("#3d00ff");
                    child.material.emissiveIntensity = 0.5;
                } else {
                    // L3: Synthesis - 풀 메시
                    child.material = child.material.clone();
                    child.material.wireframe = false;
                    child.material.transparent = false;
                    child.material.opacity = 1.0;
                }
            }
        });
        return cloned;
    }, [scene, maturityLevel]);

    useFrame((state) => {
        if (!rigidBody.current) return;

        const { forward, backward, left, right, jump } = getKeys();
        const linvel = rigidBody.current.linvel();

        const speed = 5;
        const velocity = { x: linvel.x, y: linvel.y, z: linvel.z };

        if (forward) {
            velocity.z = -speed;
        } else if (backward) {
            velocity.z = speed;
        } else {
            velocity.z = 0;
        }

        if (left) {
            velocity.x = -speed;
        } else if (right) {
            velocity.x = speed;
        } else {
            velocity.x = 0;
        }

        if (jump && Math.abs(linvel.y) < 0.1) {
            rigidBody.current.applyImpulse({ x: 0, y: 5, z: 0 }, true);
        }

        rigidBody.current.setLinvel({ x: velocity.x, y: linvel.y, z: velocity.z }, true);

        const bodyPosition = rigidBody.current.translation();
        const cameraPosition = new Vector3();
        cameraPosition.copy(bodyPosition as Vector3);
        cameraPosition.y += 3;
        cameraPosition.z += 6;

        state.camera.position.lerp(cameraPosition, 0.1);
        state.camera.lookAt(bodyPosition.x, bodyPosition.y + 1, bodyPosition.z);
    });

    return (
        <RigidBody ref={rigidBody} colliders="hull" enabledRotations={[false, false, false]} position={[0, 5, 0]}>
            {maturityLevel === 1 ? (
                // L1: 포인트 클라우드 표현 (간단한 버전)
                <points position={[0, -0.9, 0]}>
                    <sphereGeometry args={[0.8, 16, 16]} />
                    <pointsMaterial color="#00f2ff" size={0.1} transparent opacity={0.7} />
                </points>
            ) : (
                <primitive object={clonedScene} position={[0, -0.9, 0]} />
            )}
            <Familiar isSync={isSync} stability={stability} />
        </RigidBody>
    )
}

export default WorldScene;
