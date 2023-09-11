from datetime import datetime
import socket
import sys
from urllib.parse import urlparse

import requests


if __name__ == '__main__':
    url = 'https://rdap.verisign.com/com/v1/domain/{domain}'
    domainname = 'wanderlog.com'
    response = requests.get(url.format(domain=domainname))

    data = response.json()
    other_data = requests.get(data.get('links')[-1]['value']).json()

    registrar_id = data['entities'][0].get('publicIds')[0]['identifier']
    registrar_name = data['entities'][0]['vcardArray'][1][1][3]
    print('Registrar Info: ', registrar_name, 'IANA ID: ', registrar_id)

    print('Domain Information')
    domain_name = data.get('ldhName')
    print('Name: ', domain_name)
    registry_domain_id = data.get('handle')
    print('Registry Domain ID: ', registry_domain_id)

    domain_status = data.get('status') and ', '.join(data.get('status'))
    print(domain_status)

    nameservers = [name['ldhName'] for name in data.get('nameservers')]
    print('Nameservers: ', nameservers)
    creation_date = data['events'][0]['eventDate']
    expiration_date = data['events'][1]['eventDate']
    update_date = data['events'][3]['eventDate']
    print('Created: ', creation_date)
    print('Updated: ', update_date)
    print('Registry Expiration: ', expiration_date)


    def days_left_registry_expiration(expiration_date):
        # Текущая дата и время
        current_date = datetime.utcnow()
        # Целевая дата и время
        target_date = datetime.fromisoformat(expiration_date.replace("Z", ""))
        # Разница между целевой и текущей датой
        time_difference = target_date - current_date
        # Вычисление оставшихся дней и часов
        remaining_days = time_difference.days
        remaining_hours = time_difference.seconds // 3600
        print(f"Days left: {remaining_days}, {remaining_hours} hours.")


    days_left_registry_expiration(expiration_date)
    street = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][2]['value']['values'][0][
        'stringValue']
    locality = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][3]['value']['values'][0][
        'stringValue']
    region = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][4]['value']['values'][0][
        'stringValue']
    postal_code = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][5]['value']['values'][0][
        'stringValue']
    country = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][6]['value']['values'][0][
        'stringValue']
    print('Address: ', street, locality, region, postal_code, country)
    entities = other_data.get('entities', [])

    email = None
    telephone = None
    for entity in entities:
        vcard_array = entity.get('vcardArray', {}).get('properties', [])
        for prop in vcard_array:
            if prop.get('name', '') == 'EMAIL':
                email = prop.get('value', {}).get('stringValue', '')
            elif prop.get('name', '') == 'TEL':
                telephone = prop.get('value', {}).get('stringValue', '')

    print("Email:", email)
    print("Telephone:", telephone)


    #  """Reverse IP"""
    def get_ip_by_domain(domain):
        try:
            ip_address = socket.gethostbyname(domain)
            return ip_address
        except socket.gaierror:
            return None


    def reverseLookup(inp):
        lookup = 'https://api.hackertarget.com/reverseiplookup/?q=%s' % inp
        try:
            result = requests.get(lookup).text
            print(result)
        except:
            sys.stdout.write('Invalid IP address')


    print('Reverse ip: ')
    reverseLookup(get_ip_by_domain(domain_name))


