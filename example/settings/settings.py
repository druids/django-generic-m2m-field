from settings.base import *  # pylint: disable=E0401


DEBUG = TEMPLATE_DEBUG = THUMBNAIL_DEBUG = True

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'var', 'db', 'sqlite.db'),
        'USER': '',
        'PASSWORD': '',
    },
}

ROOT_URLCONF = 'urls'

STATIC_ROOT = ''

# Additional locations of static files
STATICFILES_DIRS = (
    STATICFILES_ROOT,
)
