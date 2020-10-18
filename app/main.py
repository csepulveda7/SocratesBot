from flask import Flask
from tweet import *
from flask_cors import CORS, cross_origin
from flask import request

app = Flask(__name__)
CORS(app)
gc = gspread.service_account(filename='gsheet_credentials.json')
sh = gc.open_by_key('1SbPgsCba39nGz5-vNF6b3q8Qn_12D92TxSizIFtfYmw')
worksheet = sh.sheet1

@app.route('/post', methods = ['GET','POST'])
@cross_origin()
def postyPost():
    if request.method == 'POST':
        quest = request.get_json()
        # q = request.data()
        print(quest.get('question'))
        str = quest.get('question')
        list = [str]
        print(list)
        worksheet.append_row(list)   
        return "Done"
    return '''
        <h1>Post request</h1>
    '''


@app.route('/get', methods = ['GET'])
@cross_origin()
def getGets():
    if request.method == 'GET':
        sheets = worksheet.get_all_values()
        print(sheets)
        return '''<h1>requests.get(sheets)</h1>'''
    return '''
        <h1>get request</h1>
    '''


@app.route('/')
def initializeBot():
    # Read Google Sheet 
    response_list = get_response_list()

    # Post daily tweet
    #daily_post(response_list)
    
    # Start tweet stream miner
    start_mining(['!SocratesJoin','!SocratesHelp','!AskQuestion', '!SuggestTopic'])

    return "epic"

