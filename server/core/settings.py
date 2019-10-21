"""
Django settings for cariot_backend project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import re
import sys

import dj_database_url
from django.utils.translation import ugettext_lazy as _
from dotenv import load_dotenv, find_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from core.env_utils import bool_value

load_dotenv(find_dotenv())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')
BASE_HOST_NAME = re.sub(r"https?://", '', BASE_URL)

SITE_NAME = os.environ.get('SITE_NAME', 'CreativeDay')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
SIGNING_SECRET = os.environ.get('SIGNING_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool_value(os.environ.get('DEBUG', ''))
TEST = 'test' in sys.argv

ALLOWED_HOSTS = ['*']

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ELASTIC_URL = os.environ.get('ELASTICSEARCH_URL',
                             os.environ.get('FOUNDELASTICSEARCH_URL', os.environ.get('BONSAI_URL')))

# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.search.backends.elasticsearch5',
#         'URLS': [ELASTIC_URL],
#         'INDEX': 'wagtail',
#         'TIMEOUT': 5,
#         'OPTIONS': {},
#         'INDEX_SETTINGS': {},
#     }
# }

APPEND_SLASH = False
WAGTAIL_APPEND_SLASH = APPEND_SLASH

# Application definition

INSTALLED_APPS = [
    'taggit',

    'core',
    'api',
    'cms',
    'search',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.api.v2',
    'modelcluster',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'raven.contrib.django.raven_compat',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_filters',
    'graphene_django',
    'django_extensions',
    'compressor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware'
]

# Enable CORS for local development
if DEBUG:
    INSTALLED_APPS += [
        'wagtail.contrib.styleguide',
        'corsheaders',
        # 'debug_toolbar'
    ]
    MIDDLEWARE += ['corsheaders.middleware.CorsMiddleware',
                   # 'debug_toolbar.middleware.DebugToolbarMiddleware'
                   ]
    CORS_ORIGIN_WHITELIST = (
        'get.localhost:8080',
        'localhost:8080',
        'localhost:8080',
        '127.0.0.1:8080',
        '0.0.0.0:8080',
    )
    CORS_ALLOW_CREDENTIALS = True

MIDDLEWARE += [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    'core.middleware.ThreadLocalMiddleware',
    'core.middleware.CommonRedirectMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '..', 'client/dist'), os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.settings_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# Database
DATABASES = {
    'default': dj_database_url.config()
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

WEAK_PASSWORDS = DEBUG
if WEAK_PASSWORDS:
    AUTH_PASSWORD_VALIDATORS = []
else:
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

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '..', 'client/dist/static'),
)

if not TEST:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

COMPRESS_CSS_FILTERS = [
    # 'django_compressor_autoprefixer.AutoprefixerFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_ENABLED = True

if not DEBUG:
    COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
    COMPRESS_OFFLINE = True

# AWS S3
# http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

USE_AWS = bool_value(os.environ.get('USE_AWS'))
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False

# use with cloudfront
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
if USE_AWS:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # use with cloudfront
    # MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.environ.get('DJANGO_MEDIAFILES', os.path.join(BASE_DIR, 'media'))

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

USE_404_FALLBACK_IMAGE = os.environ.get('USE_404_FALLBACK_IMAGE', False)

# Logging Conf

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose_format': {
            'format': '%(levelname)s %(asctime)s %(module)s %(name)s (%(process)d): %(message)s'
        },
        'simple_format': {
            'format': '%(levelname)s %(name)s: %(message)s'
        },
    },
    'disable_existing_loggers': True,
    'handlers': {
        'mail_admins': {
            'level': 'CRITICAL',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple_format'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/root/code/tmp.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['mail_admins'],
            'level': 'CRITICAL',
            'propagate': False,
        },
    }
}

if not DEBUG and os.environ.get('SENTRY_DSN'):
    # import raven
    RAVEN_CONFIG = {
        'dsn': os.environ.get('SENTRY_DSN'),
    }

    LOGGING['handlers'] = {
        'sentry': {
            'level': 'ERROR',  # ERROR, WARNING, INFO
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple_format'
        }
    }

    for k, v in LOGGING['loggers'].items():
        LOGGING['loggers'][k]['handlers'] = ['sentry', 'console']
else:
    RAVEN_CONFIG = ''

RAVEN_DSN_JS = os.environ.get('RAVEN_DSN_JS', '')

GOOGLE_TAG_MANAGER_CONTAINER_ID = os.environ.get('GOOGLE_TAG_MANAGER_CONTAINER_ID')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

GRAPHENE = {
    'SCHEMA': 'api.schema.schema',
}

# http://docs.wagtail.io/en/v2.1/advanced_topics/settings.html?highlight=urls
WAGTAIL_SITE_NAME = SITE_NAME
WAGTAILIMAGES_IMAGE_MODEL = 'cms.CmsImage'

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')
SLACK_WEBHOOK_URL_SEARCH_LOG = os.environ.get('SLACK_WEBHOOK_URL_SEARCH_LOG')
INTERCOM_ACCESS_TOKEN = os.environ.get('INTERCOM_ACCESS_TOKEN')

# FEATURE FLAGS
LOGIN_REQUIRED = bool_value(os.environ.get('LOGIN_REQUIRED', 'True'))

SERVICE_COLLECTION_ID = os.environ.get('SERVICE_COLLECTION_ID')

OVERWRITE_MEDIA_DOMAIN = os.environ.get('OVERWRITE_MEDIA_DOMAIN', False)
