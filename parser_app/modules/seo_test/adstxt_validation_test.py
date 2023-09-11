import requests


def check_ads_txt_validity(url):
    try:
        ads_txt_url = f"{url}/ads.txt"
        response = requests.get(ads_txt_url)

        if response.status_code == 200:
            ads_txt_content = response.text
            lines = ads_txt_content.split('\n')
            # print(ads_txt_content)
            for line in lines:
                parts = line.split(',')
                if len(parts) != 3:
                    return ["ads.txt is in a valid format.", line]
                if parts[1].strip() != "DIRECT" and parts[1].strip() != "RESELLER":
                    return ["ads.txt is in a valid format.", line]

                # Additional checks could be performed here if needed
            print("ads.txt is in a valid format.")
        else:
            print(f"ads.txt not found or error: {response.status_code}")
            return [f"ads.txt not found or error:", response.status_code]
    except Exception as e:
        print(f"An error occurred: {e}")
        return [f"An error occurred:", e]

# Replace "https://example.com" with the actual website's URL
# print(check_ads_txt_validity("https://example.com"))


def adstxt_validation_test(link):
    return check_ads_txt_validity(link)
