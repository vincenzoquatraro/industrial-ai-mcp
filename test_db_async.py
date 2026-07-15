# test_db_async.py
import asyncio
from app.core.dependencies import get_machine_service


async def main():
    service = await get_machine_service()

    try:
        machines = await service.get_all_machines()
        print(machines)
    finally:
        await service.close()


asyncio.run(main())