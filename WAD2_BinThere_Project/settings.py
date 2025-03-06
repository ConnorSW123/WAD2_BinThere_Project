"""
Django settings for WAD2_BinThere_Project project.

Generated by 'django-admin startproject' using Django 2.2.28.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Join Paths for BASE_DIR and Templates Subdirectory
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

#Static Helper Path Variable to reach the static/images subdirectory
STATIC_DIR = os.path.join(BASE_DIR, 'static')

#Media Helper Path Variable to allocate pathing for videos
MEDIA_DIR = os.path.join(BASE_DIR, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lvnh*)sjrilx$^5v(ee-j3+ucdnvbzs5i%0e%c(hz^2ewh&a4f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CHAPTER 19 ADDITION
#TO DO: Change this to the username of the PythonAnywhere Account we plan on hosting our WebApp.
# First Item is a PythonAnywhere Hosting URL - Using Connor's as default/placeholder at the moment.
# Second Item is device port for hosting webapp locally - Do not remove or Webapp will not host locally.

ALLOWED_HOSTS = ['ConnorSweeney.pythonanywhere.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'BinThere',
    'registration'

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

ROOT_URLCONF = 'WAD2_BinThere_Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]


WSGI_APPLICATION = 'WAD2_BinThere_Project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#Static Files Subdirectory Path
STATICFILES_DIRS = [STATIC_DIR, ]

STATIC_URL = '/static/'

#Media Files Root and URL Variables
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = MEDIA_DIR 
MEDIA_URL = '/media/'

#Login URL Redirection
LOGIN_URL = 'BinThere:login'


# If True, users can register. 
REGISTRATION_OPEN = True 

# If True, the user will be automatically logged in after registering. 
REGISTRATION_AUTO_LOGIN = True 

# The URL that Django redirects users to after logging in.
LOGIN_REDIRECT_URL = 'BinThere:index' 

# The page users are directed to if they are not logged in. 
# # This was set in a previous chapter. 
# The registration package uses this, too. 
LOGIN_URL = 'auth_login'
