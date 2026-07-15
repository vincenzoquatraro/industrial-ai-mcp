import json
from typing import Any

from app.clients.ollama_client import OllamaClient
from app.clients.gemini_client import GeminiClient
from app.core.dependencies import get_machine_service, get_rag_service
from app.core.logger import logger

AVAILABLE_TOOLS = {
    "get_machine_status": "Restituisce lo stato attuale di tutte le macchine (id, nome, stato, temperatura).",
    "analyze_machine_health": "Analizza la salute termica di tutte le macchine (OK/WARNING/CRITICAL).",
    "search_technical_docs": "Cerca informazioni nei manuali tecnici in base a una domanda.",
}


class PlanningAgent:
    """
    Agente semplice: dato un obiettivo in linguaggio naturale,
    1) chiede al modello locale quali tool servono,
    2) li esegue davvero,
    3) chiede al modello di sintetizzare la risposta finale.
    """

    def __init__(self, llm: GeminiClient):
        self.llm = llm

    def plan(self, goal: str) -> list[str]:
        tools_description = "\n".join(f"- {name}: {desc}" for name, desc in AVAILABLE_TOOLS.items())

        system_prompt = (
            "Sei un pianificatore. Hai a disposizione questi tool:\n"
            f"{tools_description}\n\n"
            "Dato l'obiettivo dell'utente, rispondi SOLO con un array JSON dei nomi dei tool "
            "da chiamare, in ordine, senza nessun altro testo. "
            'Esempio di risposta valida: ["get_machine_status"]'
        )

        raw = self.llm.chat(system_prompt, goal)
        logger.info(f"planning agent - piano grezzo del modello: {raw!r}")

        try:
            plan = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning("planning agent - il modello non ha risposto con JSON avalido, uso FALLBACK")
            plan = list(AVAILABLE_TOOLS.keys())

        return [step for step in plan if step in AVAILABLE_TOOLS]


    def execute_step(self, step: str):
        if step == "get_machine_status":
            return get_machine_service().get_all_machines()
        if step == "analyze_machine_health":
            return get_machine_service().analyze_machine_health()
        if step == "search_techincal_docs":
            return get_rag_service().search_documents(query="informazioni rilevanti", top_k=3)
        return None
    
    def run(self, goal: str) -> str:

        logger.info(f"planning agent avviato - obiettivo: {goal!r}")
        steps = self.plan(goal)
        logger.info(f"planning agent - piano scelto: {steps}")

        results = {step: self.execute_step(step) for step in steps}

        synthesis_prompt = (
            f"Obiettivo originale: {goal}\n\n"
            f"Dati raccolti: {results}\n\n"
            "Rispondi all'obiettivo usando questi dati, in italiano, in modo chiaro e conciso."
        )

        return self.llm.chat(
            "Sei un assistente tecnico industriale. Rispondi in modo chiaro e diretto.",
            synthesis_prompt
        )