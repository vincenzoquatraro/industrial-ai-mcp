from app.core.dependencies import get_machine_service

print("1) prendo il service...")
service = get_machine_service()

print("2) service ottenuto:", service)
print("3) chiamo get_all_machines...")

machines = service.get_all_machines()

print("4) risultato:", machines)