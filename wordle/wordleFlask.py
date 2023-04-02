from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
#import json
#need to add validator lib?

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ICESECRET'

def fresh():
    global suggestions
    global colors
    suggestions = []
    colors = []
    suggestions.append("e")
    return colors, suggestions







@app.route("/", methods=['GET', 'POST'])
def index():
    colors, suggestions = fresh()
    return render_template('wordle.html', suggestions=suggestions)

@app.route('/2/<string:wordAfter>', methods=['POST'])
def process2p(wordAfter):
    print(wordAfter, "#2 from flask!") 
    colors.append(wordAfter)
    return ""

@app.route('/2', methods=['GET'])
def process2g():
    sug2 = "test"
    suggestions.append(sug2)
    return render_template('wordle2.html', colors=colors, suggestions=suggestions)

@app.route('/3/<string:wordAfter>', methods=['POST'])
def process3p(wordAfter):
    print(wordAfter, "#3 from flask!") 
    colors.append(wordAfter)
    return ""

@app.route('/3', methods=['GET'])
def process3g():
    sug3 = "test3"
    suggestions.append(sug3)
    return render_template('wordle3.html', colors=colors, suggestions=suggestions)

@app.route('/4/<string:wordAfter>', methods=['POST'])
def process4p(wordAfter):
    print(wordAfter, "#4 from flask!") 
    colors.append(wordAfter)
    return ""

@app.route('/4', methods=['GET'])
def process4g():
    sug4 = "test4"
    suggestions.append(sug4)
    return render_template('wordle4.html', colors=colors, suggestions=suggestions)

@app.route('/5/<string:wordAfter>', methods=['POST'])
def process5p(wordAfter):
    print(wordAfter, "#5 from flask!") 
    colors.append(wordAfter)
    return ""

@app.route('/5', methods=['GET'])
def process5g():
    sug5 = "test5"
    suggestions.append(sug5)
    return render_template('wordle5.html', colors=colors, suggestions=suggestions)

@app.route('/6/<string:wordAfter>', methods=['POST'])
def process6p(wordAfter):
    print(wordAfter, "#6 from flask!") 
    colors.append(wordAfter)
    return ""

@app.route('/6', methods=['GET'])
def process6g():
    sug6 = "test6"
    suggestions.append(sug6)
    return render_template('wordle6.html', colors=colors, suggestions=suggestions)

app.run()