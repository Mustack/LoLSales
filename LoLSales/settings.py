# Django settings for LoLSales project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_DIR = os.path.join( os.path.dirname( __file__ ), '..' )

ADMINS = (
	# ('Your Name', 'your_email@example.com'),
	('Jean-Luc Martin', 'mail@jlmart.in'),
	('Sam Wilson', 'tecywiz121@hotmail.com'),
)

MANAGERS = ADMINS

# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
# 		'NAME': '',                      # Or path to database file if using sqlite3.
# 		'USER': '',                      # Not used with sqlite3.
# 		'PASSWORD': '',                  # Not used with sqlite3.
# 		'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
# 		'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
# 	}
# }

import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'app','media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(BASE_DIR, 'LoLSales', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rb#l1n4v(8kra4_7p^tp7d8=u4@q)+$m9v6b(bj27v^dn0d9hi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'LoLSales.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'LoLSales.wsgi.application'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	BASE_DIR + '/LoLSales/templates',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'gunicorn',
	'kombu.transport.django',
	'djcelery',
	'django_extensions',
	'south',
	'registration',
	'djrill',
	'crispy_forms',
	'champions',
	'accounts',
	'pages',
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
)

# Registration Settings

ACCOUNT_ACTIVATION_DAYS = 2

# Djrill Settings

MANDRILL_API_KEY = '9f15b814-82f1-4456-b843-b6339cda2df2'
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
DEFAULT_FROM_EMAIL = 'webmaster@lolsales.example.com'

# Crispy Forms Settings

CRISPY_TEMPLATE_PACK = 'bootstrap'
CRISPY_FAIL_SILENTLY = not DEBUG

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}

BROKER_BACKEND = 'django'

# Load local configuration options (like db username/password)
try:
	from .local_settings import *
except ImportError:
	pass

import djcelery
djcelery.setup_loader()
