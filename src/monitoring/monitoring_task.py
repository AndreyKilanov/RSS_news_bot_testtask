import asyncio
import json

import aiohttp

from rss_parser import parser_news

API_URLS_ENDPOINT = 'http://api:8000/monitoring/all_urls'
API_UPDATE_ENDPOINT = 'http://api:8000/monitoring/update_news'
DELAY = 60


async def get_rss_data(
        session: aiohttp.ClientSession, url: str
) -> tuple[str, str | None]:
    """
    Загружает данные из RSS рассылок.
    """
    async with session.get(url) as response:
        if response.status == 200:
            return url, await response.text()
        else:
            return url, None


async def get_api_data(
        session: aiohttp.ClientSession, endpoint: str
) -> list[str]:
    """
    Получает ссылки и новости из БД.
    """
    async with session.get(endpoint) as response:
        data = await response.json()
        if response.status == 200 and data:
            return data


async def patch_news_in_db(
        session: aiohttp.ClientSession,
        endpoint: str,
        data: list[dict[str, list[dict[str, str, str]]]]
) -> None:
    """
    Отправляет данные в БД.
    """
    async with session.patch(endpoint, json=data) as response:
        if response.status == 201:
            return


async def monitoring_task() -> None:
    while True:
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
                headers={'User-Agent': 'Mozilla/5.0'},
                json_serialize=json.dumps
        ) as session:
            db_data = await get_api_data(session, API_URLS_ENDPOINT)

            if not db_data:
                await asyncio.sleep(DELAY)
                continue

            tasks = [get_rss_data(session, url['name']) for url in db_data] # noqa
            results = await asyncio.gather(*tasks)
            data_dict = {
                url: content
                for url, content in results if content is not None
            }
            news = parser_news(data_dict)
            await patch_news_in_db(session, API_UPDATE_ENDPOINT, news)
            await asyncio.sleep(DELAY)


if __name__ == "__main__":
    asyncio.run(monitoring_task())
