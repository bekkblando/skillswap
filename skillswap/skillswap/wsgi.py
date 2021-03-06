"""
WSGI config for skillswap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillswap.settings")

application = get_wsgi_application()
