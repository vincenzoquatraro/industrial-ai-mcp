from app.clients.gemini_client import GeminiClient
# from app.agents.planning_agent import PlanningAgent
from app.agents.graph import build_agent_graph
from app.core.logger import logger


def register_agent_tools(mcp):

    @mcp.tool()
    def run_planning_agent(goal: str) -> str:
        """
        Esegue il grafo multi-agente (supervisor + data agent + rag agent)
        per rispondere a un obiettivo complesso.

        Args:
            goal: l'obiettivo o la domanda da porre.

        Returns:
            La risposta testuale sintetizzata dal supervisore.
        """
        logger.info(f"tool chiamato: run_planning_agent (goal={goal!r})")

        graph = build_agent_graph(GeminiClient())

        result = graph.invoke({
            "goal": goal,
            "use_data_agent": False,
            "use_rag_agent": False,
            "data_result": None,
            "rag_result": None,
            "final_answer": None,
            })
        
        return result["final_answer"] or ""