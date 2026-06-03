"""
ASGI config for agendate_narino project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agendate_narino.settings')
application = get_asgi_application()
