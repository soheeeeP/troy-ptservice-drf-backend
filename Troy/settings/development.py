from .base import *

DEBUG = True
# print(getattr(mod, 'django'))
ALLOWED_HOSTS = getattr(mod, 'django')['hosts']['dev']

INSTALLED_APPS +=[
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
