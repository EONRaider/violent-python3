import mechanicalsoup
import http.cookiejar


def print_cookies(url):
    """ This function is not part of the original code of Violent
    Python. It used the deprecated 'mechanize' library for Python 2
    to perform the same task. A new solution using the MechanicalSoup
    library has been implemented here by EONRaider.
    https://github.com/EONRaider """

    browser = mechanicalsoup.StatefulBrowser()
    cookie_jar = http.cookiejar.CookieJar()
    browser.set_cookiejar(cookie_jar)
    browser.open(url)

    for cookie in cookie_jar:
        print(cookie.__dict__)


if __name__ == '__main__':
    _url = 'http://www.syngress.com/'
    print_cookies(_url)
