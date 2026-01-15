import React, { useState, useEffect } from 'react';
import { Shield, Database, Trash2, Download, Check, X } from 'lucide-react';

interface PrivacyConsentProps {
    userId: string;
    onConsent: (granted: boolean) => void;
    onClose: () => void;
}

interface ConsentState {
    behavioralTracking: boolean;
    profileStorage: boolean;
    continuousLearning: boolean;
}

import config from '../utils/config';

const PrivacyConsent = ({ userId, onConsent, onClose }: PrivacyConsentProps) => {
    const [consent, setConsent] = useState<ConsentState>({
        behavioralTracking: true,
        profileStorage: true,
        continuousLearning: true,
    });
    const [showDataManagement, setShowDataManagement] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [isExporting, setIsExporting] = useState(false);

    const handleConsentChange = (key: keyof ConsentState) => {
        setConsent(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleSubmit = async () => {
        try {
            // Save consent record to backend
            await fetch(config.getApiUrl(`/api/user/${userId}/consent`), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    consent_record: consent,
                    timestamp: new Date().toISOString(),
                }),
            });

            // Save to localStorage for quick access
            localStorage.setItem(`privacy_consent_${userId}`, JSON.stringify({
                ...consent,
                timestamp: new Date().toISOString(),
            }));

            onConsent(consent.behavioralTracking && consent.profileStorage);
        } catch (error) {
            console.error('Failed to save consent:', error);
            onConsent(false);
        }
    };

    const handleDeleteData = async () => {
        if (!confirm('정말로 모든 데이터를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
            return;
        }

        setIsDeleting(true);
        try {
            const response = await fetch(config.getApiUrl(`/api/user/${userId}`), {
                method: 'DELETE',
            });

            if (response.ok) {
                localStorage.removeItem(`privacy_consent_${userId}`);
                alert('모든 데이터가 성공적으로 삭제되었습니다.');
                onClose();
            } else {
                throw new Error('Delete failed');
            }
        } catch (error) {
            console.error('Failed to delete data:', error);
            alert('데이터 삭제에 실패했습니다.');
        } finally {
            setIsDeleting(false);
        }
    };

    const handleExportData = async () => {
        setIsExporting(true);
        try {
            const response = await fetch(config.getApiUrl(`/api/user/${userId}/export`));
            const data = await response.json();

            // Download as JSON file
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `my_data_${userId}_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Failed to export data:', error);
            alert('데이터 내보내기에 실패했습니다.');
        } finally {
            setIsExporting(false);
        }
    };

    return (
        <div className="privacy-overlay fade-in">
            <div className="privacy-content glass-panel">
                <div className="privacy-header">
                    <Shield size={32} className="neon-cyan" />
                    <h2>개인정보 보호 및 동의</h2>
                </div>

                {!showDataManagement ? (
                    <>
                        <div className="privacy-intro">
                            <p>
                                Cube는 귀하의 상호작용 패턴을 분석하여 개인화된 디지털 트윈을
                                생성합니다. 수집되는 데이터와 사용 방법을 확인하시고 동의해주세요.
                            </p>
                        </div>

                        <div className="consent-items">
                            <ConsentItem
                                icon={<Database size={20} />}
                                title="행동 데이터 수집"
                                description="마우스 움직임, 결정 시간, 수정 패턴 등의 상호작용 데이터를 수집합니다."
                                checked={consent.behavioralTracking}
                                onChange={() => handleConsentChange('behavioralTracking')}
                                required
                            />

                            <ConsentItem
                                icon={<Shield size={20} />}
                                title="프로필 저장"
                                description="분석된 성격 프로필을 서버에 저장하여 세션 간 연속성을 유지합니다."
                                checked={consent.profileStorage}
                                onChange={() => handleConsentChange('profileStorage')}
                                required
                            />

                            <ConsentItem
                                icon={<Database size={20} />}
                                title="지속적 학습"
                                description="여러 세션에 걸쳐 프로필을 개선하여 더 정확한 개인화를 제공합니다."
                                checked={consent.continuousLearning}
                                onChange={() => handleConsentChange('continuousLearning')}
                            />
                        </div>

                        <div className="privacy-rights">
                            <h4>귀하의 권리</h4>
                            <ul>
                                <li>언제든지 동의를 철회할 수 있습니다</li>
                                <li>저장된 데이터를 내보내기할 수 있습니다</li>
                                <li>모든 데이터 삭제를 요청할 수 있습니다</li>
                            </ul>
                            <button
                                className="btn btn-secondary"
                                onClick={() => setShowDataManagement(true)}
                            >
                                데이터 관리
                            </button>
                        </div>

                        <div className="privacy-actions">
                            <button
                                className="btn btn-secondary"
                                onClick={onClose}
                            >
                                거부
                            </button>
                            <button
                                className="btn btn-primary glow-effect"
                                onClick={handleSubmit}
                                disabled={!consent.behavioralTracking || !consent.profileStorage}
                            >
                                동의하고 시작하기
                            </button>
                        </div>
                    </>
                ) : (
                    <>
                        <div className="data-management">
                            <h3>내 데이터 관리</h3>

                            <div className="data-action-card">
                                <div className="data-action-info">
                                    <Download size={24} />
                                    <div>
                                        <h4>데이터 내보내기</h4>
                                        <p>저장된 모든 데이터를 JSON 형식으로 다운로드합니다.</p>
                                    </div>
                                </div>
                                <button
                                    className="btn btn-secondary"
                                    onClick={handleExportData}
                                    disabled={isExporting}
                                >
                                    {isExporting ? '내보내는 중...' : '내보내기'}
                                </button>
                            </div>

                            <div className="data-action-card danger">
                                <div className="data-action-info">
                                    <Trash2 size={24} />
                                    <div>
                                        <h4>데이터 삭제</h4>
                                        <p>모든 행동 데이터와 프로필을 영구적으로 삭제합니다. 이 작업은 되돌릴 수 없습니다.</p>
                                    </div>
                                </div>
                                <button
                                    className="btn btn-danger"
                                    onClick={handleDeleteData}
                                    disabled={isDeleting}
                                >
                                    {isDeleting ? '삭제 중...' : '모두 삭제'}
                                </button>
                            </div>
                        </div>

                        <button
                            className="btn btn-secondary"
                            onClick={() => setShowDataManagement(false)}
                            style={{ marginTop: '20px', width: '100%' }}
                        >
                            ← 돌아가기
                        </button>
                    </>
                )}
            </div>

            <style dangerouslySetInnerHTML={{
                __html: `
                .privacy-overlay {
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
                .privacy-content {
                    max-width: 550px;
                    max-height: 90vh;
                    overflow-y: auto;
                    padding: 40px;
                    border: 1px solid rgba(0, 255, 255, 0.2);
                    box-shadow: 0 0 60px rgba(0, 255, 255, 0.1);
                }
                .privacy-header {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    margin-bottom: 25px;
                }
                .privacy-header h2 {
                    font-size: 1.5rem;
                    margin: 0;
                }
                .privacy-intro {
                    color: rgba(255, 255, 255, 0.7);
                    margin-bottom: 25px;
                    line-height: 1.6;
                }
                .consent-items {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    margin-bottom: 25px;
                }
                .consent-item {
                    display: flex;
                    align-items: flex-start;
                    gap: 15px;
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.03);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    transition: all 0.3s ease;
                }
                .consent-item:hover {
                    border-color: rgba(0, 255, 255, 0.2);
                }
                .consent-item.checked {
                    border-color: rgba(0, 255, 255, 0.3);
                    background: rgba(0, 255, 255, 0.05);
                }
                .consent-icon {
                    color: var(--neon-cyan);
                    flex-shrink: 0;
                    margin-top: 2px;
                }
                .consent-text {
                    flex: 1;
                }
                .consent-text h4 {
                    margin: 0 0 5px 0;
                    font-size: 0.95rem;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .consent-text p {
                    margin: 0;
                    color: rgba(255, 255, 255, 0.6);
                    font-size: 0.85rem;
                    line-height: 1.5;
                }
                .required-badge {
                    font-size: 0.7rem;
                    padding: 2px 6px;
                    background: rgba(255, 100, 100, 0.2);
                    color: #ff6b6b;
                    border-radius: 4px;
                }
                .consent-toggle {
                    width: 44px;
                    height: 24px;
                    border-radius: 12px;
                    background: rgba(255, 255, 255, 0.1);
                    border: none;
                    cursor: pointer;
                    position: relative;
                    transition: all 0.3s ease;
                    flex-shrink: 0;
                }
                .consent-toggle.active {
                    background: var(--neon-cyan);
                }
                .consent-toggle::after {
                    content: '';
                    position: absolute;
                    width: 18px;
                    height: 18px;
                    border-radius: 50%;
                    background: white;
                    top: 3px;
                    left: 3px;
                    transition: all 0.3s ease;
                }
                .consent-toggle.active::after {
                    left: 23px;
                }
                .privacy-rights {
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.02);
                    border-radius: 12px;
                    margin-bottom: 25px;
                }
                .privacy-rights h4 {
                    margin: 0 0 10px 0;
                    color: var(--neon-cyan);
                }
                .privacy-rights ul {
                    margin: 0 0 15px 0;
                    padding-left: 20px;
                    color: rgba(255, 255, 255, 0.7);
                }
                .privacy-rights li {
                    margin: 5px 0;
                }
                .privacy-actions {
                    display: flex;
                    gap: 15px;
                }
                .privacy-actions .btn {
                    flex: 1;
                    padding: 12px;
                }
                .data-management h3 {
                    margin: 0 0 20px 0;
                }
                .data-action-card {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.03);
                    border-radius: 12px;
                    margin-bottom: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                }
                .data-action-card.danger {
                    border-color: rgba(255, 100, 100, 0.2);
                }
                .data-action-info {
                    display: flex;
                    align-items: flex-start;
                    gap: 15px;
                }
                .data-action-info h4 {
                    margin: 0 0 5px 0;
                }
                .data-action-info p {
                    margin: 0;
                    color: rgba(255, 255, 255, 0.6);
                    font-size: 0.85rem;
                }
                .btn-danger {
                    background: rgba(255, 100, 100, 0.2);
                    color: #ff6b6b;
                    border: 1px solid rgba(255, 100, 100, 0.3);
                }
                .btn-danger:hover {
                    background: rgba(255, 100, 100, 0.3);
                }
            `}} />
        </div>
    );
};

interface ConsentItemProps {
    icon: React.ReactNode;
    title: string;
    description: string;
    checked: boolean;
    onChange: () => void;
    required?: boolean;
}

const ConsentItem = ({ icon, title, description, checked, onChange, required }: ConsentItemProps) => (
    <div className={`consent-item ${checked ? 'checked' : ''}`}>
        <div className="consent-icon">{icon}</div>
        <div className="consent-text">
            <h4>
                {title}
                {required && <span className="required-badge">필수</span>}
            </h4>
            <p>{description}</p>
        </div>
        <button
            className={`consent-toggle ${checked ? 'active' : ''}`}
            onClick={onChange}
            disabled={required && checked}
        />
    </div>
);

export default PrivacyConsent;
