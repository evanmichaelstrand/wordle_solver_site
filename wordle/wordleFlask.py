from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
import numpy as np


with open('wordle_words.txt') as f:
    global lines
    lines = f.readlines()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ICESECRET'

def fresh():
    global suggestions
    global colors
    global cur_wordlist

    suggestions = []
    colors = []
    cur_wordlist = lines

    #starters = ['slice', 'tried', 'crane']
    #suggestions.append(np.random.choice(starters))

    return

def filter_black_letter(cur_words, letter, unknowns, blacks, yellows, bi, yi):
    for i in bi:
        if not (letter in blacks and letter in yellows):
            cur_words = list(filter(lambda x: letter not in x[i], cur_words))
    '''for i in yi:
        if not (letter in blacks and letter in yellows):
            cur_words = list(filter(lambda x: letter not in x[i], cur_words))'''
    return cur_words

def filter_green_letter(cur_words, letter, pos):
    new_cur_words = list(filter(lambda x: letter == x[pos], cur_words))
    return new_cur_words

def filter_yellow_letter(cur_words, letter, pos):
    new_cur_words = list(filter(lambda x: (letter != x[pos]) and (letter in x), cur_words))
    return new_cur_words

def get_words_from_guess(cur_words, word, colors):
    unknowns, bi, yi  = get_unknowns(colors)
    blacks = []
    yellows = []
    for b in bi:
        blacks.append(word[b])
    for y in yi:
        yellows.append(word[y])
    for i in range(5):
        if colors[i] == 'b':
            cur_words = filter_black_letter(cur_words, word[i], unknowns, blacks, yellows, bi, yi)
        elif colors[i] == 'y':
            cur_words = filter_yellow_letter(cur_words, word[i], i)
        elif colors[i] == 'g':
            cur_words = filter_green_letter(cur_words, word[i], i)
        else:
            return "error"

    return cur_words

def get_unknowns(colors):
    blacks = []
    yellows = []
    unknowns = []
    for i in range(5):
        if colors[i] != 'g':
            unknowns.append(i)
            if colors[i] == 'b':
                blacks.append(i)
            elif colors[i] == 'y':
                yellows.append(i)
    return unknowns, blacks, yellows

def get_suggestion(cur_words, unknowns):
    score_record = np.zeros(len(cur_words))
    for u in unknowns:
        for i in range(len(cur_words)):
            for j in range(len(cur_words)):
                word = cur_words[i]
                other = cur_words[j]
                if i != j and word[u] == other[u]:
                    score_record[i] += 1
    
    index = np.argmax(score_record)
    
    for score in score_record:
        score += 1

    sorted_indices = np.argsort(score_record)

    top_words = []
    top_scores = []
    for ind in sorted_indices:
        top_words.append(cur_words[ind])
        top_scores.append(int(score_record[ind]))

    top_words.reverse()
    top_scores.reverse()

    #this will get the list up to length 5
    '''if len(cur_words) > 5:
        sug_len = 5
    else:
        sug_len = len(cur_words)

    
    top_indices = np.argpartition(score_record, -sug_len)[-sug_len:]
    top_words = []
    top_scores = []
    for ind in top_indices:
        top_words.append(cur_words[ind])
        top_scores.append(int(score_record[ind]))
    top_words.reverse()
    top_scores.reverse()'''
    
    return cur_words[index], int(score_record[index]), top_words, top_scores


@app.route("/", methods=['GET', 'POST'])
def index():
    fresh()
    guess, score, top_words, top_scores = get_suggestion(cur_wordlist, get_unknowns('bbbbb')[0])
    remaining = len(cur_wordlist)
    return render_template('wordle.html', suggestions=suggestions, remaining=remaining, top_words=top_words, top_scores = top_scores)

@app.route('/2/<string:wordAfter>/<string:choice>', methods=['POST'])
def process2p(wordAfter,choice):
    global colors
    colors.append(wordAfter)
    suggestions.append(choice)
    return ""

@app.route('/2', methods=['GET'])
def process2g():
    global cur_wordlist
    print(suggestions[0])
    print(colors[0])
    cur_wordlist = get_words_from_guess(cur_wordlist, suggestions[0], colors[0])
    remaining = len(cur_wordlist)
    if remaining == 0:
        return render_template('noWords.html')
    guess, score, top_words, top_scores = get_suggestion(cur_wordlist, get_unknowns(colors[0])[0])
    return render_template('wordle2.html', colors=colors, suggestions=suggestions, remaining=remaining, top_words=top_words, top_scores = top_scores)

@app.route('/3/<string:wordAfter>/<string:choice>', methods=['POST'])
def process3p(wordAfter, choice):
<<<<<<< HEAD
    global colors
