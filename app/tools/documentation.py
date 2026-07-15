from app.core.dependencies import get_rag_service
from app.core.logger import logger
from app.exceptions.rag import RagError
from app.schemas.rag import SearchDocsRequest


def register_documentation_tools(mcp):

    @mcp.tool()
    def search_technical_docs(request: SearchDocsRequest) -> list[dict]:
        """
        Cerca nei documenti tecnici (manuali) i passaggi più rilevanti rispetto a una domanda.

        Args:
            request: contiene la query di ricerca e il numero massimo di risultati (top_k).

        Returns:
            Lista di dict con "text" (il passaggio trovato) e "score" (rilevanza, 0-1).
            In caso di errore: dict con chiave "error".
        """

        logger.info(f"tool chiamato. search_technical_docs (query={request.query})")

        service = get_rag_service()

        try:
            return service.search_documents(request.query, request.top_k)        
        except RagError as e:
            return [{"error": str(e)}]