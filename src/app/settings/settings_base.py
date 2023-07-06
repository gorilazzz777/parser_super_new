import os
from pathlib import Path

from celery.schedules import crontab


BASE_DIR = str(Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent)

SECRET_KEY = os.getenv('APP_KEY')

# Application definition

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'crispy_forms',
    'celery',


    'parser',
    'tariff_guide',
    'location',

    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'parser.middleware.GetMenuDataMiddleware'
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates'],
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

JAZZMIN_SETTINGS = {
    "site_title": "Парсер",
    "site_header": "Парсер",
    "site_brand": "Парсер",
    "site_logo": "parser/img/logo.png",
    "login_logo": "parser/img/login_logo.png",
    "site_icon":"parser/img/icon_logo.png",
    "welcome_sign": "Авторизация",
    "copyright": "Boxberry Parser",
    "usermenu_links": [
        {"name": "Поддержка", "url": "https://jira.boxberry.ru/projects/LKP/", "new_window": True},
        {"model": "auth.user"}
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "order_with_respect_to": ["parser"],
    "icons": {
        "parser": "fas fa-envelope",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "parser.message": "fas fa-comments",
        "parser.push": "fas fa-mobile",
        "parser.messagetemplate": "fas fa-layer-group",
        "parser.service": "fas fa-sitemap",
        "parser.providersettings": "fas fa-wrench",
        "parser.sendtype": "fas fa-comment-dots",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": "parser/css/main.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "custom_links": {
        "parser": [{
            "name": "Отчеты",
            "url": "reports",
            "icon": "fas fa-comments",
            # "permissions": ["location.city"]
        }]
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": True,
    "brand_colour": False,
    "accent": "accent-teal",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "materia",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True,
}

WSGI_APPLICATION = 'app.wsgi.application'

REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.TokenAuthentication',
   ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser'
   ),
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CELERY_BEAT_SCHEDULE = {
#     'update-tariffs': {
#         'task': 'app.tasks.update_tariffs',
#         'schedule': crontab(minute=0),
#     },
#     'update-report-pip': {
#         'task': 'app.tasks.create_report_pip',
#         'schedule': crontab(hour=7, minute=30),
#     },
#     'update-report-im': {
#         'task': 'app.tasks.create_report_im',
#         'schedule': crontab(hour=7, minute=30),
#     },
#     'heart-beat': {
#         'task': 'app.tasks.beat',
#         'schedule': crontab(),
#     },
# }


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

CELERY_BROKER_URL = 'redis://:boxberrypasswOrd12@redis:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 90 * 60

STATIC_ROOT = './static/'
MEDIA_ROOT = './media/'


LOG_PATH = BASE_DIR + 'log_viewer/log/app.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(levelname)s] [%(asctime)s] [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_PATH,
            'when': 'D', # this specifies the interval
            'interval': 1, # defaults to 1, only necessary for other values
            'backupCount': 10, # how many backup file to keep, 10 days
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['django_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}

MAIL_ADDR_FROM = "gorilazzz777@gmail.com"
MAIL_PASSWORD = "bcvsosndfldqcwlc"
MAIL_MSG_SUBJ = "Данные по ценам доставки конкурентов"
MAIL_MSG_TEXT = "Добрый день!\nДанные во вложении."

MA_TOKEN = os.getenv('MA_TOKEN')
MA_URL = os.getenv('MA_URL')
LKP_API_URL = os.getenv('LKP_API_URL')
LKP_API_STANDARD_TOKEN = os.getenv('LKP_API_STANDARD_TOKEN')

BILLING_URL = os.getenv('BILLING_URL')
BILLING_CLIENT_ID = os.getenv('BILLING_CLIENT_ID')

POCHTA_API_URL = os.getenv('POCHTA_API_URL')

BOXBERRY_BILLING_URL = os.getenv('BOXBERRY_BILLING_URL')
BOXBERRY_BILLING_CLIENT_ID = os.getenv('BOXBERRY_BILLING_CLIENT_ID')

DPD_API_URL_GEO = os.getenv('DPD_API_URL_GEO')
DPD_API_URL_CALC = os.getenv('DPD_API_URL_CALC')
DPD_CLIENT_NUMBER = os.getenv('DPD_CLIENT_NUMBER')
DPD_CLIENT_KEY = os.getenv('DPD_CLIENT_KEY')


YANDEX_MAPS_API_KEY = os.getenv('YANDEX_MAPS_API_KEY')

FIVE_POST_API_URL = os.getenv('FIVE_POST_API_URL')

SBERLOGISTIC_CALC_URL_IM = os.getenv('SBERLOGISTIC_CALC_URL_IM')
SBERLOGISTIC_CALC_URL_PIP = os.getenv('SBERLOGISTIC_CALC_URL_PIP')
SBERLOGISTIC_GET_POINT_URL = os.getenv('SBERLOGISTIC_GET_POINT_URL')

CDEK_BOX_URL = os.getenv('CDEK_BOX_URL')
CDEK_BOX_COST_URL = os.getenv('CDEK_BOX_COST_URL')
CDEK_URL_FOR_CITY_UUID = os.getenv('CDEK_URL_FOR_CITY_UUID')

S3_BUCKET = os.getenv('S3_BUCKET')
S3_SERVICE_NAME = os.getenv('S3_SERVICE_NAME')
S3_URL = os.getenv('S3_URL')
S3_REGION = os.getenv('S3_REGION')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_ACCESS_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
AWS_QUEUE_URL = os.getenv('AWS_QUEUE_URL')
YANDEX_ACCESS_KEY = os.getenv('YANDEX_ACCESS_KEY')
YANDEX_SECRET_KEY = os.getenv('YANDEX_SECRET_KEY')
PRICES_QUEUE = os.getenv('PRICES_QUEUE')

PATH_TO_TEMPLATES_REPORTS = BASE_DIR + '/parser/reports/templates/'
PATH_TO_RESULT_REPORTS = BASE_DIR + '/parser/reports/result_files/'
