from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from movies import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/seats/(?P<show_id>\d+)/$', consumers.SeatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
