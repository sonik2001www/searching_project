from http import server
import sys
import re
import socket
import time
from urllib.parse import urlparse


sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


class General(E_URL):
    
    def __init__(self, url):
        
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url
        self.schema = urlparse(self.url)
    
    def check_favicon(self):

        self.favicon = {}

        favicon = self.soup.find('link', {'rel': re.compile("(icon|shortcut icon)")})

        if favicon:
            
            self.favicon['status'] = "Ok"
            self.favicon['text'] = "You have favicon on your website"
            self.favicon['class'] = "ok"
    
        else:

            self.favicon['status'] = "Error"
            self.favicon['text'] = "You don't have favicon on your website"
            self.favicon['class'] = "error"

        return self.favicon

    def check_viewport(self):

        self.viewport = {}

        if "viewport" in self.source:

            self.viewport['text'] = "Your page specifies a viewport matching the device's size, allowing it to render appropriately across devices."
            self.viewport['status'] = "Ok"
            self.viewport['class'] = "ok"

        else:

            self.viewport['text'] = "Your page doesn't have a viewport tag"
            self.viewport['status'] = "Error"
            self.viewport['class'] = "error"

        return self.viewport
    
    def check_noindex(self):

        self.noindex = {}

        if not "<noindex>" in self.source:

            self.noindex['text'] = "You don't have noindex tags on your site"
            self.noindex['status'] = "Ok"
            self.noindex['class'] = "ok"

        else:

            self.noindex['text'] = "You have noindex tags on your site"
            self.noindex['status'] = "Error"
            self.noindex['class'] = "error"
            
        return self.noindex

    def check_nofollow(self):

        self.nofollow = {}

        pattern = "rel.?=.?(\"|')nofollow(\"|')"
        nofollow_tag = re.search(pattern, self.source)

        if nofollow_tag:

            self.nofollow['text'] = "You have nofollow tags on your site"
            self.nofollow['status'] = "Error"
            self.nofollow['class'] = "error"

        else:

            self.nofollow['text'] = "You don't have nofollow tags on your site"
            self.nofollow['status'] = "Ok"
            self.nofollow['class'] = "ok"

        return self.nofollow

    def check_frame(self):

        self.frame = {}

        if not "<frame>" in self.source:

            self.frame['text'] = "You don't have frames on your site"
            self.frame['status'] = "Ok"
            self.frame['class'] = "ok"

        else:

            self.frame['text'] = "You have frames on your site"
            self.frame['status'] = "Error"
            self.frame['status'] = "error"

        return self.frame

    # Removed 2022-12-08
    # def check_canonical(self):

    #     self.canonical = {}

    #     pattern = "rel.?=.?(\"|')canonical(\"|')"
    #     canonical_tag = re.search(pattern, self.source)

    #     if canonical_tag:
    #         self.canonical['text'] = "You have rel=\"canonical\" on your site"
    #         self.canonical['status'] = "Info"
    #     else:
    #         self.canonical['text'] = "You don't have rel=\"canonical\" on your site"
    #         self.canonical['status'] = "Info"
    #     return self.canonical

    def check_styles(self):
        
        self.styles = {}

        pattern = "style.?="
        style_tag = re.search(pattern, self.source)

        if style_tag:

            self.styles['text'] = "You are using inline styles."
            self.styles['status'] = "Error"
            self.styles['class'] = "error"

        else:

            self.styles['text'] = "No inline styles found"
            self.styles['status'] = "OK"
            self.styles['class'] = "ok"

        return self.styles

    def check_deprecated_tags(self):

        self.deprecated_tags = {}

        deprecated_tags_list = [
            '<acronym>',
            '<applet>',
            '<basefont>',
            '<big>',
            '<center>',
            '<dir>',
            '<font>',
            '<frame>',
            '<frameset>',
            '<isindex>',
            '<noframes>',
            '<s>',
            '<strike>',
            '<tt>',
        ]
        tags_found_list = []
        for dep_tag in deprecated_tags_list:

            if dep_tag in self.source:
                tags_found_list.append(dep_tag)
                self.deprecated_tags['text'] = f"We found the following deprecated tags on the page: {tags_found_list}"
                self.deprecated_tags['status'] = "Error"
                self.deprecated_tags['class'] = "error"

            else:
                self.deprecated_tags['text'] = "Your page does not use HTML deprecated tags"
                self.deprecated_tags['status'] = "Ok"
                self.deprecated_tags['class'] = "ok"

        return self.deprecated_tags

    def check_meta_refresh(self):

        self.meta_refresh = {}
        
        pattern = "http-equiv.?=.?(\"|')refresh(\"|')"
        meta_refresh_tag = re.search(pattern, self.source)

        if meta_refresh_tag:

            self.meta_refresh['text'] = "We found meta refresh redirect on your page"
            self.meta_refresh['status'] = "Error"
            self.meta_refresh['class'] = "error"

        else:

            self.meta_refresh['text'] = "Webpage is not using a meta refresh tag."
            self.meta_refresh['status'] = "Ok"
            self.meta_refresh['class'] = "ok"

        return self.meta_refresh

    def check_cloudflare(self):

        cloudflare = {}

        try:

            if self.requests.headers['server'] == 'cloudflare':

                cloudflare['text'] = 'Your website is using Cloudflare'
                cloudflare['status'] = 'Ok'
                cloudflare['class'] = 'ok'

            else:

                cloudflare['text'] = 'Your website is not using Cloudflare'
                cloudflare['status'] = 'Error'
                cloudflare['class'] = 'error'

        except KeyError:
                cloudflare['text'] = 'Your website is not using Cloudflare'
                cloudflare['status'] = 'Error'
                cloudflare['class'] = 'error'
                
        return cloudflare

    def check_encoding(self):

        encoding = {}
        
        try:
            enc = self.requests.headers['content-encoding'].lower()

            if enc == 'gzip':

                encoding['status'] = 'Ok'
                encoding['text'] = 'Your website is using gzip'
                encoding['class'] = 'ok'

            else:

                encoding['status'] = 'Error'
                encoding['text'] = 'Your website is not using gzip'
                encoding['class'] = 'error'
            
        except KeyError:

                encoding['status'] = 'Error'
                encoding['text'] = 'Econding not found'
                encoding['class'] = 'error'
        
        return encoding

    def check_content_type(self):

        content_type = {}

        c = self.requests.headers['content-type'].split(';')[0]
        print

        if c == 'text/html':

            content_type['status'] = 'Ok'
            content_type['text'] = 'Your website is using text/html'
            content_type['class'] = 'ok'

        else:

            content_type['status'] = 'Error'
            content_type['text'] = 'Your website is not using text/html'
            content_type['class'] = 'error'

        return content_type

    def check_charset(self):

        charset = {}
        
        try:
            char = self.requests.headers['content-type'].split(';')[1].split('=')[1].lower()

            if char == 'utf-8':

                charset['status'] = 'Ok'
                charset['text'] = 'Your website is using UTF-8'
                charset['class'] = 'ok'

            else:

                charset['status'] = 'Error'
                charset['text'] = f'Your website is using {char}'
                charset['class'] = 'error'
        
        except IndexError:
            
            charset['status'] = 'Error'
            charset['text'] = f'Charset not found'
            charset['class'] = 'error'

        return charset

    def check_google_an(self):

        google_an = {}
        
        if 'googleanalytics' in self.source.lower() or 'google-analytics':

            google_an['status'] = 'Ok'
            google_an['text'] = f'Your website is using Google Analytics'
            google_an['class'] = 'ok'

        else:
            
            google_an['status'] = 'Error'
            google_an['text'] = f'Google Analytics not found'
            google_an['class'] = 'error'

        return google_an

    def check_ip(self):
        return socket.gethostbyname(self.schema.netloc)

    def check_server_response_time(self):

        time = {}

        t = round(self.requests.elapsed.total_seconds() * 1000)

        if t > 200:

            time['status'] = 'Error'
            time['text'] = f'Your server response time is {t} ms.'
            time['class'] = 'error'

        else:

            time['status'] = 'Ok'
            time['text'] = f'Your server response time is {t} ms.'
            time['class'] = 'ok'

        return time
    
    def check_page_size(self):

        size = {}

        s = round(len(self.source) / 1000)
        
        if s > 100:

            size['status'] = 'Error'
            size['text'] = f'Your page size is {s} kb.'
            size['class'] = 'error'

        else:

            size['status'] = 'Ok'
            size['text'] = f'Your page size is {s} kb.'
            size['class'] = 'ok'

        return size


