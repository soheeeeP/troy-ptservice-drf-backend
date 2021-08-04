from .base import *

DEBUG = False
ALLOWED_HOSTS = getattr(mod, 'django')['hosts']['prod']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        # psql DB
    }
}