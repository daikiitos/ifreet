import os
import tweepy
from flask import flash


consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
# access_token = os.environ['ACCESS_TOKEN']
# access_token_secret = os.environ['ACCESS_TOKEN_SECRET']


# make a tweet
def do_tweet(text, token, token_secret):
    try:
        client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, \
            access_token=token, access_token_secret=token_secret)
        response = client.create_tweet(text=text, reply_settings='mentionedUsers', user_auth=True)
        id = dict(response.data)['id']
        return id
    except Exception as e:
        flash(str(e))
        print(str(e))


# get recent tweets (this function is not used)
def get_recent_tweets(token, token_secret):
    try:
        client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, \
            access_token=token, access_token_secret=token_secret)
        return client.search_recent_tweets('ifreet', user_auth=True)
    except Exception as e:
        flash(str(e))
        print(str(e))


# get tweets by ids
def get_tweets(ids, token, token_secret):
    try:
        client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, \
            access_token=token, access_token_secret=token_secret)
        return client.get_tweets(ids=ids, tweet_fields=['created_at'], user_auth=True)
    except Exception as e:
        flash(str(e))
        print(str(e))


# delete tweets
def delete_tweets(tweetsWithUsers):
    try:
        client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret)

        # store ids of tweets deleted successfully
        deleted = []

        for tw in tweetsWithUsers:
            client.access_token = tw['access_token']
            client.access_token_secret = tw['access_token_secret']
            print(client.access_token)
            print(client.access_token_secret)
            response = client.delete_tweet(tw.Tweet.id, user_auth=True)

            if dict(response.data)['deleted']:
                deleted.append(tw.Tweet.id)

        return deleted
    except Exception as e:
        print(str(e))
