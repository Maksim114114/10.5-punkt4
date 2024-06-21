import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
app = Celery('NewsPortal')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_manday_8am': {
        'task': 'news.tasks.weekly_send_email_task',
        #'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
       'schedule': crontab(),
        'args': (),
    },
}