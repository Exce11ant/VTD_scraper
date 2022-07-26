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

conn = sqlite3.connect('vinted_db_pl.db')
cur = conn.cursor()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Выбери пункт !", reply_markup=keyboard)

# После начала работы, каждые 30 секунд бот будет выдавать 10 последних обьявлений, если объявление уже было,
# он его пропустит.
@dp.message_handler(Text(equals="Начать Работу"))
async def get_last_ads(message: types.Message):
    conn = sqlite3.connect('vinted_db.db')
    cur = conn.cursor()
    while True:
        select_sql = "SELECT * FROM vinted_page_users ORDER BY id DESC LIMIT 10;"
        results = cur.execute(select_sql)
        for row in results:
            ids = int(row[1])
            link = str(row[3])
            print(link, ids)
            info = f"{ids}\n{link}"
            if ids not in ids_trash:
                ids_trash.append(ids)
                await message.bot.send_message(message.from_user.id, info)
            else:
                print("пока что все!")
        time.sleep(30)


if __name__ == '__main__':
    executor.start_polling(dp)
