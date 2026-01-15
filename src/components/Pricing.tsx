import { useEffect, useRef, useState } from 'react';
import GlassCard from './GlassCard';

const Pricing = () => {
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
        <section id="pricing" ref={sectionRef} className={`section-reveal ${isVisible ? 'visible' : ''}`}>
            <h2 className="section-title">Choose Your <span className="gradient-text">Plan</span></h2>
            <div className="pricing-grid">
                <GlassCard className="pricing-card">
                    <h3>Starter</h3>
                    <div className="price">$0<span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>/mo</span></div>
                    <ul style={{ listStyle: 'none', textAlign: 'left', margin: '1.5rem 0' }}>
                        <li style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>✓ Basic Features</li>
                        <li style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>✓ 1 Project</li>
                        <li style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>✓ Community Support</li>
                    </ul>
                    <button className="btn btn-outline">Join Free</button>
                </GlassCard>

                <GlassCard className="pricing-card highlighted">
                    <div className="popular-tab" style={{ position: 'absolute', top: '-12px', left: '50%', transform: 'translateX(-50%)', background: 'var(--primary)', padding: '0.25rem 1rem', borderRadius: '100px', fontSize: '0.8rem', fontWeight: 700 }}>
                        Most Popular
                    </div>
                    <h3>Pro</h3>
                    <div className="price">$29<span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>/mo</span></div>
                    <ul style={{ listStyle: 'none', textAlign: 'left', margin: '1.5rem 0' }}>
                        <li style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>✓ All Features</li>
                        <li style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>✓ Unlimited Projects</li>
                        <li style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>✓ Priority Support</li>
                        <li style={{ marginBottom: '0.75rem', color: 'var(--text-muted)' }}>✓ Custom Domains</li>
                    </ul>
                    <button className="btn btn-primary">Get Started</button>
                </GlassCard>
            </div>
        </section>
    );
};

export default Pricing;
