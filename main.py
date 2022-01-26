from parse import unpackg
import telebot

with open('id_bot') as file:
    botid = file.read()
bot = telebot.TeleBot(botid)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, " + message.from_user.first_name +
                         " давай я тебе расскажу, что едят твои ночные коллеги")
    elif message.text == "/help":
        bot.send_message(
            message.from_user.id, "Напиши дату вида 2022-01-06 и получишь список еды за этот день по твоему рациону ")
    else:

        bot.send_message(message.from_user.id, str(unpack(message.text)))


bot.polling(none_stop=True, interval=0)
