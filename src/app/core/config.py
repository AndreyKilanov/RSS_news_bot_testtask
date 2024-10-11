import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')


DEFAULT_TITLE_APP = 'Сервис для получения новостей'
DEFAULT_APP_DESCRIPTION = 'Сервис получения новостей из rss каналов'
DEFAULT_POSTGRES_USER = 'user'
DEFAULT_POSTGRES_PASSWORD = 'password'
DEFAULT_POSTGRES_DB = 'postgres_db'
POSTGRES_PORT = '5432'
POSTGRES_CONTAINER_NAME = 'postgres'


class Settings:
    app_title: str = os.getenv('APP_TITLE', DEFAULT_TITLE_APP)
    app_description: str = os.getenv('APP_DESCRIPTION', DEFAULT_APP_DESCRIPTION)

    postgres_user: str = os.getenv('POSTGRES_USER', DEFAULT_POSTGRES_USER)
    postgres_password: str = os.getenv('POSTGRES_PASSWORD', DEFAULT_POSTGRES_PASSWORD)
    postgres_db: str = os.getenv('POSTGRES_DB', DEFAULT_POSTGRES_DB)
    db_container_name: str = os.getenv('POSTGRES_CONTAINER_NAME', POSTGRES_CONTAINER_NAME)
    postgres_port: str = os.getenv('POSTGRES_PORT', POSTGRES_PORT)
    database_url: str = (
        f'postgresql+asyncpg://{postgres_user}:{postgres_password}@'
        f'{db_container_name}:{postgres_port}/{postgres_db}'
    )

    date_format: str = '%a, %d %b %Y %H:%M:%S %z'


settings = Settings()
