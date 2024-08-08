"""
Django settings for backend project.
"""
import os
from datetime import timedelta
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v+cpha+j%2o4+nge+7$=1v^e#al^etdx+jd(xgc&tud8j55+0i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# -------------- START - CORS Setting --------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://*.127.0.0.1",
    "http://localhost",
]
# -------------- END - CORS Setting -----------------

# APPEND_SLASH=True: URLs without trailing slash redirect to URL with slash, potentially losing POST data.
APPEND_SLASH = False
# Site ID is used for Django Allauth
SITE_ID = 1


# Application definition
INSTALLED_APPS = [
    # ========================
    # Django apps
    # ========================
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for Django Allauth
    #=========================
    # Third party apps
    # ========================
    "corsheaders",
    'rest_framework',
    "drf_yasg",
    # ========================
    # Django Allauth
    # ========================
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.microsoft',
    'allauth.socialaccount.providers.line',
    # ========================
    # Local apps
    # ========================
    'custom_jwt', # Custom JWT (override some of the default JWT settings)
    'authentication', # Custom 3rd party authentication
    'dashboard', # Demo dashboard
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ========================
    "corsheaders.middleware.CorsMiddleware",
    # ========================
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ========================
    # Django Allauth
    # ========================
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

ASGI_APPLICATION = 'backend.asgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "Y/m/d H:i:s"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Taipei"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "api/__hidden_statics/"
STATIC_ROOT = "staticfiles"


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------------- START - Allauth Setting --------------
SOCIALACCOUNT_PROVIDERS = {}
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
MS_CLIENT_ID = os.environ.get("MS_CLIENT_ID", None)
LINE_CLIENT_ID = os.environ.get("LINE_CLIENT_ID", None)

if GOOGLE_CLIENT_ID:
    SOCIALACCOUNT_PROVIDERS['google'] = {
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': os.environ.get("GOOGLE_CLIENT_SECRET"),
            'key': ''
        }
    }

if MS_CLIENT_ID:
    SOCIALACCOUNT_PROVIDERS['microsoft'] = {
        "APPS": [
            {
                "client_id": MS_CLIENT_ID,
                "secret": os.environ.get("MS_CLIENT_SECRET"),
                "settings": {
                    "tenant": "common",
                    # Optional: override URLs (use base URLs without path)
                    "login_url": "https://login.microsoftonline.com",
                    "graph_url": "https://graph.microsoft.com",
                }
            }
        ]
    }

if LINE_CLIENT_ID:
    SOCIALACCOUNT_PROVIDERS['line'] = {
        'APP': {
            'client_id': LINE_CLIENT_ID,
            'secret': os.environ.get("LINE_CLIENT_SECRET"),
        },
        "SCOPE": ['profile', 'openid', 'email']
    }

SOCIALACCOUNT_LOGIN_ON_GET=True # Allow login via GET request
ACCOUNT_LOGOUT_ON_GET=True # Allow logout via GET request
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_ADAPTER = 'authentication.adapter.MyAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'authentication.adapter.MySocialAccountAdapter'

# --------------- END - Allauth Setting ----------------


# -------------- START - Swagger Setting --------------

USE_X_FORWARDED_HOST = True

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Token(add prefix `Bearer` yourself)": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
    "LOGIN_URL": "/api/__hidden_dev_dashboard/login",
    "LOGOUT_URL": "/api/__hidden_admin/logout/?next=/api/__hidden_swagger",
}

# --------------- END - Swagger Setting----------------

# ---------------------------- START - REST_FRAMEWORK setting --------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Support JWT token
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # Support session authentication
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        # Only authenticated users can access API
        "rest_framework.permissions.IsAuthenticated",
    ),
    # Use JSONRenderer as default renderer for API instead of REST framework's Browsable API
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}
# ----------------------------- END - REST_FRAMEWORK setting ----------------------------


# -------------- Start - SimpleJWT Setting --------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=3600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
# -------------- END - SimpleJWT Setting --------------