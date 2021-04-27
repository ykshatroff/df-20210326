from settings.local import *


SEND_EMAILS = False


DATABASES["default"]["TEST"] = {
    "NAME": "df_20210326_test",
}

DATABASES["default"] = {
    "TEST": {
        "NAME": "df_20210326_test",
    },
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': 'postgres',
    'NAME': 'testuser',
    'USER': 'testuser',
    'PASSWORD': 'testpassword',
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Use session in tests to make api login easier
REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
    "rest_framework.authentication.SessionAuthentication",
)

