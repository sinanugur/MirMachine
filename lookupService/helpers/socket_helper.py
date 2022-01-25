from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers
from websocket import create_connection
import math


current_job = None

def announce_status_change(job_object):
    str_id = job_object.species
    message = {'type': 'status.update',
               'status': job_object.status}
    announce_message(message, str_id)


def announce_changed_model(job_object):
    message = {'type': 'model.change'}
    announce_message(message, job_object.species)


def announce_progress(species, progress):
    ws = create_connection('ws://127.0.0.1:8000/ws/job/{species}'.format(species=species))
    ws.send(progress)
    ws.close()


def announce_queue_position(job_object, queue_pos):
    str_id = str(job_object.species)
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
    str_id = str(job_object.species)
    time = serializers.DateTimeField().to_representation(job_object.initiated)
    message = {'type': 'initiation',
               'time': time}
    announce_message(message, str_id)


def announce_completed(job_object):
    str_id = str(job_object.species)
    time = serializers.DateTimeField().to_representation(job_object.completed)
    message = {'type': 'completed',
               'time': time}
    announce_message(message, str_id)


def log_handler(msg):
    global current_job
    if current_job is None:
        if msg.get('level') == 'job_info':
            print(msg)
            wildcards = msg['wildcards']
            if 'species' not in wildcards:
                return
            species = wildcards['species']
            current_job = species
    if msg.get('level') == 'progress':
        print(msg)
        cur = msg['done']
        total = msg['total']
        interval = math.ceil(total/20)
        if cur % interval == 0:
            progress = '{cur} of {total} steps ({percent}%) done'.format(cur=cur, total=total, percent=int((cur/total)*100))
            announce_progress(current_job, progress)