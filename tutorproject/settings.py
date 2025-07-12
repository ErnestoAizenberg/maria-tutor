import os
from pathlib import Path

import dotenv
from typing import Optional

from .logger import setup_logger

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.load_dotenv(BASE_DIR / ".env")

logger = setup_logger(log_file="settings.log")
DEBUG: bool = os.getenv("DEBUG", "True") == "True"
SECRET_KEY: str = str(os.getenv("SECRET_KEY"))

TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env!")

MINI_APP_URL: str = "https://mariaseredinskaya.pythonanywhere.com"
ALLOWED_HOSTS = ["mariaseredinskaya.pythonanywhere.com", "localhost", "127.0.0.1", "*"]

INSTALLED_APPS = [
    "jazzmin",
    "ckeditor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "main",
    "telegram_bot.apps.TelegramBotConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "main.middleware.CustomErrorMiddleware",
]

ROOT_URLCONF = "tutorproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.context_processors.teacher_context",
            ],
        },
    },
]

WSGI_APPLICATION = "tutorproject.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

CKEDITOR_CONFIGS = {
    "default": {
        "contentsCss": "/static/css/ckeditor-content.css",
        "bodyClass": "article-content",
        "allowedContent": True,
        "extraPlugins": "stylesheetparser",
        "toolbar_Full": [
            ["Styles", "Format", "Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList", "Blockquote"],
            ["Image", "Table", "Link"],
            ["Source"],
        ],
    },
}

HTML_MINIFY = True
EXCLUDE_FROM_MINIFYING = ("/admin/", "/api/")
KEEP_COMMENTS_ON_MINIFYING = False

logger.info(f"Debug is {DEBUG}")
