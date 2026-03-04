import { useState, useRef, useEffect } from 'react';
import { HiChevronDown, HiCheck } from 'react-icons/hi';
import { AVAILABLE_MODELS } from '../utils/constants';
import { useSettings } from '../context/SettingsContext';
import './ModelSelector.css';

export default function ModelSelector() {
    const { selectedModel, setSelectedModel } = useSettings();
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    const allModels = AVAILABLE_MODELS.flatMap((g) => g.models);
    const currentModel = allModels.find((m) => m.id === selectedModel) || allModels[0];

    useEffect(() => {
        function handleClickOutside(e) {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                setIsOpen(false);
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <div className="model-selector" ref={dropdownRef}>
            <label className="model-selector__label">Model</label>
            <button
                className="model-selector__trigger"
                onClick={() => setIsOpen(!isOpen)}
                type="button"
            >
                <div className="model-selector__selected">
                    <span className="model-selector__name">{currentModel.name}</span>
                    <span className="model-selector__desc">{currentModel.description}</span>
                </div>
                <HiChevronDown
                    className={`model-selector__chevron ${isOpen ? 'model-selector__chevron--open' : ''}`}
                    size={18}
                />
            </button>

            {isOpen && (
                <div className="model-selector__dropdown glass-card">
                    {AVAILABLE_MODELS.map((group) => (
                        <div key={group.provider} className="model-selector__group">
                            <div className="model-selector__provider">{group.provider}</div>
                            {group.models.map((model) => (
                                <button
                                    key={model.id}
                                    className={`model-selector__option ${model.id === selectedModel ? 'model-selector__option--selected' : ''}`}
                                    onClick={() => {
                                        setSelectedModel(model.id);
                                        setIsOpen(false);
                                    }}
                                >
                                    <div>
                                        <div className="model-selector__option-name">{model.name}</div>
                                        <div className="model-selector__option-desc">{model.description}</div>
                                    </div>
                                    {model.id === selectedModel && <HiCheck size={16} className="model-selector__check" />}
                                </button>
                            ))}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
