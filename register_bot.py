import asyncio
import logging
import random
import sys
import psycopg2
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())

def get_connection():
    return psycopg2.connect(
        dbname= "postgres",
        user="postgres",
        password="000",
        host="localhost",
        port=5432
    )

class Register(StatesGroup):
    waiting = State()

@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM followers WHERE user_id = %s", (message.from_user.id,))
    follower = cur.fetchone()

    if follower:
        await message.answer("You are already registered.")
        conn.close()
        return

    await state.set_state(Register.waiting)
    await message.answer("Enter your name:")
    conn.close()

@dp.message(Register.waiting)
async def register_name(message: Message, state: FSMContext):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM followers WHERE user_id = %s", (message.from_user.id,))
    follower = cur.fetchone()

    if follower:
        await message.answer("You're already in the system.")
        await state.clear()
        conn.close()
        return

    name = message.text

    cur.execute("INSERT INTO followers (user_id, name) VALUES (%s, %s)", (message.from_user.id, name))
    conn.commit()
    conn.close()

    await message.answer(f"Thank you {name}, you are now registered!")
    await state.clear()


@dp.message(Command("followers"))
async def count_followers(message: Message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM followers")
    count = cur.fetchone()[0]
    conn.close()

    await message.answer(f"Total followers: {count}")


@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())







