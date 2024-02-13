import unittest
from datetime import datetime
from server import app, competitions

class TestEventDate(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_event_in_future(self):
        # Choisissez une compétition dans le futur
        future_event = competitions[0]
        future_event_date = datetime.strptime(future_event['date'], '%Y-%m-%d %H:%M:%S')

        # Vérifiez que l'accès à la page de réservation est possible
        response = self.app.get(f"/book/{future_event['name']}/Sample Club")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Places', response.data)

    def test_event_in_past(self):
        # Choisissez une compétition dans le passé
        past_event = competitions[1]
        past_event_date = datetime.strptime(past_event['date'], '%Y-%m-%d %H:%M:%S')

        # Vérifiez que l'accès à la page de réservation est impossible
        response = self.app.get(f"/book/{past_event['name']}/Sample Club")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You cannot register for this event as it has already passed.", response.data)

if __name__ == "__main__":
    unittest.main()
