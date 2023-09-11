import sys
import time
import re


sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


def check_mformat(tag, soup):
    mformat = {}

    result = soup.find('meta', attrs={"property":tag})

    mformat['tag'] = tag

    if result :
        mformat['text'] = result['content']
        mformat['status'] = 'Ok'
    else:
        mformat['text'] = f'{tag} NOT found on page'
        mformat['status'] = 'Error'
    return mformat

def check_twitter(tag, soup):
    mformat = {}

    result = soup.find('meta', attrs={"name":tag})

    mformat['tag'] = tag

    if result :
        mformat['text'] = result['content']
        mformat['status'] = 'Ok'
    else:
        mformat['text'] = 'Non found on page'
        mformat['status'] = 'Error'
    return mformat


class MicroFormats(E_URL):

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url

    # Open Graph
    def check_og_title(self):
        og_title = check_mformat('og:title', self.soup)
        return og_title

    def check_og_type(self):
        og_type = check_mformat('og:type', self.soup)
        return og_type

    def check_og_image(self):
        og_image = check_mformat('og:image', self.soup)
        return og_image

    def check_og_url(self):
        og_url = check_mformat('og:url', self.soup)
        return og_url

    def check_og_audio(self):
        og_audio = check_mformat('og:audio', self.soup)
        return og_audio

    def check_og_description(self):
        og_description = check_mformat('og:description', self.soup)
        return og_description

    def check_og_determiner(self):
        og_determiner = check_mformat('og:determiner', self.soup)
        return og_determiner

    def check_og_locale(self):
        og_locale = check_mformat('og:locale', self.soup)
        return og_locale

    def check_og_site_name(self):
        og_site_name = check_mformat('og:site_name', self.soup)
        return og_site_name

    def check_og_video(self):
        og_video = check_mformat('og:video', self.soup)
        return og_video


    def check_twitter_card(self):
        twitter_card = check_twitter('twitter:card', self.soup)
        return twitter_card

    
    def check_twitter_site(self):
        twitter_site = check_twitter('twitter:site', self.soup)
        return twitter_site


    def check_twitter_creator(self):
        twitter_creator = check_twitter('twitter:creator', self.soup)
        return twitter_creator

    
    def check_twitter_description(self):
        twitter_description = check_twitter('twitter:description', self.soup)
        return twitter_description


    def check_twitter_title(self):
        twitter_title = check_twitter('twitter:title', self.soup)
        return twitter_title


    def check_twitter_image(self):
        twitter_image = check_twitter('twitter:image', self.soup)
        return twitter_image


    def check_twitter_player(self):
        twitter_player = check_twitter('twitter:player', self.soup)
        return twitter_player


    def check_twitter_app(self):
        twitter_app = check_twitter('twitter:app', self.soup)
        return twitter_app


def micro_pars(link):

    lst = []

    print()
    print('#########################')
    print(link)
    print('#########################')

    MF = MicroFormats(link)

    # Title
    og_title = MF.check_og_title()
    print(og_title)
    lst.append(og_title)

    # Type
    og_type = MF.check_og_type()
    print(og_type)
    lst.append(og_type)

    # Image
    og_image = MF.check_og_image()
    print(og_image)
    lst.append(og_image)

    # URL
    og_url = MF.check_og_url()
    print(og_url)
    lst.append(og_url)

    # Audio
    og_audio = MF.check_og_audio()
    print(og_audio)
    lst.append(og_audio)

    # Description
    og_description = MF.check_og_description()
    print(og_description)
    lst.append(og_description)

    # Determiner
    og_determiner = MF.check_og_determiner()
    print(og_determiner)
    lst.append(og_determiner)

    # Locale
    og_locale = MF.check_og_locale()
    print(og_locale)
    lst.append(og_locale)

    # Site Name
    og_site_name = MF.check_og_site_name()
    print(og_site_name)
    lst.append(og_site_name)

    # Video
    og_video = MF.check_og_video()
    print(og_video)
    lst.append(og_video)

    # Twitter Card
    twitter_card = MF.check_twitter_card()
    print(twitter_card)
    lst.append(twitter_card)

    # Twitter Site
    twitter_site = MF.check_twitter_site()
    print(twitter_site)
    lst.append(twitter_site)

    # Twitter Creator
    twitter_creator = MF.check_twitter_creator()
    print(twitter_creator)
    lst.append(twitter_creator)

    # Twitter Description
    twitter_description = MF.check_twitter_description()
    print(twitter_description)
    lst.append(twitter_description)

    # Twitter Title
    twitter_title = MF.check_twitter_title()
    print(twitter_title)
    lst.append(twitter_title)

    # Twitter Image
    twitter_image = MF.check_twitter_image()
    print(twitter_image)
    lst.append(twitter_image)

    # Twitter Player
    twitter_player = MF.check_twitter_player()
    print(twitter_player)
    lst.append(twitter_player)

    # Twitter App
    twitter_app = MF.check_twitter_app()
    print(twitter_app)
    lst.append(twitter_app)

    return lst


if __name__ == '__main__':

    sites_list = ['https://www.kinofilms.ua/movie/942584/']
    
    for url in sites_list:

        print()
        print('#########################')
        print(url)
        print('#########################')

        start = time.time()

        MF = MicroFormats(url)

        # Title
        og_title = MF.check_og_title()
        print(og_title)

        # Type
        og_type = MF.check_og_type()
        print(og_type)

        # Image
        og_image = MF.check_og_image()
        print(og_image)

        # URL
        og_url = MF.check_og_url()
        print(og_url)

        # Audio
        og_audio = MF.check_og_audio()
        print(og_audio)

        # Description
        og_description = MF.check_og_description()
        print(og_description)

        # Determiner
        og_determiner = MF.check_og_determiner()
        print(og_determiner)

        # Locale
        og_locale = MF.check_og_locale()
        print(og_locale)

        # Site Name
        og_site_name = MF.check_og_site_name()
        print(og_site_name)

        # Video
        og_video = MF.check_og_video()
        print(og_video)

        # Twitter Card
        twitter_card = MF.check_twitter_card()
        print(twitter_card)

        # Twitter Site
        twitter_site = MF.check_twitter_site()
        print(twitter_site)

        # Twitter Creator
        twitter_creator = MF.check_twitter_creator()
        print(twitter_creator)

        # Twitter Description
        twitter_description = MF.check_twitter_description()
        print(twitter_description)

        # Twitter Title
        twitter_title = MF.check_twitter_title()
        print(twitter_title)

        # Twitter Image
        twitter_image = MF.check_twitter_image()
        print(twitter_image)

        # Twitter Player
        twitter_player = MF.check_twitter_player()
        print(twitter_player)

        # Twitter App
        twitter_app = MF.check_twitter_app()
        print(twitter_app)

