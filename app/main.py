from flask import Flask
from tweet import *
app = Flask(__name__)


@app.route('/')
def initializeBot():
    # Read Google Sheet 
    response_list = get_response_list()

    # Post daily tweet
    #daily_post(response_list)
    
    # Start tweet stream miner
    start_mining(['!SocratesJoin','!SocratesHelp','!AskQuestion', '!SuggestTopic'])

    return "epic"
