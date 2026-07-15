from abc import ABC, abstractmethod
from app.database.models import Machine


class MachineRepositoryInterface(ABC):
    """
    Contratto che ogni repository di macchine deve rispettare.
    """

    @abstractmethod
    async def get_all(self) -> list[Machine]:
        ...

    @abstractmethod
    async def get_by_status(self, status: str) -> list[Machine]:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...