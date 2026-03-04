import { useState, useRef } from 'react';
import { HiCloudUpload, HiDocument, HiX } from 'react-icons/hi';
import { useSettings } from '../context/SettingsContext';
import './FileUpload.css';

export default function FileUpload() {
    const { uploadedFile, setUploadedFile } = useSettings();
    const [isDragOver, setIsDragOver] = useState(false);
    const inputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragOver(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragOver(false);
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            setUploadedFile({
                name: file.name,
                size: file.size,
                type: file.type,
                lastModified: file.lastModified,
            });
        }
    };

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            setUploadedFile({
                name: file.name,
                size: file.size,
                type: file.type,
                lastModified: file.lastModified,
            });
        }
    };

    const handleRemove = () => {
        setUploadedFile(null);
        if (inputRef.current) inputRef.current.value = '';
    };

    const formatSize = (bytes) => {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    };

    if (uploadedFile) {
        return (
            <div className="file-upload__uploaded glass-card">
                <div className="file-upload__file-info">
                    <div className="file-upload__file-icon">
                        <HiDocument size={24} />
                    </div>
                    <div className="file-upload__file-details">
                        <p className="file-upload__file-name">{uploadedFile.name}</p>
                        <p className="file-upload__file-size">{formatSize(uploadedFile.size)}</p>
                    </div>
                    <button className="file-upload__remove" onClick={handleRemove} title="Remove file">
                        <HiX size={18} />
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div
            className={`file-upload__zone ${isDragOver ? 'file-upload__zone--drag' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
        >
            <input
                ref={inputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="file-upload__input"
            />
            <div className="file-upload__icon">
                <HiCloudUpload size={40} />
            </div>
            <p className="file-upload__text">
                <span className="file-upload__text-highlight">Click to upload</span> or drag and drop
            </p>
            <p className="file-upload__hint">PDF files only (max 50MB)</p>
        </div>
    );
}