def whois_pars(domainname):
    if 'http' in domainname:
        parsed_url = urlparse(domainname)
        domainname = parsed_url.netloc
        print(domainname)
        if 'www' in domainname:
            domainname = domainname[4:]
            print(domainname)

    lst = []

    try:
        url = 'https://rdap.verisign.com/com/v1/domain/{domain}'
        response = requests.get(url.format(domain=domainname))

        data = response.json()
        other_data = requests.get(data.get('links')[-1]['value']).json()

        try:
            registrar_name = data['entities'][0]['vcardArray'][1][1][3]
            print('Registrar Info: ', registrar_name)
            lst.append(['Registrar Info', registrar_name])
        except:
            lst.append(['Registrar Info', '-'])

        try:
            registrar_id = data['entities'][0].get('publicIds')[0]['identifier']
            print('IANA ID: ', registrar_id)
            lst.append(['IANA ID', registrar_id])
        except:
            lst.append(['IANA ID', '-'])

        try:
            print('Domain Information')
            domain_name = data.get('ldhName')
            print('Name: ', domain_name)
            lst.append(['Name', domain_name])
        except:
            lst.append(['Name', '-'])

        try:
            registry_domain_id = data.get('handle')
            print('Registry Domain ID: ', registry_domain_id)
            lst.append(['Registry Domain ID', registry_domain_id])
        except:
            lst.append(['Registry Domain ID', '-'])

        try:
            domain_status = data.get('status') and ', '.join(data.get('status'))
            print(domain_status)
            lst.append(['Domain status', domain_status])
        except:
            lst.append(['Domain status', '-'])

        try:
            nameservers = [name['ldhName'] for name in data.get('nameservers')]
            print('Nameservers: ', nameservers)
            lst.append(['Nameservers', nameservers])
        except:
            lst.append(['Nameservers', '-'])

        try:
            creation_date = data['events'][0]['eventDate']
            print('Created: ', creation_date)
            lst.append(['Created', creation_date])
        except:
            lst.append(['Created', '-'])

        try:
            expiration_date = data['events'][1]['eventDate']
            print('Registry Expiration: ', expiration_date)
            lst.append(['Registry Expiration', expiration_date])
        except:
            lst.append(['Registry Expiration', '-'])

        try:
            update_date = data['events'][3]['eventDate']
            print('Updated: ', update_date)
            lst.append(['Updated', update_date])
        except:
            lst.append(['Updated', '-'])


        def days_left_registry_expiration(expiration_date):
            try:
                # Текущая дата и время
                current_date = datetime.utcnow()
                # Целевая дата и время
                target_date = datetime.fromisoformat(expiration_date.replace("Z", ""))
                # Разница между целевой и текущей датой
                time_difference = target_date - current_date
                # Вычисление оставшихся дней и часов
                remaining_days = time_difference.days
                remaining_hours = time_difference.seconds // 3600
                print(f"Days left: {remaining_days}, {remaining_hours} hours.")
                lst.append(['Days left', f"{remaining_days}, {remaining_hours} hours."])
            except:
                lst.append(['Days left', '-'])

        try:
            days_left_registry_expiration(expiration_date)
            street = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][2]['value']['values'][0][
                'stringValue']
            locality = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][3]['value']['values'][0][
                'stringValue']
            region = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][4]['value']['values'][0][
                'stringValue']
            postal_code = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][5]['value']['values'][0][
                'stringValue']
            country = other_data['entities'][0]['vcardArray']['properties'][1]['value']['components'][6]['value']['values'][0][
                'stringValue']
            print('Address: ', street, locality, region, postal_code, country)
            lst.append(['Address', f'{street}, {locality}, {region}, {postal_code}, {country}'])
        except:
            lst.append(['Address', '-'])

        try:
            entities = other_data.get('entities', [])

            email = None
            telephone = None
            for entity in entities:
                vcard_array = entity.get('vcardArray', {}).get('properties', [])
                for prop in vcard_array:
                    if prop.get('name', '') == 'EMAIL':
                        email = prop.get('value', {}).get('stringValue', '')
                    elif prop.get('name', '') == 'TEL':
                        telephone = prop.get('value', {}).get('stringValue', '')

            print("Email:", email)
            lst.append(['Email: ', email])
            print("Telephone:", telephone)
            lst.append(['Telephone: ', telephone])
        except:
            lst.append(['Email: ', '-'])
            lst.append(['Telephone: ', '-'])


        #  """Reverse IP"""
        def get_ip_by_domain(domain):
            try:
                ip_address = socket.gethostbyname(domain)
                return ip_address
            except socket.gaierror:
                return None


        def reverseLookup(inp):
            lookup = 'https://api.hackertarget.com/reverseiplookup/?q=%s' % inp
            try:
                result = requests.get(lookup).text
                print(result)
                lst.append(['Reverse ip', result])
            except:
                sys.stdout.write('Invalid IP address')


        print('Reverse ip: ')
        reverseLookup(get_ip_by_domain(domain_name))
    except:
        lst.append(['Invalid domain', 'Try again!'])

    return lst
