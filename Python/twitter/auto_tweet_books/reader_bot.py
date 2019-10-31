"""
This is my new reader bot.
"""

import configparser
import twitter
import json
import sys
import os
from datetime import datetime, timedelta
from dateutil import parser
import time
import random
import math

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
    '''
    Get the configuration for all twitter activities.
    :return: config_file
    '''

    # Get System path and config file
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
    config['record_count'] = configuration.get('params', 'record_count')
    config['read_length'] = configuration.get('params', 'read_length')
    return config


class readerBotTools(object):
    '''
    Tools for manipulating the readerBot
    '''
    def __init__(self, api=None):
        self.config = get_configuration()
        # search = api.GetSearch(term='#scifi #novel', result_type='recent', count=int(self.config['record_count']))
        # print(search)

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
        print(listed_tweets)
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

    def collect_random_seed(self):
        text_seed = self.get_tweets(api=api, screen_name=self.config['user'])
        collection = ''
        for s in text_seed:
            data = s.AsDict()
            text = data['text']
            for x in text:
                collection += x
        return collection

    def truly_random(self, collection=None):
        rando = 0.0
        if collection:
            final = collection
            a = 0
            b = 0
            c = 0
            d = 0

            random.seed = int(time.time() * math.sin(time.time()))
            A = random.randrange(a, len(final) + 1)
            B = random.randrange(b, len(final) + 1)
            C = random.randrange(c, len(final) + 1)
            D = random.randrange(d, len(final) + 1)
            a = ord(final[A])
            b = ord(final[B])
            c = ord(final[C])
            d = ord(final[D])
            rando = ((a * b) / c) * ((d / 2) * math.sin(4 * time.time()))
        return rando

    def rando_range(self, min=None, max=None, integer=False):
        collection = self.collect_random_seed()
        if not min and not max:
            min = 0.0
            max = 100.0
        elif min and not max:
            max = float(min)
            min = 0.0
        elif max and not min:
            max = float(max)
            min = 0.0
        else:
            max = float(max)
            min = float(min)
        A = self.truly_random(collection)
        B = self.truly_random(collection)
        C = self.truly_random(collection)
        num_list = sorted([A, B, C])
        low = num_list[0]
        hi = num_list[2]
        mid = num_list[1]
        diff = hi - low
        m_diff = mid - low

        range_diff = max - min
        rando = (min + (range_diff * (m_diff / diff)))
        if integer:
            rando = int(rando)
        return rando

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


if __name__ == "__main__":
    config = get_configuration()
    api = twitter.Api(config['consumer_api_key'], config['consumer_secret_key'], config['api_token'],
                      config['api_secret'])
    test = readerBotTools(api=api)
    print(test.rando_range(0, 500, integer=False))

