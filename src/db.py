from src.utils import calculate_water_target, calculate_calorie_target

from loguru import logger

from datetime import date

# Временная реализация, в будущем будет заменена работой с базой данных
user_data = {}


async def set_profile(user_id: int, weight: float, height: float, age: float,
                      activity_time: int, city: str, calorie_target: int) -> None:
    """Настройка профиля пользователя."""

    user_data[user_id] = {
        'weight': weight,
        'height': height,
        'age': age,
        'activity_time': activity_time,
        'city': city,
        'water_target': await calculate_water_target(weight, city),
        'calorie_target': calorie_target if calorie_target != 0
            else await calculate_calorie_target(weight, height, age),
        'logged_water': 0,
        'logged_calories': 0,
        'burned_calories': 0,
        'date': date.today()
    }

    logger.success(f'Профиль пользователя {user_id} настроен')


async def update_data(user_id: int) -> None:
    """Обновить данные пользователя с id `user_id`."""

    if user_id not in user_data:
        logger.error(f'Пользователь с id {user_id} не найден в БД')
        raise KeyError(f'Пользователь с id {user_id} не найден в БД')

    data = user_data[user_id]
    data['water_target'] = await calculate_water_target(data['weight'], data['city'])
    if data['date'] != date.today():
        data['logged_water'] = 0
        data['logged_calories'] = 0
        data['burned_calories'] = 0
        data['date'] = date.today()

    logger.info(f'Данные пользователя {user_id} обновлены')
