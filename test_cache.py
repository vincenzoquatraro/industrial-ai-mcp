import time

from app.core.dependencies import get_weather_service

service = get_weather_service()

print("1) prima chiamata (dovrebbe interrogare l'API vera)...")
start = time.perf_counter()
result1 = service.get_weather("Bari")
elapsed1 = (time.perf_counter() - start) * 1000
print(f"   risultato: {result1}")
print(f"   tempo: {elapsed1:.2f} ms")

print()
print("2) seconda chiamata, stessa città (dovrebbe leggere da Redis, molto più veloce)...")
start = time.perf_counter()
result2 = service.get_weather("Bari")
elapsed2 = (time.perf_counter() - start) * 1000
print(f"   risultato: {result2}")
print(f"   tempo: {elapsed2:.2f} ms")

print()
if elapsed2 < elapsed1 / 2:
    print(f"OK, la cache sembra funzionare: {elapsed1:.2f} ms -> {elapsed2:.2f} ms")
else:
    print("Attenzione: la seconda chiamata non è nettamente più veloce, controlla la cache")