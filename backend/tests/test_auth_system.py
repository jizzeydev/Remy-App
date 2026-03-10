"""
Test suite for Remy Authentication System
Testing: Email/password auth, user session management, admin user management
Features tested:
- POST /api/auth/register - Email/password registration
- POST /api/auth/login - Email/password login
- GET /api/auth/me - Get current user from session
- POST /api/auth/logout - Logout and clear session
- GET /api/admin/users - Admin list users (with filters)
- GET /api/admin/users/stats - Admin user statistics
- POST /api/admin/users/grant-access - Admin grant manual access
- GET /api/payments/plans - Payment plans listing
"""
import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test unique identifier to avoid conflicts
TEST_PREFIX = f"TEST_{uuid.uuid4().hex[:6]}_"


class TestEmailAuthentication:
    """Test email/password authentication endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data"""
        self.test_email = f"{TEST_PREFIX}user@example.com"
        self.test_password = "Test123456"
        self.test_name = f"{TEST_PREFIX}User"
        
    def test_register_new_user(self):
        """Test registering a new user with email/password"""
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": self.test_email,
                "password": self.test_password,
                "name": self.test_name
            }
        )
        
        assert response.status_code == 200, f"Registration failed: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "session_token" in data, "session_token missing from response"
        assert "user" in data, "user data missing from response"
        
        # Verify user data
        user = data["user"]
        assert user["email"] == self.test_email.lower()
        assert user["name"] == self.test_name
        assert "user_id" in user
        assert user["subscription_status"] == "inactive"
        
        print(f"✓ Registration successful for {self.test_email}")
        return data["session_token"]
    
    def test_register_duplicate_email(self):
        """Test that duplicate email registration fails"""
        # First registration
        requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": f"{TEST_PREFIX}dupe@example.com",
                "password": "Test123456",
                "name": "Dupe Test"
            }
        )
        
        # Second registration with same email
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": f"{TEST_PREFIX}dupe@example.com",
                "password": "Test123456",
                "name": "Dupe Test"
            }
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        print("✓ Duplicate email registration rejected correctly")
    
    def test_login_with_valid_credentials(self):
        """Test login with correct email/password"""
        # First register
        register_email = f"{TEST_PREFIX}login@example.com"
        requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": register_email,
                "password": "Test123456",
                "name": "Login Test"
            }
        )
        
        # Then login
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": register_email,
                "password": "Test123456"
            }
        )
        
        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        
        assert "session_token" in data
        assert "user" in data
        assert data["user"]["email"] == register_email.lower()
        
        print("✓ Login with valid credentials successful")
        return data["session_token"]
    
    def test_login_with_wrong_password(self):
        """Test login with incorrect password"""
        # First register
        register_email = f"{TEST_PREFIX}wrongpw@example.com"
        requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": register_email,
                "password": "Test123456",
                "name": "Wrong PW Test"
            }
        )
        
        # Then try login with wrong password
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": register_email,
                "password": "WrongPassword"
            }
        )
        
        assert response.status_code == 401
        print("✓ Login with wrong password rejected correctly")
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent email"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": "nonexistent@nowhere.com",
                "password": "Test123456"
            }
        )
        
        assert response.status_code == 401
        print("✓ Login with non-existent email rejected correctly")


