import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, Float } from '@react-three/drei';
import * as THREE from 'three';

interface FamiliarProps {
    isSync: boolean;
    stability: boolean;
}

const Familiar = ({ isSync, stability }: FamiliarProps) => {
    const meshRef = useRef<THREE.Mesh>(null);
    const lightRef = useRef<THREE.PointLight>(null);

    useFrame((state) => {
        const t = state.clock.getElapsedTime();
        if (meshRef.current) {
            // Gentle orbiting movement around the player's head area (relative to parent)
            meshRef.current.position.y = Math.sin(t * 2) * 0.2 + 1.5;
            meshRef.current.position.x = Math.cos(t) * 1.2;
            meshRef.current.position.z = Math.sin(t) * 1.2;

            // Pulse scale based on stability
            const s = stability ? 1.0 + Math.sin(t * 4) * 0.1 : 0.8;
            meshRef.current.scale.set(s, s, s);
        }
        if (lightRef.current) {
            lightRef.current.intensity = isSync ? 2.0 + Math.sin(t * 5) : 0.5;
        }
    });

    return (
        <group>
            <Float speed={2} rotationIntensity={1} floatIntensity={1}>
                <Sphere ref={meshRef} args={[0.3, 32, 32]}>
                    <MeshDistortMaterial
                        color={isSync ? "#ff00ff" : "#00f3ff"}
                        speed={stability ? 2 : 5}
                        distort={stability ? 0.3 : 0.6}
                        radius={1}
                        emissive={isSync ? "#ff00ff" : "#00f3ff"}
                        emissiveIntensity={1}
                    />
                    <pointLight ref={lightRef} color={isSync ? "#ff00ff" : "#00f3ff"} distance={5} />
                </Sphere>
            </Float>
        </group>
    );
};

export default Familiar;
