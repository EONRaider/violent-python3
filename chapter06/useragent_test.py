import mechanicalsoup


def test_user_agent(url, user_agent):
    """ This function is not part of the original code of Violent
    Python. It used the deprecated 'mechanize' library for Python 2
    to perform the same task. A new solution using the MechanicalSoup
    library has been implemented here by EONRaider.
    https://github.com/EONRaider """

    browser = mechanicalsoup.StatefulBrowser(user_agent=user_agent)
    browser.open(url)

    source_code = browser.get_current_page()
    print(source_code)


if __name__ == '__main__':
    """ The following webservice is a functioning and more modern 
    alternative to the one presented in the book """

    _url = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'
    _user_agent = 'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586; en-US; m18) ' \
                  'Gecko/20010131 Netscape6/6.01'

    test_user_agent(_url, _user_agent)
