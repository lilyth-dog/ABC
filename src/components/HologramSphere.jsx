import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, Stars, Trail } from '@react-three/drei';

const AnimatedSphere = () => {
  const sphereRef = useRef();

  useFrame(({ clock }) => {
    const t = clock.getElapsedTime();
    if (sphereRef.current) {
        sphereRef.current.rotation.x = t * 0.2;
        sphereRef.current.rotation.y = t * 0.3;
    }
  });

  return (
    <Sphere ref={sphereRef} args={[1, 64, 64]} scale={1.8}>
      <MeshDistortMaterial
        color="#00f3ff"
        attach="material"
        distort={0.4}
        speed={2}
        roughness={0.2}
        metalness={0.8}
        emissive="#b026ff" // Magenta glow
        emissiveIntensity={0.5}
        wireframe={true} // Cyberpunk feel
      />
    </Sphere>
  );
};

const Core = () => {
    const coreRef = useRef();
    useFrame(({ clock }) => {
        const t = clock.getElapsedTime();
        if (coreRef.current) {
            coreRef.current.scale.setScalar(1 + Math.sin(t * 3) * 0.1); // Pulse effect
        }
    });

    return (
        <Sphere ref={coreRef} args={[0.5, 32, 32]}>
             <meshStandardMaterial 
                color="#ffffff" 
                emissive="#ffffff"
                emissiveIntensity={1}
                toneMapped={false}
             />
        </Sphere>
    )
}

const HologramSphere = () => {
  return (
    <div className="hologram-container" style={{ width: '100%', height: '100%', minHeight: '500px' }}>
      <Canvas camera={{ position: [0, 0, 4] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#00f3ff"/>
        <pointLight position={[-10, -10, -10]} intensity={0.5} color="#ff00ff"/>
        
        <AnimatedSphere />
        <Core />
        <Stars radius={100} depth={50} count={2000} factor={4} saturation={0} fade speed={1} />
      </Canvas>
    </div>
  );
};

export default HologramSphere;
