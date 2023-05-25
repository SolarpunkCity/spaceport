"""
Django settings for apiserver project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import logging.config
logger = logging.getLogger(__name__)


from . import secrets

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.DJANGO_SECRET_KEY or 'OaOBN2E+brpoRyDMlTD9eTE5PgBtkkl+L7Bzt6pQ5Qr3GS82SH'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG_ENV = os.environ.get('DEBUG', False)
BINDALL_ENV = os.environ.get('BINDALL', False)
DEBUG = DEBUG_ENV or False


PRODUCTION_HOST = 'my.protospace.ca'


# production hosts
ALLOWED_HOSTS = [
    'api.' + PRODUCTION_HOST,
]

if DEBUG:
    ALLOWED_HOSTS += [
        'localhost',
        '127.0.0.1',
        'api.spaceport.dns.t0.vc',
    ]

if BINDALL_ENV:
    ALLOWED_HOSTS = ['*']
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'same-origin'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'apiserver.api',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount', # to support user deletion
    'rest_auth.registration',
    'simple_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

if BINDALL_ENV:
    INSTALLED_APPS += [
        'corsheaders',
    ]
    MIDDLEWARE += [
        'corsheaders.middleware.CorsMiddleware',
    ]
    CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'apiserver.urls'

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

WSGI_APPLICATION = 'apiserver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data/db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,  # increased because generate_backups.py blocks
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': None,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]



# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

if DEBUG:
    STATIC_URL = 'devstatic/'
    MEDIA_URL = 'static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'data/static')
else:
    STATIC_URL = 'https://static.{}/'.format(PRODUCTION_HOST)
    STATIC_ROOT = os.path.join(BASE_DIR, 'data/static')


DEFAULT_RENDERER_CLASSES = (
    'rest_framework.renderers.JSONRenderer',
)

if DEBUG:
    DEFAULT_RENDERER_CLASSES += (
        'rest_framework.renderers.BrowsableAPIRenderer',
    )

DEFAULT_AUTHENTICATION_CLASSES = (
        'rest_framework.authentication.TokenAuthentication',
    )

if DEBUG:
    DEFAULT_AUTHENTICATION_CLASSES += (
	    'rest_framework.authentication.SessionAuthentication',
	)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 500,
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_THROTTLE_CLASSES': ['apiserver.api.throttles.LoggingThrottle'],
    'EXCEPTION_HANDLER': 'apiserver.api.utils.custom_exception_handler'
}

#DEFAULT_LOGGING = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'medium': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)7s] %(message)s'
        },
    },
    'filters': {
        'ignore_stats': {
            '()': 'apiserver.filters.IgnoreStats',
        },
        'ignore_lockout': {
            '()': 'apiserver.filters.IgnoreLockout',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['ignore_stats', 'ignore_lockout'],
            'class': 'logging.StreamHandler',
            'formatter': 'medium'
        },
    },
    'loggers': {
        #'django.db.backends': {
        #    'handlers': ['console'],
        #    'level': 'DEBUG',
        #    'propagate': False,
        #    },
        'gunicorn': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'root': {
        'level': 'DEBUG' if DEBUG else 'INFO',
        'handlers': ['console'],
    },
}
logging.config.dictConfig(LOGGING)

SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USERNAME_MIN_LENGTH = 3
ACCOUNT_AUTHENTICATION_METHOD = 'username'
OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_PRESERVE_USERNAME_CASING = False

if not secrets.EMAIL_USER or not secrets.EMAIL_PASS:
    logger.info('Logging outgoing emails to console')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_PORT = '587'
EMAIL_HOST_USER = secrets.EMAIL_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_PASS
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'Protospace Portal <portal@mg.protospace.ca>'

if DEBUG: logger.info('Debug mode ON')
logger.info('Test logging for each thread')

APP_VERSION = 5  # TODO: automate this

SHELL_PLUS = 'ipython'

#import logging_tree
#logging_tree.printout()
