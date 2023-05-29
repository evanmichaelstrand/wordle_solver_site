from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
import numpy as np

with open('wordle_words.txt') as f:
    global lines
    lines = f.readlines()

def filter_black_letter(cur_words, letter, unknowns, blacks, yellows, bi, yi):
    for i in bi:
        if not (letter in blacks and letter in yellows):
            cur_words = list(filter(lambda x: letter not in x[i], cur_words))
    '''for i in yi:
        if not (letter in blacks and letter in yellows):
            cur_words = list(filter(lambda x: letter not in x[i], cur_words))'''
    #print("for letter", letter,":", cur_words)
    return cur_words

def filter_green_letter(cur_words, letter, pos):
    new_cur_words = list(filter(lambda x: letter == x[pos], cur_words))
    return new_cur_words

def filter_yellow_letter(cur_words, letter, pos):
    new_cur_words = list(filter(lambda x: (letter != x[pos]) and (letter in x), cur_words))
    return new_cur_words

def get_words_from_guess(cur_words, word, colors):
    unknowns, bi, yi  = get_unknowns(colors)
    #blacks is an array of the letters that are in a black position
    #yellows is an array of the letters that are in a black position
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
    #blacks are the indices of the guessed word that are black
    #yellows are the indices of the guessed word that are yellow
    #unknowns are the indices of the guessed word that are not green
    bi = []
    yi = []
    unknowns = []
    for i in range(5):
        if colors[i] != 'g':
            unknowns.append(i)
            if colors[i] == 'b':
                bi.append(i)
            elif colors[i] == 'y':
                yi.append(i)
    return unknowns, bi, yi

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

    if len(cur_words) > 5:
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
    top_scores.reverse()
    #for i in top_indices:
        #print(cur_words[i], score_record[i])
    return cur_words[index], int(score_record[index]), top_words, top_scores



wordlist = lines
#first guess
wordlist = get_words_from_guess(wordlist, "slice", "byybb")
#igloo is in here so far
wordlist = get_words_from_guess(wordlist, "vigil", "byyby")
#problem with filter black letters. In the case letter appears twice, once as yellow and once as black




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
