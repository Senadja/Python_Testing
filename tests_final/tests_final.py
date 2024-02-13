import unittest
from server import app, competitions, clubs

class TestPurchasePlaces(unittest.TestCase):

    def test_purchase_places_negative(self):
        with app.test_client() as client:
            # Tente d'acheter un nombre négatif de places
            club_name = 'Simply Lift'
            original_points = next((club['points'] for club in clubs if club['name'] == club_name), None)
            data = {'competition': 'Spring Festival', 'club': club_name, 'places': '-5'}
            response = client.post('/purchasePlaces', data=data, follow_redirects=True)
            updated_points = next((club['points'] for club in clubs if club['name'] == club_name), None)

            # Vérifie que le nombre de points du club n'a pas changé (est toujours le même)
            self.assertEqual(int(updated_points), int(original_points))

if __name__ == '__main__':
    unittest.main()


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
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b"You cannot register for this event as it has already passed.", response.data)

if __name__ == "__main__":
    unittest.main()


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


import unittest
from server import app

class TestLogoutFunction(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_logout_redirect(self):
        # Effectuer une requête GET vers la route /logout
        response = self.app.get('/logout', follow_redirects=True)
        
        # Vérifier si la redirection vers la page d'accueil a eu lieu
        self.assertEqual(response.status_code, 200)  # Code de statut 200 indique succès
        self.assertIn(b'index', response.data)  # Vérifie la présence du contenu de la page d'accueil
        
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

import unittest
from server import app, competitions, clubs

class TestPurchasePlaces(unittest.TestCase):

    def test_purchase_places_sufficient_points(self):
        with app.test_client() as client:
            # Assurez-vous que le club a suffisamment de points
            club_name = 'Simply Lift'
            original_points = next((club['points'] for club in clubs if club['name'] == club_name), None)
            places_to_book = 3
            data = {'competition': 'Spring Festival', 'club': club_name, 'places': places_to_book}
            response = client.post('/purchasePlaces', data=data, follow_redirects=True)
            updated_points = next((club['points'] for club in clubs if club['name'] == club_name), None)

            # Vérifie que le nombre de points du club a été correctement réduit
            self.assertEqual(int(updated_points), int(original_points) - places_to_book)

    def test_purchase_places_insufficient_points(self):
        with app.test_client() as client:
            # Assurez-vous que le club n'a pas suffisamment de points
            club_name = 'Iron Temple'
            original_points = next((club['points'] for club in clubs if club['name'] == club_name), None)
            places_to_book = 15  # Supposons que cela dépasse le nombre de points disponibles
            data = {'competition': 'Spring Festival', 'club': club_name, 'places': places_to_book}
            response = client.post('/purchasePlaces', data=data, follow_redirects=True)
            updated_points = next((club['points'] for club in clubs if club['name'] == club_name), None)

            # Vérifie que le nombre de points du club n'a pas changé (est toujours le même)
            self.assertEqual(int(updated_points), int(original_points))

if __name__ == '__main__':
    unittest.main()
