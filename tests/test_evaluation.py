import unittest
from src.evaluation.grade import grade_submission
from src.evaluation.feedback import generate_feedback

class TestEvaluation(unittest.TestCase):

    def test_grade_submission(self):
        rubric = {"criteria1": 0.5, "criteria2": 0.5}

        # Test with a "good" submission
        score_good = grade_submission("This is a good submission.", rubric)
        self.assertEqual(score_good, 90)

        # Test with an "average" submission
        score_average = grade_submission("This is an average submission.", rubric)
        self.assertEqual(score_average, 70)

        # Test with a general submission
        score_general = grade_submission("This is a submission.", rubric)
        self.assertEqual(score_general, 50)

    def test_generate_feedback(self):
        # Test with a high score
        feedback_high = generate_feedback(95)
        self.assertEqual(feedback_high, "Excellent work! Keep it up.")

        # Test with a medium score
        feedback_medium = generate_feedback(65)
        self.assertEqual(feedback_medium, "Good effort. There's room for improvement.")

        # Test with a low score
        feedback_low = generate_feedback(45)
        self.assertEqual(feedback_low, "Needs significant improvement. Please review the material.")

if __name__ == '__main__':
    unittest.main()
