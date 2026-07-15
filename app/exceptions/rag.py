from app.exceptions.base import IndustrialAIError

class RagError(IndustrialAIError):
    """Errore base per la ricerca di documenti"""
    pass

class RagSearchError(RagError):
    """La ricerca Qdrant è falita"""
    pass