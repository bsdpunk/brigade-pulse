import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
from django.conf import settings

import celery
import raven
from raven.contrib.celery import register_signal, register_logger_signal


class Celery(celery.Celery):

    def on_configure(self):
        client = raven.Client('https://9829e8b7954e4aba8d561ce8db55d616:ba7519259cb541b88470801bbde64555@sentry.trailblazingtech.com/3')

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)

app = Celery(__name__)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