class TestSessionManagement:
    """Test session management endpoints"""
    
    def test_get_current_user_with_valid_token(self):
        """Test getting current user with valid session token"""
        # Register and get token
        test_email = f"{TEST_PREFIX}session@example.com"
        register_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": test_email,
                "password": "Test123456",
                "name": "Session Test"
            }
        )
        token = register_response.json()["session_token"]
        
        # Get current user
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200, f"Get me failed: {response.text}"
        user = response.json()
        
        assert user["email"] == test_email.lower()
        assert "user_id" in user
        assert "subscription_status" in user
        
        print("✓ Get current user with valid token successful")
    
    def test_get_current_user_without_token(self):
        """Test getting current user without any token"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        
        assert response.status_code == 401
        print("✓ Get current user without token rejected correctly")
    
    def test_get_current_user_with_invalid_token(self):
        """Test getting current user with invalid token"""
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": "Bearer invalid_token_12345"}
        )
        
        assert response.status_code == 401
        print("✓ Get current user with invalid token rejected correctly")
    
    def test_logout(self):
        """Test logout clears session"""
        # Register and get token
        test_email = f"{TEST_PREFIX}logout@example.com"
        register_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": test_email,
                "password": "Test123456",
                "name": "Logout Test"
            }
        )
        token = register_response.json()["session_token"]
        
        # Logout
        logout_response = requests.post(
            f"{BASE_URL}/api/auth/logout",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert logout_response.status_code == 200
        
        # Verify token no longer works
        me_response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert me_response.status_code == 401
        print("✓ Logout successful and session invalidated")


class TestAdminUserManagement:
    """Test admin user management endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup admin auth"""
        login_response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={
                "username": "admin",
                "password": "#Alex060625"
            }
        )
        assert login_response.status_code == 200, "Admin login failed"
        self.admin_token = login_response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.admin_token}"}
    
    def test_get_user_list(self):
        """Test getting list of all users"""
        response = requests.get(
            f"{BASE_URL}/api/admin/users",
            headers=self.headers
        )
        
        assert response.status_code == 200, f"Get users failed: {response.text}"
        data = response.json()
        
        assert "users" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data
        assert isinstance(data["users"], list)
        
        print(f"✓ Admin user list returned {data['total']} users")
    
    def test_get_user_list_with_filter(self):
        """Test filtering users by subscription status"""
        response = requests.get(
            f"{BASE_URL}/api/admin/users?status_filter=active",
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # All returned users should have active status
        for user in data["users"]:
            assert user.get("subscription_status") == "active"
        
        print(f"✓ Admin user filter returned {len(data['users'])} active users")
    
    def test_get_user_list_with_search(self):
        """Test searching users by email"""
        response = requests.get(
            f"{BASE_URL}/api/admin/users?search=test",
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        print(f"✓ Admin user search returned {len(data['users'])} users")
    
    def test_get_user_stats(self):
        """Test getting user statistics"""
        response = requests.get(
            f"{BASE_URL}/api/admin/users/stats",
            headers=self.headers
        )
        
        assert response.status_code == 200, f"Get stats failed: {response.text}"
        data = response.json()
        
        assert "total_users" in data
        assert "subscription_stats" in data
        assert "active" in data["subscription_stats"]
        assert "inactive" in data["subscription_stats"]
        assert "subscription_types" in data
        assert "mercadopago" in data["subscription_types"]
        assert "manual" in data["subscription_types"]
        assert "auth_providers" in data
        
        print(f"✓ Admin stats: {data['total_users']} total users, {data['subscription_stats']['active']} active")
    
    def test_grant_access_new_user(self):
        """Test granting access to a new user (creates user)"""
        test_email = f"{TEST_PREFIX}grant_new@example.com"
        
        response = requests.post(
            f"{BASE_URL}/api/admin/users/grant-access",
            headers=self.headers,
            json={
                "email": test_email,
                "name": "Granted User",
                "duration_months": 1
            }
        )
        
        assert response.status_code == 200, f"Grant access failed: {response.text}"
        data = response.json()
        
        assert data["success"] == True
        assert data["action"] == "created"
        assert data["email"] == test_email.lower()
        assert "subscription_end" in data
        
        print(f"✓ Grant access to new user successful - user created")
    
    def test_grant_access_existing_user(self):
        """Test granting access to an existing user"""
        # First create user
        test_email = f"{TEST_PREFIX}grant_existing@example.com"
        requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": test_email,
                "password": "Test123456",
                "name": "Existing User"
            }
        )
        
        # Then grant access
        response = requests.post(
            f"{BASE_URL}/api/admin/users/grant-access",
            headers=self.headers,
            json={
                "email": test_email,
                "duration_months": 1
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] == True
        assert data["action"] == "updated"
        
        print("✓ Grant access to existing user successful - subscription updated")
    
    def test_admin_endpoints_without_auth(self):
        """Test that admin endpoints require authentication"""
        response = requests.get(f"{BASE_URL}/api/admin/users")
        assert response.status_code == 401 or response.status_code == 403
        
        response = requests.get(f"{BASE_URL}/api/admin/users/stats")
        assert response.status_code == 401 or response.status_code == 403
        
        print("✓ Admin endpoints properly protected")


class TestPaymentPlans:
    """Test payment plans endpoint"""
    
    def test_get_payment_plans(self):
        """Test getting available payment plans (public endpoint)"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        
        assert response.status_code == 200, f"Get plans failed: {response.text}"
        data = response.json()
        
        assert "plans" in data
        plans = data["plans"]
        
        assert len(plans) >= 2  # At least monthly and semestral
        
        # Verify plan structure
        for plan in plans:
            assert "id" in plan
            assert "name" in plan
            assert "amount" in plan
            assert "currency" in plan
            assert "features" in plan
            assert isinstance(plan["features"], list)
        
        # Verify we have both monthly and semestral
        plan_ids = [p["id"] for p in plans]
        assert "monthly" in plan_ids
        assert "semestral" in plan_ids
        
        print(f"✓ Payment plans returned {len(plans)} plans")


class TestProtectedStudentRoutes:
    """Test that student routes require authentication"""
    
    def test_protected_routes_without_auth(self):
        """Test that certain routes redirect when not logged in - backend aspect"""
        # This is mainly frontend behavior, but we can verify the backend
        # returns 401 for protected endpoints
        
        # The /api/auth/me endpoint is the key one that frontend checks
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401
        
        print("✓ Auth endpoint properly returns 401 when not authenticated")


# Cleanup fixture to remove test users after all tests
@pytest.fixture(scope="module", autouse=True)
def cleanup_test_users():
    """Cleanup test users after all tests in this module"""
    yield
    # Note: In a real scenario, we'd have a cleanup endpoint
    # For now, test data with TEST_PREFIX can be identified and cleaned manually
    print(f"\n[INFO] Test users created with prefix: {TEST_PREFIX}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
