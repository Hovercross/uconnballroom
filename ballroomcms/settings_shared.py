import os

ADMINS = (
     ('Adam Peacock', 'adam@thepeacock.net'),
)

EMAIL_BACKEND = 'django_ses.SESBackend'

SERVER_EMAIL = 'ballroom-web-app@tigger.peacockhosting.net'

MANAGERS = ADMINS

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

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.abspath(os.path.join(os.path.split(__file__)[0], '../', 'static_data')),
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

AWS_ACCESS_KEY_ID = 'AKIAJZOPPO2KOEXOY3TQ'
AWS_SECRET_ACCESS_KEY = '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'

MAILGUN_KEY = 'key-7w2cv-5b8w8zn9n-bl8g625i3-re27z0'

SECRET_KEY = 'e=5u$-o+p7mm4hmz5fwc3_npgkzt!%ex3@0(qf#6bhb8*qxd#v'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	  'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'content.middleware.DisableClientSideCachingMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ballroomcms.urls'

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
	'django_ses',
	'feincms',
	'mptt',
	'feincms.module.page',
	'content',
	'adminsortable',
	'south',
	'easy_thumbnails',
	'biographies',
	'galleries',
	'registration',
	'mailhandler',
	'dashboard',
	# Uncomment the next line to enable the admin:
	 'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
)

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.static', 'django.contrib.auth.context_processors.auth', 'feincms.context_processors.add_page_if_missing', 'django.core.context_processors.request')

THUMBNAIL_ALIASES = {
	'': {
		'galleryThumb': {'size': (100, 100), 'crop': 'Smart'},
		'galleryLightbox': {'size': (800, 800), 'crop': False},
		'adminThumb': {'size': (100, 100), 'crop': 'Smart'},
		'imageContent': {'size': (700, 0), 'crop': False}
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
	'biographies': 'migrate.biographies',
	'galleries': 'migrate.galleries',
}

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
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
		},
		'console':{
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
		'registration': {
			'handlers': ['console'],
			'level': 'DEBUG'
			
		}
	}
}
