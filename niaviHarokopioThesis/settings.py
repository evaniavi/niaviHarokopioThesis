"""
Django settings for niaviHuaThesis project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import ldap
from django.utils.translation import gettext_noop
from decouple import config
from django.conf import global_settings
from django_auth_ldap.config import LDAPSearch, LDAPGroupQuery, GroupOfNamesType
from pathlib import Path
from django.contrib.messages import constants as messages


MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STAT=os.path.join(BASE_DIR,'static')
TAMPLATES_DIR=os.path.join(BASE_DIR,'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'personal',
    'bootstrap5',
    'django_filters',
    'captcha',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'niaviHarokopioThesis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TAMPLATES_DIR],
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

WSGI_APPLICATION = 'niaviHarokopioThesis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'), 
        'USER' : config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST' : config('HOST'),
        'PORT' : config('PORT'),


    }
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)


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
LOGIN_REDIRECT_URL = 'home'
#Logout redirection
LOGOUT_REDIRECT_URL = 'home'

AUTH_LDAP_CACHE_TIMEOUT = 3600
AUTH_LDAP_SERVER_URI = config('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = config('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = config('AUTH_LDAP_BIND_PASSWORD')
AUTH_LDAP_START_TLS = config('AUTH_LDAP_START_TLS') == 'True'
AUTH_LDAP_BASE_DN = config('AUTH_LDAP_BASE_DN')
AUTH_LDAP_USER_SEARCH_ATTR = config('AUTH_LDAP_USER_SEARCH_ATTR')
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_BASE_DN,
    ldap.SCOPE_SUBTREE,
    "(" + AUTH_LDAP_USER_SEARCH_ATTR + "=%(user)s)"
)
AUTH_LDAP_SN = config('AUTH_LDAP_SN')
AUTH_LDAP_EMAIL = config('AUTH_LDAP_EMAIL')
AUTH_LDAP_TITLE = config('AUTH_LDAP_TITLE')
AUTH_LDAP_DEPARTMENT = config('AUTH_LDAP_DEPARTMENT')
AUTH_LDAP_GIVEN_NAME = config('AUTH_LDAP_GIVEN_NAME')
AUTH_LDAP_USER_ATTR_MAP = {
  "first_name" : AUTH_LDAP_GIVEN_NAME,
  "last_name": AUTH_LDAP_SN,
  "email" : AUTH_LDAP_EMAIL,
  "department" : AUTH_LDAP_DEPARTMENT,
   "title" : AUTH_LDAP_TITLE
}
AUTH_LDAP_INTERNAL_DOMAIN = config('AUTH_LDAP_INTERNAL_DOMAIN')
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose' : {
            'format' : '{asctime} {levelname} {message}',
            'style' : '{',
        },
    },
    'handlers': {
        'console' : {
            'class' : 'logging.StreamHandler',
           },
        'file' : {
            'class' : 'logging.FileHandler',
            'filename' : '/Users/USER/Desktop/log/django_app.log',
            'formatter' : 'verbose'
        }
    },
    'loggers': {
        'django_auth_ldap': {
            'level': 'DEBUG',
            'handlers': ['file', 'console']
            },
        'huaskel' : {
            'level' : 'DEBUG',
            'handlers': ['file', 'console'],
            }
        }
}



# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'


LANGUAGE_CODE = 'el-GR'
LANGUAGES = [
    ('en-gb', gettext_noop('British English')),
    ('el', gettext_noop('Greek')),]

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
CRISPY_TAMPLATE_PACK="bootstrap4"

MEDIA_URL = '/media/'

MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))


DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_USE_TLS = config('EMAIL_USE_TLS',bool)
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')

X_FRAME_OPTIONS = 'SAMEORIGIN'
