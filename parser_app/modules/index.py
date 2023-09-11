import sys
import time
import re
from bs4 import BeautifulSoup

sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


class Index(E_URL):

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url

    def check_404_page(self):

        check_404 = {}

        url_404 = f'{self.url}asfkj4543df'
        r = requests.get(url_404, allow_redirects=False)

        if r.status_code == 200:
            check_404['status'] = 'Ok'
            check_404['text'] = 'Error page responds 404 status code'
            check_404['class'] = 'ok'

        else:
            check_404['status'] = 'Error'
            check_404['text'] = 'Error page does not respond 404 status code'
            check_404['class'] = 'error'

        return check_404

    
    def noindex(self):
        self.noindex = {}
        
        if not "<noindex>" in self.source:
            self.noindex['status'] = "Ok"
            self.noindex['text'] = "You don't have noindex tags on your site"
            self.noindex['class'] = "ok"
            
        
        else:
            self.noindex['status'] = "Error"
            self.noindex['text'] = "You have noindex tags on your site"
            self.noindex['class'] = "error"
            
        return self.noindex


    def nofollow(self):

        self.nofollow = {}

        pattern = "rel.?=.?(\"|')nofollow(\"|')"
        nofollow_tag = re.search(pattern, self.source)

        if nofollow_tag:
            self.nofollow['status'] = "Error"
            self.nofollow['text'] = "You have nofollow tags on your site"
            self.nofollow['class'] = "error"

        else:
            self.nofollow['status'] = "Ok"
            self.nofollow['text'] = "You don't have nofollow tags on your site"
            self.nofollow['class'] = "ok"
            

        return self.nofollow

    
    def meta_noidex(self):

        meta_noindex = {}

        meta_list = self.soup.find_all('meta')
            
        for meta in meta_list:

            if 'noindex' in meta:
                meta_noindex['status'] = 'Error'
                meta_noindex['text'] = 'You have meta noindex tag'
                meta_noindex['class'] = 'error'

            else:
                meta_noindex['status'] = 'Ok'
                meta_noindex['text'] = 'You do not have meta noindex tag'
                meta_noindex['class'] = 'ok'

        return meta_noindex


    
    def meta_nofollow(self):

        meta_nofollow = {}

        meta_list = self.soup.find_all('meta')
            
        for meta in meta_list:

            if 'nofollow' in meta:
                meta_nofollow['status'] = 'Error'
                meta_nofollow['text'] = 'You have meta nofollow tag'
                meta_nofollow['class'] = 'error'

            else:
                meta_nofollow['status'] = 'Ok'
                meta_nofollow['text'] = 'You do not have meta nofollow tag'
                meta_nofollow['class'] = 'ok'

        return meta_nofollow

    
    def content_type(self):
        
        content_type = {}

        try:
            content = self.requests.headers['Content-Type'].split(';')[0].strip().lower()
            
            if content == 'text/html':
                content_type['status'] = 'Ok'
                content_type['text'] = f'Content-Type is correct: {content}'
                content_type['class'] = 'ok'

            else:
                content_type['status'] = 'Error'
                content_type['text'] = 'Content-Type is not text/html'
                content_type['class'] = 'error'

        except:
            
            content_type['status'] = 'Error'
            content_type['text'] = 'Content-Type is not set'
            content_type['class'] = 'error'

        return content_type


    def encoding(self):
        
        encoding = {}

        try:
            encoding_headers = self.requests.headers['Content-Type'].split(';')[1].split('=')[1].strip().lower()
            
            if encoding_headers == 'utf-8':
                encoding['status'] = 'Ok'
                encoding['text'] = f'Encoding is correct: {encoding_headers}'
                encoding['class'] = 'ok'

            else:
                encoding['status'] = 'Error'
                encoding['text'] = 'encoding is not utf-8'
                encoding['class'] = 'error'

        except:
            
            encoding['status'] = 'Error'
            encoding['text'] = 'Encoding is not set'
            encoding['class'] = 'error'

        return encoding


    def base_url_avaliable(self):

        base_url = {}

        try:

            base = self.soup.find('base')
            
            if base != None:

                base_url['status'] = 'Ok'
                base_url['text'] = 'Base URL found'
                base_url['class'] = 'ok'

            else:

                base_url['status'] = 'Error'
                base_url['text'] = 'Base URL not found'
                base_url['class'] = 'error'


        except:

            base_url['status'] = 'Error'
            base_url['text'] = 'Base URL not found'
            base_url['class'] = 'error'

        
        return base_url


    def base_url_empty(self):

        base_url_empty = {}

        try:

            base = self.soup.find('base')['href']
            
            if base != None and base != '' and base != ' ':

                base_url_empty['status'] = 'Ok'
                base_url_empty['text'] = 'Base URL href attr is not empty'
                base_url_empty['class'] = 'ok'

            else:

                base_url_empty['status'] = 'Error'
                base_url_empty['text'] = 'Base URL href attr is empty'
                base_url_empty['class'] = 'error'


        except:

            base_url_empty['status'] = 'Error'
            base_url_empty['text'] = 'Base URL not found'
            base_url_empty['class'] = 'error'

        return base_url_empty


    def base_url_equal(self):

        base_url_equal = {}

        try:

            base = self.soup.find('base')['href']
            
            if base == self.url:

                base_url_equal['status'] = 'Ok'
                base_url_equal['text'] = 'Base URL = website URL'
                base_url_equal['class'] = 'ok'

            else:

                base_url_equal['status'] = 'Error'
                base_url_equal['text'] = 'Base URL and website URL differs'
                base_url_equal['class'] = 'error'

        except:

            base_url_equal['status'] = 'Error'
            base_url_equal['text'] = 'Base URL not found'
            base_url_equal['class'] = 'error'

        return base_url_equal


    def base_url_quantity(self):

        base_url_quantity = {}

        try:

            base = self.soup.find_all('base')
            count = len(base)
            
            if count == 0:

                base_url_quantity['status'] = 'Error'
                base_url_quantity['text'] = 'Base URL not found'
                base_url_quantity['class'] = 'error'

            elif count == 1:

                base_url_quantity['status'] = 'Ok'
                base_url_quantity['text'] = 'You have 1 base URL tag'
                base_url_quantity['class'] = 'ok'

            elif count > 1:

                base_url_quantity['status'] = 'Error'
                base_url_quantity['text'] = f'You have {count} base URL tags'
                base_url_quantity['class'] = 'error'

        except:

            base_url_quantity['status'] = 'Error'
            base_url_quantity['text'] = 'Base URL not found'
            base_url_quantity['class'] = 'error'

        return base_url_quantity


    def robots_noindex(self):

        robots_noindex = {}

        try:

            meta = self.soup.find('meta', attrs={'name':'robots'})['content']
            
            if 'noindex' in meta:

                robots_noindex['status'] = 'Error'
                robots_noindex['text'] = 'Meta Robots Noindex found'
                robots_noindex['class'] = 'error'

            else:

                robots_noindex['status'] = 'Ok'
                robots_noindex['text'] = 'Meta Robots Noindex not found'
                robots_noindex['class'] = 'ok'

        except Exception as e:
            
            robots_noindex['status'] = 'Ok'
            robots_noindex['text'] = 'Meta Robots Noindex not found'
            robots_noindex['class'] = 'ok'

        return robots_noindex


    def robots_nofollow(self):

        robots_nofollow = {}

        try:

            meta = self.soup.find('meta', attrs={'name':'robots'})['content']
            
            if 'nofollow' in meta:

                robots_nofollow['status'] = 'Error'
                robots_nofollow['text'] = 'Meta Robots Nofollow found'
                robots_nofollow['class'] = 'error'

            else:

                robots_nofollow['status'] = 'Ok'
                robots_nofollow['text'] = 'Meta Robots Nofollow not found'
                robots_nofollow['class'] = 'ok'


        except Exception as e:
            
            robots_nofollow['status'] = 'Ok'
            robots_nofollow['text'] = 'Meta Robots Nofollow not found'
            robots_nofollow['class'] = 'ok'

        return robots_nofollow


    def robots_none(self):

        robots_none = {}

        try:

            meta = self.soup.find('meta', attrs={'name':'robots'})['content']
            
            if 'none' in meta:

                robots_none['status'] = 'Error'
                robots_none['text'] = 'Meta Robots None found'
                robots_none['class'] = 'error'

            else:

                robots_none['status'] = 'Ok'
                robots_none['text'] = 'Meta Robots None not found'
                robots_none['class'] = 'ok'


        except Exception as e:
            
            robots_none['status'] = 'Ok'
            robots_none['text'] = 'Meta Robots None not found'
            robots_none['class'] = 'ok'

        return robots_none


    def robots_noimageindex(self):

        robots_noimageindex = {}

        try:

            meta = self.soup.find('meta', attrs={'name':'robots'})['content']
            
            if 'noimageindex' in meta:

                robots_noimageindex['status'] = 'Error'
                robots_noimageindex['text'] = 'Meta Robots Noimageindex found'
                robots_noimageindex['class'] = 'error'

            else:

                robots_noimageindex['status'] = 'Ok'
                robots_noimageindex['text'] = 'Meta Robots Noimageindex not found'
                robots_noimageindex['class'] = 'ok'


        except Exception as e:
            
            robots_noimageindex['status'] = 'Ok'
            robots_noimageindex['text'] = 'Meta Robots Noimageindex not found'
            robots_noimageindex['class'] = 'ok'

        return robots_noimageindex

    
    def content_after_html(self):
        
        content_after_html = {}

        try:

            html = self.source.split('</html>')
            content_after = len(html[1].strip())
            
            if content_after > 0:

                content_after_html['status'] = 'Error'
                content_after_html['text'] = 'Page has content after </html> tag'
                content_after_html['class'] = 'error'

            else:

                content_after_html['status'] = 'Ok'
                content_after_html['text'] = 'Page has no content after </html> tag'
                content_after_html['class'] = 'ok'

        except Exception as e:
            
            content_after_html['status'] = 'Error'
            content_after_html['text'] = 'Closing </html> tag not found'
            content_after_html['class'] = 'error'

        return content_after_html


    def content_before_doctype(self):
        
        content_before_doctype = {}

        try:

            pattern = "<!.* html>"
            doctype = re.search(pattern, self.source.lower()).group()
            doctype_split = self.source.split(doctype)
            before = doctype_split[0]
            
            if len(before) > 0:

                content_before_doctype['status'] = 'Error'
                content_before_doctype['text'] = 'Page has content before Doctype tag'
                content_before_doctype['class'] = 'error'

            else:

                content_before_doctype['status'] = 'Ok'
                content_before_doctype['text'] = 'Page has no content before Doctype tag'
                content_before_doctype['class'] = 'ok'

        except Exception as e:
            
            content_before_doctype['status'] = 'Error'
            content_before_doctype['text'] = 'Doctype tag not found'
            content_before_doctype['class'] = 'error'

        return content_before_doctype


    def meta_robots_head(self):

        meta_robots_head = {}

        meta_robots = self.soup.find_all('meta', attrs={'name':'robots'})

        if meta_robots:
            
            # Delete <head> from html
            head = '<head.*>[\s\S]*</head>'
            html_no_head = re.sub(head, '', self.source)

            # Check if robots is outside <head>
            no_head_soup = BeautifulSoup(html_no_head, 'html.parser')
            robots = no_head_soup.find_all('meta', attrs={'name':'robots'})
            robots_len = len(robots)

            if robots_len == 0:
                
                meta_robots_head['status'] = 'Ok'
                meta_robots_head['text'] = 'Robots tag was not found outside of <head></head>'
                meta_robots_head['class'] = 'ok'

            else:
                meta_robots_head['status'] = 'Error'
                meta_robots_head['text'] = f'{robots_len} robots tags were found outside of <head></head>'
                meta_robots_head['class'] = 'error'

        else:
            meta_robots_head['status'] = 'Ok'
            meta_robots_head['text'] = 'Robots tags not found'
            meta_robots_head['class'] = 'ok'

        return meta_robots_head


