from app.core.dependencies import get_rag_service
from app.core.logger import logger


class RagAgent:
    """
    Agente 'esecutore': sa solo cercare nei documenti tecnici
    """

    def search(self, query: str, top_k: int = 3) -> list[dict]:

        logger.info(f"rag agent: cerco '{query}'")
        service = get_rag_service()

        return service.search_documents(query, top_k)