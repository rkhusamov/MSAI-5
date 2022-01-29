# SQLAlchemy — создавать класс и наследовать их от классов этой библиотеки
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Объявление бота
import telebot
from telebot import types
import vars
from db_bot import Pair, Session, User, Cryptocurrency

bot = telebot.TeleBot(vars.BOT_TOKEN, parse_mode=None)
session = Session()

# Команда /start и запрос имени для нового пользователя
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # get user
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    if db_user is not None: # if user exists
        bot.reply_to(message, f"Добро пожаловать, {db_user.name}!")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('/curr')
        itembtn2 = types.KeyboardButton('Skip')
        markup.row(itembtn1, itembtn2)
        bot.send_message(message.chat.id, f"Если хотите просмотреть список всех валют, то нажмите /curr !", reply_markup=markup)
    else: # if no user exists
        bot.reply_to(message, "Добро пожаловать, как мне вас называть?")
        new_user = User()
        new_user.chat_id = message.chat.id
        new_user.current_state = "need_name"
        session.add(new_user)
    session.commit()


# Команда /curr, показать все пары крипты
@bot.message_handler(commands=['curr'])
def show_currencies(message):
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    currs = session.query(Cryptocurrency).all()
    if (db_user is not None) and (db_user.fav_currency is not None):
        bot.send_message(message.chat.id, f"Ваша любимая валюта - {db_user.fav_currency.name}")
    if currs is not None:
        if db_user is not None:
            name = db_user.name
        else:
            name = "Уважаемый пользователь"
        bot.send_message(message.chat.id, f"{name}, вот список валют:")
        text_to_send = []
        for cur in currs:
            text_to_send.append(f'{cur.name}')
        bot.send_message(message.chat.id, ', '.join(text_to_send))
        # спрашиваем, хочет ли пользователь установить любимую валюту
        if db_user is not None:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            itembtnyes = types.KeyboardButton('Yes')
            itembtnno = types.KeyboardButton('No')
            markup.row(itembtnyes, itembtnno)
            bot.send_message(message.chat.id, f"Установить любимую валюту?", reply_markup=markup)
            db_user.current_state = "check_fav_curr"
    else:
        bot.send_message(message.chat.id, "No cryptocurrencies")
    session.commit()


# Удаление из базы своего пользователя командой /d
@bot.message_handler(commands=['d'])
def user_removal(message):
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    if db_user is not None:
        db_user.current_state = "need_check_user_removal"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        itembtnyes = types.KeyboardButton('Yes')
        itembtnno = types.KeyboardButton('No')
        markup.row(itembtnyes, itembtnno)
        bot.send_message(message.chat.id, f"{db_user.name}, вы точно хотите удалить все свои данные?", reply_markup=markup)
    else:
        bot.reply_to(message, "Пользователя не суещствует")
    session.commit()


# Обработчик всех сообщений в зависимости от current_state
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text in ("Hi", "hi", "Привет", "привет"):
        bot.send_message(message.from_user.id, "Привет, я — Криптобот =)")
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    if db_user is not None:
        match db_user.current_state:
            case "need_name": # текст следующего сообщения записать в имя пользователя User.name
                db_user.current_state = ""
                db_user.name = message.text
                bot.send_message(message.chat.id, f"{db_user.name}, приятно познакомиться! Я Криптобот =)")
                bot.send_message(message.chat.id, "Если хотите просмотреть список всех валют, то нажмите /curr !")
            case "check_fav_curr": # обработка ответа на вопрос, установить ли любимую валюту
                if message.text == "Yes":
                    bot.send_message(message.chat.id, "Введите название любимой валюты")
                    db_user.current_state = "need_set_fav_curr"
                else:
                    db_user.current_state = ""
                    bot.send_message(message.chat.id, "Понял, пока ничего менять не будем")
            case "need_set_fav_curr": # текст следующего сообщения установить как любимую валюту пользователья fav_currency
                db_user.current_state = ""
                curr_name = session.query(Cryptocurrency).filter(Cryptocurrency.name == message.text).distinct().first()
                if curr_name is not None:
                    db_user.fav_currency = curr_name
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    itembtn = types.KeyboardButton('Wow!')
                    markup.row(itembtn)
                    bot.send_message(message.chat.id, f"Любимая валюта {curr_name.name} установлена", reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, "У меня нет такой валюты. Попробуйте ещё раз командой /curr")
            case "need_check_user_removal": # обработка ответа на вопрос, нужно ли удалять пользователя
                db_user.current_state = ""
                if message.text == "Yes":
                    session.delete(db_user)
                    bot.send_message(message.chat.id, "Ваши данные успешно удалены!")
                else:
                    bot.send_message(message.chat.id, "Рад, что вы с нами!")
            case _:
                bot.send_message(message.chat.id, "Пожалуйста, введите команду /start или /curr")
    else:
        new_user = User()
        new_user.chat_id = message.chat.id
        new_user.current_state = "begin"
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Пожалуйста, введите команду /start или /curr", reply_markup=markup)
    session.commit()

# Launch bot
bot.infinity_polling()

session.close()
