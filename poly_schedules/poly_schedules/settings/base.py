import ldap
import os

from django.core.exceptions import ImproperlyConfigured

from django_auth_ldap.config import LDAPSearch, NestedActiveDirectoryGroupType
from unipath import Path


def get_env_variable(name):
    """ Gets the specified environment variable.

    :param name: The name of the variable.
    :type name: str
    :returns: The value of the specified variable.
    :raises: **ImproperlyConfigured** when the specified variable does not exist.

    """

    try:
        return os.environ[name]
    except KeyError:
        error_msg = "The %s environment variable is not set!" % name
        raise ImproperlyConfigured(error_msg)

# ======================================================================================================== #
#                                         General Management                                               #
# ======================================================================================================== #

ADMINS = (
    ('Alex Kavanaugh', 'kavanaugh.development@outlook.com'),
    ('Chase Kragenbrink', 'ckragenb@calpoly.edu'),
    ('Chris Opperwall', 'copperwa@calpoly.edu')
)

MANAGERS = ADMINS

# ======================================================================================================== #
#                                         General Settings                                                 #
# ======================================================================================================== #

# Local time zone for this installation. Choices can be found here:
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation.
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

DATE_FORMAT = 'l, F d, Y'

TIME_FORMAT = 'h:i a'

DATETIME_FORMAT = 'l, F d, Y h:i a'

DEFAULT_CHARSET = 'utf-8'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Dajax media setting
DAJAXICE_MEDIA_PREFIX = "dajaxice"

ROOT_URLCONF = 'poly_schedules.urls'

# ======================================================================================================== #
#                                          Database Configuration                                          #
# ======================================================================================================== #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'polyschedules',
        'USER': 'polyschedules',
        'PASSWORD': get_env_variable('POLY_SCHEDULES_DB_DEFAULT_PASSWORD'),
        'HOST': 'polyschedules.db.9302206.hostedresource.com',
        'PORT': '3306',
    },
}

# ======================================================================================================== #
#                                            E-Mail Configuration                                          #
# ======================================================================================================== #

# Outgoing email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # This configuration uses the SMTP protocol as a backend
EMAIL_HOST = ''  # The host to use for sending email. Set to empty string for localhost.
EMAIL_PORT = 25  # The port to use. Defaul values: 25, 587
EMAIL_USE_TLS = False  # Whether or not to use SSL (Boolean)
EMAIL_HOST_USER = ''  # The username to use. The full email address is what most servers require.
EMAIL_HOST_PASSWORD = '' # The password to use. Note that only clearText authentication is supported.

# Set the server's email address (for sending emails only)
SERVER_EMAIL = 'Poly Schedules Mail Relay Server <schedules@kavanaughdevelopment.com>'

# ======================================================================================================== #
#                                        Authentication Configuration                                      #
# ======================================================================================================== #

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/login/'

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = 'ldaps://129.65.69.11'

AUTH_LDAP_BIND_DN = get_env_variable('POLY_SCHEDULES_LDAP_USER_DN')
AUTH_LDAP_BIND_PASSWORD = get_env_variable('POLY_SCHEDULES_LDAP_PASSWORD')

AUTH_LDAP_USER_SEARCH = LDAPSearch('OU=Depts,DC=CP-Calpoly,DC=edu', ldap.SCOPE_SUBTREE, '(&(objectClass=user)(sAMAccountName=%(user)s))')
AUTH_LDAP_GROUP_SEARCH = LDAPSearch('OU=Depts,DC=CP-Calpoly,DC=edu', ldap.SCOPE_SUBTREE, '(objectClass=group)')
AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
AUTH_LDAP_FIND_GROUP_PERMS = True

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

AUTH_USER_MODEL = 'core.PolySchedulesUser'

#
# For the scope of this project, only CSC instructors are instructors.
# When the scope expands, more groups can be added.
#
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
     'is_instructor': 'CN=CSC,OU=Depts,DC=CP-Calpoly,DC=edu',
}

# ======================================================================================================== #
#                                      Session/Security Configuration                                      #
# ======================================================================================================== #

# Cookie settings.
SESSION_COOKIE_HTTPONLY = True

# Session expiraton
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('POLY_SCHEDULES_SECRET_KEY')

# ======================================================================================================== #
#                                  File/Application Handling Configuration                                 #
# ======================================================================================================== #

PROJECT_DIR = Path(__file__).ancestor(3)

# The directory that will hold user-uploaded files.
MEDIA_ROOT = PROJECT_DIR.child("media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a trailing slash.
MEDIA_URL = '/media/'

# The directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = PROJECT_DIR.child("static")

# URL prefix for static files. Make sure to use a trailing slash.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    PROJECT_DIR.child("poly_schedules", "core", "static"),
)

# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    PROJECT_DIR.child("poly_schedules", "templates"),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'poly_schedules.core.middleware.TermMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#   'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'dajaxice',
    'poly_schedules.core',
    'poly_schedules.schedules',
    'poly_schedules.preferences',
    'poly_schedules.votes',
    #'south',
)

# ======================================================================================================== #
#                                         Logging Configuration                                            #
# ======================================================================================================== #

RAVEN_CONFIG = {
     'dsn': get_env_variable('POLY_SCHEDULES_SENTRY_DSN'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'dajaxice': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
