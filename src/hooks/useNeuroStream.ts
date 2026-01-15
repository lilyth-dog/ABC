import { useState, useEffect, useCallback, useRef } from 'react';
import config from '../utils/config';

interface NeuroStreamData {
    sim_params?: {
        alpha?: number;
        beta?: number;
        theta?: number;
    };
    fluidity_index?: number;
    current_action?: string;
    behavioral_traits?: {
        analytical: boolean;
        stable: boolean;
        drive: number;
        resonance: number;
    };
    aesthetics?: string;
    world_params?: {
        fog_color: string;
        glow: number;
    };
}

interface UseNeuroStreamReturn {
    data: NeuroStreamData | null;
    isConnected: boolean;
    error: string | null;
    connect: () => void;
    disconnect: () => void;
    send: (params: Record<string, unknown>) => void;
    sendEEG: (theta: number, beta: number) => void;
    sendAction: (action: string) => void;
}

export const useNeuroStream = (
    endpoint = '/ws/simulation',
    autoConnect = true
): UseNeuroStreamReturn => {
    const [data, setData] = useState<NeuroStreamData | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

    const connect = useCallback(() => {
        if (wsRef.current?.readyState === WebSocket.OPEN) return;

        try {
            const ws = new WebSocket(config.getWsUrl(endpoint));
            wsRef.current = ws;

            ws.onopen = () => {
                console.log('[NeuroStream] Connected to', endpoint);
                setIsConnected(true);
                setError(null);
            };

            ws.onmessage = (event) => {
                try {
                    const parsed = JSON.parse(event.data);
                    setData(parsed);
                } catch (e) {
                    console.error('[NeuroStream] Parse error:', e);
                }
            };

            ws.onerror = () => {
                console.error('[NeuroStream] Error');
                setError('WebSocket connection error');
            };

            ws.onclose = () => {
                console.log('[NeuroStream] Disconnected');
                setIsConnected(false);

                reconnectTimeoutRef.current = setTimeout(() => {
                    console.log('[NeuroStream] Attempting reconnect...');
                    connect();
                }, 3000);
            };

        } catch (err) {
            console.error('[NeuroStream] Connection failed:', err);
            setError((err as Error).message);
        }
    }, [endpoint]);

    const disconnect = useCallback(() => {
        if (reconnectTimeoutRef.current) {
            clearTimeout(reconnectTimeoutRef.current);
        }
        if (wsRef.current) {
            wsRef.current.close();
            wsRef.current = null;
        }
        setIsConnected(false);
    }, []);

    const send = useCallback((params: Record<string, unknown>) => {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(params));
        } else {
            console.warn('[NeuroStream] Cannot send: not connected');
        }
    }, []);

    const sendEEG = useCallback((theta: number, beta: number) => {
        send({ theta, beta });
    }, [send]);

    const sendAction = useCallback((action: string) => {
        send({ action });
    }, [send]);

    useEffect(() => {
        if (autoConnect) {
            connect();
        }
        return () => disconnect();
    }, [autoConnect, connect, disconnect]);

    return {
        data,
        isConnected,
        error,
        connect,
        disconnect,
        send,
        sendEEG,
        sendAction,
    };
};

export default useNeuroStream;
