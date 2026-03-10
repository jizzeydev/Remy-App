"""
Test suite for Remy Platform - Payment and Subscription Features
Tests subscription flows, payment endpoints, and user access control
"""
import pytest
import requests
import os
from datetime import datetime

# Get base URL from environment
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test session for non-subscriber user
TEST_SESSION_TOKEN = "test_session_1773102170118"
TEST_USER_ID = "test-user-1773102170118"


class TestPaymentPlansAPI:
    """Test /api/payments/plans endpoint"""
    
    def test_get_plans_returns_success(self):
        """Plans endpoint should return 200"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        print("✓ GET /api/payments/plans returns 200")
    
    def test_get_plans_returns_two_plans(self):
        """Should return both monthly and semestral plans"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        assert "plans" in data, "Response missing 'plans' key"
        assert len(data["plans"]) == 2, f"Expected 2 plans, got {len(data['plans'])}"
        
        plan_ids = [p["id"] for p in data["plans"]]
        assert "monthly" in plan_ids, "Missing 'monthly' plan"
        assert "semestral" in plan_ids, "Missing 'semestral' plan"
        print("✓ Plans API returns monthly and semestral plans")
    
    def test_monthly_plan_correct_price(self):
        """Monthly plan should be 9990 CLP"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        monthly = next(p for p in data["plans"] if p["id"] == "monthly")
        assert monthly["amount"] == 9990, f"Expected 9990, got {monthly['amount']}"
        assert monthly["currency"] == "CLP", f"Expected CLP, got {monthly['currency']}"
        print(f"✓ Monthly plan: ${monthly['amount']} {monthly['currency']}/mes")
    
    def test_semestral_plan_correct_price(self):
        """Semestral plan should be 29990 CLP with discount"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        semestral = next(p for p in data["plans"] if p["id"] == "semestral")
        assert semestral["amount"] == 29990, f"Expected 29990, got {semestral['amount']}"
        assert semestral.get("discount") == "50%", f"Expected 50% discount, got {semestral.get('discount')}"
        assert semestral.get("original_amount") == 59940, f"Expected original 59940, got {semestral.get('original_amount')}"
        print(f"✓ Semestral plan: ${semestral['amount']} (50% OFF from ${semestral.get('original_amount')})")
    
    def test_plans_include_mercadopago_public_key(self):
        """Response should include MercadoPago public key"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        assert "mercadopago_public_key" in data, "Missing mercadopago_public_key"
        assert data["mercadopago_public_key"].startswith("TEST-"), "Public key should start with TEST-"
        print(f"✓ MercadoPago public key present: {data['mercadopago_public_key'][:20]}...")
    
    def test_plans_have_features(self):
        """Each plan should have feature list"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        for plan in data["plans"]:
            assert "features" in plan, f"Plan {plan['id']} missing features"
            assert len(plan["features"]) > 0, f"Plan {plan['id']} has no features"
        print("✓ All plans have features list")


class TestSubscriptionEndpoints:
    """Test subscription-related endpoints"""
    
    def test_subscribe_requires_authentication(self):
        """Subscribe endpoint should require auth"""
        response = requests.post(
            f"{BASE_URL}/api/payments/subscribe",
            json={"plan_id": "monthly", "card_token": "test_token"}
        )
        # Should return 401 or 403 without auth
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
        print("✓ POST /api/payments/subscribe requires authentication")
    
    def test_subscription_status_requires_authentication(self):
        """Get subscription status should require auth"""
        response = requests.get(f"{BASE_URL}/api/payments/subscription")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
        print("✓ GET /api/payments/subscription requires authentication")
    
    def test_cancel_subscription_requires_authentication(self):
        """Cancel subscription should require auth"""
        response = requests.post(f"{BASE_URL}/api/payments/cancel")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
        print("✓ POST /api/payments/cancel requires authentication")


class TestAuthenticatedSubscription:
    """Test subscription endpoints with authenticated user"""
    
    @pytest.fixture
    def auth_headers(self):
        return {"Authorization": f"Bearer {TEST_SESSION_TOKEN}"}
    
    def test_get_subscription_status_with_auth(self, auth_headers):
        """Should return subscription status for authenticated user"""
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            headers=auth_headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "has_subscription" in data, "Missing has_subscription field"
        assert "subscription_status" in data, "Missing subscription_status field"
        print(f"✓ Subscription status: has_subscription={data['has_subscription']}, status={data['subscription_status']}")
    
    def test_user_without_subscription_shows_inactive(self, auth_headers):
        """Test user without subscription should have inactive status"""
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            headers=auth_headers
        )
        data = response.json()
        
        assert data["has_subscription"] == False, "User should not have active subscription"
        assert data["subscription_status"] in ["inactive", None, ""], f"Expected inactive, got {data['subscription_status']}"
        print("✓ Non-subscriber user correctly shows inactive subscription")
    
    def test_subscribe_with_invalid_plan_fails(self, auth_headers):
        """Subscribe with invalid plan should fail"""
        response = requests.post(
            f"{BASE_URL}/api/payments/subscribe",
            headers=auth_headers,
            json={"plan_id": "invalid_plan", "card_token": "test_token"}
        )
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        print("✓ Invalid plan_id correctly rejected with 400")
    
    def test_subscribe_missing_card_token_fails(self, auth_headers):
        """Subscribe without card token should fail"""
        response = requests.post(
            f"{BASE_URL}/api/payments/subscribe",
            headers=auth_headers,
            json={"plan_id": "monthly"}
        )
        assert response.status_code == 422, f"Expected 422 (validation error), got {response.status_code}"
        print("✓ Missing card_token correctly rejected with 422")


class TestAuthFlows:
    """Test authentication flows with redirect"""
    
    def test_auth_me_without_token_fails(self):
        """Auth/me should fail without token"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
        print("✓ /api/auth/me requires authentication")
    
    def test_auth_me_with_valid_token(self):
        """Auth/me should return user data with valid token"""
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {TEST_SESSION_TOKEN}"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "user_id" in data or "email" in data, "User data should contain user_id or email"
        print(f"✓ Auth/me returns user data: {data.get('email', 'N/A')}")


class TestCoursesAPI:
    """Test courses API for Biblioteca"""
    
    def test_courses_list_accessible(self):
        """Courses endpoint should be accessible"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"✓ Courses API returns {len(response.json())} courses")


class TestWebhook:
    """Test webhook endpoint (basic availability)"""
    
    def test_webhook_accepts_post(self):
        """Webhook should accept POST requests"""
        response = requests.post(
            f"{BASE_URL}/api/payments/webhook/mercadopago",
            json={"action": "test", "data": {}}
        )
        # Should return 200 (webhooks should always acknowledge)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ MercadoPago webhook endpoint accessible")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
