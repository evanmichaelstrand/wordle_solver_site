from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    test = "test from flask"
    color = "#4CAF50"
    return render_template('wordle.html', test=test, color=color)

#def hello_world():
    #return "<p>Hello, World!</p>"

'''def colorChange():
    color="#fcba03"
    return (color=color)'''

app.run()