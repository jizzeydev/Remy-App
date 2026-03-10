"""
Tests for Admin User Management endpoints
- GET /api/admin/users - list all users with pagination
- GET /api/admin/users/stats - get user and subscription statistics
- GET /api/admin/users/revenue/summary - get revenue for date range
- GET /api/admin/users/revenue/monthly - get monthly revenue comparison
- POST /api/admin/users/grant-access - grant manual access
- POST /api/admin/users/{user_id}/revoke-access - revoke access
- POST /api/admin/users/{user_id}/extend-access - extend access
"""

import pytest
import requests
import os
from datetime import datetime, timedelta

# Get backend URL from environment
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
API_URL = f"{BASE_URL}/api"

# Admin credentials from env
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = '#Alex060625'  # From test request


class TestAdminAuth:
    """Tests for admin authentication"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200, f"Admin login failed: {response.text}"
        data = response.json()
        assert "access_token" in data, "No access_token in response"
        return data["access_token"]
    
    def test_admin_login_success(self):
        """Test admin login with correct credentials"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0
    
    def test_admin_login_invalid_credentials(self):
        """Test admin login with wrong credentials"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": "wrong", "password": "wrong"}
        )
        assert response.status_code == 401


class TestAdminUsersList:
    """Tests for GET /api/admin/users"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_list_users_success(self, admin_token):
        """Test listing users with valid admin token"""
        response = requests.get(
            f"{API_URL}/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "users" in data
        assert "total" in data
        assert "page" in data
        assert "limit" in data
        assert "pages" in data
        
        # Validate types
        assert isinstance(data["users"], list)
        assert isinstance(data["total"], int)
        assert data["total"] >= 0
    
    def test_list_users_with_pagination(self, admin_token):
        """Test pagination parameters"""
        response = requests.get(
            f"{API_URL}/admin/users?page=1&limit=5",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 5
        assert data["page"] == 1
    
    def test_list_users_with_status_filter(self, admin_token):
        """Test filtering by subscription status"""
        response = requests.get(
            f"{API_URL}/admin/users?status_filter=active",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # All returned users should have active status
        for user in data["users"]:
            assert user.get("subscription_status") == "active"
    
    def test_list_users_with_search(self, admin_token):
        """Test search by email/name"""
        response = requests.get(
            f"{API_URL}/admin/users?search=test",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
    
    def test_list_users_unauthorized(self):
        """Test listing users without token fails"""
        response = requests.get(f"{API_URL}/admin/users")
        assert response.status_code in [401, 403]
    
    def test_list_users_invalid_token(self):
        """Test listing users with invalid token fails"""
        response = requests.get(
            f"{API_URL}/admin/users",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


class TestAdminUserStats:
    """Tests for GET /api/admin/users/stats"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_get_stats_success(self, admin_token):
        """Test getting user statistics"""
        response = requests.get(
            f"{API_URL}/admin/users/stats",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "total_users" in data
        assert "subscription_stats" in data
        assert "subscription_types" in data
        assert "recent_registrations" in data
        
        # Validate subscription_stats structure
        sub_stats = data["subscription_stats"]
        assert "active" in sub_stats
        assert "inactive" in sub_stats
        assert "cancelled" in sub_stats
        assert "expired" in sub_stats
        
        # Validate subscription_types structure
        sub_types = data["subscription_types"]
        assert "mercadopago" in sub_types
        assert "manual" in sub_types
        
        # Validate types are integers
        assert isinstance(data["total_users"], int)
        assert isinstance(sub_stats["active"], int)
        assert isinstance(sub_types["manual"], int)


class TestAdminRevenueSummary:
    """Tests for GET /api/admin/users/revenue/summary"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_revenue_summary_default(self, admin_token):
        """Test revenue summary with default date range (current month)"""
        response = requests.get(
            f"{API_URL}/admin/users/revenue/summary",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "period" in data
        assert "start" in data["period"]
        assert "end" in data["period"]
        assert "total_revenue" in data
        assert "currency" in data
        assert "total_subscriptions" in data
        assert "revenue_by_plan" in data
        assert "daily_revenue" in data
        assert "average_per_subscription" in data
        
        # Validate types
        assert isinstance(data["total_revenue"], (int, float))
        assert isinstance(data["total_subscriptions"], int)
        assert data["currency"] == "CLP"
        assert isinstance(data["daily_revenue"], list)
    
    def test_revenue_summary_with_date_range(self, admin_token):
        """Test revenue summary with custom date range"""
        # Last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        response = requests.get(
            f"{API_URL}/admin/users/revenue/summary",
            headers={"Authorization": f"Bearer {admin_token}"},
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "period" in data
        assert "total_revenue" in data
    
    def test_revenue_summary_last_3_months(self, admin_token):
        """Test revenue summary for last 3 months"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        response = requests.get(
            f"{API_URL}/admin/users/revenue/summary",
            headers={"Authorization": f"Bearer {admin_token}"},
            params={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Revenue should be >= 0 (could be $0 if no paid subscriptions)
        assert data["total_revenue"] >= 0


class TestAdminMonthlyRevenue:
    """Tests for GET /api/admin/users/revenue/monthly"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_monthly_revenue_default(self, admin_token):
        """Test monthly revenue with default 6 months"""
        response = requests.get(
            f"{API_URL}/admin/users/revenue/monthly",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "monthly_data" in data
        assert "currency" in data
        assert data["currency"] == "CLP"
        
        # Validate monthly_data structure
        assert isinstance(data["monthly_data"], list)
        assert len(data["monthly_data"]) <= 6
        
        for month_data in data["monthly_data"]:
            assert "month" in month_data
            assert "month_name" in month_data
            assert "revenue" in month_data
            assert "subscriptions" in month_data
    
    def test_monthly_revenue_custom_months(self, admin_token):
        """Test monthly revenue with custom month count"""
        response = requests.get(
            f"{API_URL}/admin/users/revenue/monthly?months=3",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["monthly_data"]) <= 3


class TestAdminGrantAccess:
    """Tests for POST /api/admin/users/grant-access"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_grant_access_new_user(self, admin_token):
        """Test granting access to a new user"""
        test_email = f"TEST_grant_user_{datetime.now().timestamp()}@example.com"
        
        response = requests.post(
            f"{API_URL}/admin/users/grant-access",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "email": test_email,
                "name": "Test Grant User",
                "duration_months": 1
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Validate response
        assert data["success"] is True
        assert data["email"] == test_email.lower()
        assert "user_id" in data
        assert "subscription_end" in data
        assert "message" in data
        assert data["action"] in ["created", "updated"]
    
    def test_grant_access_missing_email(self, admin_token):
        """Test grant access without email fails"""
        response = requests.post(
            f"{API_URL}/admin/users/grant-access",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"duration_months": 1}
        )
        assert response.status_code == 422  # Validation error


class TestAdminExtendAccess:
    """Tests for POST /api/admin/users/{user_id}/extend-access"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_extend_access_existing_user(self, admin_token):
        """Test extending access for an existing user"""
        # First, get list of users to find one
        users_response = requests.get(
            f"{API_URL}/admin/users?status_filter=active&limit=1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        if users_response.status_code == 200 and users_response.json()["users"]:
            user_id = users_response.json()["users"][0]["user_id"]
            
            response = requests.post(
                f"{API_URL}/admin/users/{user_id}/extend-access?months=1",
                headers={"Authorization": f"Bearer {admin_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "new_end_date" in data
        else:
            pytest.skip("No active users to test extension")
    
    def test_extend_access_invalid_user(self, admin_token):
        """Test extending access for non-existent user"""
        response = requests.post(
            f"{API_URL}/admin/users/invalid_user_id_12345/extend-access?months=1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 404


class TestAdminRevokeAccess:
    """Tests for POST /api/admin/users/{user_id}/revoke-access"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Login as admin and get token"""
        response = requests.post(
            f"{API_URL}/admin/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        return response.json()["access_token"]
    
    def test_revoke_access_invalid_user(self, admin_token):
        """Test revoking access for non-existent user"""
        response = requests.post(
            f"{API_URL}/admin/users/invalid_user_id_12345/revoke-access",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
