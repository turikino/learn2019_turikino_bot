from handlers import *
import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')

import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )





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

