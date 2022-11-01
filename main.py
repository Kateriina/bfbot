import logging
from aiogram import Bot, Dispatcher, executor, types
import mysql.connector
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token="5625802533:AAHko3i9I-lyYB-WctFer1HsmMCgSVGi-_A")
dp = Dispatcher(bot)



db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    port="3306",
    database="bonchfood"
)


@dp.message_handler(lambda message: message.text and 'меню' in message.text.lower())
async def onMenu(message: types.Message):
    await button(message)

@dp.message_handler(commands=['start','меню'])
async def onStart(message: types.Message):
    await button(message)


async def button(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.KeyboardButton('Столовая 1', callback_data='canteen1')
    item2 = types.KeyboardButton('Столовая 2', callback_data='canteen2')
    item3 = types.KeyboardButton('Столовая 3', callback_data='canteen3')
    markup.add(item1, item2, item3)

    # await bot.send_message(message.chat.id, 'Привет! Здесь вы можете узнать меню.')
    await message.answer('Выберите столовую:', reply_markup=markup)


@dp.callback_query_handler(func=None)
async def callback(call: types.CallbackQuery):
    if call.message:
        if call.data == 'canteen1':
            await call.message.answer('*Меню столовой №1:*',  parse_mode='MarkdownV2')
            await call.message.answer(await view(call.data))

        elif call.data == 'canteen2':
            await call.message.answer('*Меню столовой №2:*',  parse_mode='MarkdownV2')
            await call.message.answer(await view(call.data))

        elif call.data == 'canteen3':
            db_task = asyncio.create_task(view(call.data))
            answer1_task = asyncio.create_task(answer_message(call.message))
            print('1')
            await answer1_task

            await call.message.answer(await db_task)

    await bot.answer_callback_query(call.id) #for remove clock icon
    await call.message.delete()


async def answer_message(message):
    await message.answer('*Меню столовой №3:*', parse_mode='MarkdownV2')
    print('2')


async def view_db(cant, num):


async def view(cant):
    print('start DB')
    cursor = db.cursor()
    #cursor.execute("SELECT dish_name from " + str(cant))
    cursor.execute("select d.name from " + str(cant) + "c join dishes d on c.dish_id = d.id join dish_type dt on d.type_id = dt.id where dt.id = 1")
    menu = cursor.fetchall()
    # for n in range(1, 6):как асинхронно работать с тг и бд
    #     print('DB wait', n)
    #     await asyncio.sleep(1)
    my_list = []
    for dish in menu:
        my_list.append(dish[0])
    my_str = '\n'.join(my_list)
    print('end DB')
    return my_str


if __name__ == '__main__':
    executor.start_polling(dp)

#
# *bold \*text*
# _italic \*text_
# __underline__
# ~strikethrough~