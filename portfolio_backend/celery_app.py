"""
Celery configuration for portfolio_backend project.
"""
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')

app = Celery('portfolio_backend')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()

# Celery Beat Schedule (for periodic tasks)
app.conf.beat_schedule = {
    # Send call reminders 24 hours before scheduled time
    'send-call-reminders': {
        'task': 'contact.tasks.send_call_reminder',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9 AM
    },
}


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
