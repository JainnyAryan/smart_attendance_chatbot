import unittest
from backend.services.intent_processing import get_best_intent


class ChatbotIntentTest(unittest.TestCase):
    def setUp(self):
        """Set up test cases with example inputs and expected intents."""
        self.test_cases = [
            {"message": "hello", "expected_intent": "greeting"},
            {"message": "helloooo man!", "expected_intent": "greeting"},
            {"message": "What are my working hours?",
                "expected_intent": "working_hours"},
            {"message": "Tell me my attendance summary",
                "expected_intent": "attendance_summary"},
            {"message": "I want to apply for leave",
                "expected_intent": "leave_request"},
            {"message": "Check in for work", "expected_intent": "check_in"},
            {"message": "Check out", "expected_intent": "check_out"},
            {"message": "What is the status of my leave?",
                "expected_intent": "leave_status"},
            {"message": "Who am I?", "expected_intent": "unknown"},
            {"message": "When will I receive my salary?",
                "expected_intent": "payroll"},
            {"message": "Schedule a meeting with HR",
                "expected_intent": "meeting_schedule"},
            {"message": "Can I work from home?",
                "expected_intent": "work_from_home"}
        ]

    def test_intent_recognition(self):
        """Test intent recognition using different test cases."""
        for case in self.test_cases:
            message = case["message"]
            expected_intent = case["expected_intent"]

            intent, confidence = get_best_intent(message)

            print(f"\n🗣️ User: {message}")
            print(
                f"🤖 Intent: {intent} (Expected: {expected_intent}, Confidence: {confidence:.2f})")

            self.assertEqual(intent, expected_intent,
                             f"Expected '{expected_intent}' but got '{intent}'")
            self.assertGreaterEqual(
                confidence, 0.3, f"Confidence too low for message: {message}")


if __name__ == "__main__":
    unittest.main()
