import requests
import json
import sys
from datetime import datetime

class RemyAPITester:
    def __init__(self, base_url="https://remy-exam-prep.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.user_id = "demo-user-001"

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)

            print(f"   Status: {response.status_code}")
            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed")
                try:
                    return response.json() if response.content else {}
                except:
                    return {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                if response.content:
                    try:
                        error_detail = response.json()
                        print(f"   Error: {error_detail}")
                    except:
                        print(f"   Response: {response.text[:200]}")
                return {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root Endpoint", "GET", "", 200)

    def test_get_courses(self):
        """Test fetching courses"""
        response = self.run_test("Get Courses", "GET", "courses", 200)
        if response and isinstance(response, list):
            print(f"   Found {len(response)} courses")
            return response
        return []

    def test_chat_with_remy(self):
        """Test chat functionality with GPT 5.2"""
        data = {
            "user_id": self.user_id,
            "message": "¿Cuál es la derivada de x²?",
            "course_context": "Cálculo"
        }
        print("   Testing GPT 5.2 integration...")
        response = self.run_test("Chat with Remy", "POST", "chat", 200, data, timeout=60)
        
        if response and 'message' in response:
            print(f"   AI Response: {response['message'][:100]}...")
            return True
        return False

    def test_quiz_generation(self, courses):
        """Test quiz generation with GPT 5.2"""
        if not courses:
            print("   ❌ No courses available for quiz generation")
            return False
            
        data = {
            "user_id": self.user_id,
            "course_id": courses[0]['id'],
            "topic": "derivadas",
            "num_questions": 3
        }
        print("   Testing GPT 5.2 quiz generation...")
        response = self.run_test("Generate Quiz", "POST", "quiz/generate", 200, data, timeout=60)
        
        if response and 'questions' in response:
            print(f"   Generated {len(response['questions'])} questions")
            return True
        return False

    def test_formulas_search(self):
        """Test formula search functionality"""
        data = {
            "query": "derivada",
            "course_id": None
        }
        response = self.run_test("Search Formulas", "POST", "formulas/search", 200, data)
        
        if isinstance(response, list):
            print(f"   Found {len(response)} formulas")
            return len(response)
        return 0

    def test_user_progress(self):
        """Test user progress endpoint"""
        response = self.run_test("Get User Progress", "GET", f"progress/{self.user_id}", 200)
        
        if isinstance(response, list):
            print(f"   Found progress for {len(response)} courses")
            return True
        return False

    def test_user_quizzes(self):
        """Test user quizzes endpoint"""
        response = self.run_test("Get User Quizzes", "GET", f"quizzes/{self.user_id}", 200)
        
        if isinstance(response, list):
            print(f"   Found {len(response)} user quizzes")
            return True
        return False

    def test_chat_history(self):
        """Test chat history endpoint"""
        response = self.run_test("Get Chat History", "GET", f"chat/history/{self.user_id}", 200)
        
        if isinstance(response, list):
            print(f"   Found {len(response)} chat messages")
            return True
        return False

def main():
    print("🚀 Starting Remy API Testing...")
    print("=" * 50)
    
    tester = RemyAPITester()
    
    # Test basic connectivity
    tester.test_root_endpoint()
    
    # Test course management
    courses = tester.test_get_courses()
    
    # Test AI-powered features (GPT 5.2)
    chat_works = tester.test_chat_with_remy()
    quiz_works = tester.test_quiz_generation(courses)
    
    # Test data retrieval
    formula_count = tester.test_formulas_search()
    tester.test_user_progress()
    tester.test_user_quizzes()
    tester.test_chat_history()
    
    # Results summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Tests passed: {tester.tests_passed}/{tester.tests_run}")
    print(f"Success rate: {(tester.tests_passed/tester.tests_run*100):.1f}%")
    
    print("\n📋 KEY FINDINGS:")
    print(f"• Courses available: {len(courses)}")
    print(f"• Formulas available: {formula_count}")
    print(f"• GPT 5.2 Chat integration: {'✅ Working' if chat_works else '❌ Failed'}")
    print(f"• GPT 5.2 Quiz generation: {'✅ Working' if quiz_works else '❌ Failed'}")
    
    # Determine overall success
    critical_features = [chat_works, quiz_works, len(courses) > 0]
    success_rate = tester.tests_passed / tester.tests_run
    
    if success_rate >= 0.8 and all(critical_features):
        print("\n🎉 OVERALL STATUS: HEALTHY")
        return 0
    else:
        print("\n⚠️ OVERALL STATUS: NEEDS ATTENTION")
        return 1

if __name__ == "__main__":
    sys.exit(main())