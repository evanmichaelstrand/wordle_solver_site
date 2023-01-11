from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('wordle.html')

#def hello_world():
    #return "<p>Hello, World!</p>"