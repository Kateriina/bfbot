import telebot

bot = telebot.TeleBot("5625802533:AAHko3i9I-lyYB-WctFer1HsmMCgSVGi-_A")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '<b>Добро пожаловать!</b>', parse_mode='html')


bot.polling(none_stop=True)