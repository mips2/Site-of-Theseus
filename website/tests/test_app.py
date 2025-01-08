import unittest
import sys
import os

# Add the parent directory to sys.path:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import from website/app.py
# (If your Flask app is in website/app.py, do this instead of from app import app)
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        # Just check for a 200 OK status
        response = self.client.get("/")
        self.assertEqual(
            response.status_code,
            200,
            f"Home page returned {response.status_code} - body: {response.data}",
        )

        # Also ensure no "Traceback" in the HTML (a common sign of a Python exception)
        self.assertNotIn(b"Traceback", response.data, "Flask error/exception occurred")


if __name__ == "__main__":
    unittest.main()
