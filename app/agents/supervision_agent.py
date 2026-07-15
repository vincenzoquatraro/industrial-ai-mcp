import json

from app.agents.data_agent import DataAgent
from app.agents.rag_agent import RagAgent
from app.clients.gemini_client import GeminiClient
from app.core.logger import logger

class SupervisorAgent:
    """
    Unico agente che pensa: decide quali esecutori chiamare per rispondere ad un obbiettivo e poi sintetizza i risultati
    """

    def __init__(self, llm: GeminiClient):
        self.llm = llm
        self.data_agent = DataAgent()
        self.rag_agent = RagAgent()

    def decide(self, goal:str) -> dict:
        system_prompt = (
            "Sei un supervisore. Hai a disposizione due agenti:\n"
            "- data_agent: recupera stato e salute delle macchine industriali\n"
            "- rag_agent: cerca informazioni nei manuali tecnici\n\n"
            "Dato l'obiettivo, rispondi SOLO con un JSON con questa forma, senza altro testo:\n"
            '{"use_data_agent": true/false, "use_rag_agent": true/false}'
        )

        raw = self.llm.chat(system_prompt, goal)
        logger.info(f"supervisior - decisione: {raw!r}")

        try:
            decision = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("JSON non valido - uso entrambi gli egenti")
            decision = {"use_data_agent": True, "use_rag_agent": True}

        return decision
    

    def run(self, goal:str) -> str:

        logger.info(f"supervisor avviato - obbiettivo: {goal!r}")

        decision = self.decide(goal)

        collected = {}

        if decision.get("use_data_agent"):
            collected["dati_macchine"] = self.data_agent.get_health_analysis()

        if decision.get("use_rag_agent"):
            collected["documenti_tecnici"] = self.rag_agent.search(goal)

        synthesis_prompt = (
            f"Obiettivo: {goal}\n\n"
            f"Dati raccolti dagli agenti: {collected}\n\n"
            "Rispondi in italiano, in modo chiaro e diretto."
        )

        return self.llm.chat(
            "Sei un assistente tecnico industriale.",
            synthesis_prompt
        )