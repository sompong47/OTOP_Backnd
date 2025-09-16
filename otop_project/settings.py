"""
Django settings for otop_project project - Railway Deployment Version
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
# Railway sets this environment variable automatically
RAILWAY_ENVIRONMENT = os.environ.get('RAILWAY_ENVIRONMENT_NAME')
RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN')

# -----------------------------
# SECURITY SETTINGS
# -----------------------------
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-please')

# Debug mode
if RAILWAY_ENVIRONMENT:
    DEBUG = config('DEBUG', default=False, cast=bool)
else:
    DEBUG = config('DEBUG', default=True, cast=bool)

# Allowed hosts
if RAILWAY_ENVIRONMENT:
    ALLOWED_HOSTS = [
        '.railway.app',
        '.up.railway.app',
        'localhost',
        '127.0.0.1',
    ]
    # เพิ่ม custom domain ถ้ามี
    if RAILWAY_PUBLIC_DOMAIN:
        ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']

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
    'whitenoise.middleware.WhiteNoiseMiddleware',  # สำหรับ static files
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
        'DIRS': [BASE_DIR / 'templates'],
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
    # Production database (Railway PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Local development (SQLite)
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
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -----------------------------
# INTERNATIONALIZATION
# -----------------------------
LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

# -----------------------------
# STATIC FILES & MEDIA
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static files handling for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
] if (BASE_DIR / 'static').exists() else []

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------
# REST FRAMEWORK CONFIGURATION
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# -----------------------------
# JWT CONFIGURATION
# -----------------------------
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# -----------------------------
# CORS CONFIGURATION
# -----------------------------
if RAILWAY_ENVIRONMENT:
    # Production CORS settings
    CORS_ALLOWED_ORIGINS = [
        "https://your-frontend-domain.vercel.app",  # เปลี่ยนเป็น domain จริงของ frontend
        "https://your-frontend-domain.netlify.app",  # ถ้าใช้ Netlify
    ]
    # เพิ่ม origins อื่นๆ ตามต้องการ
    additional_origins = config('CORS_ALLOWED_ORIGINS', default='').split(',')
    if additional_origins and additional_origins[0]:  # ตรวจสอบว่าไม่ใช่ string ว่าง
        CORS_ALLOWED_ORIGINS.extend(additional_origins)
    
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_ALL_ORIGINS = False
else:
    # Development CORS settings
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True

# Headers ที่อนุญาต
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# -----------------------------
# SECURITY SETTINGS FOR PRODUCTION
# -----------------------------
if RAILWAY_ENVIRONMENT:
    # Security settings for production
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_REFERRER_POLICY = 'same-origin'
    
    # SSL settings (Railway provides HTTPS automatically)
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Cookie security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # X-Frame-Options
    X_FRAME_OPTIONS = 'DENY'

# -----------------------------
# LOGGING CONFIGURATION
# -----------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple' if DEBUG else 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'otop_app': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# -----------------------------
# SWAGGER/OPENAPI SETTINGS
# -----------------------------
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
}

# -----------------------------
# DEFAULT SETTINGS
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cache (ใช้ในกรณีที่ต้องการ caching)
if RAILWAY_ENVIRONMENT:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_cache_table',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Email settings (สำหรับ production ถ้าต้องการส่ง email)
if RAILWAY_ENVIRONMENT:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yoursite.com')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

print(f"🚀 Django running in {'PRODUCTION' if RAILWAY_ENVIRONMENT else 'DEVELOPMENT'} mode")
if RAILWAY_ENVIRONMENT:
    print(f"🔗 Public domain: {RAILWAY_PUBLIC_DOMAIN}")
    print(f"🛡️  Security: SSL={SECURE_SSL_REDIRECT}, HSTS={SECURE_HSTS_SECONDS}s")