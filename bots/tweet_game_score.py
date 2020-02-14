#!/usr/bin/env python
# check mentions for matching links award a point for each match


import tweepy
import logging
import os
from config import create_api
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
searchkey = str(os.getenv("SEARCH_KEY"))
link_list = ['https://blog.2vcps.io/2019/12/13/quickly-install-cloud-native-storage-csi-driver-for-vsphere-6-7/', 'https://blog.2vcps.io/2019/10/25/k8s-python-twitter-pi/', 'https://blog.2vcps.io/2019/10/02/managing-multiple-kubernetes-clusters/']

def check_old_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        logger.info(new_since_id)
    return new_since_id

def generate_response():
    message_body = random.choice(link_list)
    logger.info(message_body)
    return message_body

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name} - {tweet.text} ")

            if not tweet.user.following:
                tweet.user.follow()
            sn = tweet.user.screen_name
            message_body = generate_response()
            message = "@{} you get a point! #pybot #PURESKO2020".format(sn, message_body)
            logger.info(message)
            api.update_status(
                status= message,
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id


def main():
    since_id = 1
    api = create_api()
    since_id = check_old_mentions(api, since_id)
    while True:
        logger.info("Searching for %s" % searchkey)
        #logger.info(since_id)
        since_id = check_mentions(api, [(searchkey)], since_id)
        logger.info(since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()