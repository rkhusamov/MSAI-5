# SQLAlchemy — создавать класс и наследовать их от классов этой библиотеки
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Объявление бота
import telebot
from telebot import types
import vars
from db_bot import Pair, Session, User, Cryptocurrency, Сonsensus, Adoption

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


# Выбор криптовалюты пользователем /сhoose
@bot.message_handler(commands=['choose'])
def choose_crypt(message):
    db_user = session.query(User).filter(User.chat_id == message.chat.id).first()
    if db_user is not None:
        db_user.current_state = "need_save_consensus"
        bot.send_message(message.chat.id, f"{db_user.name}, I could help you to choose a Crypto!")
        bot.send_message(message.chat.id, "We have these types of consensus:")
        consensuses = session.query(Сonsensus).all()
        text_to_send = []
        for cons in consensuses:
            text_to_send.append(f'{cons.name}')
        bot.send_message(message.chat.id, ', '.join(text_to_send))
        bot.send_message(message.chat.id, "Please, type a consensus name:")
        # спрашиваем, хочет ли пользователь установить любимую валюту
    else:
        bot.send_message(message, "Please, create a user with /start command")
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
                    markup = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, "Понял, пока ничего менять не будем", reply_markup=markup)
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
            case "need_save_consensus":  # обработка ответа по выбору консенсуса
                db_user.current_state = ""
                consensuses = session.query(Сonsensus).all()
                for cons in consensuses:
                    if message.text == cons.name:
                        bot.send_message(message.chat.id, f"Cool! I remember the consensus {message.text}")
                        db_user.consensus_id = cons.id
                        db_user.current_state = "need_ask_smart_contract"
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        itembtnyes = types.KeyboardButton('Yes')
                        itembtnno = types.KeyboardButton('No')
                        markup.row(itembtnyes, itembtnno)
                        bot.send_message(message.chat.id, "Go to smart contract choosing?", reply_markup=markup)
                        break
                else:
                    db_user.current_state = ""
                    bot.send_message(message.chat.id, "Sorry, invalid consensus name! Use /choose for start again")
            case "need_ask_smart_contract":  # обработка ответа на вопрос, нужно ли переходить к шагу по Смарт_контракткам
                if message.text == "Yes":
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    itembtnyes = types.KeyboardButton('Yes')
                    itembtnno = types.KeyboardButton('No')
                    markup.row(itembtnyes, itembtnno)
                    bot.send_message(message.chat.id, "Do you need smart contract to be in Crypto?", reply_markup=markup)
                    db_user.current_state = "need_set_smart_contract"
                else:
                    db_user.current_state = ""
                    markup = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, "Ok, here is the list of Crypto", reply_markup=markup)
                    currs = session.query(Cryptocurrency).filter(Cryptocurrency.consensus_id == db_user.consensus_id).all()
                    text_to_send = []
                    for cur in currs:
                        text_to_send.append(f'{cur.name}')
                    bot.send_message(message.chat.id, ', '.join(text_to_send))
                    bot.send_message(message.chat.id, "Use /start, /curr or /choose to interact with me!")
            case "need_set_smart_contract":  # обработка ответа по выбору cмарт-контракта
                db_user.current_state = ""
                if message.text == "Yes":
                    db_user.has_smart_contract = True
                    db_user.current_state = "need_ask_adoption"
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    itembtnyes = types.KeyboardButton('Yes')
                    itembtnno = types.KeyboardButton('No')
                    markup.row(itembtnyes, itembtnno)
                    bot.send_message(message.chat.id, "Ok, you need smart contract. Go to adoption step in choosing Crypto?", reply_markup=markup)
                elif message.text == "No":
                    db_user.has_smart_contract = False
                    db_user.current_state = "need_ask_adoption"
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    itembtnyes = types.KeyboardButton('Yes')
                    itembtnno = types.KeyboardButton('No')
                    markup.row(itembtnyes, itembtnno)
                    bot.send_message(message.chat.id, "Ok, you don't need smart contract. Go to adoption step in choosing Crypto?", reply_markup=markup)
                else:
                    db_user.current_state = ""
                    markup = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, f"Don't get your reply, but this is your list with choosed consensus", reply_markup=markup)
                    currs = session.query(Cryptocurrency).filter(Cryptocurrency.consensus_id == db_user.consensus_id).all()
                    text_to_send = []
                    for cur in currs:
                        text_to_send.append(f'{cur.name}')
                    bot.send_message(message.chat.id, ', '.join(text_to_send))
                    bot.send_message(message.chat.id, "Use /start, /curr or /choose to interact with me!")
            case "need_ask_adoption":  # вопрос по выбору распространенности
                if message.text == "Yes":
                    db_user.current_state = "need_set_adoption"
                    bot.send_message(message.chat.id, "We have these types of adoption:")
                    adoptions = session.query(Adoption).all()
                    text_to_send = []
                    for ads in adoptions:
                        text_to_send.append(f'{ads.name}')
                    bot.send_message(message.chat.id, ', '.join(text_to_send))
                    bot.send_message(message.chat.id, "Please, type a adoption level:")
                else:
                    db_user.current_state = ""
                    markup = types.ReplyKeyboardRemove()
                    bot.send_message(message.chat.id, "Ok, here is the list of Crypto", reply_markup=markup)
                    currs = session.query(Cryptocurrency).filter(Cryptocurrency.consensus_id == db_user.consensus_id).all()
                    text_to_send = []
                    text_to_send.append("Here is a list of Crypto matching your criteria:")
                    print(text_to_send)
                    for cur in currs:
                        text_to_send.append(f'{cur.name}')
                    bot.send_message(message.chat.id, ', '.join(text_to_send))
                    bot.send_message(message.chat.id, "Use /start, /curr or /choose to interact with me!")
            case "need_set_adoption":  # обработка ответа по выбору распространенности
                db_user.current_state = ""
                adoptions = session.query(Adoption).all()
                db_user.adoption_id = None
                for ads in adoptions:
                    if message.text == ads.name:
                        bot.send_message(message.chat.id, f"Cool! I remember the adoption {message.text}. Let me see what i have found.")
                        db_user.adoption_id = ads.id
                        break
                else:
                    db_user.current_state = ""
                    bot.send_message(message.chat.id, "Sorry, invalid adoption name! Use /choose for start again")
                text_to_send = []
                currs_count = session.query(Cryptocurrency).filter(Cryptocurrency.consensus_id == db_user.consensus_id, Cryptocurrency.adoption_id == db_user.adoption_id, Cryptocurrency.has_smart_contract == db_user.has_smart_contract).count()
                if currs_count > 0:
                    currs = session.query(Cryptocurrency).filter(Cryptocurrency.consensus_id == db_user.consensus_id,
                                                                 Cryptocurrency.adoption_id == db_user.adoption_id,
                                                                 Cryptocurrency.has_smart_contract == db_user.has_smart_contract).all()
                    for cur in currs:
                        text_to_send.append(f'{cur.name}')
                    bot.send_message(message.chat.id, ', '.join(text_to_send))
                    bot.send_message(message.chat.id, "Please, use /start, /curr or /choose")
                else:
                    bot.send_message(message.chat.id, 'No Crypto match your criteria. Use /choose for start again')


            case _:
                bot.send_message(message.chat.id, "Please, use /start, /curr or /choose")
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
