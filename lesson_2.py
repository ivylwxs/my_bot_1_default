import asyncio
import logging
import random
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())


class GameState(StatesGroup):
    guessing = State()


@dp.message(CommandStart())  # Fine State Machine
async def command_start_handler(message: Message, state: FSMContext) -> None:
    guess_number = random.randint(1, 100)
    await state.set_state(GameState.guessing)
    await state.update_data(guess_number=guess_number, attempt=0)
    await message.answer('Men 1 dan 100 oralig`ida bir son o`yladim.\nUni toping: ?')


@dp.message(GameState.guessing)
async def loop_state(message: Message, state: FSMContext):
    state_data = await state.get_data()
    guess_number = state_data.get('guess_number')
    text = message.text
    if text == 'help':
        await message.answer(f"Men {guess_number} sonini o'ylagandim, vaaa 😊")
        await state.clear()
        return
    if not text.isdigit():
        await message.answer('Faqat 1 dan 100 gacha oraliqda son kiriting: ')
        return
    if int(text) > guess_number:
        attempt = state_data.get('attempt', 0) + 1
        await state.update_data(attempt=attempt)
        await message.answer(f'Men o`ylagan son {text} dan kichikroq')
        return
    elif int(text) < guess_number:
        attempt = state_data.get('attempt', 0) + 1
        await state.update_data(attempt=attempt)
        await message.answer(f'Men o`ylagan son {text} dan kattaroq')
        return

    attempt = state_data.get('attempt') + 1
    await message.answer(f'Tabriklaymiz siz {attempt} urinishda topdingiz! 🎉')
    await state.clear()


@dp.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())