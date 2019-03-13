import ephem
from random import choice
from datetime import datetime
from glob import glob
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')

import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = "Привет {}".format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard())
    # smile = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    # name = update["message"]["chat"]["first_name"]
    # text = "Привет, {}! {}".format(name, smile)
    # update.message.reply_text(text)



def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']


def talk_to_me(bot, update, user_data):
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
    else:
        word = settings.word_for_counter(count,'слово', 'слова', 'слов')
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

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
        ['Прислать ракету'],
        [contact_button, location_button]
    ], resize_keyboard=True
    )
    return my_keyboard

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово {}'.format(get_user_emo(user_data), reply_markup=get_keyboard()))


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово {}'.format(get_user_emo(user_data), reply_markup=get_keyboard()))


def main():
    mybot = Updater(settings.BOT_TOKEN)
    logging.info('Бот запускается...')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", planet_info))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_fool_moon", next_fool_moon))
    dp.add_handler(CommandHandler("spacex", send_spacex_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать ракету)$', send_spacex_picture, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()

