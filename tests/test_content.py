import unittest
from src.content.static_site_generator import generate_static_html

class TestContent(unittest.TestCase):

    def test_generate_static_html(self):
        markdown_input = "# Test Heading\n\nThis is a **test** paragraph."
        html_output = generate_static_html(markdown_input)

        self.assertIsInstance(html_output, str)
        self.assertIn("<h1>Test Heading</h1>", html_output)
        self.assertIn("<p>This is a <strong>test</strong> paragraph.</p>", html_output)

if __name__ == '__main__':
    unittest.main()
