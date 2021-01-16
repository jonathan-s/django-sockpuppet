from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import channels

channels_version = channels.__version__.split('.')[0]
if int(channels_version) >= 3:
    from sockpuppet.consumer import SockpuppetConsumerAsgi as SockpuppetConsumer
    socket_patterns = [
        re_path(r'ws/sockpuppet-sync', SockpuppetConsumer.as_asgi())
    ]

    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(socket_patterns)
        ),
    })
else:
    from sockpuppet.consumer import SockpuppetConsumer
    socket_patterns = [re_path(r'ws/sockpuppet-sync', SockpuppetConsumer)]

    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(socket_patterns)
        ),
    })
