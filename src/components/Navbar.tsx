import { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';

interface NavbarProps {
    onSignUp?: () => void;
    onShowMemories?: () => void;
}

const Navbar = ({ onSignUp, onShowMemories }: NavbarProps) => {
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 50);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const closeMenu = () => setMobileMenuOpen(false);

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="logo gradient-text">NEXUS</div>

            {/* Desktop Navigation */}
            <ul className="nav-links desktop-nav">
                <li><a href="#features">Experience</a></li>
                <li><a href="#" onClick={(e) => { e.preventDefault(); onShowMemories?.(); }}>Memories</a></li>
                <li><a href="#pricing">Plan</a></li>
            </ul>

            <div className="nav-cta desktop-nav">
                <button className="btn btn-outline">Log In</button>
                <button className="btn btn-primary" onClick={onSignUp}>Get Started</button>
            </div>

            {/* Mobile Hamburger Button */}
            <button
                className="mobile-menu-btn"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                aria-label="Toggle menu"
            >
                {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            {/* Mobile Menu Overlay */}
            {mobileMenuOpen && (
                <div className="mobile-menu-overlay" onClick={closeMenu}>
                    <div className="mobile-menu" onClick={(e) => e.stopPropagation()}>
                        <ul className="mobile-nav-links">
                            <li><a href="#features" onClick={closeMenu}>Experience</a></li>
                            <li><a href="#" onClick={(e) => { e.preventDefault(); closeMenu(); onShowMemories?.(); }}>Memories</a></li>
                            <li><a href="#pricing" onClick={closeMenu}>Plan</a></li>
                        </ul>
                        <div className="mobile-nav-cta">
                            <button className="btn btn-outline" onClick={closeMenu}>Log In</button>
                            <button className="btn btn-primary" onClick={() => { closeMenu(); onSignUp?.(); }}>Get Started</button>
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
