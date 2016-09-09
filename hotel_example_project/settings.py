import os
import mongoengine
import tokenlib
from decouple import config
from logging import getLogger
from logging.config import dictConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS',
                       cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = config('INSTALLED_APPS',
                        cast=lambda v: [s.strip() for s in v.split(',')])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotel_example_project.urls'

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

WSGI_APPLICATION = 'hotel_example_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DEFAULT_DB_ENGINE', cast=str),
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = config('STATIC_ROOT', default=None, cast=str)

# LOGGING CONFIG
LOG_PATH = config('LOG_PATH', cast=str)
LOG_LEVEL = config('LOG_LEVEL', cast=str)
LOG_HANDLERS = config('LOG_HANDLERS',
                      cast=lambda l: [handler for handler in l.split(',')])
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s][pid:%(process)d][%(funcName)s]:%(lineno)d: - %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] - %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOG_PATH,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': LOG_HANDLERS,
            'propagate': True,
        },
        'hotel_example': {
            'handlers': LOG_HANDLERS,
            'propagate': True,
        }
    }
}

dictConfig(LOGGING)

# Email configuration
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

# AUTH_USER_MODEL = 'hotel_example.User'

# Auth settings
TOKEN_MANAGER = tokenlib.TokenManager(secret=config('EMAIL_PORT', cast=str,
                                                    default='I_LIKE_UNICORNS!'))
HASH_ROUNDS = 2000
HASH_SALT_SIZE = 16


# MongoDB
_MONGODB_USER = config('MONGODB_USER', cast=str, default=None)
_MONGODB_PASSWD = config('MONGODB_PASSWORD', cast=str, default=None)
_MONGODB_HOST = config('MONGODB_HOST', cast=str, default=None)
_MONGODB_NAME = config('MONGODB_NAME', cast=str, default=None)
if '' not in (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST):
    _MONGODB_DATABASE_HOST = 'mongodb://{}:{}@{}/{}'.format(
        _MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)
else:
    _MONGODB_DATABASE_HOST = 'mongodb://localhost/{}'.format(
        _MONGODB_NAME)

mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)
# SESSION_ENGINE = 'mongoengine.django.sessions'  # optional
