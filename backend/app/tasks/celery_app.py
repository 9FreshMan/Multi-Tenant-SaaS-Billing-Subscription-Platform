from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "saas_billing",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.billing", "app.tasks.notifications"],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)

# Periodic tasks schedule
celery_app.conf.beat_schedule = {
    "check-trial-expiration": {
        "task": "app.tasks.billing.check_trial_expiration",
        "schedule": 3600.0,  # Every hour
    },
    "generate-monthly-invoices": {
        "task": "app.tasks.billing.generate_monthly_invoices",
        "schedule": 86400.0,  # Every day
    },
    "calculate-usage-metrics": {
        "task": "app.tasks.billing.calculate_usage_metrics",
        "schedule": 3600.0,  # Every hour
    },
    "send-payment-reminders": {
        "task": "app.tasks.notifications.send_payment_reminders",
        "schedule": 43200.0,  # Every 12 hours
    },
}

if __name__ == "__main__":
    celery_app.start()
