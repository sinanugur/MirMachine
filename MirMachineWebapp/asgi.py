"""
ASGI config for MirMachineWebapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MirMachineWebapp.settings')
django_asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import lookupService.urls
import django

django.setup()
application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            lookupService.urls.websocket_patterns
        )
    )
})
