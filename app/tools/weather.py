from app.core.dependencies import get_weather_service
from app.core.logger import logger
from app.exceptions.weather import WeatherError
from app.schemas.weather import WeatherRequest

from pydantic import ValidationError


def register_weather_tools(mcp):

    @mcp.tool()
    async def get_weather(request: WeatherRequest) -> dict:
        """
        Restituisce il meteo corrente di una città

        Args:
            request: contiene il nome della città (non vuoto, spazi iniziali/finali rimossi automaticamente)

        Returns:
            dict con chiavi "city", "temperature" (°C), "description".
            In caso di errore: dict con chiave "error" e messaggio testuale.
        """

        logger.info(f"tool chiamato: get_weather (city={request.city})")

        try:
            request =  WeatherRequest(city= request.city)
        except ValidationError as e:
            return {"error": f"Input non valido {e.errors()[0]['msg']}"}

        service = (get_weather_service())

        try:
            result = await service.get_weather(request.city)

            return {
                "city": result.city,
                "temperature": (result.temperature),
                "description": (result.description)
            }
        
        except WeatherError as e:
            return {
                "error": str(e)
            }