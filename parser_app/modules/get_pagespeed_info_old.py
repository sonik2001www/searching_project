import requests
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


def print_audit_details(audits):
    for audit_key, audit_data in audits.items():
        if audit_key == "screenshot-thumbnails":
            continue  # Skip printing details for "Screenshot Thumbnails" audit
        print(f"{'-' * 40}")
        print(f"Audit: {audit_data['title']}")
        print(f"Score: {audit_data['score']}")
        if 'description' in audit_data:
            print(f"Description: {audit_data['description']}")
        if 'details' in audit_data:
            if isinstance(audit_data['details'], dict):  # Check if 'details' is a dictionary
                for detail_key, detail_value in audit_data['details'].items():
                    if isinstance(detail_value, dict) and 'displayValue' in detail_value:
                        print(f"   {detail_key}: {detail_value['displayValue']}")
            else:
                for detail_value in audit_data['details']:
                    if isinstance(detail_value, dict) and 'displayValue' in detail_value:
                        print(f"   {audit_key}: {detail_value['displayValue']}")


def print_performance_metrics(metrics, word):
    ls = []
    print(f"{'-' * 40}")
    print("Performance Metrics:")
    for metric_key, metric_data in metrics.items():
        if 'displayValue' in metric_data:
            print(f"{metric_key}: {metric_data['displayValue']} ({metric_data['percentile']} " f"{metric_data.get('category', '')})")

            ls.append([metric_key, metric_data['displayValue'], f"({metric_data['percentile']} {metric_data.get('category', '')})"])

        else:
            print(f"{metric_key}: {metric_data['percentile']} {metric_data.get('category', '')}")
            ls.append([word, metric_key, metric_data['percentile'], metric_data.get('category', '')])
    return ls


def get_pagespeed_info_pars(link):
    api_key = 'AIzaSyCRCu-0gmSjP2dTBh1NTXlO3vEWrLiKr_k'

    E = E_URL(link)
    req = E.get_requests()
    link = req.url
    url_test = link

    data = get_pagespeed_data(api_key, url_test)
    output_list = []
    lst = []
    lst_perfom = []

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
            lst_perfom.extend(print_performance_metrics(metrics, 'DESKTOP'))

        # Показатели мобильной версии
        if "originLoadingExperience" in data:
            print('MOBILE')
            mobile_metrics = data["originLoadingExperience"]["metrics"]
            lst_perfom.extend(print_performance_metrics(mobile_metrics, 'MOBILE'))

        # Print audit details
        audits = data["lighthouseResult"]["audits"]
        for audit_key, audit_data in audits.items():
            ist_out = []
            if audit_key == "screenshot-thumbnails":
                continue
            print("-" * 40)
            print("Audit Title:", audit_data["title"])
            ist_out.append(["Audit Title", audit_data["title"]])
            if 'description' in audit_data:
                print("Description:", audit_data['description'])
                ist_out.append(["Description", audit_data['description']])
            else:
                print('-')
            print("Score:", audit_data["score"])
            ist_out.append(["Score:", audit_data["score"]])
            print("Display Value:", audit_data.get("displayValue"), "\n")
            ist_out.append(["Display Value:", audit_data.get("displayValue")])
            output_list.append(ist_out)
    else:
        print("Error")

    return lst, output_list, lst_perfom


if __name__ == "__main__":
    get_pagespeed_info_pars('https://www.liga.net/')
