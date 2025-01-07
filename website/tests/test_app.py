# website/tests/test_app.py

import unittest
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
