"""
ASGI config for announcer project.

Exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import broadcaster.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'announcer.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(broadcaster.routing.websocket_urlpatterns)
    ),
})