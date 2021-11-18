"""
ASGI config for MirMachineWebapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application

django_asgi_application = get_asgi_application()

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import lookupService.urls
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MirMachineWebapp.settings')
django.setup()
application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            lookupService.urls.websocket_patterns
        )
    )
})
