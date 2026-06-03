"""
WSGI config for agendate_narino project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agendate_narino.settings')
application = get_wsgi_application()
