import { useEffect, useRef, useState } from 'react';
import GlassCard from './GlassCard';

interface IntegrationLogo {
    name: string;
    color: string;
}

const IntegrationHub = () => {
    const sectionRef = useRef<HTMLElement>(null);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) setIsVisible(true);
        }, { threshold: 0.1 });

        if (sectionRef.current) observer.observe(sectionRef.current);
        return () => observer.disconnect();
    }, []);

    const logos: IntegrationLogo[] = [
        { name: 'AWS', color: '#FF9900' },
        { name: 'Google Cloud', color: '#4285F4' },
        { name: 'Snowflake', color: '#29B5E8' },
        { name: 'Azure', color: '#0078D4' },
        { name: 'OpenAI', color: '#74AA9C' },
        { name: 'Databricks', color: '#FF3621' }
    ];

    return (
        <section id="integrations" ref={sectionRef} className={`section-reveal ${isVisible ? 'visible' : ''}`} style={{ padding: '80px 10%' }}>
            <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem', letterSpacing: '2px', marginBottom: '3rem' }}>BUILT FOR THE MODERN ECOSYSTEM</h3>
            <div className="logo-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '4rem', opacity: 0.6 }}>
                {logos.map((logo, i) => (
                    <div
                        key={i}
                        style={{
                            fontWeight: 800,
                            fontSize: '1.2rem',
                            color: 'white',
                            filter: 'grayscale(100%) brightness(0.8)',
                            transition: 'filter 0.3s ease'
                        }}
                        onMouseOver={e => (e.currentTarget.style.filter = 'grayscale(0%)')}
                        onMouseOut={e => (e.currentTarget.style.filter = 'grayscale(100%) brightness(0.8)')}
                    >
                        {logo.name}
                    </div>
                ))}
            </div>
        </section>
    );
};

export default IntegrationHub;
