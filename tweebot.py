import tweepy
import requests
import time
from datetime import datetime, date, timedelta
from pytz import timezone
import pytz
import xml.etree.ElementTree as ET
from config import *

#api.update_status(status=raw_input("Enter tweet: "))

# Get date  with Pacific timezone information. days_ago is an offset; with a value of 0, it gets you today's date; with a value of 1, it gets you yesterday's date.
def get_date(days_ago=0):
    utc = pytz.utc
    pacific = timezone('US/Pacific')
    naive_today = datetime.today()
    utc_today = utc.localize(naive_today)
    date = utc_today.astimezone(pacific).date() - timedelta(days=days_ago)
    return date

# Get all jobs posted today as a list
def get_jobs(url, date):
    collection = requests.get(url).json()['results']['collection1']
    DATE_FORMAT = SEIA_DATEFORMAT
    jobs = []
    for x in collection:
        if datetime.strptime(x['seia_date']['text'], DATE_FORMAT).date() == date:
            try:
                jobs.append([x['seia_title']['text'], x['seia_title']['href'], x['seia_location']['text'], x['seia_company']['text'], x['seia_date']['text']])
            except:
                pass
    return jobs

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
        short_url = shorten_url(x[1])
        tweet = x[3] + " is looking for a " + x[0] + " in " + x[2] + ". Apply here: " + short_url
        tweets.append(tweet)
    return tweets

# Use psbe.co to shorten urls. Parse through xml response and extract shortened URL.
def shorten_url(tweet_url):
    shorten = 'http://psbe.co/API.asmx/CreateUrl?real_url='
    r = requests.get(shorten+tweet_url)
    root = ET.fromstring(r.text)
    shortened_url = root[3].text
    return shortened_url



api = authorize_twitter(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
d = get_date()
tweets = form_tweets(get_jobs(SEIA_URL, d))

'''
for tweet in tweets:
    api.update_status(status=tweet)
    time.sleep(10)
'''
