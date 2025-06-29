import os
from pathlib import Path

from dotenv import load_dotenv

from .logger import setup_logger

logger = setup_logger(log_file="settings.log")

# Load environment variables from .env file
load_dotenv()

DEBUG = os.getenv("DEBUG", "True") == "True"

logger.info(f"Debug is {DEBUG}")

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = 587
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-ojp6ewm9ue68@xmo*gau5fka4o*1o8p91n)9!8wxjm@tue=yly"
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
    # "django_minify_html",
    "main",
]
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "main.middleware.CustomErrorMiddleware",

    # "htmlmin.middleware.HtmlMinifyMiddleware",
    # "htmlmin.middleware.MarkRequestMiddleware", # (кеширование)
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
HTML_MINIFY = True
EXCLUDE_FROM_MINIFYING = ("/admin/", "/api/")
KEEP_COMMENTS_ON_MINIFYING = False

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
            ],
        },
    },
]

CKEDITOR_CONFIGS = {
    "default": {
        "contentsCss": "/static/css/ckeditor-content.css",
        "bodyClass": "article-content",  # Добавляем класс к body редактора
        "allowedContent": True,  # Разрешаем классы и стили
        "extraPlugins": "stylesheetparser",
        "toolbar_Full": [
            ["Styles", "Format", "Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList", "Blockquote"],
            ["Image", "Table", "Link"],
            ["Source"],  # Кнопка просмотра HTML
        ],
    },
}

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

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