def general_pars(link):
    lst = []
    lst_status = []
    Gen = General(link)

    start = time.time()

    # Favicon
    favicon = Gen.check_favicon()
    print('Favicon: ', favicon)
    lst_status.append(['Favicon', favicon])

    Viewport = Gen.check_viewport()
    lst_status.append(['Viewport', Viewport])

    Noindex = Gen.check_noindex()
    lst_status.append(['Noindex', Noindex])

    Nofollow = Gen.check_nofollow()
    lst_status.append(['Nofollow', Nofollow])

    Frame = Gen.check_frame()
    lst_status.append(['Frame', Frame])

    Styles = Gen.check_frame()
    lst_status.append(['Styles', Styles])

    deprecated_tags = Gen.check_deprecated_tags()
    lst_status.append(['Deprecated Tags', deprecated_tags])

    meta_refresh = Gen.check_meta_refresh()
    print('\nMeta Refresh: ', meta_refresh)
    lst_status.append(['Meta Refresh', meta_refresh])

    cloudflare = Gen.check_cloudflare()
    print('\nCloudflare: ', cloudflare)
    lst_status.append(['Cloudflare', cloudflare])

    encoding = Gen.check_encoding()
    print('\nEncoding: ', encoding)
    lst_status.append(['Encoding', encoding])

    content_type = Gen.check_content_type()
    print('\nContent_type: ', content_type)
    lst_status.append(['Content type', content_type])

    charset = Gen.check_charset()
    print('\nCharset: ', charset)
    lst_status.append(['Charset', charset])

    google_an = Gen.check_google_an()
    print('\nGoogle Analytics: ', google_an)
    lst_status.append(['Google Analytics', google_an])

    ip = Gen.check_ip()
    print('\nIP: ', ip)
    lst.append(['IP', ip])

    server_response_time = Gen.check_server_response_time()
    print('\nServer Response Time: ', server_response_time)
    lst_status.append(['Server Response Time', server_response_time])

    page_size = Gen.check_page_size()
    print('\nPage Size: ', page_size)
    lst_status.append(['Page Size', page_size])

    print('HEADERS')
    for key, info in Gen.requests.headers.items():
        print(key, ' - ', info)
        lst.append([key, info])

    end = time.time()
    result = end - start
    print('\nTIME: ', result)
    lst.append(['TIME', result])

    return lst, lst_status


