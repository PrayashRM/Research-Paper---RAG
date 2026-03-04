import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { HiMenuAlt3, HiX } from 'react-icons/hi';
import { useAuth } from '../context/AuthContext';
import { APP_NAME, NAV_LINKS } from '../utils/constants';
import './Navbar.css';

export default function Navbar() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [mobileOpen, setMobileOpen] = useState(false);

    const isDashboard = location.pathname === '/dashboard';

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <nav className="navbar glass">
            <div className="navbar__inner container">
                <Link to="/" className="navbar__logo">
                    <span className="navbar__logo-icon">📄</span>
                    <span className="navbar__logo-text gradient-text">{APP_NAME}</span>
                </Link>

                {!isDashboard && (
                    <div className={`navbar__links ${mobileOpen ? 'navbar__links--open' : ''}`}>
                        {NAV_LINKS.map((link) => (
                            <a key={link.label} href={link.href} className="navbar__link" onClick={() => setMobileOpen(false)}>
                                {link.label}
                            </a>
                        ))}
                    </div>
                )}

                <div className="navbar__actions">
                    {user ? (
                        <div className="navbar__user">
                            <div className="navbar__avatar">
                                {user.name.charAt(0).toUpperCase()}
                            </div>
                            <span className="navbar__user-name">{user.name}</span>
                            {!isDashboard && (
                                <Link to="/dashboard" className="btn btn--sm btn--primary">
                                    Dashboard
                                </Link>
                            )}
                            <button onClick={handleLogout} className="btn btn--sm btn--ghost">
                                Logout
                            </button>
                        </div>
                    ) : (
                        <div className="navbar__auth">
                            <Link to="/login" className="btn btn--sm btn--ghost">
                                Sign In
                            </Link>
                            <Link to="/signup" className="btn btn--sm btn--primary">
                                Get Started
                            </Link>
                        </div>
                    )}

                    <button
                        className="navbar__toggle"
                        onClick={() => setMobileOpen(!mobileOpen)}
                        aria-label="Toggle menu"
                    >
                        {mobileOpen ? <HiX size={24} /> : <HiMenuAlt3 size={24} />}
                    </button>
                </div>
            </div>
        </nav>
    );
}
