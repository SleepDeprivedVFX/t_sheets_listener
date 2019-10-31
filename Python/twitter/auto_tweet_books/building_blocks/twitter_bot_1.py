"""
Twitter Bot 1
A simple device that searches for a list of terms in order to find new people and potential users and engage with them.
This could mean following, or sending messages to people.
The second main operation of the utility is to listen to my own tweets, test to see when last I tweeted, and then send
a random tweet from an archive.
"""

import configparser
import twitter
import json
import sys
import os
from datetime import datetime, timedelta
from dateutil import parser
import requests

twitter_keys = [
    "coordinates",
    "geo",
    "favorited",
    "hashtags",
    "id",
    "lang",
    "place",
    "source",
    "text",
    "truncated",
    "urls",
    "user",
    "user_mentions",
    "retweet_count",
    "retweeted_status",
    "retweeted"
]


def get_configuration():
    sys_path = sys.path
    config_file = 'twit_config.cfg'
    try:
        config_path = [f for f in sys_path if os.path.isfile(f + '/' + config_file)][0] + '/' + config_file
        config_path = config_path.replace('\\', '/')
    except IndexError as e:
        raise e

    # Create the configuration connection
    configuration = configparser.ConfigParser()
    configuration.read(config_path)

    config = {}
    # Parse out the configuration to local variables
    # Shotgun
    config['consumer_api_key'] = configuration.get('Consumer', 'api_key')
    config['consumer_secret_key'] = configuration.get('Consumer', 'api_secret_key')
    config['api_token'] = configuration.get('Access Tokens', 'api_token')
    config['api_secret'] = configuration.get('Access Tokens', 'api_secret')
    config['user'] = configuration.get('User', 'screen_name')
    return config


class twitter_bot_1(object):
    def __init__(self):
        super(twitter_bot_1, self).__init__()
        # print('Hola')
        self.config = get_configuration()
        self.api = twitter.Api(self.config['consumer_api_key'], self.config['consumer_secret_key'],
                               self.config['api_token'], self.config['api_secret'])

    def save_tweet(self, text=None, image=None, link=None, last_posted=None):
        previous_tweets = self.get_saved_tweets()
        print(previous_tweets)

        if not last_posted:
            last_posted = '%s %s' % (datetime.now().date(), datetime.now().time())

        all_tweets = previous_tweets['Tweets']

        sorted_tweets = sorted(all_tweets, key=lambda x: x['id'], reverse=True)
        last_id = sorted_tweets[0]['id']
        next_id = last_id + 1

        new_data = {
            'text': text,
            'id': next_id,
            'image': image,
            'link': link,
            'last_posted': last_posted
        }

        all_tweets.append(new_data)
        print(all_tweets)
        data = {
            "Tweets": all_tweets
        }
        print(data)
        tweet_file = open('tweets.json', 'w')
        save_this_data = json.dump(data, tweet_file, indent=4)
        tweet_file.close()
        print(save_this_data)

    def get_saved_tweets(self):
        fh = open('data/tweets.json', 'r')
        listed_tweets = json.load(fh)
        # print(listed_tweets)
        return listed_tweets

    def get_tweets(self, api=None, screen_name=None):
        timeline = api.GetUserTimeline(screen_name=screen_name, count=10)
        earliest_tweet = min(timeline, key=lambda x: x.id).id

        while True:
            tweets = api.GetUserTimeline(
                screen_name=screen_name, max_id=earliest_tweet, count=10
            )
            new_earliest = min(tweets, key=lambda x: x.id).id

            if not tweets or new_earliest == earliest_tweet:
                break
            else:
                earliest_tweet = new_earliest
                # print("getting tweets before:", earliest_tweet)
                timeline += tweets
                break

        return timeline

    def twit_search(self, terms=None, result_type='recent', count=20):
        search = self.api.GetSearch(term=terms, result_type=result_type, count=count)
        found = {}
        for txt in search:
            text = str(txt)
            parse_search = json.loads(text)
            for k in twitter_keys:
                if k in parse_search.keys():
                    tweet = parse_search[k]
                    found[k] = tweet
        return found

    def pick_random_tweet(self):
        tweet_list = self.get_saved_tweets()
        tweets_collection = []
        for tweet in tweet_list['Tweets']:
            date_obj = parser.parse(tweet['last_posted'])
            if date_obj > (datetime.now() - timedelta(days=4)):
                print('hello %s' % tweet)
                tweets_collection.append(tweet)
        if tweets_collection:
            pass


if __name__ == '__main__':
    bot = twitter_bot_1()

    # Quick Search:
    # text_search = bot.twit_search(terms='#scifi #books')
    # print(text_search)

    tweet = twitter_bot_1()
    tweet.pick_random_tweet()
