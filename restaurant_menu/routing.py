from django.urls import path
from ..chat import consumers

websocket_urlpatterns = [
    path("ws/chat/<str:target>/", consumers.ChatConsumer.as_asgi()),
]
