import json
import requests
from sql_bot import insert_menu, select_menu


def pars(yourmenu):  # парсим еду с сайта и записываем в базу

    url = 'https://caloristika.ru/api/rations'
    response = requests.get(url)

    response_json = json.loads(response.text)

    for x in response_json['sets']:
        if x['category'] == yourmenu:
            if len(x['dishesList']) > 0:
                insert_menu(str(x['day']),
                            str(x['dishesList'][0]),
                            str(x['dishesList'][1]),
                            str(x['dishesList'][2]),
                            str(x['dishesList'][3]))
            else:
                insert_menu(str(x['dishesList']), '', '', '', '')


def unpack(data):  # распаковка полученного ответа из базы(были проблемы с переменной None и кавычками)
    string = select_menu(data)
    if len(string) == 0:
        return "Нет еды("
    string = string[0][0].replace('"', '')
    string = string.replace("'", '"')
    string = string.replace('None', '"None"')
    dic = json.loads(string)
    return dic['name']


if __name__ == "__main__":
    pars('raduem')
