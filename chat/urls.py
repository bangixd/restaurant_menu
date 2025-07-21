from django.urls import path
from .views import UserChatRoomListView, ChatMessageListCreateView

urlpatterns = [
    path('rooms/', UserChatRoomListView.as_view(), name='user-chat-rooms'),
    path('rooms/<int:room_id>/messages/', ChatMessageListCreateView.as_view(), name='chat-room-messages'),
]
