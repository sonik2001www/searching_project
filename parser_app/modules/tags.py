import sys
import time

sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


def check_len(tag_name, min, max, text):
    
    tag_len = {}
    tag_len_check = []

    if len(tag_name) !=0:
    
        for tag in tag_name:
            
            length = len(tag)
            
            if length >= min and length <= max:
                status = 'Ok'
                tag_class = 'ok'
            else:
                status = 'Error'
                tag_class = 'error'

            tag_len['tag'] = tag
            tag_len['len'] = f'{length}'
            tag_len['status'] = status
            tag_len['class'] = tag_class
            tag_len_check.append(tag_len.copy())
    
    else:
        tag_len['tag'] = f'{text} tags not found'
        tag_len['len'] = '-'
        tag_len['status'] = 'Error'
        tag_len['class'] = 'error'
        tag_len_check.append(tag_len.copy())

    return tag_len_check


def check_avaliabe(tag_name, tag_text):

    tag_avaliable = {}
    
    if tag_name:
        tag_avaliable['text'] = tag_name
        tag_avaliable['status'] = 'Ok'
        tag_avaliable['class'] = 'ok'

    else:
        tag_avaliable['text'] = [f'{tag_text} NOT found on the page']
        tag_avaliable['status'] = 'Error'
        tag_avaliable['class'] = 'error'

    return tag_avaliable


def check_quantity(tag_name, tag_text):

    quantity = {}
    length = len(tag_name)

    if length == 1:
        quantity['text'] = f'We found 1 {tag_text} tag on page'
        quantity['status'] = 'Ok'
        quantity['class'] = 'ok'

    elif length > 1:
        quantity['text'] = f'We found {length} {tag_text} tags on page'
        quantity['status'] = 'Error'
        quantity['class'] = 'error'
    elif length == 0:
        quantity['text'] = f'Keywords not found'
        quantity['status'] = 'Error'
        quantity['class'] = 'error'

    return quantity


class Tags(E_URL):

    def __init__(self, url):
        # self.key = key
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url
        self.title = self.get_tag('title')
        self.description = self.get_meta('description')
        self.keywords = self.get_meta('keywords')
        self.h1 = self.get_tag('h1')
        self.h2 = self.get_tag('h2')
        self.h3 = self.get_tag('h3')
        self.h4 = self.get_tag('h4')
        self.h5 = self.get_tag('h5')
        self.h6 = self.get_tag('h6')
        

    def get_tag(self, tag_name):
        tag_html = self.soup.find_all(tag_name)
        tag = [t.text for t in tag_html]
        return tag


    def get_meta(self, tag_name):
        tag_html = self.soup.find_all('meta', attrs={"name":tag_name})
        tag = [t['content'] for t in tag_html]
        return tag


    def check_title_avaliabe(self):
        self.title_avaliable = check_avaliabe(self.title, 'title')
        return self.title_avaliable


    def check_description_avaliabe(self):
        self.description_avaliable = check_avaliabe(self.description, 'Description')
        return self.description_avaliable


    def check_keywords_avaliabe(self):
        self.keywords_avaliable = check_avaliabe(self.keywords, 'Keywords')
        return self.keywords_avaliable


    def check_h1_avaliable(self):
        self.h1_avaliable = check_avaliabe(self.h1, 'H1')
        return self.h1_avaliable


    def check_title_quantity(self):
        self.title_quantity = check_quantity(self.title, 'Title')
        return self.title_quantity


    def check_description_quantity(self):
        self.description_quantity = check_quantity(self.description, 'Description')
        return self.description_quantity


    def check_keywords_quantity(self):
        self.keywords_quantity = check_quantity(self.keywords, 'Keywords')
        return self.keywords_quantity


    def check_h1_quantity(self):
        self.h1_quantity = check_quantity(self.h1, 'H1')
        return self.h1_quantity


    def check_title_len(self):
        title_len = check_len(self.title, 50, 60, 'Title')
        return title_len

    
    def check_description_len(self):
        description_len = check_len(self.description, 50, 160, 'Description')
        return description_len

    
    def check_keywords_len(self):
        keywords_len = check_len(self.keywords, 100, 250, 'Keywords')
        return keywords_len


    def check_h1_len(self):
        h1_len = check_len(self.h1, 1, 70, 'H1')
        return h1_len


    def check_h2_len(self):
        h2_len = check_len(self.h2, 5, 70, 'H2')
        return h2_len

    
    def check_h3_len(self):
        h3_len = check_len(self.h3, 5, 70, 'H3')
        return h3_len


    def check_h4_len(self):
        h4_len = check_len(self.h4, 5, 70, 'H4')
        return h4_len


    def check_h5_len(self):
        h5_len = check_len(self.h5, 5, 70, 'H5')
        return h5_len


    def check_h6_len(self):
        h6_len = check_len(self.h6, 5, 70, 'H6')
        return h6_len


    def check_title_h1(self):

        self.title_h1 = {}

        if self.title == self.h1:
            self.title_h1['text'] = 'Title and H1 are the same'
            self.title_h1['status'] = 'Ok'
            self.title_h1['class'] = 'ok'
        else:
            self.title_h1['text'] = 'Title and H1 are different'
            self.title_h1['status'] = 'Error'
            self.title_h1['class'] = 'error'

        return self.title_h1


