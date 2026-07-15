from app.core.dependencies import get_machine_service
from app.core.logger import logger
from app.exceptions.machine import MachineError

def register_machine_tools(mcp):

    @mcp.tool()
    async def get_machine_status() -> list[dict]:
        """
        Restituisce lo stato attuale di tutte le macchine industriali monitorate.

        Returns:
            Lista di dict, ognuno con "id", "name", "status" (es. ACTIVE/STOPPED), "temperature" (°C).
            In caso di errore: dict con chiave "error".
        """

        logger.info("tool chiamato: get_machine_status")

        service = await get_machine_service()

        try:
            machines = await service.get_all_machines()
            return [
                {"id": m.id, "name": m.name, "status": m.status, "temperature": m.temperature}
                for m in machines
            ]
        except MachineError as e:
            return [{"error": str(e)}]
        finally:
            await service.close()
        
        

    
    @mcp.tool()
    async def analyze_machine_health() -> list[dict]:
        """
        Analizza lo stato termico di tutte le macchine e ne valuta la salute.

        Returns:
            Lista di dict con "name", "temperature", "health" (OK / WARNING / CRITICAL).
            In caso di errore: dict con chiave "error".
        """
        logger.info("tool chiamato: analyze_machine_health")
        service = await get_machine_service()

        try:
            return await service.analyze_machine_health()
        except MachineError as e:
            return [{"error": str(e)}]
        finally:
            await service.close()