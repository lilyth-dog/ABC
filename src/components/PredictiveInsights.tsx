/**
 * 예측 인사이트 대시보드
 * 행동 트렌드, 스트레스 분석, 이상 감지 결과를 시각화
 */
import { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import GlassCard from './GlassCard';
import { AlertTriangle, TrendingUp, TrendingDown, Activity, Brain, Heart } from 'lucide-react';
import { config } from '../utils/config';

interface PredictiveInsightsProps {
    userId: string;
}

interface StressAnalysis {
    status: string;
    stress_level?: number;
    stress_category?: string;
    indicators?: string[];
    recommendation?: string;
}

interface BehaviorTrend {
    status: string;
    trends?: {
        [key: string]: {
            current: number;
            predicted: number;
            trend: string;
            slope: number;
        };
    };
}

interface AnomalyDetection {
    status: string;
    has_anomaly?: boolean;
    anomaly_score?: number;
    anomalies?: Array<{
        type: string;
        severity: string;
        description: string;
    }>;
}

const PredictiveInsights = ({ userId }: PredictiveInsightsProps) => {
    const [stressData, setStressData] = useState<StressAnalysis | null>(null);
    const [behaviorTrend, setBehaviorTrend] = useState<BehaviorTrend | null>(null);
    const [anomalyData, setAnomalyData] = useState<AnomalyDetection | null>(null);
    const [evolutionData, setEvolutionData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchInsights = async () => {
            try {
                // 예측 인사이트 API 호출
                const insightsRes = await fetch(config.getApiUrl(`/api/insights/${userId}`));
                if (insightsRes.ok) {
                    const insights = await insightsRes.json();
                    
                    if (insights.status === 'success') {
                        // 스트레스 분석
                        if (insights.stress_analysis) {
                            setStressData(insights.stress_analysis);
                        }
                        
                        // 이상 감지
                        if (insights.anomaly_detection) {
                            setAnomalyData(insights.anomaly_detection);
                        }
                        
                        // 행동 트렌드
                        if (insights.behavior_trend) {
                            setBehaviorTrend(insights.behavior_trend);
                        }
                    } else {
                        // 데이터 부족
                        setStressData({
                            status: 'insufficient_data',
                            stress_level: 0,
                            stress_category: 'low',
                            indicators: [],
                            recommendation: insights.message || '데이터가 부족합니다.'
                        });
                        setBehaviorTrend({
                            status: 'insufficient_data',
                            trends: {}
                        });
                        setAnomalyData({
                            status: 'insufficient_data',
                            has_anomaly: false,
                            anomaly_score: 0,
                            anomalies: []
                        });
                    }
                }

                // 진화 데이터 가져오기 (30일 예측용)
                const evolutionRes = await fetch(config.getApiUrl(`/api/evolution/${userId}`));
                if (evolutionRes.ok) {
                    const evolution = await evolutionRes.json();
                    setEvolutionData(evolution);
                }

                setLoading(false);
            } catch (error) {
                console.error('Failed to fetch predictive insights:', error);
                
                // 에러 상태 설정
                setStressData({
                    status: 'error',
                    stress_level: 0,
                    stress_category: 'unknown',
                    indicators: [],
                    recommendation: '데이터를 불러오는 중 오류가 발생했습니다.'
                });
                setBehaviorTrend({
                    status: 'error',
                    trends: {}
                });
                setAnomalyData({
                    status: 'error',
                    has_anomaly: false,
                    anomaly_score: 0,
                    anomalies: []
                });
                
                setLoading(false);
            }
        };

        if (userId) {
            fetchInsights();
        }
    }, [userId]);

    if (loading) {
        return (
            <div style={{ 
                padding: '2rem', 
                textAlign: 'center', 
                color: 'var(--text-muted)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '1rem'
            }}>
                <div style={{
                    width: '40px',
                    height: '40px',
                    border: '3px solid rgba(112, 0, 255, 0.3)',
                    borderTop: '3px solid #7000ff',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite'
                }}></div>
                <div>예측 인사이트를 분석 중...</div>
                <style>{`
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `}</style>
            </div>
        );
    }

    // 행동 트렌드 차트 데이터
    const trendChartData = behaviorTrend?.trends ? Object.entries(behaviorTrend.trends).map(([key, value]) => ({
        trait: key,
        current: value.current * 100,
        predicted: value.predicted * 100,
        change: (value.predicted - value.current) * 100
    })) : [];

    // 스트레스 레벨 색상
    const getStressColor = (level?: number) => {
        if (!level) return '#10b981';
        if (level < 0.3) return '#10b981'; // green
        if (level < 0.6) return '#f59e0b'; // yellow
        return '#ef4444'; // red
    };

    return (
        <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '1rem' }}>
                예측 인사이트 <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 400 }}>Predictive Insights</span>
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem' }}>
                {/* 스트레스 분석 */}
                <GlassCard style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                        <div style={{ 
                            padding: '0.75rem', 
                            background: `rgba(${stressData?.stress_level && stressData.stress_level > 0.6 ? '239, 68, 68' : stressData?.stress_level && stressData.stress_level > 0.3 ? '245, 158, 11' : '16, 185, 129'}, 0.1)`, 
                            borderRadius: '8px',
                            color: getStressColor(stressData?.stress_level)
                        }}>
                            <Heart size={20} />
                        </div>
                        <div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                                스트레스 레벨
                            </div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: getStressColor(stressData?.stress_level) }}>
                                {stressData?.stress_level ? (stressData.stress_level * 100).toFixed(0) : 0}%
                            </div>
                        </div>
                    </div>
                    <div style={{ 
                        fontSize: '0.85rem', 
                        color: 'var(--text-muted)',
                        padding: '0.75rem',
                        background: 'rgba(255, 255, 255, 0.03)',
                        borderRadius: '8px'
                    }}>
                        {stressData?.recommendation || '분석 중...'}
                    </div>
                    {stressData?.indicators && stressData.indicators.length > 0 && (
                        <div style={{ marginTop: '0.75rem', fontSize: '0.75rem', color: '#f59e0b' }}>
                            {stressData.indicators.map((ind, i) => (
                                <div key={i}>• {ind}</div>
                            ))}
                        </div>
                    )}
                </GlassCard>

                {/* 이상 감지 */}
                <GlassCard style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                        <div style={{ 
                            padding: '0.75rem', 
                            background: anomalyData?.has_anomaly ? 'rgba(239, 68, 68, 0.1)' : 'rgba(16, 185, 129, 0.1)', 
                            borderRadius: '8px',
                            color: anomalyData?.has_anomaly ? '#ef4444' : '#10b981'
                        }}>
                            <AlertTriangle size={20} />
                        </div>
                        <div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                                이상 감지
                            </div>
                            <div style={{ 
                                fontSize: '1.5rem', 
                                fontWeight: 700, 
                                color: anomalyData?.has_anomaly ? '#ef4444' : '#10b981'
                            }}>
                                {anomalyData?.has_anomaly ? '감지됨' : '정상'}
                            </div>
                        </div>
                    </div>
                    {anomalyData?.anomalies && anomalyData.anomalies.length > 0 && (
                        <div style={{ fontSize: '0.85rem', color: '#ef4444' }}>
                            {anomalyData.anomalies.map((anomaly, i) => (
                                <div key={i} style={{ marginTop: '0.5rem' }}>
                                    <strong>{anomaly.type}:</strong> {anomaly.description}
                                </div>
                            ))}
                        </div>
                    )}
                </GlassCard>

                {/* 행동 트렌드 요약 */}
                <GlassCard style={{ padding: '1.5rem' }}>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '1rem' }}>
                        다음 세션 예측
                    </div>
                    {behaviorTrend?.trends && Object.entries(behaviorTrend.trends).map(([trait, data]) => (
                        <div key={trait} style={{ 
                            display: 'flex', 
                            justifyContent: 'space-between', 
                            alignItems: 'center',
                            marginBottom: '0.75rem',
                            padding: '0.5rem',
                            background: 'rgba(255, 255, 255, 0.02)',
                            borderRadius: '6px'
                        }}>
                            <span style={{ fontSize: '0.85rem', textTransform: 'capitalize' }}>{trait}</span>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <span style={{ fontSize: '0.9rem', fontWeight: 600 }}>
                                    {(data.predicted * 100).toFixed(0)}%
                                </span>
                                {data.trend === 'increasing' ? (
                                    <TrendingUp size={16} color="#10b981" />
                                ) : data.trend === 'decreasing' ? (
                                    <TrendingDown size={16} color="#ef4444" />
                                ) : (
                                    <Activity size={16} color="#6b7280" />
                                )}
                            </div>
                        </div>
                    ))}
                </GlassCard>
            </div>

            {/* 행동 트렌드 차트 */}
            {trendChartData.length > 0 && (
                <GlassCard style={{ padding: '1.5rem', minHeight: '300px' }}>
                    <h4 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1.5rem' }}>
                        성격 가중치 트렌드 예측
                    </h4>
                    <ResponsiveContainer width="100%" height={250}>
                        <AreaChart data={trendChartData}>
                            <defs>
                                <linearGradient id="currentGradient" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#7000ff" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#7000ff" stopOpacity={0} />
                                </linearGradient>
                                <linearGradient id="predictedGradient" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#00f2ff" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#00f2ff" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="trait" stroke="rgba(255,255,255,0.3)" />
                            <YAxis stroke="rgba(255,255,255,0.3)" />
                            <Tooltip 
                                contentStyle={{ 
                                    background: 'rgba(15, 15, 20, 0.95)', 
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    borderRadius: '8px'
                                }}
                            />
                            <Area 
                                type="monotone" 
                                dataKey="current" 
                                stroke="#7000ff" 
                                fill="url(#currentGradient)" 
                                name="현재"
                            />
                            <Area 
                                type="monotone" 
                                dataKey="predicted" 
                                stroke="#00f2ff" 
                                fill="url(#predictedGradient)" 
                                name="예측"
                                strokeDasharray="5 5"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </GlassCard>
            )}

            {/* 진화 예측 */}
            {evolutionData?.prediction && evolutionData.prediction.status === 'predicted' && (
                <GlassCard style={{ padding: '1.5rem' }}>
                    <h4 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1.5rem' }}>
                        30일 후 성격 진화 예측
                    </h4>
                    <ResponsiveContainer width="100%" height={300}>
                        <RadarChart data={Object.entries(evolutionData.prediction.predictions).map(([key, value]: [string, any]) => ({
                            trait: key,
                            current: value.current * 100,
                            predicted: value.predicted_30days * 100,
                            fullMark: 100
                        }))}>
                            <PolarGrid />
                            <PolarAngleAxis dataKey="trait" stroke="rgba(255,255,255,0.5)" />
                            <PolarRadiusAxis angle={90} domain={[0, 100]} stroke="rgba(255,255,255,0.3)" />
                            <Radar 
                                name="현재" 
                                dataKey="current" 
                                stroke="#7000ff" 
                                fill="#7000ff" 
                                fillOpacity={0.3}
                            />
                            <Radar 
                                name="30일 후 예측" 
                                dataKey="predicted" 
                                stroke="#00f2ff" 
                                fill="#00f2ff" 
                                fillOpacity={0.2}
                                strokeDasharray="5 5"
                            />
                            <Tooltip 
                                contentStyle={{ 
                                    background: 'rgba(15, 15, 20, 0.95)', 
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    borderRadius: '8px'
                                }}
                            />
                        </RadarChart>
                    </ResponsiveContainer>
                </GlassCard>
            )}
        </div>
    );
};

export default PredictiveInsights;
