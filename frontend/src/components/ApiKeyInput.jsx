import { useState } from 'react';
import { HiEye, HiEyeOff, HiKey } from 'react-icons/hi';
import { useSettings } from '../context/SettingsContext';
import './ApiKeyInput.css';

export default function ApiKeyInput() {
    const { apiKey, setApiKey } = useSettings();
    const [showKey, setShowKey] = useState(false);
    const [saved, setSaved] = useState(false);

    const handleSave = () => {
        setSaved(true);
        setTimeout(() => setSaved(false), 2000);
    };

    const maskedKey = apiKey
        ? `${apiKey.substring(0, 6)}${'•'.repeat(Math.max(0, apiKey.length - 10))}${apiKey.substring(apiKey.length - 4)}`
        : '';

    return (
        <div className="api-key-input">
            <label className="api-key-input__label">
                <HiKey size={14} />
                API Key
            </label>
            <div className="api-key-input__wrapper">
                <input
                    type={showKey ? 'text' : 'password'}
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="Paste your API key here..."
                    className="api-key-input__field"
                    spellCheck={false}
                />
                <button
                    className="api-key-input__toggle"
                    onClick={() => setShowKey(!showKey)}
                    type="button"
                    title={showKey ? 'Hide key' : 'Show key'}
                >
                    {showKey ? <HiEyeOff size={16} /> : <HiEye size={16} />}
                </button>
                <button
                    className={`api-key-input__save ${saved ? 'api-key-input__save--saved' : ''}`}
                    onClick={handleSave}
                    type="button"
                    disabled={!apiKey}
                >
                    {saved ? '✓ Saved' : 'Save'}
                </button>
            </div>
            {apiKey && (
                <p className="api-key-input__hint">
                    Key stored locally in your browser. Never sent to our servers.
                </p>
            )}
        </div>
    );
}
