import unittest
from src.syllabus.prompts import generate_syllabus_prompt

class TestSyllabus(unittest.TestCase):

    def test_generate_syllabus_prompt(self):
        # Test that generate_syllabus_prompt returns a string
        prompt = generate_syllabus_prompt("web_development")
        self.assertIsInstance(prompt, str)
        self.assertTrue(len(prompt) > 0)
        self.assertIn("Web Development", prompt)
        self.assertIn("Introduction to HTML", prompt)
        self.assertIn("Introduction to CSS", prompt)
        self.assertIn("Introduction to JavaScript", prompt)

    def test_generate_syllabus_prompt_invalid_path(self):
        # Test with an invalid learning path
        prompt = generate_syllabus_prompt("non_existent_path")
        self.assertEqual(prompt, "Error: Learning path not found.")

if __name__ == '__main__':
    unittest.main()