=======
>>>>>>> 235396f06358c4c6b0b9b1e8c811fc89b80c18fc
    colors.append(wordAfter)
    suggestions.append(choice)
    return ""

@app.route('/3', methods=['GET'])
def process3g():
    global cur_wordlist
    cur_wordlist = get_words_from_guess(cur_wordlist, suggestions[1], colors[1])
    remaining = len(cur_wordlist)
    if remaining == 0:
        return render_template('noWords.html')
    print(len(cur_wordlist))
    guess, score, top_words, top_scores = get_suggestion(cur_wordlist, get_unknowns(colors[1])[0])
    return render_template('wordle3.html', colors=colors, suggestions=suggestions, remaining=remaining, top_words=top_words, top_scores = top_scores)

@app.route('/4/<string:wordAfter>/<string:choice>', methods=['POST'])
def process4p(wordAfter, choice):
<<<<<<< HEAD
    global colors 
=======
    print(wordAfter, "#4 from flask!") 
>>>>>>> 235396f06358c4c6b0b9b1e8c811fc89b80c18fc
    colors.append(wordAfter)
    suggestions.append(choice)
    return ""

@app.route('/4', methods=['GET'])
def process4g():
    global cur_wordlist
    cur_wordlist = get_words_from_guess(cur_wordlist, suggestions[2], colors[2])
    remaining = len(cur_wordlist)
    if remaining == 0:
        return render_template('noWords.html')
    print(len(cur_wordlist))
    guess, score, top_words, top_scores = get_suggestion(cur_wordlist, get_unknowns(colors[2])[0])
    return render_template('wordle4.html', colors=colors, suggestions=suggestions, remaining=remaining, top_words=top_words, top_scores = top_scores)

@app.route('/5/<string:wordAfter>/<string:choice>', methods=['POST'])
def process5p(wordAfter,choice):
<<<<<<< HEAD
    global colors
=======
    print(wordAfter, "#5 from flask!") 
>>>>>>> 235396f06358c4c6b0b9b1e8c811fc89b80c18fc
    colors.append(wordAfter)
    suggestions.append(choice)
    return ""

@app.route('/5', methods=['GET'])
def process5g():
    global cur_wordlist
    cur_wordlist = get_words_from_guess(cur_wordlist, suggestions[3], colors[3])
    remaining = len(cur_wordlist)
    if remaining == 0:
        return render_template('noWords.html')
    print(len(cur_wordlist))
    guess, score, top_words, top_scores = get_suggestion(cur_wordlist, get_unknowns(colors[3])[0])
    return render_template('wordle5.html', colors=colors, suggestions=suggestions, remaining=remaining, top_words=top_words, top_scores = top_scores)

@app.route('/6/<string:wordAfter>/<string:choice>', methods=['POST'])
def process6p(wordAfter, choice):
<<<<<<< HEAD
    #print(wordAfter, "#6 from flask!") 
    global colors
=======
    print(wordAfter, "#6 from flask!") 
>>>>>>> 235396f06358c4c6b0b9b1e8c811fc89b80c18fc
    colors.append(wordAfter)
    suggestions.append(choice)
    return ""

@app.route('/6', methods=['GET'])
def process6g():
    global cur_wordlist
    cur_wordlist = get_words_from_guess(cur_wordlist, suggestions[4], colors[4])
    remaining = len(cur_wordlist)
    if remaining == 0:
        return render_template('noWords.html')
    print(len(cur_wordlist))
    guess, score, top_words, top_scores = get_suggestion(cur_wordlist, get_unknowns(colors[4])[0])
    return render_template('wordle6.html', colors=colors, suggestions=suggestions, remaining=remaining, top_words=top_words, top_scores = top_scores)


if __name__ == '__main__':
    app.run(debug=True)





'''
print()
def run_game():
    cur_wordlist = lines
    starters = ['slice', 'tried', 'crane']
    print("##################### START #######################")
    guess = np.random.choice(starters)
    guess = get_suggestion(cur_wordlist, get_unknowns('bbbbb')[0])
    print("NEXT GUESS:", guess)
    count = 0
    while True:
        print("Enter the colors you got:")
        colors = str(input())
        if colors == 'ggggg':
            print("hurray! we won :)")
            break
        cur_wordlist = get_words_from_guess(cur_wordlist, guess, colors)
        if not cur_wordlist:
            print("no more words!!!")
            break
        guess = get_suggestion(cur_wordlist, get_unknowns(colors)[0])
        print("NEXT GUESS:", guess)
        count += 1
        if count == 6:
            print("Out of Tries!")
            break
'''
