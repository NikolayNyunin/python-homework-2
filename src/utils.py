from src.config import WEATHER_API_KEY

import aiohttp


async def calculate_water_target(weight: float, city: str) -> int:
    """Вычисление цели потребления воды (в мл)."""

    result = weight * 30
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

    try:
        params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    return 0, (await response.json())['main']['temp']
                else:
                    return -1, await response.text()
    except aiohttp.ClientError as e:
        return -1, str(e)
