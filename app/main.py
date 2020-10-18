from flask import Flask
from flask import request
import gspread
from random import randrange
from tweet import *

app = Flask(__name__)
gc = gspread.service_account(filename='gsheet_credentials.json')
sh = gc.open_by_key('1SbPgsCba39nGz5-vNF6b3q8Qn_12D92TxSizIFtfYmw')
worksheet = sh.sheet1


class Tweet:
        def __init__(self, questions, row_idx):
            self.questions = questions
            self.row_idx = row_idx


@app.route('/')
def tweet_list():
    tweet_respones = worksheet.get_all_records()
    tweets= []
    for idx, tweet in enumerate(tweet_respones, start=2):
        tweet = Tweet(**tweet, row_idx=idx)
        tweets.append(tweet)
    
    responseID = randrange(len(tweets))
    tweetResponse(tweets[responseID].questions)
    
    return tweets[responseID].questions


@app.route('/post', methods = ['GET', 'POST'])
def postyPost():
    if request.method == 'POST':
        print("its a post request")
        request.headers.add("Access-Control-Allow-Origin", "*")
        question = request.form.get('question')
        list = [question]
        worksheet.append_row(list)
    print("something")