import tweepy
import requests
import time
from datetime import datetime, date, timedelta
from pytz import timezone
import pytz
from config import *

#api.update_status(status=raw_input("Enter tweet: "))

# Get today's date (not datetime) with Pacific timezone information
def date_today():
    utc = pytz.utc
    pacific = timezone('US/Pacific')
    naive_today = datetime.today()
    utc_today = utc.localize(naive_today)
    today = utc_today.astimezone(pacific).date()
    return today

# Get all jobs posted today as a list
def get_todays_jobs(url):
    collection = requests.get(url).json()['results']['collection1']
    DATE_FORMAT = SEIA_DATEFORMAT
    todays_jobs = []
    #today's date in Pacific Timezone
    t = date_today()
    for x in collection:
        if datetime.strptime(x['seia_date']['text'], DATE_FORMAT).date() == t:
            try:
                todays_jobs.append([x['seia_title']['text'], x['seia_title']['href'], x['seia_location']['text'], x['seia_company']['text']])
            except:
                pass
    return todays_jobs

# Authorize Twitter and return an API object that we can use to tweet and do other fun stuff with
def authorize_twitter(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

# Form a tweet from a list of jobs, gotten from the get_todays_jobs function, and form a list of tweets
def form_tweets(job_list):
    tweets = []
    for x in job_list:
        tweet = x[3] + " is looking for a " + x[0] + " in " + x[2] + ". Apply here: " + x[1]
        tweets.append(tweet)
    return tweets


api = authorize_twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweets = form_tweets(get_todays_jobs(SEIA_URL))

for tweet in tweets:
    api.update_status(status=tweet)
    time.sleep(300)
