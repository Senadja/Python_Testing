import json
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages



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
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    places_requested = request.form['places']

    if not places_requested:
        flash('Please enter the number of places you want to book.')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    competition = [c for c in competitions if c['name'] == competition_name][0]
    club = [c for c in clubs if c['name'] == club_name][0]

    if int(places_requested) <= 0:
        flash('Please enter a valid number of places.')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    if int(places_requested) > int(competition['numberOfPlaces']):
        flash('Not enough places available for booking.')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - int(places_requested)
    flash('Booking successful!')
    return redirect(url_for('index'))



# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))