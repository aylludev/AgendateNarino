"""
ASGI config for agendate_narino project.
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agendate_narino.settings')

django_asgi = get_asgi_application()

from messaging.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})