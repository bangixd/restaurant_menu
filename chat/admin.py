from django.contrib import admin
from .models import ChatRoom, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['sender', 'message', 'timestamp']

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'room_type', 'created_at']
    inlines = [ChatMessageInline]
