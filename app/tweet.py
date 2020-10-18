from os import environ
import gspread
import tweepy
import time
from random import randrange
from dotenv import load_dotenv
load_dotenv()

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import logging
import time
import csv
import sys


CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
gc = gspread.service_account(filename='gsheet_credentials.json')
sh = gc.open_by_key('1SbPgsCba39nGz5-vNF6b3q8Qn_12D92TxSizIFtfYmw')
worksheet = sh.sheet1

# Create a streamer object
class StdOutListener(StreamListener):

    # When a tweet appears
    def on_status(self, status):

        # If the tweet is not a retweet
        if not 'RT @' in status.text:
            # Try to 
            try:
                if status.text == '!SocratesJoin':
                    response = "Hello there! Let's start a #HealthyConverstation \nHow can I be of service? @" + status.user.screen_name
                    api.update_status(response, status.id)

                    user_name = "@csepulveda3211"
                    replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name), since_id=status.id, tweet_mode='extended').items()

                    while True:
                        reply = replies.next()
                        if not hasattr(reply, 'in_reply_to_status_id_str'):
                            continue
                        if str(reply.in_reply_to_status_id) == status.id:
                            print("reply of tweet:{}".format(reply.text))

                        if status.text == '!SocratesHelp':
                            response = "Let's dig deep, healthy conversations aren't always the easiest, but that's what I'm here for. Let's make some friends and open our minds. In the end, we are not truly strangers after all. @" + status.user.screen_name
                            api.update_status(response, status.id)
                        
                        elif status.text == '!AskQuestion':
                            response_list = get_response_list()
                            response = get_response(response_list) + " @" + status.user.screen_name
                            api.update_status(response, status.id)
                
                        elif status.text == '!SuggestTopic':
                            response_list = get_response_list()
                            response = get_response(response_list) + " @" + status.user.screen_name
                            api.update_status(response, status.id)
                
                        
                        if status.text == '!EndSession':
                            response = "Goodbye friends. @" + status.user.screen_name
                            api.update_status(response, status.id)

                            break
                            
            # If some error occurs
            except Exception as e:
                # Print the error
                print(e)
                # and continue
                pass

        # Return nothing
        return

    # When an error occurs
    def on_error(self, status_code):
        # Print the error code
        print('Encountered error with status code:', status_code)
        
        # If the error code is 401, which is the error for bad credentials
        if status_code == 401 or status_code == 420:
            # End the stream
            return False

    # When a deleted tweet appears
    def on_delete(self, status_id, user_id):
        
        # Print message
        print("Delete notice")
        
        # Return nothing
        return

    # When reach the rate limit
    def on_limit(self, track):
        
        # Print rate limiting error
        print("Rate limited, continuing")
        
        # Continue mining tweets
        return True

    # When timed out
    def on_timeout(self):
        
        # Print timeout message
        print(sys.stderr, 'Timeout...')
        
        # Wait 10 seconds
        time.sleep(10)
        
        # Return nothing
        return

class Tweet:
        def __init__(self, questions, row_idx):
            self.questions = questions
            self.row_idx = row_idx

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


def get_response_list():
    tweet_responses = worksheet.get_all_records()
    tweets= []
    for idx, tweet in enumerate(tweet_responses, start=2):
        tweet = Tweet(**tweet, row_idx=idx)
        tweets.append(tweet)
    
    return tweets

# Get Socrates response message from Google Sheet
def get_response(response_list):
    interval = 60 * 60 * 24

    response_id = randrange(len(response_list))
    message = response_list[response_id].questions

    return message

# Post daily question/topic on timeline
def daily_post(response_list):
    interval = 60 * 60 * 24

    response_id = randrange(len(response_list))
    message = response_list[response_id].questions

    while True:
        api.update_status(message)
        time.sleep(interval)

# Mine tweet stream for bot callout
def start_mining(queries):

    print('mining started')
    # Create a listener
    listener = StdOutListener()
    
    # Create a stream object with listener and authorization
    stream = tweepy.Stream(auth, listener)

    # Run the stream object using the user defined queries
    stream.filter(track=queries)
