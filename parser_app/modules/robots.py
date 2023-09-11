import os

import requests
import pathlib
import random
# import urllib.request
from urllib.parse import urlparse
import time
import re
import sys


import ssl
ssl._create_default_https_context = ssl._create_unverified_context


sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *

from pathlib import Path


headers={"User-Agent":"Mozilla/5.0"}


class TiRobots:

    def __init__(self, url):
        self.url = url

    def get_robots_url(self):

        url_parse = urlparse(self.url)
        scheme = url_parse.scheme
        netloc = url_parse.netloc

        url = f'{scheme}://{netloc}'

        if url.endswith('robots.txt'):
            self.robots_url = url
        elif url.endswith('/'):
            self.robots_url = url + "robots.txt" 
        else:
            self.robots_url = url + "/robots.txt"
        return self.robots_url

    def get_robots_requests(self):
        self.robots_requests = requests.get(self.robots_url, headers=headers, verify=True)
        # self.robots_requests = requests.get('https://www.tibrains.com/static/img/robo.txt', headers = headers)
        
        return self.robots_requests

    def check_robots_avaliable(self):
        
        self.robots_avaliable = {}
        
        if self.robots_requests.status_code == 200:

            self.robots_avaliable['text'] = "Robots.txt is avaliable"
            self.robots_avaliable['status'] = "Ok"
            self.robots_avaliable['class'] = "ok"

        else:

            self.robots_avaliable['text'] = "Robots.txt file is missing"
            self.robots_avaliable['status'] = "Error"
            self.robots_avaliable['class'] = "error"

        return self.robots_avaliable

    def check_robots_status_code(self):

        self.robots_status_code = {}

        if self.robots_requests.status_code == 200:

            self.robots_status_code['text'] = "Robots.txt status code is " + str(self.robots_requests.status_code)
            self.robots_status_code['status'] = "Ok"
            self.robots_status_code['class'] = "ok"

        else:

            self.robots_status_code['text'] = "Robots.txt status code is " + str(self.robots_requests.status_code) + "You should configure your robots.txt file to give status code 200"
            self.robots_status_code['status'] = "Error"
            self.robots_status_code['class'] = "error"

        return self.robots_status_code

    def check_robots_host(self):

        self.robots_host = {}

        if "host" in self.robots_requests.text.lower():

            self.robots_host['text'] = "Your Robots.txt file contains Host"
            self.robots_host['status'] = "Ok"
            self.robots_host['class'] = "ok"

        else:

            self.robots_host['text'] = "Host is missing in your Robots.txt file"
            self.robots_host['status'] = "Error"
            self.robots_host['class'] = "error"

        return self.robots_host

    def check_robots_sitemap(self):

        self.robots_sitemap = {}

        if "sitemap" in self.robots_requests.text.lower():

            self.robots_sitemap['text'] = "Your Robots.txt file contains Sitemap"
            self.robots_sitemap['status'] = "Ok"
            self.robots_sitemap['class'] = "ok"

        else:

            self.robots_sitemap['text'] = "Sitemap is missing in your Robots.txt file"
            self.robots_sitemap['status'] = "Error"
            self.robots_sitemap['class'] = "error"

        return self.robots_sitemap


    def check_robots_css(self):

        self.robots_css = {}
        pattern = "Disallow:.*\.css"

        try:

            disallow = re.search(pattern, self.robots_requests.text).group()
            self.robots_css['text'] = 'CSS files are blocked in your Robots.txt file.'
            self.robots_css['status'] = 'Error'
            self.robots_css['class'] = 'error'

        except:

            self.robots_css['text'] = 'CSS files are not blocked in your Robots.txt file.'
            self.robots_css['status'] = 'Ok'
            self.robots_css['class'] = 'ok'
        
        return self.robots_css


    def check_robots_js(self):
        
        self.robots_js = {}
        pattern = "Disallow:.*\.js"
        
        try:

            disallow = re.search(pattern, self.robots_requests.text).group()
            self.robots_js['text'] = 'JS files are blocked in your Robots.txt file.'
            self.robots_js['status'] = 'Error'
            self.robots_js['class'] = 'error'

        except:

            self.robots_js['text'] = 'JS files are not blocked in your Robots.txt file.'
            self.robots_js['status'] = 'Ok'
            self.robots_js['class'] = 'ok'
        
        return self.robots_js


    def check_robots_size(self):

        self.robots_size = {}

        dir = str(pathlib.Path(__file__).parent.resolve()).replace('seo', 'temp/')
        name = random.randint(1, 1000000)
        path = f"{dir}{name}.txt"

        save_file(self.robots_url, path)
        self.size = (os.path.getsize(path) / 1024) 
        os.remove(path)

        if self.size < 500:

            self.robots_size['text'] = f'{self.size} KB'
            self.robots_size['status'] = 'Ok'
            self.robots_size['class'] = 'ok'

        else:

            self.robots_size['text'] = f'{self.size} KB'
            self.robots_size['status'] = 'Error'
            self.robots_size['class'] = 'error'

        return self.robots_size

    
    def check_crawl_delay(self):

        crawl_delay = {}

        if 'Crawl-delay:' in self.robots_requests.text:

            crawl_delay['text'] = 'Your Robots.txt file contains Crawl-delay directive'
            crawl_delay['status'] = 'Ok'
            crawl_delay['class'] = 'ok'

        else:

            crawl_delay['text'] = 'Crawl-delay directive not found'
            crawl_delay['status'] = 'Error'
            crawl_delay['class'] = 'error'

        return crawl_delay


