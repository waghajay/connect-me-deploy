# """
# ASGI config for ConnectMe project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter,URLRouter

# import chat.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ConnectMe.settings')


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     )
# })



"""
ASGI config for ConnectMe project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Ensure DJANGO_SETTINGS_MODULE is set correctly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ConnectMe.settings')

# Initialize Django settings before accessing them
django_asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import call.routing

application = ProtocolTypeRouter({
    "http": django_asgi_application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            call.routing.websocket_urlpatterns
        )
    ),
})

