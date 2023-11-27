from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gru.settings")

# create a Celery instance and configure it using the settings from Django
app = Celery("SuperAGI_workflow")

# Update config.
app.conf.update(
    result_backend=os.environ.get("CELERY_RESULT_BACKEND"),
    broker_url=os.environ.get("CELERY_BROKER_URL"),
    include=["api.tasks"],
)

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Configure periodic tasks
app.conf.beat_schedule = {
    "handle_and_check_agent_runs_every_10m": {
        "task": "api.tasks.handle_workflow_statuses",
        "schedule": crontab(minute="*/10"),
    },
}
