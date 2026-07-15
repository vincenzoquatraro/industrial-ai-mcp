from dataclasses import dataclass

@dataclass
class MachineSchema:
    id: int
    name: str
    status: str
    temperature: float

