import { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import NeuralEngine from '../utils/NeuralEngine';

interface BrainWaveVisualizerProps {
    couplingStrength?: number;
}

const BrainWaveVisualizer = ({ couplingStrength = 0 }: BrainWaveVisualizerProps) => {
    const count = 500;
    const engine = useMemo(() => new NeuralEngine(count), [count]);
    const mesh = useRef<THREE.InstancedMesh>(null);

    const [dummy] = useState(() => new THREE.Object3D());
    const [positions] = useState(() => {
        const pos = new Float32Array(count * 3);
        for (let i = 0; i < count; i++) {
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.acos((Math.random() * 2) - 1);
            const r = 4 + (Math.random() - 0.5);

            pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
            pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
            pos[i * 3 + 2] = r * Math.cos(phi);
        }
        return pos;
    });

    useFrame(() => {
        engine.setCoupling(couplingStrength);
        const { phases } = engine.update();

        if (mesh.current) {
            for (let i = 0; i < count; i++) {
                const i3 = i * 3;

                dummy.position.set(positions[i3], positions[i3 + 1], positions[i3 + 2]);

                const signal = Math.sin(phases[i]);
                const scale = 0.5 + (signal > 0.8 ? 0.3 : 0);
                dummy.scale.set(scale, scale, scale);

                dummy.updateMatrix();
                mesh.current.setMatrixAt(i, dummy.matrix);

                const hue = (phases[i] / (Math.PI * 2));
                const color = new THREE.Color().setHSL(hue, 1.0, 0.5);
                mesh.current.setColorAt(i, color);
            }
            mesh.current.instanceMatrix.needsUpdate = true;
            if (mesh.current.instanceColor) {
                mesh.current.instanceColor.needsUpdate = true;
            }
        }
    });

    return (
        <>
            <instancedMesh ref={mesh} args={[undefined, undefined, count]}>
                <sphereGeometry args={[0.05, 8, 8]} />
                <meshStandardMaterial toneMapped={false} vertexColors />
            </instancedMesh>
        </>
    );
};

export default BrainWaveVisualizer;
