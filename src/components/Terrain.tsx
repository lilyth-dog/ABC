import React, { useMemo } from 'react';
import * as THREE from 'three';
import { RigidBody } from '@react-three/rapier';

interface TerrainProps {
    aesthetic: string;
}

const Terrain = ({ aesthetic }: TerrainProps) => {
    const size = 64;
    const resolution = 64;

    const { geometry, vertices } = useMemo(() => {
        const geo = new THREE.PlaneGeometry(100, 100, resolution, resolution);
        geo.rotateX(-Math.PI / 2);

        const posAttr = geo.getAttribute('position') as THREE.BufferAttribute;
        const verts = posAttr.array as Float32Array;

        // Simple procedural noise for terrain
        for (let i = 0; i < verts.length; i += 3) {
            const x = verts[i];
            const z = verts[i + 2];

            // Perlin-like pseudo-noise
            let height = 0;
            if (aesthetic === 'Zen/Minimal') {
                height = Math.sin(x * 0.1) * Math.cos(z * 0.1) * 2;
            } else if (aesthetic === 'Neon/Vibrant') {
                height = (Math.sin(x * 0.3) + Math.cos(z * 0.3)) * 3;
            } else { // Cyber/Industrial
                height = (Math.floor(x / 5) % 2 === 0 ? 1 : 0) * (Math.floor(z / 5) % 2 === 0 ? 1 : 0) * 2;
            }

            verts[i + 1] = height; // Set Y coordinate
        }

        geo.computeVertexNormals();
        return { geometry: geo, vertices: verts };
    }, [aesthetic]);

    // Terrain color mapping
    const colorMap = {
        'Zen/Minimal': '#e0f7fa',
        'Cyber/Industrial': '#001a1a',
        'Neon/Vibrant': '#1a001a'
    };

    return (
        <RigidBody type="fixed" colliders="trimesh">
            <mesh geometry={geometry} receiveShadow>
                <meshStandardMaterial
                    color={colorMap[aesthetic as keyof typeof colorMap] || '#1a1a3a'}
                    wireframe={aesthetic === 'Cyber/Industrial'}
                />
            </mesh>

            {/* Grid helper for Cyber vibe */}
            {aesthetic === 'Cyber/Industrial' && (
                <gridHelper args={[100, 20, '#00d4ff', '#004444']} position={[0, 2.1, 0]} />
            )}
        </RigidBody>
    );
};

export default Terrain;
