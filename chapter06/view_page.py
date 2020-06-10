import mechanicalsoup


def view_page(url):
    """ This function is not part of the original code of Violent
    Python. It used the deprecated 'mechanize' library for Python 2
    to perform the same task. A new solution using the MechanicalSoup
    library has been implemented here by EONRaider.
    https://github.com/EONRaider """

    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)

    source_code = browser.get_current_page()
    print(source_code)


if __name__ == '__main__':
    view_page('http://www.syngress.com/')
