from .base import *
from celery.schedules import crontab

DEBUG = True
# print(getattr(mod, 'django'))
ALLOWED_HOSTS = getattr(mod, 'django')['hosts']['dev']

INSTALLED_APPS +=[
    'debug_toolbar',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ('127.0.0.1',)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {}

DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191
