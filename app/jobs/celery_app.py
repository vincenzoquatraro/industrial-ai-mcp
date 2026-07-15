from celery import Celery
from app.config import settings


celery_app = Celery(
    "industrial_ai",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    "analyze-machines-nightly": {
        "task": "analyze_all_machines",
        "schedule": crontab(minute="*/1"),
    },
}

# celery_app.conf.timezone = "Europe/Rome"
celery_app.conf.enable_utc = True