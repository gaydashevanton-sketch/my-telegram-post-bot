import os
from dotenv import load_dotenv

load_dotenv()  # для локальной разработки

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Проверяем, что ID получен и преобразуем в число
if CHANNEL_ID is None:
    raise ValueError("CHANNEL_ID не установлен в переменных окружения!")
CHANNEL_ID = int(CHANNEL_ID)  # Telegram ожидает число, а не строку
