from bs4 import BeautifulSoup
import requests
from concurrent import futures

headers = {"User-Agent": "Mozilla/5.0"}


def get_pages():
    url = 'https://www.ioutletstore.pt/categoria-produto/iphones/page/2/'
    pages_list = set()

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        pagen = int(soup.select('a.page-numbers')[-2].text)
    except (ValueError, AttributeError):
        pagen = 100

    pages = [f'https://www.ioutletstore.pt/categoria-produto/iphones/page/{i}/' for i in range(1, pagen + 1)]

    return pages


def get_data(page):
    print(page)

    response = requests.get(page, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.find_all('div', attrs={'class': 'woocommerce-card__header'})
    print(len(cards))

    grades = {'Grau C Mais': '1', 'Grau C': '2', 'Grau B': '3', 'Grau A': '4', 'Grau Premium': '5', }

    for card in cards:
        link = card.find('a').get('href')
        card_header = [item.strip() for item in card.find('a').text.split('–')[0].split('/')]

        try:
            grade = card_header[2].lower()
            color = card_header[1].strip().lower()
            *name, gb = card_header[0].split()
            gb = gb.replace('GB', 'Gb')
            name = ' '.join(name)

        except IndexError:
            try:
                if 'gb' in card_header[0]:
                    card_header[0] = card_header[0].replace('gb', 'GB')

                name_gb = card_header[0].split('GB')[0]
                color_grade = card_header[0].split('GB')[1]

                *name, gb = name_gb.split()
                name = ' '.join(name)
                gb = f'{gb}Gb'

                *color, grade = color_grade.split('Grau')
                print(' '.join(color).strip(), f'Grau {grade.strip()}')
                color = ' '.join(color).strip().lower()
                grade = f'Grau {grade.strip()}'.lower()
                print(name, gb, color, grade)
            except IndexError:
                continue

        full_name = f'{name} - {gb} - {color} - {grade}'

        price = card.find('span', attrs={'class': 'woocommerce-Price-amount amount'}).text.strip()[:-1].replace(',',
                                                                                                                '.')
        try:
            ss = card.find_all('span', attrs={'class': 'woocommerce-Price-amount amount'})

            if len(ss) >= 2:
                price = ss[1].text.strip()[:-1].replace(',', '.')
        except:
            print("no------")
        if price.count('.') > 1:
            price = ''.join(price.split('.', maxsplit=1))
        try:
            price = float(price)
        except ValueError:
            price = None

        print(full_name, price, link)
        defaults = {'name': full_name, 'price': price, 'imported': False}


def main():
    pages_list = get_pages()
    # for page in pages_list[::-1]:
    #     get_data(page)

    with futures.ThreadPoolExecutor(20) as executor:
        executor.map(get_data, pages_list[::-1])

    requests.get('https://scraper.isell.pt/admin/competitor/stop/3')

main()