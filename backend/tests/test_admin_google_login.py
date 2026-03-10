"""
Test suite for Admin Google Login Endpoint
Tests the /api/admin/google-login endpoint which:
- Accepts session_id from Emergent Auth
- Verifies email is in allowed admin list
- Generates JWT with type='admin_google'
"""

import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL')
if BASE_URL:
    BASE_URL = BASE_URL.rstrip('/')

# Allowed admin emails
ALLOWED_ADMIN_EMAILS = ['seremonta.cl@gmail.com', 'admin@seremonta.cl']

class TestAdminGoogleLogin:
    """Tests for POST /api/admin/google-login endpoint"""
    
    def test_google_login_rejects_empty_session_id(self):
        """Test that endpoint rejects empty session_id"""
        response = requests.post(
            f"{BASE_URL}/api/admin/google-login",
            json={"session_id": ""}
        )
        # Should return 400 for empty/missing session_id
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.json()
        assert "session_id requerido" in data.get("detail", ""), f"Unexpected error: {data}"
        print(f"✓ Empty session_id correctly rejected with 400: {data.get('detail')}")
    
    def test_google_login_rejects_invalid_session_id(self):
        """Test that endpoint rejects invalid session_id"""
        response = requests.post(
            f"{BASE_URL}/api/admin/google-login",
            json={"session_id": "invalid-test-session-123456"}
        )
        # Should return 401 for invalid session
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        data = response.json()
        assert "Error de autenticación" in data.get("detail", ""), f"Unexpected error: {data}"
        print(f"✓ Invalid session_id correctly rejected with 401: {data.get('detail')}")
    
    def test_google_login_rejects_missing_session_id(self):
        """Test that endpoint rejects request without session_id field"""
        response = requests.post(
            f"{BASE_URL}/api/admin/google-login",
            json={}
        )
        # Should return 422 for missing field
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        print("✓ Missing session_id correctly rejected with 422")
    
    def test_traditional_admin_login_works(self):
        """Test that traditional username/password login still works"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "access_token" in data, "Missing access_token in response"
        assert data.get("token_type") == "bearer", "Token type should be bearer"
        print("✓ Traditional admin login works correctly")
    
    def test_admin_verify_with_traditional_token(self):
        """Test that admin verify works with traditional login token"""
        # First login
        login_response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={"username": "admin", "password": "#Alex060625"}
        )
        token = login_response.json().get("access_token")
        
        # Verify
        verify_response = requests.get(
            f"{BASE_URL}/api/admin/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert verify_response.status_code == 200, f"Expected 200, got {verify_response.status_code}"
        data = verify_response.json()
        assert data.get("verified") == True, "Admin should be verified"
        print(f"✓ Admin verify works: username={data.get('username')}")


class TestMigrationDataExport:
    """Tests for migration script export functionality"""
    
    def test_courses_json_exists(self):
        """Verify courses.json was exported"""
        import json
        from pathlib import Path
        
        file_path = Path("/app/backend/migration_data/courses.json")
        assert file_path.exists(), "courses.json not found"
        
        with open(file_path) as f:
            courses = json.load(f)
        assert isinstance(courses, list), "courses.json should contain a list"
        assert len(courses) >= 2, f"Expected at least 2 courses, got {len(courses)}"
        print(f"✓ courses.json exists with {len(courses)} courses")
    
    def test_chapters_json_exists(self):
        """Verify chapters.json was exported"""
        import json
        from pathlib import Path
        
        file_path = Path("/app/backend/migration_data/chapters.json")
        assert file_path.exists(), "chapters.json not found"
        
        with open(file_path) as f:
            chapters = json.load(f)
        assert isinstance(chapters, list), "chapters.json should contain a list"
        assert len(chapters) >= 2, f"Expected at least 2 chapters, got {len(chapters)}"
        print(f"✓ chapters.json exists with {len(chapters)} chapters")
    
    def test_lessons_json_exists(self):
        """Verify lessons.json was exported"""
        import json
        from pathlib import Path
        
        file_path = Path("/app/backend/migration_data/lessons.json")
        assert file_path.exists(), "lessons.json not found"
        
        with open(file_path) as f:
            lessons = json.load(f)
        assert isinstance(lessons, list), "lessons.json should contain a list"
        assert len(lessons) >= 5, f"Expected at least 5 lessons, got {len(lessons)}"
        print(f"✓ lessons.json exists with {len(lessons)} lessons")
    
    def test_questions_json_exists(self):
        """Verify questions.json was exported"""
        import json
        from pathlib import Path
        
        file_path = Path("/app/backend/migration_data/questions.json")
        assert file_path.exists(), "questions.json not found"
        
        with open(file_path) as f:
            questions = json.load(f)
        assert isinstance(questions, list), "questions.json should contain a list"
        assert len(questions) >= 9, f"Expected at least 9 questions, got {len(questions)}"
        print(f"✓ questions.json exists with {len(questions)} questions")
    
    def test_formulas_json_exists(self):
        """Verify formulas.json was exported"""
        import json
        from pathlib import Path
        
        file_path = Path("/app/backend/migration_data/formulas.json")
        assert file_path.exists(), "formulas.json not found"
        
        with open(file_path) as f:
            formulas = json.load(f)
        assert isinstance(formulas, list), "formulas.json should contain a list"
        assert len(formulas) >= 10, f"Expected at least 10 formulas, got {len(formulas)}"
        print(f"✓ formulas.json exists with {len(formulas)} formulas")
    
    def test_export_summary_matches(self):
        """Verify export summary matches expected counts"""
        import json
        from pathlib import Path
        
        summary_path = Path("/app/backend/migration_data/_export_summary.json")
        assert summary_path.exists(), "_export_summary.json not found"
        
        with open(summary_path) as f:
            summary = json.load(f)
        
        expected = {
            "courses": 2,
            "chapters": 2,
            "lessons": 5,
            "questions": 9,
            "formulas": 10
        }
        
        collections = summary.get("collections", {})
        for coll, expected_count in expected.items():
            actual = collections.get(coll, 0)
            assert actual >= expected_count, f"{coll}: expected >={expected_count}, got {actual}"
        
        print(f"✓ Export summary verified: {collections}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
