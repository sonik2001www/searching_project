import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class BuiltWithParser:
    BASE_URL = 'https://builtwith.com/'
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self, domain: str):
        self.domain = domain.strip()

    def get_page_records(self):
        lst = []
        page = self.session.get(self.BASE_URL + self.domain, headers=self.headers)
        soup = BeautifulSoup(page.content, 'lxml')
        print(soup.select_one('[class="card-body pb-0"] .card-title').text)
        cards = soup.select('[class="card-body pb-0"]')
        for card in cards:
            title = card.select_one('.card-title').text
            # print(title)
            technologies = card.select('.row.mb-2.mt-2')
            technology_list = []
            for item in technologies:
                technology_name = item.select_one('h2 a').text
                sub_list = item.select('.row.mb-2')
                if sub_list:
                    sub_technologies = list(map(lambda x: x.select_one('a').text, item.select('.row.mb-2')))
                    technology_list.append(f'{technology_name}: {", ".join(sub_technologies)}')
                    # lst.append([title, f'{technology_name}: {", ".join(sub_technologies)}'])
                else:
                    technology_list.append(technology_name)
                    # lst.append([title, technology_name])
            # print(technology_list)
            lst.append([title, technology_list])

        print(lst)
        return lst


if __name__ == '__main__':
    parser = BuiltWithParser('4phones.eu')
    parser.get_page_records()


def builtwith_pars(domainname):
    if 'http' in domainname:
        parsed_url = urlparse(domainname)
        domainname = parsed_url.netloc
        print(domainname)
        if 'www' in domainname:
            domainname = domainname[4:]
            print(domainname)
    parser = BuiltWithParser(domainname)
    lst = parser.get_page_records()
    return lst
