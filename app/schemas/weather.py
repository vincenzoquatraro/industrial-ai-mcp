from dataclasses import dataclass

@dataclass
class WeatherData:
    city: str
    temperature: float
    description: str


from pydantic import BaseModel, field_validator, Field

class WeatherRequest(BaseModel):
    city: str = Field(description="Nome della città di cui vuoi il meteo, es: 'Bari'")

    @field_validator("city")
    @classmethod
    def city_non_vuota(cls, v:str) -> str:
        v= v.strip()
        if not v:
            raise ValueError("city non può essere vuota")
        return v