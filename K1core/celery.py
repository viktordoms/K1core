from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'K1core.settings')

app = Celery('K1core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.task_asks_late = False
app.conf.task_ignore_result = True
app.conf.broker_connection_retry_on_startup = True