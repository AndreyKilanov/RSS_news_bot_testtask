from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.validators import (
    check_user_in_db, check_url_availability, check_url_in_db,
    check_url_in_user_list, URL_VALID
)
from core import get_async_session
from models import UsersModel, UrlsModel, NewsModel
from schemas import (
    UrlsSchema, UsersSchema, UsersSchemaResponse,
    NewsOutSchema
)

router = APIRouter(
    prefix='/user',
    tags=['User'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/', response_model=UsersSchemaResponse, status_code=201)
async def create_user(
        user: UsersSchema,
        session: AsyncSession = Depends(get_async_session)
) -> UsersModel:
    """
    Создает пользователя в БД.
    """
    await check_user_in_db(user.telegram_id, session)
    user = UsersModel(telegram_id=user.telegram_id, username=user.username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get(
    '/all_users', response_model=list[UsersSchemaResponse], status_code=200
)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    """
    Возвращает всех пользователей из БД.
    """
    get_users = await session.execute(select(UsersModel))
    return get_users.scalars().all()


@router.get(
    '/{telegram_id}', response_model=UsersSchemaResponse, status_code=200
)
async def get_user(
        telegram_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Возвращает пользователя по telegram_id.
    """
    return await check_user_in_db(telegram_id, session, return_user=True)


@router.post(
    '/{telegram_id}', status_code=201
)
async def add_url(
        telegram_id: int,
        url: UrlsSchema,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Добавляет новую ссылку пользователю и в общую БД ссылок.
    """
    url = await check_url_availability(url.name)
    user = await check_user_in_db(telegram_id, session, return_user=True)
    new_url = await check_url_in_db(url, session)

    if not new_url:
        new_url = UrlsModel(name=url)
        session.add(new_url)

    user = await check_url_in_user_list(new_url, user)
    await session.commit()
    await session.refresh(user)
    return URL_VALID.format(url=new_url.name)


@router.get(
    '/{telegram_id}-{hours}/fresh_news',
    response_model=list[NewsOutSchema],
    status_code=200
)
async def get_fresh_news(
        hours: int,
        telegram_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Возвращает список новостей для конкретного пользователя за последние
    hours часов.
    В пути указывается telegram_id и hours: время за которое нужно получить
    новости.
    """
    start_date = datetime.now() - timedelta(hours=hours)
    start_date = start_date.replace(microsecond=0, tzinfo=timezone.utc)

    new_news = await session.execute(
        select(NewsModel)
        .join(UrlsModel, UrlsModel.id == NewsModel.url_id)
        .join(UsersModel, UsersModel.urls.any(UrlsModel.id == NewsModel.url_id))
        .where(UsersModel.telegram_id == telegram_id)
        .order_by(NewsModel.pubdate.desc())
    )
    new_news = new_news.scalars().all()
    return [news for news in new_news if news.pubdate >= start_date]
