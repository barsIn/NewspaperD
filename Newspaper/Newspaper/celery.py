from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Newspaper.settings')

app = Celery('Newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'sending_weekle_email': {
        'task': 'news.tasks.ategory_send',
        'schedule': crontab(day_of_week='monday', hour=8, ),

    },
}



app.autodiscover_tasks()