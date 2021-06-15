"""
WSGI config for weatherdep project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append(os.getcwd())

# Nazwa modułu z ustawieniami
os.environ['DJANGO_SETTINGS_MODULE'] = "weatherdep.settings.production"


application = get_wsgi_application()
