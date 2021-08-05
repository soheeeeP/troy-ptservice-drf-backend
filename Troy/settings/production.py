from .base import *

DEBUG = False
ALLOWED_HOSTS = getattr(mod, 'django')['hosts']['prod']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
print(getattr(mod, 'database'))
DATABASES = {
    'default': {
        # psql DB
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getattr(mod, 'database')['name'],
        'USER': getattr(mod, 'database')['user'],
        'PASSWORD': getattr(mod, 'database')['password'],
        'HOST': getattr(mod,'database')['host'],
        'PORT': '5432',
    }
}
