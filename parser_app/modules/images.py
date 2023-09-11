import time
import pathlib
import sys
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import urllib.request
from urllib.parse import urlparse

import requests

sys.path.insert(0, '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project')
from parser_app.modules.url import E_URL
from parser_app.modules.files import *


headers={"User-Agent":"Mozilla/5.0"}


def get_url(url, src):

    try:

        if src.startswith('https') or src.startswith('http'):
            image_url = src

        elif src.startswith('/'):
            if url.endswith('/'):
                image_url = url[:-1] + src
            else:
                image_url = url + src
        else:
            image_url = url + src

    except KeyError:
        image_url = None

    return image_url


# def get_pil(images_ht, url):

#         pil_list = []
#         pil = {}

#         for image in images_ht:
            
#             # if img src is empry, use data
#             image_src = image['src']
#             if image_src == '' or image_src == ' ':
#                 image_src = image['data']

#             link = get_url(url, image_src)

#             pil['url'] = link

#             try:
#                 pil['pil'] = Image.open(requests.get(link, stream=True, headers=headers).raw)

#             except Exception as e:
#                 print()
#                 print(link)
#                 print('e')
#                 print("ERROR")

#                 pil['pil'] = 'Image Format Unknown'

#             pil_list.append(pil.copy())
        
#         return pil_list


class TiImages(E_URL): 

    def __init__(self, url):
        E = E_URL(url)
        self.requests = E.get_requests()
        self.source = self.requests.text
        self.soup = E.get_soup()
        self.url = self.requests.url
        self.images = self.soup.find_all('img')
    

    # def get_empty_src(self):

    #     empty = {}
    #     empty_list = []

    #     for im in self.images:
            
    #         try:
    #         im_src = im['src']

    #         empty['ht'] = im
    #         empty['src'] = im_src

    #         if im_src == None or im_src == '' or im_src == ' ':
                
    #             empty['status'] = 'Error'
    #             empty['text'] = 'Image src attr is empty'

    #         else:
                
    #             empty['status'] = 'Ok'
    #             empty['text'] = 'Image has src link'

    #         empty_list.append(empty.copy())

    #     return empty_list
    
    def get_url(self, src):

        url_parse = urlparse(self.url)
        scheme = url_parse.scheme
        netloc = url_parse.netloc
        url = f'{scheme}://{netloc}/'

        if src.startswith('https') or src.startswith('http'):
            image_url = src

        elif src.startswith('/'):
            if url.endswith('/'):
                image_url = url[:-1] + src
            else:
                image_url = url + src
        else:
            image_url = url + src

        return image_url

    
    def get_images_list(self):

        image = {}
        self.images_list = []

        images_ht = self.soup.find_all('img')

        for im in images_ht:

            image['ht'] = im

            # Get image src
            try:
                image['src'] = im['src']
            except KeyError:
                image['src'] = None

            # Get image data
            try:
                image['data'] = im['data']
            except KeyError:
                image['data'] = None

            self.images_list.append(image.copy())

        return self.images_list

    
    def get_empty_src(self):

        empty = {}
        empty_list = []

        for im in self.images_list:

            empty['ht'] = str(im['ht'])
            empty['src'] = im['src']

            if im['src'] == None or im['src'] == '' or im['src'] == ' ':

                empty['status'] = 'Error'
                empty['class'] = 'error'
                empty['text'] = 'Image src is not set or is empty'

            else:

                empty['status'] = 'Ok'
                empty['class'] = 'ok'
                empty['text'] = 'Image src is set'

            empty_list.append(empty.copy())

        return empty_list

      
    def check_src(self, src):

        if src == None or src == '' or src == ' ':
            source = None
        
        elif 'data:image' in  src:
            source = None

        else:
            source = self.get_url(src)
        
        return source

    
    def check_data_src(self, data_src):

        if data_src == None or data_src == '' or data_src == ' ':
            source = None
        
        elif 'data:image' in  data_src:
            source = None

        else:
            source = self.get_url(data_src)

        return source

    
    def get_src_list(self):
        
        self.src_list = []

        for im in self.images_list:

            src = self.check_src(im['src'])
            if src != None and src not in self.src_list:
                self.src_list.append(src)

            data_src = self.check_data_src(im['data'])
            if data_src != None and data_src not in self.src_list:
                self.src_list.append(data_src)

        return self.src_list


    def get_pil(self):

        self.pil_list = []
        pil = {}

        src_list = self.get_src_list()

        for src in src_list:

            pil['src'] = src

            r = requests.get(src, headers=headers)
            if r.status_code == 200:

                try:
                    i = Image.open(BytesIO(r.content))
                    pil['format'] = i.format
                    pil['dim'] = i.size

                except UnidentifiedImageError:
                    
                    if src.endswith('.svg'):
                        pil['format'] = 'SVG'
                        pil['dim'] = None

                    else:
                        pil['format'] = 'Unknown'
                        pil['dim'] = 'Unknown'
            
            self.pil_list.append(pil.copy())

        return self.pil_list


    def check_alt(self):
        
        alt_list = []
        alt = {}
        
        for im in self.images:

            alt['url'] = str(im)

            try:
                alt['alt'] = im['alt']  

                if alt['alt'] != None and alt['alt'] != '' and alt['alt'] != ' ':
                        alt['status'] = 'Ok'
                        alt['class'] = 'ok'

                else:
                    alt['status'] = 'Error'
                    alt['class'] = 'error'

            except KeyError:
                alt['alt'] = ''
                alt['status'] = 'Error'
                alt['class'] = 'error'

            alt_list.append(alt.copy())
        
        return alt_list


    def check_title(self):
        
        title_list = []
        title = {}
        
        for im in self.images:

            title['url'] = str(im)

            try:
                title['title'] = im['title']
                print('TITLE: ', title['title'])  

                if title['title'] != None and title['title'] != '' and title['title'] != ' ':
                        title['status'] = 'Ok'
                        title['class'] = 'ok'
                        

                else:
                    title['status'] = 'Error'
                    title['class'] = 'error'

            except KeyError:
                title['title'] = None
                title['status'] = 'Error'
                title['class'] = 'error'

            title_list.append(title.copy())
        
        return title_list


    def check_format(self):

        format = {}
        format_list = []

        for im in self.pil_list:

            format['src'] = im['src']

            format['format'] = im['format']
            if format['format'] == 'WEBP' or format['format'] == 'AVIF':
                format['status'] = 'Ok'
                format['class'] = 'ok'
            else:
                format['status'] = 'Error'
                format['class'] = 'error'

            format_list.append(format.copy())

        return format_list


    def check_dimensions(self):

        dim = {}
        dim_list = []

        for im in self.pil_list:

            dim['src'] = im['src']

            print(im['dim'])

            if im['dim'] == None:     
                print('COOL')    
                dim['dim'] = im['dim']
                dim['status'] = 'Error'
                dim['class'] = 'error'

            
            else:
                width = im['dim'][0]
                height = im['dim'][0]

                dim['dim'] = f'{width} X {height}'

                if width <= 1080 and height <= 1080:

                    dim['status'] = 'Ok'
                    dim['class'] = 'Ok'

                else:

                    dim['status'] = 'Error'
                    dim['class'] = 'error'

            dim_list.append(dim.copy())

        return dim_list


