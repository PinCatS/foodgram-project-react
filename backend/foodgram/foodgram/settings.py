import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '..', 'infra', '.env'))

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    default='django-insecure-h6)nh_el*5xi!(z#q^od!@d%7ioux5cyp5+7_%(o%=$b(8*ff+',
)

DEBUG = os.getenv('DJANGO_DEBUG', default='false').lower() == 'true'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', default='').split()

INTERNAL_IPS = os.getenv('DJANGO_INTERNAL_IPS', default='').split()


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "drf_yasg",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "djoser",
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "recipes.apps.RecipesConfig",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = "foodgram.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "foodgram.wsgi.application"


# Database

DATABASES = {
    'default': {
        'ENGINE': os.getenv(
            'DB_ENGINE', default='django.db.backends.postgresql'
        ),
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default=5432),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

DJOSER = {
    'SERIALIZERS': {
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'current_user': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_list': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'subscriptions': ['rest_framework.permissions.IsAuthenticated'],
        'subscribe': ['rest_framework.permissions.IsAuthenticated'],
    },
    'HIDE_USERS': False,
}

# CORS and CSRF

CSRF_TRUSTED_ORIGINS = os.getenv(
    'DJANGO_CSRF_TRUSTED_ORIGINS', default=''
).split()

CORS_ALLOWED_ORIGINS = os.getenv(
    'DJANGO_CORS_ALLOWED_ORIGINS', default=''
).split()

CORS_URLS_REGEX = r'^(/api/|/admin/).*$'

# Internationalization

LOCALE_PATHS = ['recipes/locale']

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/backend/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ORIGIN = os.getenv('DJANGO_MEDIA_ORIGIN', default='')
MEDIA_URL = os.path.join(MEDIA_ORIGIN, 'media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user
AUTH_USER_MODEL = 'users.User'

# Path to data for importdata manage.py command
TEST_DATA_DIR = os.path.join(BASE_DIR, 'static', 'data')

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}
    },
}
