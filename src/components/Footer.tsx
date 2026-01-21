const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-brand">
                    <div className="logo gradient-text">NEXUS</div>
                    <p style={{ color: 'var(--text-muted)', marginTop: '1rem' }}>디지털 경험의 새로운 정의.</p>
                </div>
                <div className="footer-links" style={{ display: 'flex', gap: '4rem' }}>
                    <div className="link-group">
                        <h4 style={{ marginBottom: '1.5rem' }}>제품</h4>
                        <a href="#features" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>주요 기능</a>
                        <a href="#pricing" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>가격 정책</a>
                    </div>
                    <div className="link-group">
                        <h4 style={{ marginBottom: '1.5rem' }}>회사</h4>
                        <a href="#" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>소개</a>
                        <a href="#" style={{ display: 'block', color: 'var(--text-muted)', textDecoration: 'none', marginBottom: '0.75rem' }}>채용</a>
                    </div>
                </div>
            </div>
            <div className="footer-bottom" style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem', paddingTop: '2rem', borderTop: '1px solid var(--glass-border)' }}>
                &copy; 2025 Nexus. 모든 권리 보유.
            </div>
        </footer>
    );
};

export default Footer;
