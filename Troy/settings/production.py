from .base import *

DEBUG = False
ALLOWED_HOSTS = getattr(mod, 'django')['hosts']['prod']

INSTALLED_APPS += [
    'storages',
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
aws_key = getattr(mod, 'aws')
DATABASES = {
    'default': {
        # psql DB
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': aws_key['rds']['name'],
        'USER': aws_key['rds']['user'],
        'PASSWORD': aws_key['rds']['password'],
        'HOST': aws_key['rds']['host'],
        'PORT': '5432',
    }
}

aws_key = getattr(mod, 'aws')
AWS_ACCESS_KEY_ID = aws_key['s3']['access_key_id']
AWS_SECRET_ACCESS_KEY = aws_key['s3']['secret_access_key']
AWS_REGION = aws_key['s3']['region']

# AWS S3 storage parameters
AWS_STORAGE_BUCKET_NAME = aws_key['s3']['storage_bucket_name']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}


# default storage system class
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# add 'collectstatic' static dir at S3 Bucket storage
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'