import sys
import time
import re
from urllib.parse import urlparse


sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


class Mobile(E_URL):

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url


    def apple_touch(self):

        apple_touch = {}

        apple_html = self.soup.find('link', attrs={'rel':'apple-touch-icon'})

        if apple_html == None:

            apple_touch['status'] = 'Error'
            apple_touch['class'] = 'error'
            apple_touch['text'] = 'Page does not have apple touch icon'

        else:

            apple_touch['status'] = 'Ok'
            apple_touch['class'] = 'ok'
            apple_touch['text'] = 'Page contains apple touch icon'

        return apple_touch

    

    def viewport(self):

        viewport = {}

        if "viewport" in self.source:
            viewport['text'] = "Your page specifies a viewport matching the device's size, allowing it to render appropriately across devices."
            viewport['status'] = "Ok"
            viewport['class'] = "ok"

        else:
            viewport['text'] = "Your page doesn't have a viewport tag"
            viewport['status'] = "Error"
            viewport['class'] = "error"

        return viewport


    def viewport_scale(self):

        viewport_scale = {}

        pattern = "initial-scale.*?=.*?1(.0)?"
        
        try:
            re.search(pattern, self.source).group()
            viewport_scale['status'] = 'Ok'
            viewport_scale['class'] = 'ok'
            viewport_scale['text'] = 'Initial Scale is set to 1'

        except AttributeError:
            viewport_scale['status'] = 'Error'
            viewport_scale['class'] = 'error'
            viewport_scale['text'] = 'Initial Scale is not set or is set incorrectly'

        return viewport_scale


    def viewport_width(self):

        viewport_width = {}

        pattern = "width.*?=.*?device-width"
        
        try:
            re.search(pattern, self.source).group()
            viewport_width['status'] = 'Ok'
            viewport_width['class'] = 'ok'
            viewport_width['text'] = 'Viewport width is set correctly'

        except AttributeError:

            viewport_width['status'] = 'Error'
            viewport_width['class'] = 'error'
            viewport_width['text'] = 'Viewport width is not set or is set incorrectly'

        return viewport_width

    
    def html5(self):

        html5 = {}

        if '<!DOCTYPE html>' in self.source:

            html5['status'] = "Ok"
            html5['class'] = "ok"
            html5['text'] = "The pages is using HTML5."
            
        else:

            html5['status'] = "Error"
            html5['class'] = "error"
            html5['text'] = "The page is using old version of HTML"
            
        return html5

    
    def medai_query(self):

        medai_query = {}

        css = self.soup.find('link', attrs={'rel':'stylesheet'})
        print(css)

        if '<!DOCTYPE html>' in self.source:

            medai_query['status'] = "Ok"
            medai_query['class'] = "ok"
            medai_query['text'] = "The pages is using HTML5."
            
        else:

            medai_query['status'] = "Error"
            medai_query['class'] = "error"
            medai_query['text'] = "The page is using old version of HTML"
            
        return medai_query


def mobile_pars(url):

    lst = []

    M = Mobile(url)

    html5 = M.html5()
    print(html5)
    lst.append(["html5", html5])

    apple_touch = M.apple_touch()
    print(apple_touch)
    lst.append(["apple_touch", apple_touch])

    viewport = M.viewport()
    print(viewport)
    lst.append(["viewport", viewport])

    viewport_scale = M.viewport_scale()
    print(viewport_scale)
    lst.append(["viewport_scale", viewport_scale])

    viewport_width = M.viewport_width()
    print(viewport_width)
    lst.append(["viewport_width", viewport_width])

    medai_query = M.medai_query()
    print(medai_query)
    lst.append(["medai_query", medai_query])

    return lst

    
if __name__ == '__main__':

    url = 'https://zabor.zp.ua'
    # url = 'rai.bz'

    M = Mobile(url)

    html5 = M.html5()
    print(html5)

    apple_touch = M.apple_touch()
    print(apple_touch)

    viewport = M.viewport()
    print(viewport)

    viewport_scale = M.viewport_scale()
    print(viewport_scale)

    viewport_width = M.viewport_width()
    print(viewport_width)

    medai_query = M.medai_query()
    print(medai_query)

