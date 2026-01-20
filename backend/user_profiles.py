"""
User Profile Database for Continuous Learning
Digital Human Twin - Behavioral Profile Persistence Layer
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "user_profiles.db")
DB_PATH = os.getenv("DB_PATH", DEFAULT_DB_PATH)


def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table - unique user identification
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            avatar_url TEXT,
            display_name TEXT,
            maturity_level INTEGER DEFAULT 1,
            sync_score REAL DEFAULT 0.0
        )
    """)
    
    # Migration: Add columns if they don't exist (for existing databases)
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    if "maturity_level" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN maturity_level INTEGER DEFAULT 1")
    if "sync_score" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN sync_score REAL DEFAULT 0.0")
    
    # Behavioral sessions - raw session data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS behavioral_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            avg_decision_latency REAL,
            revision_rate REAL,
            path_efficiency REAL,
            total_interactions INTEGER,
            contextual_choices TEXT,  -- JSON: aesthetics, traits, etc.
            raw_metrics TEXT,         -- JSON: full behavioral profile
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Profile evolution - aggregated personality weights over time
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            logic_weight REAL,
            intuition_weight REAL,
            fluidity_weight REAL,
            complexity_weight REAL,
            archetype TEXT,
            confidence_score REAL,
            session_count INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Consent records table - GDPR compliance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consent_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            behavioral_tracking BOOLEAN,
            profile_storage BOOLEAN,
            continuous_learning BOOLEAN,
            ip_address TEXT,
            user_agent TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")


