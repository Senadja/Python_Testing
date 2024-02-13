import json
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages

def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        for club in listOfClubs:
            club['total_reserved'] = 0  # Initialiser 'total_reserved' pour chaque club
            club['reserved'] = {}  # Initialiser 'reserved' pour chaque club
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    messages = get_flashed_messages()
    return render_template('index.html', messages=messages)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form['email']
    if not email:
        flash('Please enter your email.')
        return redirect(url_for('index'))

    club = [club for club in clubs if club['email'] == email]
    if not club:
        flash('Email not found in the database.')
        return redirect(url_for('index'))
    
    club = club[0]
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_required_str = request.form['places']  # Capturer la valeur comme une chaîne

    # Vérifier si le champ pour le nombre de places est vide
    if not places_required_str:
        flash('Please enter the number of places you want to book.')
        return redirect(url_for('book', competition=competition_name, club=club_name))  # Rediriger vers la page de réservation

    # Convertir le nombre de places en entier
    try:
        places_required = int(places_required_str)
    except ValueError:
        flash('Please enter a valid number for the places.')
        return redirect(url_for('book', competition=competition_name, club=club_name))  # Rediriger vers la page de réservation

    # Vérifier que le nombre de places demandées est positif
    if places_required <= 0:
        flash('Please enter a valid number of places (greater than zero).')
        return redirect(url_for('book', competition=competition_name, club=club_name))  # Rediriger vers la page de réservation

    # Recherche de la compétition et du club dans la liste des compétitions et des clubs
    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    if competition and club:
        # Vérifier s'il y a suffisamment de places disponibles dans la compétition
        if int(competition['numberOfPlaces']) >= places_required:
            # Vérifier si le club peut réserver plus de places
            if club['total_reserved'] + places_required <= 12:
                # Déduire les points du club
                club_points = int(club['points'])
                if club_points >= places_required:
                    club_points -= places_required
                    club['points'] = str(club_points)  # Mettre à jour le nombre de points du club
                    # Mettre à jour le nombre total de places réservées par le club
                    club['total_reserved'] += places_required
                    # Mettre à jour le nombre de places disponibles dans la compétition
                    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)
                    # Message de succès
                    flash('Great-booking complete!')
                else:
                    flash('Insufficient points for booking!')
            else:
                flash('You cannot buy more than 12 places.')
        else:
            flash('Insufficient places available!')
    else:
        flash('Competition or club not found!')

    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    flash('You have been logged out.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
