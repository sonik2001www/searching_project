import sys
import time

import requests
from urllib.parse import urlparse
from urllib3.exceptions import NewConnectionError


sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


class Redirects(E_URL):

    headers={"User-Agent":"Mozilla/5.0"}

    def __init__(self, url):

        # self.url = url
        # self.netloc = urlparse(url).netloc.replace('www.', '')
        # self.f_url = self.netloc + self.url.split(self.netloc)[1]
        # self.http_url = "http://" + self.netloc
        # self.https_url = "https://" + self.netloc
        # self.www_http_url = "http://www." + self.netloc
        # self.www_https_url = "https://www." + self.netloc

        self.netloc = urlparse(url).netloc.replace('www.', '')
        self.url = self.netloc + url.split(self.netloc)[1]
        self.http_url = "http://" + self.url
        self.https_url = "https://" + self.url
        self.www_http_url = "http://www." + self.url
        self.www_https_url = "https://www." + self.url

        print()
        print('#####')
        print('HTTP: ', self.http_url)
        print('HTTPS: ', self.https_url)
        print('WWW HTTP: ', self.www_http_url)
        print('WWW HTTPS: ', self.www_https_url)
        print('#####')

    
    def get_schema(self, link):

        self.schema = {}
        try:
            r = requests.get(link, headers=self.headers)

            self.schema['source_link'] = link

            history = r.history
            if len(history) > 0:
                self.schema['source_status_code'] = history[-1].status_code
            else:
                self.schema['source_status_code'] = 200

            self.schema['final_link'] = r.url
            self.schema['final_status_code'] = r.status_code
        
        except requests.exceptions.ConnectionError:
            self.schema['source_link'] = link
            self.schema['source_status_code'] = 'Connection Error'
            self.schema['final_link'] = 'Connection Error'
            self.schema['final_status_code'] = 'Connection Error'

        return self.schema

    
    def get_http(self):
        return self.get_schema(self.http_url)


    def get_https(self):
        return self.get_schema(self.https_url)


    def get_www_http(self):
        return self.get_schema(self.www_http_url)


    def get_www_https(self):
        return self.get_schema(self.www_https_url) 


def redirects_pars(url):

    lst = []
    lst_status = []

    print()
    print('#########################')
    print(url)
    print('#########################')

    E = E_URL(url)
    base_url_requests = E.get_requests()
    url = base_url_requests.url
    print('Final URL: ', url)
    lst.append(['Final URL: ', url])

    R = Redirects(url)

    r_http = R.get_http()
    print(r_http)
    lst_status.append(['r http', r_http])
    r_https = R.get_https()
    print(r_https)
    lst_status.append(['r https', r_https])
    r_www_http = R.get_www_http()
    print(r_www_http)
    lst_status.append(['r www http', r_www_http])
    r_www_https = R.get_www_https()
    print(r_www_https)
    lst_status.append(['r www https', r_www_https])

    return lst, lst_status


if __name__ == '__main__':

    sites_list = ['https://www.kinofilms.ua/movie/942584/']
    
    for url in sites_list:
        
        print()
        print('#########################')
        print(url)
        print('#########################')


        E = E_URL(url)
        base_url_requests = E.get_requests()
        url = base_url_requests.url
        print('Final URL: ', url)

        R = Redirects(url)

        r_http = R.get_http()
        print(r_http)
        r_https = R.get_https()
        print(r_https)
        r_www_http = R.get_www_http()
        print(r_www_http)
        r_www_https = R.get_www_https()
        print(r_www_https)






