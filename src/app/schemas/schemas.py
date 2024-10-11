from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsersSchema(BaseModel):
    telegram_id: int
    username: str


class UsersSchemaResponse(UsersSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    urls: list[UrlsSchemaRequest]


class UsersOutSchema(UsersSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UrlsSchema(BaseModel):
    name: str


class UrlsSchemaRequest(UrlsSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    news: list[NewsOutSchema]


class UrlsSchemaResponse(UrlsSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    news: list[NewsOutSchema]
    users: list[UsersOutSchema]


class UrlsUpdateSchema(UrlsSchema):
    news: list[NewsUpdateSchema]


class NewsUpdateSchema(BaseModel):
    link: str
    pubdate: str
    title: str


class NewsInSchema(BaseModel):
    link: str
    pubdate: datetime
    title: str


class NewsOutSchema(NewsInSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
