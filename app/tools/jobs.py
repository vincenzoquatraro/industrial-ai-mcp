# app/tools/jobs.py
from app.jobs.tasks import analyze_all_machines
from app.core.logger import logger


def register_job_tools(mcp):

    @mcp.tool()
    def trigger_machine_analysis_job() -> dict:
        """
        Avvia manualmente (in background) il job di analisi salute macchine,
        senza aspettare la schedulazione notturna.
        """
        logger.info("tool chiamato: trigger_machine_analysis_job")

        task = analyze_all_machines.delay()
        return {"job_id": task.id, "status": "avviato"}