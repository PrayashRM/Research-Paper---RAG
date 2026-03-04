import { createContext, useContext, useCallback } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

const SettingsContext = createContext(null);

export function SettingsProvider({ children }) {
    const [selectedModel, setSelectedModel] = useLocalStorage('rl_model', 'gpt-4o');
    const [apiKey, setApiKey] = useLocalStorage('rl_api_key', '');
    const [uploadedFile, setUploadedFile] = useLocalStorage('rl_uploaded_file', null);

    const clearSettings = useCallback(() => {
        setSelectedModel('gpt-4o');
        setApiKey('');
        setUploadedFile(null);
    }, [setSelectedModel, setApiKey, setUploadedFile]);

    return (
        <SettingsContext.Provider
            value={{
                selectedModel,
                setSelectedModel,
                apiKey,
                setApiKey,
                uploadedFile,
                setUploadedFile,
                clearSettings,
            }}
        >
            {children}
        </SettingsContext.Provider>
    );
}

export function useSettings() {
    const context = useContext(SettingsContext);
    if (!context) {
        throw new Error('useSettings must be used within a SettingsProvider');
    }
    return context;
}
