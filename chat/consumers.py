import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from chat.models import Room, Message
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import base64

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
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
        message = data.get('message')
        username = data.get('username')
        room = data.get('room')
        image_data = data.get('data')  # Change 'image_data' to 'data'

        await self.save_message(username, room, message, image_data)

        if message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'room': room,
                }
            )
        elif image_data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_image',
                    'image_data': image_data,
                    'username': username,
                    'room': room,
                }
            )
        
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    async def chat_image(self, event):
        image_data = event['image_data']
        username = event['username']
        room = event['room']
        await self.send(text_data=json.dumps({
            'image_data': image_data,
            'username': username,
            'room': room,
            'type': 'image',
        }))
        
    @sync_to_async
    def save_message(self, username, room, message, image_data):
        if username:
            user = User.objects.get(username=username)
        else:
            user = None
        room = Room.objects.get(name=room)
        if message:
            Message.objects.create(user=user, room=room, content=message)
        elif image_data:
            # Decode base64 image data
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = ContentFile(base64.b64decode(imgstr), name=f'image_{user.username}.{ext}')
            Message.objects.create(user=user, room=room, content="Image Message" , image=image_data)
