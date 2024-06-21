from django.conf import settings
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor


scheduler = BackgroundScheduler(
    jobstores={'default': SQLAlchemyJobStore(url=settings.DB_URL)},
    executors={'default': ThreadPoolExecutor(20)},
    job_defaults={'misfire_grace_time': 3600}
)

def send_birthday_notification(subscriber_email, birthday_person_name):
    send_mail(
        "Happy Birthday!",
        f"Happy birthday to {birthday_person_name}!",
        settings.EMAIL_HOST_USER,
        [subscriber_email],
    )
