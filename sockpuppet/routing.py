from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from sockpuppet.consumer import SockpuppetConsumer

socket_patterns = [re_path(r'websocket', SockpuppetConsumer)]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(socket_patterns)
    ),
})
