from app.core.dependencies import get_machine_service
from app.core.logger import logger
from app.exceptions.machine import MachineError

def register_machine_resources(mcp):

    @mcp.resource("industrial://machines/status")
    def machines_status_resource():
        """
        Espone lo stato di tutte le macchine come source leggibile
        """

        logger.info("resource letta: industrial://machines/status")

        service = get_machine_service()

        try:
            machines = service.get_all_machines()
        except MachineError as e:
            return {"error": str(e)}
        
        return [
            {
                "id": m.id,
                "name": m.name,
                "status": m.status,
                "temperature": m.temperature
            }
            for m in machines
        ]
    

    @mcp.resource("industrial://machines/{machine_id}")
    def machine_detail_resource(machine_id: str):
        """
        Espone il dettaglio di una singola macchina, dato il suo id.
        """
        logger.info(f"resource letta: industrial://machines/{machine_id}")

        service = get_machine_service()

        try:
            machines = service.get_all_machines()
        except MachineError as e:
            return {"error": str(e)}

        for m in machines:
            if str(m.id) == machine_id:
                return {
                    "id": m.id,
                    "name": m.name,
                    "status": m.status,
                    "temperature": m.temperature
                }

        return {"error": f"Nessuna macchina trovata con id {machine_id}"}