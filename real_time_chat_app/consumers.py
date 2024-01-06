import json
from django.core.serializers import serialize
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = 'new_group'
        await self.accept()
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        message = text_data_json["message"]
        user = text_data_json["user"]
        get_user = self.scope["user"]
        create_message = await sync_to_async(UserMessages.objects.create)(user=get_user,message=message)
        await sync_to_async(create_message.save)()
        latest = await sync_to_async(UserMessages.objects.latest)('id')
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type":"sendMessage",
                "message":latest,
                "username":user
            }
        )
    async def sendMessage(self,event):
        message=event["message"]
        username=event["username"]
        serialize_data = serialize('json',[message])
        await self.send(text_data=json.dumps(
            {
                "username":username,
                "message":serialize_data
            }
        ))