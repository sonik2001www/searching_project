import sys
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


class Canonical(E_URL):

    headers={"User-Agent":"Mozilla/5.0"}

    ERROR = 'You do not have rel="canonical" tag on your page'

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url

        pattern = "rel.?=.?(\"|')canonical(\"|')"
        self.canonical_tag = self.soup.find_all('link', rel = 'canonical')

    def check_canonical(self):

        self.canonical = {}

        if self.canonical_tag:
            self.canonical['status'] = 'Ok'
            self.canonical['class'] = 'ok'
            self.canonical['text'] = 'You have rel="canonical" tag on your page'
            
        else:
            self.canonical['status'] = 'Error'
            self.canonical['class'] = 'error'
            self.canonical['text'] = self.ERROR

        return self.canonical

    def count_canonical(self):

        self.count = {}

        if self.canonical_tag:

            canonical_len = len(self.canonical_tag)

            if canonical_len == 1:
                self.count['status'] = 'Ok'
                self.count['class'] = 'ok'
                self.count['text'] = 'You have 1 canonical tag'

            else:
                self.count['status'] = 'Error'
                self.count['class'] = 'error'
                self.count['text'] = f'You have {canonical_len} canonical tags'

        else:
            self.count['status'] = 'Error'
            self.count['class'] = 'error'
            self.count['text'] = self.ERROR

        return self.count

    def get_canonical_status_code(self):

        self.status_code = {}

        if self.canonical_tag:

            canonical_page = self.canonical_tag[0]['href']

            r = requests.get(canonical_page, headers=self.headers)
            
            if r.status_code == 200:

                self.status_code['status'] = 'Ok'
                self.status_code['class'] = 'ok'
                self.status_code['text'] = 'Canonical ulr responds 200 status code'

            else:
                self.status_code['status'] = 'Error'
                self.status_code['class'] = 'error'
                self.status_code['text'] = f'Canonical ulr responds {r.status_code} status code'

        else:
            self.status_code['status'] = 'Error'
            self.status_code['class'] = 'error'
            self.status_code['text'] = self.ERROR

        return self.status_code

    def check_empty(self):

        self.empty = {}

        if self.canonical_tag:

            canonical_page = self.canonical_tag[0]['href'].strip()
            
            if canonical_page == '' or canonical_page == ' ':

                self.empty['status'] = 'Error'
                self.empty['class'] = 'error'
                self.empty['text'] = 'Canonical ulr is empty'

            else:
                self.empty['status'] = 'Ok'
                self.empty['class'] = 'ok'
                self.empty['text'] = 'Canonical ulr is not empty'

        else:
            self.empty['status'] = 'Error'
            self.empty['class'] = 'error'
            self.empty['text'] = self.ERROR

        return self.empty

    def check_relative(self):

        self.relative = {}

        if self.canonical_tag:

            canonical_page = self.canonical_tag[0]['href'].strip()
            
            if canonical_page.startswith('/'):

                self.relative['status'] = 'Error'
                self.relative['class'] = 'error'
                self.relative['text'] = 'Canonical is a relative URL'

            else:
                self.relative['status'] = 'Ok'
                self.relative['class'] = 'ok'
                self.relative['text'] = 'Canonical is not a relative URL'

        else:
            self.relative['status'] = 'Error'
            self.relative['class'] = 'error'
            self.relative['text'] = self.ERROR

        return self.relative

    def canonical_equal(self):

        self.canonical = {}

        if self.canonical_tag:

            canonical_page = self.canonical_tag[0]['href'].strip()
            
            if canonical_page == self.url:

                self.canonical['status'] = 'Ok'
                self.canonical['class'] = 'ok'
                self.canonical['text'] = 'Canonical url equals page url'

            else:
                self.canonical['status'] = 'Error'
                self.canonical['class'] = 'error'
                self.canonical['text'] = 'Сanonical url is not equal to page url'

        else:
            self.canonical['status'] = 'Error'
            self.canonical['class'] = 'error'
            self.canonical['text'] = self.ERROR

        return self.canonical

    def canonical_head(self):

        self.head = {}

        if self.canonical_tag:
            
            # Delete <head> from html
            head = '<head.*>[\s\S]*</head>'
            html_no_head = re.sub(head, '', self.source)

            # Check if canonical is outside <head>
            no_head_soup = BeautifulSoup(html_no_head, 'html.parser')
            canonical = no_head_soup.find_all('link', rel = 'canonical')  
            canonical_len = len(canonical)

            if canonical_len == 0:
                
                self.head['status'] = 'Ok'
                self.head['class'] = 'ok'
                self.head['text'] = 'Canonical was not found outside of <head></head>'

            else:
                self.head['status'] = 'Error'
                self.head['class'] = 'error'
                self.head['text'] = f'{canonical_len} found outside of <head></head>'

        else:
            self.head['status'] = 'Error'
            self.head['class'] = 'error'
            self.head['text'] = self.ERROR

        return self.head

    def check_scheme(self):
        
        self.scheme = {}

        if self.canonical_tag:
        
            canonical_url  = canonical_page = self.canonical_tag[0]['href'].strip()
            base_url_scheme = urlparse(self.url).scheme

            if canonical_url.startswith('/'):

                self.scheme['status'] = 'Error'
                self.scheme['class'] = 'error'
                self.scheme['text'] = 'Canonical url is set as a relative path. You should set it as an absolute path with correct scheme: https or http'

            elif base_url_scheme == urlparse(canonical_url).scheme:
                
                self.scheme['status'] = 'Ok'
                self.scheme['class'] = 'ok'
                self.scheme['text'] = f'Website ulr and canonical url have the same scheme: {base_url_scheme}'
            
            else:

                self.scheme['status'] = 'Ok'
                self.scheme['class'] = 'ok'
                self.scheme['text'] = 'Website ulr and canonical have different schemes'

        else:
            self.scheme['status'] = 'Error'
            self.scheme['class'] = 'error'
            self.scheme['text'] = self.ERROR

        return self.scheme

    def canonical_robots(self):

        self.robots = {}

        if self.canonical_tag:

            netloc = urlparse(self.url).netloc
            scheme = urlparse(self.url).scheme
            robots_url = f'{scheme}://{netloc}/robots.txt'
            
            r = requests.get(robots_url, headers=self.headers)

            canonical_page = self.canonical_tag[0]['href'].strip()
            canonical_disallow = f'Disallow: {canonical_page}'
            
            if canonical_disallow in r.text:

                self.robots['status'] = 'Error'
                self.robots['class'] = 'error'
                self.robots['text'] = 'Canonical url is disallowed in robots.txt'

            else:
                self.robots['status'] = 'Ok'
                self.robots['class'] = 'ok'
                self.robots['text'] = 'Сanonical url is not disallowed in robots.txt'

        else:
            self.robots['status'] = 'Error'
            self.robots['class'] = 'error'
            self.robots['text'] = self.ERROR

        return self.robots
    
    def canonical_meta(self):

        self.meta = {}

        if self.canonical_tag:

            canonical_page = self.canonical_tag[0]['href'].strip()
            
            if canonical_page.startswith('/'):
                canonical_page = f'{self.url[:-1]}{canonical_page}'
            
            r = requests.get(canonical_page, headers=self.headers)
            meta_soup = BeautifulSoup(r.text, 'html.parser')
            meta_list = meta_soup.find_all('meta')
            
            for meta in meta_list:
                if 'noindex' in meta or 'nofollow' in meta:

                    self.meta['status'] = 'Error'
                    self.meta['class'] = 'error'
                    self.meta['text'] = 'Canonical page has meta noindex or nofollow'

                else:
                    self.meta['status'] = 'Ok'
                    self.meta['class'] = 'ok'
                    self.meta['text'] = 'Canonical page has no meta noindex or nofollow'

        else:
            self.meta['status'] = 'Error'
            self.meta['class'] = 'error'
            self.meta['text'] = self.ERROR

        return self.meta


