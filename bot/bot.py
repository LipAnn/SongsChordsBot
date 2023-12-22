import io
import logging
import asyncio
from os import getenv
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InputFile, MediaGroup
from aiogram.types.input_file import FSInputFile
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    stream=open('./bot.log', 'w'),
    format="[%(asctime)s] %(levelname)s %(message)s"
)

from backend import *
backend = Backend()

load_dotenv(find_dotenv())
TOKEN = getenv('TELEGRAM_API_BOT_TOKEN')

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    start_info = "/n".join(
        "Добро пожаловать! Данный бот умеет распознавать текст и аккорды присланной Вами песни.",
        "Качество распознавания зависит от качества аудиозаписи.",
        "Максимальное время получаемого аудиофайла - 5 минут.",
        "Можно присылать как и файл с аудиозаписью, так и голосовое сообщение."
        "Получить помощь можно по команде /help",
        "Играйте с удовольствием! :)"
    )
    await message.answer(start_info)


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    help_info = "/n".join(
        "Качество распознавания зависит от качества аудиозаписи.",
        "Максимальное время получаемого аудиофайла - 5 минут.",
        "Можно присылать как и файл с аудиозаписью, так и голосовое сообщение."
    )
    await message.answer(help_info)


async def query_txt_from_backend(file_id) -> None:
    return backend.query_txt(audio=f'voice/voice_{file_id}.mp3')


@dp.message(F.content_type.in_({'audio', 'voice'}))
async def voice_handler(message: Message) -> None:
    file_id = (message.audio.file_id if message.audio else message.voice.file_id)
    file = await bot.get_file(file_id)
    file_duraion = (message.audio.duration if message.audio else message.voice.duration)
    if file_duraion > 5*60:
        await message.answer(
            f'Файл с музыкой слишком большой!\nОтправьте, пожалуйста, файл длительностью не более 5 минут'
        )
        logging.info(f'Get voice with a size exceeding the maximum from user id={message.from_user.id}')
        return
    
    file_path = file.file_path
    
    file_on_disk = Path(f'./voice/voice_{file_id}.mp3')
    await bot.download_file(file_path, file_on_disk)
    await message.answer(
        f'Я загрузил Вашу музыку на сервер, ожидайте результат.'
    )
    logging.info(f'Get voice from user id={message.from_user.id}. File id={file_id}')
    
    text = await query_txt_from_backend(file_id)
    with open(f'./text/txt_{file_id}.txt', "wb") as f:
        f.write(text.getbuffer())
    
    file_on_disk.unlink()
   
    # Send answer in several formats
    media_group = MediaGroup()

    media_group.attach_document(FSInputFile(f'./text/txt_{file_id}.txt'))
    media_group.attach_document(FSInputFile(f'./text/pdf_{file_id}.pdf'))
    media_group.attach_photo(FSInputFile(f'text/jpg_{file_id}.jpg'))

    await bot.send_media_group(media=media_group, reply_to_message_id=message.message_id)

    Path(f'./text/txt_{file_id}.txt').unlink()
    Path(f'./text/pdf_{file_id}.pdf').unlink()
    Path(f'./text/jpg_{file_id}.jpg').unlink()


@dp.message()
async def unknown_format_handler(message: Message):
    await message.answer(
        f'Данный формат файла я пока не умею обрабатывать 😢\nЯ понимаю только Голосовые сообщения и сообщения формата Аудио'
    )


async def main() -> None:
    await dp.start_polling(bot)


def start_bot() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    start_bot()
