from typing import TypedDict, Optional

class AgentState(TypedDict):
    """
    Lo stato che viaggia attraverso tutti i nodi del grafo.
    Ogni nodo legge quello che gli serve e aggiunge il proprio risultato.
    """

    goal:str
    use_data_agent:bool
    use_rag_agent:bool
    data_result: Optional[list]
    rag_result: Optional[list]
    final_answer: Optional[list]