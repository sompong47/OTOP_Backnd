"""
Django settings for otop_project project
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url
import pymysql

# ใช้ PyMySQL แทน MySQLdb
pymysql.install_as_MySQLdb()

# -----------------------------
# BASE DIRECTORY
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# ENVIRONMENT
# -----------------------------
ENVIRONMENT = config('ENVIRONMENT', default='local')  # 'local' หรือ 'production'

# -----------------------------
# SECURITY
# -----------------------------
SECRET_KEY = config('SECRET_KEY', default='your-default-secret-key')
DEBUG = config('DEBUG', default=(ENVIRONMENT == 'local'), cast=bool)

if ENVIRONMENT == 'production':
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

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

    'rest_framework',
    'corsheaders',
    'otop_app',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': dj_database_url.parse(
            config('DATABASE_URL', default='mysql://root:password@mysql.railway.internal:3306/railway'),
            conn_max_age=600,
            engine='django.db.backends.mysql',
        )
    }
else:
    # local ใช้ SQLite
    DATABASES = {
        'default': dj_database_url.parse(
            config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
            conn_max_age=600,
            engine='django.db.backends.sqlite3',
        )
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
# STATIC & MEDIA FILES
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -----------------------------
# REST FRAMEWORK
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# -----------------------------
# CORS
# -----------------------------
if ENVIRONMENT == 'production':
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='').split(',')
    CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
else:
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000').split(',')
    CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)

# -----------------------------
# DEFAULT AUTO FIELD
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
