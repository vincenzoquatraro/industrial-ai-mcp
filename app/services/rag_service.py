from app.clients.embedding_client import EmbeddingClient
from app.clients.qdrant_client import QdrantClientWrapper
from app.core.logger import log_execution
from app.exceptions.rag import RagSearchError


class RagService:

    def __init__(self, embedding_client: EmbeddingClient, qdrant_client: QdrantClientWrapper):
        self.embedding_client = embedding_client
        self.qdrant_client = qdrant_client

    @log_execution
    def search_documents(self, query: str, top_k: int = 3) -> list[dict]:

        try:
            vector = self.embedding_client.embed(query)
            results = self.qdrant_client.search(vector, top_k=top_k)
        except Exception as e:
            raise RagSearchError(f"Ricerca sui documenti fallita: {e}")

        return [
            {
                "text": (point.payload or {}).get("text", ""),
                "score": point.score
            }
            for point in results
        ]