"""
Test suite for Remy educational platform API endpoints
Testing: courses, chapters, lessons, formulas, quiz, progress, and admin endpoints
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestPublicEndpoints:
    """Test public API endpoints for students"""
    
    def test_root_endpoint(self):
        """Test root API endpoint returns welcome message"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Remy" in data["message"]
        print("✓ Root endpoint working")
    
    def test_get_courses(self):
        """Test getting list of courses"""
        response = requests.get(f"{BASE_URL}/api/courses")
        assert response.status_code == 200
        courses = response.json()
        assert isinstance(courses, list)
        if len(courses) > 0:
            course = courses[0]
            assert "id" in course
            assert "title" in course
            assert "description" in course
            assert "level" in course
        print(f"✓ Courses endpoint returned {len(courses)} courses")
    
    def test_get_specific_course(self):
        """Test getting a specific course by ID"""
        response = requests.get(f"{BASE_URL}/api/courses/course-001")
        assert response.status_code == 200
        course = response.json()
        assert course["id"] == "course-001"
        assert "title" in course
        assert "description" in course
        print(f"✓ Course detail endpoint working - got '{course['title']}'")
    
    def test_get_nonexistent_course(self):
        """Test getting a course that doesn't exist returns 404"""
        response = requests.get(f"{BASE_URL}/api/courses/nonexistent-course")
        assert response.status_code == 404
        print("✓ Nonexistent course returns 404")
    
    def test_get_course_chapters(self):
        """Test getting chapters for a course"""
        response = requests.get(f"{BASE_URL}/api/courses/course-001/chapters")
        assert response.status_code == 200
        chapters = response.json()
        assert isinstance(chapters, list)
        if len(chapters) > 0:
            chapter = chapters[0]
            assert "id" in chapter
            assert "title" in chapter
            assert "course_id" in chapter
        print(f"✓ Course chapters endpoint returned {len(chapters)} chapters")
    
    def test_get_chapter_lessons(self):
        """Test getting lessons for a chapter"""
        response = requests.get(f"{BASE_URL}/api/chapters/chapter-001/lessons")
        assert response.status_code == 200
        lessons = response.json()
        assert isinstance(lessons, list)
        if len(lessons) > 0:
            lesson = lessons[0]
            assert "id" in lesson
            assert "title" in lesson
            assert "content" in lesson
            # Verify LaTeX content is present in lesson
            assert "$$" in lesson["content"] or "\\lim" in lesson["content"] or "fórmula" in lesson["content"].lower()
        print(f"✓ Chapter lessons endpoint returned {len(lessons)} lessons")
    
    def test_get_specific_lesson(self):
        """Test getting a specific lesson by ID"""
        # First get lessons from chapter to get a valid lesson ID
        lessons_response = requests.get(f"{BASE_URL}/api/chapters/chapter-001/lessons")
        lessons = lessons_response.json()
        if len(lessons) > 0:
            lesson_id = lessons[0]["id"]
            response = requests.get(f"{BASE_URL}/api/lessons/{lesson_id}")
            assert response.status_code == 200
            lesson = response.json()
            assert lesson["id"] == lesson_id
            assert "content" in lesson
            print(f"✓ Lesson detail endpoint working - got '{lesson['title']}'")
        else:
            pytest.skip("No lessons available to test")


class TestFormulasEndpoints:
    """Test formulas API endpoints"""
    
    def test_search_formulas_empty_query(self):
        """Test searching formulas with empty query returns all formulas"""
        response = requests.post(
            f"{BASE_URL}/api/formulas/search",
            json={"query": "", "course_id": None}
        )
        assert response.status_code == 200
        formulas = response.json()
        assert isinstance(formulas, list)
        if len(formulas) > 0:
            formula = formulas[0]
            assert "id" in formula
            assert "name" in formula
            assert "latex" in formula
            assert "description" in formula
        print(f"✓ Formulas search returned {len(formulas)} formulas")
    
    def test_search_formulas_with_query(self):
        """Test searching formulas with specific query"""
        response = requests.post(
            f"{BASE_URL}/api/formulas/search",
            json={"query": "Derivadas", "course_id": None}
        )
        assert response.status_code == 200
        formulas = response.json()
        assert isinstance(formulas, list)
        # All returned formulas should relate to Derivadas
        for formula in formulas:
            assert "Derivada" in formula.get("topic", "") or "Derivada" in formula.get("name", "") or "derivada" in formula.get("description", "").lower()
        print(f"✓ Formulas search with query returned {len(formulas)} matching formulas")
    
    def test_search_formulas_by_course(self):
        """Test filtering formulas by course_id"""
        response = requests.post(
            f"{BASE_URL}/api/formulas/search",
            json={"query": "", "course_id": "course-001"}
        )
        assert response.status_code == 200
        formulas = response.json()
        assert isinstance(formulas, list)
        # All returned formulas should belong to course-001
        for formula in formulas:
            assert formula.get("course_id") == "course-001"
        print(f"✓ Formulas filtered by course returned {len(formulas)} formulas")


