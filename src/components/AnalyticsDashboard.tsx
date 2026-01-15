import { useState, useEffect, useRef } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import GlassCard from './GlassCard';
import { Activity, Shield, Zap } from 'lucide-react';

interface DataPoint {
    time: number;
    value: number;
    latency: number;
}

const AnalyticsDashboard = () => {
    const [data, setData] = useState<DataPoint[]>([]);
    const sectionRef = useRef<HTMLElement>(null);
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const initialData: DataPoint[] = Array.from({ length: 20 }, (_, i) => ({
            time: i,
            value: 400 + Math.random() * 200,
            latency: 20 + Math.random() * 10
        }));
        setData(initialData);

        const interval = setInterval(() => {
            setData(prevData => {
                const lastVal = prevData[prevData.length - 1].value;
                const newVal = lastVal + (Math.random() - 0.5) * 50;
                const clampedVal = Math.max(300, Math.min(900, newVal));

                return [
                    ...prevData.slice(1),
                    {
                        time: prevData[prevData.length - 1].time + 1,
                        value: clampedVal,
                        latency: 15 + Math.random() * 15
                    }
                ];
            });
        }, 2000);

        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) setIsVisible(true);
        }, { threshold: 0.1 });

        if (sectionRef.current) observer.observe(sectionRef.current);

        return () => {
            clearInterval(interval);
            observer.disconnect();
        };
    }, []);

    return (
        <section id="analytics" ref={sectionRef} className={`section-reveal ${isVisible ? 'visible' : ''}`} style={{ padding: '100px 10%' }}>
            <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
                <h2 className="section-title">Global <span className="gradient-text">Performance</span></h2>
                <p style={{ color: 'var(--text-muted)', maxWidth: '600px', margin: '0 auto' }}>Monitoring over 2.4 trillion AI inferences per month with sub-millisecond precision.</p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '1.5rem' }}>
                <GlassCard style={{ gridColumn: '1 / span 8', padding: '2rem', minHeight: '400px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem', alignItems: 'center' }}>
                        <div>
                            <h4 style={{ color: 'var(--text-muted)', fontSize: '0.8rem', letterSpacing: '1px' }}>NETWORK THROUGHPUT</h4>
                            <div style={{ fontSize: '1.8rem', fontWeight: 700 }}>{Math.round(data[data.length - 1]?.value || 0)} MB/s</div>
                        </div>
                        <div className="badge" style={{ background: 'rgba(16, 185, 129, 0.1)', color: '#10b981' }}>LIVE STREAM</div>
                    </div>

                    <div style={{ height: '280px', width: '100%' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data}>
                                <defs>
                                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="var(--primary)" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                <Tooltip
                                    contentStyle={{ background: 'rgba(15, 15, 20, 0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                                    itemStyle={{ color: 'white' }}
                                />
                                <Area type="monotone" dataKey="value" stroke="var(--primary)" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" isAnimationActive={false} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </GlassCard>

                <div style={{ gridColumn: '9 / span 4', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <GlassCard style={{ flex: 1, padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.2rem' }}>
                        <div style={{ padding: '1rem', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '12px', color: 'var(--primary)' }}>
                            <Zap size={24} />
                        </div>
                        <div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>AVG LATENCY</div>
                            <div style={{ fontSize: '1.4rem', fontWeight: 700 }}>12.4ms</div>
                        </div>
                    </GlassCard>

                    <GlassCard style={{ flex: 1, padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.2rem' }}>
                        <div style={{ padding: '1rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px', color: '#10b981' }}>
                            <Shield size={24} />
                        </div>
                        <div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>SECURITY SCORE</div>
                            <div style={{ fontSize: '1.4rem', fontWeight: 700 }}>99.9%</div>
                        </div>
                    </GlassCard>

                    <GlassCard style={{ flex: 1, padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.2rem' }}>
                        <div style={{ padding: '1rem', background: 'rgba(245, 158, 11, 0.1)', borderRadius: '12px', color: '#f59e0b' }}>
                            <Activity size={24} />
                        </div>
                        <div>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>NODES ONLINE</div>
                            <div style={{ fontSize: '1.4rem', fontWeight: 700 }}>4,182</div>
                        </div>
                    </GlassCard>
                </div>
            </div>
        </section>
    );
};

export default AnalyticsDashboard;
