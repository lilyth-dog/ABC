import { useEffect, useRef, useState } from 'react';
import { useAudio } from './AudioManager';

interface AvatarCreatorProps {
    onAvatarExported: (url: string) => void;
    onCancel: () => void;
}

const AvatarCreator = ({ onAvatarExported, onCancel }: AvatarCreatorProps) => {
    const subdomain = 'demo';
    const iframeUrl = `https://${subdomain}.readyplayer.me/avatar?frameApi`;
    const iframeRef = useRef<HTMLIFrameElement>(null);
    const { playChime } = useAudio();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        playChime(600, 'sine', 0.1);

        const timer = setTimeout(() => {
            setLoading(false);
            playChime(1000, 'sine', 0.1);
        }, 2000);

        const handleMessage = (event: MessageEvent) => {
            if (event.source !== iframeRef.current?.contentWindow) return;

            try {
                const json = JSON.parse(event.data);

                if (json.source === 'readyplayerme' && json.eventName === 'v1.avatar.exported') {
                    console.log('Avatar URL:', json.data.url);
                    playChime(1200, 'sine', 0.15);
                    onAvatarExported(json.data.url);
                }
            } catch (error) {
                // Ignore non-JSON messages
            }
        };

        window.addEventListener('message', handleMessage);
        return () => {
            window.removeEventListener('message', handleMessage);
            clearTimeout(timer);
        };
    }, [onAvatarExported, playChime]);

    return (
        <div className="avatar-creator-overlay">
            <div className="avatar-creator-header">
                <button onClick={onCancel} className="btn btn-secondary glass-effect" style={{ borderColor: '#ff0055', color: '#ff0055' }}>
                    시퀀스 중단 (ABORT)
                </button>
            </div>

            {loading ? (
                <div className="loading-container">
                    <h2 className="glitch-text" style={{ fontSize: '2rem' }}>뉴럴 링크 설정 중...</h2>
                    <div className="scanner-line"></div>
                    <p style={{ marginTop: '1rem', color: '#00f3ff', opacity: 0.7 }}>생체 데이터 암호화 중</p>
                </div>
            ) : (
                <iframe
                    ref={iframeRef}
                    src={iframeUrl}
                    allow="camera *; microphone *"
                    className="avatar-creator-iframe"
                    title="Avatar Creator"
                />
            )}
        </div>
    );
};

export default AvatarCreator;
