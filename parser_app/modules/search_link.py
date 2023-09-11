import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def is_video_link(href):
    # Перевіряємо, чи URL містить рядок із словами "video" або "watch" (можна додати інші ключові слова)
    return 'video' in href.lower() or 'watch' in href.lower()


def get_base_url(link):
    pattern = r'^https?://[^/]+'
    match = re.match(pattern, link)
    if match:
        return match.group(0)
    else:
        return None


def search_links(link):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    base_url = get_base_url(link)

    # Створюємо окремі списки для зберігання знайдених посилань різних типів
    links = []
    image_links = []
    video_links = []
    file_links = []

    # Регулярний вираз для перевірки протоколу "http" або "https"
    http_https_pattern = re.compile(r'^https?://')

    # Регулярний вираз для перевірки розширень файлів
    file_extensions_pattern = re.compile(r'\.(pdf|docx?|mp3|wav|wma|ogg|mp4|avi|mov|mkv|wmv|flv|webm|mpeg|mpg|txt|csv|xls|xlsx|ppt|pptx|doc|odt|ods|odp|rtf|zip|rar|7z|gz|tar|exe|msi|apk)$', re.IGNORECASE)

    # Знаходимо всі теги <a> та отримуємо значення атрибуту "href" для кожного з них
    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']

        if http_https_pattern.match(url):
            links.append(url)
        else:
            abs_url = urljoin(link, url)
            links.append(abs_url)

        # Перевіряємо, чи містить посилання на файли з відповідними розширеннями
        if file_extensions_pattern.search(url):
            file_links.append(url)

    # Знаходимо всі теги <img> та отримуємо значення атрибуту "src" для кожного з них
    for img_tag in soup.find_all('img', src=True):
        src = img_tag['src']

        if http_https_pattern.search(src):
            image_links.append(src)
        else:
            abs_url = urljoin(link, src)
            image_links.append(abs_url)

    # Знаходимо всі теги <video> та отримуємо значення атрибутів "src" і "source" для кожного з них
    for video_tag in soup.find_all('video'):
        src = video_tag.get('src')
        source = video_tag.find('source')
        if source:
            src = source.get('src')

        # Якщо посилання містить "http" або "https", то додаємо його в список
        if src and http_https_pattern.search(src):
            video_links.append(src)
        elif src:
            abs_url = urljoin(link, src)
            video_links.append(abs_url)

    video_links.extend([urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) if is_video_link(a['href'])])

    return image_links, video_links, file_links, links


if __name__ == '__main__':
    url = 'https://www.kinofilms.ua/movie/942584/'
    image_links, video_links, file_links, links = search_links(url)

    print("Ссылки на изображения:")
    for link in image_links:
        print(link)

    print("\nСсылки на видео:")
    for link in video_links:
        print(link)

    print("\nfile_links:")
    for link in file_links:
        print(link)

    print("\nДругие ссылки:")
    for link in links:
        print(link)



