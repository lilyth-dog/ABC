
import React, { useEffect, useRef, useState } from 'react';
import { useAudio } from './AudioManager';

const AvatarCreator = ({ onAvatarExported, onCancel }) => {
  const subdomain = 'demo'; 
  const iframeUrl = `https://${subdomain}.readyplayer.me/avatar?frameApi`;
  const iframeRef = useRef(null);
  const { playChime } = useAudio();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Play entrance sound
    playChime(600, 'sine', 0.1); 
    
    // Simulate connection delay for effect
    const timer = setTimeout(() => {
        setLoading(false);
        playChime(1000, 'sine', 0.1); // Success chime when loaded
    }, 2000);

    const handleMessage = (event) => {
      const source = event.srcElement || event.originalEvent?.source;
      if (source !== iframeRef.current?.contentWindow) return;

      try {
        const json = JSON.parse(event.data);

        // Ready Player Me Event: v1.avatar.exported
        if (json.source === 'readyplayerme' && json.eventName === 'v1.avatar.exported') {
          console.log('Avatar URL:', json.data.url);
          playChime(1200, 'sine', 0.15); // Celebration chime
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
        <button onClick={onCancel} className="btn btn-secondary glass-effect" style={{borderColor: '#ff0055', color: '#ff0055'}}>
             ABORT SEQUENCE
        </button>
      </div>

      {loading ? (
          <div className="loading-container">
              <h2 className="glitch-text" style={{fontSize: '2rem'}}>ESTABLISHING NEURAL LINK...</h2>
              <div className="scanner-line"></div>
              <p style={{marginTop: '1rem', color: '#00f3ff', opacity: 0.7}}>Encrypting Bio-Metric Data</p>
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
