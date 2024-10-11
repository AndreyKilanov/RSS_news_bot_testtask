# Телеграм бот для RSS рассылок

---

## Описание проекта
Бот, который получает rss-ссылки и возвращает новости за час или за сутки, по списку рассылки  

Авторизует пользователя в бд по его **telegram id**.  
Добавляет рассылки.  
Новости хранятся в бд и обновляются раз в минуту

---

## Запуск проекта

- Клонируйте репозиторий
```bash
git clone git@github.com:AndreyKilanov/RSS_news_bot_testtask.git
```

- Создайте и заполните `.env` по пути `./infra`

```bash
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres_db
POSTGRES_PORT=5432

BOT_TOKEN=bot token

```


- Запустите контейнера из `./infra` командой:
```bash
docker-compose up -d --build
```
- После запуска проекта Swagger будет доступен по [адресу](http://127.0.0.1:8000/docs)


## Стек
1. [x] Python 3.11
2. [x] Aiogram 3.5.0
3. [x] Fastapi 0.115.0
4. [x] SQLAlchemy 2.0.35
5. [x] Alembic 1.13.3
6. [x] Aiohttp 3.10.5
7. [x] Feedparser 6.0.11

## Контакты
[![](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/AndyFebruary)
