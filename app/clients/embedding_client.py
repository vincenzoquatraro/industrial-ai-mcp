from sentence_transformers import SentenceTransformer
from app.config import settings

class EmbeddingClient:
    """
    Wrapper attorno al modello di embedding.
    Il modello è pesante da caricare, quindi lo teniamo in memoria
    e lo riusiamo per ogni ricerca (vedi dependencies.py sotto).
    """
        
    
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def embed(self, text:str) -> list[float]:
        return self.model.encode(text).tolist()