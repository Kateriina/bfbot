import logging
import sys
import datetime
import time
from array import array
from datetime import date

from aiogram import Bot, Dispatcher, executor, types
import mysql.connector
import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import link, hlink

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token="5305942373:AAHAairFXm4RtAnuHb4fKPbJJErpf5cTu1o")
dp = Dispatcher(bot)


def connect():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            port="3306",
            database="bonchfood"
        )
        return db
    except:
        sys.exit()





@dp.message_handler(lambda message: message.text and ('с' in message.text.lower()
                                                      or 'еще' in message.text.lower()
                                                      or 'меню' in message.text.lower()
                                                      or 'ещё' in message.text.lower()
                                                      or 'хочу' in message.text.lower()
                                                      or 'есть' in message.text.lower()
                                                      or 'жрать' in message.text.lower()
                                                      or 'дальше' in message.text.lower()
                                                      or 'next' in message.text.lower()
                                                      or 'покажи' in message.text.lower()
                                                      or 'спросить' in message.text.lower()
                                                      or 'информ' in message.text.lower()
                                                      #or 'menu' in message.text.lower()
                                                      or 'more' in message.text.lower()))
async def on_menu(message: types.Message):
    await button(message)


@dp.message_handler(commands=['start', 'старт'])
async def on_start(message: types.Message):
    await start_button(message)


@dp.message_handler(commands=['menu', 'меню'])
async def on_menu(message: types.Message):
    await button(message)

@dp.message_handler(lambda message: message.text and ('спасибо' in message.text.lower()
                                                      or 'спс' in message.text.lower()
                                                      or 'thank you' in message.text.lower()
                                                      or 'thanks' in message.text.lower()))
async def on_thanks(message: types.Message):
    await message.answer('Пожалуйста!')


@dp.message_handler(lambda message: message.text and ('hello' in message.text.lower()
                                                      or 'hi' in message.text.lower()
                                                      or 'привет' in message.text.lower()
                                                      or 'здарова' in message.text.lower()))
async def on_hello(message: types.Message):
    await message.answer('Здраствуйте! Здесь вы можете узнать меню.')


@dp.message_handler(lambda message: message.text  and ('bye' in message.text.lower()
                                                       or 'goodbye' in message.text.lower()
                                                       or 'пока' in message.text.lower()
                                                       or 'до свидания' in message.text.lower()
                                                       or 'бай' in message.text.lower()
                                                       or 'прощай' in message.text.lower()))
async def on_goodbye(message: types.Message):
    await message.answer('До скорой встречи! Ведь кушать хочется всегда.')


@dp.message_handler(lambda message: message.text)
async def onAnother(message: types.Message):
    await message.answer('Извините, мне вас не понять. Попробуйте спросить меня про меню.')
    print(message.text)


def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end

async def button(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton('Столовая 1', callback_data='canteen1')
    item2 = types.KeyboardButton('Столовая 2', callback_data='canteen2')
    item3 = types.KeyboardButton('Столовая 3', callback_data='canteen3')
    #is_work_time('10:00', '17:00') &
    print(date.today().weekday())
    #время работы столовых
    start1 = datetime.time(10, 0)
    end1 = datetime.time(17, 00)

    start2 = datetime.time(10, 0)
    end2 = datetime.time(15, 00)

    start3 = datetime.time(11, 0)
    end3 = datetime.time(15, 00)
    current = datetime.datetime.now().time()

    print(start1)
    print(start2)
    print(start3)

    if (time_in_range(start1, end1, current) and
            date.today().weekday() != 6):
        markup.add(item1)

    if (time_in_range(start2, end2, current) and
            date.today().weekday() != 5 and date.today().weekday() != 6):
        markup.add(item2)

    if (time_in_range(start3, end3, current) and
            date.today().weekday() != 5 and date.today().weekday() != 6):
        markup.add(item3)

    if markup.inline_keyboard != []:
        await message.answer('Выберите столовую:', reply_markup=markup)
    else:
        await message.answer('Извините, все столовые закрыты.')



async def start_button(message: types.Message):
    kb = [[types.KeyboardButton('Меню')],]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
        # input_field_placeholder="Выберите столовую"
    )
    await message.answer('Привет! Здесь вы можете узнать меню.', reply_markup=keyboard)


@dp.callback_query_handler(func=None)
async def callback(call: types.CallbackQuery):
    if call.message:
        if call.data == 'canteen1':
            await call.message.answer('<b>Меню столовой №1:</b>\n' + hlink('Маршрут', 'https://nav.sut.ru/?cab=k1-218'), disable_web_page_preview=True, parse_mode="HTML")
            await call.message.answer(await view(call.data), parse_mode='MarkdownV2')

        elif call.data == 'canteen2':
            await call.message.answer('<b>Меню столовой №2:</b>\n' + hlink('Маршрут', 'https://nav.sut.ru/?cab=k1-326'),
                                      disable_web_page_preview=True, parse_mode="HTML")
            await call.message.answer(await view(call.data), parse_mode='MarkdownV2')


        elif call.data == 'canteen3':
            db_task = asyncio.create_task(view(call.data))
            answer1_task = asyncio.create_task(answer_message(call.message))
            #print('1')
            await answer1_task

            await call.message.answer(await db_task, parse_mode='MarkdownV2')

    await bot.answer_callback_query(call.id) #for remove clock icon
    await call.message.delete()


async def answer_message(message):
    await message.answer('<b>Меню столовой №3:</b>\n' + hlink('Маршрут', 'https://nav.sut.ru/?cab=k2-321'),
                              disable_web_page_preview=True, parse_mode="HTML")
    #print('2')


async def view_db(cant, num):
    #print('start DB')
    db = connect()
    cursor = db.cursor()
    cursor.execute("select type from dish_type where id = " + str(num))
    name = '\n'.join(cursor.fetchall()[0])
    #print(name)

    cursor.execute("select d.name from " + str(
        cant) + " c join dishes d on c.dish_id = d.id join dish_type dt on d.type_id = dt.id where dt.id = " + str(num))
    menu = cursor.fetchall()

    # for n in range(1, 6):как асинхронно работать с тг и бд
    #     print('DB wait', n)
    #     await asyncio.sleep(1)
    my_list = []
    for dish in menu:
        my_list.append(dish[0])
    my_str = '\n'.join(my_list)
    #print('end DB')
    if my_str == "":
        new_str = ""
    else:
        new_str = "*" +name + "*" + ":\n" + my_str + "\n\n"
    return new_str


async def view(cant):
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT MAX(id) FROM dish_type")
    max_id = cursor.fetchall()[0][0]
    global menu_str
    menu_str = ""
    for n in range(1, max_id + 1):
        # global menu_str
        menu_str += await view_db(cant, n)

    return menu_str


if __name__ == '__main__':
    executor.start_polling(dp)


#
# *bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~