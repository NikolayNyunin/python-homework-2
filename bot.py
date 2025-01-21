from config import BOT_TOKEN, LoggingMiddleware

from aiogram import Bot, Dispatcher
from aiogram.types import Message

import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.message.middleware(LoggingMiddleware())


@dp.message()
async def echo(message: Message):
    await message.reply(f'Получено сообщение: "{message.text}"')


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
