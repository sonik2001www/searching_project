from celery import shared_task
from django.shortcuts import render
from parser_app.modules.search_link_2 import search_links
from parser_app.modules.get_pagespeed_info import get_pagespeed_info_pars
from parser_app.modules.general import general_pars
from parser_app.modules.micro import micro_pars
from parser_app.modules.html_validate import html_validate_pars
from parser_app.modules.robots import robots_pars
from parser_app.modules.sitemap import sitemap_pars
from parser_app.modules.canonical import canonical_pars
from parser_app.modules.images import images_pars
from parser_app.modules.index import index_pars
from parser_app.modules.main import main_pars
from parser_app.modules.mobile import mobile_pars
from parser_app.modules.redirects import redirects_pars
from parser_app.modules.social import social_pars
from parser_app.modules.tags import tags_pars
from parser_app.modules.whois import whois_pars
from parser_app.modules.builtwith import builtwith_pars
from parser_app.modules.text_analiz import text_analiz_pars
from parser_app.modules.keywords import keywords_pars
from parser_app.templates.modules.get_text_pdf import get_text_pdf_pars


@shared_task
def search_links_async(link):
    print("start pars")
    css_links, js_links, image_links, internal_links, external_links, video_links, file_links = search_links(link)
    print("end pars")
    return css_links, js_links, image_links, internal_links, external_links, video_links, file_links


@shared_task
def get_pagespeed_info_pars_async(link):
    print("start pars")
    lst, output_list, lst_perfom = get_pagespeed_info_pars(link)
    print("end pars")
    return lst, output_list, lst_perfom


@shared_task
def text_analiz_pars_async(link):
    print("start pars")
    lst, semantic_core, significant_words, stop_words = text_analiz_pars(link)

    semantic_core = [[key, value] for key, value in semantic_core[0][1].items()]
    significant_words = [[key, value] for key, value in significant_words[0][1].items()]
    stop_words = [[key, value] for key, value in stop_words[0][1].items()]

    semantic_core = ['Semantic core', semantic_core]
    significant_words = ['Significant words', significant_words]
    stop_words = ['Stop words', stop_words]

    print("end pars")
    return lst, semantic_core, significant_words, stop_words


@shared_task
def general_pars_async(link):
    print("start parsing")
    lst, lst_status = general_pars(link)
    print("end parsing")
    return lst, lst_status


@shared_task
def micro_pars_async(link):
    print("start parsing")
    lst = micro_pars(link)
    print("end parsing")
    return lst


@shared_task
def html_validate_pars_async(link):
    print("start parsing")
    result = html_validate_pars(link)
    print("end parsing")
    return result


@shared_task
def robots_pars_async(link):
    print("start parsing")
    result = robots_pars(link)
    print("end parsing")
    return result


@shared_task
def sitemap_pars_async(link):
    print("start parsing")
    result = sitemap_pars(link)
    print("end parsing")
    return result


@shared_task
def canonical_pars_async(link):
    print("start parsing")
    result = canonical_pars(link)
    print("end parsing")
    return result


@shared_task
def images_pars_async(link):
    print("start parsing")
    result = images_pars(link)
    print("end parsing")
    return result


@shared_task
def index_pars_async(link):
    print("start parsing")
    result = index_pars(link)
    print("end parsing")
    return result


@shared_task
def main_pars_async(link):
    print("start parsing")
    result = main_pars(link)
    print("end parsing")
    return result


@shared_task
def mobile_pars_async(link):
    print("start parsing")
    result = mobile_pars(link)
    print("end parsing")
    return result


@shared_task
def redirects_pars_async(link):
    print("start parsing")
    result = redirects_pars(link)
    print("end parsing")
    return result


@shared_task
def social_pars_async(link):
    print("start parsing")
    result = social_pars(link)
    print("end parsing")
    return result


@shared_task
def tags_pars_async(link):
    print("start parsing")
    result = tags_pars(link)
    print("end parsing")
    return result


@shared_task
def whois_pars_async(link):
    print("start parsing")
    result = whois_pars(link)
    print("end parsing")
    return result


@shared_task
def builtwith_pars_async(link):
    print("start parsing")
    result, fast_check_list, caching_test_list, nested_tables_list, adstxt_list = builtwith_pars(link)
    print("end parsing")
    return result, fast_check_list, caching_test_list, nested_tables_list, adstxt_list


@shared_task
def keywords_pars_async(text):
    print("start parsing")
    output = keywords_pars(text)
    print("end parsing")
    return output


@shared_task
def responsive_page_async(request, E_URL):
    url = request.POST.get("url")

    E = E_URL(url)
    req = E.get_requests()
    url = req.url

    size_display = {
        'iPhone_se': [375, 667],
        'iPhone_xr': [414, 896],
        'iPhone_12_pro': [390, 844],
        'Pixel_5': [1080, 2340],
        'Samsung_Galaxy_S8_plus': [1440, 2960],
        'Samsung_Galaxy_S20_Ultra': [1440, 3200],
        'iPad_Air': [1640, 2360],
        'iPad_Mini': [1488, 1920],
        'Surface_Pro_7': [2736, 1824],
        'Surface_Duo': [1800, 2700],
        'Galaxy_Fold': [1536, 2152],
        'Samsung_Galaxy_A51_71': [1080, 2400],
        'Nest_Hub': [1024, 768],
        'Nest_Hub_Max': [1280, 800],
        'Facebook_for_Android_v407_on_Pixel_6': [1080, 2340]
    }
    select = request.POST.get("select")
    size_display_list = size_display[select]
    if size_display_list[1] > 800:
        height = 800
        width = (800 / size_display_list[1]) * size_display_list[0]
    else:
        height = size_display_list[1]
        width = size_display_list[0]

    pars = True

    # Збереження URL у сховище браузера
    response = render(request, "responsive_page.html", locals())
    response.set_cookie("saved_url", url)

    return response


@shared_task
def get_text_pdf_async(file_path, file_output):
    print("start parsing")
    output = get_text_pdf_pars(file_path, file_output)
    print("end parsing")
    return output

