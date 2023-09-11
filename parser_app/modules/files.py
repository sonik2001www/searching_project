import requests
import os
import time
import urllib.request
import random
from PIL import Image
from io import BytesIO


def save_file(url, path):
    print("ok ups")
    print(url)
    print(path)
    content = requests.get(url).text
    file = open(path, "w")
    file.write(content)
    file.close()


def save_image(url):
    path = '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project/parser_app/modules/test.png'
    import urllib.request
    urllib.request.urlretrieve(url, path)


def save_image_pil(url, path):
    r = requests.get(url)
    im = Image.open(BytesIO(r.content))
    print(im.format)
    im.save(path)


def save_image(url, path):
    content = requests.get(url).text
    file = open(path, "w")
    file.write(content)
    file.close


def get_file_size(path):
    size = os.path.getsize(path)
    os.remove(path)
    return size


def to_webp():
    pass


url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Kim_Weston.png/220px-Kim_Weston.png'
path = '/Users/applebuy/PycharmProjects/projects1/search_link/search_link_project/parser_app/modules/test.png'

urllib.request.urlretrieve(url, path)
