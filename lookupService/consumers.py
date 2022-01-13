from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Job
from rest_framework import serializers
import json


class MonitorConsumer(WebsocketConsumer):
    def connect(self):
        self.species = self.scope['url_route']['kwargs']['species']
        if Job.objects.filter(species=self.species).exists():
            async_to_sync(self.channel_layer.group_add)(
                self.species,
                self.channel_name
            )
            self.accept()
        # print('Connection refused due to non-existent db entry')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.species,
            self.channel_name
        )

    def receive(self, text_data):
        print(text_data)
        if text_data == 'request status':
            job = Job.objects.get(species=self.species)
            self.send(text_data=json.dumps({
                'type': 'status',
                'status': job.status
            }))
            queued = Job.objects.filter(status='queued')
            for i in range(len(queued)):
                if queued[i].species == job.species:
                    self.send(text_data=json.dumps({
                        'type': 'queue',
                        'queuePos': i+1
                    }))
        elif text_data.endswith('done'):
            async_to_sync(self.channel_layer.group_send)(
                self.species,
                {
                    'type': 'progress.update',
                    'progress': text_data
                }
            )


    def status_update(self, event):
        status = event['status']
        self.send(text_data=json.dumps({
            'type': 'status',
            'status': status,
        }))

    def progress_update(self, event):
        self.send(text_data=json.dumps({
            'type': 'progress',
            'progress': event['progress']
        }))

    def queue_update(self, event):
        self.send(text_data=json.dumps({
            'type': 'queue',
            'queuePos': event['queue_pos']
        }))

    def initiation(self, event):
        self.send(text_data=json.dumps({
            'type': 'initiation',
            'time': event['time']
        }))

    def completed(self, event):
        self.send(text_data=json.dumps({
            'type': 'completed',
            'time': event['time']
        }))

    def model_change(self, event):
        self.send(text_data=json.dumps(({
            'type': 'model_change'
        })))
