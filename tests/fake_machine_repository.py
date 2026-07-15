# tests/fake_machine_repository.py
from dataclasses import dataclass
from app.repositories.base import MachineRepositoryInterface


@dataclass
class FakeMachine:
    id: int
    name: str
    status: str
    temperature: float


class FakeMachineRepository(MachineRepositoryInterface):

    def __init__(self, machines: list[FakeMachine]):
        self.machines = machines

    async def get_all(self):
        return self.machines

    async def get_by_status(self, status: str):
        return [m for m in self.machines if m.status == status]
    
    async def close(self) -> None:
        pass  # nessuna sessione vera da chiudere, è un repository finto