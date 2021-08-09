import os, sys, json
from datetime import timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRETS_PATH = os.path.join(BASE_DIR, '.config')
SECRET_BASE_FILE = os.path.join(SECRETS_PATH, 'secret_key.json')

mod = sys.modules[__name__]

secret = json.loads(open(SECRET_BASE_FILE).read())
for key, value in secret.items():
    setattr(sys.modules[__name__], key, value)

SECRET_KEY = getattr(mod, 'django')['secret_key']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'users',
    'quests',
    'centers',
    'services',
    'tags',

    'rest_framework',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    # django-allauth (social login)
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF = 'Troy.urls.base'
SET_MODE = os.environ.get('DJANGO_SETTINGS_MODULE')
if SET_MODE == 'Troy.settings.production':
    ROOT_URLCONF = 'Troy.urls.production'
else:
    ROOT_URLCONF = 'Troy.urls.development'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': os.path.join(BASE_DIR, 'templates'),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Troy.wsgi.base.application'

# Rest-Framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # session authentication
        'rest_framework.authentication.SessionAuthentication',
        # use JWT instead of token-based authentication
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )
}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
}

JWT_AUTH_COOKIE = 'troy-auth'

JWT_AUTH_REFRESH_COOKIE = 'troy-refresh-token'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.UserProfile'
SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')