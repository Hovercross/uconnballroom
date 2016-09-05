import os
import email.utils

import dj_database_url
import configparser

config = configparser.ConfigParser()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
defaultConfigFilePath = os.path.abspath(os.path.join(BASE_DIR, "..", "settings.ini"))

CONFIG_FILE = os.environ.get("DJANGO_CONFIG_FILE", defaultConfigFilePath)

config.read(CONFIG_FILE)

DATABASE_URL = config['database']['URL']

DEBUG = config.getboolean('debug', 'DEBUG')


MEDIA_ROOT = config['files']['MEDIA_ROOT']
STATIC_ROOT = config['files']['STATIC_ROOT']

MEDIA_URL = config['urls']['MEDIA_URL']
STATIC_URL = config['urls']['STATIC_URL']

AWS_ACCESS_KEY_ID = config['cloud'].get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config['cloud'].get('AWS_SECRET_ACCESS_KEY')

MAILGUN_KEY = config['cloud'].get('MAILGUN_KEY')

BROKER_URL = config['celery'].get('BROKER_URL')
CELERY_RESULT_BACKEND = config['celery'].get('CELERY_RESULT_BACKEND')

#Serve static is true by default is DEBUG is true
SERVE_STATIC = config.getboolean('debug', 'SERVE_STATIC')
ALLOWED_HOSTS = [host.strip() for host in config['production'].get('ALLOWED_HOSTS', "").split(",")]

STATICFILES_STORAGE = config['files']['STORAGE']

EMAIL_BACKEND = config['email']['BACKEND']
SERVER_EMAIL = config['email']['SERVER_ADDRESS']

TIME_ZONE = config['internationalization']['TIME_ZONE']
LANGUAGE_CODE = config['internationalization']['LANGUAGE_CODE']

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

ADMINS = [email.utils.parseaddr(a.strip()) for a in config['email']['ERRORS'].split(",")]
MANAGERS = [email.utils.parseaddr(a.strip()) for a in config['email']['MANAGERS'].split(",")]

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static_data'),
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#	 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'e=5u$-o+p7mm4hmz5fwc3_npgkzt!%ex3@0(qf#6bhb8*qxd#v'



MIDDLEWARE_CLASSES = (
	'corsheaders.middleware.CorsMiddleware',
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


CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
#	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'feincms',
	'mptt',
	'feincms.module.page',
	'content',
	'adminsortable',
	'easy_thumbnails',
	'biographies',
	'galleries',
	'registration',
	'mailhandler',
	'dashboard',
	'lists',
	'corsheaders',
    'rest_framework',
	'django.contrib.admin',
	'django.contrib.admindocs',
)


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

MIGRATION_MODULES = {
	'page': 'migrate.page',
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'feincms.context_processors.add_page_if_missing',
            ],
        },
    },
]

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
		},
		'lists': {
			'handlers': ['console'],
			'level': 'INFO'
		},
		'mailhandler': {
			'handlers': ['console'],
			'level': 'INFO'
		},
		'dashboard': {
			'handlers': ['console'],
			'level': 'INFO'
		}
	}
}
