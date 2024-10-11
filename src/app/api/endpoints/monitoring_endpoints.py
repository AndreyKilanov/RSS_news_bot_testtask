from datetime import datetime as dt, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_async_session, config
from models import UrlsModel, NewsModel
from schemas import UrlsSchemaResponse, UrlsUpdateSchema

router = APIRouter(
    prefix='/monitoring',
    tags=['Monitoring'],
    responses={404: {'description': 'Not found'}}
)


@router.get(
    '/all_urls', response_model=list[UrlsSchemaResponse], status_code=200
)
async def get_all_urls(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает все ссылки из БД.
    """
    get_urls = await session.execute(select(UrlsModel))
    get_urls = get_urls.scalars().all()
    return get_urls


@router.patch('/update_news', status_code=201)
async def update_news(
        new_data: list[UrlsUpdateSchema],
        session: AsyncSession = Depends(get_async_session)
):
    """
    Получает новости из модуля "monitoring" и добавляет их в БД.
    """
    db_urls = await session.execute(select(UrlsModel))
    db_news = await session.execute(select(NewsModel))
    db_urls = db_urls.scalars().all()
    db_news = db_news.scalars().all()

    list_lincs_on_news_in_db = [news.link for news in db_news]

    for data in new_data:
        url_db = None

        for news in data.news:

            if news.link in list_lincs_on_news_in_db:
                continue

            if url_db is None:
                for url in db_urls:
                    if url.name == data.name:
                        url_db = url
                        break

            pubdate = dt.strptime(
                news.pubdate, config.settings.date_format
            ).replace(tzinfo=timezone.utc)
            new_news = NewsModel(
                title=news.title,
                pubdate=pubdate,
                link=news.link
            )
            session.add(new_news)
            url_db.news.append(new_news)

    await session.commit()
