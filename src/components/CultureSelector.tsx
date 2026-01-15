import { useState } from 'react';
import { Globe, ChevronDown, Check } from 'lucide-react';

export interface CulturalContext {
    id: string;
    name: string;
    flag: string;
    description: string;
}

const CULTURAL_CONTEXTS: CulturalContext[] = [
    {
        id: 'default',
        name: 'Global Default',
        flag: '🌐',
        description: 'No cultural adjustments applied'
    },
    {
        id: 'east_asian',
        name: '동아시아',
        flag: '🇰🇷',
        description: '신중함과 조화를 중시하는 문화권'
    },
    {
        id: 'western',
        name: 'Western',
        flag: '🇺🇸',
        description: 'Individual decision-making focused'
    },
    {
        id: 'latin_american',
        name: 'Latin American',
        flag: '🇲🇽',
        description: 'Relationship-oriented culture'
    },
    {
        id: 'middle_eastern',
        name: 'Middle Eastern',
        flag: '🇸🇦',
        description: 'Collectivist with deliberation emphasis'
    }
];

interface CultureSelectorProps {
    selectedCulture: string;
    onCultureChange: (cultureId: string) => void;
    compact?: boolean;
}

const CultureSelector = ({
    selectedCulture,
    onCultureChange,
    compact = false
}: CultureSelectorProps) => {
    const [isOpen, setIsOpen] = useState(false);

    const currentCulture = CULTURAL_CONTEXTS.find(c => c.id === selectedCulture)
        || CULTURAL_CONTEXTS[0];

    return (
        <div className="culture-selector">
            <button
                className={`culture-trigger ${compact ? 'compact' : ''}`}
                onClick={() => setIsOpen(!isOpen)}
            >
                <Globe size={compact ? 16 : 18} />
                <span className="culture-flag">{currentCulture.flag}</span>
                {!compact && <span className="culture-name">{currentCulture.name}</span>}
                <ChevronDown size={14} className={`chevron ${isOpen ? 'open' : ''}`} />
            </button>

            {isOpen && (
                <div className="culture-dropdown">
                    <div className="dropdown-header">
                        <h4>문화권 선택 / Select Culture</h4>
                        <p>성격 분석의 문화적 해석을 조정합니다</p>
                    </div>

                    <div className="culture-options">
                        {CULTURAL_CONTEXTS.map(culture => (
                            <button
                                key={culture.id}
                                className={`culture-option ${selectedCulture === culture.id ? 'selected' : ''}`}
                                onClick={() => {
                                    onCultureChange(culture.id);
                                    setIsOpen(false);
                                }}
                            >
                                <span className="option-flag">{culture.flag}</span>
                                <div className="option-info">
                                    <span className="option-name">{culture.name}</span>
                                    <span className="option-desc">{culture.description}</span>
                                </div>
                                {selectedCulture === culture.id && (
                                    <Check size={18} className="check-icon" />
                                )}
                            </button>
                        ))}
                    </div>

                    <div className="dropdown-footer">
                        <p>
                            <strong>Note:</strong> Cultural adjustments help provide
                            more accurate personality interpretations based on
                            cultural context. You can change this at any time.
                        </p>
                    </div>
                </div>
            )}

            <style dangerouslySetInnerHTML={{
                __html: `
                .culture-selector {
                    position: relative;
                }
                .culture-trigger {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 10px 16px;
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    color: white;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }
                .culture-trigger:hover {
                    background: rgba(255, 255, 255, 0.08);
                    border-color: rgba(0, 255, 255, 0.3);
                }
                .culture-trigger.compact {
                    padding: 8px 12px;
                }
                .culture-flag {
                    font-size: 1.2em;
                }
                .culture-name {
                    font-size: 0.9rem;
                }
                .chevron {
                    transition: transform 0.3s ease;
                    color: var(--text-muted);
                }
                .chevron.open {
                    transform: rotate(180deg);
                }
                .culture-dropdown {
                    position: absolute;
                    top: calc(100% + 8px);
                    right: 0;
                    min-width: 320px;
                    background: rgba(15, 15, 25, 0.98);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                    z-index: 1000;
                    animation: dropdownFadeIn 0.2s ease;
                }
                @keyframes dropdownFadeIn {
                    from {
                        opacity: 0;
                        transform: translateY(-10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                .dropdown-header {
                    padding: 16px 20px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
                }
                .dropdown-header h4 {
                    margin: 0 0 4px 0;
                    font-size: 0.9rem;
                    color: var(--neon-cyan);
                }
                .dropdown-header p {
                    margin: 0;
                    font-size: 0.75rem;
                    color: var(--text-muted);
                }
                .culture-options {
                    padding: 8px;
                    max-height: 300px;
                    overflow-y: auto;
                }
                .culture-option {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    width: 100%;
                    padding: 12px;
                    background: transparent;
                    border: 1px solid transparent;
                    border-radius: 8px;
                    color: white;
                    cursor: pointer;
                    text-align: left;
                    transition: all 0.2s ease;
                }
                .culture-option:hover {
                    background: rgba(255, 255, 255, 0.05);
                }
                .culture-option.selected {
                    background: rgba(0, 255, 255, 0.1);
                    border-color: rgba(0, 255, 255, 0.3);
                }
                .option-flag {
                    font-size: 1.5em;
                    flex-shrink: 0;
                }
                .option-info {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    gap: 2px;
                }
                .option-name {
                    font-weight: 500;
                    font-size: 0.9rem;
                }
                .option-desc {
                    font-size: 0.75rem;
                    color: var(--text-muted);
                }
                .check-icon {
                    color: var(--neon-cyan);
                    flex-shrink: 0;
                }
                .dropdown-footer {
                    padding: 12px 16px;
                    border-top: 1px solid rgba(255, 255, 255, 0.05);
                }
                .dropdown-footer p {
                    margin: 0;
                    font-size: 0.7rem;
                    color: var(--text-muted);
                    line-height: 1.5;
                }
            `}} />
        </div>
    );
};

export { CULTURAL_CONTEXTS };
export default CultureSelector;
