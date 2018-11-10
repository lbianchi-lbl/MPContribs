"""
Django settings for test_site project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from django.conf.global_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from django_extensions.management.commands.generate_secret_key import get_random_secret_key
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
JPY_USER = os.environ.get('JPY_USER')
DEBUG = os.environ.get('MPCONTRIBS_DEBUG', bool(JPY_USER))

ALLOWED_HOSTS = ['portal.mpcontribs.org', 'contribs.materialsproject.org', 'localhost']

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'django_cas_ng.backends.CASBackend',
    'webtzite.backends.CASBackend',
    #'webtzite.backends.CustomModelBackend',
    ##'webtzite.backends.CustomBrowserIDBackend',
    #'nopassword.backends.email.EmailBackend'
)

# Application definition

from mpcontribs.users_modules import get_user_installed_apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    #'django_browserid',
    'nopassword',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_cas_ng',
    'require',
    'webtzite',
    'mpcontribs.portal',
    'mpcontribs.rest',
    'mpcontribs.explorer',
    'zappa_django_utils'
] + get_user_installed_apps()

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'webtzite.middleware.APIKeyMiddleware',
)

ROOT_URLCONF = 'test_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'test_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

AWS_STORAGE_BUCKET_NAME = 'mpcontribs-sqlite'
#DATABASE_ENGINE = 'django.db.backends.sqlite3',
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'zappa_django_utils.db.backends.s3sqlite',
        'NAME': 'db.sqlite3',
        'BUCKET': AWS_STORAGE_BUCKET_NAME
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

PROXY_URL_PREFIX = '/flaskproxy/{}'.format(JPY_USER) if JPY_USER else ''
ROOT_PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = ROOT_PROJECT_DIR
STATIC_ROOT += '/webtzite/static' if DEBUG else '/static'
STATIC_URL = PROXY_URL_PREFIX + '/static/'

STATIC_ROOT_URLS = {
    STATIC_URL[:-1]: STATIC_ROOT,
    STATIC_URL[:-1] + '_rest': ROOT_PROJECT_DIR + '/mpcontribs/rest/static',
    STATIC_URL[:-1] + '_portal': ROOT_PROJECT_DIR + '/mpcontribs/portal/static'
}
from mpcontribs.users_modules import get_user_static_dirs
STATIC_ROOT_USER_URLS = {}
for static_dir in get_user_static_dirs():
    static_url_suffix = static_dir.split(os.sep)[-3]
    key = '_'.join([STATIC_URL[:-1], static_url_suffix])
    STATIC_ROOT_USER_URLS[key] = os.path.join(ROOT_PROJECT_DIR, static_dir)

STATIC_ROOT_URLS.update(STATIC_ROOT_USER_URLS)

AWS_S3_CUSTOM_DOMAIN = 's3.amazonaws.com/{}'.format(AWS_STORAGE_BUCKET_NAME)
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None

STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
#STATICFILES_STORAGE = 'leftbehind.apps.matchmaker.utils.S3PipelineStorage'
#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'pipeline.finders.PipelineFinder',
#)
#PIPELINE_DISABLE_WRAPPER = True


#if not DEBUG:
#    LOGGING = {
#        'version': 1,
#        'disable_existing_loggers': False,
#        'handlers': {
#            'file': {
#                'level': 'DEBUG',
#                'class': 'logging.FileHandler',
#                'filename': os.path.join(ROOT_PROJECT_DIR, 'test_site.log'),
#            },
#        },
#        'loggers': {
#            'django.request': {
#                'handlers': ['file'],
#                'level': 'DEBUG',
#                'propagate': True,
#            },
#            'webtzite': {
#                'handlers': ['file'],
#                'level': 'DEBUG',
#                'propagate': True,
#            },
#        },
#    }

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'Test Site <test_site@jupyterhub.materialsproject.org>'

REQUIRE_JS = 'components/requirejs/require.js'
REQUIRE_DEBUG = True

if not DEBUG or os.environ.get('DEPLOYMENT') == 'MATGEN':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CAS_SERVER_URL = 'https://materialsproject.org/cas/'
CAS_VERSION = '3'
CAS_LOGOUT_COMPLETELY = False
CAS_REDIRECT_URL = '/'
CAS_RETRY_LOGIN = True
CAS_USERNAME_ATTRIBUTE = 'username'
CAS_APPLY_ATTRIBUTES_TO_USER = True
