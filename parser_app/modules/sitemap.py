import os
import random

import requests
import pathlib
from urllib.parse import urlparse
import re
import time
import sys


sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *



class Sitemap(E_URL):

    headers={"User-Agent": "Mozilla/5.0"}

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url

    def check_tag(self, tag):

        result = {}

        if tag in str(self.source.lower()):
            result['text'] = 'Tag found'
            result['status'] = 'Ok'
            result['class'] = 'ok'

        else:
            result['text'] = 'Tag is missing'
            result['status'] = 'Error'
            result['class'] = 'error'

        return result

# # Deleted 2022-01-12    
#     def get_sitemap_url(self):

#         url_parse = urlparse(self.url)
#         scheme = url_parse.scheme
#         netloc = url_parse.netloc

#         url = f'{scheme}://{netloc}'

#         if url.endswith('.xml'):
#             self.sitemap_url = url 
#         elif url.endswith('/'):
#             self.sitemap_url = url + "sitemap.xml" 
#         else:
#             self.sitemap_url = url + "/sitemap.xml"

#         return self.sitemap_url

    # Deleted 2022-01-12    
    # def get_sitemap_requests(self):
    #     self.sitemap_requests = requests.get(self.sitemap_url, headers=self.headers)
    #     return self.sitemap_requests

    def check_sitemap_avaliable(self):

        self.sitemap_avaliable = {}

        if self.requests.status_code == 200:

            self.sitemap_avaliable['text'] = "Sitemap.xml file is avalibale"
            self.sitemap_avaliable['status'] = "Ok"
            self.sitemap_avaliable['class'] = "ok"

        else:

            self.sitemap_avaliable['text'] = "Sitemap.xml file is NOT avalibale"
            self.sitemap_avaliable['status'] = "Error"
            self.sitemap_avaliable['class'] = "error"

        return self.sitemap_avaliable

    def check_sitemap_length(self):

        self.number_res = {}

        if self.requests.status_code == 200:

            number = self.requests.text.lower().count('<url>')

            if number > 1 and number < 50001:

                self.number_res['text'] = f'Sitemap.xml has {number} URLs.'
                self.number_res['status'] = 'Ok'
                self.number_res['class'] = 'ok'

            else:
                self.number_res['text'] = f'Sitemap.xml has {number} URLs.'
                self.number_res['status'] = 'Error'
                self.number_res['class'] = 'error'

        else:
            self.number_res['text'] = "Sitemap.xml file is NOT avalibale"
            self.number_res['status'] = "Error"
            self.number_res['class'] = "error"

        return self.number_res

    def check_sitemap_size(self):

        self.sitemap_size = {}

        if self.requests.status_code == 200:

            dir = str(pathlib.Path(__file__).parent.resolve()).replace('seo', 'temp/')
            name = random.randint(1, 1000000)
            path = f"{dir}{name}.xml"
            
            rew = save_file(self.url, path)

            if rew == False:
                self.sitemap_size['text'] = "Sitemap.xml file is NOT avalibale"
                self.sitemap_size['status'] = "Error"
                self.sitemap_size['class'] = "error"
                return self.sitemap_size

            self.size = (os.path.getsize(path) / 1024 / 1024)
            os.remove(path)

            if self.size < 50:
                self.sitemap_size['text'] = f'{self.size} MB'
                self.sitemap_size['status'] = 'Ok'
                self.sitemap_size['class'] = 'ok'

            else:
                self.sitemap_size['text'] = f'{self.size} MB'
                self.sitemap_size['status'] = 'Error'
                self.sitemap_size['class'] = 'error'

        else:
            self.sitemap_size['text'] = "Sitemap.xml file is NOT avalibale"
            self.sitemap_size['status'] = "Error"
            self.sitemap_size['class'] = "error"

        return self.sitemap_size

    def check_sitemap_status_code(self):

        self.sitemap_status_code = {}

        if self.requests.status_code == 200:

            self.sitemap_status_code['text'] = f'Sitemap.xml status code is {self.requests.status_code}'
            self.sitemap_status_code['status'] = "Ok"
            self.sitemap_status_code['class'] = "ok"

        else:

            self.sitemap_status_code['text'] = f'Sitemap.xml status code is {self.requests.status_code}. You should configure your sitemap.xml file to give status code 200'
            self.sitemap_status_code['status'] = "Error"
            self.sitemap_status_code['class'] = "error"

        return self.sitemap_status_code

    def check_sitemap_encoding(self):

        sitemap_encoding = {}

        if 'UTF-8'.lower() in self.source.lower():

            sitemap_encoding['text'] = "Sitemap.xml has correct Encoding: UTF-8"
            sitemap_encoding['status'] = "Ok"
            sitemap_encoding['class'] = "ok"

        else:

            sitemap_encoding['text'] = "Sitemap.xml has wrong Encoding. The correct Encodign for Sitemap.xml files is UTF-8"
            sitemap_encoding['status'] = "Error"
            sitemap_encoding['class'] = "error"

        return sitemap_encoding

    def check_sitemap_urlset(self):
        return self.check_tag('<urlset')

    def check_sitemap_url_tag(self):
        return self.check_tag('<url>')

    def check_sitemap_loc(self):
        return self.check_tag('<loc>')

    def check_sitemap_lastmod(self):
        return self.check_tag('<lastmod>')

    def check_sitemap_changefreq(self):
        return self.check_tag('<changefreq>')

    def check_sitemap_priority(self):
        return self.check_tag('<priority>')

    def check_domain_in_link(self):
        self.wrong_urls = []
        self.url_in_link = {}
        pattern = '<loc>.*</loc>'
        self.urls_list = re.findall(pattern, self.requests.text)
        for link in self.urls_list:
            if self.url in link:
                self.wrong_urls.append(link)
        
        if len(self.wrong_urls) == 0:
            self.url_in_link['text'] = 'All URLs start with domain name'
            self.url_in_link['status'] = 'Ok'
            self.url_in_link['class'] = 'ok'
        else:
            self.url_in_link['text'] = f'Some URLs don\'t start with domain name:\n {self.wrong_urls}'
            self.url_in_link['status'] = 'Error'
            self.url_in_link['class'] = 'error'

        return self.url_in_link


