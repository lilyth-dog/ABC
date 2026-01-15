import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface DNAHelixProps {
    count?: number;
    radius?: number;
    height?: number;
    color1?: string;
    color2?: string;
}

interface DNAPoint {
    x: number;
    y: number;
    z: number;
    color: string;
}

const DNAHelix = ({ count = 40, radius = 2, height = 10, color1 = '#00d4ff', color2 = '#ff00ff' }: DNAHelixProps) => {
    const groupRef = useRef<THREE.Group>(null);

    const points = useMemo<DNAPoint[]>(() => {
        const tempPoints: DNAPoint[] = [];
        for (let i = 0; i < count; i++) {
            const t = i / count;
            const angle = t * Math.PI * 4;
            const y = (t - 0.5) * height;

            const x1 = Math.cos(angle) * radius;
            const z1 = Math.sin(angle) * radius;

            const x2 = Math.cos(angle + Math.PI) * radius;
            const z2 = Math.sin(angle + Math.PI) * radius;

            tempPoints.push({ x: x1, y, z: z1, color: color1 });
            tempPoints.push({ x: x2, y, z: z2, color: color2 });
        }
        return tempPoints;
    }, [count, radius, height, color1, color2]);

    useFrame((_, delta) => {
        if (groupRef.current) {
            groupRef.current.rotation.y += delta * 0.5;
        }
    });

    return (
        <group ref={groupRef}>
            {points.map((point, index) => (
                <mesh key={index} position={[point.x, point.y, point.z]}>
                    <sphereGeometry args={[0.2, 16, 16]} />
                    <meshStandardMaterial
                        color={point.color}
                        emissive={point.color}
                        emissiveIntensity={0.8}
                        roughness={0.1}
                        metalness={0.8}
                    />
                </mesh>
            ))}

            {Array.from({ length: count }).map((_, i) => {
                const t = i / count;
                const angle = t * Math.PI * 4;
                return (
                    <mesh key={`bond-${i}`} position={[0, (t - 0.5) * height, 0]} rotation={[0, angle, Math.PI / 2]}>
                        <cylinderGeometry args={[0.03, 0.03, radius * 2, 8]} />
                        <meshBasicMaterial color="#ffffff" opacity={0.2} transparent />
                    </mesh>
                )
            })}
        </group>
    );
};

export default DNAHelix;
