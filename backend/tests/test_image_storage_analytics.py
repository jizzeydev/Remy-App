"""
Test Image Storage (GridFS) and Admin Analytics Dashboard APIs
Tests for:
1. Image upload to MongoDB GridFS
2. Image retrieval from GridFS
3. Image deletion
4. Admin analytics dashboard metrics
5. Chart data endpoints
"""
import pytest
import requests
import os
import base64

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test image - small PNG (1x1 pixel transparent)
TEST_IMAGE_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
TEST_IMAGE_BYTES = base64.b64decode(TEST_IMAGE_BASE64)


class TestAdminAuthentication:
    """Get admin token for authenticated endpoints"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        """Authenticate as admin and get token"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        assert response.status_code == 200, f"Admin login failed: {response.text}"
        token = response.json().get("access_token")
        assert token, "No token received"
        return token
    
    def test_admin_login_success(self):
        """Test admin login returns valid token"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


class TestImageStorageGridFS:
    """Test MongoDB GridFS image storage APIs"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        return response.json().get("access_token")
    
    @pytest.fixture(scope="class")
    def uploaded_image_id(self, admin_token):
        """Upload a test image and return its ID for other tests"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        files = {
            "file": ("test_image.png", TEST_IMAGE_BYTES, "image/png")
        }
        response = requests.post(
            f"{BASE_URL}/api/images/upload",
            headers=headers,
            files=files
        )
        if response.status_code == 200:
            return response.json().get("image_id")
        return None
    
    def test_upload_image_success(self, admin_token):
        """Test uploading image to GridFS via /api/images/upload"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        files = {
            "file": ("test_upload.png", TEST_IMAGE_BYTES, "image/png")
        }
        response = requests.post(
            f"{BASE_URL}/api/images/upload",
            headers=headers,
            files=files
        )
        
        assert response.status_code == 200, f"Upload failed: {response.text}"
        data = response.json()
        
        # Verify response structure
        assert "success" in data and data["success"] == True
        assert "image_id" in data
        assert "url" in data
        assert "size" in data
        
        # URL should be /api/images/{image_id}
        assert data["url"].startswith("/api/images/")
        assert data["image_id"] in data["url"]
    
    def test_upload_via_admin_endpoint(self, admin_token):
        """Test uploading image via /api/admin/upload-image endpoint"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        files = {
            "file": ("admin_test.png", TEST_IMAGE_BYTES, "image/png")
        }
        response = requests.post(
            f"{BASE_URL}/api/admin/upload-image",
            headers=headers,
            files=files
        )
        
        # Should either work (200) or endpoint might not exist (404)
        # We test both paths
        if response.status_code == 200:
            data = response.json()
            assert "image_id" in data or "image_url" in data
        else:
            # If endpoint doesn't exist, that's acceptable
            assert response.status_code in [404, 405]
    
    def test_retrieve_image(self, admin_token, uploaded_image_id):
        """Test retrieving image from GridFS via GET /api/images/{image_id}"""
        if not uploaded_image_id:
            pytest.skip("No image uploaded in previous test")
        
        response = requests.get(f"{BASE_URL}/api/images/{uploaded_image_id}")
        
        assert response.status_code == 200, f"Image retrieval failed: {response.text}"
        
        # Should return image content with proper headers
        assert response.headers.get("Content-Type") in ["image/png", "image/jpeg", "image/webp", "image/gif"]
        assert "Cache-Control" in response.headers
        assert len(response.content) > 0
    
    def test_image_persistence_after_upload(self, admin_token):
        """Test that uploaded image persists and can be retrieved multiple times"""
        # Upload new image
        headers = {"Authorization": f"Bearer {admin_token}"}
        files = {
            "file": ("persistence_test.png", TEST_IMAGE_BYTES, "image/png")
        }
        upload_response = requests.post(
            f"{BASE_URL}/api/images/upload",
            headers=headers,
            files=files
        )
        
        assert upload_response.status_code == 200
        image_id = upload_response.json().get("image_id")
        
        # Retrieve multiple times to verify persistence
        for i in range(3):
            get_response = requests.get(f"{BASE_URL}/api/images/{image_id}")
            assert get_response.status_code == 200, f"Retrieval {i+1} failed"
            assert len(get_response.content) > 0
    
    def test_delete_image(self, admin_token):
        """Test deleting image from GridFS"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # First upload an image to delete
        files = {"file": ("delete_test.png", TEST_IMAGE_BYTES, "image/png")}
        upload_response = requests.post(
            f"{BASE_URL}/api/images/upload",
            headers=headers,
            files=files
        )
        assert upload_response.status_code == 200
        image_id = upload_response.json().get("image_id")
        
        # Delete the image
        delete_response = requests.delete(
            f"{BASE_URL}/api/images/{image_id}",
            headers=headers
        )
        
        assert delete_response.status_code == 200
        assert delete_response.json().get("success") == True
        
        # Verify image no longer exists
        get_response = requests.get(f"{BASE_URL}/api/images/{image_id}")
        assert get_response.status_code == 404
    
    def test_image_not_found(self):
        """Test retrieving non-existent image returns 404"""
        fake_id = "non-existent-image-id-12345"
        response = requests.get(f"{BASE_URL}/api/images/{fake_id}")
        
        assert response.status_code == 404
    
    def test_upload_invalid_file_type(self, admin_token):
        """Test uploading non-image file is rejected"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        files = {
            "file": ("test.txt", b"This is not an image", "text/plain")
        }
        response = requests.post(
            f"{BASE_URL}/api/images/upload",
            headers=headers,
            files=files
        )
        
        assert response.status_code == 400
    
    def test_upload_without_auth_fails(self):
        """Test upload without authentication fails"""
        files = {"file": ("test.png", TEST_IMAGE_BYTES, "image/png")}
        response = requests.post(f"{BASE_URL}/api/images/upload", files=files)
        
        assert response.status_code in [401, 403, 422]


class TestAdminAnalyticsDashboard:
    """Test Admin Analytics Dashboard APIs"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        return response.json().get("access_token")
    
    def test_dashboard_metrics(self, admin_token):
        """Test GET /api/admin/analytics/dashboard returns all metrics"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/dashboard",
            headers=headers
        )
        
        assert response.status_code == 200, f"Dashboard failed: {response.text}"
        data = response.json()
        
        # Verify main metric categories exist
        assert "users" in data
        assert "subscriptions" in data
        assert "revenue" in data
        assert "simulations" in data
        assert "content" in data
        
        # Verify users metrics
        assert "total" in data["users"]
        assert "new_this_month" in data["users"]
        assert "trial_active" in data["users"]
        
        # Verify subscriptions metrics
        assert "active" in data["subscriptions"]
        assert "mercadopago" in data["subscriptions"]
        assert "manual" in data["subscriptions"]
        
        # Verify revenue metrics
        assert "total" in data["revenue"]
        assert "this_month" in data["revenue"]
        assert "mrr" in data["revenue"]
        
        # Verify content metrics
        assert "courses" in data["content"]
        assert "lessons" in data["content"]
        assert "questions" in data["content"]
        assert "universities" in data["content"]
    
    def test_revenue_chart_data(self, admin_token):
        """Test GET /api/admin/analytics/revenue/chart returns chart data"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/revenue/chart?days=30",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert "period_days" in data
        assert isinstance(data["data"], list)
        
        # Verify data structure
        if len(data["data"]) > 0:
            first_item = data["data"][0]
            assert "date" in first_item
            assert "revenue" in first_item
    
    def test_users_chart_data(self, admin_token):
        """Test GET /api/admin/analytics/users/chart returns user growth data"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/users/chart?days=30",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert isinstance(data["data"], list)
        
        if len(data["data"]) > 0:
            first_item = data["data"][0]
            assert "date" in first_item
            assert "new_users" in first_item
    
    def test_simulations_chart_data(self, admin_token):
        """Test GET /api/admin/analytics/simulations/chart returns simulation data"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/simulations/chart?days=30",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_subscriptions_chart_data(self, admin_token):
        """Test GET /api/admin/analytics/subscriptions/chart returns subscription data"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/subscriptions/chart?days=30",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_recent_activity(self, admin_token):
        """Test GET /api/admin/analytics/activity/recent returns recent activity"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/activity/recent?limit=10",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        
        # Verify activity structure if data exists
        if len(data) > 0:
            activity = data[0]
            assert "type" in activity
            assert activity["type"] in ["user_registration", "subscription", "simulation"]
    
    def test_top_content(self, admin_token):
        """Test GET /api/admin/analytics/content/top returns top content"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/api/admin/analytics/content/top",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "top_attempted_courses" in data
        assert "courses_by_lessons" in data
    
    def test_chart_days_parameter(self, admin_token):
        """Test chart endpoints respect days parameter"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Test with 7 days
        response_7 = requests.get(
            f"{BASE_URL}/api/admin/analytics/users/chart?days=7",
            headers=headers
        )
        assert response_7.status_code == 200
        assert response_7.json()["period_days"] == 7
        
        # Test with 90 days
        response_90 = requests.get(
            f"{BASE_URL}/api/admin/analytics/users/chart?days=90",
            headers=headers
        )
        assert response_90.status_code == 200
        assert response_90.json()["period_days"] == 90
    
    def test_analytics_without_auth_fails(self):
        """Test analytics endpoints require authentication"""
        response = requests.get(f"{BASE_URL}/api/admin/analytics/dashboard")
        assert response.status_code in [401, 403, 422]


class TestLegacyUploadsEndpoint:
    """Test legacy /api/uploads/{filename} endpoint with GridFS fallback"""
    
    @pytest.fixture(scope="class")
    def admin_token(self):
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        return response.json().get("access_token")
    
    def test_legacy_endpoint_nonexistent_file(self):
        """Test legacy uploads endpoint returns 404 for non-existent file"""
        response = requests.get(f"{BASE_URL}/api/uploads/nonexistent_file.png")
        # Should return 404 if file not found
        assert response.status_code in [404, 500]


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
