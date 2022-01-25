# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Объявление бота
import telebot

bot = telebot.TeleBot("ТОКЕН",parse_mode=None)
# You can set parse_mode by default. HTML or MARKDOWN


# TODO удалить токен перед заливкой онлайн


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Текст при старте")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()

tempp = 0


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}', tempp)  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/ изменения тест2 ветка test 2 changesgit
