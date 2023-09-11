import sys
import time
import re


sys.path.insert(0, '/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


def check_social(soup):
    
    results = {}

    html = soup.find('div', class_='fb-like')

    # if value in source:
    #     results['text'] = (f'{text}')
    #     results['status'] = 'Ok'
    # else:
    #     results['text'] = (f'{text}')
    #     results['status'] = 'Error'

    return html

class Social(E_URL):

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url

    def check_social(self, pattern):
        
        social = {}

        social_raw = re.finditer(pattern, self.source)
        list = [s.group() for s in social_raw]

        # removes duplicates
        social['list'] = set(list)
        if len(social['list'] ) == 0:
            social['status'] = 'Error'
        else:
            social['status'] = 'Ok'

        return social

    def check_fb(self):
        self.facebook_pattern = 'facebook.com/[-._a-zA-Z0-9]*'
        return self.check_social(self.facebook_pattern)

    def check_instagram(self):
        self.instagram_pattern = 'instagram.com/[-._a-zA-Z0-9]*'
        return self.check_social(self.instagram_pattern)

    def check_pinterest(self):
        self.pinterest_pattern = "pinterest.ru/[-._a-zA-Z0-9]*"
        return self.check_social(self.pinterest_pattern)

    def check_youtube(self):
        self.youtube_pattern = "youtube.com/[-._a-zA-Z0-9/]*"
        return self.check_social(self.youtube_pattern)

    def check_twitter(self):
        self.twitter_pattern = "twitter.com/[-._a-zA-Z0-9/]*"
        return self.check_social(self.twitter_pattern)

    def check_vk(self):
        self.vk_pattern = "(vkontakte|vk).(ru|com)/[-._a-zA-Z0-9/]*"
        return self.check_social(self.vk_pattern)
    
    def check_ok(self):
        self.ok_pattern = "ok.ru/[-._a-zA-Z0-9/]*"
        return self.check_social(self.ok_pattern)
    
    def check_linkedin(self):
        linkedin_pattern = "linkedin.com/[-._a-zA-Z0-9/]*"
        return self.check_social(linkedin_pattern)

    def check_telegram(self):
        self.telegram_pattern = "t.me/[-._a-zA-Z0-9/]*"
        return self.check_social(self.telegram_pattern)

    def check_viber(self):
        self.viber_pattern = "chats.viber.com/[-._a-zA-Z0-9/]*"
        return self.check_social(self.viber_pattern)

    def check_fb_like(self):
        
        results = {}

        html = self.soup.find(class_='fb-like')

        if html:
            if html['data-action'] == 'like':
                results['text'] = ('Facebook Like Button found')
                results['status'] = 'Ok'
                results['class'] = 'ok'
            else:
                results['text'] = ('Facebook Like Button NOT found')
                results['status'] = 'Error'
                results['class'] = 'error'
        else:
                results['text'] = ('Facebook Like Button NOT found')
                results['status'] = 'Error'
                results['class'] = 'error'

        return results

    def check_fb_recommend(self):
        
        results = {}

        html = self.soup.find(class_='fb-like')

        if html:

            if html['data-action'] == 'recommend':
                results['text'] = ('Facebook Recommend Button found')
                results['status'] = 'Ok'
                results['class'] = 'ok'
            else:
                results['text'] = ('Facebook Recommend Button NOT found')
                results['status'] = 'Error'
                results['class'] = 'error'

        else:
            results['text'] = ('Facebook Recommend Button NOT found')
            results['status'] = 'Error'
            results['class'] = 'error'

        return results

    def check_fb_share(self):
        
        results = {}

        html = self.soup.find(class_='fb-share-button')

        if html:
            results['text'] = ('Facebook Share Button found')
            results['status'] = 'Ok'
            results['class'] = 'ok'
        else:
            results['text'] = ('Facebook Share Button NOT found')
            results['status'] = 'Error'
            results['class'] = 'error'

        return results

    def check_fb_comments(self):
        
        results = {}

        html = self.soup.find(class_='fb-comments')

        if html:
            results['text'] = ('Facebook Comments found')
            results['status'] = 'Ok'
            results['class'] = 'ok'
        else:
            results['text'] = ('Facebook Comments NOT found')
            results['status'] = 'Error'
            results['class'] = 'error'

        return results
  
    def twitter_share(self):
        
        results = {}

        html = self.soup.find(class_='twitter-share-button')

        if html:
            results['text'] = ('Twitter Share Button found')
            results['status'] = 'Ok'
            results['class'] = 'ok'
        else:
            results['text'] = ('Twitter Share Button NOT found')
            results['status'] = 'Error'
            results['class'] = 'error'

        return results
    
    def pin_save_button(self):
        
        results = {}

        pattern = "data-pin-do.?=.?(\"|')buttonBookmark(\"|')"
        save_button = re.search(pattern, self.source)

        if save_button:
            results['text'] = ('Twitter Share Button found')
            results['status'] = 'Ok'
            results['class'] = 'ok'
        else:
            results['text'] = ('Twitter Share Button found')
            results['status'] = 'Error'
            results['class'] = 'error'

        return results


def social_pars(url):

    lst = []
    lst_status = []

    print()
    print('#########################')
    print(url)
    print('#########################')

    start = time.time()

    S = Social(url)

    fb = S.check_fb()
    print('Facebook: ', fb)
    lst_status.append(['Facebook: ', fb])

    vk = S.check_vk()
    print('VK: ', vk)
    lst_status.append(['VK: ', vk])

    ok = S.check_ok()
    print('OK: ', ok)
    lst_status.append(['OK: ', ok])

    instagram = S.check_instagram()
    print('Instagram: ', instagram)
    lst_status.append(['Instagram: ', instagram])

    youtube = S.check_youtube()
    print('Youtube: ', youtube)
    lst_status.append(['Youtube: ', youtube])

    twitter = S.check_twitter()
    print('Twitter: ', twitter)
    lst_status.append(['Twitter: ', twitter])

    linkedin = S.check_linkedin()
    print('Linkedin: ', linkedin)
    lst_status.append(['Linkedin: ', linkedin])

    telegram = S.check_telegram()
    print('Telegram: ', telegram)
    lst_status.append(['Telegram: ', telegram])

    viber = S.check_viber()
    print('Viber: ', viber)
    lst_status.append(['Viber: ', viber])

    pinterest = S.check_pinterest()
    print('Pinterest: ', pinterest)
    lst_status.append(['Pinterest: ', pinterest])

    fb_like = S.check_fb_like()
    print(fb_like)
    lst_status.append(['fb_like: ', fb_like])

    fb_share = S.check_fb_share()
    print(fb_share)
    lst_status.append(['fb_share: ', fb_share])

    fb_recommend = S.check_fb_recommend()
    print(fb_recommend)
    lst_status.append(['fb_recommend: ', fb_recommend])

    fb_comments = S.check_fb_comments()
    print(fb_comments)
    lst_status.append(['fb_comments: ', fb_comments])

    twitter_share = S.twitter_share()
    print(twitter_share)
    lst_status.append(['twitter_share: ', twitter_share])

    end = time.time()
    result = end - start
    print('TIME: ', result)
    lst.append(['TIME: ', result])

    return lst, lst_status


if __name__ == '__main__':

    sites_list = ['https://www.kinofilms.ua/movie/942584/']
    
    for url in sites_list:

        print()
        print('#########################')
        print(url)
        print('#########################')

        start = time.time()

        S = Social(url)

        fb = S.check_fb()
        print('Facebook: ', fb)

        vk = S.check_vk()
        print('VK: ', vk)

        ok = S.check_ok()
        print('OK: ', ok)

        instagram = S.check_instagram()
        print('Instagram: ', instagram)

        youtube = S.check_youtube()
        print('Youtube: ', youtube)

        twitter = S.check_twitter()
        print('Twitter: ', twitter)

        linkedin = S.check_linkedin()
        print('Linkedin: ', linkedin)

        telegram = S.check_telegram()
        print('Telegram: ', telegram)

        viber = S.check_viber()
        print('Viber: ', viber)

        pinterest = S.check_pinterest()
        print('Pinterest: ', pinterest)

        fb_like = S.check_fb_like()
        print(fb_like)

        fb_share = S.check_fb_share()
        print(fb_share)

        fb_recommend = S.check_fb_recommend()
        print(fb_recommend)

        fb_comments = S.check_fb_comments()
        print(fb_comments)

        twitter_share = S.twitter_share()
        print(twitter_share)

        end = time.time()
        result = end-start
        print('TIME: ', result)
