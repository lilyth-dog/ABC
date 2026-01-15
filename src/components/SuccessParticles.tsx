import { useEffect, useState } from 'react';

interface SuccessParticlesProps {
    color?: string;
    count?: number;
    duration?: number;
    onComplete?: () => void;
}

interface Particle {
    id: number;
    x: number;
    y: number;
    size: number;
    delay: number;
    duration: number;
    type: 'heart' | 'star' | 'circle';
    color: string;
}

const SuccessParticles = ({
    color = 'magenta',
    count = 40,
    duration = 3000,
    onComplete
}: SuccessParticlesProps) => {
    const [particles, setParticles] = useState<Particle[]>([]);
    const [isVisible, setIsVisible] = useState(true);

    const colors = {
        magenta: ['#ff00ff', '#ff66ff', '#ff99ff'],
        cyan: ['#00ffff', '#66ffff', '#99ffff'],
        gold: ['#ffd700', '#ffea00', '#fff200'],
        rainbow: ['#ff0000', '#ff7f00', '#ffff00', '#00ff00', '#0000ff', '#8b00ff']
    };

    const particleColors = colors[color] || colors.magenta;

    useEffect(() => {
        const newParticles: Particle[] = Array.from({ length: count }, (_, i) => ({
            id: i,
            x: 50 + (Math.random() - 0.5) * 20,
            y: 50 + (Math.random() - 0.5) * 20,
            size: 8 + Math.random() * 16,
            delay: Math.random() * 0.5,
            duration: 1 + Math.random() * 1.5,
            type: ['heart', 'star', 'circle'][Math.floor(Math.random() * 3)] as 'heart' | 'star' | 'circle',
            color: particleColors[Math.floor(Math.random() * particleColors.length)]
        }));

        setParticles(newParticles);

        const timeout = setTimeout(() => {
            setIsVisible(false);
            onComplete?.();
        }, duration);

        return () => clearTimeout(timeout);
    }, [count, duration, onComplete, particleColors]);

    if (!isVisible) return null;

    return (
        <div className="success-particles-container">
            {particles.map(particle => (
                <div
                    key={particle.id}
                    className={`success-particle particle-${particle.type}`}
                    style={{
                        left: `${particle.x}%`,
                        top: `${particle.y}%`,
                        fontSize: `${particle.size}px`,
                        color: particle.color,
                        animationDelay: `${particle.delay}s`,
                        animationDuration: `${particle.duration}s`,
                        textShadow: `0 0 10px ${particle.color}, 0 0 20px ${particle.color}`
                    }}
                >
                    {particle.type === 'heart' && '💖'}
                    {particle.type === 'star' && '✨'}
                    {particle.type === 'circle' && '●'}
                </div>
            ))}

            <style dangerouslySetInnerHTML={{
                __html: `
                .success-particles-container {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    pointer-events: none;
                    z-index: 10000;
                    overflow: hidden;
                }
                .success-particle {
                    position: absolute;
                    animation: particleExplode 2s forwards ease-out;
                }
                @keyframes particleExplode {
                    0% {
                        opacity: 1;
                        transform: translate(-50%, -50%) scale(0);
                    }
                    10% {
                        transform: translate(-50%, -50%) scale(1.5);
                    }
                    100% {
                        opacity: 0;
                        transform: translate(
                            calc(-50% + ${() => (Math.random() - 0.5) * 400}px),
                            calc(-50% + ${() => (Math.random() - 0.5) * 400}px)
                        ) scale(0.5) rotate(${() => Math.random() * 360}deg);
                    }
                }
                .particle-heart {
                    animation-name: particleExplodeHeart;
                }
                .particle-star {
                    animation-name: particleExplodeStar;
                }
                @keyframes particleExplodeHeart {
                    0% { opacity: 1; transform: translate(-50%, -50%) scale(0); }
                    20% { transform: translate(-50%, -50%) scale(1.8); }
                    40% { transform: translate(-50%, -50%) scale(1.2); }
                    100% { 
                        opacity: 0; 
                        transform: translate(
                            calc(-50% + var(--tx, 100px)),
                            calc(-50% + var(--ty, -200px))
                        ) scale(0.3); 
                    }
                }
                @keyframes particleExplodeStar {
                    0% { opacity: 1; transform: translate(-50%, -50%) scale(0) rotate(0deg); }
                    30% { transform: translate(-50%, -50%) scale(1.5) rotate(180deg); }
                    100% { 
                        opacity: 0; 
                        transform: translate(
                            calc(-50% + var(--tx, 150px)),
                            calc(-50% + var(--ty, -150px))
                        ) scale(0) rotate(720deg); 
                    }
                }
            `}} />
        </div>
    );
};

export default SuccessParticles;
