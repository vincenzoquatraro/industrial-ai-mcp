# test_weather_async.py
import asyncio
from app.core.dependencies import get_weather_service


async def main():
    service = get_weather_service()
    result = await service.get_weather("Bari")
    print(result)


asyncio.run(main())