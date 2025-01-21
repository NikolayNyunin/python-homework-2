from config import BOT_TOKEN, LoggingMiddleware
from profile import router

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.message.middleware(LoggingMiddleware())


@dp.message(Command('start'))
async def start_command(message: Message):
    """Начало взаимодействия с ботом."""

    await message.answer(
        'Привет! Я — бот, позволяющий отслеживать потребление воды и расход калорий.\n'
        'Используйте команду /help для просмотра списка поддерживаемых команд.'
    )


@dp.message(Command('help'))
async def help_command(message: Message):
    """Справка по возможностям бота."""

    await message.answer(
        'Я могу помочь в отслеживании потребления воды и расхода калорий.\n'
        'Список реализованных команд:'  # TODO: list commands
    )


# @dp.message()
# async def unknown_command(message: Message):
#     await message.reply(f'Команда не распознана: "{message.text}"')


async def main():
    """Основная функция для запуска бота."""

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
