"""
Test Course Restructure Features - Library Universities, Enrollments, Settings, Import Chapters
Tests for the new multi-university course system
"""
import pytest
import requests
import os
import uuid
from datetime import datetime

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')
if not BASE_URL:
    BASE_URL = "https://remy-exam-prep.preview.emergentagent.com"

# Admin credentials
ADMIN_EMAIL = "seremonta.cl@gmail.com"

class TestLibraryUniversitiesPublic:
    """Test public library universities endpoint"""
    
    def test_get_active_library_universities(self):
        """GET /api/library-universities - list active universities"""
        response = requests.get(f"{BASE_URL}/api/library-universities")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        
        # If there are universities, verify structure
        if len(data) > 0:
            uni = data[0]
            assert "id" in uni, "University should have id"
            assert "name" in uni, "University should have name"
            assert "short_name" in uni, "University should have short_name"
            # All returned should be active
            assert uni.get("is_active", True) == True, "Public endpoint should only return active universities"
        
        print(f"✓ GET /api/library-universities returned {len(data)} active universities")


class TestLibraryUniversitiesAdmin:
    """Test admin library universities CRUD"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Get admin token"""
        # Try Google admin login
        self.admin_token = self._get_admin_token()
        self.headers = {"Authorization": f"Bearer {self.admin_token}"}
        self.created_university_id = None
        yield
        # Cleanup
        if self.created_university_id:
            try:
                requests.delete(
                    f"{BASE_URL}/api/admin/library-universities/{self.created_university_id}",
                    headers=self.headers
                )
            except:
                pass
    
    def _get_admin_token(self):
        """Get admin token via traditional login"""
        response = requests.post(f"{BASE_URL}/api/admin/login", json={
            "username": "admin",
            "password": "remy2026admin"
        })
        if response.status_code == 200:
            return response.json().get("access_token")
        pytest.skip("Could not get admin token")
    
    def test_admin_list_all_universities(self):
        """GET /api/admin/library-universities - list all universities (admin)"""
        response = requests.get(
            f"{BASE_URL}/api/admin/library-universities",
            headers=self.headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"✓ Admin GET /api/admin/library-universities returned {len(data)} universities")
    
    def test_admin_create_university(self):
        """POST /api/admin/library-universities - create university"""
        unique_suffix = str(uuid.uuid4())[:6].upper()
        payload = {
            "name": f"Test University {unique_suffix}",
            "short_name": f"TU{unique_suffix[:3]}"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/admin/library-universities",
            json=payload,
            headers=self.headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert data.get("success") == True, "Should return success"
        assert "university" in data, "Should return university object"
        
        uni = data["university"]
        assert uni["name"] == payload["name"], "Name should match"
        assert uni["short_name"] == payload["short_name"].upper(), "Short name should be uppercase"
        assert "id" in uni, "Should have id"
        
        self.created_university_id = uni["id"]
        print(f"✓ Created university: {uni['name']} ({uni['short_name']})")
    
    def test_admin_create_duplicate_short_name_fails(self):
        """POST /api/admin/library-universities - duplicate short_name should fail"""
        # First create a university
        unique_suffix = str(uuid.uuid4())[:6].upper()
        payload = {
            "name": f"Test University {unique_suffix}",
            "short_name": f"DUP{unique_suffix[:2]}"
        }
        
        response1 = requests.post(
            f"{BASE_URL}/api/admin/library-universities",
            json=payload,
            headers=self.headers
        )
        assert response1.status_code == 200
        self.created_university_id = response1.json()["university"]["id"]
        
        # Try to create another with same short_name
        payload2 = {
            "name": "Another University",
            "short_name": payload["short_name"]
        }
        response2 = requests.post(
            f"{BASE_URL}/api/admin/library-universities",
            json=payload2,
            headers=self.headers
        )
        assert response2.status_code == 400, f"Expected 400 for duplicate, got {response2.status_code}"
        print("✓ Duplicate short_name correctly rejected")
    
    def test_admin_update_university(self):
        """PUT /api/admin/library-universities/{id} - update university"""
        # First create
        unique_suffix = str(uuid.uuid4())[:6].upper()
        create_response = requests.post(
            f"{BASE_URL}/api/admin/library-universities",
            json={"name": f"Original Name {unique_suffix}", "short_name": f"ON{unique_suffix[:3]}"},
            headers=self.headers
        )
        assert create_response.status_code == 200
        uni_id = create_response.json()["university"]["id"]
        self.created_university_id = uni_id
        
        # Update
        update_payload = {"name": f"Updated Name {unique_suffix}"}
        update_response = requests.put(
            f"{BASE_URL}/api/admin/library-universities/{uni_id}",
            json=update_payload,
            headers=self.headers
        )
        assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}: {update_response.text}"
        
        data = update_response.json()
        assert data.get("success") == True
        assert data["university"]["name"] == update_payload["name"]
        print(f"✓ Updated university name to: {data['university']['name']}")
    
    def test_admin_delete_university_without_courses(self):
        """DELETE /api/admin/library-universities/{id} - delete university without courses"""
        # Create a university
        unique_suffix = str(uuid.uuid4())[:6].upper()
        create_response = requests.post(
            f"{BASE_URL}/api/admin/library-universities",
            json={"name": f"To Delete {unique_suffix}", "short_name": f"TD{unique_suffix[:3]}"},
            headers=self.headers
        )
        assert create_response.status_code == 200
        uni_id = create_response.json()["university"]["id"]
        
        # Delete
        delete_response = requests.delete(
            f"{BASE_URL}/api/admin/library-universities/{uni_id}",
            headers=self.headers
        )
        assert delete_response.status_code == 200, f"Expected 200, got {delete_response.status_code}: {delete_response.text}"
        
        data = delete_response.json()
        assert data.get("success") == True
        print("✓ Successfully deleted university without courses")


