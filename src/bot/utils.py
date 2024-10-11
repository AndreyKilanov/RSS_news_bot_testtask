import json
from aiohttp import ClientSession


async def registration_to_api(
    endpoint: str,
    username: str,
    telegram_id: int
) -> None:
    """
    Регистрирует пользователя в БД.
    """
    async with (ClientSession(json_serialize=json.dumps) as session):
        async with session.post(
                endpoint,
                json={'username': username, 'telegram_id': telegram_id}
        ) as response:
            return


async def add_url_to_api(endpoint: str, url: str) -> str:
    """
    Добавляет ссылку в БД.
    """
    async with (ClientSession(json_serialize=json.dumps) as session):
        async with session.post(endpoint, json={'name': url}) as response:
            data = await response.json()

            if response.status == 201:
                return data

            return data['detail']


async def get_fresh_news(endpoint: str) -> list:
    """
    Получает ссылки и новости из БД.
    """
    async with (ClientSession(json_serialize=json.dumps) as session):
        async with session.get(endpoint) as response:
            return await response.json()


def escape_reserved_chars(text):
    """
    Экранирует зарезервированные символы.
    """
    reserved_chars = [
        '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|',
        '{', '}', '.', '!'
    ]
    escaped_text = ""

    for char in text:
        if char in reserved_chars:
            escaped_text += "\\" + char
        else:
            escaped_text += char

    return escaped_text
