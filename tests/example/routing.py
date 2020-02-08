from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from tests.example import consumer

websocket_urlpatterns = [
    re_path(r'^ws/cable/$', consumer.TestConsumer),
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumer.ChatConsumer),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': SessionMiddlewareStack(  # AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
