"""
This is my new reader bot.
"""

import configparser
import twitter
import json
import sys
import os
from datetime import datetime, timedelta


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
    return config


class readerBotTools(object):
    '''
    Tools for manipulating the readerBot
    '''
    def __init__(self, parent=None):
        super(readerBotTools).__init__(self, parent)

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
        fh = open('tweets.json', 'r')
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


if __name__ == "__main__":
    config = get_configuration()
    api = twitter.Api(config['consumer_api_key'], config['consumer_secret_key'], config['api_token'],
                      config['api_secret'])

