import telebot
import json
import requests
import sqlite3

def insert_menu(date, course_0,course_1,course_2,course_3): #записываем еду в базу
    if not(select_menu(date)): 
        try:
            condb = sqlite3.connect('daily_food.db')
            cursor = condb.cursor()

            sql_insert = """INSERT INTO date_menu
                                      (date, course_0, course_1, course_2, course_3)
                                  VALUES (?, ?, ?, ?, ?);"""

            data_tuple = (date, course_0,course_1,course_2,course_3)
            cursor.execute(sql_insert, data_tuple)
            condb.commit()

            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

def select_menu(date): #получаем еду из базы по дате 
    try:
        condb = sqlite3.connect('daily_food.db')
        cursor = condb.cursor()

        sql_query = """SELECT course_0, course_1, course_2, course_3 FROM date_menu
                              WHERE date = ?;"""

        cursor.execute(sql_query, (date,))
        record = cursor.fetchall()
        

        cursor.close()
        return(record)

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

def pars(yourmenu): # парсим еду с сайта и записываем в базу

    url = 'https://caloristika.ru/api/rations'
    response = requests.get(url)

    response_json = json.loads(response.text)

    for x in response_json['sets']:
        if x['category'] == yourmenu :
            if len(x['dishesList'])>0:
                insert_menu(str(x['day']), 
                    str(x['dishesList'][0]),
                    str(x['dishesList'][1]),
                    str(x['dishesList'][2]),
                    str(x['dishesList'][3]))
            else:
                insert_menu(str(x['dishesList']),'','','','')



def unpack(data): #распаковка полученного ответа из базы(были проблемы с переменной None и кавычками)
    string = select_menu(data)
    if len(string) == 0:
    	return "Нет еды("
    string = string[0][0].replace('"', '')
    string = string.replace("'",'"')
    string = string.replace('None','"None"')
    dic = json.loads(string)
    return dic['name']


pars('raduem')
with open('id_bot') as file:
        botid =  file.read()
bot = telebot.TeleBot(botid);
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, " + message.from_user.first_name  + " давай я тебе расскажу, что едят твои ночные коллеги")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши дату вида 2022-01-06 и получишь список еды за этот день по твоему рациону ")
    else:

        bot.send_message(message.from_user.id, str(unpack(message.text)))

bot.polling(none_stop=True, interval=0)