def index_pars(url):

    lst = []

    I = Index(url)

    check_404 = I.check_404_page()
    print(check_404)
    lst.append(["check_404", check_404])

    noindex = I.noindex()
    print(noindex)
    lst.append(["noindex", noindex])

    nofollow = I.nofollow()
    print(nofollow)
    lst.append(["nofollow", nofollow])

    meta_noindex = I.meta_noidex()
    print(meta_noindex)
    lst.append(["meta_noindex", meta_noindex])

    meta_nofollow = I.meta_nofollow()
    print(meta_nofollow)
    lst.append(["meta_nofollow", meta_nofollow])

    content_type = I.content_type()
    print(content_type)
    lst.append(["content_type", content_type])

    encoding = I.encoding()
    print('Encoding: ', encoding)
    lst.append(['Encoding: ', encoding])

    base_avaliable = I.base_url_avaliable()
    print('Avaliable: ', base_avaliable)
    lst.append(['Avaliable: ', base_avaliable])

    base_url_empty = I.base_url_empty()
    print('Empty: ', base_url_empty)
    lst.append(['Empty: ', base_url_empty])

    base_url_equal = I.base_url_equal()
    print('Equal: ', base_url_equal)
    lst.append(['Equal: ', base_url_equal])

    base_url_quantity = I.base_url_quantity()
    print('Quantity: ', base_url_quantity)
    lst.append(['Quantity: ', base_url_quantity])

    robots_noindex = I.robots_noindex()
    print('Robots Noindex: ', robots_noindex)
    lst.append(['Robots Noindex: ', robots_noindex])

    robots_nofollow = I.robots_nofollow()
    print('Robots Nofollow: ', robots_nofollow)
    lst.append(['Robots Nofollow: ', robots_nofollow])

    robots_none = I.robots_none()
    print(robots_none)
    lst.append(['robots_none', robots_none])

    robots_noimageindex = I.robots_noimageindex()
    print('Robots Noimageindex: ', robots_noimageindex)
    lst.append(['Robots Noimageindex: ', robots_noimageindex])

    content_after_html = I.content_after_html()
    print(content_after_html)
    lst.append(['content_after_html', content_after_html])

    content_before_doctype = I.content_before_doctype()
    print(content_before_doctype)
    lst.append(['content_before_doctype', content_before_doctype])

    meta_robots_head = I.meta_robots_head()
    print(meta_robots_head)
    lst.append(['meta_robots_head', meta_robots_head])

    return lst


