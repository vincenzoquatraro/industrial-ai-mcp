from app.core.dependencies import get_machine_service
from app.core.logger import logger

class DataAgent:
    """
    Agente 'esecutore': sa solo recuperare i dati sulle macchine, non ragione e non decide, esegue.
    """

    def get_machines_status(self) -> list[dict]:
        logger.info("data agent: recupero stato macchina")
        service = get_machine_service()
        machines = service.get_all_machines()

        return [
            {"id": m.id, "name": m.name, "status": m.status, "temperature": m.temperature}
            for m in machines
        ]
    
    def get_health_analysis(self) -> list[dict]:
        logger.info("data agent: analizzo salute macchina")
        service = get_machine_service()
        return service.analyze_machine_health()
    
    