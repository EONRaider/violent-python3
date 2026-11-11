import http.cookiejar
import mechanicalsoup
import random
import time


class AnonBrowser(mechanicalsoup.StatefulBrowser):
    """ This class is not part of the original code of Violent
    Python. It used the deprecated 'mechanize' library for Python 2
    to perform the same task. A new solution using the MechanicalSoup
    library has been implemented here by EONRaider.
    https://github.com/EONRaider """

    def __init__(self, proxies=None, user_agents=None):
        super().__init__()
        self.user_agents = [] if user_agents is None else user_agents
        self.proxies = [] if proxies is None else proxies
        self.session.proxies = None
        self.user_agents = self.user_agents + ['Mozilla/4.0 ', 'FireFox/6.01',
                                               'ExactSearch', 'Nokia7110/1.0']
        self.cookie_jar = http.cookiejar.CookieJar()
        self.set_cookiejar(self.cookie_jar)
        self.anonymize()

    def clear_cookies(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.set_cookiejar(self.cookie_jar)

    def change_user_agent(self):
        random_user_agent = random.choice(self.user_agents)
        # MechanicalSoup sends the agent set via set_user_agent(); assigning to a
        # plain attribute (as the original did) had no effect on the request.
        self.set_user_agent(random_user_agent)

    def change_proxy(self):
        if self.proxies:
            random_proxy = random.choice(self.proxies)
            # Route BOTH http and https through the chosen proxy, and stop
            # requests from consulting the HTTP(S)_PROXY environment variables
            # (trust_env). Setting only the 'http' scheme, as the original did,
            # left https requests with no proxy entry: trust_env then let an
            # https fetch follow HTTPS_PROXY or go out directly, bypassing the
            # chosen proxy and leaking the real IP.
            self.session.trust_env = False
            self.session.proxies = {'http': random_proxy, 'https': random_proxy}

    def anonymize(self, sleep=False):
        self.clear_cookies()
        self.change_user_agent()
        self.change_proxy()

        if sleep:
            time.sleep(60)
