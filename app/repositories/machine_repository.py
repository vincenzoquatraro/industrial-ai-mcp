from app.database.models import Machine
from sqlalchemy import select
from app.repositories.base import MachineRepositoryInterface

class MachineRepository(MachineRepositoryInterface):

    def __init__(self, session):
        self.session = session

    async def get_all(self) -> list[Machine]:
        stmt = select(Machine)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_by_status(self, status: str) -> list[Machine]:
        stmt = select(Machine).where(Machine.status == status)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def close(self) -> None:
        await self.session.close()