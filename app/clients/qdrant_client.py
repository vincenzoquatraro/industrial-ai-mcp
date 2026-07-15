from qdrant_client import QdrantClient
from app.config import settings

class QdrantClientWrapper:

    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)

    def search(self, vector: list[float], top_k: int = 3):
        response = self.client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=vector,
            limit=top_k
        )
        return response.points