def images_pars(url):
    images_lst = []
    empty_lst = []
    src_lst = []
    pil_lst = []
    alt_lst = []
    title_lst = []
    format_lst = []
    dim_lst = []

    TiIm = TiImages(url)

    images = TiIm.get_images_list()
    for im in images:
        # print()
        # print(im['ht'])
        im['ht'] = str(im['ht'])
        # print(im['src'])
        # print(im['data'])
        images_lst.append(["Images", im])

    empty_src = TiIm.get_empty_src()
    for empty in empty_src:
        # print()
        # print(empty['ht'])
        # print(empty['src'])
        # print(empty['status'])
        # print(empty['text'])
        empty_lst.append(["Empty src", empty])

    src_list = TiIm.get_src_list()
    for src in src_list:
        # print(src)
        src_lst.append(["List src", src])

    pil = TiIm.get_pil()
    # print(pil)
    for p in pil:
        pil_lst.append(["Pil", p])

    alt = TiIm.check_alt()
    # print(alt)
    for a in alt:
        alt_lst.append(a)

    title = TiIm.check_title()
    # print(title)
    for t in title:
        title_lst.append(t)

    format = TiIm.check_format()
    for f in format:
        # print()
        # print(f['src'])
        # print(f['format'])
        # print(f['status'])
        format_lst.append(f)

    dim = TiIm.check_dimensions()
    print(dim)
    for d in dim:
        dim_lst.append(d)

    return images_lst, empty_lst, src_lst, pil_lst, alt_lst, title_lst, format_lst, dim_lst


if __name__ == '__main__':

    url = 'https://www.liga.net/'

    TiIm = TiImages(url)

    images = TiIm.get_images_list()
    for im in images:
        print()
        print('ht', im['ht'])
        print('src', im['src'])
        print('data', im['data'])


        
    # empty_src = TiIm.get_empty_src()
    # for empty in empty_src:
    #     print()
    #     print(empty['ht'])
    #     print(empty['src'])
    #     print(empty['status'])
    #     print(empty['text'])
    #
    # # pil_info = TiIm.get_pil()
    #
    # # src = TiIm.check_src()
    # # data_src = TiIm.check_data_src()
    #
    # src_list = TiIm.get_src_list()
    # for src in src_list:
    #     print(src)
    #
    # pil = TiIm.get_pil()
    # print(pil)
    #
    # alt = TiIm.check_alt()
    # print(alt)
    #
    # title = TiIm.check_title()
    # print(title)
    #
    # format = TiIm.check_format()
    # for f in format:
    #     print()
    #     print(f['src'])
    #     print(f['format'])
    #     print(f['status'])
    #
    # dim = TiIm.check_dimensions()
    # print(dim)
    #
    # print()
    # print(images[0])
    # print(empty_src[0])
    # print(src_list[0])


# if __name__ == '__main__':
#
#     url = 'liga.net'
#
#     TiIm = TiImages(url)
#     images = TiIm.get_images_list()
#
#     for im in TiIm.images:
#         print()
#         print(im)
#
#     alt = TiIm.check_alt()
#     title = TiIm.check_title()
#     for t in title:
#         print()
#         print(t['url'])
#         print(t['title'])
#         print(t['status'])
#
#     empty_src = TiIm.get_empty_src()
#     for e in empty_src:
#         print(e)
#
#     pil = TiIm.get_pil()
#     format = TiIm.check_format()
#     for f in format:
#         print()
#         print(f)
#
#     dim = TiIm.check_dimensions()
#     for d in dim:
#         print()
#         print(d)
