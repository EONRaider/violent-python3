import re
import argparse
import os
import sqlite3


def print_downloads(download_db):
    with sqlite3.connect(download_db) as conn:
        c = conn.cursor()
        c.execute("SELECT name, source, datetime(endTime/1000000, 'unixepoch') "
                  "FROM moz_downloads;")
        print('\n[*] -- Files Downloaded -- ')
        for row in c:
            print(f'{"":>3}[+] File: {str(row[0])} from source: '
                  f'{str(row[1])} at: {str(row[2])}')


def print_cookies(cookies_db):
    try:
        with sqlite3.connect(cookies_db) as conn:
            c = conn.cursor()
            c.execute('SELECT host, name, value FROM moz_cookies')

            print('\n[*] -- Found Cookies --')

            for row in c:
                host = str(row[0])
                name = str(row[1])
                value = str(row[2])
                print(f'{"":>3}[+] Host: {host}, Cookie: {name}, Value: {value}')

    except Exception as e:
        if 'encrypted' in str(e):
            print(f'\n{"":>3}[*] Error reading your cookies database.'
                  f'{"":>3}[*] Upgrade your Python-Sqlite3 Library')


def print_history(places_db):
    try:
        with sqlite3.connect(places_db) as conn:
            c = conn.cursor()
            c.execute("select url, datetime(visit_date/1000000, 'unixepoch') "
                      "from moz_places, moz_historyvisits where "
                      "visit_count > 0 "
                      "and moz_places.id==moz_historyvisits.place_id;")

            print('\n[*] -- Found History --')

            for row in c:
                url = str(row[0])
                date = str(row[1])
                print(f'{"":>3}[+] {date} - Visited: {url}')

    except Exception as e:
        if 'encrypted' in str(e):
            print(f'\n{"":>3}[*] Error reading your places database.'
                  f'{"":>3}[*] Upgrade your Python-Sqlite3 Library')


def print_google(places_db):
    with sqlite3.connect(places_db) as conn:
        c = conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, 'unixepoch') "
                  "from moz_places, moz_historyvisits where visit_count > 0 "
                  "and moz_places.id==moz_historyvisits.place_id;")

        print('\n[*] -- Found Google --')

        for row in c:
            url = str(row[0])
            date = str(row[1])
            if 'google' in url.lower():
                r = re.findall(r'q=.*', url)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+', ' ')
                    print(f'[+] {date} - Searched For: {search}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage='python3 firefox_parse.py FIREFOX_PROFILE')
    parser.add_argument('firefox_prof', type=str, metavar='FIREFOX_PROFILE',
                        help='specify path to the directory containing '
                             'the firefox profile database file(s)')

    args = parser.parse_args()
    path_name = args.firefox_prof

    download_dbase = os.path.join(path_name, 'downloads.sqlite')
    if os.path.isfile(download_dbase):
        print_downloads(download_dbase)
    else:
        print(f'[!] Downloads DB does not exist: {download_dbase}')

    cookies_dbase = os.path.join(path_name, 'cookies.sqlite')
    if os.path.isfile(cookies_dbase):
        print_cookies(cookies_dbase)
    else:
        print(f'[!] Cookies DB does not exist: {cookies_dbase}')

    places_dbase = os.path.join(path_name, 'places.sqlite')
    if os.path.isfile(places_dbase):
        print_history(places_dbase)
        print_google(places_dbase)
    else:
        print(f'[!] Places DB does not exist: {places_dbase}')
