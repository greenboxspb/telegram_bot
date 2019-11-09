import requests
from bs4 import BeautifulSoup as bs
import lxml
import json


headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}

#СТРАНИЦА СО ВСЕМИ ОБЪЕКТАМИ
url_all_objects = 'http://gorcenter.spb.ru/objects'


def all_obj_pars(url_all_objects, headers):
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
        print('shit')
    return data


all_obj_pars(url_all_objects, headers)
# print(all_obj_pars(url_all_objects, headers))

# =============================================================================
# =============================================================================

# url_single_object = 'http://gorcenter.spb.ru/object/70'
# ПОДУМАТЬ КАК ДИНАМИЧЕСКИ МЕНЯТЬ УРЛ НЫНЕШНИХ ОБЪЕКТОВ И ВОЗМОЖНО ВСЕ ЭТО ПРИКРУТИТЬ К КНОПКАМ

# def single_obj_pars(url_single_object, headers):
#     session = requests.Session()
#     main_page = session.get(url_single_object, headers=headers)
#
#     if main_page.status_code == 200:
#         page_list = bs(main_page.content, features='lxml')
#         name = page_list.find('td', style='vertical-align:top').next.next.next_sibling
#         deadline = page_list.find('div', style='margin:30px 0 30px 0;border:1px solid #D2D2D2;padding:20px;text-align:center;font-size:21px;background-color: #ecf2fa;')
#         apartments = page_list.find_all('div', style='margin-top:10px;color:#777777;font-size:11px;font-style:italic;')
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
        print('shit')
    return data

all_future_obj_pars(url_future_objects, headers)
# print(all_future_obj_pars(url_future_objects, headers))