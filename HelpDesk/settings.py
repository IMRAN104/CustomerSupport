from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e&6j(zio9ib*7-uj4*rpcxmq_cb97$(_&pb323s*7hmmlijs$r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'debug_toolbar',
    #'ecom',
    'Main',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
]

INTERNAL_IPS = [
    '127.0.0.1'
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True
}
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 18000
SESSION_SAVE_EVERY_REQUEST = True


ROOT_URLCONF = 'HelpDesk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'Templates')],
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

WSGI_APPLICATION = 'HelpDesk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ]
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), ) 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#FS_IMAGE_UPLOADS = os.path.join(MEDIA_ROOT,'item_pics/')
#FS_IMAGE_URL = os.path.join(MEDIA_URL,'item_pics/')

FS_ECOM_ITEM_THUMBNAIL_UPLOADS = os.path.join(MEDIA_ROOT,'item_card_image/')
FS_ECOM_ITEM_THUMBNAIL_URL = os.path.join(MEDIA_URL,'item_card_image/')

FS_ECOM_ITEM_IMAGE_UPLOADS = os.path.join(MEDIA_ROOT,'ecom_item_image/')
FS_ECOM_ITEM_IMAGE_URL = os.path.join(MEDIA_URL,'ecom_item_image/')

LOGIN_REDIRECT_URL='/userauth/home/'
LOGIN_URL = 'loginpage'

#* For Email Sending
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.netdefense.com.bd'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'poserp@netdefense.com.bd'
EMAIL_HOST_PASSWORD = 'poserp@123'

CSRF_COOKIE_SECURE  = False

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BEn5ZzZC1GE0ZspGIjYjhX0e41Cq7SF5uKL7HpWlOd3hYyivefIHrSCmcuaiXgDPSAShhWbjUg0-cn_fmU13luQ",
    "VAPID_PRIVATE_KEY":"KLl2QCvWXuTLqHm-EveeV1Fp3NPVW5VZTnNjXWEjqk4",
    "VAPID_ADMIN_EMAIL": "narmiemon@gmail.com"
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
