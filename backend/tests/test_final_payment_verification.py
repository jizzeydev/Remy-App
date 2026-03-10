"""
FINAL Payment Verification Test Suite - Remy Platform
Tests production Mercado Pago integration for payment system before launch.

Mercado Pago Mode: PRODUCTION (APP_USR-* keys)
"""
import pytest
import requests
import os
from datetime import datetime

# Environment Setup
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test Users created via MongoDB
NOSUB_SESSION = "test_session_nosub_1773105967226"  # User without subscription
SUB_SESSION = "test_session_sub_1773105967823"  # User with active subscription
ADMIN_CREDENTIALS = {"username": "admin", "password": "#Alex060625"}


class TestProductionPaymentPlans:
    """Verify /api/payments/plans returns PRODUCTION keys and correct pricing"""
    
    def test_plans_endpoint_returns_200(self):
        """Plans endpoint accessible"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        assert response.status_code == 200
        print("✓ GET /api/payments/plans returns 200")
    
    def test_returns_production_public_key(self):
        """CRITICAL: Public key must be PRODUCTION (APP_USR-*)"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        assert "mercadopago_public_key" in data
        public_key = data["mercadopago_public_key"]
        assert public_key.startswith("APP_USR-"), f"Expected production key (APP_USR-*), got: {public_key[:20]}"
        print(f"✓ Production public key: {public_key[:30]}...")
    
    def test_monthly_plan_9990_clp(self):
        """Monthly plan: $9.990 CLP"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        monthly = next(p for p in data["plans"] if p["id"] == "monthly")
        assert monthly["amount"] == 9990, f"Expected 9990, got {monthly['amount']}"
        assert monthly["currency"] == "CLP"
        print(f"✓ Monthly: ${monthly['amount']} {monthly['currency']}")
    
    def test_semestral_plan_29990_clp_50_discount(self):
        """Semestral plan: $29.990 CLP (50% off from $59.940)"""
        response = requests.get(f"{BASE_URL}/api/payments/plans")
        data = response.json()
        
        semestral = next(p for p in data["plans"] if p["id"] == "semestral")
        assert semestral["amount"] == 29990
        assert semestral.get("original_amount") == 59940
        assert semestral.get("discount") == "50%"
        print(f"✓ Semestral: ${semestral['amount']} (50% off from ${semestral['original_amount']})")


class TestSubscriptionEndpointSecurity:
    """Test authentication requirements for subscription endpoints"""
    
    def test_subscribe_requires_auth(self):
        """POST /subscribe requires authentication"""
        response = requests.post(
            f"{BASE_URL}/api/payments/subscribe",
            json={"plan_id": "monthly", "card_token": "test"}
        )
        assert response.status_code in [401, 403]
        print("✓ POST /subscribe requires authentication (401/403)")
    
    def test_subscription_status_requires_auth(self):
        """GET /subscription requires authentication"""
        response = requests.get(f"{BASE_URL}/api/payments/subscription")
        assert response.status_code in [401, 403]
        print("✓ GET /subscription requires authentication (401/403)")
    
    def test_cancel_requires_auth(self):
        """POST /cancel requires authentication"""
        response = requests.post(f"{BASE_URL}/api/payments/cancel")
        assert response.status_code in [401, 403]
        print("✓ POST /cancel requires authentication (401/403)")


class TestSubscriptionStatusEndpoint:
    """Test GET /api/payments/subscription for logged users"""
    
    @pytest.fixture
    def nosub_headers(self):
        return {"Authorization": f"Bearer {NOSUB_SESSION}"}
    
    def test_returns_status_for_authenticated_user(self, nosub_headers):
        """Authenticated user gets subscription status"""
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            headers=nosub_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "has_subscription" in data
        assert "subscription_status" in data
        print(f"✓ Status: has_subscription={data['has_subscription']}, status={data['subscription_status']}")
    
    def test_inactive_user_has_subscription_false(self, nosub_headers):
        """User without subscription shows has_subscription=false"""
        response = requests.get(
            f"{BASE_URL}/api/payments/subscription",
            headers=nosub_headers
        )
        data = response.json()
        assert data["has_subscription"] == False
        assert data["subscription_status"] in ["inactive", None, ""]
        print("✓ Non-subscriber correctly shows inactive")


class TestSubscribeEndpoint:
    """Test POST /api/payments/subscribe validation"""
    
    @pytest.fixture
    def nosub_headers(self):
        return {"Authorization": f"Bearer {NOSUB_SESSION}"}
    
    def test_requires_plan_id_and_card_token(self, nosub_headers):
        """Subscribe requires both plan_id and card_token"""
        response = requests.post(
            f"{BASE_URL}/api/payments/subscribe",
            headers=nosub_headers,
            json={"plan_id": "monthly"}  # Missing card_token
        )
        assert response.status_code == 422  # Pydantic validation error
        print("✓ Missing card_token returns 422")
    
    def test_invalid_plan_returns_400(self, nosub_headers):
        """Invalid plan_id returns 400"""
        response = requests.post(
            f"{BASE_URL}/api/payments/subscribe",
            headers=nosub_headers,
            json={"plan_id": "invalid_plan", "card_token": "test"}
        )
        assert response.status_code == 400
        assert "Plan inválido" in response.json()["detail"]
        print("✓ Invalid plan_id returns 400 with message")
    
    def test_invalid_card_token_returns_error(self, nosub_headers):
        """Invalid card token returns 500 with 'Card token service not found'"""
        response = requests.post(
            f"{BASE_URL}/api/payments/subscribe",
            headers=nosub_headers,
            json={"plan_id": "monthly", "card_token": "invalid_token_123"}
        )
        # Expected: 500 with message about invalid card token
        assert response.status_code == 500
        detail = response.json()["detail"]
        assert "Card token" in detail or "token" in detail.lower()
        print(f"✓ Invalid card token returns 500: {detail[:50]}...")


class TestCancelEndpoint:
    """Test POST /api/payments/cancel"""
    
    @pytest.fixture
    def nosub_headers(self):
        return {"Authorization": f"Bearer {NOSUB_SESSION}"}
    
    def test_cancel_without_subscription_fails(self, nosub_headers):
        """Cancel without active subscription returns 400"""
        response = requests.post(
            f"{BASE_URL}/api/payments/cancel",
            headers=nosub_headers
        )
        assert response.status_code == 400
        assert "No tienes una suscripción activa" in response.json()["detail"]
        print("✓ Cancel without subscription returns 400 with message")


class TestWebhookEndpoint:
    """Test POST /api/payments/webhook/mercadopago"""
    
    def test_webhook_receives_and_acknowledges(self):
        """Webhook accepts POST and returns status:received"""
        response = requests.post(
            f"{BASE_URL}/api/payments/webhook/mercadopago",
            json={
                "action": "payment.created",
                "data": {"id": "12345", "status": "approved"}
            }
        )
        assert response.status_code == 200
        assert response.json()["status"] == "received"
        print("✓ Webhook returns {status: received}")
    
    def test_webhook_handles_subscription_events(self):
        """Webhook handles subscription_preapproval events"""
        response = requests.post(
            f"{BASE_URL}/api/payments/webhook/mercadopago",
            json={
                "action": "subscription_preapproval.authorized",
                "data": {"id": "preapproval_123", "status": "authorized"}
            }
        )
        assert response.status_code == 200
        print("✓ Webhook handles subscription events")


class TestAdminGrantAccess:
    """Test POST /api/admin/users/grant-access"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin JWT token"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json=ADMIN_CREDENTIALS
        )
        if response.status_code != 200:
            pytest.skip("Admin login failed")
        return response.json()["access_token"]
    
    def test_grant_access_requires_auth(self):
        """Grant access requires admin authentication"""
        response = requests.post(
            f"{BASE_URL}/api/admin/users/grant-access",
            json={"email": "test@test.com"}
        )
        assert response.status_code in [401, 403]
        print("✓ Grant access requires admin auth")
    
    def test_grant_access_creates_user(self, admin_token):
        """Admin can grant access to new email"""
        test_email = f"test_grant_{datetime.now().timestamp()}@test.com"
        
        response = requests.post(
            f"{BASE_URL}/api/admin/users/grant-access",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "email": test_email,
                "name": "Test Grant User",
                "duration_months": 1
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["email"] == test_email.lower()
        assert "user_id" in data
        print(f"✓ Admin granted access to {test_email}")


class TestAuthMeEndpoint:
    """Test GET /api/auth/me for user authentication"""
    
    def test_auth_me_without_token_fails(self):
        """Auth/me requires authentication"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code in [401, 403]
        print("✓ /api/auth/me requires authentication")
    
    def test_auth_me_with_valid_token(self):
        """Auth/me returns user data with valid token"""
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {NOSUB_SESSION}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "email" in data
        print(f"✓ Auth/me returns user: {data['email']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