if __name__ == '__main__':
    
    sites_list = ['https://sefon.pro/']
    
    for url in sites_list:

        # url = 'liga.net'

        print()
        print('#########################')
        print(url)
        print('#########################')

        start = time.time()

        Gen = General(url)

        # Favicon
        favicon = Gen.check_favicon()
        print('Favicon: ', favicon)

        # Viewport
        print(Gen.check_viewport()['text'])
        print(Gen.check_viewport()['status'])

        # Noindex
        print(Gen.check_noindex()['text'])
        print(Gen.check_noindex()['status'])

        # Nofollow
        print(Gen.check_nofollow()['text'])
        print(Gen.check_nofollow()['status'])

        # Frame
        print(Gen.check_frame()['text'])
        print(Gen.check_frame()['status'])


        # Styles
        print(Gen.check_styles()['text'])
        print(Gen.check_styles()['status'])

        # Deprecated Tags
        deprecated_tags = Gen.check_deprecated_tags()
        print()
        print('Deprecated Tags: ', deprecated_tags['text'])
        print('Deprecated Tags: ', deprecated_tags['status'])

        # Meta Refresh Redirect
        meta_refresh = Gen.check_meta_refresh()
        print('\nMeta Refresh: ', meta_refresh)

        cloudflare = Gen.check_cloudflare()
        print('\nCloudflare: ', cloudflare)

        encoding = Gen.check_encoding()
        print('\nEncoding: ', encoding)

        content_type = Gen.check_content_type()
        print('\nContent_type: ', content_type)

        charset = Gen.check_charset()
        print('\nCharset: ', charset)

        google_an = Gen.check_google_an()
        print('\nGoogle Analytics: ', google_an)

        ip = Gen.check_ip()
        print('\nIP: ', ip)

        server_response_time = Gen.check_server_response_time()
        print('\nServer Response Time: ', server_response_time)

        page_size = Gen.check_page_size()
        print('\nPage Size: ', page_size)

        print('HEADERS')
        for key, info in Gen.requests.headers.items():
            print(key, ' - ', info)

        end = time.time()
        result = end-start
        print('\nTIME: ', result)
