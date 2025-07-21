from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from rest_framework.exceptions import PermissionDenied


class UserChatRoomListView(generics.ListAPIView):
    """
    لیست چت‌روم‌های کاربر لاگین کرده
    """
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(customer=self.request.user)


class ChatMessageListCreateView(generics.ListCreateAPIView):
    """
    لیست و ایجاد پیام‌ها در یک چت‌روم خاص
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        room = ChatRoom.objects.filter(id=room_id).first()
        if not room or room.customer != self.request.user:
            raise PermissionDenied("شما اجازه دسترسی به این چت را ندارید.")
        return ChatMessage.objects.filter(room=room).order_by('timestamp')

    def perform_create(self, serializer):
        room_id = self.kwargs['room_id']
        room = ChatRoom.objects.filter(id=room_id).first()
        if not room or room.customer != self.request.user:
            raise PermissionDenied("شما اجازه ارسال پیام در این چت را ندارید.")
        serializer.save(sender=self.request.user, room=room)
