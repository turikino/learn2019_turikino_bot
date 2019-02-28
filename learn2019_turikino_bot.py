from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



PROXY = {'proxy_url': 'socks5://t2.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    name = update["message"]["chat"]["first_name"]
    update.message.reply_text("Привет, {}!".format(name))
    print(update)

def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def ephem_info(bot, update):
    user_text = update.message.text
    planet_name = user_text.split()[-1]
    print(planet_name)


def main():
    mybot = Updater(settings.BOT_TOKEN, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(MessageHandler("planet", ephem_info))
    mybot.start_polling()
    mybot.idle()

main()

