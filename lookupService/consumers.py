from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Job
import json


class MonitorConsumer(WebsocketConsumer):
    def connect(self):
        print('inside connection method')
        self._id = self.scope['url_route']['kwargs']['_id']
        if Job.objects.filter(id=self._id).exists():
            async_to_sync(self.channel_layer.group_add)(
                self._id,
                self.channel_name
            )
        self.accept()
        # print('Connection refused due to non-existent db entry')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self._id,
            self.channel_name
        )

    def receive(self, text_data):
        print(text_data)
        # mostly used for debugging
        # just echoes the transmitted data
        #text_data_json = json.loads(text_data)
        #message = text_data_json['message']
        #self.send(text_data=json.dumps({
        #    'message': message
        #}))

    def status_update(self, event):
        status = event['status']
        self.send(text_data=json.dumps({
            'status': status
        }))
