import json
import re
import urllib.error
import urllib.parse
import urllib.request
from anon_browser import *


class ReconPerson:
    def __init__(self, handle):
        self.handle = handle
        self.tweets = self.get_tweets()

    def get_tweets(self):
        query = urllib.parse.quote_plus(f'from:{self.handle} since:2009-01-01 '
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

    def find_interests(self):
        interests = {
            'links': [],
            'users': [],
            'hashtags': []
        }

        for tweet in self.tweets:
            text = tweet['tweet']
            link = ''
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

    def twitter_locate(self, city_file):
        cities = []
        if city_file:
            for line in open(city_file).readlines():
                city = line.strip('\n').strip('\r').lower()
                cities.append(city)

        locations = []
        loc_cnt = 0
        city_cnt = 0
        tweets_text = ''

        for tweet in self.tweets:
            if tweet['geo']:
                locations.append(tweet['geo'])
                loc_cnt += 1
            tweets_text += tweet['tweet'].lower()

        for city in cities:
            if city in tweets_text:
                locations.append(city)
                city_cnt += 1

        return locations
