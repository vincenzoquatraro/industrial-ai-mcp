from app.database.connection import engine
from app.database.models import Machine
from sqlalchemy.orm import Session

print("1) inserisco le macchine di test...")
with Session(engine) as session:
    session.add_all([
        Machine(name="Pressa 01", status="ACTIVE", temperature=65.5),
        Machine(name="Robot 02", status="STOPPED", temperature=40.2),
        Machine(name="Forno 03", status="ACTIVE", temperature=120.8),
    ])
    session.commit()

print("2) fatto!")