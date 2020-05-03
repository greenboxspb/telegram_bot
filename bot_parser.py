import requests
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import key
import parser
from parser import all_obj_pars, all_future_obj_pars

app = Flask(__name__) # LOCAL

# application = Flask(__name__) # SERVER


headers = parser.headers
url_all_objects = parser.url_all_objects
url_future_objects = parser.url_future_objects

token = key.token
URL = 'https://api.telegram.org/bot' + token + '/'

# Ports currently supported for Webhooks: 443, 80, 88, 8443

proxies = {
    'http': '200.89.178.156:80',
    'https': '200.89.178.156:80',
}


# ЗДЕСЬ СОЗДАЕМ json словарь И В ДРУГОЙ ФУНКЦИИ ЗАПИСЫВАЕМ ДАННЫЕ ОТ ПОЛЬЗОВАТЕЛЯ
# функция выполняет ЧТО? записывает последнее обращение пользователя, т.е файл постоянно перезаписывается
# в файле не хранится ВСЯ переписка с пользователем, хотя ВРОДЕ БЫ должна? хз, нужно проверять
def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



# ЗДЕСЬ ТЕЛЕГРАМ ПРИСЫЛАЕТ НА СЕРВЕР ОБНОВЛЕНИЯ ОТ ПОЛЬЗОВАТЕЛЯ
def get_updates():
    url = URL + 'Updates'
    r = requests.get(url, proxies=proxies)
    write_json(r.json())
    return r.json()



# ЗДЕСЬ ОТПРАВЛЯЕТСЯ ОТВЕТ ПОЛЬЗОВАТЕЛЮ
def get_message(chat_id, text):
    url = URL + 'sendMessage'
    reply_markup = {
        'keyboard': [['Сейчас 💩'], ['Потом 🌈'], ['Интересное 👀'], ['Спасибо, брат ✊']],
        'resize_keyboard': True,
    }
    answer = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup,
    }
    r = requests.post(url, proxies=proxies, json=answer)


def send_all_objects():
    r = request.get_json()
    chat_id = r['message']['chat']['id']
    message = r['message']['text']
    text = all_obj_pars(url_all_objects, headers)
    a = 0
    data = []
    data.append('\n')
    data.append('''============\nНЫНЕШНИЕ ОБЪЕКТЫ\n============\n''')
    for name in text['text']:
        data.append(text['text'][a])
        data.append(text['url'][a])
        data.append('\n')
        a += 1
    # data.append(f'ВСЕГО {a}')
    data.append('ВСЕГО {}'.format(a))
    return '\n'.join(data)


def send_future_objects():
    r = request.get_json()
    chat_id = r['message']['chat']['id']
    message = r['message']['text']
    text = all_future_obj_pars(url_future_objects, headers)
    a = 0
    data = []
    data.append('\n')
    data.append('''============\nБУДУЩИЕ ОБЪЕКТЫ\n============\n''')
    for name in text['name']:
        data.append(text['name'][a])
        data.append(text['url'][a])
        data.append('\n')
        a += 1
    # data.append(f'ВСЕГО {a}')
    data.append('ВСЕГО {}'.format(a))
    return '\n'.join(data)

get_updates()


@app.route('/', methods=['POST', 'GET']) # LOCAL

# @application.route('/', methods=['POST', 'GET']) # SERVER

def answer_bot():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        if 'сейчас' in message.lower():
            answer_now = send_all_objects()
            get_message(chat_id, answer_now)

        elif 'потом' in message.lower():
            answer_future = send_future_objects()
            get_message(chat_id, answer_future)

        elif 'спасибо, брат' in message.lower():
            ans = 'Салям Алейкум, брат!'
            get_message(chat_id, ans)

        else:
            get_message(chat_id, 'Ержан, брат! '
                                  'Если хочешь узнать что построено сейчас, '
                                 'нажми "сейчас", '
                                  'если хочешь знать что сдается в будущем, '
                                 'нажми "потом". Салям Алейкум, брат!')
        write_json(r)
        return jsonify(r)
    return 'hello butts!' # ЛОКАЛКА
    # return render_template('index.html') # ДЛЯ СЕРВЕРА


if __name__ == '__main__': # LOCAL
    app.run()

# if __name__ == '__main__':
#     application.run(host='0.0.0.0') # SERVER

# некоторые изменения для тестовой ветки
# теперь делаем коммит в тестовую ветку


# еще какие то изменения в тестовой ветке и коммит
# коммитим еще какие то изменения и сливаем с мастером