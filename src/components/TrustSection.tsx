import { useEffect, useRef, useState } from 'react';
import GlassCard from './GlassCard';

const TrustSection = () => {
    const sectionRef = useRef<HTMLElement>(null);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) setIsVisible(true);
        }, { threshold: 0.1 });

        if (sectionRef.current) observer.observe(sectionRef.current);
        return () => observer.disconnect();
    }, []);

    return (
        <section id="trust" ref={sectionRef} className={`section-reveal ${isVisible ? 'visible' : ''}`} style={{ background: 'rgba(255,255,255,0.02)', padding: '100px 10%' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '3rem' }}>
                <div style={{ textAlign: 'left' }}>
                    <h2 className="section-title" style={{ textAlign: 'left', fontSize: '2.5rem' }}>Enterprise-Grade <span className="gradient-text">Trust</span></h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>Nexus is built to handle the most demanding workloads with uncompromising security and global compliance standards.</p>
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                    <GlassCard style={{ textAlign: 'center', padding: '2rem' }}>
                        <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🔒</div>
                        <div style={{ fontWeight: 700 }}>SOC2 Type II</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Certified Security</div>
                    </GlassCard>
                    <GlassCard style={{ textAlign: 'center', padding: '2rem' }}>
                        <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🌍</div>
                        <div style={{ fontWeight: 700 }}>99.99%</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Uptime SLA</div>
                    </GlassCard>
                </div>
            </div>
        </section>
    );
};

export default TrustSection;