class TestEnrollments:
    """Test student enrollment system"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Create test user and get token"""
        self.user_token = self._create_test_user_and_get_token()
        self.headers = {"Authorization": f"Bearer {self.user_token}"} if self.user_token else {}
        self.enrolled_course_id = None
        yield
        # Cleanup enrollment
        if self.enrolled_course_id and self.user_token:
            try:
                requests.delete(
                    f"{BASE_URL}/api/enrollments/{self.enrolled_course_id}",
                    headers=self.headers
                )
            except:
                pass
    
    def _create_test_user_and_get_token(self):
        """Create a test user in MongoDB and get session token"""
        import subprocess
        import json
        
        user_id = f"test-enroll-{uuid.uuid4()}"
        session_token = f"test_session_{uuid.uuid4()}"
        email = f"test.enroll.{uuid.uuid4()}@example.com"
        
        # Create user with active subscription for testing
        mongo_cmd = f'''
        use('test_database');
        db.users.insertOne({{
          id: "{user_id}",
          user_id: "{user_id}",
          email: "{email}",
          name: "Test Enrollment User",
          subscription: {{
            status: "authorized",
            manual_access: true
          }},
          trial_start: new Date(),
          created_at: new Date()
        }});
        db.user_sessions.insertOne({{
          user_id: "{user_id}",
          session_token: "{session_token}",
          expires_at: new Date(Date.now() + 7*24*60*60*1000),
          created_at: new Date()
        }});
        '''
        
        try:
            result = subprocess.run(
                ["mongosh", "--quiet", "--eval", mongo_cmd],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return session_token
        except Exception as e:
            print(f"Warning: Could not create test user: {e}")
        
        return None
    
    def test_get_enrollments_requires_auth(self):
        """GET /api/enrollments - requires authentication"""
        response = requests.get(f"{BASE_URL}/api/enrollments")
        assert response.status_code in [401, 403], f"Expected 401/403 without auth, got {response.status_code}"
        print("✓ GET /api/enrollments correctly requires authentication")
    
    def test_get_enrollments_with_auth(self):
        """GET /api/enrollments - returns enrolled courses"""
        if not self.user_token:
            pytest.skip("Could not create test user")
        
        response = requests.get(
            f"{BASE_URL}/api/enrollments",
            headers=self.headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"✓ GET /api/enrollments returned {len(data)} enrolled courses")
    
    def test_enrollment_stats(self):
        """GET /api/enrollments/stats - returns enrollment statistics"""
        if not self.user_token:
            pytest.skip("Could not create test user")
        
        response = requests.get(
            f"{BASE_URL}/api/enrollments/stats",
            headers=self.headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "enrolled_count" in data, "Should have enrolled_count"
        assert "can_enroll_more" in data, "Should have can_enroll_more"
        assert "has_subscription" in data, "Should have has_subscription"
        print(f"✓ Enrollment stats: {data}")
    
    def test_enroll_in_course(self):
        """POST /api/enrollments - enroll in a course"""
        if not self.user_token:
            pytest.skip("Could not create test user")
        
        # First get available courses
        courses_response = requests.get(f"{BASE_URL}/api/courses")
        if courses_response.status_code != 200 or len(courses_response.json()) == 0:
            pytest.skip("No courses available for enrollment test")
        
        course = courses_response.json()[0]
        course_id = course["id"]
        
        # Enroll
        response = requests.post(
            f"{BASE_URL}/api/enrollments",
            json={"course_id": course_id},
            headers=self.headers
        )
        
        # Could be 200 (success) or 400 (already enrolled)
        if response.status_code == 200:
            data = response.json()
            assert data.get("success") == True
            self.enrolled_course_id = course_id
            print(f"✓ Successfully enrolled in course: {course['title']}")
        elif response.status_code == 400:
            # Already enrolled is acceptable
            print(f"✓ Already enrolled in course (expected behavior)")
        else:
            assert False, f"Unexpected status {response.status_code}: {response.text}"
    
    def test_unenroll_from_course(self):
        """DELETE /api/enrollments/{course_id} - unenroll from course"""
        if not self.user_token:
            pytest.skip("Could not create test user")
        
        # First enroll
        courses_response = requests.get(f"{BASE_URL}/api/courses")
        if courses_response.status_code != 200 or len(courses_response.json()) == 0:
            pytest.skip("No courses available")
        
        course = courses_response.json()[0]
        course_id = course["id"]
        
        # Enroll first
        requests.post(
            f"{BASE_URL}/api/enrollments",
            json={"course_id": course_id},
            headers=self.headers
        )
        
        # Unenroll
        response = requests.delete(
            f"{BASE_URL}/api/enrollments/{course_id}",
            headers=self.headers
        )
        
        # Could be 200 (success) or 404 (not enrolled)
        assert response.status_code in [200, 404], f"Expected 200 or 404, got {response.status_code}"
        print(f"✓ Unenroll endpoint working correctly")


class TestSettings:
    """Test app settings endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Get admin token"""
        self.admin_token = self._get_admin_token()
        self.headers = {"Authorization": f"Bearer {self.admin_token}"}
    
    def _get_admin_token(self):
        """Get admin token"""
        response = requests.post(f"{BASE_URL}/api/admin/login", json={
            "username": "admin",
            "password": "remy2026admin"
        })
        if response.status_code == 200:
            return response.json().get("access_token")
        pytest.skip("Could not get admin token")
    
    def test_get_public_settings(self):
        """GET /api/settings - get public app settings"""
        response = requests.get(f"{BASE_URL}/api/settings")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "tu_universidad_enabled" in data, "Should have tu_universidad_enabled setting"
        print(f"✓ Public settings: tu_universidad_enabled={data.get('tu_universidad_enabled')}")
    
    def test_get_admin_settings(self):
        """GET /api/admin/settings - get admin settings"""
        response = requests.get(
            f"{BASE_URL}/api/admin/settings",
            headers=self.headers
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "tu_universidad_enabled" in data
        print(f"✓ Admin settings retrieved successfully")
    
    def test_update_settings(self):
        """PUT /api/admin/settings - update settings"""
        # Get current value
        get_response = requests.get(
            f"{BASE_URL}/api/admin/settings",
            headers=self.headers
        )
        current_value = get_response.json().get("tu_universidad_enabled", False)
        
        # Toggle value
        new_value = not current_value
        update_response = requests.put(
            f"{BASE_URL}/api/admin/settings",
            json={"tu_universidad_enabled": new_value},
            headers=self.headers
        )
        assert update_response.status_code == 200, f"Expected 200, got {update_response.status_code}: {update_response.text}"
        
        data = update_response.json()
        assert data.get("success") == True
        assert data["settings"]["tu_universidad_enabled"] == new_value
        
        # Restore original value
        requests.put(
            f"{BASE_URL}/api/admin/settings",
            json={"tu_universidad_enabled": current_value},
            headers=self.headers
        )
        
        print(f"✓ Settings update working correctly")


class TestCoursesWithFilters:
    """Test courses endpoints with university filters"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Get admin token"""
        self.admin_token = self._get_admin_token()
        self.headers = {"Authorization": f"Bearer {self.admin_token}"}
    
    def _get_admin_token(self):
        """Get admin token"""
        response = requests.post(f"{BASE_URL}/api/admin/login", json={
            "username": "admin",
            "password": "remy2026admin"
        })
        if response.status_code == 200:
            return response.json().get("access_token")
        pytest.skip("Could not get admin token")
    
    def test_get_courses_public(self):
        """GET /api/courses - public courses list"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list)
        
        # Check that courses have university info
        if len(data) > 0:
            course = data[0]
            assert "university" in course or "university_id" in course, "Course should have university info"
        
        print(f"✓ GET /api/courses returned {len(data)} courses")
    
    def test_get_courses_with_search_filter(self):
        """GET /api/courses?search=... - filter by search term"""
        response = requests.get(f"{BASE_URL}/api/courses?search=Cálculo")
        assert response.status_code == 200
        
        data = response.json()
        print(f"✓ Search filter returned {len(data)} courses matching 'Cálculo'")
    
    def test_get_courses_with_university_filter(self):
        """GET /api/courses?university_id=general - filter by university"""
        response = requests.get(f"{BASE_URL}/api/courses?university_id=general")
        assert response.status_code == 200
        
        data = response.json()
        # All returned courses should be general (no university_id)
        for course in data:
            assert course.get("university_id") is None or course.get("university", {}).get("short_name") == "GEN", \
                f"Course {course.get('title')} should be general"
        
        print(f"✓ University filter (general) returned {len(data)} courses")
    
    def test_admin_get_courses_with_filters(self):
        """GET /api/admin/courses with filters"""
        # Test search filter
        response = requests.get(
            f"{BASE_URL}/api/admin/courses?search=test",
            headers=self.headers
        )
        assert response.status_code == 200
        
        # Test university filter
        response2 = requests.get(
            f"{BASE_URL}/api/admin/courses?university_id=general",
            headers=self.headers
        )
        assert response2.status_code == 200
        
        print("✓ Admin courses filters working correctly")


class TestImportChapters:
    """Test chapter import functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Get admin token"""
        self.admin_token = self._get_admin_token()
        self.headers = {"Authorization": f"Bearer {self.admin_token}"}
    
    def _get_admin_token(self):
        """Get admin token"""
        response = requests.post(f"{BASE_URL}/api/admin/login", json={
            "username": "admin",
            "password": "remy2026admin"
        })
        if response.status_code == 200:
            return response.json().get("access_token")
        pytest.skip("Could not get admin token")
    
    def test_import_chapters_requires_auth(self):
        """POST /api/admin/courses/{id}/import-chapters requires auth"""
        response = requests.post(
            f"{BASE_URL}/api/admin/courses/test-id/import-chapters",
            json={"source_course_id": "test", "chapter_ids": []}
        )
        assert response.status_code in [401, 403], f"Expected 401/403, got {response.status_code}"
        print("✓ Import chapters correctly requires authentication")
    
    def test_import_chapters_invalid_course(self):
        """POST /api/admin/courses/{id}/import-chapters - invalid target course"""
        response = requests.post(
            f"{BASE_URL}/api/admin/courses/nonexistent-course/import-chapters",
            json={
                "source_course_id": "also-nonexistent",
                "chapter_ids": ["chapter-1"]
            },
            headers=self.headers
        )
        assert response.status_code == 404, f"Expected 404 for invalid course, got {response.status_code}"
        print("✓ Import chapters correctly returns 404 for invalid course")
    
    def test_import_chapters_structure(self):
        """Test import chapters endpoint accepts correct structure"""
        # Get existing courses
        courses_response = requests.get(
            f"{BASE_URL}/api/admin/courses",
            headers=self.headers
        )
        
        if courses_response.status_code != 200 or len(courses_response.json()) < 2:
            pytest.skip("Need at least 2 courses to test import")
        
        courses = courses_response.json()
        source_course = courses[0]
        target_course = courses[1] if len(courses) > 1 else courses[0]
        
        # Get chapters from source
        chapters_response = requests.get(
            f"{BASE_URL}/api/courses/{source_course['id']}/chapters"
        )
        
        if chapters_response.status_code != 200 or len(chapters_response.json()) == 0:
            pytest.skip("Source course has no chapters")
        
        # Test with empty chapter_ids (should work but import nothing)
        response = requests.post(
            f"{BASE_URL}/api/admin/courses/{target_course['id']}/import-chapters",
            json={
                "source_course_id": source_course["id"],
                "chapter_ids": [],
                "include_lessons": True,
                "include_questions": True
            },
            headers=self.headers
        )
        
        # Should return 200 with 0 imported
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        data = response.json()
        assert "imported" in data, "Should have imported counts"
        print(f"✓ Import chapters endpoint structure validated")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
