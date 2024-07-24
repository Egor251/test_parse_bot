import os

import aiogram
from aiogram import Router
from aiogram.types import Message
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from pymystem3 import Mystem
from dotenv import load_dotenv
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

import config
import pars.main_parser
import db.crud

load_dotenv()  # Подгружаем переменные окружения (для чувствительных данных)

stem = Mystem()  # Морфологический модуль


# Проверяем есть ли искомое слово в заголовке
def find_keyword(titles, keyword):
    for title in titles:
        pure_title = stem.lemmatize(title[0].lower())  # Разбиваем текст на массив слов и приводим все слова к начальной форме
        for word in pure_title:
            if word == keyword.lower():
                logger.debug(f'{title=}, {keyword=}')
                return title[0]
    return False


bot = aiogram.Bot(token=os.environ.get("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()


@router.message(Command("start"))  # Обработка команды /start, отправленной боту
async def start_handler(msg: Message):
    logger.info(f'{msg.chat.id} /start')
    news = pars.main_parser.main_parse(config.site_for_parsing)
    db.crud.insert(news)
    await msg.answer(f'Приветствую в боте!\n\n {config.help_message}')


@router.message(Command("latest"))  # Обработка команды /start, отправленной боту
async def start_handler(msg: Message):
    logger.info(f'{msg.chat.id} /latest')
    news = db.crud.select_latest()
    await msg.answer(f'{news.time} - {news.title}\n\n{news.link}')


@router.message(Command("search"))  # Обработка команды /search, отправленной боту
async def start_handler(msg: Message):
    logger.info(f'{msg.chat.id} {msg.text}')

    try:
        keyword = msg.text.split()[1]
        await msg.answer('Секунду, ищу новость по вашему запросу')
        title = find_keyword(db.crud.select_all_titles(), keyword)

        if title:
            news = db.crud.select_news(title)
            await msg.answer(f'{news.time} - {news.title}\n\n{news.link}')
        else:
            await msg.answer("К сожалению, ничего не найдено по вашему запросу.")
    except IndexError:
        await msg.answer("Вы не ввели слово")



@router.message(Command("help"))  # Обработка команды /help, отправленной боту
async def start_handler(msg: Message):
    logger.info(f'{msg.chat.id} /help')
    await msg.answer(config.help_message)