if __name__ == '__main__':

    url = 'https://studiocake.kiev.ua'

    I = Index(url)
    
    check_404 = I.check_404_page()
    print(check_404)

    noindex = I.noindex()
    print(noindex)

    nofollow = I.nofollow()
    print(nofollow)

    meta_noindex = I.meta_noidex()
    print(meta_noindex)

    meta_nofollow = I.meta_nofollow()
    print(meta_nofollow)

    content_type = I.content_type()
    print(content_type)

    encoding = I.encoding()
    print('Encoding: ', encoding)

    base_avaliable = I.base_url_avaliable()
    print('Avaliable: ', base_avaliable)

    base_url_empty = I.base_url_empty()
    print('Empty: ', base_url_empty)

    base_url_equal = I.base_url_equal()
    print('Equal: ', base_url_equal)

    base_url_quantity = I.base_url_quantity()
    print('Quantity: ', base_url_quantity)

    robots_noindex = I.robots_noindex()
    print('Robots Noindex: ', robots_noindex)

    robots_nofollow = I.robots_nofollow()
    print('Robots Nofollow: ', robots_nofollow)

    robots_none = I.robots_none()
    print(robots_none)

    robots_noimageindex = I.robots_noimageindex()
    print('Robots Noimageindex: ', robots_noimageindex)

    content_after_html = I.content_after_html()
    print(content_after_html)

    content_before_doctype = I.content_before_doctype()
    print(content_before_doctype)

    meta_robots_head = I.meta_robots_head()
    print(meta_robots_head)
