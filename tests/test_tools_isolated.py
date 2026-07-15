import json

from app.core.dependencies import get_machine_service, get_rag_service

print("=== TEST MACHINE SERVICE ===")

print("1) prendo il service...")
machine_service = get_machine_service()

print("2) chiamo get_all_machines...")
machines = machine_service.get_all_machines()
print(f"   ricevute {len(machines)} macchine")

print("3) costruisco il dict come fa il tool...")
machines_dict = [
    {
        "id": m.id,
        "name": m.name,
        "status": m.status,
        "temperature": m.temperature
    }
    for m in machines
]

print("4) provo a serializzare in JSON (questo è ciò che fa FastMCP internamente)...")
try:
    serialized = json.dumps(machines_dict)
    print("   OK, JSON valido:")
    print("  ", serialized)
except TypeError as e:
    print("   *** ERRORE DI SERIALIZZAZIONE ***")
    print("  ", e)
    print("   tipi dei campi nella prima macchina:")
    for key, value in machines_dict[0].items():
        print(f"     {key}: {type(value)}")


print()
print("=== TEST RAG SERVICE ===")

print("1) prendo il rag service (carica il modello embedding, può volerci qualche secondo)...")
rag_service = get_rag_service()

print("2) eseguo una ricerca di prova...")
try:
    results = rag_service.search_documents("temperatura motore", top_k=3)
    print(f"   ricevuti {len(results)} risultati")

    print("3) provo a serializzare in JSON...")
    serialized = json.dumps(results)
    print("   OK, JSON valido:")
    for r in results:
        print(f"     score={r['score']:.3f} | {r['text'][:80]}...")

except Exception as e:
    print("   *** ERRORE ***")
    print(f"   {type(e).__name__}: {e}")