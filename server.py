import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
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
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    entered_email = request.form['email']

    # Vérifie si l'e-mail est dans la liste des clubs
    if any(club['email'] == entered_email for club in clubs):
        # Si oui, récupère le club correspondant
        club = next(club for club in clubs if club['email'] == entered_email)
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        # Si l'e-mail n'est pas dans la liste des clubs, affiche un message demandant de saisir un e-mail déjà référencé
        flash('Invalid email. Please enter a registered email.')
        # Ne redirige pas immédiatement, laisse la page actuelle (index.html) être rendue
        return redirect(url_for('index'))



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
    places_required = int(request.form['places'])

    # Recherche de la compétition et du club dans la liste des compétitions et des clubs
    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    if competition and club:
        # Vérifier s'il y a suffisamment de places disponibles dans la compétition
        if int(competition['numberOfPlaces']) >= places_required:
            # Déduire les points du club
            club_points = int(club['points'])
            if club_points >= places_required:
                club_points -= places_required
                club['points'] = str(club_points)  # Mettre à jour le nombre de points du club
                # Mettre à jour le nombre de places disponibles dans la compétition
                competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)
                # Message de succès
                flash('Great-booking complete!')
            else:
                flash('Insufficient points for booking!')
        else:
            flash('Insufficient places available!')
    else:
        flash('Competition or club not found!')

    return render_template('welcome.html', club=club, competitions=competitions)




# TODO: Add route for points display


@app.route('/logout')
def logout():
    flash('You have been logged out.')
    return redirect(url_for('index'))