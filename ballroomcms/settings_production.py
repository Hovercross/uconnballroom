from settings_shared import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

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

MEDIA_ROOT = '/var/www/ballroom/data/cms_user_media/'
STATIC_ROOT = '/var/www/ballroom/cms_static/'