# website/tests/test_app.py

import unittest
import sys
import os


# Add the parent directory to sys.path:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the AI-updated website!", response.data)

if __name__ == "__main__":
    unittest.main()
