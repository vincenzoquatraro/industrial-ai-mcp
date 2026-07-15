# test_job.py
from app.jobs.tasks import analyze_all_machines

result = analyze_all_machines.delay()
print("job avviato, id:", result.id)
print("risultato (aspetto max 10 secondi):", result.get(timeout=10))