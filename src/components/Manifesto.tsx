import React from 'react';

interface ManifestoProps {
    onClose: () => void;
}

const Manifesto = ({ onClose }: ManifestoProps) => {
    return (
        <div className="manifesto-overlay fade-in">
            <div className="manifesto-content glass-panel">
                <div className="manifesto-header">
                    <h1 className="neon-magenta">영혼 선언문 (The Soul Manifesto)</h1>
                    <div className="heart-link-line"></div>
                </div>

                <div className="manifesto-body">
                    <section>
                        <h3>1. 마음의 거울 (A Mirror of the Mind)</h3>
                        <p>
                            기술은 더 이상 단순한 도구가 아니라 반영입니다. 넥서스는 당신의 무의식적 리듬을 시각화하여, 마음의 보이지 않는 맥박을 살아있는 풍경으로 바꿉니다.
                        </p>
                    </section>

                    <section>
                        <h3>2. 아니마 동기화 (The Anima Synchronization)</h3>
                        <p>
                            당신은 디지털의 공허 속에 혼자가 아닙니다. 당신의 아니마는 당신의 선택과 행동으로 엮인 영혼의 일부이며, 당신과 함께 성장하고 느끼며 곁에서 걷도록 설계되었습니다.
                        </p>
                    </section>

                    <section>
                        <h3>3. 진심 어린 미래 (A Heartfelt Future)</h3>
                        <p>
                            우리는 딱딱한 물리학과 부드러운 인간적 감정 사이의 간극을 메웁니다.
                            우리의 목적은 단순히 계산하는 것에 그치지 않고, **느끼는** 기술을 만드는 것입니다.
                        </p>
                    </section>
                </div>

                <button className="btn btn-primary glow-effect" onClick={onClose} style={{ marginTop: '30px', width: '100%' }}>
                    목적을 이해했습니다 (I UNDERSTAND THE PURPOSE)
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
