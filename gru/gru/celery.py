from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

settings.configure()

# create a Celery instance and configure it using the settings from Django
app = Celery("superAGI_workflow")

# Update config.
app.conf.update(
    result_backend=os.environ.get("CELERY_RESULT_BACKEND"),
    broker_url=os.environ.get("CELERY_BROKER_URL"),
)

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
