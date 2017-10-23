#-*- coding:utf-8 -*- 
"""
Django settings for SCMDB project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p(s=7em51ftfc4c7&6n7d%!@xyqfe@ca4wx+6hec3=@(@z&26$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'bootstrap_toolkit',
    'servermanage',
    #'devself',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SCMDB.urls'

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

WSGI_APPLICATION = 'SCMDB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zabbix',
        'USER': 'zabbix',
        'PASSWORD':'zabbix@SCM',
        'HOST':'10.183.97.42',
        "PORT":'3306'
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

TEMPLATES = [ 
{ 
'BACKEND': 'django.template.backends.django.DjangoTemplates', 
'DIRS': [os.path.join(BASE_DIR, 'templates'),
], 
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

'''
TEMPLATE_DIRS = (
                 os.path.join(BASE_DIR, 'templates'),
                 )
STATICFILES_DIRS = (
                 os.path.join(BASE_DIR, 'statics'),
                 )
'''

STATIC_URL = '/static/'
STATICFILES_DIRS =(
    os.path.join(BASE_DIR,'static'),
)

'''
import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
'''

import ldap
from django_auth_ldap.config import LDAPSearch
from django_auth_ldap import backend


# Baseline configuration.

AUTHENTICATION_BACKENDS = (  
    'django_auth_ldap.backend.LDAPBackend', 
    'django.contrib.auth.backends.ModelBackend',  
)  


AUTH_LDAP_SERVER_URI = 'ldap://ldap.letv.cn:3268'
AUTH_LDAP_BIND_DN = "username@letv.local"
AUTH_LDAP_BIND_PASSWORD = 'xxxxxxx@'
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
AUTH_LDAP_USER_DN_TEMPLATE = "%(user)s@letv.local"
AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=letv,DC=local", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")


AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "mailNickname",  
    "email": "mail",
}



class _LDAPUser(backend._LDAPUser):
    def _authenticate_user_dn(self, password):
        """
        Binds to the LDAP server with the user's DN and password. Raises
        AuthenticationFailed on failure.
        """
        if self.dn is None:
            raise self.AuthenticationFailed(
                "Failed to map the username to a DN.")

        try:
            sticky = self.settings.BIND_AS_AUTHENTICATING_USER

            self._bind_as(self.dn, password, sticky=sticky)
            ## RED_FLAG: this is the added code, which if both
            ##           AUTH_LDAP_BIND_AS_AUTHENTICATING_USER and
            ##           AUTH_LDAP_USER_SEARCH are set, then re-populate the
            ##           user DN with the result of the search.
            if sticky and self.settings.USER_SEARCH:
                self._search_for_user_dn()

        except self.ldap.INVALID_CREDENTIALS:
            raise self.AuthenticationFailed("User DN/password rejected by LDAP server.")
                        
backend._LDAPUser = _LDAPUser
