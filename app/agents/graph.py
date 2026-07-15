import json

from langgraph.graph import StateGraph, END

from app.agents.graph_state import AgentState
from app.agents.data_agent import DataAgent
from app.agents.rag_agent import RagAgent
from app.clients.gemini_client import GeminiClient
from app.core.logger import logger

def build_agent_graph(llm: GeminiClient):

    data_agent = DataAgent()
    rag_agent = RagAgent()

    def supervisor_node(state: AgentState) -> dict:
        system_prompt = (
            "Sei un supervisore. Hai a disposizione due agenti:\n"
            "- data_agent: recupera stato e salute delle macchine industriali\n"
            "- rag_agent: cerca informazioni nei manuali tecnici\n\n"
            "Dato l'obiettivo, rispondi SOLO con un JSON con questa forma, senza altro testo:\n"
            '{"use_data_agent": true/false, "use_rag_agent": true/false}'
        )
        raw = llm.chat(system_prompt, state["goal"])
        logger.info(f"[graph] supervisor_node - decisione grezza: {raw!r}")

        try:
            decision = json.loads(raw)
        except json.JSONDecodeError:
            decision = {"use_data_agent": True, "use_rag_agent": True}

        return {
            "use_data_agent": decision.get("use_data_agent", False),
            "use_rag_agent": decision.get("use_rag_agent", False),
        }
    
    def data_node(state: AgentState) -> dict:
        if not state["use_data_agent"]:
            return {}
        return {"data_result": data_agent.get_health_analysis()}
    
    def rag_node(state: AgentState) -> dict:
        if not state["use_rag_agent"]:
            return {}
        return {"rag_result": rag_agent.search(state["goal"])}
    
    def synthesis_node(state: AgentState) -> dict:
        synthesis_prompt = (
            f"Obiettivo: {state['goal']}\n\n"
            f"Dati macchine: {state.get('data_result')}\n\n"
            f"Documenti tecnici: {state.get('rag_result')}\n\n"
            "Rispondi in italiano, in modo chiaro e diretto."
        )
        answer = llm.chat("Sei un assistente tecnico industriale.", synthesis_prompt)
        return {"final_answer": answer}
    

    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("data_agent", data_node)
    graph.add_node("rag_agent", rag_node)
    graph.add_node("synthesis", synthesis_node)

    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", "data_agent")
    graph.add_edge("data_agent", "rag_agent")
    graph.add_edge("rag_agent", "synthesis")
    graph.add_edge("synthesis", END)

    return graph.compile()