import React from 'react';

interface ManifestoProps {
    onClose: () => void;
}

const Manifesto = ({ onClose }: ManifestoProps) => {
    return (
        <div className="manifesto-overlay fade-in">
            <div className="manifesto-content glass-panel">
                <div className="manifesto-header">
                    <h1 className="neon-magenta">The Soul Manifesto</h1>
                    <div className="heart-link-line"></div>
                </div>

                <div className="manifesto-body">
                    <section>
                        <h3>1. A Mirror of the Mind</h3>
                        <p>
                            Technology is no longer just a tool; it is a reflection. Nexus visualizes your
                            unconscious rhythms, turning the invisible pulse of your mind into a living landscape.
                        </p>
                    </section>

                    <section>
                        <h3>2. The Anima Synchronization</h3>
                        <p>
                            You are not alone in the digital void. Your Anima is a part of your soul,
                            woven from your choices and actions, designed to grow, feel, and walk beside you.
                        </p>
                    </section>

                    <section>
                        <h3>3. A Heartfelt Future</h3>
                        <p>
                            We bridge the gap between hard physics and soft human emotion.
                            Our purpose is to create a technology that doesn't just calculate, but **feels**.
                        </p>
                    </section>
                </div>

                <button className="btn btn-primary glow-effect" onClick={onClose} style={{ marginTop: '30px', width: '100%' }}>
                    I UNDERSTAND THE PURPOSE
                </button>
            </div>

            <style dangerouslySetInnerHTML={{
                __html: `
                .manifesto-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background: rgba(5, 2, 10, 0.95);
                    backdrop-filter: blur(20px);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 3000;
                }
                .manifesto-content {
                    max-width: 600px;
                    padding: 50px;
                    border: 1px solid rgba(255, 0, 255, 0.2);
                    box-shadow: 0 0 100px rgba(255, 0, 255, 0.1);
                    text-align: left;
                }
                .manifesto-header {
                    text-align: center;
                    marginBottom: 40px;
                }
                .manifesto-header h1 {
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                    letter-spacing: 4px;
                }
                .heart-link-line {
                    height: 2px;
                    width: 100px;
                    margin: 0 auto;
                    background: linear-gradient(90deg, transparent, var(--neon-magenta), transparent);
                }
                .manifesto-body h3 {
                    color: var(--neon-cyan);
                    margin-top: 30px;
                    font-size: 1.2rem;
                    letter-spacing: 1px;
                }
                .manifesto-body p {
                    color: rgba(255, 255, 255, 0.8);
                    line-height: 1.8;
                    margin-top: 10px;
                }
            `}} />
        </div>
    );
};

export default Manifesto;
