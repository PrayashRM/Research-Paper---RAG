import { APP_NAME } from '../utils/constants';
import { FiGithub, FiTwitter, FiMail } from 'react-icons/fi';
import './Footer.css';

export default function Footer() {
    return (
        <footer className="footer">
            <div className="footer__inner container">
                <div className="footer__top">
                    <div className="footer__brand">
                        <div className="footer__logo">
                            <span className="footer__logo-icon">📄</span>
                            <span className="gradient-text">{APP_NAME}</span>
                        </div>
                        <p className="footer__tagline">
                            Making research papers accessible and appealing to everyone.
                        </p>
                    </div>

                    <div className="footer__links-group">
                        <h4 className="footer__heading">Product</h4>
                        <a href="/#features" className="footer__link">Features</a>
                        <a href="/#how-it-works" className="footer__link">How It Works</a>
                        <a href="/#about" className="footer__link">About</a>
                    </div>

                    <div className="footer__links-group">
                        <h4 className="footer__heading">Support</h4>
                        <a href="#" className="footer__link">Documentation</a>
                        <a href="#" className="footer__link">FAQ</a>
                        <a href="#" className="footer__link">Contact</a>
                    </div>

                    <div className="footer__links-group">
                        <h4 className="footer__heading">Legal</h4>
                        <a href="#" className="footer__link">Privacy Policy</a>
                        <a href="#" className="footer__link">Terms of Service</a>
                    </div>
                </div>

                <div className="footer__bottom">
                    <p className="footer__copyright">
                        &copy; {new Date().getFullYear()} {APP_NAME}. All rights reserved.
                    </p>
                    <div className="footer__socials">
                        <a href="#" className="footer__social" aria-label="GitHub"><FiGithub size={18} /></a>
                        <a href="#" className="footer__social" aria-label="Twitter"><FiTwitter size={18} /></a>
                        <a href="#" className="footer__social" aria-label="Email"><FiMail size={18} /></a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
