import sys
import logging
import asyncio
from os import getenv
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ContentType

load_dotenv(find_dotenv())
TOKEN = getenv('TELEGRAM_API_BOT_TOKEN')

dp = Dispatcher()


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f'Какая-то информация о боте \nПолучить помощь по команде /help'
    )
    
@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        f'Какая-то помощь Вам тут'
    )

@dp.message()
async def voice_handler(message: Message) -> None:
    voice = message.voice
    print(voice.duration)
    await message.answer_audio(audio=voice)
 
async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

def start_bot() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

if __name__ == "__main__":
    start_bot()
