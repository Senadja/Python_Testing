import unittest
from server import app

class TestLimitPlaces(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def test_limit_places(self):
        response = self.app.post('/purchasePlaces', data={'competition': 'Spring Festival', 'club': 'Simply Lift', 'places': '13'})
        self.assertIn(b'You cannot buy more than 12 places.', response.data)

if __name__ == '__main__':
    unittest.main()
