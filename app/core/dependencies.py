from app.database.connection import get_session
from app.repositories.machine_repository import MachineRepository
from app.services.machine_service import MachineService
from app.clients.weather_client import WeatherClient
from app.services.weather_service import WeatherService
from app.clients.embedding_client import EmbeddingClient
from app.clients.qdrant_client import QdrantClientWrapper
from app.services.rag_service import RagService
from app.clients.cache_client import CacheClient



_cache_client = None
_embedding_client = None

def get_rag_service() -> RagService:
    global _embedding_client

    if _embedding_client is None:
        _embedding_client = EmbeddingClient()
    
    qdrant_client = QdrantClientWrapper()
    return RagService(_embedding_client, qdrant_client)

async def get_machine_service() -> MachineService:
    session = get_session()
    repository = MachineRepository(session)

    return MachineService(repository)

def get_weather_service() -> WeatherService:
    client = WeatherClient()
    cache_client = get_cache_client()
    return WeatherService(client, cache_client)

def get_cache_client() -> CacheClient:
    global _cache_client
    if _cache_client is None:
        _cache_client = CacheClient()
    return _cache_client