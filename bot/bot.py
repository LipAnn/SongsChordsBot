import sys
import logging
import asyncio
from os import getenv
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from pathlib import Path


load_dotenv(find_dotenv())
TOKEN = getenv('TELEGRAM_API_BOT_TOKEN')

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
logging.basicConfig(
    level=logging.INFO,
    stream=open('bot.log', 'w'),
    format="[%(asctime)s] %(levelname)s %(message)s"
)


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


async def main() -> None:
    await dp.start_polling(bot)


def start_bot() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    start_bot()
