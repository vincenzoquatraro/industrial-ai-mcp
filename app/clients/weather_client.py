import httpx

from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from app.config import settings

class WeatherClient:

    @retry(
            stop=stop_after_attempt(3),
            wait=wait_fixed(2),
            reraise=True
    )
    async def get_weather(self, city: str):

        url = f"{settings.WEATHER_BASE_URL}/{city}?format=j1"

        async with httpx.AsyncClient() as client: 
            response = await client.get(url, timeout=settings.WEATHER_TIMEOUT)

        response.raise_for_status()

        return response.json()