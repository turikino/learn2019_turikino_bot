import ephem
from random import choice
from datetime import datetime
from glob import glob
from emoji import emojize
from telegram import ReplyKeyboardMarkup

import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')

import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

PROXY = {
    'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn', 'password': 'python'
    }
}


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    name = update["message"]["chat"]["first_name"]
    text = "Привет, {}! {}".format(name, smile)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def planet_info(bot, update):
    planet_name = update.message.text.split()[-1]
    planet_attr = getattr(ephem, planet_name)
    planet = planet_attr()
    planet.compute()
    planet_ephem = ephem.constellation(planet)
    update.message.reply_text("Планета находится на небосклоне в созвездии {}.".format(planet_ephem[1]))


def wordcount(bot, update):
    message = update.message.text
    count = len(message.split()) - 1
    if count == 0:
        update.message.reply_text("Ваша строка пуста.")
    elif (int(count//10))!=1 and (int(count%10))==1:
        word = "слово"
    elif (int(count%10)) in range(2,5) \
            and count != 11 \
            and count != 12 \
            and count != 13 \
            and count != 14:
        word = "слова"
    elif count > 4:
        word = "слов"
    update.message.reply_text("В переданной фразе {} {}.".format(count, word))


def next_fool_moon(bot, update):
    date = datetime.today()
    ephem_date = ephem.next_full_moon(date)
    moon_date = datetime.strptime(str(ephem_date), '%Y/%m/%d %X')
    update.message.reply_text("Следующее полнолуние произойдет в {}.".format(moon_date.strftime('%A %d %B %Y %X')))

def send_spacex_picture(bot, update, user_data):
    spacex_list = glob('images/spacex*.jpeg')
    sapcex_pic = choice(spacex_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(sapcex_pic, 'rb'))

def main():
    mybot = Updater(settings.BOT_TOKEN, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    #dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", planet_info))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_fool_moon", next_fool_moon))
    dp.add_handler(CommandHandler("spacex", send_spacex_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()

main()

