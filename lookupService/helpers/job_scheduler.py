from ..models import Job
from engine.scripts.mirmachine_args import run_mirmachine
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def schedule_job():
    ongoing = Job.objects.filter(status='ongoing')
    if ongoing.exists():
        return
    queued = Job.objects.filter(status='queued').order_by('initiated')
    # could check if none are returned, but this should never happen
    next_in_line = queued[0]
    next_in_line.status = 'ongoing'
    next_in_line.save()

    process, job_object = run_mirmachine(next_in_line)
    handle_job_end(process, job_object)


def handle_job_end(process, job_object):
    if process.returncode != 0:
        job_object.status = 'halted'
    else:
        job_object.status = 'completed'
    job_object.save()
    layer = get_channel_layer('default')
    str_id = str(job_object.id)
    print(str_id)
    print(job_object.status)
    async_to_sync(layer.group_send)(
        str_id,
        {'type': 'status.update', 'status': job_object.status}
    )

