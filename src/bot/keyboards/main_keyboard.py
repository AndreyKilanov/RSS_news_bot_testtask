from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

from keyboards import keys


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=keys.add_url),
        ],
        [
            KeyboardButton(text=keys.check_news_hour),
        ],
        [
            KeyboardButton(text=keys.check_news_day),
        ],
        [
            KeyboardButton(text=keys.faq),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...",
)
