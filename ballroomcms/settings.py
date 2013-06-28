# Django settings for ballroomcms project.

import os

if os.environ.get('BALLROOMCMS_ENVIRONMENT') == 'PRODUCTION':
	PROD = True
else:
	PROD = False

DEBUG = not PROD
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Adam Peacock', 'adam@thepeacock.net'),
)

MANAGERS = ADMINS

if PROD:
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
	        'NAME': 'ballroomcms',                      # Or path to database file if using sqlite3.
	        # The following settings are not used with sqlite3:
	        'USER': 'ballroomcms',
	        'PASSWORD': 'qieorugheiourguneurghiqufhiadfv',
	        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
	        'PORT': '',                      # Set to empty string for default.
	    }
	}
else:	
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
	        'NAME': os.path.abspath(os.path.join(os.path.split(__file__)[0], '../', 'data.db')),                      # Or path to database file if using sqlite3.
	        # The following settings are not used with sqlite3:
	        'USER': '',
	        'PASSWORD': '',
	        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
	        'PORT': '',                      # Set to empty string for default.
	    }
	}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

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
# Example: "/var/www/example.com/media/"
if PROD:
	MEDIA_ROOT = '/var/www/ballroom/data/cms_user_media/'
else:
	MEDIA_ROOT = os.path.abspath(os.path.join(os.path.split(__file__)[0], '../', 'user_media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
if PROD:
	STATIC_ROOT = '/var/www/ballroom/cms_static/'
else:
	STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(os.path.split(__file__)[0], '../', 'static_data')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e=5u$-o+p7mm4hmz5fwc3_npgkzt!%ex3@0(qf#6bhb8*qxd#v'

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
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ballroomcms.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ballroomcms.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(os.path.split(__file__)[0], '../', 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'feincms',
    'mptt',
    'feincms.module.page',
    'content',
	'adminsortable',
	'south',
    'easy_thumbnails',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.static', 'django.contrib.auth.context_processors.auth')

THUMBNAIL_ALIASES = {
    '': {
        'galleryThumb': {'size': (200, 200), 'crop': True},
        'galleryLarge': {'size': (800, 800), 'crop': False},
		'adminThumb': {'size': (100, 100), 'crop': True}
    },
}

FEINCMS_RICHTEXT_INIT_CONTEXT  = {
    'TINYMCE_JS_URL': STATIC_URL + 'admin/js/tiny_mce/tiny_mce.js',
    'TINYMCE_CONTENT_CSS_URL': None,
    'TINYMCE_LINK_LIST_URL': None
}

SOUTH_MIGRATION_MODULES = {
	'page': 'migrate.page',
	'content': 'migrate.content',
	
    }

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
