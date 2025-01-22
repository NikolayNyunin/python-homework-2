from src.db import set_profile

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

profile_router = Router()


class ProfileSetup(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity_time = State()
    city = State()
    calorie_target = State()


@profile_router.message(Command('set_profile'))
async def set_profile_command(message: Message, state: FSMContext):
    """Начало настройки профиля пользователя."""

    await state.set_state(ProfileSetup.weight)
    await message.answer('Введите ваш вес (в кг):')


@profile_router.message(ProfileSetup.weight)
async def set_weight(message: Message, state: FSMContext):
    """Задание веса."""

    # Валидация веса
    try:
        weight = float(message.text)
    except ValueError:
        await message.answer('Введено некорректное значение веса, повторите попытку')
    else:
        if weight < 30 or weight > 200:
            await message.answer('Введённый вес выходит из допустимого диапазона (30, 200) кг')
        else:
            await state.update_data(weight=weight)
            await state.set_state(ProfileSetup.height)
            await message.answer('Введите ваш рост (в см):')


@profile_router.message(ProfileSetup.height)
async def set_height(message: Message, state: FSMContext):
    """Задание роста."""

    # Валидация роста
    try:
        height = float(message.text)
    except ValueError:
        await message.answer('Введено некорректное значение роста, повторите попытку')
    else:
        if height < 140 or height > 220:
            await message.answer('Введённый рост выходит из допустимого диапазона (140, 220) см')
        else:
            await state.update_data(height=height)
            await state.set_state(ProfileSetup.age)
            await message.answer('Введите ваш возраст:')


@profile_router.message(ProfileSetup.age)
async def set_age(message: Message, state: FSMContext):
    """Задание возраста."""

    # Валидация возраста
    try:
        age = float(message.text)
    except ValueError:
        await message.answer('Введено некорректное значение возраста, повторите попытку')
    else:
        if age < 12 or age > 100:
            await message.answer('Введённый возраст выходит из допустимого диапазона (12, 100) лет')
        else:
            await state.update_data(age=age)
            await state.set_state(ProfileSetup.activity_time)
            await message.answer('Сколько минут активности у вас в день?')


@profile_router.message(ProfileSetup.activity_time)
async def set_activity_time(message: Message, state: FSMContext):
    """Задание времени активности."""

    # Валидация времени активности
    try:
        activity_time = int(message.text)
    except ValueError:
        await message.answer('Введено некорректное значение времени активности, повторите попытку')
    else:
        if activity_time < 0 or activity_time > 1440:
            await message.answer('Введённое время активности выходит из допустимого диапазона (0, 1440) минут')
        else:
            await state.update_data(activity_time=activity_time)
            await state.set_state(ProfileSetup.city)
            await message.answer('В каком городе вы находитесь? (напишите название по-английски)')


@profile_router.message(ProfileSetup.city)
async def set_city(message: Message, state: FSMContext):
    """Задание города проживания."""

    city = message.text
    # TODO: implement city validation
    await state.update_data(city=city)
    await state.set_state(ProfileSetup.calorie_target)
    await message.answer('Какая у вас цель потребления калорий (в ккал)? (для автоматического вычисления введите 0)')


@profile_router.message(ProfileSetup.calorie_target)
async def set_calorie_target(message: Message, state: FSMContext):
    """Задание цели потребления калорий (в ккал)."""

    # Валидация цели потребления калорий
    try:
        calorie_target = int(message.text)
    except ValueError:
        await message.answer('Введено некорректное значение цели потребления калорий, повторите попытку')
    else:
        if calorie_target < 0 or calorie_target > 10000:
            await message.answer('Введённая цель потребления калорий выходит из допустимого диапазона (0, 10000) ккал')
        else:
            await state.update_data(calorie_target=calorie_target)
            data = await state.get_data()
            await set_profile(message.from_user.id, **data)
            await message.answer('Настройка профиля успешно завершена')
            await state.clear()
