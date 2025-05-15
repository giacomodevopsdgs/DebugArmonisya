import os
import sys
import tempfile
from pathlib import Path
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

from django.conf import settings


########################################################################################################################
# Django init (Client)
########################################################################################################################

sys.path.append(str(Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
settings.DISABLE_AUTHENTICATION = True
settings.DEBUG = False

settings.DATABASES = {
}
settings.CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(tempfile.mkdtemp(), "django_cache"),
    }
}
settings.REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '600/minute',
        'user': '600/minute'
    }
}
settings.LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/secops-client/client.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
settings.CACHE_ENABLE = False

disable_warnings(InsecureRequestWarning)
