"""
WSGI config for weatherdep project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import sys, os
sys.path.append(os.getcwd())

os.environ['DJANGO_SETTINGS_MODULE'] = "weatherdep.settings.production"  # Nazwa modułu z ustawieniami

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
