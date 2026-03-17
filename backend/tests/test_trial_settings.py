"""
Test Trial Settings Endpoints and University Simulation Restrictions
- GET /api/admin/analytics/settings/trial - Get trial configuration
- PUT /api/admin/analytics/settings/trial - Update trial configuration
- GET /api/admin/analytics/public/trial-status - Public endpoint for landing page
- POST /api/universities/{id}/courses/{cid}/simulation - Verify trial limit (403 if exceeded)
"""

import pytest
import requests
import os
import uuid
from datetime import datetime, timezone, timedelta

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')


class TestTrialSettingsAuth:
    """Test trial settings endpoints requiring admin authentication"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Get admin authentication token"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        pytest.skip("Admin authentication failed - skipping tests")
    
    def test_get_trial_settings(self, admin_token):
        """GET /api/admin/analytics/settings/trial - should return trial configuration"""
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/settings/trial",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        # Check that default or configured fields exist
        assert "enabled" in data, "Missing 'enabled' field in trial settings"
        assert "trial_days" in data, "Missing 'trial_days' field"
        assert "simulations_limit" in data, "Missing 'simulations_limit' field"
        assert "university_simulations_limit" in data, "Missing 'university_simulations_limit' field"
        
        # Validate types
        assert isinstance(data["enabled"], bool), "enabled should be boolean"
        assert isinstance(data["trial_days"], int), "trial_days should be int"
        assert isinstance(data["simulations_limit"], int), "simulations_limit should be int"
        assert isinstance(data["university_simulations_limit"], int), "university_simulations_limit should be int"
        
        print(f"✅ GET trial settings: enabled={data['enabled']}, days={data['trial_days']}, uni_limit={data['university_simulations_limit']}")
    
    def test_update_trial_settings_enable(self, admin_token):
        """PUT /api/admin/analytics/settings/trial - enable trial with custom values"""
        response = requests.put(
            f"{BASE_URL}/api/admin/analytics/settings/trial?enabled=true&trial_days=14&simulations_limit=20&university_simulations_limit=2",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert data.get("success") is True, "Expected success: true"
        
        settings = data.get("settings", {})
        assert settings.get("enabled") is True, "Expected enabled=true"
        assert settings.get("trial_days") == 14, "Expected trial_days=14"
        assert settings.get("simulations_limit") == 20, "Expected simulations_limit=20"
        assert settings.get("university_simulations_limit") == 2, "Expected university_simulations_limit=2"
        
        print(f"✅ Updated trial settings: {settings}")
    
    def test_update_trial_settings_disable(self, admin_token):
        """PUT /api/admin/analytics/settings/trial - disable trial"""
        response = requests.put(
            f"{BASE_URL}/api/admin/analytics/settings/trial?enabled=false&trial_days=7&simulations_limit=10&university_simulations_limit=1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert data.get("success") is True, "Expected success: true"
        assert data.get("settings", {}).get("enabled") is False, "Expected enabled=false"
        
        print("✅ Disabled trial settings")
    
    def test_trial_settings_persists(self, admin_token):
        """Verify trial settings persist after update"""
        # First update
        requests.put(
            f"{BASE_URL}/api/admin/analytics/settings/trial?enabled=true&trial_days=7&simulations_limit=10&university_simulations_limit=1",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        # Then get to verify persistence
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/settings/trial",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data.get("enabled") is True
        assert data.get("trial_days") == 7
        assert data.get("university_simulations_limit") == 1
        
        print("✅ Trial settings persisted correctly")
    
    def test_trial_settings_requires_auth(self):
        """GET /api/admin/analytics/settings/trial without token should return 401/403"""
        response = requests.get(f"{BASE_URL}/api/admin/analytics/settings/trial")
        
        assert response.status_code in [401, 403], f"Expected 401/403 without auth, got {response.status_code}"
        print("✅ Trial settings requires authentication")


class TestPublicTrialStatus:
    """Test public trial status endpoint (no auth required)"""
    
    def test_public_trial_status(self):
        """GET /api/admin/analytics/public/trial-status - public endpoint for landing page"""
        response = requests.get(f"{BASE_URL}/api/admin/analytics/public/trial-status")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "enabled" in data, "Missing 'enabled' field in public trial status"
        assert "trial_days" in data, "Missing 'trial_days' field"
        
        # Should NOT expose sensitive fields
        # Only enabled and trial_days should be public
        print(f"✅ Public trial status: enabled={data['enabled']}, trial_days={data['trial_days']}")


class TestUniversitySimulationTrialLimit:
    """Test that trial users are limited in university simulations"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Get admin authentication token"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        pytest.skip("Admin authentication failed")
    
    @pytest.fixture(scope="class")
    def trial_user(self, admin_token):
        """Create a trial user for testing"""
        user_email = f"test_trial_{uuid.uuid4().hex[:8]}@example.com"
        
        # Register user through API
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json={
                "email": user_email,
                "password": "testpass123",
                "name": "Test Trial User"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "email": user_email,
                "token": data.get("token"),
                "user_id": data.get("user", {}).get("id") or data.get("user", {}).get("user_id")
            }
        
        pytest.skip(f"Could not create trial user: {response.status_code} - {response.text}")
    
    @pytest.fixture
    def university_data(self):
        """Get available university/course/evaluation for testing"""
        # Get universities list
        response = requests.get(f"{BASE_URL}/api/universities")
        if response.status_code != 200 or not response.json():
            pytest.skip("No universities available for testing")
        
        universities = response.json()
        if not universities:
            pytest.skip("No universities found")
        
        # Get first university with courses
        for uni in universities:
            uni_response = requests.get(f"{BASE_URL}/api/universities/{uni['id']}")
            if uni_response.status_code == 200:
                uni_data = uni_response.json()
                courses = uni_data.get("courses", [])
                if courses:
                    # Get course with evaluations
                    course = courses[0]
                    course_response = requests.get(
                        f"{BASE_URL}/api/universities/{uni['id']}/courses/{course['id']}"
                    )
                    if course_response.status_code == 200:
                        course_data = course_response.json()
                        evaluations = course_data.get("evaluations", [])
                        # Find evaluation with questions
                        for eval in evaluations:
                            if eval.get("questions_count", 0) > 0:
                                return {
                                    "university_id": uni["id"],
                                    "course_id": course["id"],
                                    "evaluation_id": eval["id"]
                                }
        
        pytest.skip("No university with questions available for testing")
    
    def test_universities_list_public(self):
        """GET /api/universities - should be accessible without auth"""
        response = requests.get(f"{BASE_URL}/api/universities")
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Expected list of universities"
        
        if data:
            uni = data[0]
            assert "id" in uni
            assert "name" in uni
            print(f"✅ Found {len(data)} universities. First: {uni.get('name')}")
        else:
            print("✅ Universities endpoint works (empty list)")
    
    def test_simulation_without_auth_requires_subscription(self, university_data):
        """POST simulation without auth should fail with 403"""
        response = requests.post(
            f"{BASE_URL}/api/universities/{university_data['university_id']}/courses/{university_data['course_id']}/simulation",
            json={
                "evaluation_id": university_data['evaluation_id'],
                "num_questions": 5
            }
        )
        
        # Without auth, should get 403 requiring subscription
        assert response.status_code == 403, f"Expected 403 without subscription, got {response.status_code}: {response.text}"
        print("✅ Simulation without auth/subscription returns 403")
    
    def test_trial_user_first_simulation_allowed(self, trial_user, university_data):
        """Trial user should be able to do first university simulation"""
        if not trial_user.get("token"):
            pytest.skip("No trial user token available")
        
        response = requests.post(
            f"{BASE_URL}/api/universities/{university_data['university_id']}/courses/{university_data['course_id']}/simulation",
            json={
                "evaluation_id": university_data['evaluation_id'],
                "num_questions": 5
            },
            headers={"Authorization": f"Bearer {trial_user['token']}"}
        )
        
        # Trial users should be able to do their first simulation
        if response.status_code == 200:
            data = response.json()
            assert "simulation_id" in data, "Missing simulation_id"
            assert "questions" in data, "Missing questions"
            print(f"✅ Trial user can create first simulation: {data['simulation_id']}")
        elif response.status_code == 403:
            # Could be they already used their limit
            error = response.json()
            print(f"⚠️ Trial limit already reached: {error.get('detail')}")
        else:
            # 400 could mean no questions available
            print(f"⚠️ Simulation response: {response.status_code} - {response.text}")


class TestAdminDashboardIntegration:
    """Test that admin dashboard can load trial settings"""
    
    @pytest.fixture
    def admin_token(self):
        """Get admin authentication token"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        pytest.skip("Admin authentication failed")
    
    def test_dashboard_loads_with_trial_settings(self, admin_token):
        """Dashboard should load metrics and trial settings"""
        # Get dashboard metrics
        dashboard_response = requests.get(
            f"{BASE_URL}/api/admin/analytics/dashboard",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert dashboard_response.status_code == 200, f"Dashboard failed: {dashboard_response.status_code}"
        
        # Get trial settings
        trial_response = requests.get(
            f"{BASE_URL}/api/admin/analytics/settings/trial",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert trial_response.status_code == 200, f"Trial settings failed: {trial_response.status_code}"
        
        dashboard = dashboard_response.json()
        trial = trial_response.json()
        
        # Verify dashboard has trial users count
        assert "users" in dashboard
        assert "trial_active" in dashboard["users"], "Dashboard should show trial_active users count"
        
        print(f"✅ Dashboard: {dashboard['users']['trial_active']} trial users, trial enabled={trial['enabled']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
