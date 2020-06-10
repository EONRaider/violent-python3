import json
import argparse
import urllib.error
import urllib.parse
import urllib.request
from anon_browser import AnonBrowser


class GoogleResult:
    def __init__(self, title, text, url):
        self.title = title
        self.text = text
        self.url = url

    def __repr__(self):
        return self.title


def google(search_term):
    ab = AnonBrowser()
    search_term = urllib.parse.quote_plus(search_term)
    response = ab.open(f'http://ajax.googleapis.com/'
                       f'ajax/services/search/web?v=1.0&q={search_term}')
    objects = json.load(response)
    results = []

    for result in objects['responseData']['results']:
        url = result['url']
        title = result['titleNoFormatting']
        text = result['content']
        new_gr = GoogleResult(title, text, url)
        results.append(new_gr)

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 anon_google.py KEYWORDS')
    parser.add_argument('kwords', type=str, metavar='KEYWORDS',
                        help='specify the keyword(s) for a Google search')
    args = parser.parse_args()
    keywords = args.kwords

    print(google(keywords))
