import io
import logging
import asyncio
from os import getenv
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InputFile
from aiogram.types.input_file import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from pathlib import Path
from fpdf import FPDF
from pdf2image import convert_from_path

logging.basicConfig(
    level=logging.INFO,
    stream=open('./bot.log', 'w'),
    format="[%(asctime)s] %(levelname)s %(message)s"
)

MAX_SONG_LENGTH = 5  # 5 minutes

from backend import *
backend = Backend()

load_dotenv(find_dotenv())
TOKEN = getenv('TELEGRAM_API_BOT_TOKEN')

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    start_info = (
        "Добро пожаловать! Данный бот умеет распознавать текст и аккорды присланной Вами песни.\n"
        "Качество распознавания зависит от качества аудиозаписи.\n"
        f"Максимальное время получаемого аудиофайла - {MAX_SONG_LENGTH} мин.\n"
        "Можно присылать как и файл с аудиозаписью, так и голосовое сообщение.\n"
        "Получить помощь можно по команде /help\n"
        "Играйте с удовольствием! :)\n"
    )
    await message.answer(start_info)


@dp.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    help_info = (
        "Качество распознавания зависит от качества аудиозаписи.\n"
        f"Максимальное время получаемого аудиофайла - {MAX_SONG_LENGTH} мин.\n"
        "Можно присылать как и файл с аудиозаписью, так и голосовое сообщение.\n"
    )
    await message.answer(help_info)


async def query_txt_from_backend(file_id) -> io.BytesIO:
    result = await asyncio.to_thread(backend.query_txt, audio=f'voice/voice_{file_id}.mp3')
    return result


async def dump_str_to_txt(text: str, file_path: str) -> None:
    with open(file_path, "w") as f:
        f.write(text)


async def dump_txt_to_pdf(text: str, file_path: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', './dejavu-fonts-ttf-2.37/ttf/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 8)
    for x in text.split('\n'):
        pdf.cell(200, 5, txt=x, ln=1)
    pdf.output(file_path) 


async def dump_pdf_to_jpgs(pdf_path, file_path: str) -> int:
    pass


@dp.message(F.content_type.in_({'audio', 'voice'}))
async def voice_handler(message: Message) -> None:
    file_id = (message.audio.file_id if message.audio else message.voice.file_id)
    file = await bot.get_file(file_id)
    file_duraion = (message.audio.duration if message.audio else message.voice.duration)
    if file_duraion > 60 * MAX_SONG_LENGTH:
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

    TXT_PATH = f'./text/txt_{file_id}.txt'
    PDF_PATH = f'./text/pdf_{file_id}.pdf'
    # JPG_PATH = f'./text/jpg_{file_id}.jpg'
    
    # Get text from backend
    text = await query_txt_from_backend(file_id)
    text_str = text.read().decode("utf-8")

    # Dump it to several formats
    await dump_str_to_txt(text_str, TXT_PATH)
    await dump_txt_to_pdf(text_str, PDF_PATH)
    # dump_txt_to_jpg(text_str, JPG_PATH)

    # Delete mp3
    file_on_disk.unlink()
   
    # Send answer in several formats
    media_group = MediaGroupBuilder()

    media_group.add(type='document', media=FSInputFile(TXT_PATH))
    media_group.add(type='document', media=FSInputFile(PDF_PATH))
    # media_group.attach_photo(FSInputFile(JPG_PATH))

    await bot.send_media_group(chat_id=message.chat.id, media=media_group.build(), reply_to_message_id=message.message_id)

    # Delete created files
    for path in [TXT_PATH, PDF_PATH]: # JPG_PATH]:
        Path(path).unlink()


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
