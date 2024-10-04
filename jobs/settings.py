from pathlib import Path
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, "secrets.json"), "r") as f:
    SECRETS = json.load(f)
SECRET_KEY = SECRETS.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = SECRETS.get("DEBUG", True)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # Local Apps put here to handel password change and password reset templates correctly
    "accounts.apps.AccountsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local Apps
    "core.apps.CoreConfig",
    "posts.apps.PostsConfig",
    "profiles.apps.ProfilesConfig",
    "applications.apps.ApplicationsConfig",
    # 3d party apps
    "crispy_forms",
    "crispy_bootstrap5",
    "ckeditor",
    "django_select2",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "jobs.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "jobs.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql",
        # "NAME": SECRETS.get("DB_NAME", "jobs_portal"),
        # "USER": SECRETS.get("DB_USER", ""),
        # "HOST": SECRETS.get("DB_HOST"),
        # "PASSWORD": SECRETS.get("DB_PASSWORD", ""),
        # "PORT": SECRETS.get("DB_PORT"),
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# AUTHENTICATION CONFIGS
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "job_list"
LOGOUT_URL = "logout"
LOGOUT_REDIRECT_URL = "job_list"


# settings for letting users logged in with email
AUTHENTICATION_BACKENDS = [
    "accounts.authentication.EmailAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# Crispy forms settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ckeditor settings
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
        "extraPlugins": ",".join(
            [
                # 'codesnippet',
                "widget",
                "dialog",
            ]
        ),
    },
}

if DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        pass

    else:
        INSTALLED_APPS.append("debug_toolbar")
        INTERNAL_IPS = ["127.0.0.1"]
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        )
