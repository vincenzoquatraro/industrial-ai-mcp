import logging
import time
import inspect
from functools import wraps
from app.config import settings
from app.core.metrics import tool_calls_total, tool_latency_seconds, errors_total


logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("mcp_server.log", encoding="utf-8"),  # scrive su file
        logging.StreamHandler()                                  # scrive anche a video
    ]
    )


logger = logging.getLogger(
        "industrial_ai"
    )


def log_execution(func):

    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs):

            start = time.perf_counter()

            try:
                result = await func(*args, **kwargs)

                elapsed = (time.perf_counter() - start) * 1000
                logger.info("%s executed in %.2f ms", func.__name__, elapsed)

                tool_calls_total.labels(tool_name=func.__name__, status="success").inc()
                tool_latency_seconds.labels(tool_name=func.__name__).observe(elapsed / 1000)

                return result

            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                logger.exception("%s failed after %.2f ms", func.__name__, elapsed)

                tool_calls_total.labels(tool_name=func.__name__, status="error").inc()
                tool_latency_seconds.labels(tool_name=func.__name__).observe(elapsed / 1000)
                errors_total.labels(tool_name=func.__name__, error_type=type(e).__name__).inc()

                raise

        return async_wrapper

    @wraps(func)  # uso func per mantenere il nome e docstring nella funzione decorata
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)  # qui esegue la funzione vera e propria

            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(f"{func.__name__} eseguita in {elapsed_ms:.2f} ms")

            tool_calls_total.labels(tool_name=func.__name__, status="success").inc()
            tool_latency_seconds.labels(tool_name=func.__name__).observe(elapsed_ms / 1000)

            return result

        except Exception as e:

            elapsed_ms = (time.perf_counter() - start) * 1000
            # logger.exception logga anche lo stack trace dell'errore
            logger.exception(f"{func.__name__} ha fallito")

            tool_calls_total.labels(tool_name=func.__name__, status="error").inc()
            tool_latency_seconds.labels(tool_name=func.__name__).observe(elapsed_ms / 1000)
            errors_total.labels(tool_name=func.__name__, error_type=type(e).__name__).inc()

            raise

    return wrapper