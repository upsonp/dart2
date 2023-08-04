"""
Django settings for dart2 project.

Generated by 'django-admin startproject' using Django 3.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
import environ

from django.utils.translation import gettext_lazy as _
# read the private data from the environment file
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

ASGI_APPLICATION = 'dart2.asgi.application'

# These apps are part of the core functionality for DART
# --- Please do not modify unless you know what you're doing ---
REQUIRED_APPS = [
    'core',
    'docs',
    'biochem',
    'bio_tables',
]

# Add Registered applications here for auto loading parsers, URLs and APIs
REGISTERED_APPS = REQUIRED_APPS + [
]

# Application definition
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # adds pretty icons to the mix
    'django_bootstrap_icons',

    # useful django extensions
    'django_extensions',
    'crispy_forms',
    'crispy_bootstrap5',

    # allows for filtering content
    'django_filters',

    # allows authentication, requires django.contrib.sites
    'allauth',
    'allauth.account',

    # bi-directional communication with user
    'channels',

    # bootstrap for css styling
    'bootstrap5',

] + REGISTERED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # locale middle ware for translations
    'django.middleware.locale.LocaleMiddleware',
    # whitenoise for serving static files
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

SITE_ID = 1
# AUTH_USER_MODEL = 'core.User'
LOGIN_REDIRECT_URL = ""
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

ROOT_URLCONF = 'dart2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'dart2.wsgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_ROUTERS = ["dart2.db_routers.BioChemRouter",]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, env('LOCAL_DATABASE')),
    },
}
if env.bool("BIOCHEM_ENABLED", default=False):
    DATABASES['mirror_biochem'] = {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': env('BIOCHEM_NAME'),
        'USER': env('BIOCHEM_USER'),
        'PASSWORD': env('BIOCHEM_PASS'),
        'PORT': env('BIOCHEM_PORT'),
        'HOST': env('BIOCHEM_HOST'),
    }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

FORMATTERS = (
    {
        "simple": {
            "format": "{levelname} {asctime:s} {module} {filename} {lineno:d} {funcName} {message}",
            "style": "{"
        },
        "verbose": {
            "format": "{levelname} {asctime:s} {threadName} {thread:d} {module} {filename} {lineno:d} {name} "
                      "{funcName} {process:d} {message}",
            "style": "{"
        },
    },
)

HANDLERS = {
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
    "info_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{BASE_DIR}/logs/info.log",
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "simple",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5  # 5 MB
    },
    "test_handler": {
        "class": "logging.FileHandler",
        "filename": f"{BASE_DIR}/logs/test.log",
        "mode": "w",
        "encoding": "utf-8",
        "formatter": "verbose",
    },
    "error_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{BASE_DIR}/logs/error.log",
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "verbose",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5  # 5 MB
    }
}

LOGGERS = (
    {
        "django": {
            "handlers": ["console", "info_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ['error_handler'],
            "level": "ERROR",
            "propagate": False,
        },
        "dart": {
            "handlers": ["console", "error_handler"],
            "level": "WARNING",
            "propagate": True
        },
        "dart.debug": {
            "handlers": ["console", "info_handler", "error_handler"],
            "level": "DEBUG",
            "propagate": True
        },
        "dart.test": {  # use this logger for unit testing
            "handlers": ["console", "test_handler"],
            "level": "DEBUG",
            "propagate": False
        }
    },
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS[0],
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = env("TIME_ZONE", cast=str, default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
BS_ICONS_CUSTOM_PATH = 'dart/icons/'
BS_ICONS_CACHE = os.path.join(STATIC_ROOT, 'img')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, '../settings'),
]
