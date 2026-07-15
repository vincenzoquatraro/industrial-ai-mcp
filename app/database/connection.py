import sys
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

# Su Windows, psycopg in modalità async richiede il SelectorEventLoop
# invece del ProactorEventLoop (quello di default) — va impostato prima
# che qualsiasi event loop venga creato, quindi lo facciamo qui, al
# momento dell'import di questo modulo (che avviene sempre prima di
# asyncio.run() nei nostri script).
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

def get_session():
    return SessionLocal()