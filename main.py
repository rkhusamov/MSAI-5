# This is a sample Python script.
# SQLAlchemy — создавать класс и наследовать их от классов этой библиотеки

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Объявление бота
import telebot
from telebot import types
import vars
from db_bot import Pair, Session, User, Cryptocurrency

bot = telebot.TeleBot(vars.BOT_TOKEN, parse_mode=None)

def user_exists(self):
    if self is not None:
        return True
    else:
        return False

session = Session()

# Команда /start и запрос имени для нового пользователя
@bot.message_handler(commands=['s'])
def send_welcome(message):
    print(message.chat.id)
    # - check users
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    print(db_user)
    if db_user is not None:
        bot.reply_to(message, f"Добро пожаловать, {db_user.name}!")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        itembtn = types.KeyboardButton('/c')
        markup.row(itembtn)
        bot.send_message(message.chat.id, f"Если хотите просмотреть список всех валют, то нажмите /c !", reply_markup=markup)
        # db_user.current_state = "no_need_name"
        print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}')
    else:
        bot.reply_to(message, "Добро пожаловать, как мне вас называть?")
        new_user = User()
        new_user.chat_id = message.chat.id
        new_user.current_state = "need_name"
        print(f'{new_user.id} ,{new_user.name} , {new_user.chat_id}, {new_user.current_state}')
        session.add(new_user)
    session.commit()


# Приветствие /curr, показать все пары крипты
@bot.message_handler(commands=['c'])
def show_currencies(message):
    print(message.chat.id)
    # - check users
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    currs = session.query(Cryptocurrency).all()
    print(currs)
    if currs is not None:
        if db_user is not None:
            name = db_user.name
            print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}')
        else:
            name = "уважаемый пользователь"
        bot.send_message(message.chat.id, f"Вот список валют, {name}!")
        # print all curr
        text_to_send = []
        for cur in currs:
            print(f'{cur.name}, {cur.id}')
            text_to_send.append(f'{cur.name}')
        # db_user.current_state = "no_need_name"
        print(text_to_send)
        bot.send_message(message.chat.id, ', '.join(text_to_send))
        # спрашиваем, хочет ли пользователь установить любимую валюту
        print(db_user)
        if db_user is not None:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            itembtnyes = types.KeyboardButton('Yes')
            itembtnno = types.KeyboardButton('No')
            markup.row(itembtnyes, itembtnno)
            bot.send_message(message.chat.id, f"{db_user.name}, установить любимую валюту?", reply_markup=markup)
            db_user.current_state = "check_fav_curr"
            print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}')
    else:
        bot.send_message(message.chat.id, "No cryptocurrencies")
    session.commit()


# Удаление из базы своего пользователя
@bot.message_handler(commands=['d'])
def user_removal(message):
    print(message.chat.id)
    # - check users
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    print(db_user)
    if db_user is not None:
        db_user.current_state = "need_check_user_removal"
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        itembtnyes = types.KeyboardButton('Yes')
        itembtnno = types.KeyboardButton('No')
        markup.row(itembtnyes, itembtnno)
        bot.send_message(message.chat.id, f"{db_user.name}, вы точно хотите удалить все свои данные?", reply_markup=markup)
        print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}')
    else:
        bot.reply_to(message, "Пользователя не суещствует")
    session.commit()


# Отвечаем на все сообщения в зависимости от current_state
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message.chat.id)
    if message.text in ("Hi", "hi", "Привет", "привет"):
        bot.send_message(message.from_user.id, "Hi, I'm a crypto bot!")
    # - check users
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    print(db_user)
    if db_user is not None:
        match db_user.current_state:
            case "need_name": # текст следующего сообщения записать в имя пользователя User.name
                db_user.current_state = ""
                db_user.name = message.text
                bot.send_message(message.chat.id, f"{db_user.name}, приятно познакомиться! Я Криптобот =)")
                print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}')
            case "check_fav_curr": # обработка ответа на вопрос, установить ли любимую валюту
                if message.text == "Yes":
                    bot.send_message(message.chat.id, "Введите название любимой валюты")
                    db_user.current_state = "need_set_fav_curr"
                else:
                    db_user.current_state = ""
                    bot.send_message(message.chat.id, "Понял, пока ничего менять не будем")
                print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}')
            case "need_set_fav_curr": # текст следующего сообщения установить как любимую валюту пользователья fav_currency
                db_user.current_state = ""
                curr_name = session.query(Cryptocurrency).filter(Cryptocurrency.name == message.text).distinct().first()
                print(curr_name)
                if curr_name is not None:
                    db_user.fav_currency = curr_name
                    print(db_user.fav_currency)
                    bot.send_message(message.chat.id, f"Любимая валюта {curr_name.name} установлена")
                else:
                    bot.send_message(message.chat.id, "Введите имя валюты из доступного списка")
                print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}, {db_user.fav_currency}')
            case "need_check_user_removal": # обработка ответа на вопрос, нужно ли удалять пользователя
                db_user.current_state = ""
                if message.text == "Yes":
                    session.delete(db_user)
                    bot.send_message(message.chat.id, "Ваши данные успешно удалены!")
                else:
                    bot.send_message(message.chat.id, "Рад, что вы с нами!")
                print(f'{db_user.id} ,{db_user.name} , {db_user.chat_id}, {db_user.current_state}')
            case _:
                bot.send_message(message.chat.id, "Пожалуйста, введите команду /start или /curr")
                print("Case in match code not found")
    else:
        new_user = User()
        new_user.chat_id = message.chat.id
        new_user.current_state = "begin"
        bot.send_message(message.chat.id, "Пожалуйста, введите команду /start или /curr")
        print(f'{new_user.id} ,{new_user.name} , {new_user.chat_id}, {new_user.current_state}')
    session.commit()





# Launch bot
bot.infinity_polling()

session.close()




'''
@bot.message_handler(func=lambda message: True)
def save_name(message):
    bot.reply_to(message, message.text)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     markup = types.ReplyKeyboardRemove(selective=False)
#     bot.reply_to(message, message.text, reply_markup=markup)







@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


# Спросить у пользователя имя по команде / name и подтвердить, что это имя корректно
@bot.message_handler(commands=['name'])
def send_welcome(message):
    bot.reply_to(message, "Текст при name")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Текст при старте")


# Handle all sent documents of type 'text/plain'.
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain',
                     content_types=['document'])
def command_handle_document(message):
    bot.send_message(message.chat.id, 'Document received, sir!')


# Handle all other messages.
@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document',
                                                               'text', 'location', 'contact', 'sticker'])
def default_command(message):
    bot.send_message(message.chat.id, "This is the default command handler.")



# @bot.message_handler(func=lambda message: True)
# def del_markup(message):
#     markup = types.ReplyKeyboardRemove(selective=False)
#     bot.send_message(message.chat.id, 'Привет', reply_markup=markup)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/ изменения тест2 ветка test 2 changesgit


# or add KeyboardButton one row at a time:
'''


