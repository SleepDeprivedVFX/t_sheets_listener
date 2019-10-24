import configparser
import twitter
import json
import sys
import os
import requests


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


def save_tweet(text=None, *args, **kwargs):
    print(text)
    print(args)
    print(kwargs)
    data = {
        'Tweet': 'Hello There Barney',
        'details': {
            'image': 'image_name',
            'link': 'link_location'
        }
    }
    tweet_file = open('tweets.json', 'w')
    save_this_data = json.dump(data, tweet_file, indent=4)
    tweet_file.close()
    print(save_this_data)


def get_saved_tweets():
    fh = open('tweets.json', 'r')
    listed_tweets = json.load(fh)
    print(listed_tweets)


def get_tweets(api=None, screen_name=None):
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
    search = api.GetSearch(term='science fiction novels', result_type='recent')
    for s in search:
        test = str(s)
        parse_search = json.loads(test)
        print(parse_search['text'])

    screen_name = config['user']

    # save_tweet(text='Hello There')
    get_saved_tweets()



    # timeline = get_tweets(api=api, screen_name=screen_name)
    # for t in timeline:
    #     print(t)
    # headers = {'authorization': 'OAuth oauth_consumer_key="%s",'
    #                             'oauth_signature="%s",'
    #                             'oauth_token="%s",'
    #                             'content-type": "application/json", "Accept-Charset": "UTF-8"' %
    #                             (config['consumer_api_key'], config['api_secret'], config['consumer_secret_key'])}
    # # headers = {
    #     'authorization': 'OAuth oauth_consumer_key="%s", oauth_nonce="generated-nonce", oauth_signature="%s",
    #     oauth_signature_method="HMAC-SHA1", oauth_timestamp="generated-timestamp", oauth_token="%s", oauth_version="1
    #     .0"' % (config['consumer_api_key'], config['consumer_secret_key'], config['api_token'])
    # }
    # url = 'https://api.twitter.com/1.1/search/tweets.json?q=novel%20author%20scifi'
    # payload = open("request.json")
    # r = requests.post(url, data=payload, headers=headers)
    # response = requests.get(url, headers=headers)
    # print(response)
    # test = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=novel%20author%20scifi', headers=headers)
    # print(test)

# headers = {
#     'authorization': 'OAuth oauth_consumer_key="%s", '
#                      'oauth_signature="%s", '
#                      'oauth_signature_method="HMAC-SHA1", oauth_timestamp="generated-timestamp", '
#                      'oauth_token="access-token-for-authed-user", oauth_version="1.0"',
# }

# response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=from%3Atwitterdev&result_type=mixed&count=2',
#                         headers=headers)
# print(response)
