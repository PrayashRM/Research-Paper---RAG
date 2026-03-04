import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { HiUser, HiMail, HiLockClosed, HiEye, HiEyeOff } from 'react-icons/hi';
import { useAuth } from '../context/AuthContext';
import { APP_NAME } from '../utils/constants';
import './Login.css'; /* Reuses Login.css for shared auth styling */

export default function Signup() {
    const { signup, isLoading } = useAuth();
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!name || !email || !password || !confirmPassword) {
            setError('Please fill in all fields.');
            return;
        }

        if (password !== confirmPassword) {
            setError('Passwords do not match.');
            return;
        }

        if (password.length < 6) {
            setError('Password must be at least 6 characters.');
            return;
        }

        try {
            await signup(name, email, password);
            navigate('/dashboard');
        } catch (err) {
            setError('Something went wrong. Please try again.');
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-page__bg"></div>

            <div className="auth-card glass-card animate-fade-in-up">
                <div className="auth-card__header">
                    <Link to="/" className="auth-card__logo">
                        <span>📄</span>
                        <span className="gradient-text">{APP_NAME}</span>
                    </Link>
                    <h1 className="auth-card__title">Create your account</h1>
                    <p className="auth-card__subtitle">Start reading research papers smarter</p>
                </div>

                {error && (
                    <div className="auth-card__error">
                        {error}
                    </div>
                )}

                <form className="auth-form" onSubmit={handleSubmit}>
                    <div className="auth-form__group">
                        <label className="auth-form__label" htmlFor="signup-name">Full Name</label>
                        <div className="auth-form__input-wrapper">
                            <HiUser size={18} className="auth-form__icon" />
                            <input
                                type="text"
                                id="signup-name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="John Doe"
                                className="auth-form__input"
                                autoComplete="name"
                            />
                        </div>
                    </div>

                    <div className="auth-form__group">
                        <label className="auth-form__label" htmlFor="signup-email">Email</label>
                        <div className="auth-form__input-wrapper">
                            <HiMail size={18} className="auth-form__icon" />
                            <input
                                type="email"
                                id="signup-email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="you@example.com"
                                className="auth-form__input"
                                autoComplete="email"
                            />
                        </div>
                    </div>

                    <div className="auth-form__group">
                        <label className="auth-form__label" htmlFor="signup-password">Password</label>
                        <div className="auth-form__input-wrapper">
                            <HiLockClosed size={18} className="auth-form__icon" />
                            <input
                                type={showPassword ? 'text' : 'password'}
                                id="signup-password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Min 6 characters"
                                className="auth-form__input"
                                autoComplete="new-password"
                            />
                            <button
                                type="button"
                                className="auth-form__toggle"
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? <HiEyeOff size={18} /> : <HiEye size={18} />}
                            </button>
                        </div>
                    </div>

                    <div className="auth-form__group">
                        <label className="auth-form__label" htmlFor="signup-confirm">Confirm Password</label>
                        <div className="auth-form__input-wrapper">
                            <HiLockClosed size={18} className="auth-form__icon" />
                            <input
                                type={showPassword ? 'text' : 'password'}
                                id="signup-confirm"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                placeholder="Repeat password"
                                className="auth-form__input"
                                autoComplete="new-password"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        className="btn btn--lg btn--primary auth-form__submit"
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <span className="spinner"></span>
                                Creating account...
                            </>
                        ) : (
                            'Create Account'
                        )}
                    </button>
                </form>

                <div className="auth-card__footer">
                    Already have an account?{' '}
                    <Link to="/login" className="auth-card__link">Sign in</Link>
                </div>
            </div>
        </div>
    );
}
