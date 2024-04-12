from boggle import Boggle
from flask import Flask, session, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY']="slowking"

boggle_game = Boggle()

@app.route('/')
def home():
    make_board = boggle_game.make_board()
    session['board']= make_board  #save the rand.board in a cookie.
    highest_score = session.get("high_score",0)
    num_plays = session.get("num_plays",0)

    return render_template('index.html', board = make_board, highest_score = highest_score, num_plays = num_plays)


@app.route('/check-word')
def validate_word():

    word = request.args['word']
    board= session['board']
    response= boggle_game.check_valid_word(board,word)

    return jsonify({"result": response })

@app.route("/post_score", methods=["POST"])
def post_score():

    #update the score or show any score that has already been validated.
    score = request.json['score']
    highest_score = session.get("high_score",0) 
    num_plays = session.get('num_plays',0)

    session["num_plays"]= num_plays + 1
    session["high_score"]= max(score, highest_score)

    return jsonify( record = score > highest_score )



    
