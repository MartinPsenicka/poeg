from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'poeg_dev',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Caching (good for parler)
# you need to install packages from requirements-dev.txt to use Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SLEVOMAT_TOKEN = 'provide-some-test-token-here'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# RAVEN_CONFIG = {
#     'dsn': 'provide-sentry-dsn-url-here',
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
# }

if DEBUG:
    try:
        print("Enabling django-debug-toolbar...")
        import debug_toolbar
        INSTALLED_APPS += (
            'debug_toolbar',
        )
        MIDDLEWARE += (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )
        DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
    except ImportError:
        pass

