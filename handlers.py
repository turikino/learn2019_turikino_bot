import ephem
from datetime import datetime
from glob import glob
from utils import *
import settings


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = "Привет {}".format(emo)
    update.message.reply_text(text, reply_markup=get_keyboard())
    # smile = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    # name = update["message"]["chat"]["first_name"]
    # text = "Привет, {}! {}".format(name, smile)
    # update.message.reply_text(text)


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


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово {}'.format(get_user_emo(user_data), reply_markup=get_keyboard()))


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово {}'.format(get_user_emo(user_data), reply_markup=get_keyboard()))