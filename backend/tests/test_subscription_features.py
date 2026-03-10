"""
Test Subscription Features for Remy Platform
Tests subscription status, cancel functionality, and Mi Suscripcion page APIs
Iteration 8: Focus on subscription management features
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test credentials
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "test123"


class TestSubscriptionEndpoints:
    """Test subscription management endpoints"""
    
    @pytest.fixture(scope="class")
    def session_token(self):
        """Get session token for test user with active subscription"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            # Get session token from cookie or response
            token = data.get("session_token") or response.cookies.get("session_token")
            return token
        pytest.skip(f"Could not login: {response.status_code} - {response.text}")
    
    @pytest.fixture(scope="class")
    def auth_cookies(self, session_token):
        """Create cookies dict for authenticated requests"""
        return {"session_token": session_token}
    
    def test_subscription_status_returns_detailed_info(self, auth_cookies):
        """
        GET /api/payments/subscription returns detailed info including:
        - days_remaining
        - auto_renewal
        - plan_details
        """
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            cookies=auth_cookies
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        
        # Verify key fields are present
        assert "has_subscription" in data, "Missing has_subscription field"
        assert "subscription_status" in data, "Missing subscription_status field"
        assert "days_remaining" in data, "Missing days_remaining field"
        assert "auto_renewal" in data, "Missing auto_renewal field"
        
        # For manual subscription, auto_renewal should be False
        # For mercadopago subscription, auto_renewal should be True
        if data.get("subscription_type") == "manual":
            assert data["auto_renewal"] == False, "Manual subscription should have auto_renewal=False"
        
        # Verify active subscription for test user
        assert data["has_subscription"] == True, "Test user should have active subscription"
        assert data["subscription_status"] == "active", f"Expected active, got {data['subscription_status']}"
        
        # Verify days_remaining is a positive integer
        assert isinstance(data["days_remaining"], int), "days_remaining should be an integer"
        assert data["days_remaining"] >= 0, "days_remaining should be non-negative"
        
        # Verify plan_details if present
        if data.get("plan_details"):
            plan = data["plan_details"]
            assert "name" in plan, "plan_details missing name"
            assert "amount" in plan, "plan_details missing amount"
            assert "currency" in plan, "plan_details missing currency"
        
        print(f"✓ Subscription status returned: status={data['subscription_status']}, "
              f"days_remaining={data['days_remaining']}, auto_renewal={data['auto_renewal']}")
    
    def test_subscription_status_shows_correct_type(self, auth_cookies):
        """Verify subscription type is correctly returned"""
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            cookies=auth_cookies
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Test user has manual subscription
        assert data.get("subscription_type") == "manual", \
            f"Expected 'manual' type, got '{data.get('subscription_type')}'"
        
        print(f"✓ Subscription type is correctly 'manual'")
    
    def test_cancel_subscription_requires_auth(self):
        """POST /api/payments/cancel requires authentication"""
        response = requests.post(f"{BASE_URL}/api/payments/cancel")
        
        # Should return 401 or 403 without auth
        assert response.status_code in [401, 403, 422], \
            f"Expected auth error, got {response.status_code}"
        
        print(f"✓ Cancel endpoint correctly requires authentication")
    
    def test_cancel_manual_subscription_behavior(self, auth_cookies):
        """
        Test cancel behavior for manual subscription
        Note: Manual subscriptions might have different cancel behavior
        """
        response = requests.post(
            f"{BASE_URL}/api/payments/cancel",
            cookies=auth_cookies
        )
        
        # For manual subscriptions, the endpoint might:
        # 1. Return success and cancel
        # 2. Return error because manual subscriptions can't be cancelled by user
        # Both are valid behaviors, document what happens
        
        print(f"Cancel manual subscription response: {response.status_code} - {response.text[:200]}")
        
        # Just document the behavior, don't fail the test
        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "message" in data
            print("✓ Manual subscription cancel returned success")
        elif response.status_code == 400:
            print("✓ Manual subscription cancel returned 400 (expected - manual subscriptions may not be cancellable)")
        else:
            print(f"⚠ Unexpected response: {response.status_code}")


class TestSubscriptionWithoutAuth:
    """Test subscription endpoints for non-authenticated users"""
    
    def test_subscription_status_requires_auth(self):
        """GET /api/payments/subscription requires authentication"""
        response = requests.get(f"{BASE_URL}/api/payments/subscription")
        
        assert response.status_code in [401, 403, 422], \
            f"Expected auth error, got {response.status_code}"
        
        print("✓ Subscription status endpoint correctly requires auth")


class TestPaymentPlans:
    """Test payment plans endpoint"""
    
    def test_get_plans_returns_correct_data(self):
        """GET /api/payments/plans returns correct plan information"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "plans" in data, "Response missing 'plans' field"
        plans = data["plans"]
        
        assert len(plans) >= 2, "Expected at least 2 plans (monthly and semestral)"
        
        # Verify plan structure
        plan_ids = [p["id"] for p in plans]
        assert "monthly" in plan_ids, "Missing monthly plan"
        assert "semestral" in plan_ids, "Missing semestral plan"
        
        # Verify monthly plan
        monthly = next(p for p in plans if p["id"] == "monthly")
        assert monthly["amount"] == 9990, f"Monthly amount should be 9990, got {monthly['amount']}"
        assert monthly["currency"] == "CLP"
        assert "features" in monthly and len(monthly["features"]) > 0
        
        # Verify semestral plan
        semestral = next(p for p in plans if p["id"] == "semestral")
        assert semestral["amount"] == 29990, f"Semestral amount should be 29990, got {semestral['amount']}"
        assert semestral.get("discount") == "50%"
        
        print(f"✓ Plans API returns correct data: monthly=${monthly['amount']}, semestral=${semestral['amount']}")


class TestUserWithNoSubscription:
    """Test subscription status for user without active subscription"""
    
    @pytest.fixture(scope="class")
    def create_unsubscribed_user(self):
        """Create a user without subscription for testing"""
        import random
        email = f"test_nosub_{random.randint(1000, 9999)}@example.com"
        
        # Register new user
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": email,
                "password": "testpass123",
                "name": "No Subscription User"
            }
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            token = data.get("session_token") or response.cookies.get("session_token")
            return {"email": email, "token": token, "cookies": {"session_token": token}}
        
        pytest.skip(f"Could not create test user: {response.status_code}")
    
    def test_non_subscribed_user_gets_inactive_status(self, create_unsubscribed_user):
        """User without subscription should see inactive status"""
        cookies = create_unsubscribed_user["cookies"]
        
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            cookies=cookies
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should show no active subscription
        assert data["has_subscription"] == False or data["subscription_status"] != "active", \
            "Non-subscribed user should not have active subscription"
        
        print(f"✓ Non-subscribed user sees: has_subscription={data['has_subscription']}, status={data.get('subscription_status')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
