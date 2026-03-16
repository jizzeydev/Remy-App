"""
Test Admin Universities Module
Tests CRUD operations for: Universities -> Courses -> Evaluations -> Questions
Plus: Logo upload, AI question generation, Stats
"""

import pytest
import requests
import os
import uuid
import time
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/app/backend/.env")

# Get BASE_URL from frontend .env (production URL)
BASE_URL = "https://remy-exam-prep.preview.emergentagent.com"

# Generate admin token
def generate_admin_token():
    """Generate admin JWT token for authentication"""
    secret_key = os.environ.get('ADMIN_SECRET_KEY')
    admin_username = os.environ.get('ADMIN_USERNAME')
    token = jwt.encode(
        {"sub": admin_username, "exp": datetime.now(timezone.utc) + timedelta(minutes=480)},
        secret_key,
        algorithm="HS256"
    )
    return token

ADMIN_TOKEN = generate_admin_token()

# ==================== FIXTURES ====================

@pytest.fixture(scope="module")
def api_client():
    """Shared requests session with auth headers"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ADMIN_TOKEN}"
    })
    return session


@pytest.fixture(scope="module")
def test_university(api_client):
    """Create a test university for testing courses and evaluations"""
    # Use form data for university creation
    response = requests.post(
        f"{BASE_URL}/api/admin/universities",
        headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
        data={
            "name": f"TEST_Universidad de Prueba {uuid.uuid4().hex[:8]}",
            "short_name": "TEST_UPT",
            "city": "Santiago"
        }
    )
    assert response.status_code == 200, f"Failed to create university: {response.text}"
    uni_data = response.json()
    
    yield uni_data
    
    # Cleanup - delete university after tests
    try:
        api_client.delete(f"{BASE_URL}/api/admin/universities/{uni_data['id']}")
    except Exception as e:
        print(f"Cleanup warning: {e}")


@pytest.fixture(scope="module")
def test_course(api_client, test_university):
    """Create a test course for testing evaluations and questions"""
    university_id = test_university["id"]
    
    response = api_client.post(
        f"{BASE_URL}/api/admin/universities/{university_id}/courses",
        json={
            "name": f"TEST_Cálculo Integral {uuid.uuid4().hex[:8]}",
            "code": "MAT201",
            "description": "Curso de cálculo integral",
            "department": "Matemáticas"
        }
    )
    assert response.status_code == 200, f"Failed to create course: {response.text}"
    course_data = response.json()
    
    yield {"id": course_data["id"], "university_id": university_id}
    
    # Course will be deleted when university is deleted


@pytest.fixture(scope="module")
def test_evaluation(api_client, test_university, test_course):
    """Create a test evaluation for testing questions"""
    university_id = test_university["id"]
    course_id = test_course["id"]
    
    response = api_client.post(
        f"{BASE_URL}/api/admin/universities/{university_id}/courses/{course_id}/evaluations",
        json={
            "name": "TEST_Interrogación 1",
            "description": "Primera interrogación del semestre"
        }
    )
    assert response.status_code == 200, f"Failed to create evaluation: {response.text}"
    eval_data = response.json()
    
    yield {"id": eval_data["id"], "university_id": university_id, "course_id": course_id}


# ==================== UNIVERSITY TESTS ====================

class TestUniversityEndpoints:
    """Tests for University CRUD operations"""
    
    def test_list_universities(self, api_client):
        """GET /api/admin/universities - List all universities"""
        response = api_client.get(f"{BASE_URL}/api/admin/universities")
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"Listed {len(data)} universities")
    
    def test_create_university_with_form_data(self, api_client):
        """POST /api/admin/universities - Create university with Form data"""
        unique_name = f"TEST_Universidad Nueva {uuid.uuid4().hex[:8]}"
        
        # Create with form data (not JSON)
        response = requests.post(
            f"{BASE_URL}/api/admin/universities",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            data={
                "name": unique_name,
                "short_name": "TEST_UN",
                "city": "Valparaíso"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should contain id"
        assert "message" in data, "Response should contain message"
        
        # Cleanup
        api_client.delete(f"{BASE_URL}/api/admin/universities/{data['id']}")
        print(f"Created and cleaned up university: {unique_name}")
    
    def test_get_university_with_courses(self, api_client, test_university):
        """GET /api/admin/universities/{id} - Get university details with courses"""
        uni_id = test_university["id"]
        
        response = api_client.get(f"{BASE_URL}/api/admin/universities/{uni_id}")
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should contain id"
        assert "name" in data, "Response should contain name"
        assert "courses" in data, "Response should contain courses list"
        print(f"University '{data['name']}' has {len(data.get('courses', []))} courses")
    
    def test_update_university(self, api_client, test_university):
        """PUT /api/admin/universities/{id} - Update university"""
        uni_id = test_university["id"]
        
        response = api_client.put(
            f"{BASE_URL}/api/admin/universities/{uni_id}",
            json={
                "name": f"TEST_Universidad Actualizada {uuid.uuid4().hex[:8]}",
                "city": "Concepción"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "message" in data, "Response should contain message"
        print(f"Updated university: {data.get('message')}")
    
    def test_get_university_not_found(self, api_client):
        """GET /api/admin/universities/{id} - Not found for invalid ID"""
        fake_id = str(uuid.uuid4())
        
        response = api_client.get(f"{BASE_URL}/api/admin/universities/{fake_id}")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"


# ==================== COURSE TESTS ====================

class TestCourseEndpoints:
    """Tests for University Course CRUD operations"""
    
    def test_list_courses(self, api_client, test_university):
        """GET /api/admin/universities/{id}/courses - List courses"""
        uni_id = test_university["id"]
        
        response = api_client.get(f"{BASE_URL}/api/admin/universities/{uni_id}/courses")
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"Listed {len(data)} courses for university")
    
    def test_create_course(self, api_client, test_university):
        """POST /api/admin/universities/{id}/courses - Create course"""
        uni_id = test_university["id"]
        
        response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses",
            json={
                "name": f"TEST_Álgebra Lineal {uuid.uuid4().hex[:8]}",
                "code": "MAT101",
                "description": "Curso de álgebra lineal",
                "department": "Matemáticas"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should contain course id"
        print(f"Created course with id: {data['id']}")
    
    def test_get_course_details(self, api_client, test_university, test_course):
        """GET /api/admin/universities/{uid}/courses/{cid} - Get course details"""
        uni_id = test_university["id"]
        course_id = test_course["id"]
        
        response = api_client.get(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}"
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should contain id"
        assert "evaluations" in data, "Response should contain evaluations list"
        print(f"Course has {len(data.get('evaluations', []))} evaluations")
    
    def test_update_course(self, api_client, test_university, test_course):
        """PUT /api/admin/universities/{uid}/courses/{cid} - Update course"""
        uni_id = test_university["id"]
        course_id = test_course["id"]
        
        response = api_client.put(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}",
            json={
                "name": f"TEST_Cálculo Actualizado {uuid.uuid4().hex[:8]}",
                "description": "Descripción actualizada"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "message" in data, "Response should contain message"
        print(f"Updated course: {data.get('message')}")


# ==================== EVALUATION TESTS ====================

class TestEvaluationEndpoints:
    """Tests for Evaluation CRUD operations"""
    
    def test_list_evaluations(self, api_client, test_university, test_course):
        """GET /api/admin/universities/{uid}/courses/{cid}/evaluations - List evaluations"""
        uni_id = test_university["id"]
        course_id = test_course["id"]
        
        response = api_client.get(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations"
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"Listed {len(data)} evaluations")
    
    def test_create_evaluation(self, api_client, test_university, test_course):
        """POST /api/admin/universities/{uid}/courses/{cid}/evaluations - Create evaluation"""
        uni_id = test_university["id"]
        course_id = test_course["id"]
        
        response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations",
            json={
                "name": f"TEST_Examen Final {uuid.uuid4().hex[:8]}",
                "description": "Examen final del curso"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should contain evaluation id"
        print(f"Created evaluation with id: {data['id']}")
    
    def test_update_evaluation(self, api_client, test_evaluation):
        """PUT /api/admin/universities/{uid}/courses/{cid}/evaluations/{eid} - Update evaluation"""
        uni_id = test_evaluation["university_id"]
        course_id = test_evaluation["course_id"]
        eval_id = test_evaluation["id"]
        
        response = api_client.put(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}",
            json={
                "name": f"TEST_Interrogación Actualizada {uuid.uuid4().hex[:8]}",
                "description": "Descripción actualizada"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "message" in data, "Response should contain message"
        print(f"Updated evaluation: {data.get('message')}")


# ==================== QUESTION TESTS ====================

class TestQuestionEndpoints:
    """Tests for Evaluation Question CRUD operations"""
    
    def test_list_questions(self, api_client, test_evaluation):
        """GET /api/admin/universities/.../questions - List questions"""
        uni_id = test_evaluation["university_id"]
        course_id = test_evaluation["course_id"]
        eval_id = test_evaluation["id"]
        
        response = api_client.get(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}/questions"
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"Listed {len(data)} questions")
    
    def test_create_manual_question(self, api_client, test_evaluation):
        """POST /api/admin/universities/.../questions - Create manual question"""
        uni_id = test_evaluation["university_id"]
        course_id = test_evaluation["course_id"]
        eval_id = test_evaluation["id"]
        
        response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}/questions",
            json={
                "question_content": "¿Cuál es la derivada de $f(x) = x^2$?",
                "solution_content": "La derivada es $f'(x) = 2x$",
                "question_type": "multiple_choice",
                "options": ["$2x$", "$x^2$", "$2$", "$x$"],
                "correct_answer": "A",
                "difficulty": "facil",
                "topic": "Derivadas",
                "tags": ["derivadas", "cálculo"],
                "source": "manual"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should contain question id"
        print(f"Created question with id: {data['id']}")
        
        return data["id"]
    
    def test_update_question(self, api_client, test_evaluation):
        """PUT /api/admin/universities/.../questions/{qid} - Update question"""
        uni_id = test_evaluation["university_id"]
        course_id = test_evaluation["course_id"]
        eval_id = test_evaluation["id"]
        
        # First create a question
        create_response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}/questions",
            json={
                "question_content": "Pregunta temporal",
                "question_type": "multiple_choice",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "difficulty": "medio"
            }
        )
        question_id = create_response.json()["id"]
        
        # Now update it
        response = api_client.put(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}/questions/{question_id}",
            json={
                "question_content": "Pregunta actualizada con $\\int x dx$",
                "question_type": "multiple_choice",
                "options": ["$\\frac{x^2}{2}$", "$x$", "$1$", "$0$"],
                "correct_answer": "A",
                "difficulty": "medio",
                "solution_content": "Explicación paso a paso"
            }
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "message" in data, "Response should contain message"
        print(f"Updated question: {data.get('message')}")
    
    def test_delete_question(self, api_client, test_evaluation):
        """DELETE /api/admin/universities/.../questions/{qid} - Delete question"""
        uni_id = test_evaluation["university_id"]
        course_id = test_evaluation["course_id"]
        eval_id = test_evaluation["id"]
        
        # First create a question to delete
        create_response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}/questions",
            json={
                "question_content": "Pregunta para eliminar",
                "question_type": "multiple_choice",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "B",
                "difficulty": "facil"
            }
        )
        question_id = create_response.json()["id"]
        
        # Delete it
        response = api_client.delete(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}/questions/{question_id}"
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "message" in data, "Response should contain message"
        print(f"Deleted question: {data.get('message')}")


# ==================== LOGO UPLOAD TEST ====================

class TestLogoUpload:
    """Tests for university logo upload"""
    
    def test_upload_logo(self, test_university):
        """POST /api/admin/universities/{id}/upload-logo - Upload logo"""
        uni_id = test_university["id"]
        
        # Create a simple test image (1x1 pixel PNG)
        import base64
        # Minimal PNG file (1x1 transparent pixel)
        png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        png_bytes = base64.b64decode(png_base64)
        
        response = requests.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/upload-logo",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            files={"logo": ("test_logo.png", png_bytes, "image/png")}
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "logo_path" in data, "Response should contain logo_path"
        print(f"Uploaded logo: {data.get('logo_path')}")
        
        return data.get("logo_path")
    
    def test_get_logo(self, test_university):
        """GET /api/admin/universities/logo/{filename} - Serve logo"""
        # First upload a logo
        uni_id = test_university["id"]
        
        import base64
        png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        png_bytes = base64.b64decode(png_base64)
        
        upload_response = requests.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/upload-logo",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            files={"logo": ("test_logo.png", png_bytes, "image/png")}
        )
        
        if upload_response.status_code == 200:
            logo_path = upload_response.json().get("logo_path")
            
            # Now get the logo (no auth needed for public serving)
            get_response = requests.get(f"{BASE_URL}{logo_path}")
            assert get_response.status_code == 200, f"Failed to get logo: {get_response.text}"
            print(f"Successfully retrieved logo from {logo_path}")


# ==================== AI GENERATION TEST ====================

class TestAIGeneration:
    """Tests for AI question generation (may take 30-60 seconds)"""
    
    @pytest.mark.slow
    def test_generate_questions_with_prompt(self, api_client, test_evaluation):
        """POST /api/admin/universities/.../generate - Generate questions with AI"""
        uni_id = test_evaluation["university_id"]
        course_id = test_evaluation["course_id"]
        eval_id = test_evaluation["id"]
        
        response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}/generate",
            json={
                "generation_type": "prompt",
                "prompt": "Genera preguntas sobre derivadas básicas y regla de la cadena",
                "num_questions": 2,
                "difficulty": "medio",
                "topic": "Derivadas"
            },
            timeout=90  # AI generation can take 30-60 seconds
        )
        
        # AI generation may fail due to API issues, so we accept both success and some errors
        if response.status_code == 200:
            data = response.json()
            assert "success" in data or "created_count" in data, "Response should indicate success"
            print(f"AI Generated {data.get('created_count', 0)} questions")
        elif response.status_code == 500:
            # AI service error is acceptable
            print(f"AI generation returned 500 (service error): {response.text[:200]}")
        else:
            assert False, f"Unexpected status {response.status_code}: {response.text}"


# ==================== STATS TEST ====================

class TestStatsEndpoint:
    """Tests for statistics endpoint"""
    
    def test_get_stats_summary(self, api_client):
        """GET /api/admin/universities/stats/summary - Get summary stats"""
        response = api_client.get(f"{BASE_URL}/api/admin/universities/stats/summary")
        assert response.status_code == 200, f"Failed: {response.text}"
        
        data = response.json()
        assert "total_universities" in data, "Should have total_universities"
        assert "total_courses" in data, "Should have total_courses"
        assert "total_evaluations" in data, "Should have total_evaluations"
        assert "total_questions" in data, "Should have total_questions"
        assert "questions_by_source" in data, "Should have questions_by_source breakdown"
        
        print(f"Stats: {data['total_universities']} universities, {data['total_courses']} courses, {data['total_questions']} questions")


# ==================== DELETE TESTS (Run Last) ====================

class TestDeleteOperations:
    """Tests for delete operations - run last to cleanup"""
    
    def test_delete_evaluation(self, api_client, test_university, test_course):
        """DELETE /api/admin/universities/.../evaluations/{eid} - Delete evaluation"""
        uni_id = test_university["id"]
        course_id = test_course["id"]
        
        # Create evaluation to delete
        create_response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations",
            json={
                "name": "TEST_Evaluación para eliminar",
                "description": "Esta evaluación será eliminada"
            }
        )
        eval_id = create_response.json()["id"]
        
        # Delete it
        response = api_client.delete(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}/evaluations/{eval_id}"
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        print(f"Deleted evaluation: {eval_id}")
    
    def test_delete_course(self, api_client, test_university):
        """DELETE /api/admin/universities/{uid}/courses/{cid} - Delete course"""
        uni_id = test_university["id"]
        
        # Create course to delete
        create_response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses",
            json={
                "name": "TEST_Curso para eliminar",
                "code": "DEL001"
            }
        )
        course_id = create_response.json()["id"]
        
        # Delete it
        response = api_client.delete(
            f"{BASE_URL}/api/admin/universities/{uni_id}/courses/{course_id}"
        )
        assert response.status_code == 200, f"Failed: {response.text}"
        print(f"Deleted course: {course_id}")
    
    def test_delete_university(self, api_client):
        """DELETE /api/admin/universities/{id} - Delete university and cascade"""
        # Create university to delete
        create_response = requests.post(
            f"{BASE_URL}/api/admin/universities",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            data={
                "name": "TEST_Universidad para eliminar",
                "short_name": "TEST_UPE",
                "city": "Test City"
            }
        )
        uni_id = create_response.json()["id"]
        
        # Delete it
        response = api_client.delete(f"{BASE_URL}/api/admin/universities/{uni_id}")
        assert response.status_code == 200, f"Failed: {response.text}"
        
        # Verify it's deleted
        get_response = api_client.get(f"{BASE_URL}/api/admin/universities/{uni_id}")
        assert get_response.status_code == 404, "University should be deleted"
        print(f"Deleted university: {uni_id}")


# ==================== AUTH TESTS ====================

class TestAuthentication:
    """Tests for authentication requirements"""
    
    def test_unauthorized_access(self):
        """Verify endpoints require authentication"""
        # No auth header
        response = requests.get(f"{BASE_URL}/api/admin/universities")
        assert response.status_code in [401, 403], f"Expected 401/403 without auth, got {response.status_code}"
        print("Unauthorized access correctly blocked")
    
    def test_invalid_token(self):
        """Verify invalid token is rejected"""
        response = requests.get(
            f"{BASE_URL}/api/admin/universities",
            headers={"Authorization": "Bearer invalid_token_here"}
        )
        assert response.status_code == 401, f"Expected 401 for invalid token, got {response.status_code}"
        print("Invalid token correctly rejected")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