class UserProfileManager:
    """Manages user profiles and behavioral history."""
    
    def __init__(self):
        init_database()
    
    def get_or_create_user(self, user_id: str, avatar_url: str = None, display_name: str = None) -> Dict:
        """
        기존 사용자를 조회하거나 새 사용자를 생성합니다.
        
        Args:
            user_id (str): 사용자 고유 ID
            avatar_url (str, optional): 아바타 이미지 URL
            display_name (str, optional): 표시 이름
        
        Returns:
            Dict: 사용자 정보 딕셔너리
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute(
                "INSERT INTO users (id, avatar_url, display_name) VALUES (?, ?, ?)",
                (user_id, avatar_url, display_name)
            )
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
        
        conn.close()
        return dict(user)
    
    def save_session(self, user_id: str, behavioral_profile: Dict) -> int:
        """
        행동 세션 데이터를 저장합니다 (연속 학습용).
        
        Args:
            user_id (str): 사용자 고유 ID
            behavioral_profile (Dict): 행동 프로필 데이터
        
        Returns:
            int: 생성된 세션 ID
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Ensure user exists
        self.get_or_create_user(user_id)
        
        # Extract metrics
        summary = behavioral_profile.get("summary", {})
        contextual = behavioral_profile.get("contextualChoices", {})
        
        cursor.execute("""
            INSERT INTO behavioral_sessions 
            (user_id, avg_decision_latency, revision_rate, path_efficiency, 
             total_interactions, contextual_choices, raw_metrics)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            summary.get("avgDecisionLatency", 0),
            summary.get("revisionRate", 0),
            summary.get("pathEfficiency", 0),
            summary.get("totalInteractions", 0),
            json.dumps(contextual),
            json.dumps(behavioral_profile)
        ))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
    
    def get_session_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        사용자의 행동 세션 히스토리를 조회합니다.
        
        Args:
            user_id (str): 사용자 고유 ID
            limit (int): 조회할 최대 세션 수 (기본값: 10)
        
        Returns:
            List[Dict]: 세션 데이터 리스트 (최신순)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM behavioral_sessions 
            WHERE user_id = ? 
            ORDER BY session_timestamp DESC 
            LIMIT ?
        """, (user_id, limit))
        
        sessions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return sessions
    
    def update_user_maturity(self, user_id: str, level: int, sync_score: float):
        """Update user's maturity level and sync score."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users 
            SET maturity_level = ?, sync_score = ? 
            WHERE id = ?
        """, (level, sync_score, user_id))
        
        conn.commit()
        conn.close()
    
    def save_profile_evolution(self, user_id: str, weights: Dict, archetype: str, confidence: float):
        """Save evolved profile weights."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Count sessions
        cursor.execute("SELECT COUNT(*) FROM behavioral_sessions WHERE user_id = ?", (user_id,))
        session_count = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO profile_evolution 
            (user_id, logic_weight, intuition_weight, fluidity_weight, 
             complexity_weight, archetype, confidence_score, session_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            weights.get("Logic", 0),
            weights.get("Intuition", 0),
            weights.get("Fluidity", 0),
            weights.get("Complexity", 0),
            archetype,
            confidence,
            session_count
        ))
        
        conn.commit()
        conn.close()
    
    def get_profile_evolution(self, user_id: str) -> List[Dict]:
        """Get profile evolution history for visualization."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM profile_evolution 
            WHERE user_id = ? 
            ORDER BY timestamp ASC
        """, (user_id,))
        
        evolution = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return evolution
    
    def get_latest_profile(self, user_id: str) -> Optional[Dict]:
        """Get the most recent profile snapshot."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM profile_evolution 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return dict(result) if result else None
    
    # ============== GDPR COMPLIANCE METHODS ==============
    
    def delete_user_data(self, user_id: str) -> Dict:
        """
        GDPR Article 17 - Right to be Forgotten.
        Permanently delete all user data from all tables.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Count records before deletion for audit
            cursor.execute("SELECT COUNT(*) FROM behavioral_sessions WHERE user_id = ?", (user_id,))
            sessions_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM profile_evolution WHERE user_id = ?", (user_id,))
            profiles_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM consent_records WHERE user_id = ?", (user_id,))
            consents_count = cursor.fetchone()[0]
            
            # Delete from all tables
            cursor.execute("DELETE FROM behavioral_sessions WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM profile_evolution WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM consent_records WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            conn.commit()
            
            return {
                "status": "deleted",
                "user_id": user_id,
                "deleted_records": {
                    "behavioral_sessions": sessions_count,
                    "profile_evolution": profiles_count,
                    "consent_records": consents_count,
                    "user": 1
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            conn.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            conn.close()
    
    def export_user_data(self, user_id: str) -> Dict:
        """
        GDPR Article 20 - Right to Data Portability.
        Export all user data in machine-readable format (JSON).
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get user info
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_row = cursor.fetchone()
        user_data = dict(user_row) if user_row else None
        
        # Get all behavioral sessions
        cursor.execute("""
            SELECT * FROM behavioral_sessions 
            WHERE user_id = ? 
            ORDER BY session_timestamp ASC
        """, (user_id,))
        sessions = [dict(row) for row in cursor.fetchall()]
        
        # Parse JSON fields in sessions
        for session in sessions:
            if session.get('contextual_choices'):
                try:
                    session['contextual_choices'] = json.loads(session['contextual_choices'])
                except:
                    pass
            if session.get('raw_metrics'):
                try:
                    session['raw_metrics'] = json.loads(session['raw_metrics'])
                except:
                    pass
        
        # Get profile evolution
        cursor.execute("""
            SELECT * FROM profile_evolution 
            WHERE user_id = ? 
            ORDER BY timestamp ASC
        """, (user_id,))
        evolution = [dict(row) for row in cursor.fetchall()]
        
        # Get consent records
        cursor.execute("""
            SELECT * FROM consent_records 
            WHERE user_id = ? 
            ORDER BY timestamp ASC
        """, (user_id,))
        consents = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "export_metadata": {
                "user_id": user_id,
                "export_timestamp": datetime.now().isoformat(),
                "format_version": "1.0",
                "gdpr_article": "Article 20 - Right to Data Portability"
            },
            "user_profile": user_data,
            "behavioral_sessions": sessions,
            "personality_evolution": evolution,
            "consent_history": consents,
            "data_summary": {
                "total_sessions": len(sessions),
                "total_profile_snapshots": len(evolution),
                "consent_records": len(consents)
            }
        }
    
    def save_consent(self, user_id: str, consent_data: Dict, 
                     ip_address: str = None, user_agent: str = None) -> int:
        """
        Record user consent for GDPR compliance.
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        # Ensure user exists
        self.get_or_create_user(user_id)
        
        cursor.execute("""
            INSERT INTO consent_records 
            (user_id, behavioral_tracking, profile_storage, continuous_learning, 
             ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            consent_data.get('behavioralTracking', False),
            consent_data.get('profileStorage', False),
            consent_data.get('continuousLearning', False),
            ip_address,
            user_agent
        ))
        
        consent_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return consent_id
    
    def get_latest_consent(self, user_id: str) -> Optional[Dict]:
        """Get the most recent consent record for a user."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM consent_records 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return dict(result) if result else None


# Initialize on import
if __name__ == "__main__":
    init_database()
    print("Database schema created successfully!")

