import asyncio

from app.jobs.celery_app import celery_app
from app.core.dependencies import get_machine_service
from app.core.logger import logger

async def _analyze_all_machines_async():
    service = await get_machine_service()
    try:
        return await service.analyze_machine_health()
    finally:
        await service.close()


@celery_app.task(name="analyze_all_machines")
def analyze_all_machines():
    """
    Job: analizza la salute di tutte le macchine.
    Celery esegue task sincroni: usiamo asyncio.run() per 'entrare'
    nel mondo async solo per la durata di questa funzione, poi
    torniamo a un risultato normale che Celery sa gestire.
    """
    logger.info("background job avviato: analyze_all_machines")

    result = asyncio.run(_analyze_all_machines_async())

    critical = [m for m in result if m["health"] == "CRITICAL"]
    logger.info(
        f"background job completato: {len(result)} macchine analizzate, "
        f"{len(critical)} in stato CRITICAL"
    )

    return result