import { useState, useRef, useEffect } from 'react';
import { HiChat, HiX, HiPaperAirplane, HiSparkles } from 'react-icons/hi';
import { MOCK_CHAT_MESSAGES } from '../utils/constants';
import './ChatSidebar.css';

export default function ChatSidebar({ isOpen, onToggle }) {
    const [messages, setMessages] = useState(MOCK_CHAT_MESSAGES);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        if (isOpen) inputRef.current?.focus();
    }, [isOpen]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input.trim() };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsTyping(true);

        // Simulate AI response
        await new Promise((resolve) => setTimeout(resolve, 1500));

        const assistantMessage = {
            role: 'assistant',
            content: generateMockResponse(userMessage.content),
        };
        setMessages((prev) => [...prev, assistantMessage]);
        setIsTyping(false);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <>
            {/* Toggle Button */}
            {!isOpen && (
                <button className="chat-toggle" onClick={onToggle} title="Open Q&A Chat">
                    <HiChat size={22} />
                    <span className="chat-toggle__badge">AI</span>
                </button>
            )}

            {/* Sidebar */}
            <aside className={`chat-sidebar glass ${isOpen ? 'chat-sidebar--open' : ''}`}>
                <div className="chat-sidebar__header">
                    <div className="chat-sidebar__header-info">
                        <HiSparkles size={18} className="chat-sidebar__header-icon" />
                        <div>
                            <h3 className="chat-sidebar__title">Research Q&A</h3>
                            <p className="chat-sidebar__subtitle">Ask questions about the paper</p>
                        </div>
                    </div>
                    <button className="chat-sidebar__close" onClick={onToggle}>
                        <HiX size={20} />
                    </button>
                </div>

                <div className="chat-sidebar__messages">
                    {messages.map((msg, index) => (
                        <div key={index} className={`chat-msg chat-msg--${msg.role}`}>
                            <div className="chat-msg__avatar">
                                {msg.role === 'assistant' ? '🤖' : '👤'}
                            </div>
                            <div className="chat-msg__content">
                                <p className="chat-msg__text">{msg.content}</p>
                            </div>
                        </div>
                    ))}

                    {isTyping && (
                        <div className="chat-msg chat-msg--assistant">
                            <div className="chat-msg__avatar">🤖</div>
                            <div className="chat-msg__content">
                                <div className="chat-msg__typing">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                <div className="chat-sidebar__input-area">
                    <div className="chat-sidebar__input-wrapper">
                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask a question about the paper..."
                            className="chat-sidebar__textarea"
                            rows={1}
                        />
                        <button
                            className="chat-sidebar__send"
                            onClick={handleSend}
                            disabled={!input.trim() || isTyping}
                            title="Send message"
                        >
                            <HiPaperAirplane size={18} />
                        </button>
                    </div>
                    <p className="chat-sidebar__disclaimer">
                        Responses are AI-generated and may not be fully accurate.
                    </p>
                </div>
            </aside>
        </>
    );
}

function generateMockResponse(query) {
    const responses = [
        'Based on the paper, the Transformer architecture relies entirely on self-attention mechanisms, eliminating the need for recurrent or convolutional layers. This allows for significantly more parallelization during training.',
        'The key innovation in this paper is the multi-head attention mechanism, which allows the model to attend to information from different representation subspaces at different positions simultaneously.',
        'According to the experimental results, the Transformer model achieved a BLEU score of 28.4 on the WMT 2014 English-to-German translation task, surpassing all previously reported models including ensembles.',
        'The paper proposes positional encoding using sine and cosine functions of different frequencies to inject information about the relative or absolute position of tokens in the sequence.',
        'The authors demonstrate that the Transformer generalizes well to other tasks, successfully applying it to English constituency parsing with both large and limited training data.',
    ];
    return responses[Math.floor(Math.random() * responses.length)];
}
