from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DATABASE_URL: str
    WEATHER_BASE_URL: str
    WEATHER_TIMEOUT: int
    LOG_LEVEL: str

    LOG_FILE: str = "mcp_server.log"
    LOG_MAX_BYTES: int = 5_000_000  # 5 MB
    LOG_BACKUP_COUNT: int = 3
    LOG_JSON: bool = False

    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL_SECONDS: int = 300  # 5 minuti

    GEMINI_API_KEY: str

    QDRANT_URL: str = "http://localhost:6335"
    QDRANT_COLLECTION: str = "industrial_docs"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()