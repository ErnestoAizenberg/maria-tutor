import logging
import logging.config
import os
from pathlib import Path
from typing import Final

import dotenv

dotenv.load_dotenv(".env")

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True, mode=0o755)

LOGGING: Final[dict] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                %(asctime)s %(levelname)s %(module)s
                %(message)s %(pathname)s %(lineno)d
            """,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_errors": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "errors.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "file_access": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "access.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "json",
            "encoding": "utf-8",
        },
        "file_django": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "when": "midnight",
            "backupCount": 30,
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        "file_business": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "business.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "json",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_django"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file_errors", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": os.getenv("DB_LOG_LEVEL", "WARNING"),
            "propagate": False,
        },
        "access": {
            "handlers": ["file_access"],
            "level": os.getenv("ACCESS_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "main": {
            "handlers": ["file_business", "console"],
            "level": os.getenv("APP_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

logging.config.dictConfig(LOGGING)

DEBUG: Final[bool] = os.getenv("DEBUG", "True") == "True"
SECRET_KEY: Final[str] = str(os.getenv("SECRET_KEY", ""))

TELEGRAM_BOT_TOKEN: Final[str] = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env!")

MINI_APP_URL: Final[str] = "https://mariaseredinskaya.pythonanywhere.com"
ALLOWED_HOSTS: Final[list[str]] = [
    "mariaseredinskaya.pythonanywhere.com",
    "localhost",
    "127.0.0.1",
    "*",
]

INSTALLED_APPS: list[str] = [
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

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "main.middleware.CustomErrorMiddleware",
    "main.logging_middleware.RequestLoggingMiddleware",
]

ROOT_URLCONF: Final[str] = "tutorproject.urls"

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

DATABASES: Final[dict] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD: Final[str] = "django.db.models.BigAutoField"

EMAIL_BACKEND: str = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST: str = os.getenv("EMAIL_HOST", "")
EMAIL_PORT: int = 587
EMAIL_USE_TLS: bool = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER: str = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD: str = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL: str = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

CKEDITOR_CONFIGS: Final[dict[str, dict]] = {
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

HTML_MINIFY: Final[bool] = True
EXCLUDE_FROM_MINIFYING: tuple[str, ...] = ("/admin/", "/api/")
KEEP_COMMENTS_ON_MINIFYING = False
