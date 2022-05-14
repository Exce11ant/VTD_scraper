import sqlite3
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)
ids_trash = []

conn = sqlite3.connect('vinted_db.db')
cur = conn.cursor()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # user_id = ["Дарова"+message.chat.id+"Успехов тебе"]
    # cur.execute("INSERT OR IGNORE INTO")
    start_buttons = ["Начать Работу"]
    # starts_buttons = ["Жуля"]
    # starts_buttons = ["Владичек"]
    # starts_buttons = ["SonyЭрикSan"]
    # starts_buttons = ["Рыжая Чигивара"]
    # starts_buttons = ["Свитdick"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Выбери пункт !", reply_markup=keyboard)


@dp.message_handler(Text(equals="Начать Работу"))
# async def get_last_ads(message: types.Message):
async def get_last_ads(message: types.Message):
    conn = sqlite3.connect('vinted_db.db')
    cur = conn.cursor()
    # select_last_rowid = "SELECT ROWID, * FROM vinted_page_users LIMIT 1 OFFSET(SELECT COUNT(*)FROM  vinted_page_users)-1"
    while True:
        select_sql = "SELECT * FROM vinted_page_users ORDER BY id DESC LIMIT 10;"
        results = cur.execute(select_sql)
        for row in results:
            ids = int(row[1])
            link = str(row[2])
            print(link, ids)
            info = f"{ids}\n{link}"
            if ids not in ids_trash:
                ids_trash.append(ids)
                await message.bot.send_message(message.from_user.id, info)
            else:
                print("пока что все!")
                # await message.bot.send_message(message.chat.id, "пока что все!")
        time.sleep(120)

# async def get_last_ads(message: types.Message):
#     conn = sqlite3.connect('vinted_db.db')
#     cur = conn.cursor()
#     select_sql = "SELECT * FROM vinted_page_users ORDER BY id DESC LIMIT 1;"
#     # cur.execute(select_sql)
#     results = cur.execute(select_sql)
#     for row in results:
#         ids = int(row[1])
#         link = str(row[2])
#         print(link, ids)
#         info = f"{ids}\n{link}"
#         if ids not in ids_trash:
#             ids_trash.append(ids)
#             await message.bot.send_message(message.from_user.id, info)
#     else:
#         print("пока что все!")
#         await message.bot.send_message(message.chat.id, "пока что все!")


if __name__ == '__main__':
    executor.start_polling(dp)
