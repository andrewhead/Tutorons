from defaults import *  # noqa
import sys

SECRET_KEY = open(SECRET_KEY_FILE).read()
PASSWORD = open(PASSWORD_FILE).read()
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Emulate an SSL server on localhost
INSTALLED_APPS += (
    "sslserver",
)

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
        'regionfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '.regions.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'region': {
            'handlers': ['regionfile'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fetcher',
        'USER': 'reader',
        'PASSWORD': PASSWORD[0:len(PASSWORD)-1],
        'HOST': 'clarence.eecs.berkeley.edu',
        'PORT': '5432',
    }
DATABASES['logging'] = DATABASES['default']
