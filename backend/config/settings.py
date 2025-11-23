from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key-change-me')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# REPLIT Configuration
REPLIT_DOMAIN = os.getenv('REPLIT_DEV_DOMAIN', os.getenv('REPLIT_DOMAINS', ''))
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
if REPLIT_DOMAIN:
    ALLOWED_HOSTS.append(REPLIT_DOMAIN)
ALLOWED_HOSTS.extend(os.getenv('ALLOWED_HOSTS', '').split(','))
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]

DEV_MODE = not (BASE_DIR / 'frontend' / 'build' / 'index.html').exists()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [] if DEV_MODE else [BASE_DIR / 'frontend' / 'build'],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        # This tells Django: "Look for the DATABASE_URL environment variable.
        # If you don't find it, use this local sqlite file instead."
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEV_MODE:
    STATICFILES_DIRS = [BASE_DIR / 'frontend' / 'build' / 'static']
else:
    STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOWED_ORIGINS = ['http://localhost:5000', 'http://localhost:3000', 'http://0.0.0.0:5000', 'http://127.0.0.1:5000']
if REPLIT_DOMAIN:
    CORS_ALLOWED_ORIGINS.extend([f'https://{REPLIT_DOMAIN}', f'http://{REPLIT_DOMAIN}'])
CORS_ALLOWED_ORIGINS.extend([
    origin.strip() for origin in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if origin.strip()
])

CORS_ALLOW_CREDENTIALS = True

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

CSRF_TRUSTED_ORIGINS = ['http://localhost:5000', 'http://localhost:3000', 'http://0.0.0.0:5000', 'http://127.0.0.1:5000']
if REPLIT_DOMAIN:
    CSRF_TRUSTED_ORIGINS.extend([f'https://{REPLIT_DOMAIN}', f'http://{REPLIT_DOMAIN}'])
CSRF_TRUSTED_ORIGINS.extend([
    origin.strip() for origin in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()
])

# MODIFIED: Added these settings to allow Vercel to maintain login session
# For development (HTTP), disable secure flag. Production will override this.
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = DEBUG == False  # Only secure in production
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = DEBUG == False  # Only secure in production
SESSION_COOKIE_HTTPONLY = True


EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@example.com')
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', 30))

GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID', '')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET', '')
GOOGLE_OAUTH_REDIRECT_URI = os.getenv('GOOGLE_OAUTH_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')

EMAIL_VERIFICATION_TIMEOUT_MINUTES = int(os.getenv('EMAIL_VERIFICATION_TIMEOUT_MINUTES', 10))