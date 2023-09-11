import requests
import pprint
from .get_pagespeed_info_audits import dict_audits, list_audits


from parser_app.modules.url import E_URL


def get_pagespeed_data(api_key, url):
    api_endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "key": api_key
    }

    try:
        response = requests.get(api_endpoint, params=params)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return None


def print_performance_metrics(metrics, word):
    ls = []
    print(f"{'-' * 40}")
    print("Performance Metrics:")
    for metric_key, metric_data in metrics.items():
        if 'displayValue' in metric_data:
            print(f"{metric_key}: {metric_data['displayValue']} ({metric_data['percentile']} "
                  f"{metric_data.get('category', '')})")
            ls.append([metric_key, metric_data['displayValue'],
                       f"({metric_data['percentile']} {metric_data.get('category', '')})"])

        else:
            print(f"{metric_key}: {metric_data['percentile']} {metric_data.get('category', '')}")
            ls.append([word, metric_key, metric_data['percentile'], metric_data.get('category', '')])
    return ls


def main():
    api_key = 'AIzaSyCRCu-0gmSjP2dTBh1NTXlO3vEWrLiKr_k'
    url_test = 'https://www.liga.net/'

    data = get_pagespeed_data(api_key, url_test)

    if data:
        # Обработка полученных данных
        page_title = data['lighthouseResult']['requestedUrl']
        print('Page Title: ', page_title)
        loading_status = data['loadingExperience']['overall_category']
        print('Loading Status: ', loading_status)

        # Показатели производительности
        if "metrics" in data["loadingExperience"]:
            print('DESKTOP')
            metrics = data["loadingExperience"]["metrics"]
            print_performance_metrics(metrics, '999')

        # Показатели мобильной версии
        if "originLoadingExperience" in data:
            print('MOBILE')
            mobile_metrics = data["originLoadingExperience"]["metrics"]
            print_performance_metrics(mobile_metrics, '999')

        # Print audit details
        audits = data["lighthouseResult"]["audits"]
        for audit_key, audit_data in audits.items():
            if audit_key in ['screenshot-thumbnails', 'main-thread-tasks', 'diagnostics', 'network-requests',
                             'final-screenshot', 'metrics', 'network-rtt']:
                continue
            print("-" * 40)
            print(audit_data['id'])

            print("Audit Title:", audit_data["title"])
            if 'description' in audit_data:
                print("Description:", audit_data['description'])
            print("Score:", audit_data["score"])
            print("Display Value:", audit_data.get("displayValue"), "\n")

            try:
                if audit_data.get('details', {}).get('items'):
                    print('------+++Details:')
                    dict_audits[audit_data["id"]](audit_data)
                    pprint.pprint(dict_audits[audit_data["id"]](audit_data))
                    print('------end details')
            except KeyError:
                # Details info
                items = audit_data.get('details', {}).get('items')
                if items and audit_data['details'].get('headings'):
                    # if there is no function, but there is data in detail
                    dict_audits['sub_function'](audit_data)
                    print('------+++----Details:')
                    print(dict_audits['sub_function'](audit_data))
                elif audit_data.get('details') and items:
                    print('details None')
                else:
                    print('None')
                continue
        else:
            print("Error")


def get_pagespeed_info_pars(link):
    api_key = 'AIzaSyCRCu-0gmSjP2dTBh1NTXlO3vEWrLiKr_k'

    print(link)
    E = E_URL(link)
    req = E.get_requests()
    link = req.url
    print(link)

    data = get_pagespeed_data(api_key, link)

    output_list = []
    lst = []
    lst_perfom = []
    lst_additional = []

    if data:
        # Обработка полученных данных
        page_title = data['lighthouseResult']['requestedUrl']
        print('Page Title: ', page_title)
        lst.append(['Page Title', page_title])
        loading_status = data['loadingExperience']['overall_category']
        print('Loading Status: ', loading_status)
        lst.append(['Loading Status', loading_status])

        # Показатели производительности
        if "metrics" in data["loadingExperience"]:
            print('DESKTOP')
            metrics = data["loadingExperience"]["metrics"]
            print_performance_metrics(metrics, 'DESKTOP')
            lst_perfom.extend(print_performance_metrics(metrics, 'DESKTOP'))

        # Показатели мобильной версии
        if "originLoadingExperience" in data:
            print('MOBILE')
            mobile_metrics = data["originLoadingExperience"]["metrics"]
            print_performance_metrics(mobile_metrics, 'MOBILE')
            lst_perfom.extend(print_performance_metrics(mobile_metrics, 'MOBILE'))

        # Print audit details
        audits = data["lighthouseResult"]["audits"]
        for audit_key, audit_data in audits.items():
            ist_out = []
            if audit_key in ['screenshot-thumbnails', 'main-thread-tasks', 'diagnostics', 'network-requests',
                             'final-screenshot', 'metrics', 'network-rtt']:
                continue
            print("-" * 40)
            print(audit_data['id'])

            print("Audit Title:", audit_data["title"])
            ist_out.append(["Audit Title", audit_data["title"]])
            if 'description' in audit_data:
                print("Description:", audit_data['description'])
                ist_out.append(["Description", audit_data['description']])
            print("Score:", audit_data["score"])
            ist_out.append(["Score:", audit_data["score"]])
            print("Display Value:", audit_data.get("displayValue"), "\n")
            ist_out.append(["Display Value:", audit_data.get("displayValue")])

            # print("------------------------------")
            # ist_out.extend(list_audits)
            # output_list.append(ist_out)
            print('Done start')
            try:
                print('Done try')
                if audit_data.get('details', {}).get('items'):
                    print('Details:')
                    dict_audits[audit_data["id"]](audit_data)
                    ist_out.append(["1", dict_audits[audit_data["id"]](audit_data)])

                    output_list.append(ist_out)
                    print('Done 1')

            except KeyError:
                print('Done except')
                # Details info
                items = audit_data.get('details', {}).get('items')
                if items and audit_data['details'].get('headings'):
                    # if there is no function, but there is data in detail
                    ist_out.append(["2", dict_audits['sub_function'](audit_data)])

                    output_list.append(ist_out)
                    print('Done 2')
                elif audit_data.get('details') and items:
                    print('details None')
                else:
                    print('None')
                continue

    else:
        print("Error")

    return lst, output_list, lst_perfom


if __name__ == "__main__":
    main()
