"""
Django settings for otop_project project - Railway PostgreSQL Version
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# ENVIRONMENT DETECTION
# -----------------------------
RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT_NAME')

# -----------------------------
# SECURITY SETTINGS
# -----------------------------
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
DEBUG = config('DEBUG', default=not bool(RAILWAY_ENVIRONMENT), cast=bool)

# Allowed hosts
if RAILWAY_ENVIRONMENT:
    ALLOWED_HOSTS = ['.railway.app', '.up.railway.app', 'localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# -----------------------------
# APPLICATION DEFINITION
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg',
    
    # Local apps
    'otop_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'otop_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'otop_project.wsgi.application'

# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------
if RAILWAY_ENVIRONMENT:
    # Production - Railway PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Development - SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC FILES
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------
# REST FRAMEWORK
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# -----------------------------
# JWT CONFIGURATION
# -----------------------------
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# -----------------------------
# CORS CONFIGURATION
# -----------------------------
if RAILWAY_ENVIRONMENT:
    # Production CORS
    CORS_ALLOWED_ORIGINS = [
        "https://your-frontend.vercel.app",  # แก้เป็น domain จริง
    ]
    cors_origins = config('CORS_ALLOWED_ORIGINS', default='').split(',')
    if cors_origins and cors_origins[0]:
        CORS_ALLOWED_ORIGINS.extend(cors_origins)
    CORS_ALLOW_CREDENTIALS = True
else:
    # Development CORS
    CORS_ALLOW_ALL_ORIGINS = True

# -----------------------------
# SECURITY (Production)
# -----------------------------
if RAILWAY_ENVIRONMENT:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# -----------------------------
# DEFAULT SETTINGS
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Debug output
print(f"🔧 Environment: {'PRODUCTION' if RAILWAY_ENVIRONMENT else 'DEVELOPMENT'}")
print(f"🛢️  Database: {'PostgreSQL' if RAILWAY_ENVIRONMENT else 'SQLite'}")