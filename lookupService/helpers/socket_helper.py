from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def announce_status_change(job_object, progress=''):
    layer = get_channel_layer('default')
    str_id = str(job_object.id)

    async_to_sync(layer.group_send)(
        str_id,
        {'type': 'status.update',
         'status': job_object.status,
         'progress': progress}
    )