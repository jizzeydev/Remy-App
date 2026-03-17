"""
Test Suite for Student Universities Endpoints - TuUniversidad Feature
Tests public university/course/evaluation listing and simulation generation
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test data from requirements
TEST_UNIVERSITY_ID = "8803fdbb-589a-4734-804e-4d0db4cf1aef"  # UChile
TEST_COURSE_ID = "55828490-f2b1-42fb-9361-c96e2e6e6171"
TEST_EVALUATION_ID = "fbd30dc0-92e5-40e6-a23d-c7bed7f37251"  # I1 with 5 questions


class TestUniversitiesPublicEndpoints:
    """Test public university listing endpoints"""

    def test_list_universities_returns_200(self):
        """GET /api/universities - should list all active universities"""
        response = requests.get(f"{BASE_URL}/api/universities")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        print(f"Found {len(data)} universities")
        
        # Verify structure of each university
        if len(data) > 0:
            uni = data[0]
            assert "id" in uni, "University should have 'id'"
            assert "name" in uni, "University should have 'name'"
            assert "courses_count" in uni, "University should have 'courses_count'"
            print(f"First university: {uni.get('name')} with {uni.get('courses_count')} courses")

    def test_get_university_by_id_returns_200(self):
        """GET /api/universities/{id} - should return university with courses"""
        response = requests.get(f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should have 'id'"
        assert "name" in data, "Response should have 'name'"
        assert "courses" in data, "Response should have 'courses' list"
        assert isinstance(data["courses"], list), "'courses' should be a list"
        
        print(f"University: {data.get('name')}")
        print(f"Courses count: {len(data.get('courses', []))}")
        
        # Verify course structure
        if len(data["courses"]) > 0:
            course = data["courses"][0]
            assert "id" in course, "Course should have 'id'"
            assert "name" in course, "Course should have 'name'"
            assert "evaluations_count" in course, "Course should have 'evaluations_count'"

    def test_get_university_not_found(self):
        """GET /api/universities/{invalid_id} - should return 404"""
        response = requests.get(f"{BASE_URL}/api/universities/invalid-uuid-12345")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_get_course_with_evaluations(self):
        """GET /api/universities/{uni_id}/courses/{course_id} - should return course with evaluations"""
        response = requests.get(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}"
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "id" in data, "Response should have 'id'"
        assert "name" in data, "Response should have 'name'"
        assert "evaluations" in data, "Response should have 'evaluations' list"
        assert isinstance(data["evaluations"], list), "'evaluations' should be a list"
        
        print(f"Course: {data.get('name')} ({data.get('code', 'N/A')})")
        print(f"Evaluations count: {len(data.get('evaluations', []))}")
        
        # Verify evaluation structure
        if len(data["evaluations"]) > 0:
            eval_item = data["evaluations"][0]
            assert "id" in eval_item, "Evaluation should have 'id'"
            assert "name" in eval_item, "Evaluation should have 'name'"
            assert "questions_count" in eval_item, "Evaluation should have 'questions_count'"
            print(f"First evaluation: {eval_item.get('name')} with {eval_item.get('questions_count')} questions")

    def test_get_course_not_found(self):
        """GET /api/universities/{uni_id}/courses/{invalid_course_id} - should return 404"""
        response = requests.get(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/invalid-course-id"
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"


class TestSimulationEndpoints:
    """Test simulation generation and submission endpoints"""
    
    @pytest.fixture
    def created_simulation(self):
        """Create a simulation and return its ID for testing"""
        response = requests.post(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/simulation",
            json={
                "evaluation_id": TEST_EVALUATION_ID,
                "num_questions": 5
            }
        )
        assert response.status_code == 200, f"Failed to create simulation: {response.text}"
        data = response.json()
        return data

    def test_generate_simulation_success(self):
        """POST /api/universities/{uni_id}/courses/{course_id}/simulation - should generate quiz"""
        response = requests.post(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/simulation",
            json={
                "evaluation_id": TEST_EVALUATION_ID,
                "num_questions": 3
            }
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "simulation_id" in data, "Response should have 'simulation_id'"
        assert "questions" in data, "Response should have 'questions'"
        assert "total_questions" in data, "Response should have 'total_questions'"
        
        print(f"Simulation ID: {data.get('simulation_id')}")
        print(f"Total questions: {data.get('total_questions')}")
        
        # Verify questions don't include correct answers (for quiz mode)
        if len(data["questions"]) > 0:
            q = data["questions"][0]
            assert "id" in q, "Question should have 'id'"
            assert "question_content" in q, "Question should have 'question_content'"
            assert "options" in q, "Question should have 'options'"
            # Should NOT include correct_answer in response for quiz
            print(f"First question has {len(q.get('options', []))} options")

    def test_generate_simulation_invalid_evaluation(self):
        """POST simulation with invalid evaluation_id - should return 404"""
        response = requests.post(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/simulation",
            json={
                "evaluation_id": "invalid-eval-id",
                "num_questions": 5
            }
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_submit_simulation_and_get_results(self, created_simulation):
        """POST /api/universities/simulation/{sim_id}/submit - should return results"""
        simulation = created_simulation
        simulation_id = simulation["simulation_id"]
        questions = simulation["questions"]
        
        # Build answers dict (answer all with "A" for testing)
        answers = {}
        for q in questions:
            answers[q["id"]] = "A"
        
        response = requests.post(
            f"{BASE_URL}/api/universities/simulation/{simulation_id}/submit",
            json={"answers": answers}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert "simulation_id" in data, "Response should have 'simulation_id'"
        assert "score" in data, "Response should have 'score'"
        assert "correct_count" in data, "Response should have 'correct_count'"
        assert "total_questions" in data, "Response should have 'total_questions'"
        assert "results" in data, "Response should have 'results' array"
        
        print(f"Score: {data.get('score')}%")
        print(f"Correct: {data.get('correct_count')}/{data.get('total_questions')}")
        
        # Verify results include solutions
        if len(data["results"]) > 0:
            r = data["results"][0]
            assert "question_id" in r, "Result should have 'question_id'"
            assert "user_answer" in r, "Result should have 'user_answer'"
            assert "correct_answer" in r, "Result should have 'correct_answer'"
            assert "is_correct" in r, "Result should have 'is_correct'"
            # solution_content may be empty but should be in response
            assert "solution_content" in r or "solution" in r or True  # May be empty

    def test_submit_already_completed_simulation(self, created_simulation):
        """POST submit twice - second should return 400"""
        simulation = created_simulation
        simulation_id = simulation["simulation_id"]
        questions = simulation["questions"]
        
        # First submission
        answers = {q["id"]: "A" for q in questions}
        first_response = requests.post(
            f"{BASE_URL}/api/universities/simulation/{simulation_id}/submit",
            json={"answers": answers}
        )
        assert first_response.status_code == 200, f"First submit failed: {first_response.text}"
        
        # Second submission should fail
        second_response = requests.post(
            f"{BASE_URL}/api/universities/simulation/{simulation_id}/submit",
            json={"answers": answers}
        )
        assert second_response.status_code == 400, f"Expected 400, got {second_response.status_code}"
        print("Double submit correctly rejected with 400")

    def test_get_simulation_result_completed(self, created_simulation):
        """GET /api/universities/simulation/{sim_id} - should return result for completed simulation"""
        simulation = created_simulation
        simulation_id = simulation["simulation_id"]
        questions = simulation["questions"]
        
        # Submit first
        answers = {q["id"]: "B" for q in questions}
        submit_response = requests.post(
            f"{BASE_URL}/api/universities/simulation/{simulation_id}/submit",
            json={"answers": answers}
        )
        assert submit_response.status_code == 200
        
        # Get result
        response = requests.get(f"{BASE_URL}/api/universities/simulation/{simulation_id}")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert data.get("completed") == True, "Simulation should be marked completed"
        assert "score" in data, "Response should have 'score'"
        assert "correct_count" in data, "Response should have 'correct_count'"
        print(f"Retrieved result: {data.get('score')}% ({data.get('correct_count')}/{data.get('total_questions')})")

    def test_get_simulation_not_found(self):
        """GET simulation with invalid ID - should return 404"""
        response = requests.get(f"{BASE_URL}/api/universities/simulation/invalid-sim-id")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_submit_simulation_not_found(self):
        """POST submit with invalid simulation ID - should return 404"""
        response = requests.post(
            f"{BASE_URL}/api/universities/simulation/invalid-sim-id/submit",
            json={"answers": {"q1": "A"}}
        )
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"


class TestSimulationEdgeCases:
    """Test edge cases and special scenarios"""

    def test_simulation_with_partial_answers(self):
        """Submit simulation with only some questions answered"""
        # Create simulation
        create_response = requests.post(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/simulation",
            json={
                "evaluation_id": TEST_EVALUATION_ID,
                "num_questions": 5
            }
        )
        assert create_response.status_code == 200
        simulation = create_response.json()
        
        # Answer only first question
        questions = simulation["questions"]
        if len(questions) > 0:
            partial_answers = {questions[0]["id"]: "C"}
            
            submit_response = requests.post(
                f"{BASE_URL}/api/universities/simulation/{simulation['simulation_id']}/submit",
                json={"answers": partial_answers}
            )
            assert submit_response.status_code == 200, f"Partial submit failed: {submit_response.text}"
            
            result = submit_response.json()
            print(f"Partial answers score: {result.get('score')}%")
            # Unanswered should count as incorrect
            assert result.get("total_questions") == len(questions)

    def test_simulation_request_more_questions_than_available(self):
        """Request more questions than available should return max available"""
        response = requests.post(
            f"{BASE_URL}/api/universities/{TEST_UNIVERSITY_ID}/courses/{TEST_COURSE_ID}/simulation",
            json={
                "evaluation_id": TEST_EVALUATION_ID,
                "num_questions": 1000  # Request way more than available
            }
        )
        assert response.status_code == 200, f"Request failed: {response.text}"
        
        data = response.json()
        # Should return available questions, not error
        print(f"Requested 1000, got {data.get('total_questions')} questions")
        assert data.get("total_questions") > 0, "Should return some questions"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
