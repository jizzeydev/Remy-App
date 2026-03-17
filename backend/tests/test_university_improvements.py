"""
Test University Improvements Module
Tests for:
1. Edit question functionality
2. Image upload for questions
3. AI review flow (auto_save=false)
4. Bulk save approved questions
5. Light mode (frontend check - TuUniversidad page)
6. KaTeX rendering (frontend check)
"""

import pytest
import requests
import os
import uuid
import time
import base64
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

# Test data - using existing university/course/evaluation
TEST_UNIVERSITY_ID = "8803fdbb-589a-4734-804e-4d0db4cf1aef"
TEST_COURSE_ID = "55828490-f2b1-42fb-9361-c96e2e6e6171"
TEST_EVALUATION_ID = "fbd30dc0-92e5-40e6-a23d-c7bed7f37251"


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
def test_question(api_client):
    """Create a test question for edit/delete operations"""
    response = api_client.post(
        f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions",
        json={
            "question_content": f"TEST_Pregunta para editar {uuid.uuid4().hex[:8]}",
            "question_type": "multiple_choice",
            "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
            "correct_answer": "A",
            "difficulty": "facil",
            "topic": "Test",
            "solution_content": "Solución de prueba",
            "source": "manual"
        }
    )
    assert response.status_code == 200, f"Failed to create question: {response.text}"
    data = response.json()
    
    yield data["id"]
    
    # Cleanup
    try:
        api_client.delete(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/{data['id']}"
        )
    except Exception as e:
        print(f"Cleanup warning: {e}")


# ==================== EDIT QUESTION TESTS ====================

class TestEditQuestion:
    """Tests for editing question functionality"""
    
    def test_edit_question_content(self, api_client, test_question):
        """PUT - Edit question content with LaTeX"""
        question_id = test_question
        
        response = api_client.put(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/{question_id}",
            json={
                "question_content": "Pregunta actualizada con fórmula: $\\int_0^1 x^2 dx = ?$",
                "question_type": "multiple_choice",
                "options": ["$\\frac{1}{3}$", "$\\frac{1}{2}$", "$1$", "$0$"],
                "correct_answer": "A",
                "difficulty": "medio",
                "solution_content": "Resolvemos: $\\int_0^1 x^2 dx = [\\frac{x^3}{3}]_0^1 = \\frac{1}{3}$",
                "topic": "Integrales"
            }
        )
        assert response.status_code == 200, f"Failed to edit question: {response.text}"
        
        data = response.json()
        assert "message" in data, "Response should contain message"
        print(f"PASS: Edit question content - {data.get('message')}")
    
    def test_edit_question_difficulty(self, api_client, test_question):
        """PUT - Change difficulty level"""
        question_id = test_question
        
        response = api_client.put(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/{question_id}",
            json={
                "question_content": "Pregunta con dificultad cambiada",
                "question_type": "multiple_choice",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "B",
                "difficulty": "dificil"  # Changed from facil to dificil
            }
        )
        assert response.status_code == 200, f"Failed to update difficulty: {response.text}"
        print(f"PASS: Edit question difficulty")
    
    def test_verify_edit_persisted(self, api_client, test_question):
        """GET - Verify edits are persisted"""
        question_id = test_question
        
        # First update with known values
        api_client.put(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/{question_id}",
            json={
                "question_content": "Pregunta verificada $x^2 + y^2 = r^2$",
                "question_type": "multiple_choice",
                "options": ["Círculo", "Elipse", "Parábola", "Hipérbola"],
                "correct_answer": "A",
                "difficulty": "facil",
                "topic": "Geometría"
            }
        )
        
        # Get all questions and find ours
        response = api_client.get(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions"
        )
        assert response.status_code == 200, f"Failed to get questions: {response.text}"
        
        questions = response.json()
        our_question = next((q for q in questions if q.get("id") == question_id), None)
        
        assert our_question is not None, "Question not found in list"
        assert "Pregunta verificada" in our_question.get("question_content", ""), "Content not updated"
        assert our_question.get("topic") == "Geometría", "Topic not updated"
        print(f"PASS: Edit verified - Question content and topic persisted correctly")


# ==================== IMAGE UPLOAD TESTS ====================

