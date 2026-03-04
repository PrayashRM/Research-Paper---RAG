import { useState } from 'react';
import { HiSparkles, HiBookOpen, HiChevronDown, HiChevronRight } from 'react-icons/hi';
import { MOCK_NOTES } from '../utils/constants';
import { useSettings } from '../context/SettingsContext';
import './NotesPanel.css';

export default function NotesPanel() {
    const { uploadedFile } = useSettings();
    const [notes, setNotes] = useState(null);
    const [isGenerating, setIsGenerating] = useState(false);
    const [expandedSections, setExpandedSections] = useState({});

    const handleGenerate = async () => {
        setIsGenerating(true);
        // Simulate generation delay
        await new Promise((resolve) => setTimeout(resolve, 2500));
        setNotes(MOCK_NOTES);
        // Expand all sections by default
        const expanded = {};
        MOCK_NOTES.sections.forEach((_, i) => { expanded[i] = true; });
        setExpandedSections(expanded);
        setIsGenerating(false);
    };

    const toggleSection = (index) => {
        setExpandedSections((prev) => ({ ...prev, [index]: !prev[index] }));
    };

    if (!uploadedFile) {
        return (
            <div className="notes-panel notes-panel--empty">
                <div className="notes-panel__empty-icon">
                    <HiBookOpen size={48} />
                </div>
                <h3 className="notes-panel__empty-title">No Paper Uploaded</h3>
                <p className="notes-panel__empty-text">
                    Upload a research paper to generate structured notes.
                </p>
            </div>
        );
    }

    return (
        <div className="notes-panel">
            <div className="notes-panel__header">
                <h2 className="notes-panel__title">
                    <HiBookOpen size={20} />
                    Structured Notes
                </h2>
                {!notes && (
                    <button
                        className="btn btn--md btn--primary notes-panel__generate"
                        onClick={handleGenerate}
                        disabled={isGenerating}
                    >
                        {isGenerating ? (
                            <>
                                <span className="spinner"></span>
                                Generating...
                            </>
                        ) : (
                            <>
                                <HiSparkles size={18} />
                                Generate Notes
                            </>
                        )}
                    </button>
                )}
                {notes && (
                    <button
                        className="btn btn--sm btn--outline"
                        onClick={handleGenerate}
                        disabled={isGenerating}
                    >
                        {isGenerating ? 'Regenerating...' : 'Regenerate'}
                    </button>
                )}
            </div>

            {isGenerating && !notes && (
                <div className="notes-panel__loading">
                    <div className="notes-panel__loading-bar">
                        <div className="notes-panel__loading-progress"></div>
                    </div>
                    <p className="notes-panel__loading-text">
                        Analyzing paper and generating structured notes...
                    </p>
                </div>
            )}

            {notes && (
                <div className="notes-panel__content animate-fade-in">
                    <div className="notes-panel__meta">
                        <h3 className="notes-panel__paper-title">{notes.title}</h3>
                        <p className="notes-panel__authors">{notes.authors}</p>
                    </div>

                    <div className="notes-panel__sections">
                        {notes.sections.map((section, index) => (
                            <div
                                key={index}
                                className={`notes-panel__section ${expandedSections[index] ? 'notes-panel__section--open' : ''}`}
                            >
                                <button
                                    className="notes-panel__section-header"
                                    onClick={() => toggleSection(index)}
                                >
                                    <span className="notes-panel__section-number">{String(index + 1).padStart(2, '0')}</span>
                                    <span className="notes-panel__section-heading">{section.heading}</span>
                                    {expandedSections[index] ? (
                                        <HiChevronDown size={18} className="notes-panel__section-icon" />
                                    ) : (
                                        <HiChevronRight size={18} className="notes-panel__section-icon" />
                                    )}
                                </button>
                                {expandedSections[index] && (
                                    <div className="notes-panel__section-body animate-fade-in">
                                        <p>{section.content}</p>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
