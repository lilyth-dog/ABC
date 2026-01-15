"""
Test suite for user_profiles.py GDPR compliance functions.
"""
import pytest
import os
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_profiles import UserProfileManager, init_database, get_connection


class TestUserProfileManager:
    """Test suite for UserProfileManager class."""
    
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Setup test database in temporary directory."""
        self.test_db = tmp_path / "test_profiles.db"
        # Patch the database path
        import user_profiles
        self.original_get_connection = user_profiles.get_connection
        
        def test_get_connection():
            import sqlite3
            conn = sqlite3.connect(str(self.test_db))
            conn.row_factory = sqlite3.Row
            return conn
        
        user_profiles.get_connection = test_get_connection
        init_database()
        self.manager = UserProfileManager()
        yield
        user_profiles.get_connection = self.original_get_connection
    
    def test_get_or_create_user(self):
        """Test user creation and retrieval."""
        user_id = "test_user_001"
        
        # Create user
        result = self.manager.get_or_create_user(user_id)
        assert result['id'] == user_id
        
        # Retrieve same user
        result2 = self.manager.get_or_create_user(user_id)
        assert result2['id'] == user_id
    
    def test_save_consent(self):
        """Test saving consent records."""
        user_id = "consent_test_user"
        consent_data = {
            'behavioralTracking': True,
            'profileStorage': True,
            'continuousLearning': False
        }
        
        consent_id = self.manager.save_consent(user_id, consent_data)
        
        assert consent_id is not None
        assert consent_id > 0
    
    def test_get_latest_consent(self):
        """Test retrieving latest consent."""
        user_id = "consent_get_user"
        consent_data = {
            'behavioralTracking': True,
            'profileStorage': False,
            'continuousLearning': True
        }
        
        self.manager.save_consent(user_id, consent_data)
        
        result = self.manager.get_latest_consent(user_id)
        
        assert result is not None
        assert result['behavioral_tracking'] == 1  # SQLite stores bool as int
        assert result['profile_storage'] == 0
        assert result['continuous_learning'] == 1
    
    def test_export_user_data(self):
        """Test GDPR data export functionality."""
        user_id = "export_test_user"
        
        # Create user and some data
        self.manager.get_or_create_user(user_id)
        self.manager.save_consent(user_id, {
            'behavioralTracking': True,
            'profileStorage': True,
            'continuousLearning': True
        })
        
        export = self.manager.export_user_data(user_id)
        
        assert 'export_metadata' in export
        assert export['export_metadata']['user_id'] == user_id
        assert 'user_profile' in export
        assert 'behavioral_sessions' in export
        assert 'consent_history' in export
        assert 'data_summary' in export
        assert export['data_summary']['consent_records'] == 1
    
    def test_delete_user_data(self):
        """Test GDPR data deletion (Right to be Forgotten)."""
        user_id = "delete_test_user"
        
        # Create user and data
        self.manager.get_or_create_user(user_id)
        self.manager.save_consent(user_id, {
            'behavioralTracking': True,
            'profileStorage': True,
            'continuousLearning': True
        })
        
        # Delete all data
        result = self.manager.delete_user_data(user_id)
        
        assert result['status'] == 'deleted'
        assert result['user_id'] == user_id
        assert result['deleted_records']['consent_records'] == 1
        
        # Verify data is gone
        consent = self.manager.get_latest_consent(user_id)
        assert consent is None
    
    def test_consent_with_no_existing_user(self):
        """Test consent creation for non-existing user."""
        user_id = "new_consent_user"
        
        # Should create user automatically when saving consent
        consent_id = self.manager.save_consent(user_id, {
            'behavioralTracking': True,
            'profileStorage': True,
            'continuousLearning': False
        })
        
        assert consent_id is not None
        
        # Verify user was created
        result = self.manager.get_latest_consent(user_id)
        assert result is not None


class TestBehavioralPersonalityDecoder:
    """Test suite for BehavioralPersonalityDecoder with cultural context."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup decoder instance."""
        from neuro_controller import BehavioralPersonalityDecoder
        self.decoder = BehavioralPersonalityDecoder()
    
    def test_default_cultural_context(self):
        """Test decoder uses default cultural context."""
        assert self.decoder.cultural_context == 'default'
    
    def test_set_cultural_context(self):
        """Test setting cultural context."""
        result = self.decoder.set_cultural_context('east_asian')
        assert result == True
        assert self.decoder.cultural_context == 'east_asian'
    
    def test_invalid_cultural_context(self):
        """Test setting invalid cultural context."""
        result = self.decoder.set_cultural_context('invalid_culture')
        assert result == False
        assert self.decoder.cultural_context != 'invalid_culture'
    
    def test_decode_basic_profile(self):
        """Test basic profile decoding."""
        profile = {
            'pathEfficiency': 0.8,
            'avgDecisionLatency': 2000,
            'revisionRate': 1,
            'contextualChoices': {
                'aesthetics': 'Cyber/Industrial'
            }
        }
        
        result = self.decoder.decode(profile)
        
        assert 'synthetic_theta' in result
        assert 'synthetic_beta' in result
        assert 'traits' in result
        assert 'weights' in result['traits']
    
    def test_cultural_archetype_generation(self):
        """Test cultural archetype is generated."""
        profile = {
            'pathEfficiency': 0.9,
            'avgDecisionLatency': 3000,
            'revisionRate': 2,
            'culturalContext': 'east_asian'
        }
        
        result = self.decoder.decode(profile)
        
        assert 'cultural_archetype' in result['traits']
    
    def test_available_cultures(self):
        """Test getting available cultures."""
        cultures = self.decoder.get_available_cultures()
        
        assert isinstance(cultures, list)
        assert len(cultures) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
