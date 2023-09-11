import sys
import time
from urllib.parse import urlparse

import requests

sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


class Main(E_URL):

    headers={"User-Agent":"Mozilla/5.0"}

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url

    def check_duplicate(self, value):

        index = {}

        url_parse = urlparse(self.url)
        
        url = f'{url_parse.scheme}://{url_parse.netloc}/{value}'

        r = requests.get(url, allow_redirects=False, headers=self.headers)

        if r.status_code == 200:

            index['status'] = 'Error'
            index['class'] = 'error'
            index['text'] = f'{url} status code = 200. This creates a duplicate of the main page'

        else:

            index['status'] = 'Ok'
            index['class'] = 'ok'
            index['text'] = f'{url} status code = { r.status_code }'

        return index

    def index_html(self):

        index_html = {}

        url_parse = urlparse(self.url)
        
        url = f'{url_parse.scheme}://{url_parse.netloc}/index.html'

        r = requests.get(url, allow_redirects=False, headers=self.headers)

        if r.status_code == 200:

            index_html['status'] = 'Error'
            index_html['class'] = 'error'
            index_html['text'] = f'{url} status code = 200. This creates a duplicate of the main page'

        else:

            index_html['status'] = 'Ok'
            index_html['class'] = 'ok'
            index_html['text'] = f'{url} status code = { r.status_code }'

        return index_html

    def index_php(self):

        index_php = {}

        url_parse = urlparse(self.url)
        
        url = f'{url_parse.scheme}://{url_parse.netloc}/index.php'

        r = requests.get(url, allow_redirects=False, headers=self.headers)

        if r.status_code == 200:

            index_php['status'] = 'Error'
            index_php['class'] = 'error'
            index_php['text'] = f'{url} status code = 200. This creates a duplicate of the main page'

        else:

            index_php['status'] = 'Ok'
            index_php['class'] = 'ok'
            index_php['text'] = f'{url} status code = {r.status_code}'

        return index_php

    def main_html(self):

        main_html = {}

        url_parse = urlparse(self.url)
        
        url = f'{url_parse.scheme}://{url_parse.netloc}/main.html'

        r = requests.get(url, allow_redirects=False, headers=self.headers)

        if r.status_code == 200:

            main_html['status'] = 'Error'
            main_html['class'] = 'error'
            main_html['text'] = f'{url} status code = 200. This creates a duplicate of the main page'

        else:

            main_html['status'] = 'Ok'
            main_html['class'] = 'ok'
            main_html['text'] = f'{url} status code = {r.status_code}'

        return main_html

    def main_php(self):

        main_php = {}

        url_parse = urlparse(self.url)
        
        url = f'{url_parse.scheme}://{url_parse.netloc}/main.php'

        r = requests.get(url, allow_redirects=False, headers=self.headers)

        if r.status_code == 200:

            main_php['status'] = 'Error'
            main_php['class'] = 'error'
            main_php['text'] = f'{url} status code = 200. This creates a duplicate of the main page'

        else:

            main_php['status'] = 'Ok'
            main_php['class'] = 'ok'
            main_php['text'] = f'{url} status code = {r.status_code}'

        return main_php


def main_pars(url):

    lst = []

    M = Main(url)

    M.index_html()

    index_html = M.index_html()
    print(index_html)
    lst.append(['index_html', index_html])

    index_php = M.index_php()
    print(index_php)
    lst.append(['index_php', index_php])

    main_html = M.main_html()
    print(main_html)
    lst.append(['main_html', main_html])

    main_php = M.main_php()
    print(main_php)
    lst.append(['main_php', main_php])

    return lst

    
if __name__ == '__main__':

    url = 'liga.net'

    M = Main(url)

    M.index_html()

    index_html = M.index_html()
    print(index_html)

    index_php = M.index_php()
    print(index_php)

    main_html = M.main_html()
    print(main_html)

    main_php = M.main_php()
    print(main_php)
