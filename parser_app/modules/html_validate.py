import sys
import time
import json
import requests


sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


class HtmlValidate(E_URL):

    def __init__(self, url):

        BaseURL = E_URL(url)
        url = f'https://validator.nu/?doc={BaseURL.url}'
        
        E = E_URL(url)
        
        self.requests = E.get_requests()
        print(self.requests.status_code)
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url


    def get_html_errors(self):

        error = {}
        errors_list = []

        example_er = errors = self.soup.find('li')
        print(example_er)

        errors = self.soup.find_all('li')
        

        for er in errors:
            error['type'] = er.find('p').find('strong').text
            error['message'] = er.find('p').find('span').text
            try:
                error['extract'] = er.find('p', class_='extract').text
            except AttributeError:
                error['extract'] = None

            if error['type'] == 'Warning':
                error['class'] = 'warning'
            elif error['type'] == 'Error':
                error['class'] = 'error'

            try:
                error['loc_from_1_line'] = er.find('span', class_='first-line').text
            except:
                error['loc_from_1_line'] = None

            try:
                error['loc_from_1_col'] = er.find('span', class_='first-col').text
            except:
                error['loc_from_1_col'] = None

            try:
                error['loc_to_last_line'] = er.find('span', class_='last-line').text
            except:
                error['loc_to_last_line'] = None

            try:
                error['loc_to_last_col'] = er.find('span', class_='last-col').text
            except:
                error['loc_to_last_col'] = None

            errors_list.append(error.copy())

        return errors_list


def html_validate_pars(link):
    print()
    print('#########################')
    print(link)
    print('#########################')

    HV = HtmlValidate(link)

    errors = HV.get_html_errors()
    print(errors)

    return errors


if __name__ == '__main__':
    
    sites_list = ['https://mastersofuniverse.net/']
    
    for url in sites_list:

        print()
        print('#########################')
        print(url)
        print('#########################')

        HV = HtmlValidate(url)

        errors = HV.get_html_errors()
        print(errors)

        for error in errors:
            # print(error)
            print('Error Typye: ', error['type'])
            print('Message: ', error['message'])
            print('Extract: ', error['extract'])
            print('From 1 line: ', error['loc_from_1_line'])
            print('From 1 col: ', error['loc_from_1_col'])
            print('To last line: ', error['loc_to_last_line'])
            print('To last col: ', error['loc_to_last_col'])

        

