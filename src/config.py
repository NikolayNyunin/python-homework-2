from dotenv import load_dotenv
from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

import os
from typing import Callable

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NUTRITION_API_KEY = os.getenv('NUTRITION_API_KEY')
WORKOUT_API_KEY = os.getenv('WORKOUT_API_KEY')


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event: Message, data: dict):
        logger.info(f'Получено сообщение от пользователя {event.from_user.id}: "{event.text}"')
        return await handler(event, data)
