from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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
    message = {'type': 'initiation',
               'time': job_object.initiated}
    announce_message(message, str_id)


def announce_completed(job_object):
    str_id = str(job_object.id)
    message = {'type': 'completed',
               'time': job_object.completed}
    announce_message(message, str_id)
