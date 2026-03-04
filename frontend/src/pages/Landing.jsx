import { Link } from 'react-router-dom';
import { HiSparkles, HiBookOpen, HiChat, HiLightningBolt, HiShieldCheck, HiCode } from 'react-icons/hi';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import './Landing.css';

const features = [
    {
        icon: <HiBookOpen size={28} />,
        title: 'Structured Notes',
        description: 'Automatically generate comprehensive, well-organized notes from any research paper. Every section, clearly structured.',
    },
    {
        icon: <HiChat size={28} />,
        title: 'AI-Powered Q&A',
        description: 'Ask questions about the paper and get instant, context-aware answers powered by advanced RAG architecture.',
    },
    {
        icon: <HiLightningBolt size={28} />,
        title: 'Multi-Model Support',
        description: 'Choose from GPT-4, Claude, Gemini, and open-source models. Use whichever LLM works best for you.',
    },
    {
        icon: <HiShieldCheck size={28} />,
        title: 'Your Keys, Your Data',
        description: 'Bring your own API keys. Your data stays in your browser — we never store or access your keys on our servers.',
    },
    {
        icon: <HiCode size={28} />,
        title: 'Open Architecture',
        description: 'Built on modern, extensible architecture. Easily integrate with your existing research workflows.',
    },
    {
        icon: <HiSparkles size={28} />,
        title: 'Intelligent Parsing',
        description: 'Advanced PDF parsing that understands paper structure — sections, equations, figures, and references.',
    },
];

const steps = [
    {
        number: '01',
        title: 'Upload Your Paper',
        description: 'Drag & drop any research paper PDF. Our parser extracts and structures the content automatically.',
    },
    {
        number: '02',
        title: 'Choose Your Model',
        description: 'Select from top-tier LLMs and paste your API key. Everything runs through your own credentials.',
    },
    {
        number: '03',
        title: 'Generate & Explore',
        description: 'Get structured notes instantly and ask follow-up questions through our intelligent Q&A system.',
    },
];

export default function Landing() {
    const { user } = useAuth();

    return (
        <div className="landing">
            <Navbar />

            {/* Hero */}
            <section className="hero">
                <div className="hero__bg"></div>
                <div className="hero__content container">
                    <div className="hero__badge animate-fade-in">
                        <HiSparkles size={14} />
                        <span>AI-Powered Research Assistant</span>
                    </div>
                    <h1 className="hero__title animate-fade-in-up">
                        Read Research Papers
                        <br />
                        <span className="gradient-text">Like Never Before</span>
                    </h1>
                    <p className="hero__subtitle animate-fade-in-up" style={{ animationDelay: '0.15s' }}>
                        Transform complex academic papers into structured, digestible notes.
                        Ask questions, get answers — powered by the LLM of your choice.
                    </p>
                    <div className="hero__actions animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
                        <Link to={user ? '/dashboard' : '/signup'} className="btn btn--lg btn--primary">
                            Get Started Free
                        </Link>
                        <a href="#features" className="btn btn--lg btn--ghost">
                            Learn More
                        </a>
                    </div>
                    <div className="hero__stats animate-fade-in-up" style={{ animationDelay: '0.45s' }}>
                        <div className="hero__stat">
                            <span className="hero__stat-value">10+</span>
                            <span className="hero__stat-label">LLM Models</span>
                        </div>
                        <div className="hero__stat-divider"></div>
                        <div className="hero__stat">
                            <span className="hero__stat-value">100%</span>
                            <span className="hero__stat-label">Private & Secure</span>
                        </div>
                        <div className="hero__stat-divider"></div>
                        <div className="hero__stat">
                            <span className="hero__stat-value">PDF</span>
                            <span className="hero__stat-label">Upload Support</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features */}
            <section id="features" className="features-section">
                <div className="container">
                    <div className="section-header">
                        <span className="section-tag">Features</span>
                        <h2 className="section-title">
                            Everything you need to
                            <br />
                            <span className="gradient-text">understand research</span>
                        </h2>
                        <p className="section-subtitle">
                            Powerful tools designed to make academic papers accessible to everyone.
                        </p>
                    </div>

                    <div className="features-grid stagger-children">
                        {features.map((feature, index) => (
                            <div key={index} className="feature-card glass-card">
                                <div className="feature-card__icon">{feature.icon}</div>
                                <h3 className="feature-card__title">{feature.title}</h3>
                                <p className="feature-card__desc">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works */}
            <section id="how-it-works" className="how-section">
                <div className="container">
                    <div className="section-header">
                        <span className="section-tag">How It Works</span>
                        <h2 className="section-title">
                            Three simple steps to
                            <br />
                            <span className="gradient-text">clarity</span>
                        </h2>
                    </div>

                    <div className="steps stagger-children">
                        {steps.map((step, index) => (
                            <div key={index} className="step-card">
                                <div className="step-card__number gradient-text">{step.number}</div>
                                <div className="step-card__content">
                                    <h3 className="step-card__title">{step.title}</h3>
                                    <p className="step-card__desc">{step.description}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA */}
            <section id="about" className="cta-section">
                <div className="container">
                    <div className="cta-card glass-card">
                        <h2 className="cta-card__title">
                            Ready to transform how you read research?
                        </h2>
                        <p className="cta-card__text">
                            Join researchers, students, and curious minds who are already using ResearchLens
                            to make academic papers more accessible.
                        </p>
                        <Link to={user ? '/dashboard' : '/signup'} className="btn btn--lg btn--primary">
                            Start Reading Smarter
                        </Link>
                    </div>
                </div>
            </section>

            <Footer />
        </div>
    );
}
