import unittest
from flask import Flask, render_template
from server import app

class TestLoginPage(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_page_loads_successfully(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        response = self.app.get('/')
        self.assertIn(b'<title>GUDLFT Registration</title>', response.data)

    def test_form_present(self):
        response = self.app.get('/')
        self.assertIn(b'<form action="showSummary" method="post">', response.data)

    def test_email_input_present(self):
        response = self.app.get('/')
        self.assertIn(b'<input type="email" name="email" id=""/>', response.data)

    def test_submit_button_present(self):
        response = self.app.get('/')
        self.assertIn(b'<button type="submit">Enter</button>', response.data)

if __name__ == '__main__':
    unittest.main()
