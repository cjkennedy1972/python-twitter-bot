#!/usr/bin/env python
# tweepy-bots/bots/followfollowers.py

import tweepy
import logging
from config import create_api
import time
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        logger.info(follower.screen_name)
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()
            try:
                follower_tweets = api.user_timeline(follower.screen_name, count = 100, include_rts = False)
                df = data_extract(follower_tweets)
                filepath = "/tmp/export/{}".format(follower.screen_name)
                filename = "/tmp/export/{}/tweets.csv".format(follower.screen_name)
                Path(filepath).mkdir(parents=True, exist_ok=True)
                export_csv = df.to_csv(filename, mode='a')
            except tweepy.TweepError as e:
                logger.error("Error", e)
                break
            else:
                if not follower_tweets:
                    print("not enough tweets")
                    break
    

def data_oldusers(api):
    logger.info("Dump tweets for already following")
    for follower in tweepy.Cursor(api.followers).items():
        logger.info(follower.screen_name)
        if follower.following:
            logger.info(f" Already Following {follower.name}, but dumping data once.")
            try:
                follower_tweets = api.user_timeline(follower.screen_name, count = 200, include_rts = False)
                df = data_extract(follower_tweets)
                filepath = "/tmp/export/{}".format(follower.screen_name)
                filename = "/tmp/export/{}/tweets.csv".format(follower.screen_name)
                Path(filepath).mkdir(parents=True, exist_ok=True)
                export_csv = df.to_csv(filename, mode= 'w')
            except tweepy.TweepError as e:
                logger.error("Error", e)
                break
            else:
                if not follower_tweets:
                    print("not enough tweets")
                    break



def data_extract(tweets_obj):
    tweet_list = []
    for tweet in tweets_obj:
            tweet_id = tweet.id
            text = tweet.text
            favorite_count = tweet.favorite_count
            retweet_count = tweet.retweet_count
            created_at = tweet.created_at # utc time tweet created
            source = tweet.source # utility used to post tweet
            reply_to_status = tweet.in_reply_to_status_id # if reply int of orginal tweet id
            reply_to_user = tweet.in_reply_to_screen_name # if reply original tweetes screenname
            retweets = tweet.retweet_count # number of times this tweet retweeted
            favorites = tweet.favorite_count # number of time this tweet liked
            # append attributes to list
            tweet_list.append({'tweet_id':tweet_id, 
                            'text':text, 
                            'favorite_count':favorite_count,
                            'retweet_count':retweet_count,
                            'created_at':created_at, 
                            'source':source, 
                            'reply_to_status':reply_to_status, 
                            'reply_to_user':reply_to_user,
                            'retweets':retweets,
                            'favorites':favorites})
    
    df = pd.DataFrame(tweet_list, columns=['tweet_id',
                                           'text',
                                           'favorite_count',
                                           'retweet_count',
                                           'created_at',
                                           'source',
                                           'reply_to_status',
                                           'reply_to_user',
                                           'retweets',
                                           'favorites'])
    return df


def main():
    api = create_api()
    data_oldusers(api)
    while True:
        follow_followers(api)
        # test_tweets = api.user_timeline('jon_2vcps')
        # athing = data_extract(test_tweets)
        # logger.info(athing)
        logger.info("Waiting... 300s")
        time.sleep(300)

if __name__ == "__main__":
    main()