import asyncio

import aiohttp
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import REGISTRATION_ENDPOINT, ADD_URL_ENDPOINT, FRESH_NEWS_ENDPOINT
from keyboards import keys, main_keyboard
from states import AddUrlState
from utils import (
    registration_to_api, add_url_to_api, get_fresh_news, escape_reserved_chars
)

main_router = Router()

START_MSG = '<b>Привет {name}, я RSS бот</b>👋'
ADD_URL_MSG = (
    'Введите RSS ссылку для добавления в ваш список источников новостей'
)
ADD_URL_MSG_ERR = 'При добавлении ссылки произошла ошибка'
GET_NEWS_HOUR_MSG = 'Нет новостей за последний час'
GET_NEWS_DAY_MSG = 'Нет новостей за последний день'
GET_NEWS_MSG_ERR = 'При получении новостей произошла ошибка'
FAQ_MSG = (
    '===================================\n'
    'Бот для получения новостей\n'
    '===================================\n\n'
    'Нажмите <b>добавить источник</b>, чтобы добавить новую ссылку,'
    'ссылка должны быть на источник rss новостей\n'
    'например: <b>http://news.rambler.ru/rss/world/</b>\n\n'
    'После добавления ссылки вы можете получать ежедневные новости\n'
    'Новости обновляются раз минуту\n\n'
    '===================================\n'
    'created by @AndyFebruary'
)


@main_router.message(CommandStart())
async def start_command(message: types.Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id

    await registration_to_api(REGISTRATION_ENDPOINT, full_name, telegram_id)
    await message.answer(
        START_MSG.format(name=full_name),
        reply_markup=main_keyboard,
        parse_mode='HTML'
    )


@main_router.message(F.text == keys.add_url)
async def handle_url(message: types.Message, state: FSMContext):
    await state.set_state(AddUrlState.url)
    await message.answer(
        ADD_URL_MSG,
        reply_markup=types.ReplyKeyboardRemove()
    )


@main_router.message(AddUrlState.url)
async def add_url(message: types.Message, state: FSMContext):
    url = str(message.text)
    tg_id = message.from_user.id

    try:
        api_data = await add_url_to_api(
            ADD_URL_ENDPOINT.format(tg_id=tg_id), url
        )
        await message.answer(api_data, reply_markup=main_keyboard)

    except aiohttp.ClientError:
        await message.answer(ADD_URL_MSG_ERR, reply_markup=main_keyboard)

    finally:
        await state.clear()


@main_router.message(F.text.in_([keys.check_news_hour, keys.check_news_day]))
async def check_news_hour(message: types.Message):
    tg_id = message.from_user.id
    hours = 1 if message.text == keys.check_news_hour else 24
    endpoint = FRESH_NEWS_ENDPOINT.format(tg_id=tg_id, hours=hours)

    api_data = await get_fresh_news(endpoint)

    if not api_data:
        err_msg = (
            GET_NEWS_HOUR_MSG
            if message.text == keys.check_news_hour
            else GET_NEWS_DAY_MSG
        )
        await message.answer(err_msg)
        return

    bulk_news = ''
    num_news = 0

    for news in api_data:

        if not news['title']:
            await message.answer(GET_NEWS_MSG_ERR)
            return

        title = escape_reserved_chars(news['title'])
        num_news += 1
        bulk_news += f'{num_news}\.\ [{title}]({news["link"]})\n'  # noqa

        if len(bulk_news) >= 3900:
            await message.answer(
                bulk_news,
                disable_web_page_preview=True,
                parse_mode='MarkdownV2'
            )
            bulk_news = ''
            await asyncio.sleep(1)

    await message.answer(
        bulk_news,
        disable_web_page_preview=True,
        parse_mode='MarkdownV2'
    )
    await asyncio.sleep(1)


@main_router.message(F.text == keys.faq)
async def faq(message):
    await message.answer(FAQ_MSG, parse_mode='HTML')
