"""
Tests for Session Persistence feature
Testing:
- Token storage in localStorage after login
- /auth/me endpoint accepts Bearer token from Authorization header
- Session token returned on login/register
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')

# Test credentials from main agent
TEST_USER_EMAIL = "demo@seremonta.cl"
TEST_USER_PASSWORD = "demo123"


class TestSessionPersistence:
    """Test session persistence functionality"""
    
    def test_login_returns_session_token(self):
        """Login should return session_token in response for localStorage storage"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
        )
        
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        
        # CRITICAL: session_token must be returned for localStorage persistence
        assert "session_token" in data, "session_token not in login response"
        assert data["session_token"].startswith("sess_"), f"Invalid session token format: {data.get('session_token')}"
        
        # User should also be returned
        assert "user" in data, "user not in login response"
        assert data["user"]["email"] == TEST_USER_EMAIL
        print(f"✅ Login returns session_token: {data['session_token'][:20]}...")
    
    def test_auth_me_with_bearer_token(self):
        """GET /auth/me should work with Bearer token in Authorization header"""
        # First login to get token
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
        )
        assert login_response.status_code == 200
        session_token = login_response.json()["session_token"]
        
        # Test /auth/me with Bearer token
        me_response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        
        assert me_response.status_code == 200, f"/auth/me failed: {me_response.text}"
        user_data = me_response.json()
        
        assert user_data["email"] == TEST_USER_EMAIL
        assert "user_id" in user_data
        print(f"✅ /auth/me with Bearer token works: {user_data['email']}")
    
    def test_auth_me_without_token_fails(self):
        """GET /auth/me without token should return 401"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("✅ /auth/me without token correctly returns 401")
    
    def test_auth_me_with_invalid_token_fails(self):
        """GET /auth/me with invalid token should return 401"""
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": "Bearer invalid_token_12345"}
        )
        
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        print("✅ /auth/me with invalid token correctly returns 401")
    
    def test_session_persists_across_requests(self):
        """Same session token should work for multiple requests"""
        # Login to get token
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
        )
        session_token = login_response.json()["session_token"]
        
        # Make multiple requests with same token
        for i in range(3):
            response = requests.get(
                f"{BASE_URL}/api/auth/me",
                headers={"Authorization": f"Bearer {session_token}"}
            )
            assert response.status_code == 200, f"Request {i+1} failed"
        
        print("✅ Session token persists across multiple requests")
    
    def test_logout_invalidates_token(self):
        """After logout, token should no longer work"""
        # Login to get token
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
        )
        session_token = login_response.json()["session_token"]
        
        # Verify token works
        me_response1 = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        assert me_response1.status_code == 200
        
        # Logout
        logout_response = requests.post(
            f"{BASE_URL}/api/auth/logout",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        assert logout_response.status_code == 200
        
        # Token should no longer work
        me_response2 = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        assert me_response2.status_code == 401, f"Token should be invalid after logout"
        print("✅ Logout correctly invalidates session token")


class TestRegisterSessionToken:
    """Test session token on registration"""
    
    def test_register_returns_session_token(self):
        """Register should also return session_token"""
        import uuid
        test_email = f"test_session_{uuid.uuid4().hex[:8]}@test.com"
        
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": test_email,
                "password": "test123456",
                "name": "Test Session User"
            }
        )
        
        assert response.status_code == 200, f"Registration failed: {response.text}"
        data = response.json()
        
        # CRITICAL: session_token must be returned for localStorage persistence
        assert "session_token" in data, "session_token not in register response"
        assert data["session_token"].startswith("sess_")
        
        # Clean up - delete test user
        try:
            import os
            from pymongo import MongoClient
            client = MongoClient(os.environ.get("MONGO_URL", "mongodb://localhost:27017"))
            db = client["test_database"]
            db.users.delete_one({"email": test_email})
            db.user_sessions.delete_one({"session_token": data["session_token"]})
        except:
            pass
        
        print(f"✅ Register returns session_token for new user")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