def canonical_pars(url):

    lst = []

    print()
    print('#########################')
    print(url)
    print('#########################')

    C = Canonical(url)

    canonical = C.check_canonical()
    print('Avaliable: ', canonical)
    lst.append(['Avaliable', canonical])

    count = C.count_canonical()
    print('Count: ', count)
    lst.append(['Count', count])

    canonical_status_code = C.get_canonical_status_code()
    print('Status Code: ', canonical_status_code)
    lst.append(['Status Code', canonical_status_code])

    empty = C.check_empty()
    print('Empty: ', empty)
    lst.append(['Empty', empty])

    relative = C.check_relative()
    print('Relative: ', relative)
    lst.append(['Relative', relative])

    canonical_equal = C.canonical_equal()
    print('Equal: ', canonical_equal)
    lst.append(['Equal', canonical_equal])

    head = C.canonical_head()
    print('Outside head: ', head)
    lst.append(['Outside head', head])

    scheme = C.check_scheme()
    print('Scheme: ', scheme)
    lst.append(['Scheme', scheme])

    robots = C.canonical_robots()
    print('Robots: ', robots)
    lst.append(['Robots', robots])

    meta = C.canonical_meta()
    print('Meta: ', meta)
    lst.append(['Meta', meta])

    return lst


if __name__ == '__main__':
    
    sites_list = ['https://www.liga.net/']
    
    for url in sites_list:

        print()
        print('#########################')
        print(url)
        print('#########################')

        C = Canonical(url)

        canonical = C.check_canonical()
        print('Avaliable: ', canonical)

        count = C.count_canonical()
        print('Count: ', count)

        canonical_status_code = C.get_canonical_status_code()
        print('Status Code: ', canonical_status_code)

        empty = C.check_empty()
        print('Empty: ', empty)

        relative = C.check_relative()
        print('Relative: ', relative)

        canonical_equal = C.canonical_equal()
        print('Equal: ', canonical_equal)

        head = C.canonical_head()
        print('Outside head: ', head)

        scheme = C.check_scheme()
        print('Scheme: ', scheme)

        robots = C.canonical_robots()
        print('Robots: ', robots)

        meta = C.canonical_meta()
        print('Meta: ', meta)