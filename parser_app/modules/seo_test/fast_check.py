import re
from urllib.parse import urlparse, urljoin
import socket
import ssl

import requests
from bs4 import BeautifulSoup

website_url = "https://wanderlog.com/"


def check_https(url):
    """SSL Checker and HTTPS Test"""
    response = requests.get(url)
    if response.url.startswith('https://'):
        print(f"The website {url} is using HTTPS.")
        return ['HTTPS', [True]]
    else:
        print(f"The website {url} is not using HTTPS.")
        return ['HTTPS', [False]]


# check_https(website_url)


def check_http2(domain_name):
    """HTTP2 Test"""
    socket.setdefaulttimeout(5)
    if not domain_name.startswith('https://'):
        domain_name = 'https://' + domain_name
    try:
        HOST = urlparse(domain_name).netloc
        PORT = 443

        ctx = ssl.create_default_context()
        ctx.set_alpn_protocols(['h2', 'spdy/3', 'http/1.1'])

        conn = ctx.wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
        conn.connect((HOST, PORT))

        pp = conn.selected_alpn_protocol()

        if pp == "h2":
            return ['http2', [True]]
        else:
            return ['http2', [False]]
    except Exception as e:
        print(e)


# print(check_http2('youtube.com'))


def check_hsts_support(url):
    """HSTS Test"""
    try:
        response = requests.get(url)

        if "strict-transport-security" in response.headers:
            print(f"{url} supports HSTS")
            return ['HSTS', [True]]
        else:
            print(f"{url} does not support HSTS")
            return ['HSTS', [False]]
    except Exception as e:
        print(f"An error occurred: {e}")


# Replace "https://example.com" with the actual website's URL
# check_hsts_support('https://wanderlog.com/')


def check_suspicious_website(url):
    """Safe Browsing Test"""
    api_key = "AIzaSyCRCu-0gmSjP2dTBh1NTXlO3vEWrLiKr_k"  # Replace with your actual Google API key
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"

    payload = {
        "client": {
            "clientId": "your-client-id",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "PHISHING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(api_url, json=payload)
        data = response.json()

        if "matches" in data:
            print(f"{url} is suspicious (matches found)")
            return ['Check suspicious', ['url is suspicious (matches found)']]
        else:
            print(f"{url} is safe")
            return ['Check suspicious', ['url is safe']]
    except Exception as e:
        print(f"An error occurred: {e}")


# Replace "https://example.com" with the actual website's URL
# check_suspicious_website(website_url)


def check_server_signature(url):
    """Server Signature Test"""
    try:
        response = requests.get(url)

        if "Server" in response.headers:
            server_signature = response.headers["Server"]
            print(f"Server signature: {server_signature}")
            return ['Server signature', [server_signature]]
        else:
            print("Server signature not found in response headers.")
            return ['Server signature', ['not found in response headers.']]
    except Exception as e:
        print(f"An error occurred: {e}")


# Replace "https://example.com" with the actual website's URL
# check_server_signature(website_url)


def check_directory_browsing(url):
    """Directory Browsing Test"""
    result = []
    for check in ['index', 'path', 'default', 'includes', 'main', 'files', 'images', 'pics', 'vids',
                  'home/siteurl/web/includes/.htaccess', 'default.html', '.htaccess']:
        url = urljoin(url, check)
        try:
            response = requests.get(url)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                response_text = response.text.lower()

                if content_type.startswith("text/html") and "index of" in response_text:
                    result.append(False)
                else:
                    result.append(True)
            else:
                continue
        except Exception as e:
            print(f"An error occurred: {e}")
    if all(result):
        return ['Directory browsing', ['is likely disabled.']]
    return ['Directory browsing', ['is likely allowed.']]


# Replace "https://example.com/directory/" with the actual URL of the directory
# print(check_directory_browsing(website_url))


def extract_emails_from_webpage(url):
    """Plaintext Emails Test"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            email_pattern = r"[-a-zA-Z0-9._%+]+@[-a-zA-Z0-9.]+\.[a-zA-Z]{2,4}"

            email_addresses = re.findall(email_pattern, response.text, re.IGNORECASE)

            if email_addresses:

                for match in email_addresses:
                    pattern = ("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:["
                               "\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\["
                               "\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+["
                               "a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}("
                               "?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:["
                               "\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\["
                               "\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])")
                    email = re.match(pattern, match)[0]
                    if email:
                        print(email)
                        return ['Plaintext Emails', [email]]
            else:
                print("No plaintext email addresses found.")
                return
        else:
            print(f"Server returned status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace "https://example.com" with the actual URL of the webpage
# extract_emails_from_webpage(website_url)


def check_links_for_rel_attribute(url):
    """Unsafe Cross-Origin Links Test"""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        return

    soup = BeautifulSoup(response.content, 'lxml')

    links = soup.find_all('a', target='_blank')
    without_rel = []
    for link in links:
        if 'rel' not in link.attrs or ('noopener' not in link['rel'] and 'noreferrer' not in link['rel']):
            without_rel.append(link['href'])

    if without_rel != []:
        return ['Unsafe Cross-Origin Links', without_rel]


# check_links_for_rel_attribute('https://rozetka.com.ua/ua/search/?seller=rozetka&text=iPhone+14+Pro+Max')

def fast_check_all(link):

    fast_check_list = []

    lst = check_https(link)
    if lst:
        fast_check_list.append(lst)

    lst = check_http2(link)
    if lst:
        fast_check_list.append(lst)

    lst = check_hsts_support(link)
    if lst:
        fast_check_list.append(lst)

    lst = check_suspicious_website(link)
    if lst:
        fast_check_list.append(lst)

    lst = check_server_signature(link)
    if lst:
        fast_check_list.append(lst)

    lst = check_directory_browsing(link)
    if lst:
        fast_check_list.append(lst)

    lst = extract_emails_from_webpage(link)
    if lst:
        fast_check_list.append(lst)

    lst = check_links_for_rel_attribute(link)
    if lst:
        fast_check_list.append(lst)

    return fast_check_list
