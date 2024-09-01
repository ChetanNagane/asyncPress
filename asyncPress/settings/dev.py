from asyncPress.settings.base import *

# Django

DEBUG = True

CELERY_BROKER_URL = 'redis://localhost:6379/0'