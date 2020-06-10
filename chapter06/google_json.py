import json
import urllib.error
import urllib.parse
import urllib.request
from anon_browser import *


def google(search_term):
    ab = AnonBrowser()

    search_term = urllib.parse.quote_plus(search_term)
    response = ab.open(f'http://ajax.googleapis.com/ajax/services/search/web'
                       f'?v=1.0&q={search_term}')
    objects = json.load(response)
    print(objects)


if __name__ == '__main__':
    google('Boondock Saint')
