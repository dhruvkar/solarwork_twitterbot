import tweepy
from config import *


consumer_key=CONSUMER_KEY
consumer_secret=CONSUMER_SECRET
access_token=ACCESS_TOKEN
access_token_secret=ACCESS_TOKEN_SECRET


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
	

api.update_status(status=raw_input("Enter tweet: "))


