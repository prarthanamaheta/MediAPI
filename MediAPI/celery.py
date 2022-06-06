from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings
from django.conf.global_settings import LOGGING

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MediAPI.settings')

app = Celery('MediAPI')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# CELERY-BEAT SETTING
app.conf.beat_scheduler = {

}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@setup_logging.connect()
def configure_logging(sender=None, **kwargs):
    import logging.config
    logging.config.dictConfig(LOGGING)