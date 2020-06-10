import json
import argparse
import urllib.error
import urllib.parse
import urllib.request
from anon_browser import *


def get_tweets(handle):
    query = urllib.parse.quote_plus(f'from:{handle} since:2009-01-01 '
                                    f'include:retweets')
    tweets = []
    browser = AnonBrowser()
    browser.anonymize()
    response = browser.open(f'http://search.twitter.com/'
                            f'search.json?q={query}')
    json_objects = json.load(response)

    for result in json_objects['results']:
        new_result = {
            'from_user': result['from_user_name'],
            'geo': result['geo'],
            'tweet': result['text']
        }
        tweets.append(new_result)

    return tweets


def load_cities(city_file):
    cities = []
    for line in open(city_file).readlines():
        city = line.strip('\n').strip('\r').lower()
        cities.append(city)
    return cities


def twitter_locate(tweets, cities):
    locations = []
    loc_cnt = 0
    city_cnt = 0
    tweets_text = ""

    for tweet in tweets:
        if tweet['geo']:
            locations.append(tweet['geo'])
            loc_cnt += 1
        tweets_text += tweet['tweet'].lower()

    for city in cities:
        if city in tweets_text:
            locations.append(city)
            city_cnt += 1

    print(f'[+] Found {str(loc_cnt)} locations via Twitter API '
          f'and {str(city_cnt)} locations from text search.')

    return locations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 twitter_geo.py TWITTER_HANDLE [-c LIST_OF_CITIES]')

    parser.add_argument('handle', type=str, metavar='TWITTER_HANDLE',
                        help='specify the Twitter handle')
    parser.add_argument('-c', type=str, metavar='LIST_OF_CITIES',
                        help='specify the file containing cities to search')

    args = parser.parse_args()
    _handle = args.handle
    _city_file = args.c

    _cities = load_cities(_city_file) if _city_file else []

    _tweets = get_tweets(_handle)
    _locations = twitter_locate(_tweets, _cities)

    print(f'[+] Locations: {str(_locations)}')
