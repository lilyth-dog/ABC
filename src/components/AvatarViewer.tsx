import { DTMMAvatarRenderer } from './DTMMAvatarRenderer';

const Model = ({ url, maturityLevel }: { url: string; maturityLevel: number }) => {
    return (
        <DTMMAvatarRenderer 
            avatarUrl={url} 
            maturityLevel={maturityLevel}
            position={[0, -1, 0]}
            scale={1.2}
        />
    );
};

interface AvatarViewerProps {
    avatarUrl: string;
    maturityLevel?: number;
}

const AvatarViewer = ({ avatarUrl, maturityLevel = 1 }: AvatarViewerProps) => {
    return (
        <div className="avatar-viewer-container" style={{ width: '500px', height: '500px' }}>
            <Canvas camera={{ position: [0, 1.5, 3], fov: 50 }}>
                <ambientLight intensity={0.5} />
                <directionalLight position={[10, 10, 5]} intensity={1} />
                <Suspense fallback={null}>
                    <Model url={avatarUrl} maturityLevel={maturityLevel} />
                    <Environment preset="city" />
                </Suspense>
                <OrbitControls minPolarAngle={Math.PI / 4} maxPolarAngle={Math.PI / 2} minDistance={2} maxDistance={5} />
            </Canvas>
        </div>
    );
};

export default AvatarViewer;
