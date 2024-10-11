from __future__ import annotations

from typing import List

from sqlalchemy import (
    Table, Column, Integer, ForeignKey, String, DateTime
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core import Base

secondary_table = Table(
    'users_urls',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('url_id', Integer, ForeignKey('url.id'), primary_key=True),
)


class UsersModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String(128), nullable=False)

    urls: Mapped[List[UrlsModel]] = relationship(
        secondary=secondary_table,
        back_populates='users',
        lazy='selectin'
    )


class UrlsModel(Base):
    __tablename__ = 'url'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)

    news: Mapped[List[NewsModel]] = relationship(
        back_populates='urls', lazy='selectin'
    )
    users: Mapped[List[UsersModel]] = relationship(
        secondary=secondary_table,
        back_populates='urls',
        lazy='selectin'
    )


class NewsModel(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    pubdate: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)

    url_id: Mapped[int] = mapped_column(ForeignKey('url.id'))
    urls: Mapped[UrlsModel] = relationship(back_populates='news', lazy='selectin')
