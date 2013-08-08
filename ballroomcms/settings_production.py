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

SERVER_EMAIL='django-ballroomcms@tigger.peacockhosting.net'
ALLOWED_HOSTS = ['208.82.98.186', 'tigger.peacockhosting.net', 'tigger.peacockhosting.net:', 'uconnballroom.com', 'www.uconnballroom.com', 'new.uconnballroom.com']
MEDIA_ROOT = '/var/www/uconnballroom.com/data/cms_user_media/'
STATIC_ROOT = '/var/www/uconnballroom.com/data/cms_static/'

STATIC_URL = '//d1ettfrdwah9wo.cloudfront.net/static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

SERVE_STATIC = False

FEINCMS_RICHTEXT_INIT_CONTEXT  = {
    'TINYMCE_JS_URL': STATIC_URL + 'admin/js/tiny_mce/tiny_mce.js',
    'TINYMCE_CONTENT_CSS_URL': None,
    'TINYMCE_LINK_LIST_URL': None
}
