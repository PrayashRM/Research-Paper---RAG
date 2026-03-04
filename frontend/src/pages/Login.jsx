import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { HiMail, HiLockClosed, HiEye, HiEyeOff } from 'react-icons/hi';
import { useAuth } from '../context/AuthContext';
import { APP_NAME } from '../utils/constants';
import './Login.css';

export default function Login() {
    const { login, isLoading } = useAuth();
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [remember, setRemember] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!email || !password) {
            setError('Please fill in all fields.');
            return;
        }

        try {
            await login(email, password);
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid credentials. Please try again.');
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
                    <h1 className="auth-card__title">Welcome back</h1>
                    <p className="auth-card__subtitle">Sign in to your account to continue</p>
                </div>

                {error && (
                    <div className="auth-card__error">
                        {error}
                    </div>
                )}

                <form className="auth-form" onSubmit={handleSubmit}>
                    <div className="auth-form__group">
                        <label className="auth-form__label" htmlFor="login-email">Email</label>
                        <div className="auth-form__input-wrapper">
                            <HiMail size={18} className="auth-form__icon" />
                            <input
                                type="email"
                                id="login-email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="you@example.com"
                                className="auth-form__input"
                                autoComplete="email"
                            />
                        </div>
                    </div>

                    <div className="auth-form__group">
                        <label className="auth-form__label" htmlFor="login-password">Password</label>
                        <div className="auth-form__input-wrapper">
                            <HiLockClosed size={18} className="auth-form__icon" />
                            <input
                                type={showPassword ? 'text' : 'password'}
                                id="login-password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                className="auth-form__input"
                                autoComplete="current-password"
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

                    <div className="auth-form__options">
                        <label className="auth-form__checkbox">
                            <input
                                type="checkbox"
                                checked={remember}
                                onChange={(e) => setRemember(e.target.checked)}
                            />
                            <span className="auth-form__checkbox-mark"></span>
                            Remember me
                        </label>
                        <a href="#" className="auth-form__forgot">Forgot password?</a>
                    </div>

                    <button
                        type="submit"
                        className="btn btn--lg btn--primary auth-form__submit"
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <span className="spinner"></span>
                                Signing in...
                            </>
                        ) : (
                            'Sign In'
                        )}
                    </button>
                </form>

                <div className="auth-card__footer">
                    Don't have an account?{' '}
                    <Link to="/signup" className="auth-card__link">Sign up</Link>
                </div>
            </div>
        </div>
    );
}
