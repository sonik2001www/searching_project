import requests
from bs4 import BeautifulSoup

from .seo_test.fast_check import fast_check_all
from .seo_test.caching_test import caching_test
from .seo_test.nested_tables_test import nested_tables_test
from .seo_test.adstxt_validation_test import adstxt_validation_test

from parser_app.modules.url import E_URL


class BuiltWithParser:
    BASE_URL = 'https://builtwith.com/'
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self, domain: str):
        self.domain = domain.strip()

    def get_page_records(self):
        page = self.session.get(self.BASE_URL + self.domain, headers=self.headers)
        soup = BeautifulSoup(page.content, 'lxml')
        cards = soup.select('[class="card-body pb-0"]')

        output_list = []
        for card in cards:
            title = card.select_one('.card-title').text
            # print(title)
            technologies = card.select('.row.mb-1.mt-1')
            technology_list = []
            for item in technologies:
                technology_name = item.select_one('h2 a').text
                sub_list = item.select('.row.mb-1')
                if sub_list:
                    sub_technologies = list(map(lambda x: x.select_one('a').text, item.select('.row.mb-1')))
                    sub_technologies_str = ''
                    for i in sub_technologies:
                        sub_technologies_str += i

                    technology_list.append(f"{technology_name}: {sub_technologies_str}")
                else:
                    technology_list.append(technology_name)
            print([title, technology_list])
            output_list.append([title, technology_list])

        return output_list


class Mobile(E_URL):

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        # self.domain = E.requests.domain
        self.url = self.requests.url
        self.domain = self.extract_domain(self.requests.url)

    def extract_domain(self, url):
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        return parsed_url.netloc


def builtwith_pars(link):

    E = Mobile(link)
    link = E.url
    domain = E.domain

    print(link, domain)

    # add domain not link
    parser = BuiltWithParser(domain)
    lst = parser.get_page_records()

    fast_check_list = fast_check_all(link)

    caching_test_list = caching_test(link)

    nested_tables_list = nested_tables_test(link)

    adstxt_list = adstxt_validation_test(link)

    return lst, fast_check_list, caching_test_list, nested_tables_list, adstxt_list


if __name__ == '__main__':

    url = 'https://rozetka.com.ua/ua/search/?seller=rozetka&text=iPhone+14+Pro+Max'

    E = E_URL(url)
    url = E.requests.url

    print(url)

    # parser = BuiltWithParser('rezka.ag')
    # print(parser.get_page_records())
    #
    #
    # link = "https://rozetka.com.ua/ua/search/?seller=rozetka&text=iPhone+14+Pro+Max"
    #
    # fast_check_list = fast_check_all(link)
    #
    # caching_test_list = caching_test(link)
    #
    # nested_tables_list = nested_tables_test(link)
    #
    # adstxt_list = adstxt_validation_test(link)
