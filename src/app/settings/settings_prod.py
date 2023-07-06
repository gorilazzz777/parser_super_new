# SECURITY WARNING: don't run with debug turned on in production!
import os

DEBUG = True

ALLOWED_HOSTS = ['web']

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
            'filename': '/var/log/app/app.log',
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

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': "[%(levelname)s] [%(asctime)s] [%(name)s:%(lineno)s] %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'django_file': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'app': {
#             'handlers': ['django_file'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
#         }
#     },
# }