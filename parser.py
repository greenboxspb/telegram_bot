import requests
from bs4 import BeautifulSoup as bs
import lxml
import json


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

url_all_objects = 'http://gorcenter.spb.ru/objects'

def all_obj_pars(url_all_objects, headers):

    """ СТРАНИЦА СО ВСЕМИ ОБЪЕКТАМИ """

    session = requests.Session()
    main_page = session.get(url_all_objects, headers=headers)

    if main_page.status_code == 200:
        page_list = bs(main_page.content, features='lxml')
        content = page_list.find('div', 'textSectionCommon900') #div со всеми объектами
        url_obj = content.find_all('a', 'img') #URL объекта
        h1 = content.find_all('div', 'count-rooms-raspredelenie') #заголовок объекта в пределах div
        a = 0
        text = []
        url = []
        data = {
            'text': text,
            'url': url,
        }
        for link in url_obj:
            # h = h1[a].next_sibling # заголовок объектра за пределами div (в теге <br>)
            text.append(str(h1[a].next_sibling).strip('\n')) # заголовок объектра за пределами div (в теге <br>)
            url.append(link.get('href'))
            a += 1
    else:
        return 'shit'
    return data


all_obj_pars(url_all_objects, headers)
# print(all_obj_pars(url_all_objects, headers))



# url_news = 'http://gorcenter.spb.ru/pressa'
#
# def last_news(url_news, headers):
#     session = requests.Session()
#     main_page = session.get(url_news, headers=headers)
#
#     if main_page.status_code == 200:
#         page_list = bs(main_page.content, features='lxml')
#         content = page_list.find('div', 'textSectionCommon')
#         date = content.find_all(class_='news_date')
#         text = content.find_all('div', 'news_date')
#
#
#         for d in date: # выводит чистые значения
#             print(d.text)
#             print(len(d.next.next))
#
#         # for c in text:
#         #     print(c)
#         #     # print(c.next_sibling)
#
#
# last_news(url_news, headers)
# =============================================================================
# =============================================================================

# url_single_object = 'http://gorcenter.spb.ru/object/70'
#
# """ ПОДУМАТЬ КАК ДИНАМИЧЕСКИ МЕНЯТЬ УРЛ НЫНЕШНИХ ОБЪЕКТОВ И ВОЗМОЖНО ВСЕ ЭТО ПРИКРУТИТЬ К КНОПКАМ """
#
# def single_obj_pars(url_single_object, headers):
#     session = requests.Session()
#     main_page = session.get(url_single_object, headers=headers)
#
#     if main_page.status_code == 200:
#         page_list = bs(main_page.content, features='lxml')
#         name = page_list.find('td', style='vertical-align:top').next.next.next_sibling
#         deadline = page_list.find('div', style='margin:30px 0 30px 0;border:1px solid #D2D2D2;padding:20px;text-align:center;font-size:21px;background-color: #ecf2fa;')
#         print(deadline)
#         apartments = page_list.find_all('div', style='margin-top:10px;color:#777777;font-size:11px;font-style:italic;')
#         print(apartments)
#         info = []
#         data = {
#             'name': name,
#             'deadline': deadline.text,
#             'info': info,
#         }
#         for aprt in apartments:
#             info.append(aprt)
#     else:
#         print('shit')
#     return data

# single_obj_pars(url_single_object, headers)
# print(single_obj_pars(url_single_object, headers))

# =============================================================================
# =============================================================================


url_future_objects = 'http://gorcenter.spb.ru/kapitalny-remont'

def all_future_obj_pars(url_future_objects, headers):

    """ БУДУЩИЕ ОБЪЕКТЫ """

    session = requests.Session()
    main_page = session.get(url_future_objects, headers=headers)

    if main_page.status_code == 200:
        page_list = bs(main_page.content, features='lxml')
        info = page_list.find_all('div', 'remontRowAll')
        url = []
        name = []
        data = {
            'url': url,
            'name': name,
        }
        for i in info:
            url_info = i.find('img').previous.get('href')
            url.append(url_info)
            name_obj = i.find('div', class_='remontOneTechInfoTitle')
            name.append(name_obj.text)
    else:
        return 'shit'
    return data

all_future_obj_pars(url_future_objects, headers)
# print(all_future_obj_pars(url_future_objects, headers))


# =============================================================================
# =============================================================================


def favorite_obj_pars():

    """ ИЗБРАННЫЕ ОБЪЕКТЫ, КОТОРЫЕ МЫ ИЩЕМ СРЕДИ ВСЕХ ОБЪЕКТОВ (url_future_objects)"""

    name_obj = all_future_obj_pars(url_future_objects, headers)['name']
    url_obj = all_future_obj_pars(url_future_objects, headers)['url']
    favorite_obj_name = []
    favorite_obj_url = []

    for name in name_obj:
        if 'Обводн' in name:
            favorite_obj_name.append(name)
        if 'Серпуховск' in name:
            favorite_obj_name.append(name)
        if 'Красноармейск' in name:
            favorite_obj_name.append(name)
        if '9-я лин' in name:
            favorite_obj_name.append(name)
        if 'Рижск' in name:
            favorite_obj_name.append(name)
        if 'Старо' in name:
            favorite_obj_name.append(name)

    for url in url_obj:
        if 'obvodn' in url:
            favorite_obj_url.append(url)
        if 'serp' in url:
            favorite_obj_url.append(url)
        if 'krasno' in url:
            favorite_obj_url.append(url)
        if '9-ya' in url:
            favorite_obj_url.append(url)
        if 'rig' in url:
            favorite_obj_url.append(url)
        if 'staro' in url:
            favorite_obj_url.append(url)

    data = {
        'favorite_obj_name': favorite_obj_name,
        'favorite_obj_url': favorite_obj_url,
    }

    return data
    # print(data)

favorite_obj_pars()
# print(favorite_obj_pars())


# =============================================================================
# =============================================================================


def img_favorite_obj_pars():

    """ ЗДЕСЬ МЫ ВЫТАСКИВАЕМ КАРТИНКИ ИЗ СТРАНИЦ ИЗБРАННЫХ ОБЪЕКТОВ (favorite_obj_pars) """
    
    url = favorite_obj_pars()['favorite_obj_url']
    img_url = []
    data = {
        'img_url': img_url,
    }
    a = 0
    for pars in url:
        print(pars, a)
        a += 1
        session = requests.Session()
        main_page = session.get(pars, headers=headers)
        img = []
        data = {
            'img': img,
        }
        if main_page.status_code == 200:
            try:
                page_list = bs(main_page.content, features='lxml')
                image = page_list.find('div', 'panorama-container')
                img_src = image.find_all('img')
                img = []
                data = {
                    'img': img,
                }
                # print(img, 'DAT')
                n = 0
                for i in img_src:
                    try:
                        # print(i, 'AA')
                        img.append(i['src'])
                        # print(i['src'], 'BBB', n)

                    except:
                        continue
                        # print('yhh')
                    n += 1
            except:
                continue
        else:
            continue

    img_url.append(data['img'])
            # return img
    # return data
# print(data, 'DATA')

img_favorite_obj_pars()
print(img_favorite_obj_pars())

# print(img_favorite_obj_pars())



111