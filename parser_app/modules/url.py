import requests
from bs4 import BeautifulSoup


class E_URL:
    headers = {"User-Agent": "Mozilla/5.0"}

    def __init__(self, base_url):

        if not base_url.lower().startswith('http://') and not base_url.lower().startswith('https://'):
            base_url = 'https://' + base_url

        try:
            self.url = requests.get(base_url, headers=self.headers).url

        except requests.exceptions.SSLError:
            self.url = requests.get(base_url, headers=self.headers, verify=False).url

    def check_url(self, url):
        if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
            url = 'https://' + url
        return url

    def get_requests(self):
        try:
            self.requests = requests.get(self.url, headers=self.headers)
        except requests.exceptions.SSLError:
            self.requests = requests.get(self.url, headers=self.headers, verify=False)
        return self.requests

    def get_soup(self):
        self.soup = BeautifulSoup(self.requests.text, 'html.parser')
        return self.soup