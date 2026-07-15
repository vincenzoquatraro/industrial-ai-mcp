from app.exceptions.base import IndustrialAIError

class WeatherError(IndustrialAIError):
    """Errore base per tutto ciò che riguarda il meteo"""
    pass

class WeatherTimeout(WeatherError):
    """L'api meteo non ha risposto in tempo"""
    pass

class WeatherUnavailable(WeatherError):
    """L'api meteo è irraggiungibile o ha risposto con errore"""
    pass