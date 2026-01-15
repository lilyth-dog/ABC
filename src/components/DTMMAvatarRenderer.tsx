/**
 * DTMM (Digital Twin Maturity Model) 기반 아바타 렌더러
 * 레벨별로 다른 시각적 표현을 제공:
 * - L1 (Echo): 추상적 포인트 클라우드
 * - L2 (Reflection): 와이어프레임/홀로그램
 * - L3 (Synthesis): 풀 메시 디지털 휴먼
 */
import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import { Points, BufferGeometry, BufferAttribute, Mesh } from 'three';
import * as THREE from 'three';

interface DTMMAvatarRendererProps {
    avatarUrl: string;
    maturityLevel: number;
    position?: [number, number, number];
    scale?: number;
}

/**
 * L1 (Echo): 추상적 포인트 클라우드
 * 아바타의 지오메트리에서 포인트를 추출하여 추상적으로 표현
 */
function EchoPointCloud({ scene, position, scale }: { scene: THREE.Object3D; position: [number, number, number]; scale: number }) {
    const pointsRef = useRef<Points>(null);
    
    // 아바타 지오메트리에서 포인트 추출
    const pointsGeometry = useMemo(() => {
        const geometry = new BufferGeometry();
        const positions: number[] = [];
        const colors: number[] = [];
        
        scene.traverse((child) => {
            if (child instanceof Mesh && child.geometry) {
                const pos = child.geometry.attributes.position;
                if (pos) {
                    // 더 정교한 포인트 샘플링 (노말 벡터 기반)
                    const normal = child.geometry.attributes.normal;
                    for (let i = 0; i < pos.count; i += 2) { // 더 많은 포인트 (2개마다 1개)
                        const x = pos.getX(i);
                        const y = pos.getY(i);
                        const z = pos.getZ(i);
                        positions.push(x, y, z);
                        
                        // 노말 벡터 기반 색상 (표면 방향에 따라)
                        let nx = 0, ny = 0, nz = 1;
                        if (normal) {
                            nx = normal.getX(i);
                            ny = normal.getY(i);
                            nz = normal.getZ(i);
                        }
                        
                        // 거리와 노말 기반 색상
                        const distance = Math.sqrt(x * x + y * y + z * z);
                        const intensity = Math.max(0.3, 1 - distance / 2.5);
                        const normalIntensity = (nx + ny + nz) / 3;
                        
                        // 시안-마젠타 그라데이션
                        const r = 0.0;
                        const g = 0.7 + normalIntensity * 0.3;
                        const b = 1.0;
                        colors.push(r, g, b, intensity * 0.9);
                    }
                }
            }
        });
        
        geometry.setAttribute('position', new BufferAttribute(new Float32Array(positions), 3));
        geometry.setAttribute('color', new BufferAttribute(new Float32Array(colors), 4));
        
        return geometry;
    }, [scene]);
    
    // 포인트 클라우드 애니메이션
    useFrame((state) => {
        if (pointsRef.current) {
            pointsRef.current.rotation.y = state.clock.elapsedTime * 0.2;
            const positions = pointsRef.current.geometry.attributes.position;
            if (positions) {
                for (let i = 0; i < positions.count; i++) {
                    const y = positions.getY(i);
                    positions.setY(i, y + Math.sin(state.clock.elapsedTime * 2 + i * 0.1) * 0.01);
                }
                positions.needsUpdate = true;
            }
        }
    });
    
    return (
        <Points ref={pointsRef} geometry={pointsGeometry} position={position} scale={scale}>
            <pointsMaterial
                size={0.12}
                vertexColors
                transparent
                opacity={0.8}
                sizeAttenuation
                blending={THREE.AdditiveBlending}
            />
        </Points>
    );
}

/**
 * L2 (Reflection): 와이어프레임/홀로그램 표현
 * 반투명 와이어프레임과 홀로그램 효과
 */
