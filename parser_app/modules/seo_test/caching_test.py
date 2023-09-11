import pprint
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
from requests.exceptions import MissingSchema


def get_js_scripts(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        js_scripts = []
        for script in soup.select("script"):
            src = script.get("src")
            if src and ('.js' in src or 'js?' in src):
                js_scripts.append(src)

        return ['JS scripts', js_scripts]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

# Replace this with the URL you want to check
#
# url = "https://wanderlog.com/"
#
# js_scripts = get_js_scripts(url)
# if js_scripts:
#     print("JavaScript scripts found on the page:")
#     for js_script in js_scripts:
#         print(js_script)
# else:
#     print("No JavaScript scripts found on the page.")


def check_caching_js_headers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        js_resources = []
        for script in soup.find_all("script"):
            src = script.get("src")
            if src and src.endswith(".js"):
                js_resources.append(src)

        output = []
        print("JavaScript resources on the page:")
        for js_resource in js_resources:
            if js_resource.startswith('/'):
                js_resource = urljoin(url, js_resource)
            try:
                js_response = requests.get(js_resource)
            except MissingSchema:
                continue
            cache_control = js_response.headers.get("Cache-Control")
            expires = js_response.headers.get("Expires")

            print(f"Resource: {js_resource}")
            if cache_control:
                print(f"Cache-Control: {cache_control}")
                output.append([js_resource, f"{cache_control}"])
            elif expires:
                print(f"Expires: {expires}")
                output.append([js_resource, f"Expires: {expires}"])
            else:
                print("No caching headers found")

        return output

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# Replace this with the URL you want to check
# url_to_check = "https://wanderlog.com/"
#
# check_caching_js_headers(url_to_check)


def get_css_scripts(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        js_scripts = []
        # print(soup.find_all("link"))
        for script in soup.find_all("link"):
            src = script.get("href")
            if src and ('.css' in src or 'css?' in src):
                js_scripts.append(src)

        return set(js_scripts)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


def check_caching_css_headers(url):
    try:
        output = []
        for css_resource in get_css_scripts(url):
            css_resource = requests.get(css_resource)
            cache_control = css_resource.headers.get("Cache-Control")
            expires = css_resource.headers.get("Expires")

            print(f"Resource: {css_resource.url}")
            if cache_control:
                print(f"Cache-Control: {cache_control}")
                output.append([css_resource.url, f"{cache_control}"])
            elif expires:
                print(f"Expires: {expires}")
                output.append([css_resource.url, f"Expires: {expires}"])
            else:
                print("No caching headers found")

        if output != []:
            return output

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


# url_to_check = "https://wanderlog.com/"
# check_caching_css_headers(url_to_check)


def caching_test(link):

    caching_test_link = []

    lst = check_caching_js_headers(link)
    if lst:
        caching_test_link.extend(lst)

    lst = check_caching_css_headers(link)
    if lst:
        caching_test_link.extend(lst)

    return caching_test_link


# pprint.pprint(caching_test('https://wanderlog.com/'))
