from .base import *

from Troy.settings import BASE_DIR

DEBUG = True
# print(getattr(mod, 'django'))
ALLOWED_HOSTS = getattr(mod, 'django')['hosts']['dev']

INSTALLED_APPS +=[
    'debug_toolbar',
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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{ALLOWED_HOSTS[0]}:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    # app이름으로 cache명 지정
    "apps": {
        "BACKEND": "django_redis.cache.RedisCache",
        # cache의 db_index 지정
        "LOCATION": f"redis://{ALLOWED_HOSTS[0]}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "apps",
    },
}
