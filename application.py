from flask import render_template, json, request, Response
import flask_login
import easygui
import flask


# -------------------- define app --------------------

app = flask.Flask(__name__)

saved = False
players = None
ids = None
scores = []
phases = []


# -------------------- routes -------------------

@app.route('/')
def home():
        return flask.redirect('new_game') if not saved else flask.redirect('play')


@app.route('/new_game', methods=['GET', 'POST'])
def new_game():

    #render page
    if flask.request.method == "GET":
        return flask.render_template("new_game.html")

    #start new game
    elif flask.request.method == "POST":

        global players
        players = []
        for i in range(6):
            name = str(flask.request.form["{}".format(i)])
            print name
            if name:
                players.append(name)

        #ensure at least two players
        if len(players) < 2:
            players = None
            return flask.render_template('new_game.html', error="Please enter at least 2 player names!")

        #save game state
        global ids
        global saved
        global scores
        global phases
        saved = True
        scores = [[0]*len(players)]
        ids = [str(i) for i in range(len(players))]
        phases = [set([num for num in range(1,11)])]*len(players)
        return flask.redirect('play')


@app.route('/play', methods=['GET', 'POST'])
def play():

    #access globals
    global ids
    global scores
    global phases
    global players

    #ensure players registered for game play
    if not saved or not players:
        return flask.redirect('new_game')

    #render page
    elif flask.request.method == "GET":
        return flask.render_template('play.html', players=players, indices=range(len(players)), ids=ids, scores=scores, phases=phases, phasestrings=[convert_phases_to_string(stats) for stats in phases])

    #incorporate new scores and phases
    elif flask.request.method == "POST":

        #retrieve scores
        try:
            round_scores = [int(flask.request.form[i]) for i in ids]
        except:
            return flask.render_template('play.html', players=players, indices=range(len(players)), ids=ids, scores=scores, phases=phases, phasestrings=[convert_phases_to_string(stats) for stats in phases], error="Please enter a valid score for each player (0 if the player won the round)!")

        #validate scores
        if round_scores.count(0) != 1:
            return flask.render_template('play.html', players=players, indices=range(len(players)), ids=ids, scores=scores, phases=phases, phasestrings=[convert_phases_to_string(stats) for stats in phases], error="Make sure exactly one player has a score of 0!")
        for score in round_scores:
            if score%5 != 0:
                return flask.render_template('play.html', players=players, indices=range(len(players)), ids=ids, scores=scores, phases=phases, phasestrings=[convert_phases_to_string(stats) for stats in phases], error="Scores must be multiples of 5!")

        #retrieve phases
        # try:
            # completed_phases = [int(flask.request.form[] for )]


        #update scores
        if not scores:
            scores.append(round_scores)
        else:
            scores.append([scores[-1][i]+round_scores[i] for i in range(len(players))])
        return flask.render_template('play.html', players=players, indices=range(len(players)), ids=ids, scores=scores, phases=phases, phasestrings=[convert_phases_to_string(stats) for stats in phases])



# -------------------- helper functions  --------------------

def convert_phases_to_string(phase_list):
    output = ""
    for phase in range(1,11):
        if phase in phase_list:
            output += '{} '.format(phase)
        else:
            output += '  '
    return output


# -------------------- run app --------------------

if __name__ == '__main__': 
    app.run()