def sitemap_pars(url):

    lst = []
    lst_status = []

    print()
    print('#########################')
    print(url)
    print('#########################')
    start = time.time()

    SM = Sitemap(url)

    # Check Sitemap Status Code
    sitemap_status_code = SM.check_sitemap_status_code()
    print('')
    print('Sitemap Status Code Text: ', sitemap_status_code['text'])
    print('Sitemap Status Code Status: ', sitemap_status_code['status'])
    lst_status.append(['Sitemap Status Code Status', sitemap_status_code])

    # Check Sitemap.xml Avaliable
    sitemap_avalibale = SM.check_sitemap_avaliable()
    print('')
    print('Sitemap Avalibale Text: ', sitemap_avalibale['text'])
    print('Sitemap Avalibale Status: ', sitemap_avalibale['status'])
    lst_status.append(['Sitemap Avalibale Status', sitemap_avalibale])

    # Sitemap.xml Encoding
    sitemap_encoding = SM.check_sitemap_encoding()
    print('')
    print('Sitemap Encoding Text: ', sitemap_encoding['text'])
    print('Sitemap Encoding Status: ', sitemap_encoding['status'])
    lst_status.append(['Sitemap Encoding Status', sitemap_encoding])

    # Sitemap.xml Length
    sitemap_len = SM.check_sitemap_length()
    print('')
    print('Sitemap Length Text: ', sitemap_len['text'])
    print('Sitemap Length Status: ', sitemap_len['status'])
    lst_status.append(['Sitemap Length Status', sitemap_len])

    # Urlset Value
    sitemap_urlset = SM.check_sitemap_urlset()
    print('')
    print('Sitemap Urlset Text: ', sitemap_urlset['text'])
    print('Sitemap Urlset Status: ', sitemap_urlset['status'])
    lst_status.append(['Sitemap Urlset Status', sitemap_urlset])

    # URL Tag
    sitemap_url_tag = SM.check_sitemap_url_tag()
    print('')
    print('Sitemap URL Text: ', sitemap_url_tag['text'])
    print('Sitemap URL Status: ', sitemap_url_tag['status'])
    lst_status.append(['Sitemap URL Status', sitemap_url_tag])

    # LOC Tag
    sitemap_loc = SM.check_sitemap_loc()
    print('')
    print('Sitemap LOC Text: ', sitemap_loc['text'])
    print('Sitemap LOC Status: ', sitemap_loc['status'])
    lst_status.append(['Sitemap LOC Status', sitemap_loc])

    # LastMod Value
    sitemap_lastmod = SM.check_sitemap_lastmod()
    print('')
    print('Sitemap LastMod Text: ', sitemap_lastmod['text'])
    print('Sitemap LastMod Status: ', sitemap_lastmod['status'])
    lst_status.append(['Sitemap LastMod Status', sitemap_lastmod])

    # Priority Value
    sitemap_priority = SM.check_sitemap_priority()
    print('')
    print('Sitemap Priority Text: ', sitemap_priority['text'])
    print('Sitemap Priority Status: ', sitemap_priority['status'])
    lst_status.append(['Sitemap Priority Status: ', sitemap_priority])

    # Size
    sitemap_size = SM.check_sitemap_size()
    print('')
    print('Sitemap Size Text: ', sitemap_size['text'])
    print('Sitemap Size Status: ', sitemap_size['status'])
    lst_status.append(['Sitemap Size Status: ', sitemap_size])

    # Domain in link
    domain_in_link = SM.check_domain_in_link()
    print('')
    print('Domain in link Text: ', domain_in_link['text'])
    print('Domain in link Status: ', domain_in_link['status'])
    lst_status.append(['Domain in link Status: ', domain_in_link])

    end = time.time()
    result = end - start
    print('TIME: ', result)
    lst.append(['TIME: ', result])

    return lst, lst_status