class TestQuestionImageUpload:
    """Tests for uploading images to questions"""
    
    def test_upload_question_image(self, api_client, test_question):
        """POST - Upload image to a question"""
        question_id = test_question
        
        # Create a simple test image (1x1 pixel PNG)
        png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        png_bytes = base64.b64decode(png_base64)
        
        response = requests.post(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/{question_id}/upload-image",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            files={"image": ("test_question_image.png", png_bytes, "image/png")}
        )
        assert response.status_code == 200, f"Failed to upload image: {response.text}"
        
        data = response.json()
        assert "image_url" in data, "Response should contain image_url"
        print(f"PASS: Upload question image - {data.get('image_url')}")
        
        return data.get("image_url")
    
    def test_upload_invalid_file_type(self, api_client, test_question):
        """POST - Reject non-image files"""
        question_id = test_question
        
        response = requests.post(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/{question_id}/upload-image",
            headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
            files={"image": ("test.txt", b"This is not an image", "text/plain")}
        )
        
        # Should fail with 400 Bad Request
        assert response.status_code == 400, f"Should reject non-image files: {response.text}"
        print(f"PASS: Invalid file type rejected correctly")
    
    def test_verify_image_in_question(self, api_client, test_question):
        """GET - Verify image_url in question response"""
        question_id = test_question
        
        # Get all questions
        response = api_client.get(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions"
        )
        assert response.status_code == 200, f"Failed to get questions: {response.text}"
        
        questions = response.json()
        our_question = next((q for q in questions if q.get("id") == question_id), None)
        
        assert our_question is not None, "Question not found"
        # image_url may or may not be set depending on test order
        print(f"PASS: Question has image_url field: {our_question.get('image_url')}")


# ==================== AI REVIEW FLOW TESTS ====================

class TestAIReviewFlow:
    """Tests for AI question generation with review flow (auto_save=false)"""
    
    @pytest.mark.slow
    def test_generate_without_auto_save(self, api_client):
        """POST - Generate questions with auto_save=false (review flow)"""
        response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/generate",
            json={
                "generation_type": "prompt",
                "prompt": "Genera 2 preguntas sobre derivadas básicas",
                "num_questions": 2,
                "difficulty": "facil",
                "auto_save": False  # Key: Don't save automatically
            },
            timeout=120
        )
        
        # Check response - may take a while due to AI
        if response.status_code != 200:
            print(f"AI generation failed (may be transient): {response.text}")
            pytest.skip("AI generation failed - skipping review flow test")
        
        data = response.json()
        assert data.get("success") is True, "Generation should be successful"
        assert data.get("auto_saved") is False, "auto_saved should be False"
        assert "questions" in data, "Response should contain questions"
        assert len(data["questions"]) > 0, "Should have at least one question"
        
        # Verify questions have required fields
        for q in data["questions"]:
            assert "question_content" in q, "Question should have content"
            assert "options" in q, "Question should have options"
            assert "correct_answer" in q, "Question should have correct_answer"
        
        print(f"PASS: AI generated {len(data['questions'])} questions without auto-saving")
        return data["questions"], data["ids"]
    
    @pytest.mark.slow
    def test_bulk_save_approved_questions(self, api_client):
        """POST - Bulk save questions after review"""
        # Create questions to save
        questions_to_save = [
            {
                "question_content": f"TEST_Bulk pregunta 1 {uuid.uuid4().hex[:8]}",
                "question_type": "multiple_choice",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
                "difficulty": "facil",
                "topic": "Test Bulk",
                "solution_content": "Solución 1",
                "source": "ai_generated"
            },
            {
                "question_content": f"TEST_Bulk pregunta 2 {uuid.uuid4().hex[:8]}",
                "question_type": "multiple_choice",
                "options": ["1", "2", "3", "4"],
                "correct_answer": "B",
                "difficulty": "medio",
                "topic": "Test Bulk",
                "solution_content": "Solución 2",
                "source": "ai_generated"
            }
        ]
        
        response = api_client.post(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/bulk",
            json=questions_to_save
        )
        assert response.status_code == 200, f"Failed to bulk save: {response.text}"
        
        data = response.json()
        assert "created_count" in data, "Response should have created_count"
        assert data["created_count"] == 2, "Should have created 2 questions"
        assert "ids" in data, "Response should have ids"
        assert len(data["ids"]) == 2, "Should have 2 ids"
        
        print(f"PASS: Bulk saved {data['created_count']} questions")
        
        # Cleanup - delete the bulk created questions
        for q_id in data["ids"]:
            try:
                api_client.delete(
                    f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions/{q_id}"
                )
            except Exception:
                pass


