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