def tags_pars(url):

    lst = []
    lst_status = []
    lst_h = []

    print()
    print('#########################')
    print(url)
    print('#########################')

    start = time.time()

    # url = 'https://www.w3schools.com/tags/tag_hn.asp'
    # url = 'tibrains.com'

    T = Tags(url)

    # Title Avaliable
    title_avaliable = T.check_title_avaliabe()
    print('')
    print('Title: ', title_avaliable['text'])
    print('Title: ', title_avaliable['status'])
    lst_status.append(['Title', title_avaliable])

    # Description Avaliable
    description_avaliable = T.check_description_avaliabe()
    print('')
    print('Description: ', description_avaliable['text'])
    print('Description: ', description_avaliable['status'])
    lst_status.append(['Description', description_avaliable])

    # Keywords Avaliable
    keywords_avaliable = T.check_keywords_avaliabe()
    print('')
    print('Keywords: ', keywords_avaliable['text'])
    print('Keywords: ', keywords_avaliable['status'])
    lst_status.append(['Keywords', keywords_avaliable])

    # Title Quantity
    title_quantity = T.check_title_quantity()
    print('')
    print('Title Quantity: ', title_quantity['text'])
    print('Title Quantity: ', title_quantity['status'])
    lst_status.append(['Title Quantity', title_quantity])

    # Title Length
    title_len = T.check_title_len()[0]
    print()
    print(title_len)
    lst_status.append(['title_len', title_len])
    # for title in title_len:
    #     print(title['title'])
    #     print(title['len'])
    #     print(title['status'])

    # Description Quantity
    desc_quantity = T.check_description_quantity()
    print('')
    print('Description Quantity: ', desc_quantity['text'])
    print('Description Quantity: ', desc_quantity['status'])
    lst_status.append(['Description Quantity', desc_quantity])

    # H1 Avaliable
    h1_avaliable = T.check_h1_avaliable()
    print('')
    print('H1 Avaliable: ', h1_avaliable['text'])
    print('H1 Avaliable: ', h1_avaliable['status'])
    lst_status.append(['H1 Avaliable', h1_avaliable])

    # H1 Quantity
    h1_quantity = T.check_h1_quantity()
    print('')
    print('H1 Quantity: ', h1_quantity['text'])
    print('H1 Quantity: ', h1_quantity['status'])
    lst_status.append(['H1 Quantity', h1_quantity])

    # H1 Length
    h1_len = T.check_h1_len()
    print(h1_len)
    lst_h.append(['h1', h1_len])
    # print('H1 Length: ', h1_len['text'])
    # print('H1 Length: ', h1_len['status'])

    # Title == H1
    title_h1 = T.check_title_h1()
    print('')
    print('Title == H1: ', title_h1['text'])
    print('Title == H1: ', title_h1['status'])
    lst_status.append(['Title == H1', title_h1])

    # # H2 Avaliable
    # h2_avaliable = T.check_h2_avaliable()
    # print('')
    # print('H2 Avaliable: ', h2_avaliable['text'])
    # print('H2 Avaliable: ', h2_avaliable['status'])
    # h2_avaliable

    # H2 Length
    h2_len = T.check_h2_len()
    print(h2_len)
    lst_h.append(['h2', h2_len])

    # H3 Length
    h3_len = T.check_h3_len()
    print(h3_len)
    lst_h.append(['h3', h3_len])

    # H4 Length
    print('============================================================')
    print('H4 Tags:')
    h4_len = T.check_h4_len()
    print(h4_len)
    lst_h.append(['h4', h4_len])

    # H5 Length
    print('============================================================')
    print('H5 Tags:')
    h5_len = T.check_h5_len()
    print(h5_len)
    lst_h.append(['h5', h5_len])

    # H6 Length
    print('============================================================')
    print('H6 Tags:')
    h6_len = T.check_h6_len()
    print(h6_len)
    lst_h.append(['h6', h6_len])

    end = time.time()
    result = end - start
    print('TIME: ', result)
    lst.append(['TIME: ', result])

    return lst, lst_status, lst_h


