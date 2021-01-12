from django.urls import re_path
try:
    from django.core.asgi import get_asgi_application
except ImportError:
    from channels.routing import get_default_application as get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from sockpuppet.consumer import SockpuppetConsumer

socket_patterns = [re_path(r'ws/sockpuppet-sync', SockpuppetConsumer.as_asgi())]

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(socket_patterns),
    ),
})