class TestQuizEndpoints:
    """Test quiz API endpoints"""
    
    def test_quiz_history_empty(self):
        """Test getting quiz history for a user (may be empty)"""
        response = requests.get(f"{BASE_URL}/api/quiz/history/demo-user-001")
        assert response.status_code == 200
        quizzes = response.json()
        assert isinstance(quizzes, list)
        print(f"✓ Quiz history returned {len(quizzes)} quizzes")
    
    def test_quiz_start_insufficient_questions(self):
        """Test starting a quiz with insufficient questions shows proper error"""
        response = requests.post(
            f"{BASE_URL}/api/quiz/start",
            json={
                "user_id": "test-user",
                "course_id": "course-001",
                "topic": "Derivadas",
                "num_questions": 10  # More than available (only 2 Derivadas questions)
            }
        )
        # Should fail because not enough questions
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "preguntas" in data["detail"].lower() or "disponibles" in data["detail"].lower()
        print("✓ Quiz start with insufficient questions returns proper error")
    
    def test_quiz_start_success(self):
        """Test starting a quiz with available questions"""
        response = requests.post(
            f"{BASE_URL}/api/quiz/start",
            json={
                "user_id": "test-user",
                "course_id": "course-001",
                "topic": "Derivadas",
                "num_questions": 2  # Match available questions
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "quiz_id" in data
        assert "questions" in data
        assert len(data["questions"]) == 2
        # Verify question structure
        for q in data["questions"]:
            assert "question_text" in q or "question" in q
            assert "options" in q
        print(f"✓ Quiz started successfully with {len(data['questions'])} questions")


class TestProgressEndpoints:
    """Test progress tracking API endpoints"""
    
    def test_get_user_progress(self):
        """Test getting progress for a user"""
        response = requests.get(f"{BASE_URL}/api/progress/demo-user-001")
        assert response.status_code == 200
        progress = response.json()
        assert isinstance(progress, list)
        print(f"✓ Progress endpoint returned {len(progress)} progress records")


class TestAdminAuthentication:
    """Test admin authentication endpoints"""
    
    def test_admin_login_success(self):
        """Test admin login with correct credentials"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={
                "username": "admin",
                "password": "#Alex060625"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
        print("✓ Admin login successful")
        return data["access_token"]
    
    def test_admin_login_wrong_password(self):
        """Test admin login with incorrect password"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={
                "username": "admin",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        print("✓ Admin login with wrong password returns 401")
    
    def test_admin_login_wrong_username(self):
        """Test admin login with incorrect username"""
        response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={
                "username": "wronguser",
                "password": "#Alex060625"
            }
        )
        assert response.status_code == 401
        print("✓ Admin login with wrong username returns 401")
    
    def test_admin_verify_token(self):
        """Test verifying admin token"""
        # First login to get token
        login_response = requests.post(
            f"{BASE_URL}/api/admin/login",
            json={
                "username": "admin",
                "password": "#Alex060625"
            }
        )
        token = login_response.json()["access_token"]
        
        # Verify the token
        response = requests.get(
            f"{BASE_URL}/api/admin/verify",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["verified"] == True
        assert data["username"] == "admin"
        print("✓ Admin token verification successful")


class TestMaterialsEndpoints:
    """Test materials API endpoints"""
    
    def test_get_course_materials(self):
        """Test getting materials for a course"""
        response = requests.get(f"{BASE_URL}/api/materials/course-001")
        assert response.status_code == 200
        materials = response.json()
        assert isinstance(materials, list)
        print(f"✓ Materials endpoint returned {len(materials)} materials")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
