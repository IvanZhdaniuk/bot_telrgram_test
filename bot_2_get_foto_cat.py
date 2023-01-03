# pip install pytelegrambotapi

# from dataclasses import dataclass

import telebot
from telebot import types
import requests
import time

API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://aws.random.cat/meow'
BOT_TOKEN: str =''
TEXT: str = 'first massage'
ERROR_TEXT: str = "IF YOU WANT GET A PHOTO WITH CAT, PUT BUTTON 'I want a cat'"
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int
cat_link: str
cat_response: requests.Response

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
        markup = types.ReplyKeyboardMarkup()
        button1 = types.KeyboardButton('I want a dog')
        markup.add(button1)
        bot.send_message(message.from_user.id, "Choose one letter:", reply_markup=markup)


# bekends
while counter < MAX_COUNTER:
        api_url_update = f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset+1}'
        response2 = requests.get(api_url_update).json()
        print(response2)



        if response2['result']:
                for result in response2['result']:
                        offset = result['update_id']
                        chat_id = result['message']['from']['id']
                        chat_text = str(result['message']['text'])
                        message_text = result['message']
                        cat_response = requests.get(API_CATS_URL)

                        if cat_response.status_code == 200 and chat_text == 'I want a cat':
                                cat_link = cat_response.json()['file']
                                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')

                        else:
                                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')


                time.sleep(1)
                counter += 1





#
# api_url = f'https://api.telegram.org/{token}/getMe'
#
# api_url_update = f'https://api.telegram.org/{token}/getUpdates'

# api_url_update = f'https://api.telegram.org/{token}/sendMessage?chat_id=1338444137&text=Привет, Mikhail!'
# response2 = requests.get(api_url_update)

# response = requests.get(api_url)






# @bot.message_handler(commands=['Start', 'Help'])
# def send_welcome(message):
#     bot.reply_to(message, "Привет, приветсвую тебя в самом продвинутом телеграм канале, здесь ты как в конструкторе"
#                           " можешь собрать все интересующие тебя уведомленияю: новости, курсы валют, и даже обновления"
#                           " твоих рузей в Instogtram.")

# @bot.message_handler(commands=['Start', 'Help']
# def send_welcome(message):
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     itembtn1 = types.KeyboardButton('a')
#     itembtn2 = types.KeyboardButton('v')
#     itembtn3 = types.KeyboardButton('d')
#     markup.add(itembtn1, itembtn2, itembtn3)
#     bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)
#
@bot.message_handler(func=lambda m: True)
def echo_all(message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('I wsadgagdagdagd')
        itembtn2 = types.KeyboardButton('v')
        # itembtn3 = types.KeyboardButton('d')
        markup.row(itembtn1, itembtn2)
        bot.send_message(message.from_user.id, "Choose one letter:", reply_markup=markup)


