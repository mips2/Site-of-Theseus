import unittest
import sys
import os

# Add the parent directory to sys.path:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from website/app.py
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        # Test the response of the homepage
        response = self.client.get("/")
        
        # If the user is not logged in, expect a 302 redirect to /login
        if b"Redirecting" in response.data:
            self.assertEqual(
                response.status_code,
                302,
                f"Expected 302 redirect when not logged in, got {response.status_code} - body: {response.data}",
            )
            self.assertIn(
                b"/login",
                response.data,
                "Expected redirect to /login, but the response did not indicate this.",
            )
        else:
            # If not redirected, expect a 200 OK status
            self.assertEqual(
                response.status_code,
                200,
                f"Expected 200 OK, but got {response.status_code} - body: {response.data}",
            )

        # Ensure no "Traceback" in the HTML (a common sign of a Python exception)
        self.assertNotIn(b"Traceback", response.data, "Flask error/exception occurred")


if __name__ == "__main__":
    unittest.main()
