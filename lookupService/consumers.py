from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Job
from rest_framework import serializers
import json


class MonitorConsumer(WebsocketConsumer):
    def connect(self):
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
        job = Job.objects.get(id=self._id)
        self.send(text_data=json.dumps({
            'type': 'status',
            'status': job.status,
            'progress': '0 steps (0%) done'
        }))
        queued = Job.objects.filter(status='queued')
        for i in range(len(queued)):
            if queued[i].id == job.id:
                self.send(text_data=json.dumps({
                    'type': 'queue',
                    'queuePos': i+1
                }))

    def status_update(self, event):
        status = event['status']
        self.send(text_data=json.dumps({
            'type': 'status',
            'status': status,
            'progress': event['progress']
        }))

    def queue_update(self, event):
        self.send(text_data=json.dumps({
            'type': 'queue',
            'queuePos': event['queue_pos']
        }))

    def initiation(self, event):
        str_rep = serializers.DateTimeField().to_representation(event['time'])
        self.send(text_data=json.dumps({
            'type': 'initiation',
            'time': str_rep
        }))

    def completed(self, event):
        str_rep = serializers.DateTimeField().to_representation(event['time'])
        self.send(text_data=json.dumps({
            'type': 'completed',
            'time': str_rep
        }))