if __name__ == '__main__':

    sites_list = ['https://www.kinofilms.ua/movie/942584/']
    
    for url in sites_list:

        print()
        print('#########################')
        print(url)
        print('#########################')
            
        start = time.time()

        # url = 'https://www.w3schools.com/tags/tag_hn.asp'
        # url = 'tibrains.com'

        T = Tags(url)

        # Title Avaliable
        title_avaliable = T.check_title_avaliabe()
        print('')
        print('Title: ', title_avaliable['text'])
        print('Title: ', title_avaliable['status'])

        # Description Avaliable
        description_avaliable = T.check_description_avaliabe()
        print('')
        print('Description: ', description_avaliable['text'])
        print('Description: ', description_avaliable['status'])

        # Keywords Avaliable
        keywords_avaliable = T.check_keywords_avaliabe()
        print('')
        print('Keywords: ', keywords_avaliable['text'])
        print('Keywords: ', keywords_avaliable['status'])

        # Title Quantity
        title_quantity = T.check_title_quantity()
        print('')
        print('Title Quantity: ', title_quantity['text'])
        print('Title Quantity: ', title_quantity['status'])

        # Title Length
        title_len = T.check_title_len()[0]
        print()
        print(title_len)
        # for title in title_len:
        #     print(title['title'])
        #     print(title['len'])
        #     print(title['status'])



        # Description Quantity
        desc_quantity = T.check_description_quantity()
        print('')
        print('Description Quantity: ', desc_quantity['text'])
        print('Description Quantity: ', desc_quantity['status'])

        # H1 Avaliable
        h1_avaliable = T.check_h1_avaliable()
        print('')
        print('H1 Avaliable: ', h1_avaliable['text'])
        print('H1 Avaliable: ', h1_avaliable['status'])

        # H1 Quantity
        h1_quantity = T.check_h1_quantity()
        print('')
        print('H1 Quantity: ', h1_quantity['text'])
        print('H1 Quantity: ', h1_quantity['status'])

        # H1 Length
        h1_len = T.check_h1_len()
        print(h1_len)
        # print('H1 Length: ', h1_len['text'])
        # print('H1 Length: ', h1_len['status'])

        # Title == H1
        title_h1 = T.check_title_h1()
        print('')
        print('Title == H1: ', title_h1['text'])
        print('Title == H1: ', title_h1['status'])

        # # H2 Avaliable
        # h2_avaliable = T.check_h2_avaliable()
        # print('')
        # print('H2 Avaliable: ', h2_avaliable['text'])
        # print('H2 Avaliable: ', h2_avaliable['status'])
        # h2_avaliable

        # H2 Length
        h2_len = T.check_h2_len()
        print(h2_len)

        # H3 Length
        h3_len = T.check_h3_len()
        print(h3_len)

        # H4 Length
        print('============================================================')
        print('H4 Tags:')
        h4_len = T.check_h4_len()
        print(h4_len)

        # H5 Length
        print('============================================================')
        print('H5 Tags:')
        h5_len = T.check_h5_len()
        print(h5_len)

        # H6 Length
        print('============================================================')
        print('H6 Tags:')
        h6_len = T.check_h6_len()
        print(h6_len)

        end = time.time()
        result = end-start
        print('TIME: ', result)