import os
from os.path import abspath, dirname, join
import dj_database_url
from django.utils import log

_env = os.environ.get
_pkg = _env('DJANGO_SETTINGS_MODULE').rsplit('.', 1)[0]
BASE_DIR = dirname(abspath(__import__(_pkg).__file__))
SRC_ROOT = dirname(BASE_DIR)
REPO_ROOT = dirname(SRC_ROOT)
FILE_CACHE_DIR = join(BASE_DIR, 'cached')
STATIC_ROOT = join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [join(BASE_DIR, 'static')]
TEMPLATE_ROOT = join(BASE_DIR, 'templates')

VERSION = _env('SOURCE_COMMIT')
SECRET_KEY = _env('DJANGO_SECRET_KEY')
DEBUG = _env('DJANGO_DEBUG') == 'TRUE'
ALLOWED_HOSTS = _env('DJANGO_ALLOWED_HOSTS').split(',')
INTERNAL_IPS = []

if DEBUG:
    import warnings
    print('\n  DEBUG =', DEBUG, '\n')
    warnings.simplefilter('error')
    warnings.filterwarnings('ignore', '.*collections.abc.*')  # jinja2<=2.10
else:
    assert SECRET_KEY

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

WSGI_APPLICATION = 'proj.wsgi.application'

DATABASES = {'default': dj_database_url.config()}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'proj.middleware.SystemInfoMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'handlers': ['console', 'sentry'],
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
                      '%(message)s ~ %(duration)s %(size)s',
            'datefmt': '%Y-%b-%d %a %z %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['require_debug_false'],
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
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]
    import raven
    if not VERSION:
        try:
            VERSION = raven.fetch_git_sha(REPO_ROOT)
        except raven.exceptions.InvalidGitRepository:
            import logging
            logging.exception("Failed fetching git sha.")
    RAVEN_CONFIG = {
        'release': VERSION,
        # 'CELERY_LOGLEVEL': logging.INFO,
    }
else:
    LOGGING['handlers']['sentry']['class'] = 'logging.NullHandler'