if __name__ == '__main__':

    sites_list = ['https://www.liga.net/']
    
    for url in sites_list:

        print()
        print('#########################')
        print(url)
        print('#########################')
        start = time.time()
    
        # # Get URL After Redirects
        # E = E_URL(base_url)
        # base_url_requests = E.get_requests()
        # url = base_url_requests.url
        # print('Final URL: ', url)

        SM = Sitemap(url)

        # Sitemap.xml URL
        # sitemap_url = SM.get_sitemap_url()
        # print('Sitemap URL: ', sitemap_url)

        # # Get requests 
        # sitemap_requests = SM.get_sitemap_requests()

        # Check Sitemap Status Code
        sitemap_status_code = SM.check_sitemap_status_code()
        print('')
        print('Sitemap Status Code Text: ', sitemap_status_code['text'])
        print('Sitemap Status Code Status: ', sitemap_status_code['status'])

        # Check Sitemap.xml Avaliable
        sitemap_avalibale = SM.check_sitemap_avaliable()
        print('')
        print('Sitemap Avalibale Text: ', sitemap_avalibale['text'])
        print('Sitemap Avalibale Status: ', sitemap_avalibale['status'])

        # Sitemap.xml Encoding
        sitemap_encoding = SM.check_sitemap_encoding()
        print('')
        print('Sitemap Encoding Text: ', sitemap_encoding['text'])
        print('Sitemap Encoding Status: ', sitemap_encoding['status'])

        # Sitemap.xml Length
        sitemap_len = SM.check_sitemap_length()
        print('')
        print('Sitemap Length Text: ', sitemap_len['text'])
        print('Sitemap Length Status: ', sitemap_len['status'])

        # Urlset Value
        sitemap_urlset = SM.check_sitemap_urlset()
        print('')
        print('Sitemap Urlset Text: ', sitemap_urlset['text'])
        print('Sitemap Urlset Status: ', sitemap_urlset['status'])

        # URL Tag
        sitemap_url_tag = SM.check_sitemap_url_tag()
        print('')
        print('Sitemap URL Text: ', sitemap_url_tag['text'])
        print('Sitemap URL Status: ', sitemap_url_tag['status'])

        # LOC Tag
        sitemap_loc = SM.check_sitemap_loc()
        print('')
        print('Sitemap LOC Text: ', sitemap_loc['text'])
        print('Sitemap LOC Status: ', sitemap_loc['status'])

        # LastMod Value
        sitemap_lastmod = SM.check_sitemap_lastmod()
        print('')
        print('Sitemap LastMod Text: ', sitemap_lastmod['text'])
        print('Sitemap LastMod Status: ', sitemap_lastmod['status'])

        # Priority Value
        sitemap_priority = SM.check_sitemap_priority()
        print('')
        print('Sitemap Priority Text: ', sitemap_priority['text'])
        print('Sitemap Priority Status: ', sitemap_priority['status'])

        # Size
        sitemap_size = SM.check_sitemap_size()
        print('')
        print('Sitemap Size Text: ', sitemap_size['text'])
        print('Sitemap Size Status: ', sitemap_size['status'])

        # Domain in link
        domain_in_link = SM.check_domain_in_link()
        print('')
        print('Domain in link Text: ', domain_in_link['text'])
        print('Domain in link Status: ', domain_in_link['status'])


        end = time.time()
        result = end-start
        print('TIME: ', result)


