import os
import dj_database_url
from django.utils import log
from pathlib import Path

_env = os.environ.get
_pkg = _env('DJANGO_SETTINGS_MODULE').rsplit('.', 1)[0]
PROJ_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__import__(_pkg).__file__).resolve().parent
SRC_ROOT = BASE_DIR.parent
REPO_ROOT = SRC_ROOT.parent
FILE_CACHE_DIR = BASE_DIR / 'cached'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
TEMPLATE_ROOT = BASE_DIR / 'templates'

VERSION = _env('SOURCE_COMMIT')
SECRET_KEY = _env('DJANGO_SECRET_KEY')
DEBUG = _env('DJANGO_DEBUG') == 'TRUE'
ALLOWED_HOSTS = _env('DJANGO_ALLOWED_HOSTS').split(',')
INTERNAL_IPS = []

if DEBUG:
    print('\n  DEBUG =', DEBUG, '\n')
    import warnings
    warnings.simplefilter('error')
else:
    assert SECRET_KEY

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = CSRF_COOKIE_HTTPONLY = True
    X_FRAME_OPTIONS = 'SAMEORIGIN'

    # TODO:
    # SECURE_HSTS_SECONDS
    # SECURE_HSTS_INCLUDE_SUBDOMAINS
    # SECURE_HSTS_PRELOAD

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proj',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ADMIN_URL = (_env('DJANGO_ADMIN_URL') or 'changeme').rstrip('/').lstrip('/') + '/'

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

WSGI_APPLICATION = 'proj.wsgi.application'

DATABASES = {'default': dict(dj_database_url.config(), ENGINE='django.db.backends.postgresql')}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'proj.middleware.SystemInfoMiddleware',
    'proj.middleware.CustomSessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [TEMPLATE_ROOT],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'proj.jinja2.environment',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
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

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


if _env('DJANGO_CACHE') == 'DUMMY':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
elif _env('DJANGO_CACHE') == 'LOCMEM':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
else:
    mc = _env('MEMCACHIER_SERVERS')
    CACHES = {
        'default': {
            'BACKEND': 'proj.cache.MemCachier' if mc else
                       'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': mc.replace(',', ';') if mc else 'memcached:11211',
            'USERNAME': _env('MEMCACHIER_USERNAME'),
            'PASSWORD': _env('MEMCACHIER_PASSWORD'),
            'BINARY': True,  # needed for authentication
            'TIMEOUT': None,  # disables expiration
            'OPTIONS': {
                'behaviors': {
                    'tcp_nodelay': True,  # Enable faster IO
                    'tcp_keepalive': True,  # Keep connection alive

                    # Timeout settings
                    'connect_timeout': 2000,  # ms
                    'send_timeout': 750 * 1000,  # us
                    'receive_timeout': 750 * 1000,  # us
                    '_poll_timeout': 2000,  # ms

                    # Better failover
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30,
                },
            },
        },
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': os.getenv('DJANGO_LOGGING_LEVEL', 'INFO'),
        'handlers': ['console'],
        'formatter': 'verbose',
        'propagate': True,
    },
    'filters': dict(log.DEFAULT_LOGGING['filters'], **{

    }),
    'formatters': {
        'verbose': {
            '()': 'proj.utils.logging.Formatter',
            'format': '%(asctime)s,%(msecs)03d  %(levelname)-7s  %(name)s ~  '
                      '%(message)s  ~ %(funcName)s() %(pathname)s:%(lineno)d',
            'datefmt': '%Y-%b-%d %a %z %H:%M:%S',
        },
        'django.server': {
            '()': 'proj.utils.logging.ServerFormatter',
            'format': '%(asctime)s,%(msecs)03d  %(proto)s %(status_code)s  '
                      '%(size)8s %(duration)6s  %(message)s',
            'datefmt': '%Y-%b-%d %a %z %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'requests': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

if _env('SENTRY_DSN'):
    # import logging
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    # from sentry_sdk.integrations.logging import LoggingIntegration

    v = _env('HEROKU_RELEASE_VERSION')
    if not VERSION and v:
        VERSION = '%s-%s' % (v, _env('HEROKU_SLUG_COMMIT'))

    sentry_sdk.init(integrations=[
        DjangoIntegration(),
        # LoggingIntegration(
        #     level=logging.INFO,  # Capture info and above as breadcrumbs
        #     event_level=logging.ERROR  # Send errors as events
        # )
    ], release=VERSION)
