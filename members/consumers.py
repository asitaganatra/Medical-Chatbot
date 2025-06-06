from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TrainingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("nlp_training", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("nlp_training", self.channel_name)

    async def training_complete(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))