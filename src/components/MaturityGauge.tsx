import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface MaturityGaugeProps {
    level: number;
    syncScore: number;
    isLevelUp?: boolean;
}

const LEVEL_NAMES = ["Echo", "Reflection", "Synthesis"];
const LEVEL_COLORS = ["#00f2ff", "#7000ff", "#ff00d4"];

export const MaturityGauge: React.FC<MaturityGaugeProps> = ({ level, syncScore, isLevelUp }) => {
    const [displaySync, setDisplaySync] = useState(0);

    useEffect(() => {
        // Animate sync score
        const timer = setTimeout(() => {
            setDisplaySync(syncScore * 100);
        }, 500);
        return () => clearTimeout(timer);
    }, [syncScore]);

    return (
        <div className="maturity-gauge-container p-6 bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl">
            <div className="flex justify-between items-end mb-4">
                <div>
                    <span className="text-xs uppercase tracking-[0.2em] text-white/50 block mb-1">Maturity Status</span>
                    <h3 className="text-2xl font-bold bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
                        Tier {level}: {LEVEL_NAMES[level - 1]}
                    </h3>
                </div>
                <div className="text-right">
                    <span className="text-4xl font-black font-mono" style={{ color: LEVEL_COLORS[level - 1] }}>
                        {displaySync.toFixed(1)}%
                    </span>
                    <span className="text-xs block text-white/30">Synchronization</span>
                </div>
            </div>

            {/* Progress Bar Container */}
            <div className="relative h-3 w-full bg-white/5 rounded-full overflow-hidden border border-white/5">
                <motion.div
                    className="absolute top-0 left-0 h-full rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${displaySync}%` }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                    style={{
                        background: `linear-gradient(90deg, ${LEVEL_COLORS[level - 1]}88, ${LEVEL_COLORS[level - 1]})`,
                        boxShadow: `0 0 20px ${LEVEL_COLORS[level - 1]}44`
                    }}
                />
            </div>

            {/* Level Indicators */}
            <div className="flex justify-between mt-3 px-1">
                {[1, 2, 3].map((l) => (
                    <div key={l} className="flex flex-col items-center">
                        <div
                            className={`w-2 h-2 rounded-full mb-1 transition-all duration-500 ${l <= level ? 'opacity-100 scale-125' : 'opacity-20'}`}
                            style={{ backgroundColor: LEVEL_COLORS[l - 1] }}
                        />
                        <span className={`text-[10px] uppercase font-bold tracking-tighter ${l <= level ? 'text-white/80' : 'text-white/20'}`}>
                            L{l}
                        </span>
                    </div>
                ))}
            </div>

            <AnimatePresence>
                {isLevelUp && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className="mt-4 p-2 bg-white/10 border border-white/20 rounded-lg text-center"
                    >
                        <span className="text-xs font-bold text-[#00f2ff] animate-pulse">
                            ▲ DIGITAL TWIN EVOLVED TO PHASE {level}
                        </span>
                    </motion.div>
                )}
            </AnimatePresence>

            <p className="mt-4 text-[10px] text-white/40 leading-relaxed italic border-t border-white/5 pt-3">
                * Maturity is calculated via spintronic entropy and behavioral coherence.
                Higher tiers unlock deeper physical resonance with the MuMax3 core.
            </p>
        </div>
    );
};
