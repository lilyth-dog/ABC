import { ReactNode, CSSProperties } from 'react';

interface GlassCardProps {
    children: ReactNode;
    className?: string;
    animate?: boolean;
    style?: CSSProperties;
}

const GlassCard = ({ children, className = '', animate = false, style = {} }: GlassCardProps) => {
    return (
        <div
            className={`glass-card ${animate ? 'animate-float' : ''} ${className}`}
            style={style}
        >
            {children}
        </div>
    );
};

export default GlassCard;
