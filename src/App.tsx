import React, { useEffect, useState, Suspense } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Features from './components/Features'
import Footer from './components/Footer'
import AvatarCreator from './components/AvatarCreator'
import IdentityConfigurator from './components/IdentityConfigurator'
const WorldScene = React.lazy(() => import('./components/WorldScene'));
import Manifesto from './components/Manifesto'
import MemoryVault from './components/MemoryVault'
import PrivacyConsent from './components/PrivacyConsent'
import CultureSelector from './components/CultureSelector'
import WelcomeSequence from './components/WelcomeSequence'

import AudioManager from './components/AudioManager'
import NotificationSystem from './components/NotificationSystem'
import config from './utils/config'

// Generate or retrieve persistent user ID
const getUserId = (): string => {
  let userId = localStorage.getItem('anima_user_id');
  if (!userId) {
    userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('anima_user_id', userId);
  }
  return userId;
};

function App() {
  const [mousePos, setMousePos] = useState({ x: 50, y: 50 });
  const [avatarUrl, setAvatarUrl] = useState(null);
  const [isCreatingAvatar, setIsCreatingAvatar] = useState(false);
  const [isConfiguringIdentity, setIsConfiguringIdentity] = useState(false);
  const [identityData, setIdentityData] = useState(null);
  const [neuralCoupling, setNeuralCoupling] = useState(0);
  const [isInWorld, setIsInWorld] = useState(false);
  const [isManifestoOpen, setIsManifestoOpen] = useState(false);
  const [isVaultOpen, setIsVaultOpen] = useState(false);
  const [memories, setMemories] = useState([]);

  // New states for privacy and culture
  const [showPrivacyConsent, setShowPrivacyConsent] = useState(false);
  const [hasConsented, setHasConsented] = useState(false);
  const [culturalContext, setCulturalContext] = useState('default');
  const [showWelcome, setShowWelcome] = useState(false);
  const [maturityLevel, setMaturityLevel] = useState(1);
  const [syncScore, setSyncScore] = useState(0);

  // Check for existing consent on mount
  useEffect(() => {
    const userId = getUserId();
    const savedConsent = localStorage.getItem(`privacy_consent_${userId}`);
    const isFirstVisit = !localStorage.getItem('nexus_visited');

    if (savedConsent) {
      setHasConsented(true);
    } else if (isFirstVisit) {
      // First time visitor - show welcome then privacy consent
      setShowWelcome(true);
      localStorage.setItem('nexus_visited', 'true');
    } else {
      // Returning visitor without consent
      setShowPrivacyConsent(true);
    }

    // Load saved cultural context
    const savedCulture = localStorage.getItem('nexus_cultural_context');
    if (savedCulture) {
      setCulturalContext(savedCulture);
    }

    // Fetch initial maturity status
    fetch(config.getApiUrl(`/api/profile/${userId}`))
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        if (data.profile) {
          setMaturityLevel(data.maturity_level || 1);
          setSyncScore(data.sync_score || 0);
        }
      })
      .catch((error) => {
        // 개발 모드에서만 에러 로깅
        if (config.isDevelopment) {
          console.warn('[App] Failed to fetch profile:', error);
        }
      });
  }, []);

  useEffect(() => {
    const saved = localStorage.getItem('nexus_memories');
    if (saved) setMemories(JSON.parse(saved));
  }, []);

  const saveMemory = (dominantTrait, aesthetic, rank) => {
    const newMemory = {
      date: new Date().toISOString(),
      dominantTrait,
      aesthetic,
      rank
    };
    const updated = [newMemory, ...memories].slice(0, 10);
    setMemories(updated);
    localStorage.setItem('nexus_memories', JSON.stringify(updated));
  };

  const handleCultureChange = (culture: string) => {
    setCulturalContext(culture);
    localStorage.setItem('nexus_cultural_context', culture);
  };

  const handleAvatarExported = (url) => {
    setAvatarUrl(url);
    setIsCreatingAvatar(false);
  };

  const handleIdentityComplete = (data, maturityData) => {
    setIdentityData(data);
    if (maturityData) {
      setMaturityLevel(maturityData.level);
      setSyncScore(maturityData.syncScore);
    }
    setIsConfiguringIdentity(false);
  };

  const handlePrivacyConsent = (granted: boolean) => {
    if (granted) {
      setHasConsented(true);
    }
    setShowPrivacyConsent(false);
  };

  const handleWelcomeComplete = () => {
    setShowWelcome(false);
    setShowPrivacyConsent(true);
  };

  // Show welcome sequence for first-time visitors
  if (showWelcome) {
    return (
      <AudioManager>
        <WelcomeSequence onComplete={handleWelcomeComplete} />
      </AudioManager>
    );
  }

  // Show privacy consent if needed
  if (showPrivacyConsent) {
    return (
      <AudioManager>
        <PrivacyConsent
          userId={getUserId()}
          onConsent={handlePrivacyConsent}
          onClose={() => setShowPrivacyConsent(false)}
        />
      </AudioManager>
    );
  }

  if (isInWorld) {
    return (
      <AudioManager>
        <Suspense fallback={<div style={{ color: 'white' }}>Loading World...</div>}>
          <WorldScene
            avatarUrl={avatarUrl}
            coupling={neuralCoupling}
            maturityLevel={maturityLevel}
            onExit={() => setIsInWorld(false)}
            onSaveMemory={(dominant, aesthetic, txp) => {
              const rank = txp < 0.5 ? "Budding Soul" : txp < 0.8 ? "Kindred Spirit" : "Eternal Partner";
              saveMemory(dominant, aesthetic, rank);
            }}
          />
        </Suspense>
      </AudioManager>
    )
  }

  return (
    <AudioManager>
      <div className="app-container">
        <div
          className="glow-bg"
          style={{
            background: `
            radial-gradient(circle at ${mousePos.x}% ${mousePos.y}%, rgba(176, 38, 255, 0.2), transparent 40%),
            radial-gradient(circle at 20% 20%, rgba(0, 243, 255, 0.15), transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(176, 38, 255, 0.15), transparent 40%)
          `
          }}
        />

        <Navbar onShowMemories={() => setIsVaultOpen(true)} />

        <main>
          <Hero
            onInitialize={() => setIsCreatingAvatar(true)}
            avatarUrl={avatarUrl}
            onEnterWorld={() => setIsInWorld(true)}
            onConfigureIdentity={() => setIsConfiguringIdentity(true)}
            identityData={identityData}
            onShowManifesto={() => setIsManifestoOpen(true)}
            onShowArchive={() => setIsVaultOpen(true)}
            maturityLevel={maturityLevel}
            syncScore={syncScore}
            userId={getUserId()}
          />
          <Features />
        </main>

        <Footer />

        {isCreatingAvatar && (
          <AvatarCreator
            onAvatarExported={handleAvatarExported}
            onCancel={() => setIsCreatingAvatar(false)}
          />
        )}

        {isConfiguringIdentity && (
          <IdentityConfigurator
            onComplete={handleIdentityComplete}
            onCancel={() => setIsConfiguringIdentity(false)}
            coupling={neuralCoupling}
            setCoupling={setNeuralCoupling}
          />
        )}

        {isManifestoOpen && (
          <Manifesto onClose={() => setIsManifestoOpen(false)} />
        )}

        {isVaultOpen && (
          <MemoryVault memories={memories} onClose={() => setIsVaultOpen(false)} />
        )}
      </div>
    </AudioManager>
  )
}

export default App
