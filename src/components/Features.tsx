import { useEffect, useRef, useState, ReactNode } from 'react';
import GlassCard from './GlassCard';

interface Feature {
    title: string;
    description: string;
    icon: string;
}

const Features = () => {
    const sectionRef = useRef<HTMLElement>(null);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) setIsVisible(true);
        }, { threshold: 0.1 });

        if (sectionRef.current) observer.observe(sectionRef.current);
        return () => observer.disconnect();
    }, []);

    const features: Feature[] = [
        {
            title: "하이퍼-피델리티 엔진",
            description: "언리얼 엔진 5를 기반으로, 우리의 아바타는 가상과 현실의 경계를 허뭅니다.",
            icon: "🧬"
        },
        {
            title: "AI 페르소나 코어",
            description: "당신을 기억하는 아이돌. 우리의 AI는 모든 팬과 고유하고 진화하는 상호작용을 보장합니다.",
            icon: "🧠"
        },
        {
            title: "크로스-버스 커넥트",
            description: "당신의 디지털 휴먼 트윈을 VRChat, Roblox, Unity 등으로 원활하게 내보내세요.",
            icon: "🌐"
        }
    ];

    return (
        <section id="features" ref={sectionRef} className={`section-reveal ${isVisible ? 'visible' : ''}`}>
            <h2 className="section-title">Nexus World <span className="highlight">주요 기능</span></h2>
            <div className="features-grid">
                {features.map((feature, index) => (
                    <GlassCard key={index} className="feature-card">
                        <div className="feature-icon">{feature.icon}</div>
                        <h3>{feature.title}</h3>
                        <p>{feature.description}</p>
                    </GlassCard>
                ))}
            </div>
        </section>
    );
};

export default Features;