def robots_pars(url):
    lst = []
    lst_status = []

    print()
    print('#########################')
    print(url)
    print('#########################')

    start = time.time()

    # Get URL After Redirects
    E = E_URL(url)
    base_url_requests = E.get_requests()
    url = base_url_requests.url
    print('Final URL: ', url)
    lst.append(['Final URL', url])

    TiRo = TiRobots(url)

    # Get Robots URL
    robots_url = TiRo.get_robots_url()
    print('Robots URL: ', robots_url)
    lst.append(['Robots URL', robots_url])

    # Get Requests
    robots_requests = TiRo.get_robots_requests()
    print(robots_requests.status_code)
    lst.append(['Status Code', robots_requests.status_code])

    # Check Robots Avaliable
    robots_avaliable = TiRo.check_robots_avaliable()
    print(robots_avaliable)
    lst_status.append(['Robots Avaliable', robots_avaliable])

    # Check Robots Status Code
    robots_status_code = TiRo.check_robots_status_code()
    print(robots_status_code)
    lst_status.append(['Robots Status Code Text', robots_status_code])

    # Check Host in Robots
    robots_host = TiRo.check_robots_host()
    print(robots_host)
    lst_status.append(['Host in Robots', robots_host])

    # Check Sitemap in Robots
    robots_sitemap = TiRo.check_robots_sitemap()
    print(robots_sitemap)
    lst_status.append(['Sitemap in Robots', robots_sitemap])

    # Check CSS Blocking
    robots_css = TiRo.check_robots_css()
    print(robots_css)
    lst_status.append(['CSS Blocking', robots_css])

    # Check JS Blocking
    robots_js = TiRo.check_robots_js()
    print(robots_js)
    lst_status.append(['JS Blocking', robots_js])

    # Check Robots Size
    robots_size = TiRo.check_robots_size()
    print(robots_size)
    lst_status.append(['Robots Size', robots_size])

    # Crawl-delay
    crawl_delay = TiRo.check_crawl_delay()
    print(crawl_delay)
    lst_status.append(['Crawl delay', crawl_delay])

    end = time.time()
    result = end - start
    print('TIME: ', result)
    lst.append(['TIME', result])

    return lst, lst_status


if __name__ == '__main__':

    sites_list = ['https://www.liga.net/']
    
    for url in sites_list:

        print()
        print('#########################')
        print(url)
        print('#########################')

        start = time.time()


        # Get URL After Redirects
        E = E_URL(url)
        base_url_requests = E.get_requests()
        url = base_url_requests.url
        print('Final URL: ', url)


        TiRo = TiRobots(url)

        # Get Robots URL
        robots_url = TiRo.get_robots_url()
        print('Robots URL: ', robots_url)

        # Get Requests
        robots_requests = TiRo.get_robots_requests()
        print(robots_requests.status_code)


        # Check Robots Avaliable
        robots_avaliable = TiRo.check_robots_avaliable()
        print('')
        print('Robots Avaliable: ', robots_avaliable['text'])
        print('Robots Avaliable: ', robots_avaliable['status'])

        # Check Robots Status Code
        robots_status_code = TiRo.check_robots_status_code()
        print('')
        print('Robots Status Code Text: ', robots_status_code['text'])
        print('Robots Status Code Status: ', robots_status_code['status'])

        # Check Host in Robots
        robots_host = TiRo.check_robots_host()
        print('')
        print('Host in Robots: ', robots_host['text'])
        print('Host in Robots: ', robots_host['status'])

        # Check Sitemap in Robots
        robots_sitemap = TiRo.check_robots_sitemap()
        print('')
        print('Sitemap in Robots: ', robots_sitemap['text'])
        print('Sitemap in Robots: ', robots_sitemap['status'])

        # Check CSS Blocking
        robots_css = TiRo.check_robots_css()
        print('')
        print('CSS Blocking: ', robots_css['text'])
        print('CSS Blocking: ', robots_css['status'])

        # Check JS Blocking
        robots_js = TiRo.check_robots_js()
        print('')
        print('JS Blocking: ', robots_js['text'])
        print('JS Blocking: ', robots_js['status'])

        # Check Robots Size
        robots_size = TiRo.check_robots_size()
        print('')
        # print(robots_size)
        print('Robots Size: ', robots_size['text'])
        print('Robots Size: ', robots_size['status'])

        # Crawl-delay
        crawl_delay = TiRo.check_crawl_delay()
        print(crawl_delay)

        end = time.time()
        result = end-start
        print('TIME: ', result)

        print()
        print(url)

        print(robots_url)
        print(robots_requests)

        print(robots_css)
        print(robots_avaliable)