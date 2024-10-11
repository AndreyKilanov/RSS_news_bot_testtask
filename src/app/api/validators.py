import aiohttp
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import UsersModel, UrlsModel

URL_ERROR = 'Проверьте корректность написания ссылки или доступен ли сайт'
URL_APPEND_ERROR = 'Такую ссылку вы уже добавляли'
URL_VALID = '{url} успешно добавленен в ваш список источников новостей'
USER_DB_ERROR = 'Такой пользователь уже существует'
USER_IS_NOT_IN_DB = 'Такого пользователя не существует'


async def check_url_availability(url: str) -> str:
    """
    Проверяет корректность написания ссылки и доступен ли сайт.
    """
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False),
        headers={'User-Agent': 'Mozilla/5.0'}
    ) as session:
        try:
            async with session.get(url) as response:
                return url
        except Exception:
            raise HTTPException(status_code=400, detail=URL_ERROR)


async def check_url_in_db(url: str, session: AsyncSession) -> UrlsModel | None:
    """
    Проверяет существует ли URL в БД.
    """
    url = await session.execute(select(UrlsModel).where(UrlsModel.name == url))
    url = url.scalars().first()
    return url if url else None


async def check_url_in_user_list(
        new_url: UrlsModel, user: UsersModel
) -> UsersModel:
    """
    Проверяет существует ли URL в списке ссылок пользователя.
    """
    if new_url in user.urls:
        raise HTTPException(status_code=400, detail=URL_APPEND_ERROR)
    user.urls.append(new_url)
    return user


async def check_user_in_db(
        telegram_id: int,
        session: AsyncSession,
        return_user: bool = False
) -> UsersModel | None:
    """
    Проверяет существует ли пользователь в БД.
    Если флаг return_user=True, то возвращает пользователя.
    """
    user = await session.execute(
        select(UsersModel).where(
            UsersModel.telegram_id == telegram_id  # type: ignore
        )
    )
    user = user.scalars().first()

    if return_user:
        if user:
            return user
        raise HTTPException(status_code=404, detail=USER_IS_NOT_IN_DB)

    if user:
        raise HTTPException(status_code=400, detail=USER_DB_ERROR)
