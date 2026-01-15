import React from 'react';

interface Memory {
    date: string;
    dominantTrait: string;
    aesthetic: string;
    rank: string;
}

interface MemoryVaultProps {
    memories: Memory[];
    onClose: () => void;
}

const MemoryVault = ({ memories, onClose }: MemoryVaultProps) => {
    return (
        <div className="vault-overlay fade-in">
            <div className="vault-content glass-panel">
                <div className="vault-header">
                    <h2 className="neon-cyan">The Memory Vault</h2>
                    <p style={{ color: 'var(--text-muted)' }}>Chronicles of your Soul-Synchronization</p>
                </div>

                <div className="memories-grid">
                    {memories.length === 0 ? (
                        <div style={{ textAlign: 'center', padding: '40px', color: 'rgba(255,255,255,0.3)' }}>
                            <div style={{ fontSize: '3rem', marginBottom: '10px' }}>🏺</div>
                            <p>No memories archived yet. Complete a Heart-Link to save your first journey.</p>
                        </div>
                    ) : (
                        memories.map((memory, index) => (
                            <div key={index} className="memory-card glass-panel fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                                <div className="memory-date">{new Date(memory.date).toLocaleDateString()}</div>
                                <div className="memory-title">{memory.dominantTrait} Soul</div>
                                <div className="memory-aesthetic">{memory.aesthetic} Aura</div>
                                <div className="memory-rank badge active">{memory.rank}</div>
                            </div>
                        ))
                    )}
                </div>

                <button className="btn btn-secondary glass-effect" onClick={onClose} style={{ marginTop: '30px', width: '100%' }}>
                    CLOSE THE VAULT
                </button>
            </div>

            <style dangerouslySetInnerHTML={{
                __html: `
                .vault-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background: rgba(10, 5, 20, 0.95);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 3000;
                    backdrop-filter: blur(20px);
                }
                .vault-content {
                    width: 90%;
                    max-width: 800px;
                    max-height: 80vh;
                    padding: 40px;
                    overflow-y: auto;
                }
                .vault-header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .memories-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 20px;
                }
                .memory-card {
                    padding: 20px;
                    border: 1px solid rgba(0, 212, 255, 0.2);
                    transition: all 0.3s ease;
                    cursor: pointer;
                }
                .memory-card:hover {
                    border-color: var(--neon-cyan);
                    box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
                    transform: translateY(-5px);
                }
                .memory-date {
                    font-size: 0.7rem;
                    color: var(--text-muted);
                    margin-bottom: 5px;
                }
                .memory-title {
                    font-weight: 800;
                    color: white;
                    margin-bottom: 5px;
                }
                .memory-aesthetic {
                    font-size: 0.8rem;
                    color: var(--neon-magenta);
                    margin-bottom: 10px;
                }
                .memory-rank {
                    font-size: 0.6rem;
                    padding: 2px 8px;
                }
            `}} />
        </div>
    );
};

export default MemoryVault;
