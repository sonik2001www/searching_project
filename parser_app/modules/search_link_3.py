import re
import time

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse


def format_size(size_bytes):
    if size_bytes >= 1024 * 1024:
        return "{:.2f} MB".format(size_bytes / (1024 * 1024))
    elif size_bytes >= 1024:
        return "{:.2f} KB".format(size_bytes / 1024)
    else:
        return "{:.2f} bytes".format(size_bytes)


def get_file_size(url):
    try:
        response = requests.get(url)
        file_size_bytes = len(response.content)
        formatted_size = format_size(file_size_bytes)
        return formatted_size
    except requests.exceptions.RequestException:
        return None


def is_valid_image_url(url):
    # Check if the URL is a data URI or not
    return not url.startswith('data:image/')


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def search_links(link):

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    html_str = str(soup)
    url_pattern = r'https?://\S+?["\']'

    found_links = re.findall(url_pattern, html_str)

    print(len(found_links))
    print(found_links)

    base_url = get_base_url(link)
    domain = urlparse(base_url).netloc
    print(domain)

    all_links = []
    internal_links = []
    external_links = []
    css_links = []
    js_links = []
    image_links = []
    video_links = []
    file_links = []

    http_https_pattern = re.compile(r'^https?://')
    soup = BeautifulSoup(response.text, 'lxml')

    for link in found_links:
        print(link)
        if '.css' in link:
            css_links.append(link)
        elif '.js' in link:
            js_links.append(link)
        elif '.mp4' in link or '.avi' in link or '.mov' in link:
            video_links.append(link)
        elif '.jpg' in link or '.jpeg' in link or '.png' in link or '.gif' in link or '.bmp' in link or '.tiff' in link or '.raw' in link or '.webp' in link or '.heic' in link or '.svg' in link:
            image_links.append(link)
        elif '.pdf' in link or '.docx' in link or '.xlsx' in link or '.pptx' in link or '.zip' in link or '.rar' in link or '.mp3' in link:
            file_links.append(link)
        elif domain in link:
            internal_links.append(link)
        else:
            external_links.append(link)

    # Знаходимо всі посилання на сторінці
    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']

        if http_https_pattern.match(url):
            all_links.append(url)
        else:
            abs_url = urljoin(link, url)
            all_links.append(abs_url)

    all_links = list(set(all_links))

    try:
        # Знаходимо всі CSS посилання на сторінці
        for link_tag in soup.find_all('link', href=True):
            url = link_tag['href']
            link_type = link_tag.get('type', '')

            if link_type == 'text/css' or '.css' in url:  # Перевіряємо тип або розширення файлу
                if http_https_pattern.match(url):
                    css_links.append(url)
                else:
                    abs_url = urljoin(base_url, url)  # Використовуємо base_url для створення абсолютного URL
                    css_links.append(abs_url)
    except:
        pass

    try:
        # Знаходимо всі JS посилання на сторінці
        for script_tag in soup.find_all('script', src=True):
            url = script_tag['src']

            if http_https_pattern.match(url):
                js_links.append(url)
            else:
                abs_url = urljoin(base_url, url)  # Використовуємо base_url для створення абсолютного URL
                js_links.append(abs_url)
    except:
        pass

    try:
        # Знаходимо всі посилання на зображення (фото) на сторінці
        for img_tag in soup.find_all('img', src=True):
            url = img_tag['src']

            if http_https_pattern.match(url) and is_valid_image_url(url):
                image_links.append(url)
            else:
                abs_url = urljoin(base_url, url)
                if is_valid_image_url(abs_url):
                    image_links.append(abs_url)
    except:
        pass

    try:
        # Знаходимо всі посилання на відео на сторінці
        for video_tag in soup.find_all('video', src=True):
            url = video_tag['src']

            if http_https_pattern.match(url):
                video_links.append(url)
            else:
                abs_url = urljoin(base_url, url)
                video_links.append(abs_url)
    except:
        pass

    try:
        # Знаходимо всі посилання на файли на сторінці (необхідна валідація файлових посилань)
        for file_tag in soup.find_all(['a', 'link', 'script'], href=True):
            url = file_tag['href']
            # You can add more file extensions to this regex pattern for different types of files
            if re.search(r'\.(pdf|docx?|xlsx?|pptx?|zip|rar|csv|txt|rtf|odt|ods|odp|epub|mp3|mp4|wav|avi|mov|flv|wmv)$', url, re.IGNORECASE):
                if http_https_pattern.match(url):
                    file_links.append(url)
                else:
                    abs_url = urljoin(base_url, url)
                    file_links.append(abs_url)
    except:
        pass

    # Separate internal and external links
    for link in all_links:
        if domain in link:
            internal_links.append(link)
        else:
            external_links.append(link)

    css_links = list(set(css_links))
    js_links = list(set(js_links))
    image_links = list(set(image_links))
    video_links = list(set(video_links))
    file_links = list(set(file_links))

    css_links = [link[:-1] if link[-1] == '"' else link for link in css_links]
    js_links = [link[:-1] if link[-1] == '"' else link for link in js_links]
    image_links = [link[:-1] if link[-1] == '"' else link for link in image_links]
    video_links = [link[:-1] if link[-1] == '"' else link for link in video_links]
    file_links = [link[:-1] if link[-1] == '"' else link for link in file_links]
    internal_links = [link[:-1] if link[-1] == '"' else link for link in internal_links]
    external_links = [link[:-1] if link[-1] == '"' else link for link in external_links]

    print("CSS Links:")
    print(css_links)

    print("\nJS Links:")
    print(js_links)

    print("\nImage Links:")
    print(image_links)

    print("\nInternal Links:")
    print(internal_links)

    print("\nExternal Links:")
    print(external_links)

    print("\nVideo Links:")
    print(video_links)

    print("\nFile Links:")
    print(file_links)

    css_links = [[link, get_file_size(link)] for link in css_links]
    print('Done - css_links')
    js_links = [[link, get_file_size(link)] for link in js_links]
    print('Done - js_links')
    image_links = [[link, get_file_size(link)] for link in image_links]
    print('Done - image_links')
    video_links = [[link, get_file_size(link)] for link in video_links]
    print('Done - video_links')
    file_links = [[link, get_file_size(link)] for link in file_links]
    print('Done - file_links')
    internal_links = [[link, "-"] for link in internal_links]
    print('Done - internal_links')
    external_links = [[link, "-"] for link in external_links]
    print('Done - external_links')

    return css_links, js_links, image_links, internal_links, external_links, video_links, file_links


if __name__ == '__main__':
    url = 'https://sefon.pro/'

    # print(get_file_size('https://sefon.pro/assets/main.css'))
    search_links(url)