import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'proj.settings')

app = Celery('proj')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-location-in-3-minutes': {
        'task': 'cargo.tasks.update_machine_location',
        'schedule': crontab(minute='*/3'),
    },
}
