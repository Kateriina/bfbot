import telebot
import mysql.connector

from telebot import types
bot = telebot.TeleBot("5625802533:AAHko3i9I-lyYB-WctFer1HsmMCgSVGi-_A")


# def __init__(self):
#     # подключение к базе данных
#     self.connection = mysql.connect(database='bonchfood.db',
#                                        user='root',
#                                        password='root',
#                                        host='localhost',
#                                        port='3306')
#     self.cursor = self.connection.cursor()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    port="3306",
    database="bonchfood"
)

#cursor = db.cursor()
#cursor.execute("SHOW TABLES")

#cursor.execute("SHOW DATABASES")

#for x in cursor:
#    print(x)


#for x in cursor:
#    print(x)
# cursor.execute("SELECT dish_name as Блюдо from canteen1")
#
# menu = cursor.fetchall()
# my_list = []
# for dish in menu:
#     my_list.append(' | '.join(dish))
# my_str = '\n'.join(my_list)

#menu=cursor.fetchmany()
#for dish in menu:
#    req = dish
#    print(dish)

@bot.message_handler(commands=['start'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Столовая 1', callback_data='canteen1')
    item2 = types.InlineKeyboardButton('Столовая 2', callback_data='canteen2')
    item3 = types.InlineKeyboardButton('Столовая 3', callback_data='canteen3')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'Привет! Здесь вы можете узнать меню.')
    bot.send_message(message.chat.id, 'Выберите столовую:', reply_markup=markup)
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'canteen1':
            bot.send_message(call.message.chat.id, 'Меню столовой №1:')
            bot.send_message(call.message.chat.id, view(call.data))

        elif call.data == 'canteen2':
            bot.send_message(call.message.chat.id, 'Меню столовой №2:')
            bot.send_message(call.message.chat.id, view(call.data))
        elif call.data == 'canteen3':
            bot.send_message(call.message.chat.id, 'Меню столовой №3:')
            bot.send_message(call.message.chat.id, view(call.data))

def view(cant):
    cursor = db.cursor()
    cursor.execute("SELECT dish_name from " + str(cant))
    menu = cursor.fetchall()
    my_list = []
    for dish in menu:
        my_list.append(' | '.join(dish))
    my_str = '\n'.join(my_list)
    return my_str

bot.polling(none_stop=True)



# def view():
#     cursor = db.cursor()
#     sql = "SELECT dish_name as Блюдо from canteen1"
#     try:
#         cursor.execute(sql)
#         results = cursor.fetchall()
#
#         if len(results) > 0:
#             output = ''
#             for row in results:
#
#                output = row
#                 print(row)
#         else:
#             output = 'No word in my dic'
#     except:
#         output = 'error'
#     return output
#
# def view1(cant):
#     cursor = db.cursor()
#     cursor.execute("SELECT dish_name from " + str(cant))
#     menu = cursor.fetchall()
#     my_list = []
#     for dish in menu:
#         my_list.append(' | '.join(dish))
#     my_str = '\n'.join(my_list)
#     return my_str
#
# def view2():
#     cursor = db.cursor()
#     cursor.execute("SELECT dish_name from canteen2")
#     menu = cursor.fetchall()
#     my_list = []
#     for dish in menu:
#         my_list.append(' | '.join(dish))
#     my_str = '\n'.join(my_list)
#     return my_str
#
# def view3():
#     cursor = db.cursor()
#     cursor.execute("SELECT dish_name from canteen3")
#     menu = cursor.fetchall()
#     my_list = []
#     for dish in menu:
#         my_list.append(' | '.join(dish))
#     my_str = '\n'.join(my_list)
#     return my_str