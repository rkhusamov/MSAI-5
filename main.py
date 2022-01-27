# This is a sample Python script.
# SQLAlchemy — создавать класс и наследовать их от классов этой библиотеки

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Объявление бота
import telebot
from telebot import types
import vars

bot = telebot.TeleBot(vars.BOT_TOKEN, parse_mode=None)

# You can set parse_mode by default. HTML or MARKDOWN
# TODO удалить токен перед заливкой онлайн


# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # create user if no exist
    user.state = "expecting_name"
    bot.reply_to(message, "Добро пожаловать, как мне вас называть?")
    print(message.chat.id)


@bot.message_handler(func=lambda message: True)
def save_name(message):
    bot.reply_to(message, message.text)


# or add KeyboardButton one row at a time:
# markup = types.ReplyKeyboardMarkup()
# itembtna = types.KeyboardButton('a')
# itembtnv = types.KeyboardButton('v')
# itembtnc = types.KeyboardButton('c')
# itembtnd = types.KeyboardButton('d')
# itembtne = types.KeyboardButton('e')
# markup.row(itembtna, itembtnv)
# markup.row(itembtnc, itembtnd, itembtne)
#    bot.reply_to(message, message.text, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


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


bot.infinity_polling()

tempp = 0


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}', tempp)  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/ изменения тест2 ветка test 2 changesgit
