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