function ReflectionWireframe({ scene, position, scale }: { scene: THREE.Object3D; position: [number, number, number]; scale: number }) {
    const clonedScene = useMemo(() => {
        const cloned = scene.clone();
        cloned.traverse((child) => {
            if (child instanceof Mesh) {
                child.material = child.material.clone();
                child.material.wireframe = true;
                child.material.transparent = true;
                child.material.opacity = 0.6;
                child.material.color.set("#7000ff");
                child.material.emissive.set("#3d00ff");
                child.material.emissiveIntensity = 0.5;
            }
        });
        return cloned;
    }, [scene]);
    
    const wireframeRef = useRef<THREE.Group>(null);
    
    // 홀로그램 깜빡임 및 글로우 효과
    useFrame((state) => {
        if (wireframeRef.current) {
            const time = state.clock.elapsedTime;
            wireframeRef.current.traverse((child) => {
                if (child instanceof Mesh && child.material) {
                    // 더 부드러운 깜빡임
                    const opacity = 0.5 + Math.sin(time * 1.5) * 0.15;
                    child.material.opacity = opacity;
                    
                    // 글로우 강도 변화
                    const glowIntensity = 0.4 + Math.sin(time * 2) * 0.2;
                    if (child.material.emissiveIntensity !== undefined) {
                        child.material.emissiveIntensity = glowIntensity;
                    }
                }
            });
        }
    });
    
    return (
        <group ref={wireframeRef} position={position} scale={scale}>
            <primitive object={clonedScene} />
            {/* 홀로그램 글로우 효과 (다중 레이어) */}
            <mesh position={[0, 0, 0]}>
                <sphereGeometry args={[1.5, 32, 32]} />
                <meshBasicMaterial
                    color="#7000ff"
                    transparent
                    opacity={0.15}
                    side={THREE.BackSide}
                />
            </mesh>
            <mesh position={[0, 0, 0]}>
                <sphereGeometry args={[1.8, 32, 32]} />
                <meshBasicMaterial
                    color="#3d00ff"
                    transparent
                    opacity={0.05}
                    side={THREE.BackSide}
                />
            </mesh>
        </group>
    );
}

/**
 * L3 (Synthesis): 풀 메시 디지털 휴먼
 * 완전한 텍스처와 재질을 가진 아바타
 */
function SynthesisFullMesh({ scene, position, scale }: { scene: THREE.Object3D; position: [number, number, number]; scale: number }) {
    const clonedScene = useMemo(() => {
        const cloned = scene.clone();
        cloned.traverse((child) => {
            if (child instanceof Mesh) {
                child.material = child.material.clone();
                child.material.wireframe = false;
                child.material.transparent = false;
                child.material.opacity = 1.0;
                // L3에서는 더 강한 글로우 및 반사 효과
                if (child.material.emissive) {
                    child.material.emissive.set("#ffffff");
                    child.material.emissiveIntensity = 0.15;
                }
                // 반사율 증가
                if ('roughness' in child.material) {
                    (child.material as any).roughness = 0.3;
                }
                if ('metalness' in child.material) {
                    (child.material as any).metalness = 0.2;
                }
            }
        });
        return cloned;
    }, [scene]);
    
    return (
        <primitive object={clonedScene} position={position} scale={scale} />
    );
}

/**
 * 메인 DTMM 아바타 렌더러
 */
export function DTMMAvatarRenderer({ 
    avatarUrl, 
    maturityLevel, 
    position = [0, -1, 0], 
    scale = 1.2 
}: DTMMAvatarRendererProps) {
    const { scene } = useGLTF(avatarUrl);
    
    // 레벨에 따라 다른 렌더링
    if (maturityLevel === 1) {
        // L1: Echo - 포인트 클라우드
        return <EchoPointCloud scene={scene} position={position} scale={scale} />;
    } else if (maturityLevel === 2) {
        // L2: Reflection - 와이어프레임
        return <ReflectionWireframe scene={scene} position={position} scale={scale} />;
    } else {
        // L3: Synthesis - 풀 메시
        return <SynthesisFullMesh scene={scene} position={position} scale={scale} />;
    }
}
