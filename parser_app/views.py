import time
import random

from django.shortcuts import render, redirect

import os
import shutil
from django.conf import settings

from parser_app.modules.url import E_URL

from .tasks import (
    search_links_async,
    get_pagespeed_info_pars_async,
    general_pars_async,
    micro_pars_async,
    html_validate_pars_async,
    robots_pars_async,
    sitemap_pars_async,
    canonical_pars_async,
    images_pars_async,
    index_pars_async,
    main_pars_async,
    mobile_pars_async,
    redirects_pars_async,
    social_pars_async,
    tags_pars_async,
    whois_pars_async,
    builtwith_pars_async,
    responsive_page_async,
    text_analiz_pars_async,
    keywords_pars_async,
    get_text_pdf_async,
)


def search_link(request):
    pars = False

    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        # Запуск асинхронної задачі
        print("start async")
        async_result = search_links_async.delay(link)
        print("end async")
        pars = True
        css_links, js_links, image_links, internal_links, external_links, video_links, file_links = async_result.get()

    return render(request, 'search_link.html', locals())


def get_pagespeed_info(request):

    # видалити [-1][1] і вставляри розібрані стрічки
    st = [1,2.3,3]
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        # Запуск асинхронної задачі
        async_result = get_pagespeed_info_pars_async.delay(link)
        pars = True
        lst, output_list, lst_perfom = async_result.get()

        for output in output_list:

            ls = output[-1].copy()

            output.pop()

            result_list = []  # Створюємо пустий список для результатів

            print(ls[1], '\n\n\n')

            if type(ls[1]) == list:

                for dictionary in ls[1]:
                    try:
                        sub_list = []  # Створюємо пустий список для кожного словника
                        for key, value in dictionary.items():
                            # print(type(value) == list and type(value[0]) == dict)
                            if type(value) == list and type(value[0]) == dict:
                                for dict_2 in value:
                                    if type(dict_2) != dict:
                                        sub_list.append([key, dict_2])
                                        continue

                                    for key_2, value_2 in dict_2.items():
                                        sub_list.append([key_2, value_2])

                            else:
                                sub_list.append([key, value])  # Додаємо ключ та значення у вкладений список
                        result_list.append(sub_list)  # Додаємо вкладений список до результату
                    except:
                        print('-------')

            else:
                try:
                    sub_list = []  # Створюємо пустий список для кожного словника
                    for key, value in ls[1].items():
                        if type(value) == list and type(value[0]) == dict:
                            for dict_2 in value:
                                if type(dict_2) != dict:
                                    sub_list.append([key, dict_2])
                                    continue

                                for key_2, value_2 in dict_2.items():
                                    sub_list.append([key_2, value_2])

                        else:
                            sub_list.append([key, value])  # Додаємо ключ та значення у вкладений список
                    result_list.append(sub_list)  # Додаємо вкладений список до результату
                except:
                    print('-------')

            output.append(['this', result_list])

    return render(request, 'get_pagespeed_info.html', locals())


