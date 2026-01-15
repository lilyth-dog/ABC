const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-brand">
                    <div className="logo gradient-text">NEXUS</div>
                    <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>Redefining digital excellence.</p>
                </div>
                <div className="footer-links" style={{ display: 'flex', gap: '4rem' }}>
                    <div className="link-group">
                        <h4 style={{ marginBottom: '1.5rem' }}>Product</h4>
                        <a href="#features" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>Features</a>
                        <a href="#pricing" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>Pricing</a>
                    </div>
                    <div className="link-group">
                        <h4 style={{ marginBottom: '1.5rem' }}>Company</h4>
                        <a href="#" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>About</a>
                        <a href="#" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>Careers</a>
                    </div>
                </div>
            </div>
            <div className="footer-bottom" style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem', paddingTop: '2rem', borderTop: '1px solid var(--glass-border)' }}>
                &copy; 2025 Nexus. All rights reserved.
            </div>
        </footer>
    );
};

export default Footer;
