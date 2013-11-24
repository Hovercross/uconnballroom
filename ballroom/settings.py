import os

from environment import *

ADMINS = (
     ('Adam Peacock', 'adam@thepeacock.net'),
)

MANAGERS = ADMINS

EMAIL_BACKEND = 'django_ses.SESBackend'
SERVER_EMAIL = 'ballroom-web-app@tigger.peacockhosting.net'
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
	os.path.join(ROOT_PATH, 'static_data'),
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

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

ROOT_URLCONF = 'ballroom.urls'

WSGI_APPLICATION = 'ballroom.wsgi.application'

TEMPLATE_DIRS = (
	os.path.join(ROOT_PATH, 'templates'),
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
	'lists',
	'django.contrib.admin',
	'django.contrib.admindocs',
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

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_tinymce4.html'

FEINCMS_RICHTEXT_INIT_CONTEXT  = {
	'TINYMCE_JS_URL': STATIC_URL + 'admin/js/tinymce/tinymce.min.js'
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
                'log_io': {
                    'level': 'INFO',
                    'class': 'log_io_handler.LogIOHandler',
                    'logstream': 'www_uconnballroom_app',
                    'node': 'tigger.peacockhosting.net'
                 }
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
		'registration': {
			'handlers': ['log_io', 'console'],
			'level': 'DEBUG'
		},
		'lists': {
			'handlers': ['console'],
			'level': 'INFO'
		},
		'mailhandler': {
			'handlers': ['console'],
			'level': 'INFO'
		}
	}
}
