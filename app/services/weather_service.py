import httpx
from app.schemas.weather import WeatherData

from app.core.logger import log_execution
from app.exceptions.weather import WeatherTimeout, WeatherUnavailable


class WeatherService:

    def __init__(self, client, cache_client):
        self.client = client
        self.cache_client = cache_client

    @log_execution
    async def get_weather(self, city: str) -> WeatherData:

        cache_key = f"weather:{city.lower()}"

        cached = self.cache_client.get(cache_key)
        if cached is not None:
            return WeatherData(**cached)

        try:
            data = await self.client.get_weather(city)
            current = data["current_condition"][0]

            result = WeatherData(
                city=city,
                temperature=float(current["temp_C"]),
                description=current["weatherDesc"][0]["value"]
            )

            self.cache_client.set(cache_key, {
                "city": result.city,
                "temperature": result.temperature,
                "description": result.description
            })

            return result

        except httpx.TimeoutException:
            raise WeatherTimeout("Weather API Timeout")

        except httpx.HTTPError:
            raise WeatherUnavailable("Weather API Not Available")