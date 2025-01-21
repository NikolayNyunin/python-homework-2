from src.config import BOT_TOKEN, LoggingMiddleware
from src.profile import router
from src.db import log_water, log_consumed_calories, log_burned_calories, get_progress

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, Update
from aiogram.fsm.context import FSMContext
from loguru import logger

import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.message.outer_middleware(LoggingMiddleware())


@dp.message(CommandStart())
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
        'Список реализованных команд:\n'
        '- /set_profile — настроить профиль пользователя (очищает все сохранённые ранее данные);\n'
        '- /log_water <объём воды в мл> — записать потребление воды;\n'
        '- /log_food <название блюда> — записать приём пищи;\n'
        '- /log_workout <тип тренировки> <время в мин> — записать физическую тренировку;\n'
        '- /check_progress — вывести прогресс в выполнении дневных целей;\n'
        '- /cancel — отменить текущее действие.'
    )


@dp.message(Command('cancel'))
async def cancel_command(message: Message, state: FSMContext):
    """Сброс текущего состояния (отмена действия)."""

    current_state = await state.get_state()
    if current_state is None:
        await message.answer('В данный момент нечего отменять')
    else:
        await state.clear()
        await message.answer('Действие отменено')


@dp.message(Command('log_water'))
async def log_water_command(message: Message, command: CommandObject):
    """Логирование потребления воды."""

    # Валидация потреблённого объёма воды
    water_volume = command.args
    if water_volume is None:
        await message.answer('Отсутствует объём потреблённой воды (в мл)')
        return

    try:
        water_volume = int(water_volume)
    except ValueError:
        await message.answer('Передано некорректное значение объёма воды')
        return

    if water_volume < 0 or water_volume > 3000:
        await message.answer('Введённый объём воды выходит из допустимого диапазона (0, 3000) мл')
        return

    try:
        await log_water(message.from_user.id, water_volume)
    except KeyError:
        await message.answer('Профиль пользователя не настроен! Сначала используйте команду /set_profile.')
    else:
        data = await get_progress(message.from_user.id)
        await message.answer('Выпитая вода записана! '
                             f'Прогресс за день: {data["logged_water"]}/{data["water_target"]} мл')


@dp.message(Command('log_food'))
async def log_food_command(message: Message, command: CommandObject):
    """Логирование приёма пищи."""

    # food_type = command.args
    # TODO: implement


@dp.message(Command('log_workout'))
async def log_workout_command(message: Message, command: CommandObject):
    """Логирование тренировки."""

    # command.args
    # TODO: implement


@dp.message(Command('check_progress'))
async def check_progress_command(message: Message):
    """Вывод прогресса в выполнении дневных целей."""

    try:
        data = await get_progress(message.from_user.id)
    except KeyError:
        await message.answer('Профиль пользователя не настроен! Сначала используйте команду /set_profile.')
    else:
        await message.answer(
            'Дневной прогресс:\n'
            f'Вода: выпито {data["logged_water"]}/{data["water_target"]} мл\n'
            f'Калории: поглощено {data["logged_calories"]}/{data['calorie_target']} ккал\n'
            f'Сожжено {data["burned_calories"]} ккал'
        )


# @dp.update()
# async def unknown_action(update: Update):
#     if update.message is not None:
#         await update.message.answer(f'Команда не распознана: "{update.message.text}"')


async def main() -> None:
    """Основная функция для запуска бота."""

    try:
        logger.info('Polling запущен')
        await dp.start_polling(bot)
    finally:
        logger.info('Polling прекращён')
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
