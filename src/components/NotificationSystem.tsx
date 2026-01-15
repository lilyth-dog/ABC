/**
 * 실시간 알림 시스템
 * 스트레스 감지, 레벨업, 이상 행동 등에 대한 알림 제공
 */
import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, CheckCircle, TrendingUp, Heart, Bell } from 'lucide-react';
import { config } from '../utils/config';

export type NotificationType = 'stress' | 'level_up' | 'anomaly' | 'trend' | 'info';

export interface Notification {
    id: string;
    type: NotificationType;
    title: string;
    message: string;
    timestamp: Date;
    severity?: 'low' | 'medium' | 'high';
    actionUrl?: string;
}

interface NotificationSystemProps {
    userId?: string;
    onNotificationClick?: (notification: Notification) => void;
}

const NotificationSystem = ({ userId, onNotificationClick }: NotificationSystemProps) => {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [isExpanded, setIsExpanded] = useState(false);

    // 알림 추가 함수
    const addNotification = useCallback((notification: Omit<Notification, 'id' | 'timestamp'>) => {
        const newNotification: Notification = {
            ...notification,
            id: `notif-${Date.now()}-${Math.random()}`,
            timestamp: new Date()
        };
        setNotifications(prev => [newNotification, ...prev].slice(0, 10)); // 최대 10개

        // 자동 제거 (5초 후)
        setTimeout(() => {
            setNotifications(prev => prev.filter(n => n.id !== newNotification.id));
        }, 5000);
    }, []);

    // 스트레스 알림 감지
    useEffect(() => {
        if (!userId) return;

        const checkStress = async () => {
            try {
                const res = await fetch(config.getApiUrl(`/api/insights/${userId}`));
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                
                const data = await res.json();
                if (data.status === 'success' && data.stress_analysis) {
                    const stressLevel = data.stress_analysis.stress_level || 0;
                    
                    // 높은 스트레스 감지 시 알림 (중복 방지)
                    if (stressLevel > 0.6 && (window as any).addNotification) {
                        // 이미 같은 알림이 있는지 확인
                        const existingStressNotif = notifications.find(
                            n => n.type === 'stress' && n.severity === (stressLevel > 0.8 ? 'high' : 'medium')
                        );
                        
                        if (!existingStressNotif) {
                            (window as any).addNotification({
                                type: 'stress',
                                title: '높은 스트레스 감지',
                                message: data.stress_analysis.recommendation || '충분한 휴식이 필요합니다.',
                                severity: stressLevel > 0.8 ? 'high' : 'medium'
                            });
                        }
                    }
                    
                    // 이상 행동 감지 시 알림 (중복 방지)
                    if (data.anomaly_detection?.has_anomaly && (window as any).addNotification) {
                        const existingAnomalyNotif = notifications.find(n => n.type === 'anomaly');
                        if (!existingAnomalyNotif) {
                            (window as any).addNotification({
                                type: 'anomaly',
                                title: '이상 행동 감지',
                                message: data.anomaly_detection.recommendation || '이상 행동 패턴이 감지되었습니다.',
                                severity: 'high'
                            });
                        }
                    }
                }
            } catch (error) {
                console.error('Failed to check stress:', error);
                // 에러 발생 시에도 앱이 계속 작동하도록 함
            }
        };

        const interval = setInterval(checkStress, 60000); // 1분마다 체크
        return () => clearInterval(interval);
    }, [userId]);

    // 알림 아이콘
    const getNotificationIcon = (type: NotificationType) => {
        switch (type) {
            case 'stress':
                return <Heart size={20} />;
            case 'level_up':
                return <TrendingUp size={20} />;
            case 'anomaly':
                return <AlertTriangle size={20} />;
            case 'trend':
                return <TrendingUp size={20} />;
            default:
                return <Bell size={20} />;
        }
    };

    // 알림 색상
    const getNotificationColor = (type: NotificationType, severity?: string) => {
        if (type === 'stress') {
            if (severity === 'high') return '#ef4444';
            if (severity === 'medium') return '#f59e0b';
            return '#10b981';
        }
        if (type === 'level_up') return '#7000ff';
        if (type === 'anomaly') return '#ef4444';
        if (type === 'trend') return '#00f2ff';
        return '#6b7280';
    };

    // 전역 알림 함수 (다른 컴포넌트에서 사용 가능)
    useEffect(() => {
        (window as any).addNotification = addNotification;
        return () => {
            delete (window as any).addNotification;
        };
    }, [addNotification]);

    return (
        <>
            {/* 알림 버튼 */}
            <div style={{ position: 'fixed', top: '20px', right: '20px', zIndex: 10000 }}>
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    style={{
                        position: 'relative',
                        padding: '0.75rem',
                        background: 'rgba(15, 15, 20, 0.9)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: '12px',
                        color: 'white',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        backdropFilter: 'blur(10px)'
                    }}
                >
                    <Bell size={20} />
                    {notifications.length > 0 && (
                        <span style={{
                            position: 'absolute',
                            top: '-4px',
                            right: '-4px',
                            background: '#ef4444',
                            color: 'white',
                            borderRadius: '50%',
                            width: '20px',
                            height: '20px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '0.7rem',
                            fontWeight: 700
                        }}>
                            {notifications.length}
                        </span>
                    )}
                </button>

                {/* 알림 목록 */}
                <AnimatePresence>
                    {isExpanded && (
                        <motion.div
                            initial={{ opacity: 0, y: -10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            style={{
                                position: 'absolute',
                                top: '60px',
                                right: 0,
                                width: '350px',
                                maxHeight: '500px',
                                overflowY: 'auto',
                                background: 'rgba(15, 15, 20, 0.95)',
                                border: '1px solid rgba(255, 255, 255, 0.1)',
                                borderRadius: '12px',
                                padding: '1rem',
                                backdropFilter: 'blur(20px)',
                                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.5)'
                            }}
                        >
                            {notifications.length === 0 ? (
                                <div style={{ 
                                    padding: '2rem', 
                                    textAlign: 'center', 
                                    color: 'var(--text-muted)',
                                    fontSize: '0.9rem'
                                }}>
                                    알림이 없습니다
                                </div>
                            ) : (
                                notifications.map((notification) => (
                                    <motion.div
                                        key={notification.id}
                                        initial={{ opacity: 0, x: 20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        exit={{ opacity: 0, x: -20 }}
                                        onClick={() => onNotificationClick?.(notification)}
                                        style={{
                                            padding: '1rem',
                                            marginBottom: '0.75rem',
                                            background: 'rgba(255, 255, 255, 0.03)',
                                            border: `1px solid ${getNotificationColor(notification.type, notification.severity)}33`,
                                            borderRadius: '8px',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s'
                                        }}
                                        whileHover={{ background: 'rgba(255, 255, 255, 0.05)' }}
                                    >
                                        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                                            <div style={{
                                                color: getNotificationColor(notification.type, notification.severity),
                                                flexShrink: 0
                                            }}>
                                                {getNotificationIcon(notification.type)}
                                            </div>
                                            <div style={{ flex: 1 }}>
                                                <div style={{ 
                                                    fontSize: '0.9rem', 
                                                    fontWeight: 600,
                                                    marginBottom: '0.25rem'
                                                }}>
                                                    {notification.title}
                                                </div>
                                                <div style={{ 
                                                    fontSize: '0.8rem', 
                                                    color: 'var(--text-muted)',
                                                    lineHeight: 1.4
                                                }}>
                                                    {notification.message}
                                                </div>
                                                <div style={{ 
                                                    fontSize: '0.7rem', 
                                                    color: 'var(--text-muted)',
                                                    marginTop: '0.5rem',
                                                    opacity: 0.7
                                                }}>
                                                    {notification.timestamp.toLocaleTimeString()}
                                                </div>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))
                            )}
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* 토스트 알림 (화면 하단) */}
            <div style={{
                position: 'fixed',
                bottom: '20px',
                right: '20px',
                zIndex: 10001,
                display: 'flex',
                flexDirection: 'column',
                gap: '0.75rem',
                alignItems: 'flex-end'
            }}>
                <AnimatePresence>
                    {notifications.slice(0, 3).map((notification) => (
                        <motion.div
                            key={notification.id}
                            initial={{ opacity: 0, y: 20, x: 20 }}
                            animate={{ opacity: 1, y: 0, x: 0 }}
                            exit={{ opacity: 0, y: 20, x: 20 }}
                            style={{
                                padding: '1rem 1.25rem',
                                background: 'rgba(15, 15, 20, 0.95)',
                                border: `1px solid ${getNotificationColor(notification.type, notification.severity)}`,
                                borderRadius: '12px',
                                minWidth: '300px',
                                backdropFilter: 'blur(20px)',
                                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.5)',
                                cursor: 'pointer'
                            }}
                            onClick={() => onNotificationClick?.(notification)}
                        >
                            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                                <div style={{ color: getNotificationColor(notification.type, notification.severity) }}>
                                    {getNotificationIcon(notification.type)}
                                </div>
                                <div style={{ flex: 1 }}>
                                    <div style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: '0.25rem' }}>
                                        {notification.title}
                                    </div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                                        {notification.message}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </>
    );
};

// 전역 알림 함수 타입
declare global {
    interface Window {
        addNotification?: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
    }
}

export default NotificationSystem;
