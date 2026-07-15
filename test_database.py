from app.database.connection import get_session
from app.repositories.machine_repository import MachineRepository

session = get_session()

repo = MachineRepository(session)

machines = repo.get_all()

for m in machines:
    print(
        m.name,
        m.status,
        m.temperature
    )

session.close()