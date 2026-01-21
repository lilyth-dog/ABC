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
                <li><a href="#features">체험하기</a></li>
                <li><a href="#" onClick={(e) => { e.preventDefault(); onShowMemories?.(); }}>메모리</a></li>
                <li><a href="#pricing">플랜</a></li>
            </ul>

            <div className="nav-cta desktop-nav">
                <button className="btn btn-outline">로그인</button>
                <button className="btn btn-primary" onClick={onSignUp}>시작하기</button>
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
                            <li><a href="#features" onClick={closeMenu}>체험하기</a></li>
                            <li><a href="#" onClick={(e) => { e.preventDefault(); closeMenu(); onShowMemories?.(); }}>메모리</a></li>
                            <li><a href="#pricing" onClick={closeMenu}>플랜</a></li>
                        </ul>
                        <div className="mobile-nav-cta">
                            <button className="btn btn-outline" onClick={closeMenu}>로그인</button>
                            <button className="btn btn-primary" onClick={() => { closeMenu(); onSignUp?.(); }}>시작하기</button>
                        </div>
                    </div>
                </div>
            )}
        </nav>
    );
};

export default Navbar;
