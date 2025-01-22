from src.config import WEATHER_API_KEY, NUTRITION_API_KEY, WORKOUT_API_KEY

import aiohttp


async def calculate_water_target(weight: float, activity_time: int, city: str) -> int:
    """Вычисление цели потребления воды (в мл)."""

    result = weight * 30
    result += 500 * (activity_time // 30)
    status, temperature = await get_current_temperature(city)
    if status == 0 and temperature > 25:
        result += 750
    return round(result)


async def calculate_calorie_target(weight: float, height: float, age: float) -> int:
    """Вычисление цели потребления калорий (в ккал)."""

    return round(10 * weight + 6.25 * height - 5 * age)


async def get_current_temperature(city: str) -> (int, float | str):
    """Получение текущей температуры в городе `city`."""

    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    return 0, (await response.json())['main']['temp']
                else:
                    return -1, await response.text()
    except aiohttp.ClientError as e:
        return -1, str(e)


async def get_food_nutrition(food_query: str) -> (int, float | str):
    """Получение калорийности еды `food_query`."""

    api_url = 'https://api.calorieninjas.com/v1/nutrition'
    headers = {'X-Api-Key': NUTRITION_API_KEY}
    params = {'query': food_query}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    data = (await response.json())['items']
                    if len(data) == 0:
                        return -1, 'Продукты не найдены'
                    result = {
                        'name': data[0]['name'],
                        'calories': data[0]['calories']
                    }
                    return 0, result
                else:
                    return -1, await response.text()
    except aiohttp.ClientError as e:
        return -1, str(e)


async def get_workout_calories_burned(activity_name: str, weight: float, duration: int) -> (int, tuple | str):
    """Получение количества сожжённых калорий."""

    api_url = 'https://api.api-ninjas.com/v1/caloriesburned'
    headers = {'X-Api-Key': WORKOUT_API_KEY}
    params = {'activity': activity_name, 'weight': round(weight * 2.2), 'duration': duration}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if len(data) == 0:
                        return -1, 'Тренировка не распознана'
                    result = {
                        'name': data[0]['name'],
                        'calories': data[0]['total_calories']
                    }
                    return 0, result
                else:
                    return -1, await response.text()
    except aiohttp.ClientError as e:
        return -1, str(e)
