from rest_framework import serializers
from .models import ChatRoom, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'sender_name', 'message', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp', 'sender_name']


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'customer', 'target_user', 'room_type', 'created_at']
        read_only_fields = ['id', 'customer', 'created_at']
