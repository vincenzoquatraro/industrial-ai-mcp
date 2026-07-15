from app.core.logger import logger

def register_machine_prompts(mcp):

    @mcp.prompt()
    def industrial_health_report():
        """
        Genera un report tecnico sullo stato di salute delle macchine
        """

        logger.info("prompt richiesto: industrial_health_report")

        return (
            "Analizza tutte le macchine industriali disponibili. "
            "Per ciascuna macchina, valuta lo stato di salute in base alla temperatura "
            "(OK sotto 80°C, WARNING tra 80 e 100°C, CRITICAL sopra 100°C). "
            "Produci un report tecnico chiaro, con eventuali raccomandazioni "
            "per le macchine in stato WARNING o CRITICAL."
        )
    

    @mcp.prompt()
    def machine_diagnosis(machine_id: str):
        """
        Diagnosi approfondita di una singola macchina
        """

        logger.info(f"prompt richiesto: machine_diagnosis (machine_id = {machine_id})")

        return (
            f"Analizza nel dettaglio la macchina con id {machine_id}. "
            "Leggi il suo stato attuale, valuta se la temperatura è nella norma, "
            "e spiega in linguaggio semplice cosa significherebbe se fosse in stato CRITICAL."
        )