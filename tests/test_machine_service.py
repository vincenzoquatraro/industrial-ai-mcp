# tests/test_machine_service.py
import asyncio
from app.services.machine_service import MachineService
from tests.fake_machine_repository import FakeMachineRepository, FakeMachine


async def main():
    fake_repo = FakeMachineRepository([
        FakeMachine(id=1, name="Macchina Finta CALDA", status="ACTIVE", temperature=150.0),
        FakeMachine(id=2, name="Macchina Finta OK", status="ACTIVE", temperature=50.0),
    ])

    service = MachineService(fake_repo)

    machines = await service.get_all_machines()
    assert len(machines) == 2

    health = await service.analyze_machine_health()
    assert health[0]["health"] == "CRITICAL"
    assert health[1]["health"] == "OK"

    print("tutti i test passati!")


asyncio.run(main())