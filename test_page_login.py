import unittest
from server import app


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        response = self.app.post('/showSummary', data=dict(email='john@simplylift.co'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, john@simplylift.co', response.data)

    def test_login_with_empty_email(self):
        response = self.app.post('/showSummary', data=dict(email=''))
        self.assertEqual(response.status_code, 302)

    def test_login_with_unknown_email(self):
        response = self.app.post('/showSummary', data=dict(email='unknown@example.com'))
        self.assertEqual(response.status_code, 302)

    def test_login_with_invalid_email_format(self):
        response = self.app.post('/showSummary', data=dict(email='invalid_email_format'))
        self.assertEqual(response.status_code, 302)

    def test_login_with_insufficient_points(self):
        response = self.app.post('/showSummary', data=dict(email='admin@irontemple.com'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Insufficient points for booking!', response.data)

    def test_login_page_post_method(self):
        response = self.app.post('/')
        self.assertEqual(response.status_code, 405)

    def test_login_page_get_method(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()