from app.schemas.weather import WeatherRequest
from pydantic import ValidationError

print("1) provo un input valido con spazi in più...")
r = WeatherRequest(city="  Bari  ")
print("   risultato:", repr(r.city))  # deve stampare 'Bari' (spazi tolti)

print("2) provo un input vuoto...")
try:
    WeatherRequest(city="   ")
    print("   ERRORE: non ha sollevato nulla, controlla il validator!")
except ValidationError as e:
    print("   validazione fallita come previsto ->", e.errors()[0]["msg"])