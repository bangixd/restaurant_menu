from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    """
    برای تفکیک چت‌ها بین کاربر و پشتیبانی یا صاحب رستوران
    """
    ROOM_TYPE_CHOICES = [
        ('support', 'پشتیبانی'),
        ('owner', 'صاحب رستوران'),
    ]
    customer = models.ForeignKey(User, related_name='customer_chats', on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, related_name='target_chats', on_delete=models.CASCADE, null=True, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer} -> {self.room_type}'

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.sender} at {self.timestamp}'