def text_analiz(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        # Запуск асинхронної задачі
        async_result = text_analiz_pars_async.delay(link)
        pars = True
        lst, semantic_core, significant_words, stop_words = async_result.get()

    return render(request, 'text_analiz.html', locals())


def general(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = general_pars_async.delay(link)
        pars = True
        lst, lst_status = async_result.get()

    return render(request, 'general.html', locals())


def micro(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = micro_pars_async.delay(link)
        pars = True
        lst = async_result.get()

    return render(request, 'micro.html', locals())


def html_validate(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = html_validate_pars_async.delay(link)
        lst = async_result.get()
        lst_new = []
        print()
        for i in lst:
            lst_new.append(["", i])
        pars = True

    return render(request, 'html_validate.html', locals())


def robots(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = robots_pars_async.delay(link)
        pars = True
        lst, lst_status = async_result.get()

    return render(request, 'robots.html', locals())


def sitemap(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = sitemap_pars_async.delay(link)
        pars = True
        lst, lst_status = async_result.get()

    return render(request, 'sitemap.html', locals())


def canonical(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = canonical_pars_async.delay(link)
        pars = True
        lst = async_result.get()

    return render(request, 'canonical.html', locals())


def images(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = images_pars_async.delay(link)
        pars = True
        images_lst, empty_lst, src_lst, pil_lst, alt_lst, title_lst, format_lst, dim_lst = async_result.get()

    return render(request, 'images.html', locals())


def index(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = index_pars_async.delay(link)
        pars = True
        lst = async_result.get()

    return render(request, 'index.html', locals())


def main(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = main_pars_async.delay(link)
        pars = True
        lst = async_result.get()

    return render(request, 'main.html', locals())


def mobile(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = mobile_pars_async.delay(link)
        pars = True
        lst = async_result.get()

    return render(request, 'mobile.html', locals())


def redirects(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = redirects_pars_async.delay(link)
        pars = True
        lst, lst_status = async_result.get()

    return render(request, 'redirects.html', locals())


def social(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = social_pars_async.delay(link)
        pars = True
        lst, lst_status = async_result.get()

    return render(request, 'social.html', locals())


def tags(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = tags_pars_async.delay(link)
        pars = True
        lst, lst_status, lst_h = async_result.get()

    return render(request, 'tags.html', locals())


def whois(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = whois_pars_async.delay(link)
        pars = True
        lst = async_result.get()

    return render(request, 'whois.html', locals())


def responsive_page(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == "POST":

        async_result = responsive_page_async.delay(request, E_URL)
        response = async_result.get()

        return response

    # Отримання збереженого URL з сховища браузера
    saved_url = request.COOKIES.get("saved_url", "")
    return render(request, "responsive_page.html", {"url": saved_url})


def builtwith(request):
    pars = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        link = request.POST.get('link')
        async_result = builtwith_pars_async.delay(link)
        pars = True
        lst, fast_check_list, caching_test_list, nested_tables_list, adstxt_list = async_result.get()
        len_caching_test_list = len(caching_test_list)

    return render(request, 'builtwith.html', locals())


def keyword(request):
    pars = False
    problem = False
    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        text = request.POST.get('text')

        if text:
            text_list = text.replace('\r', '').split('\n')
        else:
            print(request.FILES)
            print(request.FILES.get('file-upload'))
            uploaded_file = request.FILES.get('file-upload')
            file_content = uploaded_file.read().decode('utf-8')  # Зчитуємо вміст файлу
            text_list = file_content.replace('\r', '').split('\n')

        try:
            async_result = keywords_pars_async.delay(text_list)
            pars = True
            output = async_result.get()
            path = output.split('/')
            path = '/' + '/'.join(path[-3:])
        except:
            problem = True

    return render(request, 'keyword.html', locals())


def get_text_pdf(request):
    pars = False

    if request.method == 'POST' and not request.user.is_authenticated:
        return redirect('/accounts/login/')

    if request.method == "POST":
        print(request.FILES)
        uploaded_file = request.FILES.get('file-upload')
        file_content = uploaded_file.read()
        file_name = uploaded_file.name

        random_str = str(random.randint(1, 10000))

        include_html = f'modules/output{random_str}.html'

        save_path = '/Users/applebuy/PycharmProjects/projects1/searching/searching_project/parser_app/templates/modules/output.pdf'
        html_path = f'/Users/applebuy/PycharmProjects/projects1/searching/searching_project/parser_app/templates/modules/output{random_str}.html'

        with open(save_path, 'wb') as destination:
            destination.write(file_content)

        async_result = get_text_pdf_async.delay(save_path, html_path)

        pars = True

        time.sleep(5)

        copy_png_files_to_static()

    return render(request, 'modules/get_text_pdf.html', locals())


def copy_png_files_to_static():
    # Шлях до папки 'static', куди ми копіюємо файли
    destination_folder = os.path.join(settings.BASE_DIR, 'parser_app', 'static')

    # Перевірка і видалення всіх файлів PNG в 'static'
    for filename in os.listdir(destination_folder):
        if filename.endswith('.png'):
            file_path = os.path.join(destination_folder, filename)
            os.remove(file_path)

    # Шлях до папки 'modules', звідки ми копіюємо файли
    source_folder = os.path.join(settings.BASE_DIR, 'parser_app', 'templates', 'modules')

    # Перевірка і створення папки 'static', якщо вона не існує
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Проходження по всіх файлах у вихідній папці
    for filename in os.listdir(source_folder):
        # Перевірка, чи файл є PNG
        if filename.endswith('.png'):
            # Створення повного шляху до вихідного файлу
            source_file_path = os.path.join(source_folder, filename)

            # Створення повного шляху до призначення файлу в 'static'
            destination_file_path = os.path.join(destination_folder, filename)

            # Копіювання файлу
            shutil.copy(source_file_path, destination_file_path)

            # Видалення вихідного файла
            os.remove(source_file_path)

