from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers


def announce_status_change(job_object, progress=''):
    str_id = str(job_object.id)
    message = {'type': 'status.update',
               'status': job_object.status,
               'progress': progress}
    announce_message(message, str_id)


def announce_queue_position(job_object, queue_pos):
    str_id = str(job_object.id)
    message = {'type': 'queue.update',
               'queue_pos': queue_pos}
    announce_message(message, str_id)


def announce_message(message, _id):
    layer = get_channel_layer('default')
    async_to_sync(layer.group_send)(
        _id,
        message
    )


def announce_initiation(job_object):
    str_id = str(job_object.id)
    time = serializers.DateTimeField().to_representation(job_object.initiated)
    message = {'type': 'initiation',
               'time': time}
    announce_message(message, str_id)


def announce_completed(job_object):
    str_id = str(job_object.id)
    time = serializers.DateTimeField().to_representation(job_object.completed)
    message = {'type': 'completed',
               'time': time}
    announce_message(message, str_id)
