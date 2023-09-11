from .views import *
from django.urls import path

urlpatterns = [
    path('search_link/', search_link, name='search_link'),
    path('get_pagespeed_info/', get_pagespeed_info, name='get_pagespeed_info'),
    path('text_analiz/', text_analiz, name='text_analiz'),
    path('general/', general, name='general'),
    path('micro/', micro, name='micro'),
    path('whois/', whois, name='whois'),
    path('html_validate/', html_validate, name='html_validate'),
    path('robots/', robots, name='robots'),
    path('sitemap/', sitemap, name='sitemap'),
    path('canonical/', canonical, name='canonical'),
    path('images/', images, name='images'),
    path('index/', index, name='index'),
    path('main/', main, name='main'),
    path('mobile/', mobile, name='mobile'),
    path('redirects/', redirects, name='redirects'),
    path('social/', social, name='social'),
    path('tags/', tags, name='tags'),
    path('responsive_page/', responsive_page, name='responsive_page'),
    path('builtwith/', builtwith, name='builtwith'),
    path('keyword/', keyword, name='keyword'),
]
