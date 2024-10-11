import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)


BOT_TOKEN = os.getenv('BOT_TOKEN')

# API
BASE_ENDPOINT = 'http://api:8000/'
REGISTRATION_ENDPOINT = BASE_ENDPOINT + 'user/'
ADD_URL_ENDPOINT = BASE_ENDPOINT + 'user/{tg_id}'
FRESH_NEWS_ENDPOINT = BASE_ENDPOINT + 'user/{tg_id}-{hours}/fresh_news'
