from app.repositories.base import MachineRepositoryInterface
from app.schemas.machine import MachineSchema
from app.core.logger import log_execution

from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.machine import MachineDatabaseError

class MachineService:

    def __init__(self, repository: MachineRepositoryInterface):
        self.repository = repository

    @log_execution
    async def get_all_machines(self):

        try:
            machines = await self.repository.get_all()
        except SQLAlchemyError:
            raise MachineDatabaseError("Impossibile leggere le macchine dal database")

        return [
            MachineSchema(
                id=m.id,
                name=m.name,
                status=m.status,
                temperature=m.temperature
            )
            for m in machines
        ]
    
    @log_execution
    async def get_active_machines(self):

        try:
            machines = await self.repository.get_by_status("ACTIVE")
        except SQLAlchemyError:
            raise MachineDatabaseError("Impossibile leggere le macchine dal database")
        

        return [
            MachineSchema(
                id=m.id,
                name=m.name,
                status=m.status,
                temperature=m.temperature
            )
            for m in machines
        ]
    
    @log_execution
    async def analyze_machine_health(self):

        try:
            machines = await self.repository.get_all()
        except SQLAlchemyError:
            raise MachineDatabaseError("Impossibile leggere le macchine dal database")

        result = []

        for machine in machines:
            if machine.temperature > 100:
                health = "CRITICAL"
            elif machine.temperature > 80:
                health = "WARNING"
            else:
                health = "OK"

            result.append(
                {
                    "name": machine.name,
                    "temperature": machine.temperature,
                    "health": health
                }
            )

        return result
    
    async def close(self) -> None:
        await self.repository.close()