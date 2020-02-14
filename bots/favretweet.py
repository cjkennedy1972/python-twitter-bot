#!/usr/bin/env python
# tweepy-bots/bots/favretweet.py

import tweepy
import logging
from config import create_api
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
searchkey = os.getenv("SEARCH_KEY")

class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            return
        try:
            print(tweet.text)
            tweet.favorite()
            #tweet.retweet()
        except Exception as e:
            logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"], )

if __name__ == "__main__":
    main([searchkey])