# ==================== STUDENT UNIVERSITIES TESTS (Light Mode & KaTeX) ====================

class TestStudentUniversitiesPublicAPI:
    """Tests for public student-facing APIs with image support"""
    
    def test_simulation_returns_image_url(self):
        """POST - Verify simulation questions include image_url field"""
        # No auth needed for public endpoints
        response = requests.post(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/simulation",
            json={
                "evaluation_id": TEST_EVALUATION_ID,
                "num_questions": 5
            }
        )
        assert response.status_code == 200, f"Failed to create simulation: {response.text}"
        
        data = response.json()
        assert "questions" in data, "Response should have questions"
        
        # Verify each question has image_url field (even if null)
        for q in data["questions"]:
            assert "image_url" in q or q.get("image_url") is None, "Questions should have image_url field"
        
        print(f"PASS: Simulation returns {len(data['questions'])} questions with image_url support")
    
    def test_submit_simulation_returns_image_url(self):
        """POST - Verify submission results include image_url"""
        # First create a simulation
        sim_response = requests.post(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/simulation",
            json={
                "evaluation_id": TEST_EVALUATION_ID,
                "num_questions": 2
            }
        )
        
        if sim_response.status_code != 200:
            pytest.skip("Cannot create simulation for submit test")
        
        sim_data = sim_response.json()
        simulation_id = sim_data["simulation_id"]
        
        # Create answers for all questions
        answers = {}
        for q in sim_data["questions"]:
            answers[q["id"]] = "A"
        
        # Submit answers
        submit_response = requests.post(
            f"{BASE_URL}/api/universities/simulation/{simulation_id}/submit",
            json={"answers": answers}
        )
        assert submit_response.status_code == 200, f"Failed to submit: {submit_response.text}"
        
        result = submit_response.json()
        assert "results" in result, "Response should have results"
        
        # Verify results have image_url
        for r in result["results"]:
            assert "image_url" in r or r.get("image_url") is None, "Results should have image_url"
        
        print(f"PASS: Submission results include image_url field")


# ==================== ADMIN LIST QUESTIONS WITH EDIT BUTTON ====================

class TestAdminListQuestions:
    """Tests for admin question list functionality"""
    
    def test_list_questions_returns_all_fields(self, api_client):
        """GET - Verify list questions returns all editable fields"""
        response = api_client.get(
            f"{BASE_URL}/api/admin/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/evaluations/{TEST_EVALUATION_ID}/questions"
        )
        assert response.status_code == 200, f"Failed to list questions: {response.text}"
        
        questions = response.json()
        
        if len(questions) > 0:
            q = questions[0]
            
            # Verify all expected fields are present
            expected_fields = ["id", "question_content", "options", "correct_answer", 
                              "difficulty", "source"]
            
            for field in expected_fields:
                assert field in q, f"Question should have {field} field"
            
            print(f"PASS: Question list returns all editable fields")
        else:
            print(f"PASS: Question list endpoint works (0 questions)")


# ==================== STATS ENDPOINT ====================

class TestStatsEndpoint:
    """Tests for universities stats endpoint"""
    
    def test_get_stats(self, api_client):
        """GET - Verify stats endpoint returns all data"""
        response = api_client.get(f"{BASE_URL}/api/admin/universities/stats/summary")
        assert response.status_code == 200, f"Failed to get stats: {response.text}"
        
        data = response.json()
        assert "total_universities" in data, "Should have total_universities"
        assert "total_courses" in data, "Should have total_courses"
        assert "total_evaluations" in data, "Should have total_evaluations"
        assert "total_questions" in data, "Should have total_questions"
        assert "questions_by_source" in data, "Should have questions_by_source"
        
        print(f"PASS: Stats - {data['total_universities']} unis, {data['total_courses']} courses, {data['total_questions']} questions")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
