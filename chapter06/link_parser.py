from anon_browser import AnonBrowser
from bs4 import BeautifulSoup
import argparse
import re


def print_links(url):
    """ This function is not part of the original code of Violent
    Python. It used the deprecated 'mechanize' library for Python 2
    to perform the same task. A new solution using the MechanicalSoup
    library has been implemented here by EONRaider.
    https://github.com/EONRaider """

    ab = AnonBrowser()
    ab.anonymize()
    ab.open(url)
    html = str(ab.get_current_page())

    try:
        print('[+] Printing Links From Regex.')
        link_finder = r'href="(.*?)"'
        links = re.findall(link_finder, html)
        print(*links, sep='\n')
    except Exception as e:
        print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
        pass

    try:
        print('\n[+] Printing Links From BeautifulSoup.')
        soup = BeautifulSoup(html, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        print(*links, sep='\n')
    except Exception as e:
        print(f'{"":>3}[-] Exception: {e.__class__.__name__}')
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 link_parser.py TARGET_URL')
    parser.add_argument('tgt_url', type=str, metavar='TARGET_URL',
                        help='specify the target url')
    args = parser.parse_args()
    _url = args.tgt_url

    print_links(_url)
