import { useState } from 'react';
import { useSettings } from '../context/SettingsContext';
import Navbar from '../components/Navbar';
import ModelSelector from '../components/ModelSelector';
import ApiKeyInput from '../components/ApiKeyInput';
import FileUpload from '../components/FileUpload';
import NotesPanel from '../components/NotesPanel';
import ChatSidebar from '../components/ChatSidebar';
import { HiCog, HiChevronDown, HiChevronUp } from 'react-icons/hi';
import './Dashboard.css';

export default function Dashboard() {
    const { uploadedFile } = useSettings();
    const [chatOpen, setChatOpen] = useState(false);
    const [settingsExpanded, setSettingsExpanded] = useState(true);

    return (
        <div className={`dashboard ${chatOpen ? 'dashboard--chat-open' : ''}`}>
            <Navbar />

            <div className="dashboard__content">
                {/* Top Config Bar */}
                <div className="dashboard__config glass">
                    <button
                        className="dashboard__config-toggle"
                        onClick={() => setSettingsExpanded(!settingsExpanded)}
                    >
                        <HiCog size={18} className="dashboard__config-icon" />
                        <span className="dashboard__config-title">Configuration</span>
                        {settingsExpanded ? <HiChevronUp size={16} /> : <HiChevronDown size={16} />}
                    </button>

                    {settingsExpanded && (
                        <div className="dashboard__config-panel animate-fade-in">
                            <div className="dashboard__config-row">
                                <ModelSelector />
                                <ApiKeyInput />
                            </div>
                        </div>
                    )}
                </div>

                {/* Main Area */}
                <div className="dashboard__main">
                    {!uploadedFile ? (
                        /* Upload Area */
                        <div className="dashboard__upload-area">
                            <div className="dashboard__upload-container">
                                <h2 className="dashboard__upload-title">Upload a Research Paper</h2>
                                <p className="dashboard__upload-subtitle">
                                    Drop your PDF below to generate structured notes and start asking questions.
                                </p>
                                <FileUpload />
                            </div>
                        </div>
                    ) : (
                        /* Paper Workspace */
                        <div className="dashboard__workspace">
                            <div className="dashboard__workspace-header">
                                <FileUpload />
                            </div>
                            <div className="dashboard__workspace-content">
                                <NotesPanel />
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Chat Sidebar */}
            {uploadedFile && (
                <ChatSidebar isOpen={chatOpen} onToggle={() => setChatOpen(!chatOpen)} />
            )}
        </div>
    );
}
