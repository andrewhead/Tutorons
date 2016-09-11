#! /usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DEPS_DIR = os.path.join(BASE_DIR, 'deps')
REGEX_SVG_ENDPOINT = "http://regexsvg.tutorons.com/"


# Security

SECRET_KEY_FILE = "/etc/django/tutorons.key"
PASSWORD_FILE = "/etc/django/password.key"
CORS_ORIGIN_ALLOW_ALL = True  # We're okay accepting connections from anywhere
DEFAULT_DICTIONARY = os.path.join('tutorons', 'regex', 'google-10000-english-usa.txt')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'tutorons.common',
    'tutorons.packages',
    'tutorons'
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tutorons.middleware.crossdomain-middleware.XsSharing',
)

ROOT_URLCONF = 'tutorons.urls'

WSGI_APPLICATION = 'tutorons.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'logging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'logs.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = []
