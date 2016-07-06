import os

import dj_database_url
import raven

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = os.getenv('SECRET_KEY', '6s=km)xm-kt-xo#l-a+ei4am016_=u=$@90jsxebkve8l49la0')

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definitions.  We'll keep separate 3rd party and our apps.
THIRD_PARTY_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
)

OUR_APPS = (
    'api',
)

INSTALLED_APPS = THIRD_PARTY_APPS + OUR_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'settings.wsgi_settings.application'


# We'll use Postgres for both local and production!

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600,
                                      default='postgres://postgres:postgres@localhost:5432/brigade-pulse')
}


# We'll force all timestamps to be saved and served in UTC, regardless of client/host timezone
TIME_ZONE = 'UTC'
USE_TZ = False

# DjangoWhiteNoise requires STATIC_URL and STATIC_ROOT to be set even though we don't really use them.
# TEMPLATE_DIRS allows us to serve index.html at the root + WHITENOISE_ROOT allows us to serve files
# from the public directory directly.  Probably not *best* practice, but it works for us.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticroot')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'public'),)
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'public')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)
MEETUP_API_KEY = os.getenv('MEETUP_API_KEY', None)

BROKER_URL = os.getenv('REDIS_URL', 'redis://')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

RAVEN_CONFIG = {
    'dsn': 'https://9829e8b7954e4aba8d561ce8db55d616:ba7519259cb541b88470801bbde64555@sentry.trailblazingtech.com/3',
}
try:
    RAVEN_CONFIG['release'] = raven.fetch_git_sha(os.path.dirname(os.path.dirname(__file__)))
except:
    RAVEN_CONFIG['release'] = os.getenv('GIT_REV', '')