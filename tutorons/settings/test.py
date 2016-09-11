from defaults import *  # noqa

SECRET_KEY = open(SECRET_KEY_FILE).read()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:'
    },
    'logging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:'
    }
}
