# coding: utf-8
"""
Django settings for titor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
print "BASE_DIR"
print BASE_DIR

print "PROJECT_ROOT"
print PROJECT_ROOT

# ---- 静的ファイルは/static/に配置 ----
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
)
#STATICFILES_DIRS = (
#        os.path.join(STATIC_ROOT, 'static'),
#)

print "STATIC_ROOT"
print STATIC_ROOT

print "STATICFILES_DIRS"
print STATICFILES_DIRS
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g92b#ji+23$mt%k_=)v)c6duusty#$#$a1kz-^p*zc4c=rt-g#'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('HOSTNAME'):
    hostname = os.environ.get('HOSTNAME')
else:
    hostname = 'localhost'

ALLOWED_HOSTS = []

if 'titor' in hostname:
    DEBUG = False
    TEMPLATE_DEBUG = False
    ALLOWED_HOSTS = ['*']
    PRODUCTION = True
else:
    DEBUG = True
    TEMPLATE_DEBUG = True
    PRODUCTION = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'chartjs',
    'titorApp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'titor.urls'

WSGI_APPLICATION = 'titor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

import dj_database_url

if 'titor' in hostname:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=500)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '..', 'titorApp'),
)
