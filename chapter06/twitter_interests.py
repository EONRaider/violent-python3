import json
import argparse
import re
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


def find_interests(tweets):
    interests = {
        'links': [],
        'users': [],
        'hashtags': []
    }

    for tweet in tweets:
        text = tweet['tweet']
        links = re.compile(r'(http.*?)\Z|(http.*?)').findall(text)

        for link in links:
            if link[0]:
                link = link[0]
            elif link[1]:
                link = link[1]
            else:
                continue
            try:
                response = urllib.request.urlopen(link)
                full_link = response._url
                interests['links'].append(full_link)
            except Exception as e:
                print(f'[-] Exception: {e.__class__.__name__}')
                pass

        interests['users'] += re.compile(r'(@\w+)').findall(text)
        interests['hashtags'] += re.compile(r'(#\w+)').findall(text)

    interests['users'].sort()
    interests['hashtags'].sort()
    interests['links'].sort()

    return interests


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 twitter_interests.py TWITTER_HANDLE')
    parser.add_argument('handle', type=str, metavar='TWITTER_HANDLE',
                        help='specify the Twitter handle')

    args = parser.parse_args()
    _handle = args.handle

    _tweets = get_tweets(_handle)
    _interests = find_interests(_tweets)

    print('\n[+] Links.')
    for _link in set(_interests['links']):
        print(f' [+] {str(_link)}')

    print('\n[+] Users.')
    for user in set(_interests['users']):
        print(f' [+] {str(user)}')

    print('\n[+] HashTags.')
    for hashtag in set(_interests['hashtags']):
        print(f' [+] {str(hashtag)}')
