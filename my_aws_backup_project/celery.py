from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

app = Celery('project_name')

# Using a string here means the worker doesnt have to serialize
# the configuration object to child processes.

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()