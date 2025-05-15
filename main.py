import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!")


@dp.message(F.text == 'getMe')
async def get_me(message: Message):
    chat_id = message.chat.id
    fullname = message.from_user.full_name
    text = message.text
    username = message.from_user.username
    await message.answer(f'Custom getME! \n\n'
                         f'chat id: {chat_id}\n'
                         f'fullname: {fullname}\n'
                         f'text: {text}\n'
                         f'username: @{username}')


# function - birthday, age,

@dp.message(F.text.regexp(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'))
async def hadnle_email(message: Message):
    await message.answer('Siz email yubordingiz!')


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Yana urinib ko'ring!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())