import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ballroom',
        'USER': 'ballroom',
        'PASSWORD': 'D8HKENCpYarHeFb0vHoJ8D3APZ4LxlICf1hYYujeAM1x2cFU6b',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

DEBUG=True
TEMPLATE_DEBUG=True

ROOT_PATH = os.path.abspath(os.path.join(os.path.split(__file__)[0], '../'))

MEDIA_ROOT = os.path.join(ROOT_PATH, 'user_media')
STATIC_ROOT = ''

SERVE_STATIC = True

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

AWS_ACCESS_KEY_ID = 'AKIAJZOPPO2KOEXOY3TQ'
AWS_SECRET_ACCESS_KEY = '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'

MAILGUN_KEY = 'key-7w2cv-5b8w8zn9n-bl8g625i3-re27z0'