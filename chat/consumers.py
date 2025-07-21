from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.target = self.scope['url_route']['kwargs']['target']
        self.user = self.scope['user']

        self.room = await self.get_or_create_room()

        self.room_group_name = f"chat_{self.room.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.full_name or self.user.phone
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async
    def get_or_create_room(self):
        if self.target == "support":
            return ChatRoom.objects.get_or_create(customer=self.user, room_type="support")[0]
        elif self.target == "owner":
            # باید بر اساس منوی فعال، صاحب رستوران رو پیدا کنیم
            owner = User.objects.filter(role="owner").first()  # بهینه‌ترش هم میشه کرد
            return ChatRoom.objects.get_or_create(customer=self.user, target_user=owner, room_type="owner")[0]

    @database_sync_to_async
    def save_message(self, message):
        return ChatMessage.objects.create(
            room=self.room,
            sender=self.user,
            message=message
        )
