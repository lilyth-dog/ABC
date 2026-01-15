import { useState, useEffect, useRef } from 'react';
import GlassCard from './GlassCard';
import { Terminal, Globe } from 'lucide-react';

const InfrastructureLogs = () => {
    const [logs, setLogs] = useState([
        '[SYSTEM] Nexus Core initialized.',
        '[AUTH] Enterprise gateway established.',
        '[NODES] Scaling internal clusters...'
    ]);
    const logContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const logPool = [
            '[MODEL] Efficient-LLM deployed to edge-us-east-1',
            '[TRAFFIC] Redirecting 42k requests to Paris node',
            '[SYNC] Global state synchronized in 8ms',
            '[SECURITY] Blocked potential DDoS from 182.4.91.x',
            '[OPTIMIZE] KV-Cache compressed by 14%',
            '[COMPUTE] T4 Cluster scaling to 48 units',
            '[NETWORK] Latency spike detected in Tokyo; rerouting...'
        ];

        const interval = setInterval(() => {
            setLogs(prev => [...prev.slice(-8), logPool[Math.floor(Math.random() * logPool.length)]]);
        }, 3000);

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (logContainerRef.current) {
            logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <section id="infrastructure" style={{ padding: '80px 10%' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.2fr', gap: '4rem', alignItems: 'center' }}>
                <div>
                    <span className="badge">Differentiator</span>
                    <h2 style={{ fontSize: '3rem', marginBottom: '1.5rem', lineHeight: 1.1 }}>Live Infrastructure <span className="gradient-text">Logs</span></h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem', marginBottom: '2rem' }}>
                        Nexus isn't just a dashboard. It's a living ecosystem. Watch your global model deployment in real-time with our low-level system logs.
                    </p>
                    <div style={{ display: 'flex', gap: '2rem' }}>
                        <div>
                            <div style={{ color: 'var(--primary)', marginBottom: '0.5rem' }}>
                                <Terminal size={32} />
                            </div>
                            <h4 style={{ fontWeight: 700 }}>Integrated CLI</h4>
                            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Control infra via terminal.</p>
                        </div>
                        <div>
                            <div style={{ color: '#10b981', marginBottom: '0.5rem' }}>
                                <Globe size={32} />
                            </div>
                            <h4 style={{ fontWeight: 700 }}>Edge-First</h4>
                            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Deploy in 42 regions.</p>
                        </div>
                    </div>
                </div>

                <GlassCard style={{ padding: '0', overflow: 'hidden', height: '350px', background: '#050508', border: '1px solid rgba(255,255,255,0.05)' }}>
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', gap: '8px' }}>
                        <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ff5f56' }}></div>
                        <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ffbd2e' }}></div>
                        <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#27c93f' }}></div>
                        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginLeft: '1rem', fontFamily: 'monospace' }}>nexus-shell --monitor</span>
                    </div>
                    <div ref={logContainerRef} style={{ padding: '1.5rem', fontFamily: 'monospace', fontSize: '0.85rem', color: '#10b981', overflowY: 'auto', height: 'calc(100% - 45px)' }}>
                        {logs.map((log, i) => (
                            <div key={i} style={{ marginBottom: '8px', opacity: (i + 1) / logs.length }}>
                                <span style={{ color: 'rgba(255,255,255,0.3)', marginRight: '10px' }}>{new Date().toLocaleTimeString()}</span>
                                {log}
                            </div>
                        ))}
                        <div style={{ width: '8px', height: '16px', background: '#10b981', display: 'inline-block', animation: 'pulsate 1s infinite', verticalAlign: 'middle' }}></div>
                    </div>
                </GlassCard>
            </div>
        </section>
    );
};

export default InfrastructureLogs;
