"""
API endpoint integration tests.
"""
import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_server import app


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test /health endpoint returns OK."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["controller"] == "ready"


class TestConsentEndpoints:
    """Test consent management endpoints."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_save_consent(self, client):
        """Test POST /api/user/{id}/consent endpoint."""
        user_id = "api_test_user_001"
        consent_data = {
            "consent_record": {
                "behavioralTracking": True,
                "profileStorage": True,
                "continuousLearning": False
            },
            "timestamp": "2026-01-14T15:00:00"
        }
        
        response = client.post(f"/api/user/{user_id}/consent", json=consent_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "saved"
        assert data["user_id"] == user_id
        assert "consent_id" in data
    
    def test_get_consent(self, client):
        """Test GET /api/user/{id}/consent endpoint."""
        user_id = "api_test_user_002"
        
        # First save consent
        consent_data = {
            "consent_record": {
                "behavioralTracking": True,
                "profileStorage": True,
                "continuousLearning": True
            },
            "timestamp": "2026-01-14T15:00:00"
        }
        client.post(f"/api/user/{user_id}/consent", json=consent_data)
        
        # Then retrieve it
        response = client.get(f"/api/user/{user_id}/consent")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "found"
        assert data["user_id"] == user_id
        assert "consent" in data
    
    def test_get_consent_no_user(self, client):
        """Test GET consent for non-existing user."""
        response = client.get("/api/user/non_existing_user_xyz/consent")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "no_consent"


class TestDataExportEndpoint:
    """Test GDPR data export endpoint."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_export_user_data(self, client):
        """Test GET /api/user/{id}/export endpoint."""
        user_id = "export_api_test_user"
        
        # Create some data first
        consent_data = {
            "consent_record": {
                "behavioralTracking": True,
                "profileStorage": True,
                "continuousLearning": True
            },
            "timestamp": "2026-01-14T15:00:00"
        }
        client.post(f"/api/user/{user_id}/consent", json=consent_data)
        
        # Export data
        response = client.get(f"/api/user/{user_id}/export")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "export_metadata" in data
        assert data["export_metadata"]["user_id"] == user_id
        assert "user_profile" in data
        assert "behavioral_sessions" in data
        assert "consent_history" in data
        assert "data_summary" in data


class TestDataDeletionEndpoint:
    """Test GDPR data deletion endpoint."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_delete_user_data(self, client):
        """Test DELETE /api/user/{id} endpoint."""
        user_id = "delete_api_test_user"
        
        # Create some data first
        consent_data = {
            "consent_record": {
                "behavioralTracking": True,
                "profileStorage": True,
                "continuousLearning": True
            },
            "timestamp": "2026-01-14T15:00:00"
        }
        client.post(f"/api/user/{user_id}/consent", json=consent_data)
        
        # Delete data
        response = client.delete(f"/api/user/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "deleted"
        assert data["user_id"] == user_id
        
        # Verify deletion
        verify_response = client.get(f"/api/user/{user_id}/consent")
        assert verify_response.json()["status"] == "no_consent"


class TestBehavioralEndpoints:
    """Test behavioral processing endpoints."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_behavior_processing(self, client):
        """Test POST /api/behavior endpoint."""
        profile = {
            "pathEfficiency": 0.8,
            "avgDecisionLatency": 2000,
            "revisionRate": 1,
            "contextualChoices": {
                "aesthetics": "Cyber/Industrial"
            }
        }
        
        response = client.post("/api/behavior", json=profile)
        
        assert response.status_code == 200
        data = response.json()
        assert "synthetic_theta" in data
        assert "synthetic_beta" in data
        assert "behavioral_traits" in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
